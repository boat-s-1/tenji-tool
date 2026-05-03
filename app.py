import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE - 1vs1シンプル比較", layout="centered")

# -------------------------
# フレーム取得（軽量）
# -------------------------
@st.cache_data
def get_frame(video_path, frame_idx, width=320):
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
# 1vs1 シンプル合成
# -------------------------
def create_simple_overlay(video_path, base_f, target_f, duration_sec, slow=1.0):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    scale = 0.5
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    total_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps * slow,  # ← スロー対応
        (width, height)
    )

    for i in range(total_frames):

        # -------------------------
        # 1号艇（そのまま）
        # -------------------------
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(base_f + i))
        ret1, f1 = cap.read()

        if not ret1:
            break

        f1 = cv2.resize(f1, (width, height))

        # -------------------------
        # 比較艇
        # -------------------------
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(target_f + i))
        ret2, f2 = cap.read()

        if ret2:
            f2 = cv2.resize(f2, (width, height))

            # 赤だけ残す（比較艇）
            red = f2.copy()
            red[:, :, 1] = 0
            red[:, :, 0] = 0

            # 合成（ここが一番重要）
            blended = cv2.addWeighted(f1, 1.0, red, 0.35, 0)

        else:
            blended = f1

        # -------------------------
        # 中央ライン（比較基準）
        # -------------------------
        cv2.line(blended, (width // 2, 0), (width // 2, height), (0, 255, 0), 1)

        out.write(blended)

        if i % 20 == 0:
            gc.collect()

    out.release()
    cap.release()
    return output_path


# -------------------------
# UI
# -------------------------
st.title("🚤 1vs1 旋回比較（シンプル版）")

file = st.file_uploader("動画をアップロード", type=["mp4", "mov"])

if file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    st.video(video_path)

    st.markdown("## 🎯 スタート位置を合わせる")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("① 1号艇（基準）")
        base_f = st.slider("1号艇の開始位置", 0, total_frames, 0)

        img = get_frame(video_path, base_f)
        if img is not None:
            st.image(img, caption="ここを基準に")

    with col2:
        st.subheader("② 比較艇")
        target_no = st.selectbox("比較する艇", [2, 3, 4, 5, 6])
        target_f = st.slider(f"{target_no}号艇の開始位置", 0, total_frames, 0)

        img = get_frame(video_path, target_f)
        if img is not None:
            st.image(img, caption="ここを合わせる")

    st.markdown("## ⚙️ 設定")

    duration = st.slider("比較秒数", 1.0, 8.0, 4.0)

    slow = st.slider("再生速度（遅くするほど見やすい）", 0.3, 1.0, 0.7)

    st.markdown("## 🎬 生成")

    if st.button("🚀 比較動画を作成", use_container_width=True):
        with st.spinner("生成中..."):
            res = create_simple_overlay(video_path, base_f, target_f, duration, slow)

            st.success("完成！")
            st.video(res)

            with open(res, "rb") as f:
                st.download_button(
                    "⬇ 動画を保存",
                    f,
                    f"1vs{target_no}_comparison.mp4",
                    use_container_width=True
                )

    os.remove(video_path)
