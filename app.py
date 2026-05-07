import streamlit as st
from streamlit.components.v1 import html
import base64

# =========================================
# ページ設定
# =========================================

st.set_page_config(
    page_title="一果ちゃん新聞",
    layout="wide"
)

st.title("🌸 一果ちゃん新聞ジェネレーター")

# =========================================
# サイドバー
# =========================================

st.sidebar.header("レース情報")

race_place = st.sidebar.text_input(
    "レース場",
    "丸亀"
)

race_no = st.sidebar.text_input(
    "レース番号",
    "1R"
)

race_date = st.sidebar.text_input(
    "日付",
    "2026/05/05"
)

honmei = st.sidebar.selectbox(
    "本命",
    [
        "1号艇",
        "2号艇",
        "3号艇",
        "4号艇",
        "5号艇",
        "6号艇"
    ]
)

# =========================================
# 画像
# =========================================

st.sidebar.header("画像")

uploaded_character = st.sidebar.file_uploader(
    "キャラ画像",
    type=["png", "jpg", "jpeg"]
)

uploaded_bg = st.sidebar.file_uploader(
    "背景画像",
    type=["png", "jpg", "jpeg"]
)

# =========================================
# Base64変換
# =========================================

if uploaded_character is not None:

    character_base64 = base64.b64encode(
        uploaded_character.read()
    ).decode()

    character_src = f"data:image/png;base64,{character_base64}"

else:

    character_src = "https://placehold.co/500x900/png"

if uploaded_bg is not None:

    bg_base64 = base64.b64encode(
        uploaded_bg.read()
    ).decode()

    bg_src = f"data:image/png;base64,{bg_base64}"

else:

    bg_src = ""

# =========================================
# スタンプ
# =========================================

stamp = st.sidebar.selectbox(
    "スタンプ",
    [
        "なし",
        "本命",
        "超本命",
        "激アツ",
        "鉄板",
        "穴狙い",
        "見",
        "危険",
        "波乱警報",
        "大荒れ注意"
    ]
)

alert_stamp = st.sidebar.selectbox(
    "警報",
    [
        "なし",
        "波乱注意！",
        "展示急上昇！",
        "イン危険！",
        "高配当警戒！",
        "超波乱！"
    ]
)

# =========================================
# 数値
# =========================================

nige_rate = st.sidebar.slider(
    "イン逃げ期待度",
    0,
    100,
    84
)

up_rate = st.sidebar.slider(
    "場平均との差",
    -30,
    30,
    11
)

wave = st.sidebar.slider(
    "波乱指数",
    0,
    100,
    28
)

# =========================================
# コメント
# =========================================

comment = st.sidebar.text_area(
    "一果のひとこと",
    "1号艇中心だが2号艇の差し注意！"
)

# =========================================
# 艇コメント
# =========================================

boat1 = st.sidebar.text_input(
    "1号艇",
    "逃げ信頼度：高"
)

boat2 = st.sidebar.text_input(
    "2号艇",
    "差し注意"
)

boat3 = st.sidebar.text_input(
    "3号艇",
    "展開待ち"
)

boat4 = st.sidebar.text_input(
    "4号艇",
    "穴候補"
)

boat5 = st.sidebar.text_input(
    "5号艇",
    "展示上昇"
)

boat6 = st.sidebar.text_input(
    "6号艇",
    "大穴注意"
)

# =========================================
# 艇評価バー
# =========================================

boat1_score = st.sidebar.slider(
    "1号艇 評価",
    0,
    100,
    88
)

boat2_score = st.sidebar.slider(
    "2号艇 評価",
    0,
    100,
    65
)

boat3_score = st.sidebar.slider(
    "3号艇 評価",
    0,
    100,
    52
)

boat4_score = st.sidebar.slider(
    "4号艇 評価",
    0,
    100,
    48
)

boat5_score = st.sidebar.slider(
    "5号艇 評価",
    0,
    100,
    60
)

boat6_score = st.sidebar.slider(
    "6号艇 評価",
    0,
    100,
    22
)

# =========================================
# CSS
# =========================================

style = f"""

<style>

body{{
    background:#fff7fb;
    font-family:'Arial';
    padding:20px;
}}

.wrapper{{
    width:1000px;
    margin:auto;
    background:white;
    border:5px dashed #ff8db8;
    border-radius:30px;
    overflow:hidden;
}}

.header{{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:25px;
    border-bottom:5px dashed #ff8db8;
}}

.title{{
    font-size:64px;
    color:#ff4f93;
    font-weight:bold;
}}

.date{{
    text-align:right;
    font-size:22px;
    font-weight:bold;
}}

.sub{{
    padding:20px;
    font-size:38px;
    color:#ff4f93;
    font-weight:bold;
}}

.main{{
    display:flex;
    gap:20px;
    padding:20px;
}}

.left{{
    width:72%;
}}

.right{{
    width:28%;
}}

.box{{
    border:4px dashed #ffd0e2;
    border-radius:25px;
    padding:20px;
    margin-bottom:20px;
    background:#fffafb;
}}

.grid{{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin-top:20px;
}}

.boat{{
    border:3px dashed #ffd0e2;
    border-radius:18px;
    padding:12px;
    background:white;
}}

.boat-title{{
    font-size:24px;
    font-weight:bold;
}}

.boat-text{{
    font-size:18px;
    margin-top:8px;
}}

.score-row{{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:18px;
    border-bottom:2px dashed #ffd0e2;
    padding-bottom:10px;
}}

.score-label{{
    font-size:34px;
    color:#ff4f93;
    font-weight:bold;
}}

.score-value{{
    font-size:48px;
    color:#ff4f93;
    font-weight:bold;
}}

.score-up{{
    font-size:44px;
    color:#44aa55;
    font-weight:bold;
}}

.character-img{{
    width:100%;
    border-radius:20px;
}}

.notice{{
    margin-top:18px;
    background:#fff1b8;
    border:4px dashed #ff8db8;
    border-radius:20px;
    padding:18px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
    color:#ff4f93;
}}

.fukidashi{{
    margin-top:18px;
    background:white;
    border:4px dashed #ff8db8;
    border-radius:20px;
    padding:18px;
}}

.fuki-title{{
    font-size:28px;
    color:#ff4f93;
    font-weight:bold;
    margin-bottom:10px;
}}

.bar-box{{
    border:4px dashed #ffd0e2;
    border-radius:25px;
    padding:20px;
    background:#fffafb;
}}

.bar-title{{
    font-size:36px;
    color:#ff4f93;
    font-weight:bold;
    margin-bottom:20px;
}}

.bar-row{{
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:18px;
}}

.bar-label-inline{{
    width:80px;
    font-size:24px;
    font-weight:bold;
}}

.bar-bg-inline{{
    flex:1;
    height:42px;
    background:#ffe3ee;
    border-radius:20px;
    overflow:hidden;
}}

.bar-fill-inline{{
    height:100%;
    background:linear-gradient(
        90deg,
        #ff7eb3,
        #ff4f93
    );
    border-radius:20px;
    color:white;
    font-size:20px;
    font-weight:bold;
    text-align:right;
    line-height:42px;
    padding-right:12px;
}}

.footer{{
    background:#ff4f93;
    color:white;
    text-align:center;
    padding:25px;
    font-size:34px;
    font-weight:bold;
}}

.circle{{
    display:inline-block;
    border:5px solid red;
    color:red;
    border-radius:50%;
    padding:12px 18px;
    font-size:28px;
    font-weight:bold;
    transform:rotate(-8deg);
    margin-bottom:15px;
}}

</style>

"""

# =========================================
# HTML
# =========================================

html_code = f"""

<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
{style}
</head>

<body>

<div class="wrapper">

<div class="header">

<div class="title">
📰 一果ちゃん新聞
</div>

<div class="date">
{race_date}<br>
{race_place}<br>
{race_no}
</div>

</div>

<div class="sub">
前日版
</div>

<div class="main">

<div class="left">

<div class="box">

{
''
if stamp == "なし"
else f'''
<div class="circle">
{stamp}
</div>
'''
}

<div style="
font-size:48px;
font-weight:bold;
color:#ff4f93;
">
{honmei}
</div>

<div class="score-row">
<div class="score-label">
イン逃げ期待度
</div>

<div class="score-value">
{nige_rate}%
</div>
</div>

<div class="score-row">
<div class="score-label">
場平均との差
</div>

<div class="score-up">
+{up_rate}%
</div>
</div>

</div>

<div class="grid">

<div class="boat">
<div class="boat-title">1号艇</div>
<div class="boat-text">{boat1}</div>
</div>

<div class="boat">
<div class="boat-title">2号艇</div>
<div class="boat-text">{boat2}</div>
</div>

<div class="boat">
<div class="boat-title">3号艇</div>
<div class="boat-text">{boat3}</div>
</div>

<div class="boat">
<div class="boat-title">4号艇</div>
<div class="boat-text">{boat4}</div>
</div>

<div class="boat">
<div class="boat-title">5号艇</div>
<div class="boat-text">{boat5}</div>
</div>

<div class="boat">
<div class="boat-title">6号艇</div>
<div class="boat-text">{boat6}</div>
</div>

</div>

</div>

<div class="right">

<div class="bar-box">

<div class="bar-title">
各艇評価
</div>

<div class="bar-row">
<div class="bar-label-inline">1号艇</div>
<div class="bar-bg-inline">
<div class="bar-fill-inline" style="width:{boat1_score}%;">
{boat1_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label-inline">2号艇</div>
<div class="bar-bg-inline">
<div class="bar-fill-inline" style="width:{boat2_score}%;">
{boat2_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label-inline">3号艇</div>
<div class="bar-bg-inline">
<div class="bar-fill-inline" style="width:{boat3_score}%;">
{boat3_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label-inline">4号艇</div>
<div class="bar-bg-inline">
<div class="bar-fill-inline" style="width:{boat4_score}%;">
{boat4_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label-inline">5号艇</div>
<div class="bar-bg-inline">
<div class="bar-fill-inline" style="width:{boat5_score}%;">
{boat5_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label-inline">6号艇</div>
<div class="bar-bg-inline">
<div class="bar-fill-inline" style="width:{boat6_score}%;">
{boat6_score}
</div>
</div>
</div>

</div>

<img class="character-img" src="{character_src}">

<div class="notice">
最終判断は直前版で公開！
</div>

<div class="notice">
波乱指数<br>
{wave}
</div>

<div class="fukidashi">

<div class="fuki-title">
一果のひとこと
</div>

<div>
{comment}
</div>

</div>

</div>

</div>

<div class="footer">
展示評価・補正展示タイムは直前版で公開！
</div>

</div>

</body>
</html>

"""

# =========================================
# 表示
# =========================================

html(
    html_code,
    height=1700,
    scrolling=True
)
