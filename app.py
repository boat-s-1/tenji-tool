from PIL import Image, ImageDraw, ImageFont

# =========================
# 入力データ
# =========================

race_data = {
    "race_name": "丸亀 1R",
    "date": "2026.05.05",

    # 1号艇
    "boat1_win": 72,
    "boat1_motor": 48,
    "boat1_st": 0.12,
    "boat1_local": 68,

    # 2号艇
    "boat2_sashi": 42,
    "boat2_motor": 52,
    "boat2_st": 0.13,

    # コメント用
    "wave": 28
}

# =========================
# ST補正関数
# =========================

def st_score(st):
    if st <= 0.10:
        return 100
    elif st <= 0.13:
        return 85
    elif st <= 0.16:
        return 70
    else:
        return 50

# =========================
# イン逃げ指数
# =========================

nige_index = (
    race_data["boat1_win"] * 0.25 +
    race_data["boat1_motor"] * 0.20 +
    st_score(race_data["boat1_st"]) * 0.15 +
    race_data["boat1_local"] * 0.15
)

nige_index = int(nige_index)

# =========================
# 差し指数
# =========================

sashi_index = (
    race_data["boat2_sashi"] * 0.40 +
    race_data["boat2_motor"] * 0.30 +
    st_score(race_data["boat2_st"]) * 0.30
)

sashi_index = int(sashi_index)

# =========================
# 本命判定
# =========================

if nige_index >= 75:
    honmei = "1号艇"
else:
    honmei = "2号艇"

# =========================
# コメント生成
# =========================

if nige_index >= 80 and race_data["wave"] <= 30:
    comment = "イン中心のレース。"
elif sashi_index >= 70:
    comment = "2号艇の差しに注意。"
else:
    comment = "波乱注意の一戦。"

# =========================
# 評価
# =========================

if nige_index >= 85:
    trust = "鉄板級"
elif nige_index >= 75:
    trust = "信頼度高"
elif nige_index >= 60:
    trust = "やや高"
else:
    trust = "波乱"

# =========================
# テンプレ画像読み込み
# =========================

img = Image.open("template.png")

draw = ImageDraw.Draw(img)

# =========================
# フォント
# =========================

font_big = ImageFont.truetype("NotoSansJP-Bold.ttf", 60)
font_mid = ImageFont.truetype("NotoSansJP-Bold.ttf", 40)
font_small = ImageFont.truetype("NotoSansJP-Regular.ttf", 28)

# =========================
# テキスト描画
# =========================

# レース名
draw.text(
    (70, 40),
    f"{race_data['date']}  {race_data['race_name']}",
    font=font_small,
    fill="black"
)

# 本命
draw.text(
    (120, 180),
    honmei,
    font=font_big,
    fill="red"
)

# イン逃げ期待度
draw.text(
    (120, 290),
    f"{nige_index}%",
    font=font_big,
    fill="red"
)

# 信頼度
draw.text(
    (120, 370),
    f"逃げ信頼度：{trust}",
    font=font_mid,
    fill="green"
)

# コメント
draw.text(
    (80, 760),
    comment,
    font=font_small,
    fill="black"
)

# 分析データ
draw.text(
    (80, 470),
    f"逃げ成功率 {race_data['boat1_win']}%",
    font=font_small,
    fill="black"
)

draw.text(
    (80, 520),
    f"差し成功率 {race_data['boat2_sashi']}%",
    font=font_small,
    fill="black"
)

# 直前誘導
draw.text(
    (80, 930),
    "展示評価・補正展示タイムは直前版で公開！",
    font=font_small,
    fill="red"
)

# =========================
# 保存
# =========================

img.save("output.png")

print("新聞画像を生成しました！")        r2, f2 = cap.read()

        if not r1:
            break

        f1 = cv2.resize(f1, (w, h))

        if r2:
            f2 = cv2.resize(f2, (w, h))

            # -------------------------
            # 比較艇を赤寄りに
            # -------------------------
            red = f2.copy().astype(np.float32)

            red[:, :, 1] *= 0.2  # 緑弱め
            red[:, :, 0] *= 0.2  # 青弱め
            red[:, :, 2] = np.clip(red[:, :, 2] * 1.5, 0, 255)

            red = red.astype(np.uint8)

            # -------------------------
            # 合成
            # -------------------------
            blended = cv2.addWeighted(f1, 1.0, red, alpha, 0)

        else:
            blended = f1

        # 中央ライン
        cv2.line(blended, (w//2, 0), (w//2, h), (0,255,0), 1)

        out.write(blended)

        if i % 20 == 0:
            gc.collect()

    out.release()
    cap.release()

    return out_path


# -------------------------
# フレームUI（スマホ最強）
# -------------------------
def frame_ui(label, video_path, fps, total_frames, idx):

    st.markdown(f"### {label}")

    # 秒でざっくり
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
        base_frame -= 5
    if col2.button("-1F", key=f"m1_{idx}"):
        base_frame -= 1
    if col3.button("+1F", key=f"p1_{idx}"):
        base_frame += 1
    if col4.button("+5F", key=f"p5_{idx}"):
        base_frame += 5

    frame = max(0, min(total_frames - 1, base_frame))
    st.session_state[f"frame_{idx}"] = frame

    # プレビュー
    img = get_frame(video_path, frame)
    if img is not None:
        st.image(img)

    st.caption(f"{frame}F / {frame/fps:.2f}秒")

    return frame


# -------------------------
# UI
# -------------------------
st.title("🚤 BOAT STRIKE（2艇クリーン比較）")

file = st.file_uploader("動画アップロード", type=["mp4", "mov"])

if file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    st.video(video_path)

    st.markdown("## 🎯 スタート合わせ")

    st.session_state.sync = st.toggle("同期モード", value=False)

    col1, col2 = st.columns(2)

    with col1:
        f1 = frame_ui("① 1号艇（基準）", video_path, fps, total_frames, 0)

    with col2:
        f2 = frame_ui("② 比較艇", video_path, fps, total_frames, 1)

    # コピー
    if st.button("📋 1号艇 → コピー"):
        st.session_state["frame_1"] = st.session_state["frame_0"]

    st.markdown("## 🎛 表示調整")

    alpha = st.slider("比較艇の濃さ", 0.2, 0.9, 0.6, 0.05)

    st.markdown("## 🎬 生成")

    duration = st.slider("秒数", 1.0, 8.0, 4.0)

    if st.button("🚀 生成", use_container_width=True):
        with st.spinner("生成中..."):
            out = create_overlay_clean(video_path, f1, f2, duration, alpha)

            st.success("完成！")
            st.video(out)

            with open(out, "rb") as f:
                st.download_button("保存", f, "boat_clean_compare.mp4")

    os.remove(video_path)
