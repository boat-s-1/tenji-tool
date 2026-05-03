import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE", layout="centered")

COLORS = [
    (255,255,255),
    (80,80,80),
    (0,0,255),
    (255,0,0),
    (0,255,255),
    (0,255,0)
]

# -------------------------
# 初期化（重要）
# -------------------------
for i in range(6):
    if f"slider_{i}" not in st.session_state:
        st.session_state[f"slider_{i}"] = 0

if "lock_all" not in st.session_state:
    st.session_state.lock_all = False

if "locks" not in st.session_state:
    st.session_state.locks = [False]*6


# -------------------------
# フレーム取得
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
    # 基準
    # -------------------------
    base_frame = st.slider("基準位置", 0, total_frames, 0)

    if st.button("📋 全艇コピー"):
        for i in range(6):
            st.session_state[f"slider_{i}"] = base_frame

    if st.button("🔒 全艇ロック"):
        st.session_state.lock_all = not st.session_state.lock_all

    st.info(f"ロック：{'ON' if st.session_state.lock_all else 'OFF'}")

    # -------------------------
    # 各艇
    # -------------------------
    times = []
    use_flags = []

    for i in range(6):
        st.markdown(f"### {i+1}号艇")

        lock = st.checkbox("固定", value=st.session_state.locks[i], key=f"lock_{i}")
        st.session_state.locks[i] = lock

        frame_idx = st.slider(
            f"{i+1}号艇",
            0,
            total_frames,
            st.session_state[f"slider_{i}"],
            key=f"slider_{i}"
        )

        # ロック連動
        if st.session_state.lock_all:
            for j in range(6):
                if not st.session_state.locks[j]:
                    st.session_state[f"slider_{j}"] = frame_idx

        img = get_frame_image(video_path, frame_idx)
        if img is not None:
            st.image(img)

        st.caption(f"{frame_idx/fps:.2f}秒")

        use = st.toggle("使用", True, key=f"use_{i}")

        # ★ここが重要（修正）
        times.append(st.session_state[f"slider_{i}"] / fps)
        use_flags.append(use)

        st.divider()

    # -------------------------
    # 生成
    # -------------------------
    duration = st.slider("秒数", 1.0, 8.0, 4.0)
    ghost = st.slider("残像", 0.7, 0.95, 0.85)

    if st.button("🚀 生成"):
        with st.spinner("処理中..."):
            res = create_overlay(video_path, times, use_flags, duration, ghost)
            st.video(res)

            with open(res, "rb") as f:
                st.download_button("保存", f, "boat_strike.mp4")

    os.remove(video_path)
