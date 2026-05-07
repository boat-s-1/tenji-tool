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

race_place = st.sidebar.text_input("レース場", "丸亀")
race_no = st.sidebar.text_input("レース番号", "1R")
race_date = st.sidebar.text_input("日付", "2026/05/05")

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
# 艇別データ
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
# HTML新聞
# ==================================

html_code = f"""
<!DOCTYPE html>
<html>
<head>

<style>

body {{
    background: #fff5f8;
    font-family: sans-serif;
}}

.wrapper {{
    width: 1000px;
    margin: auto;
    background: white;
    border: 5px solid #ff6ea8;
    border-radius: 25px;
    overflow: hidden;
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 4px solid #ff6ea8;
}}

.title {{
    font-size: 64px;
    font-weight: bold;
    color: #ff4f93;
}}

.date {{
    text-align: center;
    font-size: 32px;
    font-weight: bold;
}}

.sub {{
    padding: 15px 30px;
    font-size: 32px;
    color: #ff4f93;
    font-weight: bold;
}}

.main {{
    display: flex;
    padding: 20px;
}}

.left {{
    width: 65%;
}}

.right {{
    width: 35%;
    text-align: center;
}}

.mainbox {{
    border: 4px solid #ffb3cf;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
}}

.big {{
    font-size: 90px;
    color: #ff4f93;
    font-weight: bold;
}}

.up {{
    font-size: 56px;
    color: #44aa55;
    font-weight: bold;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 10px;
    margin-top: 20px;
}}

.boat {{
    border: 3px solid #ffd0e2;
    border-radius: 15px;
    padding: 15px;
    background: white;
    min-height: 140px;
}}

.boat-title {{
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 10px;
}}

.boat-text {{
    font-size: 28px;
}}

.comment {{
    margin-top: 20px;
    border: 3px solid #ffb3cf;
    border-radius: 20px;
    padding: 20px;
    font-size: 30px;
    line-height: 1.7;
}}

.footer {{
    margin-top: 20px;
    background: #ff4f93;
    color: white;
    text-align: center;
    padding: 20px;
    font-size: 36px;
    font-weight: bold;
}}

.notice {{
    margin-top: 20px;
    background: #fff3c4;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #ff4f93;
}}

img {{
    width: 90%;
    border-radius: 20px;
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
        前日版 - 一果のイン逃げ予想 -
    </div>

    <div class="main">

        <div class="left">

            <div class="mainbox">

                <div style="font-size:38px;font-weight:bold;color:#ff4f93;">
                    本命：{honmei}
                </div>

                <div style="margin-top:20px;font-size:40px;">
                    イン逃げ期待度
                </div>

                <div class="big">
                    {nige_rate}%
                </div>

                <div style="margin-top:20px;font-size:40px;">
                    場平均との差
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

            <div class="comment">

                <div style="font-size:36px;font-weight:bold;color:#ff4f93;">
                    一果のひとこと
                </div>

                <div style="margin-top:15px;">
                    {comment}
                </div>

            </div>

        </div>

        <div class="right">

            <img src="https://i.imgur.com/0y0y0y0.png">

            <div class="notice">
                最終判断は<br>
                直前版で公開！
            </div>

            <div class="notice">
                波乱指数<br>
                {wave}
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

# ==================================
# 表示
# ==================================

html(
    html_code,
    height=1800,
    scrolling=True
)
