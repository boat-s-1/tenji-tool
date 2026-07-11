import streamlit as st
from datetime import date
from streamlit.components.v1 import html


st.set_page_config(
    page_title="BOAT STRIKE 新聞作成",
    page_icon="🚤",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
    .stApp {
        background:#f6f6f8;
    }

    .block-container {
        max-width:680px;
        padding-top:12px;
        padding-left:12px;
        padding-right:12px;
        padding-bottom:100px;
    }

    [data-testid="stSidebar"] {
        display:none;
    }

    .stTextInput input,
    .stTextArea textarea,
    div[data-baseweb="select"] > div {
        min-height:48px;
        font-size:16px !important;
        border-radius:12px;
    }

    .stButton > button {
        width:100%;
        min-height:52px;
        border-radius:14px;
        font-size:17px;
        font-weight:900;
    }

    details {
        background:white;
        border:1px solid #e6e6ea;
        border-radius:14px;
        padding:3px 8px;
        margin-bottom:10px;
    }

    @media (max-width:600px) {
        .block-container {
            padding-left:10px;
            padding-right:10px;
        }

        h1 {
            font-size:25px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


DEFAULTS = {
    "generated": False,
    "race_place": "丸亀",
    "race_no": "1R",
    "race_date": date.today(),
    "character": "一果",
    "edition": "前日版",
    "honmei": "1号艇",
    "nige_rate": 84,
    "up_rate": 11,
    "danger_boat": "なし",
    "selected_boats": ["1号艇", "2号艇", "3号艇"],
    "wave": 28,
    "comment": "1号艇中心だが、2号艇の差しに注意！",
    "motor_eval": "1号艇は出足型。3号艇の伸びにも注目。",
}


for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


if "boat_comments" not in st.session_state:
    st.session_state.boat_comments = {
        f"{i}号艇": f"{i}号艇の展開解説"
        for i in range(1, 7)
    }


if "boat_scores" not in st.session_state:
    st.session_state.boat_scores = {
        f"{i}号艇": 50
        for i in range(1, 7)
    }


st.title("🚤 BOAT STRIKE")
st.caption("スマホ新聞作成ツール")


st.markdown(
    """
    <div style="
        background:linear-gradient(135deg,#111,#333);
        color:white;
        border-radius:18px;
        padding:18px;
        margin-bottom:18px;
    ">
        <div style="
            color:#ffcc00;
            font-size:12px;
            font-weight:900;
        ">
            BOAT STRIKE ADMIN
        </div>

        <div style="
            font-size:23px;
            font-weight:900;
            margin-top:5px;
        ">
            新聞をかんたん作成
        </div>

        <div style="
            color:#ddd;
            font-size:14px;
            margin-top:5px;
        ">
            必要な情報だけ入力して画像を生成します。
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


tab_create, tab_history = st.tabs(
    ["📝 新規作成", "📂 作成履歴"]
)


with tab_create:
    st.subheader("① 新聞タイプ")

    character_label = st.radio(
        "キャラクター",
        ["🌸 一果", "⚡ キイナ", "👗 初音"],
        horizontal=True,
    )

    st.session_state.character = {
        "🌸 一果": "一果",
        "⚡ キイナ": "キイナ",
        "👗 初音": "初音",
    }[character_label]

    st.session_state.edition = st.radio(
        "種類",
        ["前日版", "直前版", "SNS速報"],
        horizontal=True,
    )

    st.divider()
    st.subheader("② レース情報")

    places = [
        "桐生", "戸田", "江戸川", "平和島",
        "多摩川", "浜名湖", "蒲郡", "常滑",
        "津", "三国", "びわこ", "住之江",
        "尼崎", "鳴門", "丸亀", "児島",
        "宮島", "徳山", "下関", "若松",
        "芦屋", "福岡", "唐津", "大村",
    ]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.session_state.race_place = st.selectbox(
            "レース場",
            places,
            index=places.index(
                st.session_state.race_place
            ),
        )

    with col2:
        races = [f"{i}R" for i in range(1, 13)]

        st.session_state.race_no = st.selectbox(
            "レース",
            races,
            index=races.index(
                st.session_state.race_no
            ),
        )

    st.session_state.race_date = st.date_input(
        "開催日",
        value=st.session_state.race_date,
    )

    st.divider()
    st.subheader("③ 予想入力")

    boats = [f"{i}号艇" for i in range(1, 7)]

    st.session_state.honmei = st.radio(
        "本命",
        boats,
        index=boats.index(
            st.session_state.honmei
        ),
        horizontal=True,
    )

    st.session_state.nige_rate = st.slider(
        "期待度",
        0,
        100,
        st.session_state.nige_rate,
        format="%d%%",
    )

    st.session_state.danger_boat = st.selectbox(
        "危険艇",
        ["なし"] + boats,
    )

    st.session_state.selected_boats = st.multiselect(
        "注目艇",
        boats,
        default=st.session_state.selected_boats,
        max_selections=4,
    )

    st.session_state.wave = st.slider(
        "波乱指数",
        0,
        100,
        st.session_state.wave,
    )

    st.session_state.comment = st.text_area(
        "ひとこと",
        value=st.session_state.comment,
        height=100,
    )

    with st.expander("詳細設定"):
        for boat in st.session_state.selected_boats:
            st.markdown(f"**{boat}**")

            st.session_state.boat_scores[boat] = st.slider(
                f"{boat} 評価",
                0,
                100,
                st.session_state.boat_scores[boat],
                key=f"score_{boat}",
            )

            st.session_state.boat_comments[boat] = st.text_area(
                f"{boat} コメント",
                value=st.session_state.boat_comments[boat],
                key=f"comment_{boat}",
                height=80,
            )

        st.session_state.motor_eval = st.text_area(
            "機力チェック",
            value=st.session_state.motor_eval,
            height=100,
        )

    st.divider()

    if st.button(
        "新聞を作成する",
        type="primary",
        use_container_width=True,
    ):
        if not st.session_state.selected_boats:
            st.error("注目艇を選択してください。")
        else:
            st.session_state.generated = True

    if st.session_state.generated:
        st.success("入力が完了しました。")

        st.markdown(
            f"""
            ### 作成内容

            **新聞：**  
            {st.session_state.character}
            ・{st.session_state.edition}

            **レース：**  
            {st.session_state.race_place}
            {st.session_state.race_no}

            **本命：**  
            {st.session_state.honmei}

            **期待度：**  
            {st.session_state.nige_rate}%
            """
        )

        # ここに現在のhtml_codeを表示します
        #
        # html(
        #     html_code,
        #     height=1500,
        #     scrolling=True,
        # )


with tab_history:
    st.info(
        "今後、作成した新聞を保存して一覧表示できます。"
    )
