import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="BOAT STRIKE - 軽量版", layout="centered")

st.title("🚤 軽量 軌跡ツール")
st.write("動画から軌跡を1枚の画像で表示します（軽量版）")

uploaded_file = st.file_uploader("動画をアップロード", type=["mp4", "mov"])

if uploaded_file:
    # 保存
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.video(video_path)

    st.write("設定")

    duration = st.slider("解析秒数（短くするほど安定）", 1, 5, 3)
    sample_rate = st.slider("フレーム間引き（大きいほど軽い）", 2, 10, 5)
    threshold = st.slider("検出感度", 5, 50, 15)

    if st.button("🚀 軌跡生成"):
        with st.spinner("処理中（数秒）"):

            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30

            scale = 0.3  # 軽量化
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)

            total_frames = int(duration * fps)

            canvas = np.zeros((height, width, 3), dtype=np.uint8)

            ret, prev = cap.read()
            if not ret:
                st.error("動画が読み込めません")
            else:
                prev = cv2.resize(prev, (width, height))

                for i in range(total_frames):

                    # フレーム間引き（超重要）
                    for _ in range(sample_rate):
                        ret, frame = cap.read()

                    if not ret:
                        break

                    frame = cv2.resize(frame, (width, height))

                    # 差分
                    diff = cv2.absdiff(prev, frame)
                    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

                    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

                    # ノイズ除去
                    mask = cv2.GaussianBlur(mask, (5,5), 0)

                    # 重心
                    ys, xs = np.where(mask > 0)

                    if len(xs) > 20:
                        cx = int(np.mean(xs))
                        cy = int(np.mean(ys))

                        # 軌跡描画（白）
                        cv2.circle(canvas, (cx, cy), 2, (255,255,255), -1)

                    prev = frame

                cap.release()

                st.success("完成！")

                st.image(canvas, caption="軌跡")

    # クリーンアップ
    if os.path.exists(video_path):
        os.remove(video_path)
