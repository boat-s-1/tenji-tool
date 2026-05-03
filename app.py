import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="BOAT STRIKE 軌跡版", layout="centered")

# 色（6艇）
COLORS = [
    (255,255,255),
    (80,80,80),
    (0,0,255),
    (255,0,0),
    (0,255,255),
    (0,255,0)
]

# -------------------------
# 軌跡抽出
# -------------------------
def extract_trajectory(video_path, start_frame, duration_frames):
    cap = cv2.VideoCapture(video_path)

    points = []
    prev_gray = None

    for i in range(duration_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame + i)
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 360))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            _, th = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

            # 重心を取る
            ys, xs = np.where(th > 0)
            if len(xs) > 0:
                x = int(np.mean(xs))
                y = int(np.mean(ys))
                points.append((x, y))

        prev_gray = gray

    cap.release()
    return points


# -------------------------
# 軌跡描画
# -------------------------
def draw_trajectories(video_path, start_frames, duration_frames):
    cap = cv2.VideoCapture(video_path)
    ret, base = cap.read()
    cap.release()

    base = cv2.resize(base, (640, 360))
    canvas = base.copy()

    for i, start in enumerate(start_frames):
        pts = extract_trajectory(video_path, start, duration_frames)

        for j in range(1, len(pts)):
            cv2.line(canvas, pts[j-1], pts[j], COLORS[i], 2)

    return canvas


# -------------------------
# UI
# -------------------------
st.title("🚤 軌跡ライン比較ツール")

file = st.file_uploader("動画アップロード", type=["mp4","mov"])

if file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    st.video(video_path)

    st.markdown("## 🎯 各艇の開始位置")

    start_frames = []

    for i in range(6):
        frame = st.slider(f"{i+1}号艇", 0, total_frames, 0, key=f"s_{i}")
        start_frames.append(frame)

        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, img = cap.read()
        cap.release()

        if ret:
            img = cv2.resize(img, (320, 180))
            st.image(img)

    duration_sec = st.slider("比較秒数", 1.0, 5.0, 3.0)
    duration_frames = int(duration_sec * fps)

    if st.button("🚀 軌跡生成"):
        img = draw_trajectories(video_path, start_frames, duration_frames)
        st.image(img, caption="軌跡比較")

        # 保存
        out_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        cv2.imwrite(out_path, img)

        with open(out_path, "rb") as f:
            st.download_button("保存", f, "trajectory.png")

    os.remove(video_path)
