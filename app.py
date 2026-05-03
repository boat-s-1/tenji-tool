import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE MOBILE", layout="centered")

COLORS = [
    (255,255,255),
    (80,80,80),
    (0,0,255),
    (255,0,0),
    (0,255,255),
    (0,255,0)
]

# -------------------------
# 処理
# -------------------------
def create_overlay(video_path, start_times, use_flags, duration_sec, ghost_decay=0.85):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    scale = 0.5
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    total_frames = int(duration_sec * fps)

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    ghost = np.zeros((height, width, 3), dtype=np.float32)

    for i in range(total_frames):
        max_frame = np.zeros((height, width, 3), dtype=np.uint8)

        for idx, t in enumerate(start_times):
            if not use_flags[idx]:
                continue

            cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps) + i)
            ret, frame = cap.read()

            if ret:
                frame = cv2.resize(frame, (width, height))
                color = COLORS[idx]

                colored = frame.astype(np.float32)
                for c in range(3):
                    colored[:,:,c] *= color[c] / 255.0

                max_frame = np.maximum(max_frame, colored.astype(np.uint8))

        ghost = ghost * ghost_decay + max_frame * (1 - ghost_decay)
        out.write(np.clip(ghost,0,255).astype(np.uint8))

        if i % 10 == 0:
            gc.collect()

    out.release()
    cap.release()
    return output_path


# -------------------------
# UI
# -------------------------
st.title("🚤 旋回比較（スマホ版）")

st.markdown("### ① 動画をアップロード")
file = st.file_uploader("タップして動画を選択", type=["mp4","mov"])

if file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    st.video(video_path)

    st.markdown("### ② まず基準を合わせる")
    st.info("👉 ターンマーク横の瞬間にスライダーを合わせてください")

    base_frame = st.slider("再生位置（ここを基準にする）", 0, total_frames, 0)

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, base_frame)
    ret, frame = cap.read()
    cap.release()

    if ret:
        st.image(frame, caption=f"{base_frame/fps:.2f}秒")

    if st.button("👉 この位置を全艇にコピー（おすすめ）"):
        for i in range(6):
            st.session_state[f"b{i}"] = base_frame

    st.markdown("### ③ 各艇を微調整（ズレてる艇だけ触る）")

    times = []
    use_flags = []

    for i in range(6):
        st.markdown(f"#### {i+1}号艇")

        frame_idx = st.slider(
            f"{i+1}号艇 位置",
            0,
            total_frames,
            st.session_state.get(f"b{i}", base_frame),
            key=f"b{i}"
        )

        sec = frame_idx / fps
        st.write(f"⏱ {sec:.2f}秒")

        use = st.toggle("この艇を使う", True, key=f"use{i}")

        times.append(frame_idx / fps)
        use_flags.append(use)

        st.divider()

    st.markdown("### ④ 動画生成")

    duration = st.slider("比較する長さ", 1.0, 8.0, 4.0)
    ghost = st.slider("軌跡の残り具合", 0.7, 0.95, 0.85)

    if st.button("🚀 比較スタート（タップ）", use_container_width=True):
        with st.spinner("生成中..."):
            res = create_overlay(video_path, times, use_flags, duration, ghost)

            st.success("完成！")
            st.video(res)

            with open(res, "rb") as f:
                st.download_button(
                    "⬇ 保存する",
                    f,
                    "boat_strike.mp4",
                    use_container_width=True
                )

    os.remove(video_path)
