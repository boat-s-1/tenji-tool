import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="BOAT STRIKE - 旋回比較オーバーレイ", layout="wide")

def create_overlay(video_path, start_times, duration_sec=4.0):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 30.0 # フォールバック
        
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(duration_sec * fps)

    combined_frames = [np.zeros((height, width, 3), dtype=np.float32) for _ in range(total_frames)]
    counts = np.zeros(total_frames)

    for boat_idx, t in enumerate(start_times):
        if t <= 0: continue
        
        start_frame = int(t * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret: break
            combined_frames[i] += frame.astype(np.float32)
            counts[i] += 1

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    # サーバー環境で最も安定するコーデックに変更
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for i in range(total_frames):
        if counts[i] > 0:
            avg_frame = (combined_frames[i] / counts[i]).astype(np.uint8)
            out.write(avg_frame)
        else:
            out.write(np.zeros((height, width, 3), dtype=np.uint8))

    out.release()
    cap.release()
    return output_path

st.title("🚤 BOAT STRIKE - 視覚的機力比較ツール")

uploaded_file = st.sidebar.file_uploader("動画をアップロード", type=["mov", "mp4"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mov') as tmp:
        tmp.write(uploaded_file.read())
        video_path = tmp.name

    st.sidebar.success("動画を読み込みました")
    st.video(video_path)
    
    st.subheader("設定")
    cols = st.columns(3)
    times = []
    for i in range(6):
        with cols[i % 3]:
            val = st.number_input(f"{i+1}号艇 (秒)", min_value=0.0, step=0.1, format="%.1f", key=f"boat_{i}")
            times.append(val)

    duration = st.slider("合成時間（秒）", 1.0, 10.0, 4.0)

    if st.button("🚀 生成開始"):
        if sum(times) == 0:
            st.error("秒数を入力してください")
        else:
            with st.spinner("処理中..."):
                try:
                    output_video = create_overlay(video_path, times, duration)
                    st.video(output_video)
                    with open(output_video, "rb") as f:
                        st.download_button("動画を保存", f, "result.mp4")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
