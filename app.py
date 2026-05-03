import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import gc

st.set_page_config(page_title="BOAT STRIKE - 完成版", layout="wide")

# 艇カラー
COLORS = [
    (255,255,255),
    (80,80,80),
    (0,0,255),
    (255,0,0),
    (0,255,255),
    (0,255,0)
]

# -------------------------
# 動画処理
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
            if not use_flags[idx] or t <= 0:
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
st.title("🚤 BOAT STRIKE - 旋回比較ツール")

# 使い方ガイド
with st.expander("📖 使い方（クリックで開く）", expanded=True):
    st.markdown("""
### ① 動画をアップロード
周回展示のリプレイ動画をアップしてください

### ② フレームを合わせる
各艇ごとに「ターンマーク横を通過した瞬間」を合わせます  
スライダーを動かしてタイミングを揃えてください

### ③ 微調整
±0.1ボタンで細かく調整できます

### ④ 生成
6艇の動きが重なって表示されます

---

### 🔍 見方
・前に色が出る → 行き足が良い  
・内側に残る → ターンが良い  
・外に広がる → 流れている  
""")

st.info("💡 まず1号艇を合わせてから他の艇を揃えると簡単です")

uploaded_file = st.sidebar.file_uploader("動画アップロード", type=["mp4","mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    st.video(video_path)

    st.subheader("🎯 フレーム指定")

    times = []
    use_flags = []

    # 1号艇 → 6号艇の順番
    for i in range(6):
        st.markdown(f"### {i+1}号艇")
        st.caption("👉 ターンマーク横を通過した瞬間に合わせてください")

        col1, col2, col3, col4 = st.columns([4,2,1,1])

        with col1:
            frame_idx = st.slider(
                f"{i+1}号艇 フレーム",
                0, total_frames, 0,
                key=f"slider_{i}"
            )

        with col2:
            sec = frame_idx / fps
            val = st.number_input(
                "秒（微調整用）",
                value=float(sec),
                step=0.1,
                key=f"time_{i}"
            )

        with col3:
            if st.button("−0.1", key=f"minus_{i}"):
                st.session_state[f"time_{i}"] -= 0.1

        with col4:
            if st.button("+0.1", key=f"plus_{i}"):
                st.session_state[f"time_{i}"] += 0.1

        use = st.checkbox(f"{i+1}号艇 使用", True, key=f"use_{i}")

        times.append(st.session_state[f"time_{i}"])
        use_flags.append(use)

        st.divider()

    duration = st.slider("合成秒数", 1.0, 8.0, 4.0)
    ghost = st.slider("残像の長さ", 0.7, 0.95, 0.85)

    # 全艇コピー機能
    if st.button("👉 このフレームを全艇にコピー"):
        base = st.session_state["slider_0"]
        for i in range(6):
            st.session_state[f"slider_{i}"] = base
            st.session_state[f"time_{i}"] = base / fps

    if st.button("🚀 生成"):
        if sum(times) == 0:
            st.warning("秒数を入力してください")
        else:
            with st.spinner("処理中..."):
                try:
                    res = create_overlay(video_path, times, use_flags, duration, ghost)

                    st.success("完成！")
                    st.video(res)

                    with open(res, "rb") as f:
                        st.download_button("ダウンロード", f, "boat_strike.mp4")

                except Exception as e:
                    st.error(f"エラー: {e}")

    os.remove(video_path)
