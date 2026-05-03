import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE AI", layout="centered")

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
# 初期化
# -------------------------
for i in range(6):
    if f"slider_{i}" not in st.session_state:
        st.session_state[f"slider_{i}"] = 0

if "lock_all" not in st.session_state:
    st.session_state.lock_all = False

if "locks" not in st.session_state:
    st.session_state.locks = [False]*6


# -------------------------
# 軽量フレーム取得
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
# AIターン検出（軽量版）
# -------------------------
def detect_turn_frame_light(video_path, sample_rate=5):
    cap = cv2.VideoCapture(video_path)
    prev = None
    max_diff = 0
    best_frame = 0
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if idx % sample_rate != 0:
            idx += 1
            continue

        small = cv2.resize(frame, (160, 90))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if prev is not None:
            diff = np.sum(cv2.absdiff(prev, gray))
            if diff > max_diff:
                max_diff = diff
                best_frame = idx

        prev = gray
        idx += 1

    cap.release()
    return best_frame


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
st.title("🚤 旋回比較ツール（AI補助付き）")

with st.expander("📖 使い方", expanded=True):
    st.markdown("""
① 動画アップ  
② 🤖AIで自動合わせ（おすすめ）  
③ 微調整  
④ 生成  
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
    # AIボタン
    # -------------------------
    if st.button("🤖 AIでターン位置を自動検出"):
        with st.spinner("解析中..."):
            best = detect_turn_frame_light(video_path)
            for i in range(6):
                st.session_state[f"slider_{i}"] = best
            st.success("自動セット完了！")

    # -------------------------
    # 全体操作
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 全艇ロック"):
            st.session_state.lock_all = not st.session_state.lock_all

    with col2:
        if st.button("📋 全艇コピー"):
            base = st.session_state["slider_0"]
            for i in range(6):
                st.session_state[f"slider_{i}"] = base

    st.info(f"全艇ロック：{'ON' if st.session_state.lock_all else 'OFF'}")

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
            f"{i+1}号艇 位置",
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

        sec = frame_idx / fps
        st.caption(f"{sec:.2f}秒")

        use = st.toggle("使用", True, key=f"use_{i}")

        times.append(sec)
        use_flags.append(use)

        st.divider()

    # -------------------------
    # 生成
    # -------------------------
    duration = st.slider("比較秒数", 1.0, 8.0, 4.0)
    ghost = st.slider("残像", 0.7, 0.95, 0.85)

    if st.button("🚀 生成", use_container_width=True):
        with st.spinner("生成中..."):
            res = create_overlay(video_path, times, use_flags, duration, ghost)
            st.video(res)

            with open(res, "rb") as f:
                st.download_button("⬇ 保存", f, "boat_strike.mp4")

    os.remove(video_path)
