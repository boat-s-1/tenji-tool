import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE - Memory Efficient", layout="wide")

def create_overlay_safe(video_path, start_times, duration_sec):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0: fps = 30.0
    
    # 負荷軽減のため解像度を半分にする
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)
    total_frames = int(duration_sec * fps)

    # 出力設定
    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 1フレームずつ処理（メモリを溜め込まない）
    for i in range(total_frames):
        frame_sum = np.zeros((height, width, 3), dtype=np.float32)
        count = 0
        
        for t in start_times:
            if t <= 0: continue
            
            # 各艇の該当フレームへジャンプ
            target_frame = int(t * fps) + i
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()
            
            if ret:
                frame_res = cv2.resize(frame, (width, height))
                frame_sum += frame_res.astype(np.float32)
                count += 1
        
        if count > 0:
            avg_frame = (frame_sum / count).astype(np.uint8)
            out.write(avg_frame)
        
        # 毎フレーム、メモリを明示的に解放
        del frame_sum
        if i % 10 == 0: gc.collect()

    out.release()
    cap.release()
    gc.collect()
    return output_path

st.title("🚤 BOAT STRIKE - 旋回比較（省メモリ版）")

uploaded_file = st.sidebar.file_uploader("動画をアップロード", type=["mov", "mp4"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mov')
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.subheader("1. 秒数確認用プレビュー")
    st.video(video_path)
    
    st.subheader("2. 設定")
    times = []
    cols = st.columns(3)
    for i in range(6):
        times.append(cols[i%3].number_input(f"{i+1}号艇 (秒)", 0.0, 1000.0, 0.0, step=0.1, key=f"boat_{i}"))
    
    duration = st.slider("合成秒数", 1.0, 8.0, 4.0)

    if st.button("🚀 生成開始"):
        if sum(times) == 0:
            st.warning("秒数を入力してください")
        else:
            with st.spinner("低メモリモードで処理中..."):
                try:
                    res_path = create_overlay_safe(video_path, times, duration)
                    st.video(res_path)
                    with open(res_path, "rb") as f:
                        st.download_button("保存する", f, "boat_strike.mp4")
                except Exception as e:
                    st.error(f"エラー: {e}")
    
    os.remove(video_path)
