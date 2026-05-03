import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="BOAT STRIKE - Overlay Pro", layout="wide")

# --- 艇カラー（視認性重視で少し強めに調整）---
BOAT_COLORS = [
    (255, 255, 255),  # 1号艇 白
    (50, 50, 50),     # 2号艇 黒（真っ黒だと見えないので少し明るく）
    (0, 0, 255),      # 3号艇 赤
    (255, 0, 0),      # 4号艇 青
    (0, 255, 255),    # 5号艇 黄
    (0, 255, 0)       # 6号艇 緑
]

def create_overlay_pro(video_path, start_times, duration_sec, alpha=0.5, ghost_decay=0.85):
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

    # 各艇ごとに独立したキャプチャ
    caps = []
    for t in start_times:
        c = cv2.VideoCapture(video_path)
        if t > 0:
            c.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        caps.append(c)

    # ゴースト用フレーム
    ghost_frame = np.zeros((height, width, 3), dtype=np.float32)

    for _ in range(total_frames):
        overlay = np.zeros((height, width, 3), dtype=np.float32)

        for boat_idx, c in enumerate(caps):
            ret, frame = c.read()
            if not ret:
                continue

            frame = cv2.resize(frame, (width, height))

            # --- グレースケール ---
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # --- 白背景除去（ここが重要）---
            mask = gray < 200  # ← 調整可能（180〜220くらいで調整）
            norm = np.zeros_like(gray, dtype=np.float32)
            norm[mask] = gray[mask] / 255.0

            # --- 色付け ---
            color = BOAT_COLORS[boat_idx]
            colored = np.zeros_like(frame, dtype=np.float32)
            for i in range(3):
                colored[:, :, i] = norm * color[i]

            # --- 合成（加算じゃなく最大値）---
            overlay = np.maximum(overlay, colored * alpha)

        # --- ゴースト（暴走防止版）---
        ghost_frame = ghost_frame * ghost_decay + overlay * (1 - ghost_decay)

        # --- 安全クリップ ---
        final_frame = np.clip(ghost_frame, 0, 255).astype(np.uint8)
        out.write(final_frame)

    out.release()
    cap.release()
    for c in caps:
        c.release()

    return output_path


# --- UI ---
st.title("🚤 BOAT STRIKE - Overlay Pro（完成版）")
st.markdown("色分け＋残像で6艇の機力を可視化")

uploaded_file = st.sidebar.file_uploader("動画アップロード", type=["mov", "mp4"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.subheader("元動画")
    st.video(video_path)

    st.divider()

    st.subheader("スタート秒数設定")

    col1 = st.columns(3)
    col2 = st.columns(3)

    times = []
    for i in range(3):
        with col1[i]:
            times.append(st.number_input(f"{i+1}号艇", 0.0, 1000.0, 0.0, step=0.1))
    for i in range(3, 6):
        with col2[i-3]:
            times.append(st.number_input(f"{i+1}号艇", 0.0, 1000.0, 0.0, step=0.1))

    duration = st.slider("合成秒数", 1.0, 10.0, 5.0)
    alpha = st.slider("色の強さ", 0.2, 1.0, 0.5)
    ghost = st.slider("残像の長さ", 0.7, 0.95, 0.85)

    if st.button("🚀 生成"):
        if sum(times) == 0:
            st.warning("秒数を入力してください")
        else:
            with st.spinner("生成中..."):
                try:
                    result = create_overlay_pro(video_path, times, duration, alpha, ghost)
                    st.success("完成！")
                    st.video(result)

                    with open(result, "rb") as f:
                        st.download_button("ダウンロード", f, "overlay_pro.mp4")

                except Exception as e:
                    st.error(f"エラー: {e}")

    if os.path.exists(video_path):
        os.remove(video_path)
