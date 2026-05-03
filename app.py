import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="BOAT STRIKE - Diff Overlay", layout="wide")

# --- 艇カラー ---
BOAT_COLORS = [
    (255, 255, 255),  # 1 白
    (80, 80, 80),     # 2 黒（見やすく調整）
    (0, 0, 255),      # 3 赤
    (255, 0, 0),      # 4 青
    (0, 255, 255),    # 5 黄
    (0, 255, 0)       # 6 緑
]

def create_overlay_diff(video_path, start_times, duration_sec, alpha=0.6, ghost_decay=0.88, threshold=25):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 30.0

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)
    total_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 各艇キャプチャ
    caps = []
    prev_frames = []

    for t in start_times:
        c = cv2.VideoCapture(video_path)
        if t > 0:
            c.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        caps.append(c)

        ret, frame = c.read()
        if ret:
            prev_frames.append(cv2.resize(frame, (width, height)))
        else:
            prev_frames.append(None)

    ghost = np.zeros((height, width, 3), dtype=np.float32)

    for _ in range(total_frames):
        overlay = np.zeros((height, width, 3), dtype=np.float32)

        for i, c in enumerate(caps):
            ret, frame = c.read()
            if not ret or prev_frames[i] is None:
                continue

            frame = cv2.resize(frame, (width, height))

            # --- 差分 ---
            diff = cv2.absdiff(prev_frames[i], frame)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            # --- ノイズ除去 ---
            _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)

            norm = mask.astype(np.float32) / 255.0

            # --- 色付け ---
            color = BOAT_COLORS[i]
            colored = np.zeros_like(frame, dtype=np.float32)

            for ch in range(3):
                colored[:, :, ch] = norm * color[ch]

            # --- 合成 ---
            overlay += colored * alpha

            # 更新
            prev_frames[i] = frame.copy()

        # --- ゴースト（軌跡）---
        ghost = ghost * ghost_decay + overlay * (1 - ghost_decay)

        final = np.clip(ghost, 0, 255).astype(np.uint8)
        out.write(final)

    out.release()
    cap.release()
    for c in caps:
        c.release()

    return output_path


# --- UI ---
st.title("🚤 BOAT STRIKE - 差分トラッキング版")
st.markdown("動いている部分だけ抽出して、軌跡と伸びを可視化")

uploaded_file = st.sidebar.file_uploader("動画アップロード", type=["mov", "mp4"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.video(video_path)

    st.subheader("スタート秒数")

    cols1 = st.columns(3)
    cols2 = st.columns(3)

    times = []
    for i in range(3):
        with cols1[i]:
            times.append(st.number_input(f"{i+1}号艇", 0.0, 1000.0, 0.0, step=0.1))
    for i in range(3, 6):
        with cols2[i-3]:
            times.append(st.number_input(f"{i+1}号艇", 0.0, 1000.0, 0.0, step=0.1))

    duration = st.slider("秒数", 1.0, 10.0, 5.0)
    alpha = st.slider("色の強さ", 0.2, 1.0, 0.6)
    ghost_decay = st.slider("軌跡の長さ", 0.7, 0.97, 0.88)
    threshold = st.slider("検出感度", 10, 60, 25)

    if st.button("🚀 生成"):
        if sum(times) == 0:
            st.warning("秒数を入力してください")
        else:
            with st.spinner("生成中..."):
                result = create_overlay_diff(video_path, times, duration, alpha, ghost_decay, threshold)

                st.success("完成")
                st.video(result)

                with open(result, "rb") as f:
                    st.download_button("ダウンロード", f, "diff_overlay.mp4")

    if os.path.exists(video_path):
        os.remove(video_path)
