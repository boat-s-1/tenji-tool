import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE", layout="centered")

# ボートレースの艇旗色に合わせた色設定（BGR形式）
COLORS = [
    (255, 255, 255), # 1:白
    (50, 50, 50),    # 2:黒
    (0, 0, 255),     # 3:赤
    (255, 0, 0),     # 4:青
    (0, 255, 255),   # 5:黄
    (0, 255, 0)      # 6:緑
]

# --- 初期化 ---
if "locks" not in st.session_state:
    st.session_state.locks = [False] * 6
if "lock_all" not in st.session_state:
    st.session_state.lock_all = False

# 各スライダーの初期値を設定
for i in range(6):
    if f"slider_{i}" not in st.session_state:
        st.session_state[f"slider_{i}"] = 0

# --- フレーム取得（プレビュー用） ---
@st.cache_data
def get_frame_image(video_path, frame_idx, width=400):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()
    if ret:
        h, w, _ = frame.shape
        scale = width / w
        return cv2.resize(frame, (width, int(h * scale)))
    return None

# --- 動画生成（ここを大幅修正） ---
def create_overlay(video_path, start_frames, use_flags, duration_sec, ghost_decay=0.85):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    scale = 0.5 # 負荷軽減
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    total_output_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    # ブラウザ再生用にavc1(H.264)を試行、ダメならmp4v
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for i in range(total_output_frames):
        # フレームごとの合成用ベース（float32で計算）
        frame_acc = np.zeros((height, width, 3), dtype=np.float32)
        active_count = 0

        for idx, base_f in enumerate(start_frames):
            if not use_flags[idx]:
                continue
            
            # 各艇の「現在のフレーム」を計算
            current_f = int(base_f + i)
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_f)
            ret, frame = cap.read()

            if ret:
                frame_res = cv2.resize(frame, (width, height))
                # 各艇の色味を少し強調（オプション）
                f_float = frame_res.astype(np.float32)
                frame_acc += f_float
                active_count += 1
        
        if active_count > 0:
            # 平均化合成（これで重なりが自然になります）
            res_frame = (frame_acc / active_count).astype(np.uint8)
            out.write(res_frame)
        else:
            out.write(np.zeros((height, width, 3), dtype=np.uint8))

        if i % 15 == 0:
            gc.collect()

    out.release()
    cap.release()
    return output_path

# --- UI ---
st.title("🚤 BOAT STRIKE - 旋回精密比較")

file = st.file_uploader("動画をアップロード (iPhone画面録画OK)", type=["mp4","mov"])

if file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mov')
    tfile.write(file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    st.video(video_path)

    st.divider()
    
    # 基準設定
    col_ctrl = st.columns(2)
    with col_ctrl[0]:
        base_frame = st.slider("基準位置（まとめて動かす用）", 0, total_frames, 0)
        if st.button("📋 全艇を基準位置に合わせる"):
            for i in range(6):
                st.session_state[f"slider_{i}"] = base_frame
            st.rerun()

    with col_ctrl[1]:
        st.session_state.lock_all = st.toggle("全艇シンクロモード", value=st.session_state.lock_all)
        st.caption("ONにすると、どれか一つのスライダーを動かすと全員動きます")

    st.divider()

    # 各艇の設定
    times_f = []
    use_flags = []

    for i in range(6):
        with st.expander(f"{i+1}号艇の設定", expanded=True):
            c1, c2 = st.columns([2, 1])
            
            with c2:
                use = st.toggle("使用する", True, key=f"use_{i}")
                use_flags.append(use)
                lock = st.checkbox("この艇を固定", key=f"lock_{i}")
            
            with c1:
                # スライダー
                current_val = st.session_state[f"slider_{i}"]
                frame_idx = st.slider(f"開始フレーム", 0, total_frames, current_val, key=f"s_{i}")
                
                # シンクロ処理
                if st.session_state.lock_all and not lock:
                    if frame_idx != current_val: # 値が動いた場合
                        diff = frame_idx - current_val
                        for j in range(6):
                            if j != i: st.session_state[f"slider_{j}"] += diff
                        st.session_state[f"slider_{i}"] = frame_idx
                        st.rerun()
                else:
                    st.session_state[f"slider_{i}"] = frame_idx

                times_f.append(frame_idx)
                
                # プレビュー
                img = get_frame_image(video_path, frame_idx)
                if img is not None:
                    st.image(img, caption=f"開始地点: {frame_idx/fps:.2f}秒")

    st.divider()

    # 生成設定
    col_fin = st.columns(2)
    with col_fin[0]:
        duration = st.slider("合成する長さ（秒）", 1.0, 10.0, 5.0)
    with col_fin[1]:
        if st.button("🚀 比較動画を生成"):
            with st.spinner("各艇のタイミングを合わせて合成中..."):
                res = create_overlay(video_path, times_f, use_flags, duration)
                st.video(res)
                with open(res, "rb") as f:
                    st.download_button("動画を保存", f, "boat_comparison.mp4")

    # クリーンアップ
    # os.remove(video_path) # 必要に応じて有効化
