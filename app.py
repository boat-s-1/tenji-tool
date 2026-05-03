import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE", layout="centered")

# -------------------------
# カラー
# -------------------------
COLORS = [
    (255,255,255),
    (80,80,80),
    (0,0,255),
    (255,0,0),
    (0,255,255),
    (0,255,0)
]

# -------------------------
# 初期状態
# -------------------------
if "lock_all" not in st.session_state:
    st.session_state.lock_all = False

if "locks" not in st.session_state:
    st.session_state.locks = [False]*6

# -------------------------
# フレーム取得（軽量）
# -------------------------
@st.cache_data
def get_frame_image(video_path, frame_idx, width=240):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()

    if ret:
        h, w, _ = frame.shape
        scale = width / w
        return cv2.resize(frame, (width, int(h * scale)))
    return None

# -------------------------
# 動画生成
# -------------------------
def create_overlay(video_path, start_times, use_flags, duration_sec, ghost_decay=0.85):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    scale = 0.5
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    total_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    ghost = np.zeros((height, width, 3), dtype=np.float32)

    for i in range(total_frames):
        max_frame = np.zeros((height, width, 3), dtype=np.uint8)

        for idx, t in enumerate(start_times):
            if not use_flags[idx]:
                continue

            cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps) + i)
            ret, frame = cap.read()

            if ret:
                frame = cv2.resize(frame, (width, height))
                color = COLORS[idx]

                colored = frame.astype(np.float32)
                for c in range(3):
                    colored[:,:,c] *= color[c] / 255.0

                max_frame = np.maximum(max_frame, colored.astype(np.uint8))

        ghost = ghost * ghost_decay + max_frame * (1 - ghost_decay)
        out.write(np.clip(ghost,0,255).astype(np.uint8))

        if i % 10 == 0:
            gc.collect()

    out.release()
    cap.release()
    return output_path

# -------------------------
# UI
# -------------------------
st.title("🚤 旋回比較ツール")

with st.expander("📖 使い方", expanded=True):
    st.markdown("""
① 動画アップ  
② 基準を合わせる  
③ 各艇を調整  
④ 生成  

▼見方  
前に出る → 行き足◎  
内に残る → ターン◎  
外に流れる → 弱い  
""")

file = st.file_uploader("動画をアップロード", type=["mp4","mov"])

if file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    st.video(video_path)

    # -------------------------
    # 基準設定
    # -------------------------
    st.markdown("## 🎯 基準を合わせる")

    base_frame = st.slider("再生位置（基準）", 0, total_frames, 0)

    img = get_frame_image(video_path, base_frame)
    if img is not None:
        st.image(img, caption=f"{base_frame/fps:.2f}秒")

    # -------------------------
    # 操作モード
    # -------------------------
    st.markdown("## 🎛 操作")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 全艇ロック"):
            st.session_state.lock_all = not st.session_state.lock_all

    with col2:
        if st.button("📋 全艇コピー"):
            for i in range(6):
                st.session_state[f"slider_{i}"] = base_frame

    st.info(f"全艇ロック：{'ON' if st.session_state.lock_all else 'OFF'}")

    # -------------------------
    # 各艇調整
    # -------------------------
    st.markdown("## ⚙️ 各艇調整")

    times = []
    use_flags = []

    for i in range(6):
        st.markdown(f"### {i+1}号艇")

        lock = st.checkbox("固定", value=st.session_state.locks[i], key=f"lock_{i}")
        st.session_state.locks[i] = lock

        if st.session_state.lock_all:
            current = base_frame
        else:
            current = st.session_state.get(f"slider_{i}", base_frame)

        frame_idx = st.slider(
            f"{i+1}号艇 位置",
            0,
            total_frames,
            current,
            key=f"slider_{i}"
        )

        # 全艇連動
        if st.session_state.lock_all:
            for j in range(6):
                if not st.session_state.locks[j]:
                    st.session_state[f"slider_{j}"] = frame_idx

        img = get_frame_image(video_path, frame_idx)
        if img is not None:
            st.image(img, caption="ここでOK？")

        if st.button("👉 決定", key=f"set_{i}"):
            st.session_state[f"slider_{i}"] = frame_idx

        st.caption(f"{frame_idx/fps:.2f}秒")

        use = st.toggle("使用", True, key=f"use_{i}")

        times.append(frame_idx / fps)
        use_flags.append(use)

        st.divider()

    # -------------------------
    # 生成
    # -------------------------
    st.markdown("## 🎬 生成")

    duration = st.slider("秒数", 1.0, 8.0, 4.0)
    ghost = st.slider("残像", 0.7, 0.95, 0.85)

    if st.button("🚀 生成", use_container_width=True):
        with st.spinner("処理中..."):
            res = create_overlay(video_path, times, use_flags, duration, ghost)

            st.success("完成！")
            st.video(res)

            with open(res, "rb") as f:
                st.download_button("⬇ 保存", f, "boat_strike.mp4", use_container_width=True)

    os.remove(video_path)
