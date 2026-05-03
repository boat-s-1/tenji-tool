import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE - 1vs1比較", layout="centered")

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
# 1vs1動画生成（強化版）
# -------------------------
def create_pair_overlay(video_path, base_f, target_f, duration_sec, slow=1.0):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    # 軽量化
    scale = 0.5
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)

    total_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps * slow,  # ← スロー調整
        (width, height)
    )

    for i in range(total_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(base_f + i))
        ret1, f1 = cap.read()

        cap.set(cv2.CAP_PROP_POS_FRAMES, int(target_f + i))
        ret2, f2 = cap.read()

        if not ret1:
            break

        f1 = cv2.resize(f1, (width, height))

        if ret2:
            f2 = cv2.resize(f2, (width, height))

            # -------------------------
            # 色分け
            # -------------------------
            base = f1.astype(np.float32)

            target = f2.astype(np.float32)
            target[:,:,1] = 0  # 緑消す
            target[:,:,0] = 0  # 青消す（赤だけ残す）

            blended = np.clip(base * 0.7 + target * 0.7, 0, 255).astype(np.uint8)

            # -------------------------
            # 差分強調
            # -------------------------
            diff = cv2.absdiff(f1, f2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

            blended[mask > 0] = [0, 0, 255]

        else:
            blended = f1

        # -------------------------
        # 中央ライン（基準）
        # -------------------------
        cv2.line(blended, (width//2, 0), (width//2, height), (0,255,0), 1)

        out.write(blended)

        if i % 20 == 0:
            gc.collect()

    out.release()
    cap.release()
    return output_path


# -------------------------
# UI
# -------------------------
st.title("🚤 1vs1 旋回比較ツール")

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

    st.markdown("## 🎯 スタート位置を合わせる")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("① 1号艇（基準）")
        base_f = st.slider("1号艇", 0, total_frames, 0)

        img = get_frame(video_path, base_f)
        if img is not None:
            st.image(img)

    with col2:
        st.subheader("② 比較艇")
        target_no = st.selectbox("艇番号", [2,3,4,5,6])
        target_f = st.slider(f"{target_no}号艇", 0, total_frames, 0)

        img = get_frame(video_path, target_f)
        if img is not None:
            st.image(img)

    st.markdown("## ⚙️ 設定")

    duration = st.slider("比較秒数", 1.0, 8.0, 4.0)

    slow = st.slider("再生速度（遅くするほど見やすい）", 0.3, 1.0, 0.7)

    st.markdown("## 🎬 生成")

    if st.button("🚀 比較動画を作る", use_container_width=True):
        with st.spinner("比較中..."):
            res = create_pair_overlay(video_path, base_f, target_f, duration, slow)

            st.success("完成！")
            st.video(res)

            with open(res, "rb") as f:
                st.download_button("⬇ 保存", f, f"1vs{target_no}.mp4", use_container_width=True)

    os.remove(video_path)
