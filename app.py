import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="BOAT STRIKE - タップ合わせ", layout="centered")

# -------------------------
# フレーム取得
# -------------------------
@st.cache_data
def get_frame(video_path, frame_idx, width=400):
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
# 動画生成（シンプル版）
# -------------------------
def create_overlay(video_path, base_f, target_f, duration_sec):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    scale = 0.5
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)

    total = int(duration_sec * fps)

    output = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    for i in range(total):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(base_f + i))
        r1, f1 = cap.read()

        cap.set(cv2.CAP_PROP_POS_FRAMES, int(target_f + i))
        r2, f2 = cap.read()

        if not r1:
            break

        f1 = cv2.resize(f1, (w, h))

        if r2:
            f2 = cv2.resize(f2, (w, h))

            red = f2.copy()
            red[:, :, 1] = 0
            red[:, :, 0] = 0

            blended = cv2.addWeighted(f1, 1.0, red, 0.35, 0)
        else:
            blended = f1

        cv2.line(blended, (w//2, 0), (w//2, h), (0,255,0), 1)
        out.write(blended)

    out.release()
    cap.release()
    return output


# -------------------------
# タップUI
# -------------------------
def tap_selector(label, video_path, total_frames, fps, key):
    st.markdown(f"### {label}")

    frame = st.slider("ざっくり位置", 0, total_frames, 0, key=f"{key}_slider")

    img = get_frame(video_path, frame)

    if img is not None:
        st.markdown("👇 タップして位置を決める")

        canvas = st_canvas(
            fill_color="rgba(255,0,0,0.3)",
            stroke_width=2,
            stroke_color="#FF0000",
            background_image=img,
            update_streamlit=True,
            height=img.shape[0],
            width=img.shape[1],
            drawing_mode="point",
            key=f"{key}_canvas"
        )

        # タップ検出
        if canvas.json_data is not None:
            objects = canvas.json_data["objects"]
            if len(objects) > 0:
                st.success("タップ検出！このフレームを採用")

    st.caption(f"{frame/fps:.2f}秒")

    return frame


# -------------------------
# UI
# -------------------------
st.title("🚤 タップで合わせる 1vs1比較")

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

    st.markdown("## 🎯 タップで位置合わせ")

    col1, col2 = st.columns(2)

    with col1:
        base_f = tap_selector("① 1号艇", video_path, total_frames, fps, "base")

    with col2:
        target_f = tap_selector("② 比較艇", video_path, total_frames, fps, "target")

    st.markdown("## 🎬 生成")

    duration = st.slider("秒数", 1.0, 8.0, 4.0)

    if st.button("🚀 生成"):
        with st.spinner("処理中..."):
            out = create_overlay(video_path, base_f, target_f, duration)
            st.video(out)

            with open(out, "rb") as f:
                st.download_button("保存", f, "result.mp4")

    os.remove(video_path)
