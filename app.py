from PIL import Image, ImageDraw, ImageFont

# =========================
# 入力データ
# =========================

race_data = {
    "race_name": "丸亀 1R",
    "date": "2026.05.05",

    # 1号艇データ
    "boat1_win": 72,
    "boat1_motor": 48,
    "boat1_st": 0.12,
    "boat1_local": 68,

    # 2号艇データ
    "boat2_sashi": 42,
    "boat2_motor": 52,
    "boat2_st": 0.13,

    # 波乱指数
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
# イン逃げ指数計算
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

    comment = "イン中心のレース"

elif sashi_index >= 70:

    comment = "2号艇の差しに注意"

else:

    comment = "波乱注意の一戦"

# =========================
# 信頼度
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

img = Image.open("template.jpg")

draw = ImageDraw.Draw(img)

# =========================
# フォント
# =========================

font_big = ImageFont.load_default()
font_mid = ImageFont.load_default()
font_small = ImageFont.load_default()

# =========================
# テキスト描画
# =========================

# 日付・レース名
draw.text(
    (70, 40),
    f"{race_data['date']}  {race_data['race_name']}",
    fill="black",
    font=font_small
)

# 本命
draw.text(
    (120, 180),
    f"本命：{honmei}",
    fill="red",
    font=font_big
)

# イン逃げ期待度
draw.text(
    (120, 260),
    f"イン逃げ期待度 {nige_index}%",
    fill="red",
    font=font_big
)

# 信頼度
draw.text(
    (120, 330),
    f"逃げ信頼度：{trust}",
    fill="green",
    font=font_mid
)

# コメント
draw.text(
    (80, 760),
    comment,
    fill="black",
    font=font_small
)

# 分析データ
draw.text(
    (80, 470),
    f"逃げ成功率 {race_data['boat1_win']}%",
    fill="black",
    font=font_small
)

draw.text(
    (80, 520),
    f"差し成功率 {race_data['boat2_sashi']}%",
    fill="black",
    font=font_small
)

# 直前誘導
draw.text(
    (80, 930),
    "展示評価・補正展示タイムは直前版で公開！",
    fill="red",
    font=font_small
)

# =========================
# 保存
# =========================

img.save("output.jpg")

print("新聞画像を生成しました！")
