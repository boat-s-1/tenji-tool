import streamlit as st
from streamlit.components.v1 import html
import base64
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

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
    "1号艇": get_base64_img("9090142A-8DC0-475F-9518-A4D9218D9D44.png"),
    "2号艇": get_base64_img("0EDEF6B0-E300-443D-BE83-B6343AA48853.png"),
    "3号艇": get_base64_img("40494128-D801-4F5A-A22B-8C2E57C607D5.png"),
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

new_hatsune_header_src = get_base64_img("S__18178051_0.jpg")
live_hatsune_header_src = get_base64_img("S__18178052_0.jpg")

# 12R新聞専用のロゴを新しく定義する場合
logo_grade_path = "S__18513925.jpg" # 実際のファイル名
logo_grade_src = get_base64_img(logo_grade_path)
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
with st.sidebar.expander("👗 初音の女子戦設定"):
    # アップローダーの設置
    hatsune_upload_img = st.file_uploader("初音ちゃんの画像を差し替え", type=['png', 'jpg', 'jpeg'], key="hatsune_main_upload")

    # 画像の優先順位付け（アップロード > デフォルト）
    if hatsune_upload_img:
        import base64
        base64_img = base64.b64encode(hatsune_upload_img.getvalue()).decode()
        hatsune_character_src = f"data:image/png;base64,{base64_img}"
    else:
        # デフォルト画像（既存のパスやURLを指定）
        hatsune_character_src = "https://your-default-image-url.png"

selected_hatsune_stamp_label = st.selectbox("初音のスタンプ", ["なし"] + list(stamp_dict.keys()), index=0, key="hatsune_stamp_select")
with st.sidebar.expander("✨ 速報ステッカー"):
    frame_type = st.selectbox(
        "フレーム種類",
        ["鉄板", "危険", "ヴィーナス", "5アタマ", "プレミア"]
    )

    sticker_place = st.text_input("レース場", race_place)
    sticker_race = st.text_input("レース番号", race_no)

    main_text = st.text_input("メイン表示", "92%")
    sub_text = st.text_input("サブ表示", "信頼度")
    kaime_text = st.text_input("買い目", "1-2-3")
    memo_text = st.text_input("一言", "本線勝負！")


    
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



def get_font(size):
    font_list = [
        "fonts/NotoSansJP-Bold.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]

    for f in font_list:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass

    return ImageFont.load_default()


def create_frame_sticker(
    frame_type="鉄板",
    place="丸亀",
    race="1R",
    main_text="92%",
    sub_text="信頼度",
    kaime_text="1-2-3",
    memo_text="本線勝負！"
):
    frame_files = {
        "鉄板": "frames/teppan.png",
        "危険": "frames/kiken.png",
        "ヴィーナス": "frames/venus.png",
        "5アタマ": "frames/five_atama.png",
        "プレミア": "frames/premium.png",
    }

    frame_path = frame_files.get(frame_type, "frames/teppan.png")

    img = Image.open(frame_path).convert("RGBA")
    img = img.resize((1080, 1080))

    draw = ImageDraw.Draw(img)

    font_main = get_font(190)
    font_sub = get_font(70)
    font_kaime = get_font(95)
    font_small = get_font(48)

    if frame_type == "危険":
        main_color = "#e60000"
        sub_color = "#111111"
    elif frame_type == "5アタマ":
        main_color = "#ffcc00"
        sub_color = "#111111"
    elif frame_type == "ヴィーナス":
        main_color = "#b24cff"
        sub_color = "#5a247a"
    elif frame_type == "プレミア":
        main_color = "#d4af37"
        sub_color = "#111111"
    else:
        main_color = "#ff4f93"
        sub_color = "#111111"

    # レース場・R
    draw.text(
        (85, 315),
        f"{place} {race}",
        fill=sub_color,
        font=font_small
    )

    # サブ表示
    draw.text(
        (90, 390),
        sub_text,
        fill=sub_color,
        font=font_sub
    )

    # メイン表示
    draw.text(
        (90, 470),
        main_text,
        fill=main_color,
        font=font_main
    )

    # 買い目ボックス
    draw.rounded_rectangle(
        (90, 705, 620, 825),
        radius=30,
        fill="#ffffff",
        outline=main_color,
        width=6
    )

    draw.text(
        (125, 710),
        kaime_text,
        fill="#111111",
        font=font_kaime
    )

    # 一言
    draw.text(
        (95, 855),
        memo_text,
        fill=main_color,
        font=font_sub
    )

    return img

def create_sns_mark_image(
    mode="危険",
    place="丸亀",
    race_no="1R",
    deadline="15:24",
    rate=28,
    main="3-2-5",
    step1="1号艇は流される",
    step2="2号艇が絞って攻める",
    step3="3号艇が差して決着へ"
):
    W, H = 1080, 1080

    img = Image.new("RGB", (W, H), "#050505")
    draw = ImageDraw.Draw(img)

    FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

    try:
        font_big = ImageFont.truetype(FONT_PATH, 120)
        font_rate = ImageFont.truetype(FONT_PATH, 170)
        font_mid = ImageFont.truetype(FONT_PATH, 52)
        font_small = ImageFont.truetype(FONT_PATH, 38)
    except:
        font_big = ImageFont.load_default()
        font_rate = ImageFont.load_default()
        font_mid = ImageFont.load_default()
        font_small = ImageFont.load_default()

    if mode == "危険":
        main_color = "#e60000"
        title = "危険"
        label = "イン逃げ成功率"
        msg = "波乱の可能性高い！"
    else:
        main_color = "#ffcc00"
        title = "鉄板！"
        label = "イン逃げ信頼度"
        msg = "軸選手は1号艇！"

    draw.rectangle((0, 0, W-1, H-1), outline=main_color, width=10)

    draw.text((70, 60), title, fill=main_color, font=font_big)
    draw.text((760, 80), f"{place} {race_no}", fill="white", font=font_mid)
    draw.text((800, 165), f"締切 {deadline}", fill="white", font=font_small)

    draw.text((70, 250), label, fill="white", font=font_mid)
    draw.text((70, 315), f"{rate}%", fill=main_color, font=font_rate)

    draw.text((70, 845), f"① {step1}", fill="white", font=font_small)
    draw.text((70, 895), f"② {step2}", fill="white", font=font_small)
    draw.text((70, 945), f"③ {step3}", fill="white", font=font_small)

    draw.rounded_rectangle((700, 860, 1010, 1010), radius=22, fill="white")
    draw.text((735, 895), main, fill="black", font=font_big)

    draw.text((70, 1000), msg, fill="#ffcc00", font=font_small)

    return img

# =========================================
# 📱 SNS画像ツール 入力
# =========================================

st.sidebar.header("📱 SNS画像ツール設定")

with st.sidebar.expander("🚨 SNS画像 基本情報"):
    sns_mode = st.selectbox("画像タイプ", ["危険", "鉄板"])
    sns_place = st.text_input("SNS用 レース場", race_place)
    sns_race_no = st.text_input("SNS用 レース番号", race_no)
    sns_deadline = st.text_input("SNS用 締切", "15:24")

    sns_rate = st.slider("成功率 / 信頼度", 0, 100, 28)
    sns_main = st.text_input("本線予想", "3-2-5")

with st.sidebar.expander("🚤 1マーク展開"):
    sns_step1 = st.text_input("展開①", "1号艇は流される")
    sns_step2 = st.text_input("展開②", "2号艇が絞って攻める")
    sns_step3 = st.text_input("展開③", "3号艇が差して決着へ")
    sns_axis = st.selectbox("軸選手", [f"{i}号艇" for i in range(1, 7)], index=2)

turn_mark_svg = """
<svg viewBox="0 0 900 320"
     style="width:100%;height:100%;">

<rect width="900" height="320" fill="#00627f"/>

<!-- ターンマーク -->
<circle cx="650" cy="160" r="35"
        fill="white" stroke="white"/>

<!-- 1号艇 -->
<ellipse cx="250" cy="100"
         rx="55" ry="28"
         fill="white"/>

<text x="250" y="115"
      text-anchor="middle"
      font-size="40"
      font-weight="bold">1</text>

<!-- 2号艇 -->
<ellipse cx="360" cy="160"
         rx="55" ry="28"
         fill="#111"/>

<text x="360" y="175"
      text-anchor="middle"
      font-size="40"
      font-weight="bold"
      fill="white">2</text>

<!-- 3号艇 -->
<ellipse cx="250" cy="240"
         rx="55" ry="28"
         fill="#e60000"/>

<text x="250" y="255"
      text-anchor="middle"
      font-size="40"
      font-weight="bold"
      fill="white">3</text>

<!-- 2号艇まくり -->
<path d="M410 160 C520 130 620 110 760 70"
      stroke="black"
      stroke-width="14"
      fill="none"/>

<!-- 3号艇差し -->
<path d="M300 240 C420 200 540 160 640 140"
      stroke="red"
      stroke-width="14"
      fill="none"/>

</svg>
"""

# =========================================
# ✨ SNSステッカー生成 完全版
# =========================================

def get_font(size):
    font_candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]

    for font_path in font_candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            pass

    return ImageFont.load_default()


# =========================================
# BOAT STRIKE SNSステッカー完成版
# =========================================

def get_font(size):
    font_candidates = [
        "fonts/NotoSansJP-Bold.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]

    for font_path in font_candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            pass

    return ImageFont.load_default()


def create_boatstrike_sticker(
    sticker_type="鉄板",
    place="丸亀",
    race_no="1R",
    value="92%",
    boat="1号艇",
    kaime="1-2-3"
):
    W, H = 1080, 1080

    designs = {
        "鉄板": {
            "emoji": "🔥",
            "title": "鉄板",
            "label": "イン逃げ信頼度",
            "main": "#ffcc00",
            "bg": "#090909",
            "accent": "#ffffff"
        },
        "危険": {
            "emoji": "🚨",
            "title": "危険",
            "label": "イン逃げ成功率",
            "main": "#e60000",
            "bg": "#150000",
            "accent": "#ffcc00"
        },
        "超抜": {
            "emoji": "⚡",
            "title": "超抜",
            "label": "展示評価",
            "main": "#ffcc00",
            "bg": "#080808",
            "accent": "#ffffff"
        },
        "5アタマ": {
            "emoji": "⚡",
            "title": "5アタマ",
            "label": "穴期待度",
            "main": "#ffcc00",
            "bg": "#111100",
            "accent": "#ffffff"
        },
        "ヴィーナス": {
            "emoji": "👑",
            "title": "ヴィーナス",
            "label": "女子戦本命",
            "main": "#ce93d8",
            "bg": "#130018",
            "accent": "#ffffff"
        },
    }

    d = designs.get(sticker_type, designs["鉄板"])

    img = Image.new("RGBA", (W, H), d["bg"])
    draw = ImageDraw.Draw(img)

    title_font = get_font(125)
    label_font = get_font(58)
    value_font = get_font(245)
    boat_font = get_font(90)
    kaime_font = get_font(86)
    logo_font = get_font(46)
    small_font = get_font(42)

    # 背景装飾
    draw.ellipse((620, -120, 1250, 520), fill=(255, 255, 255, 18))
    draw.ellipse((-220, 650, 420, 1250), fill=(255, 255, 255, 12))

    # 外枠
    draw.rounded_rectangle(
        (30, 30, 1050, 1050),
        radius=60,
        outline=d["main"],
        width=16
    )

    draw.rounded_rectangle(
        (65, 65, 1015, 1015),
        radius=45,
        outline=d["main"],
        width=4
    )

    # レース情報
    draw.rounded_rectangle(
        (650, 90, 990, 175),
        radius=25,
        fill=d["main"]
    )
    draw.text(
        (685, 108),
        f"{place} {race_no}",
        fill="#000000",
        font=small_font
    )

    # タイトル
    draw.text(
        (80, 95),
        f'{d["emoji"]} {d["title"]}',
        fill=d["main"],
        font=title_font
    )

    # ラベル
    draw.text(
        (90, 280),
        d["label"],
        fill=d["accent"],
        font=label_font
    )

    # 数値
    draw.text(
        (90, 350),
        value,
        fill=d["main"],
        font=value_font
    )

    # 対象艇
    draw.rounded_rectangle(
        (90, 685, 990, 820),
        radius=35,
        fill=d["main"]
    )
    draw.text(
        (145, 705),
        f"◎ {boat}",
        fill="#000000",
        font=boat_font
    )

    # 買い目
    draw.rounded_rectangle(
        (90, 850, 990, 945),
        radius=28,
        fill="#ffffff"
    )
    draw.text(
        (145, 850),
        f"本線 {kaime}",
        fill="#000000",
        font=kaime_font
    )

    # ロゴ
    draw.text(
        (90, 975),
        "BOAT STRIKE",
        fill="#ffffff",
        font=logo_font
    )

    return img

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

        <div style="width: 340px; flex-shrink: 0; text-align: center; display: flex; flex-direction: column; align-items: center;">
            <div style="position: relative; width: 100%;">
                <img src="{character_src}" style="width: 100%; max-width: 280px; height: auto; position: relative; z-index: 1;">
                
                <div class="fukidashi" style="background:#000; color:#ffcc00; border:4px solid #ffcc00; margin-top:-40px; position:relative; z-index:2; padding:15px; border-radius:20px; text-align: left; width: 90%; box-sizing: border-box;">
                    <div style="border-bottom:2px solid #ffcc00; margin-bottom:10px; font-weight:bold;">⚡ キイナのひとこと</div>
                    <div style="font-weight:bold; font-size: 15px; line-height: 1.4;">インが弱けりゃ私の出番でしょ！高配当いただき！</div>
                </div>
            </div>
            
            <div style="margin-top: 15px; background:rgba(0,0,0,0.9); padding:15px; border: 2px solid #ffcc00; border-radius:15px; text-align: left; width: 90%; box-sizing: border-box;">
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
# --- [5] キイナちゃん直前版（キャラクター画像サイズ修正版） ---
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

        <div style="width: 340px; flex-shrink: 0; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 15px;">
            <div style="position: relative; width: 100%;">
                <img src="{character_src}" style="width: 100%; max-width: 280px; height: auto; position: relative; z-index: 1;">
                
                <div class="fukidashi" style="background:#000; color:#ffcc00; border:4px solid #ffcc00; margin-top:-40px; position:relative; z-index:2; padding:15px; border-radius:20px; text-align: left; width: 90%; box-sizing: border-box;">
                    <div class="kiina-section-black" style="width: 100%; box-sizing: border-box; border: none; border-bottom: 2px solid #ffcc00; border-radius: 0; margin-bottom: 10px; padding-left: 0;">⚡ キイナの直前談</div>
                    <div style="font-weight:bold; font-size: 15px; line-height: 1.4;">{jikkan_comment}</div>
                    <div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-bottom: 15px solid #ffcc00;"></div>
                </div>
            </div>
            
            <div style="background:rgba(0,0,0,0.9); padding:15px; border: 2px solid #ffcc00; border-radius:15px; text-align: left; width: 90%; box-sizing: border-box;">
                <div class="kiina-section-black" style="width: 100%; box-sizing: border-box; text-align: center;">⚡ 直前確認</div>
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

</div> 
<div style="text-align:center; margin-top: 20px; margin-bottom: 50px;">
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
# 👗 初音ちゃんセクション（前日版・直前版 完全統合）
# =========================================

# --- 1. 専用スタイルの定義 ---
hatsune_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700;900&display=swap');

.wrapper-hatsune-zenjitsu, .wrapper-hatsune-live {
    width: 1000px;
    margin: auto;
    background: linear-gradient(180deg, #e0f2ff 0%, #f3e5f5 100%);
    border: 6px solid #ffb7c5;
    border-radius: 20px;
    overflow: hidden;
    font-family: 'Zen Maru Gothic', sans-serif;
    position: relative;
    box-shadow: 0 0 25px rgba(206, 147, 216, 0.3);
}

.hatsune-box {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid #ce93d8;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 2px 2px 8px rgba(179, 157, 219, 0.2);
}

.hatsune-title-ribbon {
    background: linear-gradient(90deg, #9fa8da, #ce93d8);
    color: #fff;
    font-size: 16px;
    font-weight: 900;
    padding: 6px 20px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 12px;
}

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
    box-shadow: 0 4px 12px rgba(179,157,219,0.3);
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

# --- 2. 【前日版】HTML組み立て ---
hatsune_zenjitsu_body = f"""
<div class="wrapper-hatsune-zenjitsu">
    <!-- ヘッダー -->
    <div style="position: relative; width: 1000px; height: 180px; overflow{new_hatsune_header_src}: hidden; border-bottom: 4px solid #ffb7c5;">
        <img src="{new_hatsune_header_src}" style="width: 1000px; height: auto; position: absolute; top: 0; left: 0; z-index: 1;">
        <div style="position: absolute; right: 25px; bottom: 15px; text-align: right; z-index: 2; color: #fff; text-shadow: 2px 2px 5px rgba(126, 87, 194, 0.8);">
            <div style="font-size: 20px; font-weight: 800;">{race_date}</div>
            <div style="display: flex; justify-content: flex-end; a{new_hatsune_header_src}lign-items: baseline; gap: 8px;">
                <span style="font-size: 42px; font-weight: 900; color: #fff;">{race_place}</span>
                <span style="font-size: 38px; font-weight: 900; color: #ffe082;">{race_no}</span>
            </div>
        </div>
    </div>

    <!-- メインコンテンツ -->
<div class="main" style="display: flex; gap: 20px; padding: 25px; align-items: flex-start; background: transparent; width: 1000px; box-sizing: border-box;">
        
        <div style="width: 610px; flex-shrink: 0; display: flex; flex-direction: column; gap: 15px;">
            <div class="hatsune-box">
                <div class="hatsune-title-ribbon">🦋 本命ヴィーナス候補 🦋</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 30px; margin-top: 10px;">
                    <div style="font-size: 70px; font-weight: 900; color: #d81b60; line-height: 1;">◎ {hatsune_honmei}</div>
                    <div style="border: 2px solid #ffb7c5; border-radius: 12px; padding: 10px 20px; background: #fff; text-align: center;">
                        <div style="font-size: 12px; color: #666; font-weight: bold; margin-bottom: 3px;">女子戦リズム</div>
                        <div style="font-size: 24px; font-weight: 900; color: #ff69b4;">{hatsune_rhythm}</div>
                    </div>
                </div>
                
                <div style="margin-top: 20px; text-align: left;">
                    <div style="color: #5c6bc0; font-size: 14px; font-weight: 900; margin-bottom: 10px;">◆ 初音の女子戦AI指数 ◆</div>
                    <div style="display: flex; gap: 10px; justify-content: space-between;">
                        <div style="flex: 1; border: 1.5px solid #ce93d8; border-radius: 10px; padding: 8px; text-align: center; background: #fff;">
                            <div style="font-size: 10px; color: #7e57c2; margin-bottom: 4px; font-weight: bold;">壁信頼度</div>
                            <div style="font-size: 22px; font-weight: 900; color: #5c6bc0;">{wall_rank}</div>
                        </div>
                        <div style="flex: 1; border: 1.5px solid #ce93d8; border-radius: 10px; padding: 8px; text-align: center; background: #fff;">
                            <div style="font-size: 10px; color: #7e57c2; margin-bottom: 4px; font-weight: bold;">当地相性</div>
                            <div style="font-size: 22px; font-weight: 900; color: #5c6bc0;">88%</div>
                        </div>
                        <div style="flex: 1; border: 1.5px solid #ce93d8; border-radius: 10px; padding: 8px; text-align: center; background: #fff;">
                            <div style="font-size: 10px; color: #7e57c2; margin-bottom: 4px; font-weight: bold;">ST安定度</div>
                            <div style="font-size: 22px; font-weight: 900; color: #5c6bc0;">92%</div>
                        </div>
                        <div style="flex: 1; border: 2px solid #ffb7c5; border-radius: 10px; padding: 8px; text-align: center; background: #fdf2f4;">
                            <div style="font-size: 10px; color: #d81b60; margin-bottom: 4px; font-weight: bold;">総合評価</div>
                            <div style="font-size: 22px; font-weight: 900; color: #ff69b4;">S</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="hatsune-box">
                <div class="hatsune-title-ribbon">✨ 展開ストーリー（予想） ✨</div>
                <div style="border: 1.5px dashed #b39ddb; border-radius: 10px; padding: 15px; background: #fdfbff; text-align: left;">
                    {story_items_html}
                </div>
            </div>

            <div class="hatsune-box" style="background: linear-gradient(135deg, #f3e5f5, #e8eaf6);">
                <div class="hatsune-title-ribbon" style="background: #7e57c2;">👗 初音の注目ピックアップ 👗</div>
                <div style="display: flex; flex-direction: column; gap: 5px;">
                    {pickup_html_list}
                </div>
            </div>
        </div>

        <div style="width: 340px; flex-shrink: 0; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 15px;">
            <div style="position: relative; width: 100%; display: flex; flex-direction: column; align-items: center;">
                <img src="{character_src}" style="width: 100%; max-width: 280px; height: auto; position: relative; z-index: 1; filter: drop-shadow(0 8px 12px rgba(179,157,219,0.4));">
                
                <div class="fukidashi-hatsune" style="margin-top: -40px; position: relative; z-index: 2; width: 95%; box-sizing: border-box;">
                    <div style="font-size: 14px; font-weight: 900; color: #5c6bc0; margin-bottom: 5px; border-bottom: 2px solid #ffb7c5; display: inline-block;">
                        👗 初音の女子戦コメ
                    </div>
                    <div style="font-size: 13px; line-height: 1.5; color: #444; text-align: left;">
                        「女子戦はリズムが大事。体重調整も仕上がってるこの子が主役よ♪」
                    </div>
                </div>
            </div>

            <div class="hatsune-box" style="text-align: left; width: 95%; box-sizing: border-box;">
                <div class="hatsune-title-ribbon" style="font-size: 12px; margin-bottom: 10px;">📍 注目ヴィーナス</div>
                <ul style="font-size: 13px; padding-left: 20px; color: #444; line-height: 1.8; margin: 0;">
                    <li>2号艇：差しハンドル鋭い！</li>
                    <li>4号艇：カドから展開作る！</li>
                    <li>近況の女子戦リズム重視♡</li>
                </ul>
            </div>

            <div class="hatsune-box" style="text-align: left; width: 95%; box-sizing: border-box;">
                <div class="hatsune-title-ribbon" style="font-size: 12px; margin-bottom: 10px;">📒 女子戦特化メモ</div>
                <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
                    <tr style="border-bottom: 1px dashed #ffb7c5;">
                        <td style="padding: 8px 0; color: #666;">イン1着率</td>
                        <td style="text-align:right; font-weight:bold; color: #d81b60;">42.5%</td>
                    </tr>
                    <tr style="border-bottom: 1px dashed #ffb7c5;">
                        <td style="padding: 8px 0; color: #666;">波乱指数</td>
                        <td style="text-align:right; font-weight:bold; color:#ba68c8;">★★★☆☆</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-size: 11px; color: #999;">調整メモ</td>
                        <td style="text-align:right; font-size:11px; color:#666;">{weight_memo}</td>
                    </tr>
                </table>
            </div>
        </div>
        
    </div>

    <!-- フッター -->
    <div style="background: linear-gradient(90deg, #9fa8da, #ce93d8); color: #fff; padding: 15px; text-align: center; font-size: 20px; font-weight: 900; border-top: 4px solid #fff;">
        🌸 Venus Statistics - 初音の女子戦分析 🌸
    </div>
</div>
"""

# --- 3. 【直前版】HTML組み立て ---
hatsune_live_body = f"""
<div class="wrapper-hatsune-live">
    <!-- LIVE帯 -->
    <div style="background:#ce93d8; color:white; padding:12px; font-size:28px; font-weight:bold; text-align:center; letter-spacing: 2px;">
        👗 展示終了！初音のヴィーナスLIVE判定 👗
    </div>

    <!-- ヘッダー -->
    <div style="position: relative; width: 1000px; height: 180px; overflow: hidden; border-bottom: 4px solid #ffb7c5;">
        <img src="{live_hatsune_header_src}" style="width: 1000px; height: auto; position: absolute; top: 0; left: 0; z-index: 1;">
        <div style="position: absolute; right: 25px; bottom: 15px; text-align: right; z-index: 2; color: #fff; text-shadow: 2px 2px 5px rgba(126, 87, 194, 0.8);">
            <div style="font-size: 20px; font-weight: 800;">{race_date}</div>
            <div style="display: flex; justify-content: flex-end; align-items: baseline; gap: 8px;">
                <span style="font-size: 42px; font-weight: 900; color: #fff;">{race_place}</span>
                <span style="font-size: 38px; font-weight: 900; color: #ffe082;">{race_no}</span>
            </div>
        </div>
    </div>

    <!-- メインコンテンツ -->
<div class="main" style="display: flex; gap: 20px; padding: 25px; align-items: flex-start; background: transparent; width: 1000px; box-sizing: border-box;">
        
        <div style="width: 610px; flex-shrink: 0; display: flex; flex-direction: column; gap: 15px;">
            <div class="hatsune-box">
                <div class="hatsune-title-ribbon" style="background: #7e57c2;">💖 展示評価 ＆ 進入 💖</div>
                <div style="display: flex; align-items: center; justify-content: center; gap: 30px; margin-top: 15px;">
                    <div style="font-size: 80px; font-weight: 900; color: #ba68c8; line-height: 1; font-family: 'Arial Black', sans-serif;">
                        {tenji_rank}
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 8px; flex: 1;">
                        <div style="border: 1.5px solid #b39ddb; border-radius: 8px; padding: 6px 12px; background: #fff; display: flex; justify-content: space-between;">
                            <span style="font-size: 12px; color: #666; font-weight: bold;">補正タイム</span>
                            <span style="font-size: 16px; font-weight: 900; color: #444;">{tenji_time}</span>
                        </div>
                        <div style="border: 1.5px solid #b39ddb; border-radius: 8px; padding: 6px 12px; background: #fff; display: flex; justify-content: space-between;">
                            <span style="font-size: 12px; color: #666; font-weight: bold;">進入予想</span>
                            <span style="font-size: 16px; font-weight: 900; color: #444;">{shinnyu}</span>
                        </div>
                    </div>
                </div>
            </div>

            {slit_box_html}

            <div class="hatsune-box" style="background: linear-gradient(135deg, #fff5f8, #fdf2f4); border: 3px solid #ffb7c5;">
                <div class="hatsune-title-ribbon" style="background: #d81b60;">💋 初音のヴィーナスアイ（買い目） 💋</div>
                <div style="font-size: 75px; font-weight: 900; color: #d81b60; text-align: center; margin: 15px 0; letter-spacing: 3px; line-height: 1;">
                    {honmei_kaime}
                </div>
                <div style="font-size: 20px; color: #5c6bc0; font-weight: bold; text-align: center; border-top: 1px dashed #ffb7c5; padding-top: 10px; margin-top: 10px;">
                    押さえ：{osae_kaime.replace('\\n', ' / ')}
                </div>
            </div>
        </div>

        <div style="width: 340px; flex-shrink: 0; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 15px;">
            <div style="position: relative; width: 100%; display: flex; flex-direction: column; align-items: center;">
                <img src="{character_src}" style="width: 100%; max-width: 280px; height: auto; position: relative; z-index: 1; filter: drop-shadow(0 8px 12px rgba(179,157,219,0.4));">
                
                <div class="fukidashi-hatsune" style="margin-top: -40px; position: relative; z-index: 2; width: 95%; box-sizing: border-box;">
                    <div class="hatsune-title-ribbon" style="font-size: 12px; margin-bottom: 8px; background: #7e57c2; width: auto; display: inline-block; padding: 3px 15px;">
                        👗 直前リアルタイム談
                    </div>
                    <div style="font-size: 13px; line-height: 1.5; color: #444; text-align: left;">
                        {jikkan_comment}
                    </div>
                </div>
            </div>
            
            <div class="hatsune-box" style="text-align: left; background: #fdfbff; width: 95%; box-sizing: border-box;">
                <div class="hatsune-title-ribbon" style="font-size: 12px; margin-bottom: 10px; background: #5c6bc0;">
                    ⚡ 展示気配メモ
                </div>
                <div style="font-size: 14px; font-weight: bold; color: #444; line-height: 1.6;">
                    {motor_eval}
                </div>
                
                <div style="margin-top: 15px; border-top: 1px dashed #ce93d8; padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color:#7e57c2; font-weight:bold; font-size: 13px;">🎯 的中期待度</span>
                    <span style="font-size: 28px; font-weight: 900; color: #d81b60;">{hit_rate}%</span>
                </div>
            </div>
        </div>
        
    
                <div style="font-size: 14px; color: #7e57c2; font-weight: bold; text-align: right;">
                    女子戦特化型<br>直前LIVEシステム
                </div>
            </div>

            <!-- 最終買い目 -->
           
        </div>

</div>
"""

# --- 4. JavaScriptを含む完全なHTMLの生成関数 ---
def generate_hatsune_html(body_content, target_class, filename):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        {hatsune_style}
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
        function saveHatsuneImage() {{
            const target = document.querySelector('{target_class}');
            html2canvas(target, {{
                useCORS: true,
                scale: 2,
                backgroundColor: "#ffffff"
            }}).then(canvas => {{
                const link = document.createElement('a');
                link.download = '{filename}';
                link.href = canvas.toDataURL('image/png');
                link.click();
            }});
        }}
        </script>
        <style>
        .download-btn-hatsune {{
            display: block; width: 240px; margin: 20px auto; padding: 12px;
            background: linear-gradient(90deg, #ffb7c5, #ce93d8); color: white;
            border: none; border-radius: 50px; font-size: 16px; font-weight: bold;
            cursor: pointer; box-shadow: 0 4px 12px rgba(179,157,219,0.4); transition: 0.2s;
        }}
        .download-btn-hatsune:hover {{ opacity: 0.9; transform: translateY(-1px); }}
        </style>
    </head>
    <body style="background: transparent; padding: 10px; margin: 0;">
        {body_content}
        <button class="download-btn-hatsune" onclick="saveHatsuneImage()">📸 画像として保存する</button>
    </body>
    </html>
    """

hatsune_zenjitsu_final_html = generate_hatsune_html(hatsune_zenjitsu_body, '.wrapper-hatsune-zenjitsu', f'hatsune_zenjitsu_{race_place}_{race_no}.png')
hatsune_live_final_html = generate_hatsune_html(hatsune_live_body, '.wrapper-hatsune-live', f'hatsune_live_{race_place}_{race_no}.png')





# =========================================
# 🏆 グレードレース特別紙（前日版・完成版）
# =========================================

st.sidebar.header("🏆 グレードレース12R設定")

with st.sidebar.expander("📰 12R新聞 共通情報"):

    grade_title = st.text_input(
        "Gタイトル",
        "G1 全日本王者決定戦",
        key="g_title"
    )

    grade_date = st.text_input(
        "G開催日",
        race_date,
        key="g_date"
    )

    grade_place = st.text_input(
        "G開催場",
        race_place,
        key="g_place"
    )

    grade_hit = st.text_input(
        "実績表示",
        "的中率72%｜万舟4本",
        key="g_hit"
    )

# =========================================
# データ格納
# =========================================

all_races_data = {}

# =========================================
# 12R入力欄
# =========================================

for r in range(1, 13):

    with st.sidebar.expander(f"🏁 {r}R 予想入力"):

        race_grade = st.text_input(
            f"{r}R グレード表示",
            "グレードレース",
            key=f"g_grade_{r}"
        )

        race_rank = st.selectbox(
            f"{r}R 注目度",
            ["🔥鉄板", "🎯本線", "💣波乱", "⚠荒れ注意"],
            key=f"g_rank_{r}"
        )

        ichika_mark = st.selectbox(
            f"{r}R 一果",
            ["◎", "○", "▲", "△", "×", "―"],
            index=0,
            key=f"g_i_m_{r}"
        )

        hatsune_mark = st.selectbox(
            f"{r}R 初音",
            ["◎", "○", "▲", "△", "×", "―"],
            index=1,
            key=f"g_h_m_{r}"
        )

        kiina_mark = st.selectbox(
            f"{r}R キイナ",
            ["◎", "○", "▲", "△", "×", "―"],
            index=2,
            key=f"g_k_m_{r}"
        )

        main_kaime = st.text_input(
            f"{r}R 本線",
            "1-2-3",
            key=f"g_main_{r}"
        )

        sub_kaime = st.text_input(
            f"{r}R 抑え",
            "1-3-2 / 1-2-4",
            key=f"g_sub_{r}"
        )

        race_memo = st.text_input(
            f"{r}R 短評",
            "イン信頼度高。前付け注意。",
            key=f"g_memo_{r}"
        )

        haran = st.selectbox(
            f"{r}R 波乱度",
            ["★", "★★", "★★★"],
            index=1,
            key=f"g_haran_{r}"
        )

        deadline = st.text_input(
            f"{r}R 締切",
            "14:32",
            key=f"g_dead_{r}"
        )

        all_races_data[r] = {
            "grade": race_grade,
            "rank": race_rank,
            "ichika": ichika_mark,
            "hatsune": hatsune_mark,
            "kiina": kiina_mark,
            "main": main_kaime,
            "sub": sub_kaime,
            "memo": race_memo,
            "haran": haran,
            "deadline": deadline
        }

# =========================================
# CSS
# =========================================

grade_style = """
<style>

body{
    background:#ececec;
    font-family:sans-serif;
}

.paper-wrapper{
    width:1300px;
    margin:auto;
    background:#fffdf7;
    border:5px solid #222;
    padding:20px;
    box-sizing:border-box;
}

.race-grid{
    display:grid;
    grid-template-columns:repeat(4, 1fr);
    gap:14px;
    margin-top:18px;
}

.race-box{
    border:2px solid #333;
    background:white;
    border-radius:10px;
    padding:10px;
    box-sizing:border-box;
    position:relative;
}

.main-pick{
    background:#fff5f8;
    border:4px solid #ff4f93;
    box-shadow:0 0 18px rgba(255,79,147,0.35);
}

.race-header-title{
    background:#222;
    color:white;
    padding:6px 8px;
    border-radius:6px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.race-number{
    font-size:30px;
    font-weight:900;
    color:#ff4f93;
    line-height:1;
}

.main-pick .race-number{
    font-size:34px;
}

.grade-text{
    font-size:13px;
    font-weight:bold;
    color:white;
}

.rank-badge{
    margin-top:8px;
    padding:5px;
    border-radius:6px;
    font-size:12px;
    font-weight:bold;
    text-align:center;
}

.hot{
    background:#ffebee;
    color:#d50000;
}

.normal{
    background:#e8f5e9;
    color:#2e7d32;
}

.wave{
    background:#fff3e0;
    color:#ef6c00;
}

.danger{
    background:#eceff1;
    color:#455a64;
}

.prediction-matrix{
    display:flex;
    justify-content:space-around;
    margin-top:10px;
    border-bottom:1px dashed #ccc;
    padding-bottom:8px;
}

.predict-chara{
    text-align:center;
}

.chara-mark{
    font-size:24px;
    font-weight:900;
}

.race-info{
    margin-top:8px;
    background:#f5f5f5;
    border-radius:6px;
    padding:5px;
    font-size:11px;
    color:#444;
    text-align:center;
    font-weight:bold;
}

.memo-area{
    margin-top:8px;
    font-size:12px;
    line-height:1.5;
    color:#444;
    min-height:48px;
}

.ticket-main{
    margin-top:8px;
    background:#ffeef4;
    border:1px solid #ffb3cf;
    color:#cc1155;
    padding:7px;
    border-radius:6px;
    text-align:center;
    font-size:16px;
    font-weight:900;
}

.ticket-sub{
    margin-top:5px;
    background:#f8f8f8;
    border:1px solid #ddd;
    padding:5px;
    border-radius:6px;
    text-align:center;
    font-size:12px;
    color:#555;
}

.deadline{
    margin-top:7px;
    text-align:right;
    font-size:11px;
    color:#666;
    font-weight:bold;
}

.chara-role-area{
    display:flex;
    justify-content:space-between;
    margin-top:25px;
    gap:10px;
}

.role-card{
    flex:1;
    background:#fafafa;
    border:2px solid #ddd;
    border-radius:10px;
    padding:10px;
    text-align:center;
    font-weight:bold;
}

.role-desc{
    margin-top:5px;
    font-size:12px;
    color:#666;
}

</style>
"""

# =========================================
# HTML生成
# =========================================

races_html_content = ""

for r in range(1, 13):

    r_data = all_races_data[r]

    rank_class = "normal"

    if r_data["rank"] == "🔥鉄板":
        rank_class = "hot"

    elif r_data["rank"] == "💣波乱":
        rank_class = "wave"

    elif r_data["rank"] == "⚠荒れ注意":
        rank_class = "danger"

    main_class = ""

    # 12Rだけ強調
    if r == 12:
        main_class = "main-pick"

    races_html_content += f"""

    <div class="race-box {main_class}">

        <div class="race-header-title">

            <div class="race-number">
                {r}R
            </div>

            <div class="grade-text">
                {r_data['grade']}
            </div>

        </div>

        <div class="rank-badge {rank_class}">
            {r_data['rank']}
        </div>

        <div class="prediction-matrix">

            <div class="predict-chara">
                <div style="font-weight:bold; color:#ff4f93;">
                    一果
                </div>

                <div class="chara-mark" style="color:#ff4f93;">
                    {r_data['ichika']}
                </div>
            </div>

            <div class="predict-chara">
                <div style="font-weight:bold; color:#ce93d8;">
                    初音
                </div>

                <div class="chara-mark" style="color:#ce93d8;">
                    {r_data['hatsune']}
                </div>
            </div>

            <div class="predict-chara">
                <div style="font-weight:bold; color:#ff9800;">
                    キイナ
                </div>

                <div class="chara-mark" style="color:#ff9800;">
                    {r_data['kiina']}
                </div>
            </div>

        </div>

        <div class="race-info">
            波乱度：{r_data['haran']}
        </div>

        <div class="memo-area">
            <strong>【前日短評】</strong>
            {r_data['memo']}
        </div>

        <div class="ticket-main">
            🎯 本線：{r_data['main']}
        </div>

        <div class="ticket-sub">
            抑え：{r_data['sub']}
        </div>

        <div class="deadline">
            ⏰ 締切 {r_data['deadline']}
        </div>

    </div>

    """

# =========================================
# HTML全体（ヘッダー画像組み込み版）
# =========================================

grade_newspaper_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
{common_style}
{grade_style}
{download_logic}
</head>
<body>

<div class="paper-wrapper">

    <div style="
        border-bottom: 4px double #333;
        padding-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: stretch; /* 💡 高さをロゴ画像と揃える */
        position: relative;
    ">
        <div style="flex: 0 0 auto; width: 680px;">
            <img src="{logo_grade_src}" style="width: 100%; height: auto; display: block;" alt="三姫頂上決戦新聞">
        </div>

        <div style="
            flex: 1;
            text-align: right;
            display: flex;
            flex-direction: column;
            justify-content: space-between; /* 💡 上下に綺麗に振り分け */
            padding: 5px 15px 5px 0;
            font-family: 'Zen Maru Gothic', sans-serif;
        ">
            <div>
                <span style="
                    background: #ff4f93;
                    color: white;
                    padding: 4px 10px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: 900;
                ">
                    前日版・全12R完全攻略
                </span>
            </div>
            
            <div style="line-height: 1.1; margin: 8px 0;">
                <span style="font-size: 18px; font-weight: bold; color: #444;">開催場：</span>
                <span style="
                    font-size: 54px; /* 💡 開催場をさらに巨大化 */
                    color: #ff4f93;
                    font-weight: 900;
                    letter-spacing: 2px;
                ">
                    {grade_place}
                </span>
            </div>

            <div style="font-size: 20px; font-weight: 900; color: #222; letter-spacing: 0.5px;">
                {grade_title}
            </div>

            <div style="font-size: 15px; font-weight: bold; color: #555; margin-top: 2px;">
                📅 発行日：{grade_date}
            </div>

            <div style="margin-top: 6px;">
                <span style="
                    color: #d50000;
                    background: #ffebee;
                    padding: 4px 12px;
                    border-radius: 6px;
                    font-size: 15px;
                    font-weight: 900;
                    border: 2px solid #ffcdd2;
                    display: inline-block;
                    box-shadow: 2px 2px 0px rgba(213,0,0,0.1);
                ">
                    🏆 {grade_hit}
                </span>
            </div>
        </div>
    </div>

    <div class="race-grid">
        {races_html_content}
    </div>

    <div class="chara-role-area">
        <div class="role-card" style="border-top: 4px solid #ff4f93;">
            💖 一果
            <div class="role-desc">本命特化・イン戦重視</div>
        </div>
        <div class="role-card" style="border-top: 4px solid #ce93d8;">
            🎧 初音
            <div class="role-desc">女子戦リズム解析</div>
        </div>
        <div class="role-card" style="border-top: 4px solid #ff9800;">
            ⚡ キイナ
            <div class="role-desc">超抜穴狙い担当</div>
        </div>
    </div>

</div>

<div style="text-align:center; margin-top:20px; margin-bottom: 4px;">
    <button
        class="download-btn"
        style="
            background:#222;
            color:white;
            font-size:16px;
            padding:14px 32px;
            border:none;
            border-radius:50px;
            font-weight:bold;
            cursor:pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: 0.2s;
        "
        onclick="saveImage('.paper-wrapper', 'grade_race_12r.png')"
    >
        📸 12R特別専門紙を画像として保存
    </button>
</div>

</body>
</html>
"""
# =========================================
# 📱 SNS画像 HTML
# =========================================

sns_theme = {
    "危険": {
        "main": "#e60000",
        "sub": "#ffcc00",
        "title": "🚨 危険",
        "label": "イン逃げ成功率",
        "message": "波乱の可能性高い！",
        "bg": "#050505"
    },
    "鉄板": {
        "main": "#ffcc00",
        "sub": "#ffffff",
        "title": "🔥 鉄板！",
        "label": "イン逃げ信頼度",
        "message": f"軸選手は {sns_axis}！",
        "bg": "#080808"
    }
}

theme = sns_theme[sns_mode]

sns_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
{download_logic}
<style>
body {{
    margin: 0;
    padding: 20px;
    background: #111;
    font-family: Arial, sans-serif;
}}

.sns-wrapper {{
    width: 1080px;
    height: 1080px;
    margin: auto;
    background:
        radial-gradient(circle at 70% 45%, rgba(0,120,200,0.55), transparent 35%),
        linear-gradient(180deg, #000 0%, {theme["bg"]} 100%);
    color: white;
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
    padding: 55px;
    border: 8px solid {theme["main"]};
}}

.sns-title {{
    font-size: 120px;
    font-weight: 900;
    color: {theme["main"]};
    line-height: 1;
    text-shadow: 4px 4px 0 #000;
}}

.sns-race {{
    position: absolute;
    top: 60px;
    right: 55px;
    font-size: 54px;
    font-weight: 900;
    text-align: right;
}}

.sns-rate-label {{
    margin-top: 45px;
    font-size: 42px;
    font-weight: 900;
}}

.sns-rate {{
    font-size: 190px;
    font-weight: 900;
    color: {theme["main"]};
    line-height: 1;
    text-shadow: 5px 5px 0 #000;
}}

.mark-area {{
    position: absolute;
    left: 55px;
    right: 55px;
    top: 480px;
    height: 330px;
    background: linear-gradient(135deg, #006d9c, #00364d);
    border: 4px solid white;
    border-radius: 24px;
    overflow: hidden;
}}

.turn-mark {{
    position: absolute;
    right: 260px;
    top: 125px;
    width: 70px;
    height: 70px;
    background: repeating-conic-gradient(red 0deg 30deg, white 30deg 60deg);
    border-radius: 50%;
    border: 4px solid white;
}}

.boat {{
    position: absolute;
    width: 86px;
    height: 48px;
    border-radius: 50% 50% 45% 45%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 38px;
    font-weight: 900;
    border: 4px solid white;
    box-shadow: 0 0 12px rgba(0,0,0,0.7);
}}

.boat1 {{ background: white; color: black; left: 270px; top: 70px; }}
.boat2 {{ background: #111; color: white; left: 360px; top: 145px; }}
.boat3 {{ background: #e60000; color: white; left: 300px; top: 225px; }}

.arrow {{
    position: absolute;
    height: 12px;
    border-radius: 20px;
    transform-origin: left center;
}}

.arrow1 {{
    background: white;
    width: 330px;
    left: 350px;
    top: 92px;
    transform: rotate(8deg);
    opacity: 0.9;
}}

.arrow2 {{
    background: black;
    width: 340px;
    left: 440px;
    top: 168px;
    transform: rotate(-18deg);
}}

.arrow3 {{
    background: red;
    width: 330px;
    left: 380px;
    top: 245px;
    transform: rotate(-28deg);
}}

.arrow::after {{
    content: "";
    position: absolute;
    right: -18px;
    top: -10px;
    border-left: 25px solid currentColor;
    border-top: 16px solid transparent;
    border-bottom: 16px solid transparent;
}}

.arrow1 {{ color: white; }}
.arrow2 {{ color: black; }}
.arrow3 {{ color: red; }}

.steps {{
    position: absolute;
    left: 55px;
    top: 830px;
    font-size: 34px;
    font-weight: 900;
    line-height: 1.6;
}}

.result {{
    position: absolute;
    right: 55px;
    bottom: 55px;
    background: white;
    color: black;
    padding: 20px 35px;
    border-radius: 18px;
    font-size: 86px;
    font-weight: 900;
}}

.message {{
    position: absolute;
    left: 55px;
    bottom: 55px;
    font-size: 44px;
    font-weight: 900;
    color: {theme["sub"]};
}}
</style>
</head>

<body>
<div class="sns-wrapper">

    <div class="sns-title">{theme["title"]}</div>

    <div class="sns-race">
        {sns_place} {sns_race_no}<br>
        <span style="font-size:30px;">締切 {sns_deadline}</span>
    </div>

    <div class="sns-rate-label">{theme["label"]}</div>
    <div class="sns-rate">{sns_rate}%</div>

    <div class="mark-area">
    <svg viewBox="0 0 900 320" style="width:100%; height:100%;">

        <!-- 水面 -->
        <rect x="0" y="0" width="900" height="320" fill="#00627f"/>

        <!-- ターンマーク -->
        <circle cx="650" cy="155" r="28" fill="white" stroke="white" stroke-width="4"/>
        <path d="M650 127 L678 155 L650 183 L622 155 Z" fill="#e60000"/>

        <!-- 1号艇：流される -->
        <path d="M290 110 C420 105, 560 125, 750 70"
              stroke="white" stroke-width="14" fill="none"
              stroke-linecap="round" opacity="0.9"/>
        <polygon points="750,70 720,58 727,88" fill="white"/>

        <!-- 2号艇：絞る -->
        <path d="M310 165 C430 155, 520 140, 610 125"
              stroke="#111" stroke-width="14" fill="none"
              stroke-linecap="round"/>
        <polygon points="610,125 580,112 586,142" fill="#111"/>

        <!-- 3号艇：差し -->
        <path d="M280 235 C410 210, 500 175, 610 160"
              stroke="#e60000" stroke-width="16" fill="none"
              stroke-linecap="round"/>
        <polygon points="610,160 580,145 585,177" fill="#e60000"/>

        <!-- 艇 -->
        <ellipse cx="250" cy="110" rx="55" ry="28" fill="white" stroke="white" stroke-width="4"/>
        <text x="250" y="124" text-anchor="middle" font-size="42" font-weight="900" fill="black">1</text>

        <ellipse cx="260" cy="165" rx="55" ry="28" fill="#111" stroke="white" stroke-width="4"/>
        <text x="260" y="179" text-anchor="middle" font-size="42" font-weight="900" fill="white">2</text>

        <ellipse cx="240" cy="235" rx="55" ry="28" fill="#e60000" stroke="white" stroke-width="4"/>
        <text x="240" y="249" text-anchor="middle" font-size="42" font-weight="900" fill="white">3</text>

    </svg>

    </div>

    <div class="steps">
        ① {sns_step1}<br>
        ② {sns_step2}<br>
        ③ {sns_step3}
    </div>

    <div class="message">{theme["message"]}</div>
    <div class="result">{sns_main}</div>

</div>

<div style="text-align:center; margin-top:25px;">
    <button
        onclick="saveImage('.sns-wrapper', 'sns_boatstrike.png')"
        style="
            background:{theme["main"]};
            color:white;
            font-size:24px;
            font-weight:bold;
            padding:18px 42px;
            border:none;
            border-radius:50px;
            cursor:pointer;
        "
    >
        📸 SNS画像を保存
    </button>
</div>

</body>
</html>
"""



# =========================================
# 6. メインタブ表示（タブ4つに拡張）
# =========================================

main_tab1,main_tab2,main_tab3,main_tab4,main_tab5,main_tab6 = st.tabs([
    "🌸 一果",
    "⚡ キイナ",
    "👗 初音",
    "🏆 グレード",
    "📱 SNS画像",
    "✨ ステッカー"
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
        html(hatsune_zenjitsu_final_html, height=1500, scrolling=True)
    with sub_tab6:
        html(hatsune_live_final_html, height=1200, scrolling=True)

# --- 🏆 新規追加：グレード特別紙タブ ---
with main_tab4:
    st.markdown("### 🏆 3人合同・グレードレース12R一挙掲載特別専門紙")
    html(grade_newspaper_html, height=2000, scrolling=True)

with main_tab5:
    st.markdown("### 📱 SNS用 1マーク画像")

    img = create_sns_mark_image(
        mode=sns_mode,
        place=sns_place,
        race_no=sns_race_no,
        deadline=sns_deadline,
        rate=sns_rate,
        main=sns_main,
        step1=sns_step1,
        step2=sns_step2,
        step3=sns_step3
    )

    st.image(img, use_container_width=True)

    buf = BytesIO()
    img.save(buf, format="PNG")
    st.download_button(
        label="📸 SNS画像をダウンロード",
        data=buf.getvalue(),
        file_name="sns_boatstrike.png",
        mime="image/png"
    )

with main_tab6:
    st.markdown("### ✨ 速報ステッカー生成")

    img = create_frame_sticker(
        frame_type=frame_type,
        place=sticker_place,
        race=sticker_race,
        main_text=main_text,
        sub_text=sub_text,
        kaime_text=kaime_text,
        memo_text=memo_text
    )

    st.image(img, use_container_width=True)

    buf = BytesIO()
    img.save(buf, format="PNG")

    st.download_button(
        "📸 ステッカーをダウンロード",
        data=buf.getvalue(),
        file_name=f"boatstrike_{frame_type}.png",
        mime="image/png"
    )
