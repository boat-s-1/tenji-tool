import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="BOAT STRIKE", layout="wide")

def create_overlay(video_path, start_times, duration_sec=3.0):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None: fps = 30.0
    
    # 負荷軽減のため、解像度を半分にする
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)
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
            # 処理を軽くするためにリサイズ
            frame_small = cv2.resize(frame, (width, height))
            combined_frames[i] += frame_small.astype(np.float32)
            counts[i] += 1

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    # OpenCV標準のコーデック
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for i in range(total_frames):
        if counts[i] > 0:
            avg_frame = (combined_frames[i] / counts[i]).astype(np.uint8)
            out.write(avg_frame)
    
    out.release()
    cap.release()
    return output_path

st.title("🚤 BOAT STRIKE - 軽量版")

uploaded_file = st.sidebar.file_uploader("動画をアップロード", type=["mov", "mp4"])

if uploaded_file:
    # 1. 動画の保存
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.video(video_path)
    
    # 2. 設定
    cols = st.columns(3)
    times = [cols[i%3].number_input(f"{i+1}号艇(秒)", 0.0, 1000.0, 0.0, step=0.1) for i in range(6)]
    
    if st.button("🚀 生成開始"):
        if sum(times) == 0:
            st.warning("秒数を入力してください")
        else:
            with st.spinner("処理中...（数秒かかります）"):
                try:
                    result_video = create_overlay(video_path, times)
                    st.video(result_video)
                    st.success("成功！")
                except Exception as e:
                    st.error(f"エラー: {e}")
