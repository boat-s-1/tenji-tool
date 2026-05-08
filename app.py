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
st.set_page_config(page_title="一果ちゃん新聞", layout="wide")
st.title("🌸 一果ちゃん新聞ジェネレーター")

with st.sidebar.expander("📌 レース基本情報"):
    race_place = st.text_input("レース場", "丸亀")
    race_no = st.text_input("レース番号", "1R")
    race_date = st.text_input("日付", "2026/05/05")
 


with st.sidebar.expander("📌 一果画像"):
    uploaded_character = st.file_uploader("キャラ画像", type=["png", "jpg", "jpeg"])
    uploaded_bg = st.file_uploader("背景画像", type=["png", "jpg", "jpeg"])

# 画像のBase64化
if uploaded_character:
    character_src = f"data:image/png;base64,{base64.b64encode(uploaded_character.read()).decode()}"
else:
    character_src = "https://placehold.co/500x900/png"

with st.sidebar.expander("📌 一果本命候補"):
    honmei = st.selectbox("本命", [f"{i}号艇" for i in range(1, 7)])
    stamp = st.selectbox("スタンプ", ["なし"] + list(stamp_dict.keys()))
    nige_rate = st.slider("イン逃げ期待度", 0, 100, 84)
    up_rate = st.slider("場平均との差", -30, 30, 11)
    
wave = st.sidebar.slider("波乱指数", 0, 100, 28)

comment = st.sidebar.text_area("一果のひとこと", "1号艇中心だが2号艇の差し注意！")

with st.sidebar.expander("📌 一果展開ストーリー評価"):
    selected_boats = st.multiselect("注目艇", [f"{i}号艇" for i in range(1, 7)], default=["1号艇", "2号艇", "3号艇"])

    boat_comments = {}
    boat_scores = {}
    for i in range(1, 7):
       name = f"{i}号艇"
       boat_comments[name] = st.sidebar.text_input(f"{name} コメント", f"{name}の展開解説")
       boat_scores[name] = st.sidebar.slider(f"{name} 評価", 0, 100, 50)

motor_eval = st.sidebar.text_area("機力チェック", "1号艇は出足型、3号艇の伸びが節イチ級！", height=100)

st.sidebar.header("直前情報")
tenji_rank = st.sidebar.selectbox("展示評価", ["S", "A", "B", "C"])
tenji_time = st.sidebar.text_input("補正タイム", "6.71")
shinnyu = st.sidebar.text_input("進入予想", "123/456")
ikka_hantei = st.sidebar.text_input("一果判定", "◎1 ○2 ▲5")
danger_boat = st.sidebar.selectbox("危険艇", ["なし"] + [f"{i}号艇" for i in range(1, 7)])
up_boat = st.sidebar.selectbox("展示急上昇", ["なし"] + [f"{i}号艇" for i in range(1, 7)])
jikkan_comment = st.sidebar.text_area("直前コメント", "展示は1号艇優勢！")
honmei_kaime = st.sidebar.text_input("本命買い目", "1-2-3")
osae_kaime = st.sidebar.text_area("押さえ買い目", "1-3-2\n1-2-5")
hit_rate = st.sidebar.slider("的中期待度", 0, 100, 87)
# =========================================
# 3. CSS/JavaScript (f-stringの競合回避)
# =========================================

common_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700&display=swap');
body { background:#fffdf5; padding:20px; font-family:'Arial'; }
.wrapper, .wrapper-live { width:1000px; margin:auto; background:rgba(255,255,255,0.94); border:6px dashed #ff6ea8; border-radius:25px; overflow:visible; position: relative; }
.main { display:flex; gap:20px; padding:20px; }
.left { width:65%; }
.right { width:35%; text-align:center; }
.mainbox, .mainbox-live { border:5px dashed #ffb3cf; border-radius:25px; padding:20px; margin-bottom:20px; background:#fffafb; }
.section-title { background:#ff4f93; color:white; font-size:26px; font-weight:bold; padding:8px 15px; border-radius:8px; margin-bottom:15px; display:inline-block; }
.character-img { width:100%; max-width:320px; }
.pickup-row { display:flex; align-items:center; margin-bottom:12px; background: linear-gradient(90deg, #fff5f8 0%, #ffffff 100%); border-left:8px solid #ff6ea8; border-radius:8px; padding:10px; }
.fukidashi { position:relative; background:#fff; border:4px solid #ff6ea8; border-radius:25px; padding:20px; margin-top:20px; font-size:20px; line-height:1.6; }
.notice { margin-top:20px; background:#fff3c4; border:4px dashed #ff6ea8; border-radius:20px; padding:15px; }
.motor-box { margin-top:15px; background:#f0f9ff; border:3px solid #7ec2ff; border-radius:15px; padding:15px; }
.bar-bg { width:100%; height:30px; background:#ffe3ee; border-radius:15px; overflow:hidden; margin-top:5px; }
.bar-fill { height:100%; background:linear-gradient(90deg, #ff7eb3, #ff4f93); color:white; text-align:right; padding-right:10px; line-height:30px; font-weight:bold; }
.footer { text-align:center; padding:20px; }
.footer-img { width:100%; max-width:900px; }
.download-btn { display:block; width:220px; margin:20px auto; padding:15px; background:#ff4f93; color:white; border:none; border-radius:50px; font-size:18px; font-weight:bold; cursor:pointer; }
.wrapper-kiina { width:1000px; margin:auto; background:linear-gradient(180deg, #fff8d9 0%, #fffdf5 100%); border:6px solid #ffb300; border-radius:25px; overflow:visible; position:relative; box-shadow:0 0 30px rgba(255,179,0,0.3); }
.kiina-title { font-size:54px; font-weight:bold; color:#ff9800; text-shadow: 2px 2px 0px #fff, 4px 4px 10px rgba(0,0,0,0.15); }
.kiina-box { border:4px solid #ffca28; border-radius:25px; background:white; padding:20px; margin-bottom:20px; }
.kiina-section { background:linear-gradient(90deg, #ffb300, #ff9800); color:white; font-size:24px; font-weight:bold; padding:10px 18px; border-radius:10px; display:inline-block; margin-bottom:15px; }
.warning-box { background:linear-gradient(135deg, #ff5722, #ff9800); color:white; border-radius:20px; padding:20px; margin-top:20px; font-size:26px; font-weight:bold; text-align:center; box-shadow:0 0 15px rgba(255,87,34,0.35); }
.buy-card { background:white; border:3px solid #ffb300; border-radius:15px; padding:15px; text-align:center; font-size:34px; font-weight:bold; color:#ff9800; }
.buy-grid { display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:15px; }
</style>
"""

download_logic = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function saveImage(targetClass, fileName) {
    const target = document.querySelector(targetClass);
    html2canvas(target, {
        useCORS: true,
        scale: 2,
        backgroundColor: "#ffffff"
    }).then(canvas => {
        const link = document.createElement('a');
        link.download = fileName;
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
}
</script>
"""

# =========================================
# 4. パーツ組み立て
# =========================================

header_part = f"""
<div class="header" style="display: flex; justify-content: center; position: relative; align-items: center; padding: 20px; border-bottom: 5px dashed #ff6ea8;">
    <img src="{logo_src}" style="width: 100%; max-width: 650px;">
    <div style="position: absolute; right: 20px; font-size: 22px; font-weight: bold; text-align: center;">{race_date}<br>{race_place}<br>{race_no}</div>
</div>
"""

stars = "⭐" * ((wave // 20) + 1)
attention_boats = ", ".join([b.replace("号艇", "") for b in selected_boats])
current_stamp_src = stamp_dict.get(stamp, "")
stamp_html = f'<img src="{current_stamp_src}" style="width: 200px; position: absolute; right: 20px; top: -30px; transform: rotate(-15deg); z-index: 100; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.1));">' if current_stamp_src else ""

boat_info_map = {"1号艇": "#e2e2e2", "2号艇": "#444444", "3号艇": "#ff4444", "4号艇": "#4444ff", "5号艇": "#eeaa00", "6号艇": "#22aa22"}
story_html = "".join([f'<div class="pickup-row" style="border-left: 8px solid {boat_info_map[b]};"><img src="{boat_srcs[b]}" style="width: 70px; margin-right: 15px;"><div style="font-size:20px; font-weight:bold;">{boat_comments[b]}</div></div>' for b in selected_boats])

score_html = ""
for i in range(1, 7):
    score = boat_scores[f"{i}号艇"]
    score_html += f"""
    <div style="margin-bottom:10px;">
        <div style="font-weight:bold;">{i}号艇</div>
        <div class="bar-bg"><div class="bar-fill" style="width:{score}%;">{score}</div></div>
    </div>
    """

# =========================================
# 5. 各種HTML文字列作成
# =========================================

# --- 一果 前日 ---
html_code = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper">{header_part}<div class="main"><div class="left"><div class="mainbox" style="position: relative;">{stamp_html}<div class="section-title">本命候補</div><div style="font-size:40px; font-weight:bold; color:#ff4f93; margin-left:10px;">{honmei}</div><div style="display:flex; justify-content:space-between; border-bottom:3px dashed #ffd0e2; padding:10px 0;"><div style="font-size:24px; font-weight:bold;">イン逃げ期待度</div><div style="font-size:40px; font-weight:bold; color:#ff4f93;">{nige_rate}%</div></div><div style="display:flex; justify-content:space-between; padding:10px 0;"><div style="font-size:24px; font-weight:bold;">場平均との差</div><div style="font-size:36px; font-weight:bold; color:#44aa55;">+{up_rate}%</div></div></div><div class="mainbox"><div class="section-title">展開ストーリー (予想)</div>{story_html}</div><div class="mainbox"><div class="section-title">各艇評価指数</div>{score_html}</div></div><div class="right"><img class="character-img" src="{character_src}"><div class="fukidashi"><div style="color:#ff4f93; font-weight:bold; font-size:24px; margin-bottom:5px;">🌸 一果のひとこと</div>{comment}</div><div class="notice"><div style="font-size:22px; font-weight:bold; color:#ff4f93; text-align:center; border-bottom:2px solid #ffb3cf; margin-bottom:10px;">📍 要チェックポイント</div><div>・波乱指数：{stars} ({wave})</div><div>・危険艇：{danger_boat}</div><div>・注目艇：{attention_boats}</div></div><div class="motor-box"><div style="font-size:20px; font-weight:bold; color:#0077cc; border-bottom:2px solid #b3d9ff; margin-bottom:8px;">⚙️ 一果の機力チェック</div><div style="font-weight:bold; font-size:18px;">{motor_eval}</div></div></div></div><div class="footer"><img src="{footer_img_src}" class="footer-img"></div></div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper', 'zenjitsu.png')">画像を保存する</button></div></body></html>
"""

# --- 一果 直前 ---
html_code2 = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper-live"><div style="background:#ff85b5; color:white; padding:18px; font-size:32px; font-weight:bold; text-align:center;">🌸 展示終了！一果の最終決定 🌸</div>{header_part}<div class="main"><div class="left"><div class="mainbox" style="border-color:#ff4f93;"><div style="font-size:32px; font-weight:bold; color:#ff4f93;">展示評価：{tenji_rank}</div><div style="font-size:24px;">タイム：{tenji_time} / 進入：{shinnyu}</div><div style="font-size:36px; font-weight:bold; color:#ff4f93; margin-top:15px;">一果判定：{ikka_hantei}</div></div><div class="mainbox" style="border-color:#ff4f93;"><div style="font-size:28px; font-weight:bold;">🎯 的中期待度</div><div style="font-size:72px; font-weight:bold; color:#ff4f93;">{hit_rate}%</div></div><div class="mainbox" style="border-color:#ff4f93;"><div class="section-title">🌸 一果の買い目</div><div style="font-size:24px; font-weight:bold; color:#ff4f93; text-align:center;">本命：{honmei_kaime}</div><div style="border-top:2px dashed #ffb3cf; margin:10px 0;"></div><div style="font-size:20px; text-align:center; color:#666;">押さえ：<br>{osae_kaime.replace('\\n', '<br>')}</div></div></div><div class="right"><img class="character-img" src="{character_src}"><div class="notice" style="background:#ffe5f1; border-color:#ff4f93;"><div style="font-size:22px; font-weight:bold; color:#ff4f93; text-align:center; border-bottom:2px solid #ffb3cf; margin-bottom:10px;">📍 直前チェック</div><div>・急上昇：{up_boat}</div><div>・危険艇：{danger_boat}</div></div><div class="fukidashi" style="margin-top:20px;">{jikkan_comment}</div></div></div><div style="background:#ff4f93; color:white; text-align:center; padding:20px; font-size:24px; font-weight:bold;">🌸 一果の最終判断公開中 🌸</div></div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper-live', 'chokuzen.png')">画像を保存する</button></div></body></html>
"""

# --- キイナ 前日 ---
kiina_html = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper-kiina"><div style="background:linear-gradient(90deg, #ffb300, #ff9800); padding:25px; display:flex; justify-content:space-between; align-items:center;"><div class="kiina-title">⚡ キイナの5アタマ速報</div><div style="font-size:24px; font-weight:bold; text-align:right; color:white;">{race_date}<br>{race_place}<br>{race_no}</div></div><div class="main"><div class="left"><div class="kiina-box"><div class="kiina-section">⚡ 本命候補</div><div style="font-size:88px; font-weight:bold; color:#ff9800; text-align:center; margin-top:10px;">◎5号艇</div><div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:20px;"><div style="background:#fff8e1; border-radius:15px; padding:15px; text-align:center;"><div style="font-size:22px; font-weight:bold;">5アタマ期待度</div><div style="font-size:54px; font-weight:bold; color:#ff9800;">72%</div></div><div style="background:#fff8e1; border-radius:15px; padding:15px; text-align:center;"><div style="font-size:22px; font-weight:bold;">波乱指数</div><div style="font-size:54px; font-weight:bold; color:#ff5722;">{wave}</div></div></div></div><div class="kiina-box"><div class="kiina-section">⚡ 展開ストーリー</div><div style="font-size:28px; line-height:2; font-weight:bold;">・1号艇が流れる展開！<br>・5号艇のまくり差し炸裂！<br>・2号艇が差して続く！</div></div><div class="warning-box">🚨 イン危険警報発令中 🚨</div></div><div class="right"><img class="character-img" src="{character_src}"><div class="fukidashi" style="border-color:#ffb300; background:#fffdf3;"><div style="color:#ff9800; font-size:26px; font-weight:bold; margin-bottom:10px;">⚡ キイナのひとこと</div><div style="font-size:22px; font-weight:bold; line-height:1.8;">今日は5コースが超怪しい！ 万舟狙うならここ！</div></div><div class="notice" style="background:#fff3cd; border-color:#ffb300;"><div style="font-size:24px; font-weight:bold; color:#ff9800; margin-bottom:10px;">⚡ 要チェック</div><div style="font-size:20px; line-height:1.8;">・超抜候補：5号艇<br>・展示急上昇：{up_boat}<br>・危険艇：{danger_boat}</div></div></div></div><div style="background:#ff9800; color:white; text-align:center; padding:25px; font-size:32px; font-weight:bold;">⚡ 高配当を掴み取れ！</div></div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper-kiina', 'kiina_zenjitsu.png')">画像を保存する</button></div></body></html>
"""

# --- キイナ 直前 ---
kiina_live_html = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper-kiina"><div style="background:linear-gradient(90deg, #ff9800, #ff5722); color:white; text-align:center; padding:18px; font-size:34px; font-weight:bold;">⚡ 展示終了！キイナの最終決断 ⚡</div><div style="padding:25px; display:flex; justify-content:space-between; align-items:center; background:#ffb300;"><div class="kiina-title" style="color:white;">⚡ キイナ最終決断</div><div style="font-size:24px; font-weight:bold; color:white; text-align:right;">{race_date}<br>{race_place}<br>{race_no}</div></div><div class="main"><div class="left"><div class="kiina-box"><div class="kiina-section">⚡ 最終判定</div><div style="font-size:72px; font-weight:bold; color:#ff9800; text-align:center; margin-top:20px;">◎5 ○2 ▲1</div><div style="margin-top:20px; font-size:26px; line-height:2; font-weight:bold;">展示気配は5号艇が抜群！<br>イン受け流して突き抜け期待！</div></div><div class="kiina-box"><div class="kiina-section">🎯 的中期待度</div><div style="font-size:110px; font-weight:bold; color:#ff5722; text-align:center;">{hit_rate}%</div></div><div class="kiina-box"><div class="kiina-section">⚡ キイナの買い目</div><div style="font-size:88px; font-weight:bold; color:#ff9800; text-align:center; margin-top:15px;">5-2-1</div><div style="text-align:center; font-size:28px; font-weight:bold; color:#ff9800; margin-top:25px; margin-bottom:10px;">押さえ</div><div class="buy-grid"><div class="buy-card">5-1-2</div><div class="buy-card">5-2-4</div><div class="buy-card">5-1-4</div><div class="buy-card">5-2-6</div></div></div></div><div class="right"><img class="character-img" src="{character_src}"><div class="warning-box">⚡ 万舟警報発令中 ⚡</div><div class="notice" style="background:#fff3cd; border-color:#ff9800;"><div style="font-size:24px; font-weight:bold; color:#ff9800; margin-bottom:10px;">⚡ 直前チェック</div><div style="font-size:20px; line-height:1.8;">・展示急上昇：{up_boat}<br>・危険艇：{danger_boat}<br>・波乱指数：{wave}</div></div><div class="fukidashi" style="border-color:#ffb300; background:#fffdf3;"><div style="font-size:24px; font-weight:bold; color:#ff9800; margin-bottom:10px;">⚡ キイナコメント</div><div style="font-size:22px; line-height:1.8; font-weight:bold;">今日はイン危険！ 5コース一撃あるよ！</div></div></div></div><div style="background:#ff5722; color:white; text-align:center; padding:25px; font-size:34px; font-weight:bold;">⚡ 超波乱モード突入 ⚡</div></div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper-kiina', 'kiina_chokuzen.png')">画像を保存する</button></div></body></html>
"""

# =========================================
# 6. メインタブ表示
# =========================================

main_tab1, main_tab2 = st.tabs([
    "🌸 一果ちゃん",
    "⚡ キイナちゃん"
])

# --- 一果ちゃんタブ ---
with main_tab1:
    sub_tab1, sub_tab2 = st.tabs(["📰 前日版", "🌸 直前版"])
    with sub_tab1:
        html(html_code, height=3200, scrolling=True)
    with sub_tab2:
        html(html_code2, height=1800, scrolling=True)

# --- キイナちゃんタブ ---
with main_tab2:
    sub_tab3, sub_tab4 = st.tabs(["⚡ 前日版", "⚡ 直前版"])
    with sub_tab3:
        html(kiina_html, height=2600, scrolling=True)
    with sub_tab4:
        html(kiina_live_html, height=2600, scrolling=True)
