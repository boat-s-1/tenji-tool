import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="BOAT STRIKE - タップ比較", layout="centered")

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
        frame = cv2.resize(frame, (width, int(h * scale)))
        return frame
    return None


# -------------------------
# 動画生成（シンプル重ね）
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

        # 中央ライン
        cv2.line(blended, (w//2, 0), (w//2, h), (0,255,0), 1)

        out.write(blended)

    out.release()
    cap.release()
    return output


# -------------------------
# タップでフレーム選択
# -------------------------
def tap_selector(label, video_path, total_frames, fps, key):
    st.markdown(f"### {label}")

    # 粗調整
    frame = st.slider("ざっくり位置", 0, total_frames-1, 0, key=f"{key}_slider")

    img = get_frame(video_path, frame)

    if img is None:
        st.warning("フレーム取得失敗")
        return frame

    # BGR → RGB → PIL変換（←ここが今回の修正ポイント）
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)

    st.markdown("👇 タップして確認（目印）")

    canvas = st_canvas(
        fill_color="rgba(255,0,0,0.3)",
        stroke_width=2,
        stroke_color="#FF0000",
        background_image=pil_img,  # ←修正済み
        update_streamlit=True,
        height=pil_img.height,
        width=pil_img.width,
        drawing_mode="point",
        key=f"{key}_canvas"
    )

    # タップ検出（あくまで目印）
    if canvas.json_data is not None:
        objects = canvas.json_data.get("objects", [])
        if len(objects) > 0:
            st.success("タップ位置OK（このフレームで固定）")

    st.caption(f"{frame}F / {frame/fps:.2f}秒")

    return frame


# -------------------------
# UI
# -------------------------
st.title("🚤 1vs1 タップ比較ツール")

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

    st.markdown("## 🎯 タップで開始位置を合わせる")

    col1, col2 = st.columns(2)

    with col1:
        base_f = tap_selector("① 1号艇（基準）", video_path, total_frames, fps, "base")

    with col2:
        target_f = tap_selector("② 比較艇", video_path, total_frames, fps, "target")

    st.markdown("## 🎬 生成")

    duration = st.slider("比較秒数", 1.0, 8.0, 4.0)

    if st.button("🚀 生成", use_container_width=True):
        with st.spinner("処理中..."):
            out = create_overlay(video_path, base_f, target_f, duration)

            st.success("完成！")
            st.video(out)

            with open(out, "rb") as f:
                st.download_button("⬇ 保存", f, "boat_compare.mp4", use_container_width=True)

    os.remove(video_path)
