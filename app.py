import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE - 1vs1比較", layout="wide")

def create_pair_overlay(video_path, base_f, target_f, duration_sec):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    # 負荷軽減のため50%リサイズ
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)
    total_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for i in range(total_frames):
        # 1. ベースとなる1号艇のフレームを取得
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(base_f + i))
        ret1, frame1 = cap.read()
        
        # 2. 比較対象艇のフレームを取得
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(target_f + i))
        ret2, frame2 = cap.read()

        if ret1 and ret2:
            f1 = cv2.resize(frame1, (width, height))
            f2 = cv2.resize(frame2, (width, height))
            
            # 1号艇(f1)をベースに、対象艇(f2)を50%の濃さで重ねる
            # 公式: dst = src1 * alpha + src2 * beta + gamma
            blended = cv2.addWeighted(f1, 0.7, f2, 0.3, 0)
            out.write(blended)
        elif ret1: # 相手が途切れても1号艇だけは出す
            out.write(cv2.resize(frame1, (width, height)))
        else:
            break
        
        if i % 20 == 0: gc.collect()

    out.release()
    cap.release()
    return output_path

st.title("🚤 BOAT STRIKE - 1vs1 旋回比較")

file = st.sidebar.file_uploader("動画をアップロード", type=["mp4","mov"])

if file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mov')
    tfile.write(file.read())
    video_path = tfile.name
    
    st.video(video_path)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("① 基準（1号艇）")
        base_f = st.number_input("1号艇の開始フレーム", value=0, step=1)
        # プレビュー表示
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, base_f)
        ret, img = cap.read()
        if ret:
            st.image(cv2.resize(img, (320, 180)), caption="1号艇のスタート地点")
        cap.release()

    with col2:
        st.subheader("② 比較対象")
        target_no = st.selectbox("比較する艇を選択", [2,3,4,5,6])
        target_f = st.number_input(f"{target_no}号艇の開始フレーム", value=0, step=1)
        # プレビュー表示
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_f)
        ret, img = cap.read()
        if ret:
            st.image(cv2.resize(img, (320, 180)), caption=f"{target_no}号艇のスタート地点")
        cap.release()

    duration = st.slider("合成する秒数", 1.0, 8.0, 4.0)

    if st.button("🚀 1vs1 比較動画を生成"):
        with st.spinner(f"1号艇と{target_no}号艇を同期中..."):
            res = create_pair_overlay(video_path, base_f, target_f, duration)
            st.video(res)
            with open(res, "rb") as f:
                st.download_button("動画を保存", f, f"1vs{target_no}_comparison.mp4")

    os.remove(video_path)
