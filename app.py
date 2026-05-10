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

def get_stamp_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"

# --- 各種画像の読み込み ---
logo_path = "名称未設定のデザイン (49).png"
logo_src = get_base64_img(logo_path)
# 直前版用のロゴを新しく定義
logo_live_path = "名称未設定のデザイン (51).png" 
logo_live_src = get_base64_img(logo_live_path)
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


stamp_options = {
    "なし": "",
    "波乱注意": get_base64_img("085d5af5-0e82-44da-a883-e7a1ac808d51.png"),
    "鉄板": get_base64_img("79794320-58c8-4fd2-8815-174ca1b73ab3.png"),
    "見": get_base64_img("64f255c6-e9d6-427c-890f-f6cdb55695ee.png"),
}

kiina_header_img_src = get_base64_img("S__17752068.jpg")
kiina_header_live_img_src = get_base64_img("S__17752078.jpg")

new_hatsune_header_src = get_base64_img("S__17760265.jpg")
# =========================================
# 2. ユーザー入力（サイドバー）
# =========================================
st.set_page_config(page_title="一果ちゃん新聞", layout="wide")
st.title("🌸 一果ちゃん新聞ジェネレーター")

with st.sidebar.expander("📌 レース基本情報"):
    race_place = st.text_input("レース場", "丸亀")
    race_no = st.text_input("レース番号", "1R")
    race_date = st.text_input("日付", "2026/05/05")
 


with st.sidebar.expander("📌 画像"):
    uploaded_character = st.file_uploader("キャラ画像", type=["png", "jpg", "jpeg"])
    uploaded_bg = st.file_uploader("背景画像", type=["png", "jpg", "jpeg"])

# 画像のBase64化
if uploaded_character:
    character_src = f"data:image/png;base64,{base64.b64encode(uploaded_character.read()).decode()}"
else:
    character_src = "https://placehold.co/500x900/png"
st.sidebar.header("一果")
with st.sidebar.expander("📌 一果本命候補"):
    honmei = st.selectbox("本命", [f"{i}号艇" for i in range(1, 7)])
    stamp = st.selectbox("スタンプ", ["なし"] + list(stamp_dict.keys()))
    nige_rate = st.slider("イン逃げ期待度", 0, 100, 84)
    up_rate = st.slider("場平均との差", -30, 30, 11)
with st.sidebar.expander("📌 一果展開評価"):
    selected_boats = st.multiselect("注目艇", [f"{i}号艇" for i in range(1, 7)], default=["1号艇", "2号艇", "3号艇"])

    boat_comments = {}
    boat_scores = {}
    for i in range(1, 7):
       name = f"{i}号艇"
       boat_comments[name] = st.text_input(f"{name} コメント", f"{name}の展開解説")
       boat_scores[name] = st.slider(f"{name} 評価", 0, 100, 50)
comment = st.sidebar.text_area("一果のひとこと", "1号艇中心だが2号艇の差し注意！")  
wave = st.sidebar.slider("波乱指数", 0, 100, 28)
danger_boat = st.sidebar.selectbox("危険艇", ["なし"] + [f"{i}号艇" for i in range(1, 7)])

with st.sidebar.expander("📌 一果直前"):
       tenji_rank = st.selectbox("展示評価", ["S", "A", "B", "C"], key="live_tenji_rank")
       tenji_time = st.text_input("補正タイム", "6.71")
       shinnyu = st.text_input("進入予想", "123/456")
       honmei_kaime = st.text_input("本命買い目", "1-2-3")
       osae_kaime = st.text_area("押さえ買い目", "1-3-2\n1-2-5")
       up_boat = st.selectbox("展示急上昇", ["なし"] + [f"{i}号艇" for i in range(1, 7)], key="up_boat_select")
       hit_rate = st.slider("🎯 的中期待度 (%)", 0, 100, 80)
    # 艇番のリスト [1, 2, 3, 4, 5, 6]
boat_numbers = [str(i) for i in range(1, 7)]

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    hantei_double = st.selectbox("◎ 本命", boat_numbers, index=0) # 初期値 1
with col2:
    hantei_single = st.selectbox("○ 対抗", boat_numbers, index=1) # 初期値 2
with col3:
    hantei_triangle = st.selectbox("▲ 単穴", boat_numbers, index=4) # 初期値 5
      

motor_eval = st.sidebar.text_area("機力チェック", "1号艇は出足型、3号艇の伸びが節イチ級！", height=100)



# --- 修正箇所：変数を定義する ---


# --- 修正版：サイドバー入力 ---



jikkan_comment = st.sidebar.text_area("直前コメント", "展示は1号艇優勢！")




# 💡 ここを追加：選択されたスタンプ名から、実際の画像データ（base64）を取得する

selected_stamp_name = st.sidebar.selectbox("表示するスタンプ", list(stamp_options.keys()))
stamp_img = stamp_options[selected_stamp_name]
st.sidebar.header("直前情報")
# ↓この行を、html_code2 を作成するより「前」に必ず書く

# --- サイドバー：キイナちゃん設定 ---
with st.sidebar.expander("⚡ キイナの穴党設定"):
    # ここを追加！
    kiina_5atama_rate = st.slider("5アタマ期待度 (%)", 0, 100, 72)
    
    chou_batsu = st.selectbox("超抜気配", ["★", "★★", "★★★", "★★★★", "★★★★★"], index=4)
    ana_target = st.text_input("穴ターゲット", "5号艇のまくり差し")
    keihou_msg = st.text_input("警報メッセージ", "波乱警報発令中！万舟のチャンス！")

with st.sidebar.expander("⚡ キイナのスリット予想"):
    slit_positions = {}
    for i in range(1, 7):
        # 0がスリットラインぴったり、プラスが先行（のぞいている）状態
        slit_positions[f"{i}号艇"] = st.slider(f"{i}号艇 スリット", -50, 50, 0, step=5)

with st.sidebar.expander("🎨 スリットのデザイン設定"):
    slit_bg_color = st.color_picker("スリット全体の背景色", "#111111") # デフォルトは黒
    lane_bg_color = st.color_picker("レーンの色", "#222222") # 少し明るい黒
    line_color = st.color_picker("スリットラインの色", "#ffcc00") # 稲妻イエロー

with st.sidebar.expander("⚡ 直前チェック項目"):
    check_in = st.checkbox("インの足", value=True)
    check_nobi = st.checkbox("4号艇の伸び", value=False)
    check_keihai = st.checkbox("スタ展気配", value=True)
    check_kaze = st.checkbox("風向き", value=False)
    check_time = st.checkbox("展示タイム", value=True)

# チェックの状態に合わせて表示する記号を切り替えるロジック
def get_check_mark(is_checked):
    return "☑" if is_checked else "☐"

check_items = [
    (get_check_mark(check_in), "インの足"),
    (get_check_mark(check_nobi), "4号艇の伸び"),
    (get_check_mark(check_keihai), "スタ展気配"),
    (get_check_mark(check_kaze), "風向き"),
    (get_check_mark(check_time), "展示タイム")
]

# HTMLパーツの生成
check_list_html = ""
for mark, label in check_items:
    color = "#ffcc00" if mark == "☑" else "#888" # チェック済みは黄色、未チェックはグレー
    check_list_html += f'<div style="color:{color}; font-size:18px; margin-bottom:5px; font-weight:bold;">{mark} {label}</div>'


with st.sidebar.expander("⚡ 直前LIVE設定"):
    # キー名の後ろに _v2 や _unique など、絶対に被らない文字を足します
    tenji_rank = st.selectbox("展示評価", ["S", "A", "B", "C"], index=0, key="kiina_live_rank_final")
    tenji_time = st.text_input("補正タイム", "6.71", key="kiina_live_time_final")
    shinnyu = st.text_input("進入予想", "123/456", key="kiina_live_shinnyu_final")
    diff_4 = st.text_input("4号艇との展示差", "-0.05", key="kiina_live_diff4_final")


with st.sidebar.expander("⚡ キイナのLIVEスタンプ設定"):
    # 💡 用意した画像のパスを指定してください
    stamp_images = {
        "なし": None,
        "イン信用しない": "84FD0651-C2E8-42EC-8FE5-91B3289511F4.png",
         "展示次第": "806A77BA-B630-4FE7-ADB0-E4DA441911EE.png",
         "モーター抜群": "F0A5A40E-D22C-4E2F-8566-F2F02DB1E9C4.png",
         "オッズがつかない": "76B25214-54F2-4660-B54D-AA7AEAFB235D.png",
        "荒れそうだけど": "A11D9588-C22C-4ADF-A0F6-AE8524349880.png",
        "4コースが": "0340237A-88C8-4757-876B-AF8AB31C4C11.png",
    }
    
    selected_stamp_label = st.selectbox("スタンプを選択", list(stamp_images.keys()), index=0)
    selected_stamp_path = stamp_images[selected_stamp_label]


# --- サイドバー：初音ちゃん設定 ---
with st.sidebar.expander("👗 初音の女子戦設定"):
    hatsune_honmei = st.selectbox("本命ヴィーナス", [f"{i}号艇" for i in range(1, 7)], index=0, key="hatsune_honmei_key")
    # 💡 ここで hatsune_rhythm を作ります
    hatsune_rhythm = st.select_slider("近況リズム", options=["不調", "並", "好調", "絶好調", "神掛かり"], value="好調", key="hatsune_rhythm_key")
    wall_rank = st.selectbox("壁信頼度", ["SS", "S", "A", "B", "C"], index=2, key="hatsune_wall_key")
    hatsune_kaime = st.text_input("推奨買い目", "1-23-4", key="hatsune_kaime_key")
    weight_memo = st.text_input("調整メモ", "チルト0.5", key="hatsune_weight_key")

with st.sidebar.expander("👗 初音の女子戦・ピックアップ設定"):
    player_count = st.number_input("ピックアップ人数", min_value=1, max_value=6, value=2, key="hatsune_p_count")
    
    pickup_players = []
    for i in range(int(player_count)):
        st.markdown(f"**選手 {i+1}**")
        p_name = st.text_input(f"号艇・選手名", f"{i+1}号艇", key=f"p_name_{i}")
        p_img = st.file_uploader(f"顔写真", key=f"p_img_{i}")
        p_comment = st.text_area(f"コメント", f"ここにコメントを入力", key=f"p_comment_{i}")
        
        # 画像のBase64変換（ファイルがなければデフォルト画像）
        p_img_src = "https://cdn-icons-png.flaticon.com/512/1946/1946429.png" # デフォルト
        if p_img:
            import base64
            # 画像を読み込んで変換
            base64_data = base64.b64encode(p_img.getvalue()).decode()
            p_img_src = f"data:image/png;base64,{base64_data}"
            
        pickup_players.append({"name": p_name, "img": p_img_src, "comment": p_comment})




# HTMLに埋め込むための文字列を生成
pickup_html_list = ""
for p in pickup_players:
    pickup_html_list += f"""
    <div style="display: flex; align-items: center; background: #fff; border-radius: 12px; padding: 10px; border: 1px solid #ce93d8; margin-bottom: 10px;">
        <div style="width: 60px; height: 60px; border-radius: 50%; overflow: hidden; border: 2px solid #ffb7c5; flex-shrink: 0;">
            <img src="{p['img']}" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div style="margin-left: 15px; text-align: left;">
            <div style="font-size: 14px; font-weight: 900; color: #5c6bc0;">{p['name']}</div>
            <div style="font-size: 12px; color: #444; line-height: 1.4;">「{p['comment']}」</div>
        </div>
    </div>
    """
# =========================================
# 3. CSS/JavaScript (f-stringの競合回避)
# =========================================

# --- common_style に追加 ---
kiina_style = """
<style>
/* キイナちゃん専用：全体背景と枠線 */
.wrapper-kiina {
    width: 1000px;
    margin: auto;
    background: #000; /* 黒ベース */
    border: 6px solid #ffcc00; /* 黄色枠 */
    border-radius: 15px;
    color: #fff;
    font-family: 'Zen Maru Gothic', sans-serif;
    position: relative;
    overflow: hidden;
}

/* タイトル部分の稲妻感 */
.kiina-header {
    background: linear-gradient(135deg, #ffcc00 0%, #ff9900 100%);
    color: #000;
    padding: 20px;
    text-align: center;
    font-size: 40px;
    font-weight: 900;
    text-shadow: 2px 2px 0px #fff;
    border-bottom: 4px solid #000;
}

/* 各ボックス（イエローカード風） */
.kiina-box {
    background: #fffde6; /* 薄い黄色 */
    color: #000;
    border: 3px solid #000;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 4px 4px 0px #ffcc00;
}

/* 期待度などの大きな数字 */
.kiina-huge-text {
    font-size: 60px;
    font-weight: 900;
    color: #e60000; /* 勝負の赤 */
    line-height: 1;
}

/* 稲妻バナー（下部） */
.kiina-banner {
    background: #000000; /* 漆黒 */
    color: #ffcc00;     /* 稲妻イエロー */
    padding: 20px;
    text-align: center;
    font-size: 32px;    /* 文字を大きく */
    font-weight: 900;
    border-top: 4px solid #ffcc00;
    margin-top: 10px;
    width: 1000px;      /* 幅を固定 */
    box-sizing: border-box;
}
</style>
"""




common_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700;900&display=swap');

/* 全体のフォントを丸ゴシックに強制 */
* {
    font-family: 'Zen Maru Gothic', sans-serif !important;
}

body { 
    background:#fffdf5; 
    padding:20px; 
}
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
<div class="header" style="
    position: relative; 
    width: 1000px; 
    height: 150px; 
    border-bottom: 5px dashed #ff6ea8;
">
    <!-- 背景としてロゴと花びら画像を置く -->
    <img src="{logo_src}" style="
        position: absolute; 
        top: 0; 
        left: 0; 
        width: 1000px; 
        z-index: 1;
    ">
    
    <!-- その上に文字を重ねる -->
    <div style="
        position: absolute; 
        right: 30px; 
        top: 20px; 
        text-align: right; 
        z-index: 2; /* 画像より上に表示 */
    ">
        <div style="font-size: 24px; font-weight: 800;">{race_date}</div>
        <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 15px;">
            <span style="font-size: 52px; font-weight: 900;">{race_place}</span>
            <span style="font-size: 46px; font-weight: 900;">{race_no}</span>
        </div>
    </div>
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




# 艇番ごとの色を定義
boat_colors = {
    "1号艇": "#eeeeee",
    "2号艇": "#333333",
    "3号艇": "#ff4b4b",
    "4号艇": "#007bff",
    "5号艇": "#ffc107",
    "6号艇": "#28a745"
}

# グラフ部分のHTMLを生成するループ
# グラフ部分のHTML生成（太さアップ ＆ 1号艇視認性アップ版）
graph_items_html = ""
for i in range(1, 7):
    name = f"{i}号艇"
    score = boat_scores[name]
    color = boat_colors[name]
    
    # 1号艇（白）だけ枠線を付けて見やすくする
    extra_style = "border: 1px solid #ccc;" if i == 1 else ""
    
    graph_items_html += f"""
    <div style="margin-bottom: 12px; font-family: 'Zen Maru Gothic', sans-serif;">
        <div style="display: flex; justify-content: space-between; font-size: 16px; font-weight: 900; margin-bottom: 4px;">
            <span style="color: #333;">{name}</span>
            <span style="color: #ff4f93;">{score}</span>
        </div>
        <!-- 背景のグレー部分も少し太く -->
        <div style="background: #efefef; border-radius: 15px; height: 24px; overflow: hidden; border: 1px solid #ddd;">
            <!-- 評価バー本体：heightを24pxに。1号艇のみextra_styleが適用される -->
            <div style="
                background: {color}; 
                width: {score}%; 
                height: 100%; 
                border-radius: 0 15px 15px 0;
                {extra_style}
                box-sizing: border-box;
            "></div>
        </div>
    </div>
    """
# --- 修正版：艇番をタイトル風に太字で強調 ---
story_items_html = ""
for boat_name in selected_boats:
    b_src = boat_srcs.get(boat_name, "")
    b_comment = boat_comments.get(boat_name, "展開解説がありません")
    b_color = boat_colors.get(boat_name, "#ff4f93")
    
    story_items_html += f"""
    <div style="
        display: flex; 
        align-items: flex-start; 
        background: #f9f9f9; 
        border-radius: 12px; 
        padding: 12px; 
        margin-bottom: 12px; 
        border-left: 8px solid {b_color};
        font-family: 'Zen Maru Gothic', sans-serif;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    ">
        <!-- ボート画像 -->
        <div style="flex: 0 0 70px; text-align: center; margin-top: 2px;">
            <img src="{b_src}" style="width: 60px; height: auto;">
        </div>
        
        <!-- テキストエリア -->
        <div style="flex: 1; margin-left: 12px;">
            <!-- タイトル風の艇番：ここを太字で強調 -->
            <div style="
                font-size: 18px; 
                font-weight: 900; 
              color: {b_color if boat_name != '1号艇' else '#333'};
                margin-bottom: 4px;
                letter-spacing: 1px;
            ">
                {boat_name}
            </div>
            <!-- コメント：自動改行 -->
            <div style="
                font-size: 15px; 
                color: #444; 
                line-height: 1.5; 
                word-wrap: break-word;
            ">
                {b_comment}
            </div>
        </div>
    </div>
    """


# =========================================
# 5. 各種HTML文字列作成
# =========================================

# =========================================
# 🌸 一果ちゃん 右側カラム（機力チェック追加版）
# =========================================

right_column_html = f"""
<div class="right" style="display: flex; flex-direction: column; align-items: center; width: 350px;">
    <!-- 1. キャラ画像 -->
    <img class="character-img" src="{character_src}" style="
        position: relative; 
        z-index: 1; 
        margin-bottom: 0;
        width: 100%;
        max-width: 320px;
    ">
    
    <!-- 2. 吹き出し -->
    <div class="fukidashi" style="
        position: relative; 
        z-index: 2; 
        margin-top: -60px; 
        background: rgba(255, 255, 255, 0.98);
        border: 4px solid #ff6ea8;
        border-radius: 25px;
        padding: 20px;
        width: 90%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">
        <div style="color: #ff4f93; font-weight: bold; font-size: 20px; margin-bottom: 8px; display: flex; align-items: center; justify-content: center;">
            🌸 一果のひとこと
        </div>
        <div style="font-size: 18px; line-height: 1.6; color: #333; text-align: left;">
            {comment}
        </div>
        <div style="position: absolute; top: -18px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 15px solid #ff6ea8;"></div>
    </div>

    <!-- 3. 要チェックポイント -->
    <div class="notice" style="margin-top: 20px; background: #fff3c4; border: 4px dashed #ff6ea8; border-radius: 20px; padding: 15px; width: 90%; text-align: left;">
        <div style="font-size: 18px; font-weight: bold; color: #ff4f93; text-align: center; border-bottom: 2px solid #ffb3cf; margin-bottom: 10px;">📍 要チェックポイント</div>
        <div style="font-size: 16px; line-height: 1.8;">
            ・波乱指数：{stars} ({wave})<br>
            ・危険艇：{danger_boat}<br>
            ・注目艇：{attention_boats}
        </div>
    </div>

    <!-- 4. 一果の機力チェック（ここを復活させました！） -->
    <div class="motor-box" style="
        margin-top: 20px; 
        background: #f0f9ff; 
        border: 3px solid #7ec2ff; 
        border-radius: 15px; 
        padding: 15px; 
        width: 90%; 
        text-align: left;
    ">
        <div style="font-size: 18px; font-weight: bold; color: #0077cc; border-bottom: 2px solid #b3d9ff; margin-bottom: 8px; text-align: center;">
            ⚙️ 一果の機力チェック
        </div>
        <div style="font-weight: bold; font-size: 16px; line-height: 1.5; color: #333;">
            {motor_eval}
        </div>
    </div>
</div>
"""

# 全体の組み立て（左側と右側を合体）
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {common_style}
    {download_logic}
</head>
<body>
    <div class="wrapper">
        {header_part}
        <div class="main">
            <!-- 左側カラム -->
                  <div class="left">
    <div class="mainbox" style="position: relative; overflow: visible; padding: 20px;">
        <!-- スタンプを右上に配置 -->
        <div style="position: absolute; top: -10px; right: 10px; z-index: 10;">
            {stamp_html}
        </div>

        <div class="section-title">本命候補</div>
        <div style="font-size:32px; font-weight:bold; color:#ff4f93; margin-top: 5px;">{honmei}</div>
        
        <!-- イン逃げ期待度：左右に振り分けつつ、数字を巨大化 -->
        <div style="display:flex; justify-content:space-between; align-items: baseline; border-bottom:3px dashed #ffd0e2; padding: 15px 0 5px 0; margin-bottom: 5px;">
            <div style="font-size:22px; font-weight:bold; color:#333;">イン逃げ期待度</div>
            <div style="font-size:84px; font-weight:900; color:#ff4f93; line-height: 0.8;">
                {nige_rate}<span style="font-size: 32px; font-weight: bold;">%</span>
            </div>
        </div>

        <!-- 場平均との差：左右振り分け -->
        <div style="display:flex; justify-content:space-between; align-items: center; padding: 10px 0;">
            <div style="font-size:20px; font-weight:bold; color:#666;">場平均との差</div>
            <div style="font-size:36px; font-weight:bold; color:#44aa55;">+{up_rate}%</div>
        </div>
    </div>

         <!-- 展開ストーリーセクション -->
            <div class="mainbox" style="border-color:#ff4f93; border-radius: 20px; border: 4px dashed #ffb3cf; background: #fff; padding: 15px;">
                <div class="section-title" style="background: #ff4f93; color: white; display: inline-block; padding: 2px 15px; border-radius: 5px; font-weight: bold; margin-bottom: 12px;">展開ストーリー（予想）</div>
                
                <div style="padding: 5px;">
                    {story_items_html}
                </div>
            </div>

    
                <div class="mainbox" style="padding: 15px; border-radius: 20px; border: 4px dashed #ffb3cf; background: #fff;">
    <div class="section-title" style="background: #ff4f93; color: white; display: inline-block; padding: 2px 15px; border-radius: 5px; font-weight: bold; margin-bottom: 15px;">各艇評価指数</div>
    
    <!-- ここに Python で生成した graph_items_html が入ります -->
    {graph_items_html}  </div>  </div>
            
            <!-- 右側カラム（上で作ったパーツを入れる） -->
            {right_column_html}
        </div>
        
        <div class="footer">
            <img src="{footer_img_src}" class="footer-img">
        </div>
    </div>
    <div style="text-align:center;">
        <button class="download-btn" onclick="saveImage('.wrapper', 'ikka_zenjitsu.png')">画像を保存する</button>
    </div>
</body>
</html>
"""

# --- 一果 直前版 (html_code2) ---

# 右側パーツ（念のため再定義）
right_column_live_html = f"""
<div class="right" style="display: flex; flex-direction: column; align-items: center; width: 350px;">
    <img class="character-img" src="{character_src}" style="position: relative; z-index: 1; margin-bottom: 0; width: 100%; max-width: 320px;">
    <div class="fukidashi" style="position: relative; z-index: 2; margin-top: -60px; background: rgba(255, 255, 255, 0.98); border: 4px solid #ff6ea8; border-radius: 25px; padding: 20px; width: 90%; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <div style="color: #ff4f93; font-weight: bold; font-size: 20px; margin-bottom: 8px; display: flex; align-items: center; justify-content: center;">🌸 一果の直前談</div>
        <div style="font-size: 18px; line-height: 1.6; color: #333; text-align: left;">{jikkan_comment}</div>
        <div style="position: absolute; top: -18px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 15px solid #ff6ea8;"></div>
    </div>
    <div class="notice" style="margin-top: 20px; background: #ffe5f1; border: 4px dashed #ff4f93; border-radius: 20px; padding: 15px; width: 90%; text-align: left;">
        <div style="font-size: 18px; font-weight: bold; color: #ff4f93; text-align: center; border-bottom: 2px solid #ffb3cf; margin-bottom: 10px;">📍 直前チェック</div>
        <div style="font-size: 16px; line-height: 1.8;">・展示急上昇：{up_boat}<br>・一果の危険艇：{danger_boat}</div>
    </div>
</div>
"""




# 直前用ロゴ
target_logo_live = logo_live_src if 'logo_live_src' in locals() and logo_live_src else logo_src

html_code2 = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8">{common_style}{download_logic}</head>
<body>
<div class="wrapper-live" style="width: 1000px; margin: auto; padding: 0 !important; border: 6px dashed #ff6ea8; border-radius: 25px; overflow: hidden; background: #fffdf5;">
    
    <!-- 1. LIVE帯 -->
    <div style="background:#ff85b5; color:white; padding:15px; font-size:32px; font-weight:bold; text-align:center;">
        🌸 展示終了！一果の最終決定 🌸
    </div>

    <!-- 2. ヘッダー（前日版の設定をそのまま移植） -->
    <div class="header" style="position: relative; width: 1000px; height: 150px; border-bottom: 5px dashed #ff6ea8; background: #fff;">
        <!-- ロゴ画像 -->
        <img src="{target_logo_live}" style="position: absolute; top: 0; left: 0; width: 1000px; z-index: 1;">
        
        <!-- 文字情報 -->
        <div style="position: absolute; right: 30px; top: 20px; text-align: right; z-index: 2; font-family: 'Zen Maru Gothic', sans-serif;">
            <div style="font-size: 24px; font-weight: 800; color: #333;">{race_date}</div>
            <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 15px;">
                <span style="font-size: 52px; font-weight: 900; color: #ff4f93;">{race_place}</span>
                <span style="font-size: 46px; font-weight: 900; color: #333;">{race_no}</span>
            </div>
        </div>
    </div>

    <!-- 3. メイン -->
    <div class="main" style="display: flex; gap: 20px; padding: 20px;">
        <div class="left" style="width: 610px;">
        

            <!-- 1. 展示評価・一果判定 -->
            <div class="mainbox" style="border-color:#ff4f93; margin-bottom: 20px; border-radius: 20px; border: 4px dashed #ffb3cf; background: #fff; overflow: hidden;">
                <div style="background: #fff0f5; padding: 10px 20px; border-bottom: 2px dashed #ffb3cf; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 28px; font-weight: bold; color: #ff4f93;">展示評価：<span style="font-size: 48px;">{tenji_rank}</span></span>
                    <div style="text-align: right; line-height: 1.3;">
                        <span style="font-size: 16px; color: #666;">補正タイム：{tenji_time}</span><br>
                        <span style="font-size: 16px; color: #666;">進入：{shinnyu}</span>
                    </div>
                </div>
        

<div style="padding: 20px; text-align: center;">
    <div style="font-size: 20px; color: #ff4f93; font-weight: bold; margin-bottom: 12px;">🌸 一果の直前判定</div>
    <div style="display: flex; justify-content: center; gap: 15px; align-items: center;">
        
        <!-- ◎ 本命 (変数 hantei_double を使用) -->
        <span style="background:#ff4f93; color:white; padding:5px 20px; border-radius:50px; font-size:24px; font-weight:bold; box-shadow: 0 4px 0 #d63d7a;">
            ◎ {hantei_double}
        </span>
        
        <!-- ○ 対抗 (変数 hantei_single を使用) -->
        <span style="background:#fff0f5; color:#ff4f93; padding:5px 20px; border-radius:50px; font-size:24px; font-weight:bold; border: 2px solid #ff4f93;">
            ○ {hantei_single}
        </span>
        
        <!-- ▲ 単穴 (変数 hantei_triangle を使用) -->
        <span style="background:#f5f5f5; color:#666; padding:5px 20px; border-radius:50px; font-size:24px; font-weight:bold; border: 2px solid #999;">
            ▲ {hantei_triangle}
        </span>

    
</div>
                </div>
            </div>

         <!-- 2. 的中期待度 ＆ スタンプ -->
            <div class="mainbox" style="
                border-color: #ff4f93; 
                margin-bottom: 20px; 
                padding: 15px 25px; 
                border-radius: 20px; 
                border: 4px dashed #ffb3cf; 
                background: #fff;
                display: flex; 
                align-items: center; 
                justify-content: space-between;
                overflow: visible; 
            ">
                <div style="text-align: left;">
                    <!-- タイトル部分：塗りつぶし背景に修正 -->
                    <div style="
                        background: #ff4f93; 
                        color: white; 
                        display: inline-block; 
                        padding: 2px 12px; 
                        border-radius: 5px; 
                        font-size: 18px; 
                        font-weight: 900; 
                        margin-bottom: 8px;
                    ">
                        的中期待度
                    </div>
                    <div style="font-size: 70px; font-weight: 900; color: #ff4f93; line-height: 1; margin-left: 5px;">
                        {hit_rate}<span style="font-size: 30px;">%</span>
                    </div>
                </div>

                <div style="position: relative; width: 140px; height: 100px;">
                    {f'''<img src="{stamp_img}" style="
                        position: absolute;
                        top: -30px; 
                        right: -10px; 
                        height: 140px; 
                        transform: rotate(-15deg); 
                        filter: drop-shadow(3px 3px 2px rgba(0,0,0,0.1));
                        z-index: 10;
                    ">''' if stamp_img else ""}
                </div>
            </div>

            <!-- 3. 買い目 -->
            <div class="mainbox" style="border-color:#ff4f93; padding: 20px; border-radius: 20px; border: 4px dashed #ffb3cf; background: #fffafb;">
                <div style="font-size: 20px; font-weight: bold; color: #ff4f93; margin-bottom: 10px; text-align: center;">🌸 一果の買い目</div>
                <div style="font-size:36px; font-weight:bold; color:#ff4f93; text-align:center; padding: 15px 0; background: #fff; border-radius: 15px; border: 2px solid #ffb3cf; margin-bottom: 15px;">
                    本命：{honmei_kaime}
                </div>
                <div style="font-size:24px; text-align:center; color:#666; font-weight: bold; line-height: 1.6;">
                    押さえ：{osae_kaime.replace('\\n', '<br>')}
                </div>
            </div>
        </div>
        {right_column_live_html}
    </div>
    
    <div style="background:#ff4f93; color:white; text-align:center; padding:20px; font-size:24px; font-weight:bold;">
        🌸 一果の最終判断公開中 🌸
    </div>
</div>
<div style="text-align:center;"><button class="download-btn" onclick="saveImage('.wrapper-live', 'chokuzen.png')">画像を保存する</button></div>
</body>
</html>
"""
# =========================================
# 4. パーツ組み立て（キイナちゃんセクション）
# =========================================

# --- [1] 各艇のスリットパーツを生成 ---
# --- [1] 各艇のスリットパーツを生成 ---
slit_items_html = ""
for i in range(1, 7):
    name = f"{i}号艇"
    offset = slit_positions[name]
    b_src = boat_srcs.get(name, "")
    margin_left = 50 + offset 
    
    slit_items_html += f"""
    <div style="display: flex; align-items: center; margin-bottom: 5px; height: 35px; position: relative;">
        <span style="width: 25px; font-weight: bold; font-size: 14px; color: {line_color};">{i}</span>
        <div style="flex: 1; height: 100%; position: relative; background: {lane_bg_color}; border-radius: 5px;">
            <img src="{b_src}" style="height: 30px; margin-left: {margin_left}px;">
        </div>
    </div>
    """
check_box_html = f"""
<div class="kiina-box" style="background:rgba(0,0,0,0.8); border:1px solid #ffcc00; padding:10px; margin-top:10px; text-align:left;">
    <div style="color:#ffcc00; font-size:14px; border-bottom:1px solid #ffcc00; margin-bottom:8px; font-weight:bold;">⚡ 直前チェック項目</div>
    {check_list_html}
</div>
"""

# --- [2] スリットボックス全体を定義 ---
slit_box_html = f"""
<div class="kiina-box" style="background: #111; color: #fff; padding: 15px; position: relative; border: 3px solid #ffcc00; border-radius: 10px; margin-bottom: 15px;">
    <div class="kiina-section-black" style="display: inline-block;">⚡ スリット予想</div>
    <div style="position: relative; padding-left: 10px; margin-top: 10px;">
        <div style="position: absolute; left: 110px; top: 0; bottom: 0; border-left: 2px dashed #ffcc00; z-index: 5;"></div>
        {slit_items_html}
    </div>
    <div style="text-align: right; font-size: 10px; color: #ffcc00; margin-top: 5px;">&larr; 遅れ | 先行 &rarr;</div>
</div>
"""
kiina_style = """
<style>
/* 黒背景に黄色文字のタイトル枠 */
.kiina-section-black {
    background: #000000;
    color: #ffcc00;
    font-size: 20px;
    font-weight: 900;
    padding: 5px 15px;
    border-radius: 5px;
    display: inline-block;
    margin-bottom: 12px;
    border: 1px solid #ffcc00; /* 枠線も入れるとより締まります */
    letter-spacing: 1px;
}
</style>
"""

# 前日版用のスタンプHTML生成
kiina_zenjitsu_stamp_html = ""
if selected_stamp_path:  # サイドバーで選ばれたパス
    stamp_base64 = get_stamp_base64(selected_stamp_path)
    
    # 💡 前日版のレイアウトに合わせた位置調整
    kiina_zenjitsu_stamp_html = f"""
    <img src="{stamp_base64}" style="
        position: absolute;
        top: 150px;         /* 💡 本命候補ボックスの右上付近 */
        left: 400px;        /* 💡 キャラクターの左肩あたりに重なるように */
        z-index: 100;
        width: 280px;       /* 💡 前日版は情報量が多いので、少し大きめに */
        height: auto;
        transform: rotate(-12deg); /* 💡 スタンプらしい角度 */
        pointer-events: none;
        filter: drop-shadow(4px 4px 3px rgba(0,0,0,0.4));
    ">
    """

# --- [3] キイナちゃん前日版のメインHTMLを定義 ---
kiina_zenjitsu_html = f"""
<div class="wrapper-kiina" style="width: 1000px; margin: auto; background: #fffde6; border: 6px solid #ffcc00; border-radius: 15px; overflow: hidden; font-family: 'Zen Maru Gothic', sans-serif;">
    {kiina_zenjitsu_stamp_html}
    <div style="position: relative; width: 1000px; height: 180px; overflow: hidden; border-bottom: 4px solid #ffcc00;">
        <img src="{kiina_header_img_src}" style="width: 1000px; height: auto; position: absolute; top: 0; left: 0; z-index: 1;">
        <div style="position: absolute; right: 30px; top: 25px; text-align: right; z-index: 2; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
            <div style="font-size: 22px; font-weight: 800;">{race_date}</div>
            <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 10px;">
                <span style="font-size: 48px; font-weight: 900; color: #ffcc00;">{race_place}</span>
                <span style="font-size: 42px; font-weight: 900;">{race_no}</span>
            </div>
        </div>
    </div>

    <div class="main" style="display: flex; gap: 15px; padding: 20px; background: #fffde6;">
        <div style="flex: 1.5;">
            <div class="kiina-box" style="background:#fff; border:3px solid #ffcc00; border-radius:15px; padding: 20px; margin-bottom:15px; text-align: left;">
                <div class="kiina-section-black" style="display: inline-block;">⚡ 本命候補</div>
                <div style="text-align: center;">
                    <div style="font-size: 80px; font-weight: 900; color: #000; margin: 10px 0;">◎ 5号艇</div>
                    <div style="display: flex; justify-content: space-around; gap: 10px;">
                        <div style="background:#fff; border:2px solid #000; padding:10px; border-radius:15px; flex:1;">
                            <div style="font-size:14px; font-weight:900;">5アタマ期待度</div>
                            <div style="font-size:48px; font-weight:900;">{kiina_5atama_rate}%</div>
                        </div>
                        <div style="background:#fff; border:2px solid #000; padding:10px; border-radius:15px; flex:1;">
                            <div style="font-size:14px; font-weight:900;">波乱指数</div>
                            <div style="font-size:48px; font-weight:900; color:#e60000;">{wave}</div>
                        </div>
                        <div style="background:#fff; border:2px solid #000; padding:10px; border-radius:15px; flex:1;">
                            <div style="font-size:14px; font-weight:900;">超抜気配</div>
                            <div style="font-size:24px; color:#ffcc00; margin-top:5px;">{chou_batsu}</div>
                        </div>
                    </div>
                </div>
            </div>

            {slit_box_html}

            <div class="kiina-box" style="background:#fff; border:3px solid #ffcc00; border-radius:15px; padding: 20px;">
                <div class="kiina-section-black" style="display: inline-block;">⚡ 展開ストーリー（予想）</div>
                <div style="margin-top:10px;">{story_items_html}</div>
            </div>
        </div>

        <div style="flex: 1; text-align: center;">
            <div style="position: relative;">
                <img src="{character_src}" style="width: 100%; transform: scale(1.1); position: relative; z-index: 1;">
                <div class="fukidashi" style="background:#000; color:#ffcc00; border:4px solid #ffcc00; margin-top:-30px; position:relative; z-index:2; padding:15px; border-radius:20px;">
                    <div style="border-bottom:2px solid #ffcc00; margin-bottom:10px; font-weight:bold;">⚡ キイナのひとこと</div>
                    <div style="font-weight:bold;">インが弱けりゃ私の出番でしょ！高配当いただき！</div>
                </div>
            </div>
            
            <div style="margin-top: 15px; background:rgba(0,0,0,0.9); padding:15px; border: 2px solid #ffcc00; border-radius:15px; text-align: left;">
                <div class="kiina-section-black" style="width: 100%; box-sizing: border-box; text-align: center;">⚡ 直前チェック項目</div>
                <div style="margin-top:10px;">{check_list_html}</div>
            </div>
        </div>
    </div> <div style="background: #000000; color: #ffcc00; padding: 20px; text-align: center; font-size: 32px; font-weight: 900; border-top: 4px solid #ffcc00; width: 1000px; box-sizing: border-box;">
        ⚡ {keihou_msg} ⚡
    </div>

</div> """


kiina_stamp_html = ""
if selected_stamp_path:
    # 画像を読み込んでBase64に変換
    stamp_base64 = get_stamp_base64(selected_stamp_path)
    
    # 💡edited-image.pngの赤丸の位置（キャラの横・展示ボックスの上）に配置
    kiina_stamp_html = f"""
    <img src="{stamp_base64}" style="
        position: absolute;
        top: 150px; /* 位置調整 */
        left: 480px; /* 位置調整 */
        z-index: 100; /* 最前面に */
        width: 250px; /* スタンプのサイズ */
        height: auto;
        transform: rotate(-10deg); /* 少し傾けてリアルさを出す */
        pointer-events: none; /* 下の要素のクリックを邪魔しない */
        filter: drop-shadow(3px 3px 2px rgba(0,0,0,0.3)); /* 影をつけて浮き立たせる */
    ">
    """


    
# --- [4] 最終的な kiina_html の組み立て ---
kiina_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {common_style}
    {kiina_style}
    {download_logic}
</head>
<body>
    {kiina_zenjitsu_html}
    <div style="text-align:center;">
        <button class="download-btn" style="background:#ffcc00; color:#000;" onclick="saveImage('.wrapper-kiina', 'kiina_zenjitsu.png')">画像を保存する</button>
    </div>
</body>
</html>
"""

# --- [5] キイナちゃん直前版の組み立て ---
# --- [5] キイナちゃん直前版の組み立て（ヘッダー画像 ＆ レイアウト修正版） ---
# --- [5] キイナちゃん直前版（タイトル左寄せ修正版） ---
kiina_live_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {common_style}
    {kiina_style}
    {download_logic}
</head>
<body>
<div class="wrapper-kiina" style="width: 1000px; margin: auto; background: #fffdf5; border: 6px solid #ffcc00; border-radius: 15px; overflow: hidden; font-family: 'Zen Maru Gothic', sans-serif;">
    {kiina_stamp_html}
    <div style="position: relative; width: 1000px; height: 180px; overflow: hidden; border-bottom: 4px solid #ffcc00;">
        <img src="{kiina_header_live_img_src}" style="width: 1000px; height: auto; position: absolute; top: 0; left: 0; z-index: 1;">
        <div style="position: absolute; right: 30px; top: 25px; text-align: right; z-index: 2; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
            <div style="font-size: 22px; font-weight: 800;">{race_date}</div>
            <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 10px;">
                <span style="font-size: 48px; font-weight: 900; color: #ffcc00;">{race_place}</span>
                <span style="font-size: 42px; font-weight: 900;">{race_no}</span>
            </div>
        </div>
    </div>

    <div class="main" style="display: flex; gap: 15px; padding: 20px; background: #fffdf5;">
        
        <div style="flex: 1.5; display: flex; flex-direction: column; gap: 15px;">
            

<div class="kiina-box" style="background:#fff; border:3px solid #ffcc00; border-radius:15px; padding: 20px; text-align: left;">
    <div class="kiina-section-black" style="display: inline-block;">⚡ 展示評価 ＆ 進入</div>
    
    <div style="display: flex; align-items: center; gap: 25px; margin-top: 15px;">
        <div style="flex: 0 0 100px; text-align: center;">
            <span style="font-size: 110px; font-weight: 900; color: #e60000; line-height: 0.8; font-family: 'Arial Black', sans-serif;">
                {tenji_rank}
            </span>
            <div style="font-size: 14px; font-weight: bold; color: #666; margin-top: 5px;">評価</div>
        </div>

        <div style="display: flex; gap: 12px; flex: 1;">
            <div style="border: 2px solid #000; border-radius: 8px; padding: 10px; flex: 1; text-align: center;">
                <div style="font-size: 12px; font-weight: bold; color: #666; margin-bottom: 5px;">補正タイム</div>
                <div style="font-size: 28px; font-weight: 900; color: #000;">{tenji_time}</div>
            </div>

            <div style="border: 2px solid #000; border-radius: 8px; padding: 10px; flex: 1; text-align: center;">
                <div style="font-size: 12px; font-weight: bold; color: #666; margin-bottom: 5px;">進入予想</div>
                <div style="font-size: 28px; font-weight: 900; color: #000;">{shinnyu}</div>
            </div>

            <div style="border: 3px solid #e60000; border-radius: 8px; padding: 10px; flex: 1; text-align: center; background: #fff5f5;">
                <div style="font-size: 11px; font-weight: bold; color: #e60000; margin-bottom: 5px;">4号艇展示差</div>
                <div style="font-size: 26px; font-weight: 900; color: #e60000;">{diff_4}</div>
            </div>
        </div>
    </div>
</div>

            {slit_box_html}

            <div class="kiina-box" style="background: #000; border: 4px solid #ffcc00; border-radius:15px; padding: 20px; color: #fff; text-align: left;">
                <div class="kiina-section-black" style="background:#ffcc00; color:#000;">⚡ キイナの買い目</div>
                <div style="font-size: 85px; font-weight: 900; color: #ffcc00; text-align: center; margin: 15px 0; letter-spacing: 5px;">
                    {honmei_kaime}
                </div>
                <div style="font-size: 24px; color: #fff; font-weight: bold; text-align: center; border-top: 1px dashed #555; padding-top: 10px;">
                    押さえ：{osae_kaime.replace('\\n', ' / ')}
                </div>
            </div>
        </div>

        <div style="flex: 1; text-align: center; display: flex; flex-direction: column; gap: 15px;">
            <div style="position: relative;">
                <img src="{character_src}" style="width: 100%; transform: scale(1.1); position: relative; z-index: 1;">
                <div class="fukidashi" style="background:#000; color:#ffcc00; border:4px solid #ffcc00; margin-top:-30px; position:relative; z-index:2; padding:15px; border-radius:20px; text-align: left;">
                    <div class="kiina-section-black" style="width: 100%; box-sizing: border-box; border: none; border-bottom: 2px solid #ffcc00; border-radius: 0; margin-bottom: 10px;">⚡ キイナの直前談</div>
                    <div style="font-weight:bold; font-size: 16px; padding-left: 5px;">{jikkan_comment}</div>
                    <div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 15px solid #ffcc00;"></div>
                </div>
            </div>
            
            <div style="background:rgba(0,0,0,0.9); padding:15px; border: 2px solid #ffcc00; border-radius:15px; text-align: left;">
                <div class="kiina-section-black" style="width: 100%; box-sizing: border-box; text-align: left;">⚡ 直前確認</div>
                <div style="margin-top:10px;">{check_list_html}</div>
                <div style="margin-top: 15px; border-top: 1px solid #ffcc00; padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color:#ffcc00; font-weight:bold;">🎯 的中期待度</span>
                    <span style="font-size: 32px; font-weight: 900; color: #fff;">{hit_rate}%</span>
                </div>
            </div>
        </div>
    </div>

    <div style="background: #000; color: #ffcc00; padding: 20px; text-align: center; font-size: 26px; font-weight: 900; border-top: 4px solid #ffcc00; width: 1000px; box-sizing: border-box;">
        ⚡ {keihou_msg} ⚡
    </div>

</div> <div style="text-align:center; margin-top: 20px; margin-bottom: 50px;">
    <button class="download-btn" 
            style="background:#ffcc00; color:#000; font-weight:bold; padding:10px 30px; border-radius:5px; cursor:pointer;" 
            onclick="saveImage('.wrapper-kiina', 'kiina_chokuzen.png')">
        📸 直前版を画像として保存する
    </button>
</div>

</body>
</html>
"""
# =========================================
# 初音
# =========================================
# --- 1. 画像の準備（HTMLより上で実行） ---
# 初音ちゃんのメイン画像
hatsune_character_src = get_base64_img("hatsune_main.png") # ファイル名は実際の保存名に合わせてください

# 初音ちゃん前日版のヘッダー画像
hatsune_header_img_src = get_base64_img("hatsune_header.png") 

# --- 2. 変数の初期化（HTMLより上で実行） ---
# サイドバーですでに作っている場合は、そちらが優先されます
if 'hatsune_honmei' not in locals():
    hatsune_honmei = "1号艇"
if 'wall_rank' not in locals():
    wall_rank = "A"
if 'hatsune_kaime' not in locals():
    hatsune_kaime = "1-23-4"
if 'hatsune_stamp_html' not in locals():
    hatsune_stamp_html = ""
if 'story_items_html' not in locals():
    story_items_html = "<li>ここに展開ストーリーが入ります</li>"

# --- この後に hatsune_zenjitsu_html = f"""...""" を書く ---



hatsune_style = """
<style>
/* 全体の背景 */
.wrapper-hatsune {
    width: 1000px;
    margin: auto;
    background: linear-gradient(180deg, #e0f2ff 0%, #f3e5f5 100%);
    border: 6px solid #ffb7c5;
    border-radius: 20px;
    overflow: hidden;
    font-family: 'Zen Maru Gothic', sans-serif;
    position: relative;
    padding-bottom: 0px;
}

/* ボックスデザイン */
.hatsune-box {
    background: rgba(255, 255, 255, 0.85);
    border: 2px solid #ce93d8;
    border-radius: 15px;
    padding: 12px;
    box-shadow: 2px 2px 8px rgba(179, 157, 219, 0.2);
}

/* リボンタイトル */
.hatsune-title-ribbon {
    background: linear-gradient(90deg, #9fa8da, #ce93d8);
    color: #fff;
    font-size: 16px;
    font-weight: 900;
    padding: 4px 20px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 10px;
}

/* 🌸 追加：初音ちゃんの吹き出しデザイン */
.fukidashi-hatsune {
    background: #ffffff;
    border: 3px solid #ffb7c5;
    padding: 15px;
    border-radius: 15px;
    position: relative;
    font-size: 14px;
    font-weight: bold;
    color: #5c6bc0;
    text-align: left;
}
.fukidashi-hatsune::after {
    content: "";
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    border-left: 12px solid transparent;
    border-right: 12px solid transparent;
    border-bottom: 12px solid #ffb7c5;
}
</style>
"""






# --- [1] 初音ちゃん前日版（縦長フルレイアウト） ---
hatsune_zenjitsu_html = f"""
<div class="wrapper-hatsune" style="width: 1000px; min-height: 1300px; margin: auto; background: linear-gradient(180deg, #e0f2ff 0%, #f3e5f5 100%); border: 6px solid #ffb7c5; border-radius: 20px; overflow: hidden; position: relative;">
    
    {hatsune_stamp_html}

    <div style="position: relative; width: 1000px; height: 180px; overflow: hidden; border-bottom: 4px solid #ffb7c5; border-radius: 20px 20px 0 0;">
        <img src="{new_hatsune_header_src}" style="width: 1000px; height: auto; position: absolute; top: 0; left: 0; z-index: 1;">
        
        <div style="position: absolute; right: 25px; bottom: 15px; text-align: right; z-index: 2; color: #fff; text-shadow: 2px 2px 5px rgba(126, 87, 194, 0.8);">
            <div style="font-size: 20px; font-weight: 800;">{race_date}</div>
            <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 8px;">
                <span style="font-size: 42px; font-weight: 900; color: #fff;">{race_place}</span>
                <span style="font-size: 38px; font-weight: 900; color: #ffe082;">{race_no}</span>
            </div>
        </div>
    </div>

    <div style="display: flex; gap: 20px; padding: 25px;">
        
        <div style="flex: 1.6; display: flex; flex-direction: column; gap: 15px;">
    
    <div class="hatsune-box" style="padding: 20px; border: 3px solid #b39ddb; background: rgba(255, 255, 255, 0.9);">
        
        <div style="text-align: left; margin-bottom: 20px;">
            <div class="hatsune-title-ribbon">🦋 本命ヴィーナス候補 🦋</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 30px; margin-top: 10px;">
                <div style="font-size: 80px; font-weight: 900; color: #d81b60; line-height: 1;">◎ {hatsune_honmei}</div>
                
                <div style="border: 2px solid #ffb7c5; border-radius: 12px; padding: 10px 20px; background: #fff;">
                    <div style="font-size: 12px; color: #666; font-weight: bold; margin-bottom: 3px;">女子戦リズム</div>
                    <div style="font-size: 28px; font-weight: 900; color: #ff69b4;">{hatsune_rhythm}</div>
                </div>
            </div>
        </div>

        <div style="text-align: left;">
            <div style="color: #5c6bc0; font-size: 14px; font-weight: 900; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;">
                <span style="color:#b39ddb;">◆</span> 初音の女子戦AI指数 <span style="color:#b39ddb;">◆</span>
            </div>
            
            <div style="display: flex; gap: 10px; justify-content: space-between;">
                <div style="flex: 1; border: 1.5px solid #ce93d8; border-radius: 10px; padding: 8px; text-align: center; background: #fff;">
                    <div style="font-size: 10px; color: #7e57c2; margin-bottom: 4px; font-weight: bold;">壁信頼度</div>
                    <div style="font-size: 24px; font-weight: 900; color: #5c6bc0;">{wall_rank}</div>
                </div>

                <div style="flex: 1; border: 1.5px solid #ce93d8; border-radius: 10px; padding: 8px; text-align: center; background: #fff;">
                    <div style="font-size: 10px; color: #7e57c2; margin-bottom: 4px; font-weight: bold;">当地相性</div>
                    <div style="font-size: 24px; font-weight: 900; color: #5c6bc0;">88%</div>
                </div>

                <div style="flex: 1; border: 1.5px solid #ce93d8; border-radius: 10px; padding: 8px; text-align: center; background: #fff;">
                    <div style="font-size: 10px; color: #7e57c2; margin-bottom: 4px; font-weight: bold;">ST安定度</div>
                    <div style="font-size: 24px; font-weight: 900; color: #5c6bc0;">92%</div>
                </div>

                <div style="flex: 1; border: 2px solid #ffb7c5; border-radius: 10px; padding: 8px; text-align: center; background: #fdf2f4;">
                    <div style="font-size: 10px; color: #d81b60; margin-bottom: 4px; font-weight: bold;">総合評価</div>
                    <div style="font-size: 24px; font-weight: 900; color: #ff69b4;">S</div>
                </div>
            </div>
        </div>
    </div>
            <div class="hatsune-box" style="text-align: left; min-height: 200px;">
                <div class="hatsune-title-ribbon">✨ 展開ストーリー（予想） ✨</div>
                <div style="font-size: 16px; line-height: 1.8; color: #444; padding: 10px;">
                    {story_items_html}
                </div>
            </div>

           # --- [推奨買い目] を [ピックアップ選手] に変更 ---
# --- hatsune_zenjitsu_html 内の修正箇所 ---
<div class="hatsune-box" style="background: linear-gradient(135deg, #f3e5f5, #e8eaf6); border: 3px solid #b39ddb; padding: 15px;">
    <div class="hatsune-box">
        <div class="hatsune-title-ribbon">👗 初音の注目ピックアップ 👗</div>
        <div style="display: flex; flex-direction: column; margin-top: 10px;">
            {pickup_html_list}  </div>
    </div>
</div>

        
            <div class="hatsune-box" style="text-align: left;">
                <div class="hatsune-title-ribbon" style="font-size: 12px;">📒 女子戦特化メモ</div>
                <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
                    <tr style="border-bottom: 1px dashed #ffb7c5;"><td style="padding: 8px 0;">イン1着率</td><td style="text-align:right; font-weight:bold;">42.5%</td></tr>
                    <tr style="border-bottom: 1px dashed #ffb7c5;"><td style="padding: 8px 0;">波乱指数</td><td style="text-align:right; font-weight:bold; color:#ba68c8;">★★★☆☆</td></tr>
                    <tr><td style="padding: 8px 0;">調整メモ</td><td style="text-align:right; font-size:12px;">{weight_memo}</td></tr>
                </table>
            </div>
        </div>
    </div>

    <div style="background: linear-gradient(90deg, #9fa8da, #ce93d8); color: #fff; padding: 20px; text-align: center; font-size: 24px; font-weight: 900; border-top: 4px solid #fff;">
        🌸 Venus Statistics - 初音の女子戦分析 🌸
    </div>
</div>
"""




hatsune_live_html = hatsune_zenjitsu_html





# =========================================
# 6. メインタブ表示
# =========================================

main_tab1, main_tab2, main_tab3= st.tabs([
    "🌸 一果ちゃん",
    "⚡ キイナちゃん",
    "👗 初音ちゃん",
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
        
# --- 初音ちゃんタブ ---
with main_tab3:
    sub_tab5, sub_tab6 = st.tabs(["👗 前日版", "👗 直前版"])
    with sub_tab5:
        html(hatsune_zenjitsu_html, height=2600, scrolling=True)
    with sub_tab6:
        html(hatsune_live_html, height=2600, scrolling=True)
