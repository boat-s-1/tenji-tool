import streamlit as st
from streamlit.components.v1 import html

# ==================================
# ページ設定
# ==================================

st.set_page_config(
    page_title="一果ちゃん新聞",
    layout="wide"
)

# ==================================
# タイトル
# ==================================

st.title("競艇キャラ新聞ジェネレーター")

# ==================================
# サイドバー入力
# ==================================

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
    ["1号艇", "2号艇", "3号艇"]
)

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

comment = st.sidebar.text_area(
    "一果のひとこと",
    "1号艇のイン逃げ中心！でも2号艇の差しも怖い…！"
)

# ==================================
# 艇別コメント
# ==================================

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

# ==================================
# 艇評価バー
# ==================================

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

# ==================================
# HTMLコード
# ==================================

html_code = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<link href="https://fonts.googleapis.com/css2?family=Yomogi&display=swap" rel="stylesheet">

<style>

body {{
    background:#fffdf5;
    font-family:'Yomogi', cursive;
    padding:30px;
}}

.wrapper {{
    width:1000px;
    margin:auto;
    background:white;
    border:6px dashed #ff6ea8;
    border-radius:25px;
    overflow:hidden;
    box-shadow:0px 0px 20px rgba(0,0,0,0.1);
}}

.header {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:20px;
    border-bottom:5px dashed #ff6ea8;
}}

.title {{
    font-size:72px;
    font-weight:bold;
    color:#ff4f93;
    transform:rotate(-2deg);
    letter-spacing:3px;
    text-shadow:2px 2px 0px #ffd0e2;
}}

.date {{
    text-align:center;
    font-size:30px;
    font-weight:bold;
}}

.sub {{
    padding:20px 30px;
    font-size:36px;
    color:#ff4f93;
    font-weight:bold;
}}

.marker {{
    display:inline;
    background:linear-gradient(
        transparent 60%,
        #ffe066 60%
    );
}}

.main {{
    display:flex;
    padding:20px;
}}

.left {{
    width:65%;
}}

.right {{
    width:35%;
    text-align:center;
}}

.mainbox {{
    border:5px dashed #ffb3cf;
    border-radius:25px;
    padding:25px;
    margin-bottom:20px;
    background:#fffafb;
}}

.big {{
    font-size:100px;
    color:#ff4f93;
    font-weight:bold;
    transform:rotate(-2deg);
}}

.up {{
    font-size:60px;
    color:#44aa55;
    font-weight:bold;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:15px;
    margin-top:20px;
}}

.boat {{
    border:4px dashed #ffd0e2;
    border-radius:20px;
    padding:15px;
    background:white;
    min-height:140px;
}}

.boat-title {{
    font-size:34px;
    font-weight:bold;
    margin-bottom:10px;
}}

.boat-text {{
    font-size:28px;
}}

.fukidashi {{
    position:relative;
    background:#fff;
    border:4px dashed #ff6ea8;
    border-radius:25px;
    padding:25px;
    margin-top:20px;
    font-size:30px;
    line-height:1.7;
}}

.fukidashi:after {{
    content:'';
    position:absolute;
    top:100%;
    left:60px;
    border-width:18px;
    border-style:solid;
    border-color:#ff6ea8 transparent transparent transparent;
}}

.notice {{
    margin-top:20px;
    background:#fff3c4;
    border-radius:20px;
    padding:20px;
    text-align:center;
    font-size:36px;
    font-weight:bold;
    color:#ff4f93;
    border:4px dashed #ff6ea8;
}}

.circle {{
    display:inline-block;
    border:5px solid red;
    border-radius:50%;
    padding:10px 18px;
    transform:rotate(-8deg);
    font-size:36px;
    color:red;
    font-weight:bold;
    margin-bottom:15px;
}}

.alert {{
    background:red;
    color:white;
    font-size:42px;
    font-weight:bold;
    padding:20px;
    transform:rotate(-8deg);
    display:inline-block;
    margin-top:20px;
    border-radius:15px;
}}

.footer {{
    margin-top:20px;
    background:#ff4f93;
    color:white;
    text-align:center;
    padding:25px;
    font-size:40px;
    font-weight:bold;
}}

.bar-wrap {{
    margin-top:25px;
}}

.bar-row {{
    margin-bottom:18px;
}}

.bar-label {{
    font-size:30px;
    font-weight:bold;
    margin-bottom:5px;
}}

.bar-bg {{
    width:100%;
    height:38px;
    background:#ffe3ee;
    border-radius:20px;
    overflow:hidden;
    border:3px dashed #ffb3cf;
}}

.bar-fill {{
    height:100%;
    background:linear-gradient(
        90deg,
        #ff7eb3,
        #ff4f93
    );
    border-radius:20px;
    text-align:right;
    color:white;
    font-size:24px;
    font-weight:bold;
    padding-right:15px;
    line-height:38px;
}}

img {{
    width:90%;
    border-radius:20px;
    margin-top:20px;
}}

</style>

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
        <span class="marker">
            前日版 - 一果のイン逃げ予想 -
        </span>
    </div>

    <div class="main">

        <div class="left">

            <div class="mainbox">

                <div class="circle">
                    本命
                </div>

                <div style="font-size:42px;font-weight:bold;color:#ff4f93;">
                    {honmei}
                </div>

                <div style="margin-top:20px;font-size:40px;">
                    <span class="marker">
                        イン逃げ期待度
                    </span>
                </div>

                <div class="big">
                    {nige_rate}%
                </div>

                <div style="margin-top:20px;font-size:40px;">
                    <span class="marker">
                        場平均との差
                    </span>
                </div>

                <div class="up">
                    +{up_rate}%
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
                    font-size:42px;
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
                        <div class="bar-b
