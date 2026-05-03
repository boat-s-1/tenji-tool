import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE", layout="centered")

# -------------------------
# 初期化
# -------------------------
for i in range(2):
    if f"frame_{i}" not in st.session_state:
        st.session_state[f"frame_{i}"] = 0

if "sync" not in st.session_state:
    st.session_state.sync = False


# -------------------------
# フレーム取得
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
# 動画生成
# -------------------------
def create_overlay(video_path, f1_start, f2_start, duration):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    scale = 0.5
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)

    total = int(duration * fps)

    out_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    for i in range(total):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(f1_start + i))
        r1, f1 = cap.read()

        cap.set(cv2.CAP_PROP_POS_FRAMES, int(f2_start + i))
        r2, f2 = cap.read()

        if not r1:
            break

        f1 = cv2.resize(f1, (w, h))

        if r2:
            f2 = cv2.resize(f2, (w, h))

            red = f2.copy()
            red[:,:,1] = 0
            red[:,:,0] = 0

            blended = cv2.addWeighted(f1, 1.0, red, 0.35, 0)
        else:
            blended = f1

        cv2.line(blended, (w//2,0), (w//2,h), (0,255,0),1)
        out.write(blended)

        if i % 20 == 0:
            gc.collect()

    out.release()
    cap.release()
    return out_path


# -------------------------
# UI：最強フレーム選択
# -------------------------
def frame_ui(label, video_path, fps, total_frames, idx):

    st.markdown(f"### {label}")

    # 秒スライダー（粗調整）
    sec = st.slider(
        "秒で合わせる",
        0.0,
        total_frames / fps,
        st.session_state[f"frame_{idx}"] / fps,
        step=0.1,
        key=f"sec_{idx}"
    )

    base_frame = int(sec * fps)

    # 微調整
    col1, col2, col3, col4 = st.columns(4)

    if col1.button("-5F", key=f"m5_{idx}"):
        st.session_state[f"frame_{idx}"] -= 5

    if col2.button("-1F", key=f"m1_{idx}"):
        st.session_state[f"frame_{idx}"] -= 1

    if col3.button("+1F", key=f"p1_{idx}"):
        st.session_state[f"frame_{idx}"] += 1

    if col4.button("+5F", key=f"p5_{idx}"):
        st.session_state[f"frame_{idx}"] += 5

    # 同期モード
    if st.session_state.sync:
        for i in range(2):
            st.session_state[f"frame_{i}"] = base_frame

    # 更新
    frame = max(0, min(total_frames-1, base_frame))

    st.session_state[f"frame_{idx}"] = frame

    # プレビュー
    img = get_frame(video_path, frame)
    if img is not None:
        st.image(img)

    st.caption(f"{frame}F / {frame/fps:.2f}秒")

    return frame


# -------------------------
# メイン
# -------------------------
st.title("🚤 1vs1 最強比較ツール")

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

    st.markdown("## 🎯 スタートを合わせる")

    # 同期スイッチ
    st.session_state.sync = st.toggle("同期モード（同時に動かす）", value=False)

    col1, col2 = st.columns(2)

    with col1:
        f1 = frame_ui("① 1号艇", video_path, fps, total_frames, 0)

    with col2:
        f2 = frame_ui("② 比較艇", video_path, fps, total_frames, 1)

    # コピー機能
    if st.button("📋 1号艇 → コピー"):
        st.session_state["frame_1"] = st.session_state["frame_0"]

    st.markdown("## 🎬 生成")

    duration = st.slider("秒数", 1.0, 8.0, 4.0)

    if st.button("🚀 生成", use_container_width=True):
        with st.spinner("生成中..."):
            out = create_overlay(video_path, f1, f2, duration)

            st.success("完成！")
            st.video(out)

            with open(out, "rb") as f:
                st.download_button("保存", f, "boat.mp4")

    os.remove(video_path)
