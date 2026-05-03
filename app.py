import streamlit as st
import cv2
import numpy as np
import tempfile
import os

# --- 設定 ---
st.set_page_config(page_title="BOAT STRIKE - 旋回比較オーバーレイ", layout="wide")

def create_overlay(video_path, start_times, duration_sec=4.0):
    """
    start_times: 各艇が基準点を通過する秒数のリスト [t1, t2, ..., t6]
    duration_sec: 合成する動画の長さ（秒）
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(duration_sec * fps)

    # 合成用のバッファ（浮動小数点型で加算していく）
    combined_frames = [np.zeros((height, width, 3), dtype=np.float32) for _ in range(total_frames)]
    counts = np.zeros(total_frames)

    for boat_idx, t in enumerate(start_times):
        if t == 0: continue # 0秒設定はスキップ
        
        start_frame = int(t * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret: break
            
            # 各艇の映像を加算（単純平均合成）
            combined_frames[i] += frame.astype(np.float32)
            counts[i] += 1

    # 結果を保存するための一時ファイル
    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    # ブラウザ再生用にH.264コーデックを指定
    fourcc = cv2.VideoWriter_fourcc(*'avc1') 
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for i in range(total_frames):
        if counts[i] > 0:
            # 加算したフレームを艇の数で割って平均化
            avg_frame = (combined_frames[i] / counts[i]).astype(np.uint8)
            out.write(avg_frame)
        else:
            # 艇のデータがない場合は真っ黒
            out.write(np.zeros((height, width, 3), dtype=np.uint8))

    out.release()
    cap.release()
    return output_path

# --- UI部分 ---
st.title("🚤 BOAT STRIKE - 視覚的機力比較ツール")
st.markdown("画面録画したリプレイ動画をアップロードして、6艇の旋回を重ね合わせます。")

uploaded_file = st.sidebar.file_uploader("動画をアップロード (.mov, .mp4)", type=["mov", "mp4"])

if uploaded_file:
    # 動画を一時的に保存
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mov') as tmp:
        tmp.write(uploaded_file.read())
        video_path = tmp.name

    st.sidebar.success("動画を読み込みました")
    
    # 元動画のプレビュー（タイミング確認用）
    st.subheader("1. タイミングの確認")
    st.video(video_path)
    
    st.subheader("2. 各艇の基準秒数を入力")
    st.info("リプレイ内で、各艇がターンマークの横を通過した瞬間の秒数を入力してください。")

    cols = st.columns(3)
    times = []
    for i in range(6):
        with cols[i % 3]:
            val = st.number_input(f"{i+1}号艇 (秒)", min_value=0.0, step=0.1, format="%.1f")
            times.append(val)

    duration = st.slider("合成する長さ（秒）", 1.0, 10.0, 4.0)

    if st.button("🚀 重ね合わせ動画を生成"):
        if sum(times) == 0:
            st.error("少なくとも1艇以上の秒数を入力してください。")
        else:
            with st.spinner("映像を同期中..."):
                output_video = create_overlay(video_path, times, duration)
                
                st.subheader("3. 比較結果")
                st.video(output_video)
                
                with open(output_video, "rb") as file:
                    st.download_button("合成動画を保存", file, "boat_strike_overlay.mp4")
                
                # 不要な一時ファイルを削除
                os.remove(output_video)
    
    # 素材ファイルを削除
    os.remove(video_path)
