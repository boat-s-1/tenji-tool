import streamlit as st
from streamlit.components.v1 import html
import base64
import os

# --- 画像の読み込み関数 ---
def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    return ""

# 各種画像のパス（適宜実際のファイル名に変更してください）
logo_path = "8c5a3a8d-fe42-4239-bfe9-c67326baa39a.png"
logo_src = get_base64_img(logo_path)
footer_img_src = get_base64_img("1b1a684d-c8bb-45fb-a123-0ed1b73c5046.png")

# スタンプ画像
stamp_dict = {
    "本命": get_base64_img("a7105fda-9305-4e70-98eb-212c65842325.png"),
    "超本命": get_base64_img("a7105fda-9305-4e70-98eb-212c65842325.png"), # サンプル
    "激アツ": get_base64_img("1a097861-b508-41d0-a3ea-ec276d1a4005.png"),
    "鉄板": get_base64_img("ac668bb2-8f4f-40c6-ab3f-a800c64a817c.png"),
    "穴狙い": get_base64_img("0c0491e6-0036-4e58-9e8b-c82f0a60bb80.png"),
    "見": get_base64_img("a6a958fc-8897-4e1b-8d5b-f28459220c26.png"),
    "危険": get_base64_img("ab68e233-d232-438b-8e50-e9d041eea1df.png"),
}

# 艇のアイコン画像
boat_images = {
    "1号艇": get_base64_img("IMG_4170.png"),
    "2号艇": get_base64_img("IMG_4172.png"),
    "3号艇": get_base64_img("IMG_4171.png"),
    "4号艇": get_base64_img("55e7bfa3-f032-45f8-ab82-0cd34799feb2.png"),
    "5号艇": get_base64_img("3e82f55c-1d03-46ce-a11f-9050f242877d.png"),
    "6号艇": get_base64_img("c81ee8e5-46b3-4526-bfee-3d6efdd0801b.png"),
}

# =========================================
# ページ設定 & サイドバー
# =========================================
st.set_page_config(page_title="一果ちゃん新聞", layout="wide")
st.title("🌸 一果ちゃん新聞ジェネレーター")

st.sidebar.header("レース情報")
race_place = st.sidebar.text_input("レース場", "丸亀")
race_no = st.sidebar.text_input("レース番号", "1R")
race_date = st.sidebar.text_input("日付", "2026/05/05")
honmei = st.sidebar.selectbox("本命", [f"{i}号艇" for i in range(1, 7)])

st.sidebar.header("画像設定")
uploaded_character = st.sidebar.file_uploader("キャラ画像", type=["png", "jpg", "jpeg"])
uploaded_bg = st.sidebar.file_uploader("背景画像", type=["png", "jpg", "jpeg"])

character_src = f"data:image/png;base64,{base64.b64encode(uploaded_character.read()).decode()}" if uploaded_character else "https://placehold.co/500x900/png"
bg_src = f"data:image/png;base64,{base64.b64encode(uploaded_bg.read()).decode()}" if uploaded_bg else ""

st.sidebar.header("スタンプ & 数値")
stamp_choice = st.sidebar.selectbox("スタンプ", ["なし"] + list(stamp_dict.keys()))
alert_stamp = st.sidebar.selectbox("警報", ["なし", "波乱注意！", "展示急上昇！", "イン危険！", "高配当警戒！", "超波乱！"])
nige_rate = st.sidebar.slider("イン逃げ期待度", 0, 100, 84)
up_rate = st.sidebar.slider("場平均との差", -30, 30, 11)
wave = st.sidebar.slider("波乱指数", 0, 100, 28)
hit_rate = st.sidebar.slider("的中期待度", 0, 100, 87)

comment = st.sidebar.text_area("一果のひとこと", "1号艇中心だが2号艇の差し注意！")

st.sidebar.header("展開ストーリー設定")
selected_boats = st.sidebar.multiselect("注目する艇を選択（最大3つ）", [f"{i}号艇" for i in range(1, 7)], default=["1号艇", "2号艇", "3号艇"])

boat_comments = {}
boat_scores = {}
for i in range(1, 7):
    boat_comments[f"{i}号艇"] = st.sidebar.text_input(f"{i}号艇 コメント", f"評価コメント{i}")
    boat_scores[f"{i}号艇"] = st.sidebar.slider(f"{i}号艇 評価値", 0, 100, 50)

motor_eval = st.sidebar.text_area("モーター一言メモ", "1号艇は出足型、3号艇の伸びが節イチ級！")

st.sidebar.header("直前情報")
tenji_rank = st.sidebar.selectbox("展示評価", ["S", "A", "B", "C"])
tenji_time = st.sidebar.text_input("補正展示タイム", "6.71")
shinnyu = st.sidebar.text_input("進入予想", "123/456")
ikka_hantei = st.sidebar.text_input("一果判定", "◎1 ○2 ▲5")
danger_boat = st.sidebar.selectbox("危険艇", ["なし"] + [f"{i}号艇" for i in range(1, 7)])
up_boat = st.sidebar.selectbox("展示急上昇", ["なし"] + [f"{i}号艇" for i in range(1, 7)])
jikkan_comment = st.sidebar.text_area("直前コメント", "展示は1号艇優勢！")
honmei_kaime = st.sidebar.text_input("本命買い目", "1-2-3")
osae_kaime = st.sidebar.text_area("押さえ買い目", "1-3-2\n1-2-5")

# =========================================
# HTML生成用パーツ
# =========================================

# ヘッダー部分
header_part = f"""
<div class="header">
    <div class="title">🌸 一果ちゃん新聞</div>
    <div class="date">{race_date}<br>{race_place} {race_no}</div>
</div>
"""

# スタンプ部分
stamp_html = ""
if stamp_choice != "なし" and stamp_dict[stamp_choice]:
    stamp_html = f'<img src="{stamp_dict[stamp_choice]}" style="position:absolute; top:-10px; right:10px; width:120px; z-index:100; transform:rotate(15deg);">'

# 展開ストーリー
story_html = ""
boat_colors = ["#e2e2e2", "#444444", "#ff4444", "#4444ff", "#eeaa00", "#22aa22"]
for b_name in selected_boats:
    idx = int(b_name[0]) - 1
    story_html += f"""
    <div class="pickup-row" style="border-left: 8px solid {boat_colors[idx]};">
        <img src="{boat_images[b_name]}" style="width: 80px; height: auto; margin-right: 15px;">
        <div class="boat-comment">{boat_comments[b_name]}</div>
    </div>
    """

stars = "⭐" * ((wave // 20) + 1)
attention_boats = ", ".join([b.replace("号艇", "") for b in selected_boats])

# =========================================
# CSS & JS (共通)
# =========================================
# (提示されたCSSをベースに共通化)

# --- 1. 前日版HTML 組み立て ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">
{common_style}
</head>
<body>
<div class="wrapper">
    {header_part}
    <div class="main">
        <div class="left">
            <div class="mainbox" style="position: relative;">
                {stamp_html}
                <div class="section-title">本命候補</div> 
                <div style="font-size:42px; font-weight:bold; color:#ff4f93; margin-left:10px;">{honmei}</div>
                <div class="score-row">
                    <div class="score-label">イン逃げ期待度</div>
                    <div class="score-value">{nige_rate}%</div>
                </div>
                <div class="score-row">
                    <div class="score-label">場平均との差</div>
                    <div class="score-up">+{up_rate}%</div>
                </div>
            </div>
            <div class="mainbox">
                <div class="section-title">展開ストーリー (予想)</div> 
                <div class="story-container">{story_html}</div>
            </div>
            <div class="mainbox">
                <div class="section-title">各艇評価指数</div>
                <div class="bar-wrap">
                    {"".join([f'<div class="bar-row"><div class="bar-label">{i}号艇</div><div class="bar-bg"><div class="bar-fill" style="width:{boat_scores[f"{i}号艇"]}%;">{boat_scores[f"{i}号艇"]}</div></div></div>' for i in range(1,7)])}
                </div>
            </div>
        </div>
        <div class="right">
            <img class="character-img" src="{character_src}">
            <div class="fukidashi">
                <div class="fukidashi-title">🌸 一果のひとこと</div>
                <div>{comment}</div>
            </div>
            <div class="notice">
                <div class="notice-title">📍 要チェックポイント</div>
                <div class="notice-item">・波乱指数<span class="notice-value">{stars} ({wave})</span></div>
                <div class="notice-item">・危険艇<span class="notice-value">{danger_boat}</span></div>
                <div class="notice-item">・注目艇<span class="notice-value">{attention_boats}</span></div>
            </div>
            <div class="motor-box">
                <div class="motor-title">⚙️ 一果の機力チェック</div>
                <div style="font-size: 18px; line-height: 1.5; color: #333; font-weight: bold;">{motor_eval}</div>
            </div>
        </div>
    </div>
    <div class="footer"><img src="{footer_img_src}" class="footer-img"></div>
</div>
{download_script}
</body>
</html>
"""

# --- 2. 直前版HTML 組み立て ---
# (同様に html_code2 を構成...)

# =========================================
# タブ表示
# =========================================
tab1, tab2 = st.tabs(["📰 前日版", "🌸 直前版"])
with tab1:
    html(html_code, height=1900, scrolling=True)
with tab2:
    html(html_code2, height=1800, scrolling=True)
