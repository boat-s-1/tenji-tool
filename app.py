import streamlit as st
from streamlit.components.v1 import html
import base64
import os

# =========================================
# 1. 画像読み込み・Base64変換関数
# =========================================
def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    return ""

# --- 各種画像の読み込み（ファイル名は適宜合わせてください） ---
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

st.sidebar.header("レース情報")
race_place = st.sidebar.text_input("レース場", "丸亀")
race_no = st.sidebar.text_input("レース番号", "1R")
race_date = st.sidebar.text_input("日付", "2026/05/05")
honmei = st.sidebar.selectbox("本命", [f"{i}号艇" for i in range(1, 7)])

st.sidebar.header("画像設定")
uploaded_character = st.sidebar.file_uploader("キャラ画像", type=["png", "jpg", "jpeg"])
uploaded_bg = st.sidebar.file_uploader("背景画像", type=["png", "jpg", "jpeg"])

# 画像のBase64化
character_src = f"data:image/png;base64,{base64.b64encode(uploaded_character.read()).decode()}" if uploaded_character else "https://placehold.co/500x900/png"
bg_src = f"data:image/png;base64,{base64.b64encode(uploaded_bg.read()).decode()}" if uploaded_bg else ""

stamp = st.sidebar.selectbox("スタンプ", ["なし"] + list(stamp_dict.keys()))
nige_rate = st.sidebar.slider("イン逃げ期待度", 0, 100, 84)
up_rate = st.sidebar.slider("場平均との差", -30, 30, 11)
wave = st.sidebar.slider("波乱指数", 0, 100, 28)
hit_rate = st.sidebar.slider("的中期待度", 0, 100, 87)
comment = st.sidebar.text_area("一果のひとこと", "1号艇中心だが2号艇の差し注意！")

st.sidebar.header("展開ストーリー設定")
selected_boats = st.sidebar.multiselect("注目艇", [f"{i}号艇" for i in range(1, 7)], default=["1号艇", "2号艇", "3号艇"])

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

# =========================================
# 3. デザイン（CSS）とパーツの組み立て
# =========================================

# CSS (NameErrorを防ぐため、HTMLの前に定義)
common_style = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700&display=swap');
body {{ background:#fffdf5; padding:20px; font-family:'Arial'; background-image:url('{bg_src}'); background-size:cover; background-attachment:fixed; }}
.wrapper, .wrapper-live {{ width:1000px; margin:auto; background:rgba(255,255,255,0.94); border:6px dashed #ff6ea8; border-radius:25px; overflow:visible; position: relative; }}
.section-title {{ background: #ff4f93; color: white; font-size: 26px; font-weight: bold; padding: 8px 15px; border-radius: 8px; margin-bottom: 15px; display: inline-block; font-family: 'Zen Maru Gothic', sans-serif; }}
.main {{ display:flex; gap:20px; padding:20px; }}
.left {{ width:65%; }} .right {{ width:35%; text-align:center; }}
.mainbox, .mainbox-live {{ border:5px dashed #ffb3cf; border-radius:25px; padding:20px; margin-bottom:20px; background:#fffafb; }}
.fukidashi {{ position: relative; background: #fff; border: 4px solid #ff6ea8; border-radius: 25px; padding: 20px; margin-top: -15px; z-index: 10; font-family: 'Zen Maru Gothic', sans-serif; font-size: 20px; line-height: 1.6; }}
.fukidashi::before {{ content: ""; position: absolute; top: -24px; left: 40px; border: 12px solid transparent; border-bottom: 12px solid #ff6ea8; }}
.fukidashi::after {{ content: ""; position: absolute; top: -18px; left: 40px; border: 12px solid transparent; border-bottom: 12px solid #fff; }}
.pickup-row {{ display: flex; align-items: center; margin-bottom: 12px; background: linear-gradient(90deg, #fff5f8 0%, #ffffff 100%); border-left: 8px solid #ff6ea8; border-radius: 8px; padding: 10px; }}
.notice, .notice-live {{ margin-top: 20px; background: #fff3c4; border: 4px dashed #ff6ea8; border-radius: 20px; padding: 15px; text-align: left; font-family: 'Zen Maru Gothic', sans-serif; }}
.motor-box {{ margin-top: 15px; background: #f0f9ff; border: 3px solid #7ec2ff; border-radius: 15px; padding: 15px; text-align: left; }}
.bar-bg {{ width:100%; height:30px; background:#ffe3ee; border-radius:15px; overflow:hidden; margin-top:5px; }}
.bar-fill {{ height:100%; background:linear-gradient(90deg, #ff7eb3, #ff4f93); text-align:right; color:white; padding-right:10px; line-height:30px; font-weight:bold; }}
.footer {{ text-align: center; padding: 20px; }}
.footer-img {{ width: 100%; max-width: 900px; border-radius: 10px; }}
.download-btn {{ display: block; width: 220px; margin: 20px auto; padding: 15px; background: #ff4f93; color: white; border-radius: 50px; font-weight: bold; cursor: pointer; border: none; font-size: 18px; }}
</style>
"""

header_part = f"""
<div class="header" style="display: flex; justify-content: center; position: relative; align-items: center; padding: 20px; border-bottom: 5px dashed #ff6ea8;">
    <img src="{logo_src}" style="width: 100%; max-width: 650px;">
    <div style="position: absolute; right: 20px; font-size: 22px; font-weight: bold; text-align: center;">{race_date}<br>{race_place}<br>{race_no}</div>
</div>
"""

# ロジック計算
stars = "⭐" * ((wave // 20) + 1)
attention_boats = ", ".join([b.replace("号艇", "") for b in selected_boats])
current_stamp_src = stamp_dict.get(stamp, "")
stamp_html = f'<img src="{current_stamp_src}" style="width: 200px; position: absolute; right: 20px; top: -30px; transform: rotate(-15deg); z-index: 100; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.1));">' if current_stamp_src else ""

boat_info_map = {"1号艇": "#e2e2e2", "2号艇": "#444444", "3号艇": "#ff4444", "4号艇": "#4444ff", "5号艇": "#eeaa00", "6号艇": "#22aa22"}
story_html = "".join([f'<div class="pickup-row" style="border-left: 8px solid {boat_info_map[b]};"><img src="{boat_srcs[b]}" style="width: 70px; margin-right: 15px;"><div style="font-size:20px; font-weight:bold;">{boat_comments[b]}</div></div>' for b in selected_boats])

# 保存用JavaScript
download_logic = f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function saveImage(targetClass, fileName) {{
    const target = document.querySelector(targetClass);
    html2canvas(target, {
    useCORS: true,
    allowTaint: true,
    scale: 2,
    backgroundColor: "#ffffff",
    scrollY: -window.scrollY
}).then(canvas => {{
        const link = document.createElement('a');
        link.download = fileName; link.href = canvas.toDataURL('image/png'); link.click();
    }});
}}
</script>
"""

# =========================================
# 4. HTML組み立てと出力
# =========================================

# 前日版
html_code = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper">{header_part}<div class="main"><div class="left">
<div class="mainbox" style="position: relative;">{stamp_html}<div class="section-title">本命候補</div><div style="font-size:40px; font-weight:bold; color:#ff4f93; margin-left:10px;">{honmei}</div><div style="display:flex; justify-content:space-between; border-bottom:3px dashed #ffd0e2; padding:10px 0;"><div style="font-size:24px; font-weight:bold;">イン逃げ期待度</div><div style="font-size:40px; font-weight:bold; color:#ff4f93;">{nige_rate}%</div></div><div style="display:flex; justify-content:space-between; padding:10px 0;"><div style="font-size:24px; font-weight:bold;">場平均との差</div><div style="font-size:36px; font-weight:bold; color:#44aa55;">+{up_rate}%</div></div></div>
<div class="mainbox"><div class="section-title">展開ストーリー (予想)</div>{story_html}</div>
<div class="mainbox"><div class="section-title">各艇評価指数</div>{"".join([f'<div style="margin-bottom:10px;"><div style="font-weight:bold;">{i}号艇</div><div class="bar-bg"><div class="bar-fill" style="width:{boat_scores[f"{i}号艇"]}%;">{boat_scores[f"{i}号艇"]}</div></div></div>' for i in range(1,7)])}</div>
</div><div class="right"><img class="character-img" src="{character_src}"><div class="fukidashi"><div style="color:#ff4f93; font-weight:bold; font-size:24px; margin-bottom:5px;">🌸 一果のひとこと</div>{comment}</div><div class="notice"><div style="font-size:22px; font-weight:bold; color:#ff4f93; text-align:center; border-bottom:2px solid #ffb3cf; margin-bottom:10px;">📍 要チェックポイント</div><div>・波乱指数：{stars} ({wave})</div><div>・危険艇：{danger_boat}</div><div>・注目艇：{attention_boats}</div></div><div class="motor-box"><div style="font-size:20px; font-weight:bold; color:#0077cc; border-bottom:2px solid #b3d9ff; margin-bottom:8px;">⚙️ 一果の機力チェック</div><div style="font-weight:bold; font-size:18px;">{motor_eval}</div></div></div></div><div class="footer"><img src="{footer_img_src}" class="footer-img"></div></div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper', 'zenjitsu.png')">画像を保存する</button></div></body></html>
"""

# 直前版
html_code2 = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body><div class="wrapper-live"><div style="background:#ff85b5; color:white; padding:18px; font-size:32px; font-weight:bold; text-align:center;">🌸 展示終了！一果の最終決定 🌸</div>{header_part}<div class="main"><div class="left"><div class="mainbox" style="border-color:#ff4f93;"><div style="font-size:32px; font-weight:bold; color:#ff4f93;">展示評価：{tenji_rank}</div><div style="font-size:24px;">タイム：{tenji_time} / 進入：{shinnyu}</div><div style="font-size:36px; font-weight:bold; color:#ff4f93; margin-top:15px;">一果判定：{ikka_hantei}</div></div><div class="mainbox" style="border-color:#ff4f93;"><div style="font-size:28px; font-weight:bold;">🎯 的中期待度</div><div style="font-size:72px; font-weight:bold; color:#ff4f93;">{hit_rate}%</div></div><div class="mainbox" style="border-color:#ff4f93;"><div class="section-title">🌸 一果の買い目</div><div style="font-size:24px; font-weight:bold; color:#ff4f93; text-align:center;">本命：{honmei_kaime}</div><div style="border-top:2px dashed #ffb3cf; margin:10px 0;"></div><div style="font-size:20px; text-align:center; color:#666;">押さえ：<br>{osae_kaime.replace('\\n', '<br>')}</div></div></div><div class="right"><img class="character-img" src="{character_src}"><div class="notice" style="background:#ffe5f1; border-color:#ff4f93;"><div style="font-size:22px; font-weight:bold; color:#ff4f93; text-align:center; border-bottom:2px solid #ffb3cf; margin-bottom:10px;">📍 直前チェック</div><div>・急上昇：{up_boat}</div><div>・危険艇：{danger_boat}</div></div><div class="fukidashi" style="margin-top:20px;">{jikkan_comment}</div></div></div><div style="background:#ff4f93; color:white; text-align:center; padding:20px; font-size:24px; font-weight:bold;">🌸 一果の最終判断公開中 🌸</div></div><div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper-live', 'chokuzen.png')">画像を保存する</button></div></body></html>
"""

# --- 5. タブ表示部分を以下に書き換え ---

tab1, tab2 = st.tabs(["📰 前日版", "🌸 直前版"])

with tab1:
    # 前日版を表示
    html(html_code, height=2200, scrolling=True)


with tab2:
    html(html_code2, height=1800, scrolling=True)
