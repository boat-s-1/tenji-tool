import streamlit as st
from streamlit.components.v1 import html
import base64
# --- ロゴ画像の読み込み ---
import os

# 画像ファイルがスクリプトと同じフォルダにある場合
logo_path = "8c5a3a8d-fe42-4239-bfe9-c67326baa39a.png" # ここを実際のファイル名に合わせてください

# --- スタンプ画像の読み込み関数 ---
def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    return ""

# スタンプ画像のパスを指定（実際のファイル名に変更してください）
stamp_dict = {
    "本命": get_base64_img("a7105fda-9305-4e70-98eb-212c65842325.png"),
    "激アツ": get_base64_img("1a097861-b508-41d0-a3ea-ec276d1a4005.png"),
    "鉄板": get_base64_img("ac668bb2-8f4f-40c6-ab3f-a800c64a817c.png"),
    "穴狙い": get_base64_img("0c0491e6-0036-4e58-9e8b-c82f0a60bb80.png"),
    "見": get_base64_img("a6a958fc-8897-4e1b-8d5b-f28459220c26.png"),
    "危険": get_base64_img("ab68e233-d232-438b-8e50-e9d041eea1df.png"),
}

# --- ボート画像の読み込み ---
# ファイル名はご自身が保存したもの（例: boat1.png）に合わせてください
boat1_src = get_base64_img("IMG_4170.png") 
boat2_src = get_base64_img("IMG_4172.png") 
boat3_src = get_base64_img("IMG_4171.png")
boat4_src = get_base64_img("55e7bfa3-f032-45f8-ab82-0cd34799feb2.png")
boat5_src = get_base64_img("3e82f55c-1d03-46ce-a11f-9050f242877d.png")
boat6_src = get_base64_img("c81ee8e5-46b3-4526-bfee-3d6efdd0801b.png")

# ファイル名は保存したもの（例: footer_msg.png）に合わせてください
footer_img_src = get_base64_img("1b1a684d-c8bb-45fb-a123-0ed1b73c5046.png")




if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()
    logo_src = f"data:image/png;base64,{logo_base64}"
else:
    # 画像がない場合のバックアップ（空文字またはプレースホルダー）
    logo_src = "" 


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

hit_rate = st.sidebar.slider(
    "的中期待度",
    0,
    100,
    87
)

# =========================================
# コメント
# =========================================

comment = st.sidebar.text_area(
    "一果のひとこと",
    "1号艇中心だが2号艇の差し注意！"
)
# =========================================
# 展開ストーリー設定
# =========================================
st.sidebar.header("展開ストーリー設定")

# 注目する艇を最大3つまで選べるようにする
selected_boats = st.sidebar.multiselect(
    "注目する艇を選択（最大3つ）",
    ["1号艇", "2号艇", "3号艇", "4号艇", "5号艇", "6号艇"],
    default=["1号艇", "2号艇", "3号艇"] # 初期値
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
# サイドバーの「数値」セクションあたりに追加
st.sidebar.header("モーター評価")
motor_eval = st.sidebar.text_area(
    "モーター一言メモ",
    "1号艇は出足型、3号艇の伸びが節イチ級！",
    height=100
)

# =========================================
# 直前版
# =========================================

st.sidebar.header("直前版")

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

ikka_hantei = st.sidebar.text_input(
    "一果判定",
    "◎1 ○2 ▲5"
)

danger_boat = st.sidebar.selectbox(
    "危険艇",
    [
        "なし",
        "1号艇",
        "2号艇",
        "3号艇",
        "4号艇",
        "5号艇",
        "6号艇"
    ]
)

up_boat = st.sidebar.selectbox(
    "展示急上昇",
    [
        "なし",
        "1号艇",
        "2号艇",
        "3号艇",
        "4号艇",
        "5号艇",
        "6号艇"
    ]
)

jikkan_comment = st.sidebar.text_area(
    "直前コメント",
    "展示は1号艇優勢！ただ2号艇の差し残し注意！"
)

honmei_kaime = st.sidebar.text_input(
    "本命買い目",
    "1-2-3"
)

osae_kaime = st.sidebar.text_area(
    "押さえ買い目",
    "1-3-2\n1-2-5"
)

# =========================================
# CSS
# =========================================

common_style = f"""

<style>

body{{
    background:#fffdf5;
    padding:20px;
    font-family:'Arial';
    background-image:url('{bg_src}');
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}}


/* ダウンロードボタンのスタイル */
.download-btn {{
    display: block;
    width: 250px;
    margin: 20px auto;
    padding: 15px;
    background: #ff4f93;
    color: white;
    text-align: center;
    border-radius: 50px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    border: none;
    font-size: 18px;
}}
.download-btn:hover {{
    background: #ff7eb3;
}}



/* モーター評価ボックス */
.motor-box {{
    margin-top: 15px;
    background: #f0f9ff; /* 少し青みがかった爽やかな色 */
    border: 3px solid #7ec2ff;
    border-radius: 15px;
    padding: 15px;
    font-family: 'Zen Maru Gothic', sans-serif;
    text-align: left;
    box-shadow: 3px 3px 8px rgba(0,0,0,0.05);
}}

.motor-title {{
    font-size: 22px;
    font-weight: bold;
    color: #0077cc;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    border-bottom: 2px solid #b3d9ff;
}}


/* 見出しのデザイン：ピンク塗りつぶし ＋ 白文字 */
.section-title {{
    background: #ff4f93; /* 濃いめのピンク（赤） */
    color: white;
    font-size: 28px;
    font-weight: bold;
    padding: 8px 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    display: inline-block; /* 文字の長さに合わせる場合はこれ */
    width: auto;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    font-family: 'Zen Maru Gothic', sans-serif;
}}



/* 吹き出し本体 */
.fukidashi {{
    position: relative;
    background: #fff;
    border: 4px solid #ff6ea8;
    border-radius: 25px;
    padding: 20px;
    margin-top: -15px; /* キャラ画像と少し重ねる */
    z-index: 10;
    font-family: 'Zen Maru Gothic', sans-serif;
    font-size: 20px;
    line-height: 1.6;
    color: #444;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
}}

/* 吹き出しのしっぽ（外側のピンクの縁） */
.fukidashi::before {{
    content: "";
    position: absolute;
    top: -24px;
    left: 40px;
    border: 12px solid transparent;
    border-bottom: 12px solid #ff6ea8;
}}

/* 吹き出しのしっぽ（内側の白い塗り） */
.fukidashi::after {{
    content: "";
    position: absolute;
    top: -18px;
    left: 40px;
    border: 12px solid transparent;
    border-bottom: 12px solid #fff;
}}





/* 注目艇のスタイル */
.pickup-row {{
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    background: linear-gradient(90deg, #fff5f8 0%, #ffffff 100%);
    border-left: 8px solid #ff6ea8;
    border-radius: 8px;
    padding: 10px 15px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
}}

.boat-num {{
    background: #ff6ea8;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 22px;
    font-weight: bold;
    margin-right: 15px;
    flex-shrink: 0;
}}

.boat-comment {{
    font-size: 20px;
    color: #444;
    font-weight: bold;
}}


.wrapper{{
    width:1000px;
    margin:auto;
    background:rgba(255,255,255,0.94);
    border:6px dashed #ff6ea8;
    border-radius:25px;
    overflow:hidden;
    box-shadow:0px 0px 25px rgba(0,0,0,0.15);
}}

.wrapper-live{{
    width:1000px;
    margin:auto;
    background:rgba(255,240,247,0.96);
    border:6px dashed #ff4f93;
    border-radius:25px;
    overflow:hidden;
    box-shadow:0px 0px 25px rgba(255,105,180,0.3);
}}

.header{{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:20px;
    border-bottom:5px dashed #ff6ea8;
}}

.header-live{{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:20px;
    background:#ff4f93;
}}

.title{{
    font-size:64px;
    font-weight:bold;
    color:#ff4f93;
}}

.title-live{{
    font-size:64px;
    font-weight:bold;
    color:white;
    letter-spacing:2px;
}}

.date{{
    text-align:center;
    font-size:28px;
    font-weight:bold;
}}

.sub{{
    padding:20px;
    font-size:34px;
    color:#ff4f93;
    font-weight:bold;
}}

.main{{
    display:flex;
    gap:20px;
    padding:20px;
}}

.left{{
    width:65%;
}}

.right{{
    width:35%;
    text-align:center;
}}

.mainbox{{
    border:5px dashed #ffb3cf;
    border-radius:25px;
    padding:20px;
    margin-bottom:20px;
    background:#fffafb;
}}

.mainbox-live{{
    border:5px dashed #ff4f93;
    border-radius:25px;
    padding:20px;
    margin-bottom:20px;
    background:white;
}}

.circle{{
    display:inline-block;
    border:5px solid red;
    border-radius:50%;
    padding:10px 18px;
    transform:rotate(-8deg);
    font-size:34px;
    color:red;
    font-weight:bold;
    margin-bottom:15px;
}}

.score-row{{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:20px;
    padding-bottom:12px;
    border-bottom:3px dashed #ffd0e2;
}}

.score-label{{
    font-size:36px;
    font-weight:bold;
    color:#ff4f93;
}}

.score-value{{
    font-size:52px;
    font-weight:bold;
    color:#ff4f93;
}}

.score-up{{
    font-size:48px;
    font-weight:bold;
    color:#44aa55;
}}

.grid{{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:15px;
    margin-top:20px;
}}

.boat{{
    border:4px dashed #ffd0e2;
    border-radius:20px;
    padding:15px;
    background:white;
}}

.boat-title{{
    font-size:30px;
    font-weight:bold;
}}

.boat-text{{
    font-size:22px;
    margin-top:8px;
}}

/* 前日版・直前版共通のチェックポイント枠 */
.notice, .notice-live {{
    margin-top: 20px;
    background: #fff3c4; /* 前日版は黄色系 */
    border: 4px dashed #ff6ea8;
    border-radius: 20px;
    padding: 15px;
    text-align: left;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
}}

/* 直前版だけ少し色を変えるなら（ピンク系） */
.notice-live {{
    background: #ffe5f1;
    border: 4px dashed #ff4f93;
}}

.notice-title {{
    font-size: 24px;
    font-weight: bold;
    color: #ff4f93;
    text-align: center;
    border-bottom: 2px solid #ffb3cf;
    margin-bottom: 10px;
    padding-bottom: 5px;
    font-family: 'Zen Maru Gothic', sans-serif;
}}

.notice-item {{
    font-size: 18px;
    font-weight: bold;
    color: #555;
    margin-bottom: 8px;
    display: flex;
    flex-direction: column;
    font-family: 'Zen Maru Gothic', sans-serif;
}}

.notice-value {{
    font-size: 22px;
    color: #ff4f93;
    padding-left: 10px;
}}

.alert{{
    background:red;
    color:white;
    font-size:36px;
    font-weight:bold;
    padding:20px;
    transform:rotate(-8deg);
    display:inline-block;
    margin-top:20px;
    border-radius:15px;
}}

.bar-wrap{{
    margin-top:20px;
}}

.bar-row{{
    margin-bottom:15px;
}}

.bar-label{{
    font-size:26px;
    font-weight:bold;
}}

.bar-bg{{
    width:100%;
    height:36px;
    background:#ffe3ee;
    border-radius:20px;
    overflow:hidden;
}}

.bar-fill{{
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
}}

.fukidashi{{
    background:#fff;
    border:4px dashed #ff6ea8;
    border-radius:25px;
    padding:18px;
    margin-top:20px;
    font-size:22px;
    line-height:1.7;
}}

.fukidashi-live{{
    background:white;
    border:4px dashed #ff4f93;
    border-radius:25px;
    padding:18px;
    margin-top:20px;
    font-size:24px;
    line-height:1.8;
}}

.footer {{
    margin-top: 20px;
    background: transparent; /* 背景色を透明に */
    text-align: center;
    padding: 10px 0;
}}

.footer-img {{
    width: 100%;       /* 枠の幅いっぱいに広げる */
    max-width: 900px;  /* 大きすぎないように制限 */
    height: auto;
    border-radius: 10px;
}}

}}

.footer-live{{
    margin-top:20px;
    background:#ff4f93;
    color:white;
    text-align:center;
    padding:25px;
    font-size:38px;
    font-weight:bold;
}}

.character-img{{
    width:90%;
    border-radius:20px;
    margin-top:20px;
}}

.buy-box-live{{
    background:#fff3fa;
    border:5px dashed #ff4f93;
    border-radius:25px;
    padding:30px;
    margin-top:20px;
}}

.buy-title-live{{
    font-size:42px;
    font-weight:bold;
    color:#ff4f93;
    margin-bottom:15px;
    text-align:center;
}}

.buy-kaime-live{{
    font-size:110px;
    font-weight:bold;
    color:#ff4f93;
    text-align:center;
}}

.telop{{
    background:#ff85b5;
    color:white;
    padding:18px;
    font-size:32px;
    font-weight:bold;
    text-align:center;
}}

</style>

"""

# 艇ごとのコメントを辞書にしておく
all_boat_comments = {
    "1号艇": boat1,
    "2号艇": boat2,
    "3号艇": boat3,
    "4号艇": boat4,
    "5号艇": boat5,
    "6号艇": boat6
}

# =========================================
# 展開ストーリー生成ロジック (ここを修正します)
# =========================================

# 各艇の「画像」と「艇番カラー」を紐付けます
boat_info = {
    "1号艇": {"comment": boat1, "color": "#e2e2e2", "img": boat1_src}, # boat1_srcなどはコード上部で取得済み
    "2号艇": {"comment": boat2, "color": "#444444", "img": boat2_src},
    "3号艇": {"comment": boat3, "color": "#ff4444", "img": boat3_src},
    "4号艇": {"comment": boat4, "color": "#4444ff", "img": boat4_src},
    "5号艇": {"comment": boat5, "color": "#eeaa00", "img": boat5_src},
    "6号艇": {"comment": boat6, "color": "#22aa22", "img": boat6_src},
}

# 選択された艇だけをループして、HTMLを組み立てる
story_html = ""
for b_name in selected_boats:
    info = boat_info.get(b_name)
    
    # 修正ポイント：丸数字(boat-num)の代わりに <img> タグを入れました
    story_html += f"""
    <div class="pickup-row" style="border-left: 8px solid {info['color']};">
        <img src="{info['img']}" style="width: 80px; height: auto; margin-right: 15px;">
        <div class="boat-comment">{info['comment']}</div>
    </div>
    """


# 波乱指数（0-100）を星の数（1-5個）に変換する例
star_count = (wave // 20) + 1
stars = "⭐︎" * star_count

# 注目艇（展開ストーリーで選んだ艇など）を取得
attention_boats = ", ".join([b.replace("号艇", "") for b in selected_boats])


# --- 1. ダウンロードスクリプトを先に定義 ---
download_script = f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<div style="text-align:center; padding: 20px;">
    <button class="download-btn" id="save-btn">画像を保存する</button>
</div>
<script>
document.getElementById('save-btn').addEventListener('click', function() {{
    const target = document.querySelector('.wrapper') || document.querySelector('.wrapper-live');
    html2canvas(target, {{
        useCORS: true,
        scale: 2,
        backgroundColor: "#ffffff"
    }}).then(canvas => {{
        const link = document.createElement('a');
        link.download = 'ikka_newspaper_{race_place}_{race_no}.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    }});
}});
</script>
"""

# =========================================
# 前日版HTML (全体を整理)
# =========================================

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
                <div style="font-size:42px; font-weight:bold; color:#ff4f93; margin-left:10px;">
                    {honmei}
                </div>
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
                <div class="story-container">
                    {story_html}
                </div>
            </div>

            <div class="mainbox">
                <div class="section-title">各艇評価指数</div>
                <div class="bar-wrap">
                    <div class="bar-row">
                        <div class="bar-label">1号艇</div>
                        <div class="bar-bg"><div class="bar-fill" style="width:{boat1_score}%;">{boat1_score}</div></div>
                    </div>
                    <div class="bar-row">
                        <div class="bar-label">2号艇</div>
                        <div class="bar-bg"><div class="bar-fill" style="width:{boat2_score}%;">{boat2_score}</div></div>
                    </div>
                    <div class="bar-row">
                        <div class="bar-label">3号艇</div>
                        <div class="bar-bg"><div class="bar-fill" style="width:{boat3_score}%;">{boat3_score}</div></div>
                    </div>
                    <div class="bar-row">
                        <div class="bar-label">4号艇</div>
                        <div class="bar-bg"><div class="bar-fill" style="width:{boat4_score}%;">{boat4_score}</div></div>
                    </div>
                    <div class="bar-row">
                        <div class="bar-label">5号艇</div>
                        <div class="bar-bg"><div class="bar-fill" style="width:{boat5_score}%;">{boat5_score}</div></div>
                    </div>
                    <div class="bar-row">
                        <div class="bar-label">6号艇</div>
                        <div class="bar-bg"><div class="bar-fill" style="width:{boat6_score}%;">{boat6_score}</div></div>
                    </div>
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
                <div class="notice-item">・危険艇<span class="notice-value">{danger_boat if danger_boat != "なし" else "なし"}</span></div>
                <div class="notice-item">・注目艇<span class="notice-value">{attention_boats}</span></div>
            </div>
            <div class="motor-box">
                <div class="motor-title">⚙️ 一果の機力チェック</div>
                <div style="font-size: 18px; line-height: 1.5; color: #333; font-weight: bold;">{motor_eval}</div>
            </div>
        </div>
    </div>

    <div class="footer">
        <img src="{footer_img_src}" class="footer-img">
    </div>

</div> {download_script}

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

<div class="wrapper-live">

<div class="telop">
🌸 展示終了！一果の最終決定 🌸
</div>

<div class="header-live">

<div class="title-live">
🌸 一果の最終決定
</div>

<div class="date">
{race_date}<br>
{race_place}<br>
{race_no}
</div>

</div>

<div class="main">

<div class="left">

<div class="mainbox-live">

<div style="
font-size:44px;
font-weight:bold;
color:#ff4f93;
">
展示評価：{tenji_rank}
</div>

<div style="
font-size:34px;
margin-top:20px;
">
補正展示タイム：{tenji_time}
</div>

<div style="
font-size:34px;
margin-top:20px;
">
進入予想：{shinnyu}
</div>

<div style="
font-size:42px;
font-weight:bold;
color:#ff4f93;
margin-top:30px;
">
一果判定
</div>

<div style="
font-size:52px;
font-weight:bold;
margin-top:15px;
color:#ff4f93;
">
{ikka_hantei}
</div>

</div>

<div class="mainbox-live">

<div style="
font-size:38px;
font-weight:bold;
color:#ff4f93;
">
🎯 的中期待度
</div>

<div style="
font-size:88px;
font-weight:bold;
color:#ff4f93;
margin-top:15px;
">
{hit_rate}%
</div>

</div>

<div class="fukidashi-live">

<div style="
font-size:34px;
font-weight:bold;
color:#ff4f93;
margin-bottom:15px;
">
一果コメント
</div>

<div>
{jikkan_comment}
</div>

</div>



<div class="buy-box-live">

<div class="buy-title-live">
🌸 一果の買い目
</div>

<!-- 本命 -->
<div style="
font-size:34px;
font-weight:bold;
color:#ff4f93;
margin-top:20px;
text-align:center;
">
本命
</div>

<div style="
font-size:72px;
font-weight:bold;
color:#ff4f93;
text-align:center;
margin-bottom:20px;
">
{honmei_kaime}
</div>
<!-- 押さえ下ライン -->
<div style="
margin-top:15px;
border-top:3px dashed #ff9ac2;
"></div>
<!-- 押さえ（2列カードUI） -->
<div style="
font-size:34px;
font-weight:bold;
color:#ff4f93;
text-align:center;
margin-top:20px;
margin-bottom:10px;
">
押さえ
</div>

<div style="
display:grid;
grid-template-columns:1fr 1fr;
gap:12px;
padding:10px;
">

{''.join([
f"""
<div style="
background:#fff;
border:2px solid #ff9ac2;
border-radius:14px;
padding:10px;
font-size:30px;
font-weight:bold;
color:#666;
text-align:center;
box-shadow:0 2px 6px rgba(0,0,0,0.05);
">
{line}
</div>
"""
for line in osae_kaime.splitlines()
])}

</div>







</div>

</div>


<div class="right">

<img class="character-img" src="{character_src}">

<div class="notice-live">
波乱指数<br>
{wave}
</div>

<div class="notice-live">
展示急上昇<br>
{up_boat}
</div>

<div class="notice-live">
危険艇<br>
{danger_boat}
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
</div>
</div>

<div class="footer-live">
🌸 一果の最終判断公開中 🌸
</div>

</div>

</body>
</html>
"""

# =========================================
# タブ
# =========================================

tab1, tab2 = st.tabs(
    [
        "📰 前日版",
        "🌸 直前版"
    ]
)

with tab1:

    html(
        html_code,
        height=1900,
        scrolling=True
    )

with tab2:

    html(
        html_code2,
        height=1800,
        scrolling=True
    )
