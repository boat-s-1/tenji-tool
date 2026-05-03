import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE - 完成版", layout="wide")

# 艇カラー
COLORS = [
    (255,255,255),  # 1
    (80,80,80),     # 2
    (0,0,255),      # 3
    (255,0,0),      # 4
    (0,255,255),    # 5
    (0,255,0)       # 6
]

def create_overlay_final(video_path, start_times, use_flags, duration_sec, alpha=0.6, ghost_decay=0.85):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30.0

    # 軽量化
    scale = 0.5
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    total_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # ゴースト
    ghost = np.zeros((height, width, 3), dtype=np.float32)

    for i in range(total_frames):

        max_frame = np.zeros((height, width, 3), dtype=np.uint8)

        for idx, t in enumerate(start_times):
            if not use_flags[idx] or t <= 0:
                continue

            target_frame = int(t * fps) + i
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()

            if ret:
                frame_res = cv2.resize(frame, (width, height))

                # 色付け（軽量）
                color = COLORS[idx]
                colored = frame_res.astype(np.float32)

                for c in range(3):
                    colored[:, :, c] *= (color[c] / 255.0)

                colored = colored.astype(np.uint8)

                # 最大値合成（差を残す）
                max_frame = np.maximum(max_frame, colored)

        # 残像
        ghost = ghost * ghost_decay + max_frame.astype(np.float32) * (1 - ghost_decay)

        out.write(np.clip(ghost, 0, 255).astype(np.uint8))

        if i % 10 == 0:
            gc.collect()

    out.release()
    cap.release()
    gc.collect()

    return output_path


# --- UI ---
st.title("🚤 BOAT STRIKE - 旋回比較ツール（完成版）")
st.markdown("6艇の機力差を“見える化”します")

uploaded_file = st.sidebar.file_uploader("動画アップロード", type=["mov", "mp4"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.subheader("① プレビュー")
    st.video(video_path)

    st.subheader("② 設定")

    st.info("ターンマーク通過の秒数を入力")

    cols = st.columns(3)
    times = []
    use_flags = []

    for i in range(6):
        with cols[i % 3]:
            use = st.checkbox(f"{i+1}号艇 使用", True)
            val = st.number_input(f"{i+1}号艇 秒", 0.0, 1000.0, 0.0, step=0.1, key=f"b{i}")
            use_flags.append(use)
            times.append(val)

    duration = st.slider("合成秒数", 1.0, 8.0, 4.0)
    alpha = st.slider("色の強さ", 0.3, 1.0, 0.6)
    ghost_decay = st.slider("残像の長さ", 0.7, 0.95, 0.85)

    if st.button("🚀 生成"):
        if sum(times) == 0:
            st.warning("秒数を入力してください")
        else:
            with st.spinner("処理中（軽量モード）"):
                try:
                    res = create_overlay_final(video_path, times, use_flags, duration, alpha, ghost_decay)

                    st.success("完成！")
                    st.video(res)

                    with open(res, "rb") as f:
                        st.download_button("ダウンロード", f, "boat_strike.mp4")

                except Exception as e:
                    st.error(f"エラー: {e}")

    os.remove(video_path)
