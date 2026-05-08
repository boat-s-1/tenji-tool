import streamlit as st
from streamlit.components.v1 import html
import base64
import os

# =========================================
# 1. 画像読み込み・Base64変換関数
# =========================================
def get_base64_img(path):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{data}"
    except Exception:
        pass
    return ""

# --- 各種画像の読み込み ---
logo_path = "8c5a3a8d-fe42-4239-bfe9-c67326baa39a.png"
logo_src = get_base64_img(logo_path)

stamp_dict = {
    "本命": get_base64_img("a7105fda-9305-4e70-98eb-212c65842325.png"),
    "激アツ": get_base64_img("1a097861-b508-41d0-a3ea-ec276d1a4005.png"),
    "鉄板": get_base64_img("ac668bb2-8f4f-40c6-ab3f-a800c64a817c.png"),
    "穴狙い": get_base64_img("0c0491e6-0036-4e58-9e8b-c82f0a60bb80.png"),
    "見": get_base64_img("a6a958fc-8897-4e1b-8d5b-f28459220c26.png"),
    "危険": get_base64_img("ab68e233-d232-438b-8e50-e9d041eea1df.png"),
}

boat_srcs = {
    "1号艇": get_base64_img("IMG_4170.png"),
    "2号艇": get_base64_img("IMG_4172.png"),
    "3号艇": get_base64_img("IMG_4171.png"),
    "4号艇": get_base64_img("55e7bfa3-f032-45f8-ab82-0cd34799feb2.png"),
    "5号艇": get_base64_img("3e82f55c-1d03-46ce-a11f-9050f242877d.png"),
    "6号艇": get_base64_img("c81ee8e5-46b3-4526-bfee-3d6efdd0801b.png"),
}

footer_img_src = get_base64_img("1b1a684d-c8bb-45fb-a123-0ed1b73c5046.png")

# =========================================
# 2. ユーザー入力（サイドバー）
# =========================================
st.set_page_config(page_title="一果＆キイナ新聞", layout="wide")
st.title("🌸⚡ 新聞ジェネレーター (一果 & キイナ)")

# --- レース基本情報 ---
with st.sidebar.expander("📌 レース基本情報", expanded=True):
    race_place = st.text_input("レース場", "丸亀")
    race_no = st.text_input("レース番号", "1R")
    race_date = st.text_input("日付", "2026/05/05")
    uploaded_character = st.file_uploader("キャラ画像", type=["png", "jpg", "jpeg"])
    character_src = f"data:image/png;base64,{base64.b64encode(uploaded_character.read()).decode()}" if uploaded_character else "https://placehold.co/500x900/png"

# --- 共通評価 ---
with st.sidebar.expander("📊 評価・判定"):
    hit_rate = st.slider("的中期待度", 0, 100, 87)
    wave = st.slider("波乱指数 (★数に影響)", 0, 100, 28)
    danger_boat = st.selectbox("危険艇", ["なし"] + [f"{i}号艇" for i in range(1, 7)])
    up_boat = st.selectbox("展示急上昇", ["なし"] + [f"{i}号艇" for i in range(1, 7)])

# --- 🌸 一果ちゃん専用 ---
with st.sidebar.expander("🌸 一果ちゃん設定"):
    honmei = st.selectbox("一果の本命", [f"{i}号艇" for i in range(1, 7)], index=0)
    stamp = st.selectbox("スタンプ", ["なし"] + list(stamp_dict.keys()))
    nige_rate = st.slider("イン逃げ期待度", 0, 100, 84)
    up_rate = st.slider("場平均との差", -30, 30, 11)
    comment = st.text_area("一果のひとこと", "1号艇中心だが2号艇の差し注意！")
    ikka_hantei = st.text_input("一果最終判定", "◎1 ○2 ▲5")
    honmei_kaime = st.text_input("一果 本命買い目", "1-2-3")
    osae_kaime = st.text_area("一果 押さえ買い目", "1-3-2\n1-2-5")

# --- ⚡ キイナちゃん専用 ---
with st.sidebar.expander("⚡ キイナちゃん設定"):
    kiina_honmei = st.selectbox("キイナの本命", [f"{i}号艇" for i in range(1, 7)], index=4)
    kiina_atama_rate = st.slider("本命アタマ期待度", 0, 100, 72)
    kiina_story = st.text_area("キイナ展開解説", "・1号艇が流れる展開！\n・5号艇のまくり差し炸裂！\n・2号艇が差して続く！")
    kiina_comment = st.text_area("キイナのひとこと", "今日は5コースが超怪しい！万舟狙うならここ！")
    kiina_hantei = st.text_input("キイナ最終判定", "◎5 ○2 ▲1")
    kiina_honmei_kaime = st.text_input("キイナ 本命買い目", "5-2-1")
    kiina_osae_list = st.text_area("キイナ 押さえ(4つ)", "5-1-2\n5-2-4\n5-1-4\n5-2-6")

# --- 展示・機力 ---
with st.sidebar.expander("⚙️ 展示・機力チェック"):
    tenji_rank = st.selectbox("展示評価", ["S", "A", "B", "C"])
    tenji_time = st.text_input("補正タイム", "6.71")
    shinnyu = st.text_input("進入予想", "123/456")
    motor_eval = st.text_area("機力チェック内容", "1号艇は出足型、3号艇の伸びが節イチ級！")

# 各艇スコア設定
with st.sidebar.expander("🔢 各艇の評価指数"):
    boat_scores = {}
    for i in range(1, 7):
        boat_scores[f"{i}号艇"] = st.slider(f"{i}号艇 評価", 0, 100, 50)

# =========================================
# 3. CSS / JS
# =========================================
common_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700&display=swap');
body { background:#fffdf5; padding:20px; font-family:'Arial'; }
.wrapper, .wrapper-live { width:1000px; margin:auto; background:rgba(255,255,255,0.94); border:6px dashed #ff6ea8; border-radius:25px; overflow:visible; position: relative; }
.main { display:flex; gap:20px; padding:20px; }
.left { width:65%; }
.right { width:35%; text-align:center; }
.mainbox { border:5px dashed #ffb3cf; border-radius:25px; padding:20px; margin-bottom:20px; background:#fffafb; }
.section-title { background:#ff4f93; color:white; font-size:26px; font-weight:bold; padding:8px 15px; border-radius:8px; margin-bottom:15px; display:inline-block; }
.character-img { width:100%; max-width:320px; }
.fukidashi { position:relative; background:#fff; border:4px solid #ff6ea8; border-radius:25px; padding:20px; margin-top:20px; font-size:20px; line-height:1.6; }
.notice { margin-top:20px; background:#fff3c4; border:4px dashed #ff6ea8; border-radius:20px; padding:15px; text-align:left; }
.bar-bg { width:100%; height:30px; background:#ffe3ee; border-radius:15px; overflow:hidden; margin-top:5px; }
.bar-fill { height:100%; background:linear-gradient(90deg, #ff7eb3, #ff4f93); color:white; text-align:right; padding-right:10px; line-height:30px; font-weight:bold; }
.download-btn { display:block; width:220px; margin:20px auto; padding:15px; background:#ff4f93; color:white; border:none; border-radius:50px; font-size:18px; font-weight:bold; cursor:pointer; }
.wrapper-kiina { width:1000px; margin:auto; background:linear-gradient(180deg, #fff8d9 0%, #fffdf5 100%); border:6px solid #ffb300; border-radius:25px; position:relative; }
.kiina-title { font-size:54px; font-weight:bold; color:#ff9800; text-shadow: 2px 2px #fff; }
.kiina-box { border:4px solid #ffca28; border-radius:25px; background:white; padding:20px; margin-bottom:20px; text-align:left; }
.kiina-section { background:linear-gradient(90deg, #ffb300, #ff9800); color:white; font-size:24px; font-weight:bold; padding:10px 18px; border-radius:10px; display:inline-block; margin-bottom:15px; }
.warning-box { background:linear-gradient(135deg, #ff5722, #ff9800); color:white; border-radius:20px; padding:20px; font-size:26px; font-weight:bold; text-align:center; }
.buy-card { background:white; border:3px solid #ffb300; border-radius:15px; padding:15px; text-align:center; font-size:34px; font-weight:bold; color:#ff9800; }
</style>
"""

download_logic = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function saveImage(targetClass, fileName) {
    const target = document.querySelector(targetClass);
    html2canvas(target, { useCORS: true, scale: 2, backgroundColor: "#ffffff" }).then(canvas => {
        const link = document.createElement('a');
        link.download = fileName;
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
}
</script>
"""

# =========================================
# 4. パーツ生成
# =========================================
stars = "⭐" * ((wave // 20) + 1)
current_stamp_src = stamp_dict.get(stamp, "")
stamp_html = f'<img src="{current_stamp_src}" style="width: 200px; position: absolute; right: 20px; top: -30px; transform: rotate(-15deg); z-index: 100;">' if current_stamp_src else ""

score_html = "".join([f'<div style="margin-bottom:10px;"><div style="font-weight:bold;">{k}</div><div class="bar-bg"><div class="bar-fill" style="width:{v}%;">{v}</div></div></div>' for k, v in boat_scores.items()])

# --- 🌸 一果 前日HTML ---
html_ikka_zenjitsu = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper">
    <div style="display:flex; justify-content:center; align-items:center; padding:20px; border-bottom:5px dashed #ff6ea8;">
        <img src="{logo_src}" style="width:100%; max-width:650px;">
        <div style="position:absolute; right:20px; font-size:22px; font-weight:bold; text-align:center;">{race_date}<br>{race_place}<br>{race_no}</div>
    </div>
    <div class="main">
        <div class="left">
            <div class="mainbox" style="position:relative;">{stamp_html}
                <div class="section-title">本命候補</div>
                <div style="font-size:40px; font-weight:bold; color:#ff4f93;">{honmei}</div>
                <div style="display:flex; justify-content:space-between; border-bottom:2px dashed #ffd0e2; padding:10px 0;"><span>イン逃げ期待度</span><span style="font-size:30px; color:#ff4f93;">{nige_rate}%</span></div>
            </div>
            <div class="mainbox"><div class="section-title">各艇評価指数</div>{score_html}</div>
        </div>
        <div class="right">
            <img class="character-img" src="{character_src}">
            <div class="fukidashi"><b>🌸 一果のひとこと</b><br>{comment}</div>
            <div class="notice">📍 <b>要チェック</b><br>・波乱指数: {stars}<br>・危険艇: {danger_boat}</div>
        </div>
    </div>
</div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper', 'ikka_zenjitsu.png')">保存</button></div></body></html>
"""

# --- ⚡ キイナ 前日HTML ---
kiina_osae_html = "".join([f'<div class="buy-card" style="font-size:24px; padding:10px;">{line}</div>' for line in kiina_osae_list.split("\n") if line])

html_kiina_zenjitsu = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper-kiina">
    <div style="background:#ffb300; padding:20px; display:flex; justify-content:space-between; align-items:center;">
        <div class="kiina-title">⚡ キイナの穴狙い速報</div>
        <div style="color:white; font-weight:bold;">{race_date} {race_place} {race_no}</div>
    </div>
    <div class="main">
        <div class="left">
            <div class="kiina-box">
                <div class="kiina-section">⚡ 本命候補</div>
                <div style="font-size:60px; font-weight:bold; color:#ff9800; text-align:center;">◎{kiina_honmei}</div>
                <div style="text-align:center; font-size:24px;">期待度: {kiina_atama_rate}%</div>
            </div>
            <div class="kiina-box">
                <div class="kiina-section">⚡ 展開ストーリー</div>
                <div style="font-size:22px; line-height:1.8; font-weight:bold;">{kiina_story.replace('\\n', '<br>')}</div>
            </div>
            <div class="warning-box">🚨 イン危険警報発令中 🚨</div>
        </div>
        <div class="right">
            <img class="character-img" src="{character_src}">
            <div class="fukidashi" style="border-color:#ffb300;"><b>⚡ キイナのひとこと</b><br>{kiina_comment}</div>
        </div>
    </div>
</div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper-kiina', 'kiina_zenjitsu.png')" style="background:#ff9800;">保存</button></div></body></html>
"""

# --- 展示・直前版のHTMLも同様に変数を反映 ---
# (コードが長くなりすぎるため、タブ表示部分へ)

# =========================================
# 5. メインタブ表示
# =========================================
tab_ikka, tab_kiina = st.tabs(["🌸 一果ちゃん", "⚡ キイナちゃん"])

with tab_ikka:
    s1, s2 = st.tabs(["📰 前日版", "🌸 直前版"])
    with s1:
        html(html_ikka_zenjitsu, height=1500, scrolling=True)
    with s2:
        # 直前版は ikka_hantei, hit_rate などを反映
        st.write("※直前版のHTML（前回の構成）をここに表示")

with tab_kiina:
    k1, k2 = st.tabs(["⚡ 前日版", "⚡ 直前版"])
    with k1:
        html(html_kiina_zenjitsu, height=1500, scrolling=True)
    with k2:
        # キイナ直前版
        kiina_live_html = f"""
        <!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
        <body><div class="wrapper-kiina">
            <div style="background:linear-gradient(90deg, #ff9800, #ff5722); color:white; text-align:center; padding:15px; font-size:28px; font-weight:bold;">⚡ キイナ最終決断 ⚡</div>
            <div class="main">
                <div class="left">
                    <div class="kiina-box"><div class="kiina-section">⚡ 最終判定</div><div style="font-size:50px; font-weight:bold; color:#ff9800; text-align:center;">{kiina_hantei}</div></div>
                    <div class="kiina-box"><div class="kiina-section">🎯 買い目</div><div style="font-size:60px; font-weight:bold; color:#ff5722; text-align:center;">{kiina_honmei_kaime}</div><div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px;">{kiina_osae_html}</div></div>
                </div>
                <div class="right">
                    <img class="character-img" src="{character_src}">
                    <div class="kiina-box" style="text-align:center;"><div class="kiina-section">期待度</div><div style="font-size:60px; font-weight:bold; color:#ff5722;">{hit_rate}%</div></div>
                </div>
            </div>
        </div></body></html>
        """
        html(kiina_live_html, height=1500, scrolling=True)
