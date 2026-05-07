import streamlit as st
from streamlit.components.v1 import html

# =========================================
# ページ設定
# =========================================

st.set_page_config(
    page_title="一果ちゃん新聞",
    layout="wide"
)

st.title("競艇キャラ新聞ジェネレーター")

# =========================================
# サイドバー
# =========================================

st.sidebar.header("レース入力")

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
        "波乱警報",
        "見",
        "見送り",
        "危険",
        "大荒れ注意"
    ]
)

# =========================================
# 警報スタンプ
# =========================================

alert_stamp = st.sidebar.selectbox(
    "警報スタンプ",
    [
        "なし",
        "波乱注意！",
        "波乱警報！",
        "大荒れ注意！",
        "高配当警戒！",
        "イン危険！",
        "展示急上昇！"
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
    "1号艇のイン逃げ中心！でも2号艇の差しも怖い…！"
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
    "厳しい"
)

boat6 = st.sidebar.text_input(
    "6号艇",
    "大穴注意"
)

# =========================================
# 艇評価バー
# =========================================

boat1_score = st.sidebar.slider(
    "1号艇 総合評価",
    0,
    100,
    88
)

boat2_score = st.sidebar.slider(
    "2号艇 総合評価",
    0,
    100,
    65
)

boat3_score = st.sidebar.slider(
    "3号艇 総合評価",
    0,
    100,
    52
)

boat4_score = st.sidebar.slider(
    "4号艇 総合評価",
    0,
    100,
    48
)

boat5_score = st.sidebar.slider(
    "5号艇 総合評価",
    0,
    100,
    35
)

boat6_score = st.sidebar.slider(
    "6号艇 総合評価",
    0,
    100,
    22
)

# =========================================
# 直前版入力
# =========================================

tenji_rank = st.sidebar.selectbox(
    "展示評価",
    ["S", "A", "B", "C"]
)

tenji_time = st.sidebar.text_input(
    "補正展示タイム",
    "6.71"
)

shinnyu = st.sidebar.text_input(
    "進入予想",
    "123/456"
)

kaime = st.sidebar.text_input(
    "推奨買い目",
    "1-2-3"
)

ai_mark = st.sidebar.text_input(
    "AI印",
    "◎1 ○2 ▲5"
)

# =========================================
# 共通CSS
# =========================================

common_style = """

<style>

body{
    background:#fffdf5;
    font-family:'Arial';
    padding:20px;
}

.wrapper{
    width:1000px;
    margin:auto;
    background:white;
    border:6px dashed #ff6ea8;
    border-radius:25px;
    overflow:hidden;
    box-shadow:0px 0px 20px rgba(0,0,0,0.1);
}

.header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:20px;
    border-bottom:5px dashed #ff6ea8;
}

.title{
    font-size:64px;
    font-weight:bold;
    color:#ff4f93;
}

.date{
    text-align:center;
    font-size:28px;
    font-weight:bold;
}

.sub{
    padding:20px;
    font-size:34px;
    color:#ff4f93;
    font-weight:bold;
}

.main{
    display:flex;
    gap:20px;
    padding:20px;
}

.left{
    width:65%;
}

.right{
    width:35%;
    text-align:center;
}

.mainbox{
    border:5px dashed #ffb3cf;
    border-radius:25px;
    padding:20px;
    margin-bottom:20px;
    background:#fffafb;
}

.circle{
    display:inline-block;
    border:5px solid red;
    border-radius:50%;
    padding:10px 18px;
    transform:rotate(-8deg);
    font-size:34px;
    color:red;
    font-weight:bold;
    margin-bottom:15px;
}

.score-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:20px;
    padding-bottom:12px;
    border-bottom:3px dashed #ffd0e2;
}

.score-label{
    font-size:36px;
    font-weight:bold;
    color:#ff4f93;
}

.score-value{
    font-size:52px;
    font-weight:bold;
    color:#ff4f93;
}

.score-up{
    font-size:48px;
    font-weight:bold;
    color:#44aa55;
}

.grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:15px;
    margin-top:20px;
}

.boat{
    border:4px dashed #ffd0e2;
    border-radius:20px;
    padding:15px;
    background:white;
}

.boat-title{
    font-size:30px;
    font-weight:bold;
}

.boat-text{
    font-size:22px;
    margin-top:8px;
}

.notice{
    margin-top:20px;
    background:#fff3c4;
    border-radius:20px;
    padding:20px;
    text-align:center;
    font-size:30px;
    font-weight:bold;
    color:#ff4f93;
    border:4px dashed #ff6ea8;
}

.alert{
    background:red;
    color:white;
    font-size:36px;
    font-weight:bold;
    padding:20px;
    transform:rotate(-8deg);
    display:inline-block;
    margin-top:20px;
    border-radius:15px;
}

.bar-wrap{
    margin-top:20px;
}

.bar-row{
    margin-bottom:15px;
}

.bar-label{
    font-size:26px;
    font-weight:bold;
}

.bar-bg{
    width:100%;
    height:36px;
    background:#ffe3ee;
    border-radius:20px;
    overflow:hidden;
}

.bar-fill{
    height:100%;
    background:linear-gradient(
        90deg,
        #ff7eb3,
        #ff4f93
    );
    border-radius:20px;
    text-align:right;
    color:white;
    font-size:22px;
    font-weight:bold;
    padding-right:12px;
    line-height:36px;
}

.fukidashi{
    background:#fff;
    border:4px dashed #ff6ea8;
    border-radius:25px;
    padding:18px;
    margin-top:20px;
    font-size:22px;
    line-height:1.7;
}

.footer{
    margin-top:20px;
    background:#ff4f93;
    color:white;
    text-align:center;
    padding:25px;
    font-size:34px;
    font-weight:bold;
}

img{
    width:90%;
    border-radius:20px;
    margin-top:20px;
}

</style>

"""

# =========================================
# 前日版HTML
# =========================================

html_code = f"""

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

{common_style}

</head>

<body>

<div class="wrapper">

<div class="header">

<div class="title">
一果ちゃん新聞
</div>

<div class="date">
{race_date}<br>
{race_place}<br>
{race_no}
</div>

</div>

<div class="sub">
📰 前日版
</div>

<div class="main">

<div class="left">

<div class="mainbox">

{
''
if stamp == "なし"
else f'''
<div class="circle">
{stamp}
</div>
'''
}

<div style="font-size:42px;font-weight:bold;color:#ff4f93;">
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

<div class="mainbox">

<div style="
font-size:40px;
font-weight:bold;
color:#ff4f93;
margin-bottom:20px;
">
艇評価ランキング
</div>

<div class="bar-wrap">

<div class="bar-row">
<div class="bar-label">1号艇</div>
<div class="bar-bg">
<div class="bar-fill" style="width:{boat1_score}%;">
{boat1_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label">2号艇</div>
<div class="bar-bg">
<div class="bar-fill" style="width:{boat2_score}%;">
{boat2_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label">3号艇</div>
<div class="bar-bg">
<div class="bar-fill" style="width:{boat3_score}%;">
{boat3_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label">4号艇</div>
<div class="bar-bg">
<div class="bar-fill" style="width:{boat4_score}%;">
{boat4_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label">5号艇</div>
<div class="bar-bg">
<div class="bar-fill" style="width:{boat5_score}%;">
{boat5_score}
</div>
</div>
</div>

<div class="bar-row">
<div class="bar-label">6号艇</div>
<div class="bar-bg">
<div class="bar-fill" style="width:{boat6_score}%;">
{boat6_score}
</div>
</div>
</div>

</div>

</div>

</div>

<div class="right">

<img src="https://placehold.co/400x600/png">

<div class="notice">
最終判断は<br>
直前版で公開！
</div>

<div class="notice">
波乱指数<br>
{wave}
</div>

<div class="fukidashi">

<div style="
font-size:30px;
font-weight:bold;
color:#ff4f93;
margin-bottom:10px;
">
一果のひとこと
</div>

<div>
{comment}
</div>

</div>

{
''
if alert_stamp == "なし"
else f'''
<div class="alert">
{alert_stamp}
</div>
'''
}

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
# 直前版HTML
# =========================================

html_code2 = f"""

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

{common_style}

</head>

<body>

<div class="wrapper">

<div class="header">

<div class="title">
🚨 一果 直前速報
</div>

<div class="date">
{race_date}<br>
{race_place}<br>
{race_no}
</div>

</div>

<div class="main">

<div class="left">

<div class="mainbox">

<div style="font-size:42px;font-weight:bold;color:#ff4f93;">
展示評価：{tenji_rank}
</div>

<div class="score-row">
<div class="score-label">
補正展示タイム
</div>

<div class="score-value">
{tenji_time}
</div>
</div>

<div class="score-row">
<div class="score-label">
進入予想
</div>

<div class="score-value">
{shinnyu}
</div>
</div>

<div class="score-row">
<div class="score-label">
AI印
</div>

<div class="score-value">
{ai_mark}
</div>
</div>

</div>

<div class="mainbox">

<div style="
font-size:42px;
font-weight:bold;
color:#ff4f93;
margin-bottom:15px;
">
推奨買い目
</div>

<div style="
font-size:72px;
font-weight:bold;
color:red;
text-align:center;
">
{kaime}
</div>

</div>

</div>

<div class="right">

<img src="https://placehold.co/400x600/png">

<div class="notice">
展示後更新！
</div>

<div class="notice">
波乱指数<br>
{wave}
</div>

{
''
if alert_stamp == "なし"
else f'''
<div class="alert">
{alert_stamp}
</div>
'''
}

</div>

</div>

<div class="footer">
直前情報は展示後更新！
</div>

</div>

</body>
</html>

"""

# =========================================
# タブ表示
# =========================================

tab1, tab2 = st.tabs(
    [
        "📰 前日版",
        "🚨 直前速報"
    ]
)

with tab1:

    html(
        html_code,
        height=1800,
        scrolling=True
    )

with tab2:

    html(
        html_code2,
        height=1400,
        scrolling=True
    )
