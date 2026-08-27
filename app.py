"""BoatStrikers Streamlit UI shell.

The original newspaper generator is kept intact in legacy_app.py.
This shell improves only the editor UI: wide live preview, clear input groups,
category switching, and sensible expander defaults. Newspaper generation logic
stays untouched.
"""

from pathlib import Path
import runpy
import streamlit as st

_original_set_page_config = st.set_page_config
_original_tabs = st.tabs
_original_markdown = st.markdown
_original_expander = st.expander
_original_header = st.header
_original_container = st.container

# Input widgets used by the legacy editor.  We wrap them only so inactive
# categories can stay mounted (values preserved) while being visually hidden.
_WIDGET_NAMES = [
    "text_input", "text_area", "selectbox", "select_slider", "slider",
    "multiselect", "checkbox", "color_picker", "file_uploader", "number_input",
]
_original_widgets = {name: getattr(st, name) for name in _WIDGET_NAMES}

_inserted_groups = set()
_current_group = "common"
_input_phase = False
_hidden_counter = 0

MODE_LABELS = ["🌸 一果", "⚡ キイナ", "👗 初音", "📱 SNS", "🏆 12R"]
MODE_TO_GROUP = {
    "🌸 一果": "ichika",
    "⚡ キイナ": "kiina",
    "👗 初音": "hatsune",
    "📱 SNS": "sns",
    "🏆 12R": "grade",
}


def _wide_set_page_config(*args, **kwargs):
    kwargs["layout"] = "wide"
    return _original_set_page_config(*args, **kwargs)


def _selected_group():
    return MODE_TO_GROUP.get(st.session_state.get("bs_input_mode", MODE_LABELS[0]), "ichika")


def _group_is_visible(group=None):
    group = group or _current_group
    if group == "common":
        return True
    # Sticker inputs are treated as SNS support tools so the switch stays simple.
    if group == "sticker":
        return _selected_group() == "sns"
    return group == _selected_group()


def _hidden_container():
    global _hidden_counter
    _hidden_counter += 1
    return _original_container(key=f"bs_hidden_{_hidden_counter}")


def _editor_tabs_as_columns(labels, *args, **kwargs):
    global _input_phase
    try:
        normalized = [str(x) for x in labels]
    except Exception:
        return _original_tabs(labels, *args, **kwargs)

    if normalized == ["📝 入力・設定", "🖼️ プレビュー・保存"]:
        _input_phase = True
        cols = st.columns([0.92, 1.08], gap="large")
        with cols[0]:
            _original_markdown(
                """
                <div style="font-size:12px;font-weight:900;color:#64748b;margin:2px 0 6px;">
                    入力する内容を選択
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Radio is intentionally used instead of a newer component so this
            # stays compatible with the Streamlit version already deployed.
            st.radio(
                "入力カテゴリ",
                MODE_LABELS,
                horizontal=True,
                key="bs_input_mode",
                label_visibility="collapsed",
            )
            _original_markdown(
                "<div class='bs-mode-note'>共通設定はどのカテゴリでも表示されます。入力値は切替後も保持されます。</div>",
                unsafe_allow_html=True,
            )
        return cols

    # The first tab set created inside preview_tab marks the end of the input UI.
    if normalized == ["🌸 一果", "⚡ キイナ", "👗 初音", "🏆 グレード", "📱 SNS画像", "✨ ステッカー"]:
        _input_phase = False
    return _original_tabs(labels, *args, **kwargs)


def _section_card(title, subtitle="", tone="blue"):
    if _input_phase and not _group_is_visible():
        return
    palette = {
        "blue": ("#2563eb", "#eff6ff"),
        "pink": ("#ec4899", "#fff1f6"),
        "yellow": ("#c68a00", "#fff9df"),
        "purple": ("#8b5cf6", "#f5f1ff"),
        "green": ("#0f9f74", "#ecfdf5"),
        "slate": ("#475569", "#f8fafc"),
    }
    accent, bg = palette.get(tone, palette["blue"])
    _original_markdown(
        f"""
        <div class="bs-input-section" style="border-left-color:{accent};background:{bg};">
          <div class="bs-input-title" style="color:{accent};">{title}</div>
          {f'<div class="bs-input-sub">{subtitle}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _ensure_group(key):
    global _current_group
    _current_group = key
    marker = (key, _selected_group())
    if marker in _inserted_groups:
        return
    _inserted_groups.add(marker)
    if not _group_is_visible(key):
        return
    if key == "common":
        _section_card("⚙️ 共通設定", "まずレース情報と使用画像を設定", "blue")
    elif key == "ichika":
        _section_card("🌸 一果", "前日予想・展開評価・直前判断", "pink")
    elif key == "kiina":
        _section_card("⚡ キイナ", "5アタマ・スリット・直前LIVE", "yellow")
    elif key == "hatsune":
        _section_card("👗 初音", "女子戦設定・ピックアップ", "purple")
    elif key == "sticker":
        _section_card("✨ 速報ステッカー", "SNS投稿用の速報画像", "green")
    elif key == "sns":
        _section_card("📱 SNS画像", "1マーク展開・SNS投稿画像", "blue")
    elif key == "grade":
        _section_card("🏆 グレード12R", "全12R特別専門紙", "slate")


def _group_for_expander(text):
    if text in {"📌 レース基本情報", "📌 画像"}:
        return "common"
    if text in {"📌 一果本命候補", "📌 一果展開評価", "📌 一果直前"}:
        return "ichika"
    if text in {
        "⚡ キイナの穴党設定", "⚡ キイナのスリット予想", "🎨 スリットのデザイン設定",
        "⚡ 直前チェック項目", "⚡ 直前LIVE設定", "⚡ キイナのLIVEスタンプ設定",
    }:
        return "kiina"
    if text in {"👗 初音の女子戦設定", "👗 初音の女子戦・ピックアップ設定"}:
        return "hatsune"
    if text == "✨ 速報ステッカー":
        return "sticker"
    if text in {"🚨 SNS画像 基本情報", "🚤 1マーク展開"}:
        return "sns"
    if text == "📰 12R新聞 共通情報" or text.startswith("🏁 "):
        return "grade"
    return None


def _organized_expander(label, *args, **kwargs):
    text = str(label)
    group = _group_for_expander(text)
    if group:
        _ensure_group(group)

    default_open = {
        "📌 レース基本情報",
        "📌 一果本命候補",
        "⚡ キイナの穴党設定",
        "👗 初音の女子戦設定",
        "🚨 SNS画像 基本情報",
        "📰 12R新聞 共通情報",
    }
    if "expanded" not in kwargs:
        kwargs["expanded"] = text in default_open

    if _input_phase and group and not _group_is_visible(group):
        holder = _hidden_container()
        with holder:
            exp = _original_expander(label, *args, **kwargs)
        return exp

    return _original_expander(label, *args, **kwargs)


def _organized_header(body, *args, **kwargs):
    global _current_group
    text = str(body)
    if text == "一果":
        _current_group = "ichika"
        return None
    if text == "直前情報":
        _current_group = "ichika"
        if _group_is_visible("ichika"):
            _section_card("⚡ 直前情報", "展示後に使う一果の直前項目", "slate")
        return None
    if text == "📱 SNS画像ツール設定":
        _ensure_group("sns")
        return None
    if text == "🏆 グレードレース12R設定":
        _ensure_group("grade")
        return None
    return _original_header(body, *args, **kwargs)


def _wrap_widget(name):
    original = _original_widgets[name]

    def wrapped(*args, **kwargs):
        if _input_phase and not _group_is_visible():
            holder = _hidden_container()
            with holder:
                return original(*args, **kwargs)
        return original(*args, **kwargs)

    return wrapped


def _wider_admin_css(body, *args, **kwargs):
    # During input rendering, ordinary markdown belonging to an inactive group
    # is hidden as well (e.g. Hatsune player labels). Global CSS remains visible.
    if _input_phase and isinstance(body, str) and ".block-container" not in body and not _group_is_visible():
        holder = _hidden_container()
        with holder:
            return _original_markdown(body, *args, **kwargs)

    if isinstance(body, str) and ".block-container" in body:
        body = body.replace("max-width: 760px;", "max-width: 1680px;")
        body = body.replace(
            "「入力・設定」で編集し、「プレビュー・保存」で画像を確認します。",
            "左で入力しながら、右のプレビューをリアルタイム確認できます。",
        )
        body = body.replace(
            "</style>",
            """

    /* BoatStrikers input editor polish */
    .bs-mode-note {
        margin: 6px 0 12px;
        padding: 8px 10px;
        border-radius: 10px;
        background: #f8fafc;
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
    }
    div[data-testid=\"stRadio\"] > div {
        gap: 6px !important;
    }
    div[data-testid=\"stRadio\"] label {
        background: #ffffff;
        border: 1px solid #dbe3ee;
        border-radius: 999px;
        padding: 5px 10px !important;
        min-height: 38px !important;
        box-shadow: 0 1px 3px rgba(15,23,42,.04);
    }
    div[data-testid=\"stRadio\"] label:has(input:checked) {
        border-color: #2563eb;
        background: #eff6ff;
        box-shadow: 0 0 0 2px rgba(37,99,235,.08);
    }

    [class*="st-key-bs_hidden_"] {
        display: none !important;
    }

    .bs-input-section {
        border-left: 6px solid #2563eb;
        border-radius: 14px;
        padding: 12px 14px;
        margin: 18px 0 10px;
        box-shadow: 0 2px 10px rgba(15,23,42,.05);
    }
    .bs-input-title {
        font-size: 20px;
        font-weight: 900;
        line-height: 1.25;
    }
    .bs-input-sub {
        margin-top: 3px;
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
    }

    details[data-testid=\"stExpander\"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        background: #ffffff !important;
        box-shadow: 0 1px 5px rgba(15,23,42,.035) !important;
        overflow: hidden;
        margin-bottom: 9px !important;
    }
    details[data-testid=\"stExpander\"] summary {
        min-height: 48px;
        font-weight: 900 !important;
        color: #253247 !important;
    }
    details[data-testid=\"stExpander\"][open] {
        border-color: #cbd5e1 !important;
        box-shadow: 0 4px 12px rgba(15,23,42,.055) !important;
    }

    [data-testid=\"stTextInput\"],
    [data-testid=\"stTextArea\"],
    [data-testid=\"stSelectbox\"],
    [data-testid=\"stSlider\"],
    [data-testid=\"stFileUploader\"],
    [data-testid=\"stNumberInput\"] {
        margin-bottom: .35rem;
    }
    [data-testid=\"stWidgetLabel\"] p {
        font-weight: 800 !important;
        color: #334155 !important;
    }

    @media (min-width: 900px) {
        .block-container {
            max-width: 1680px !important;
        }
        [data-testid=\"stHorizontalBlock\"] > [data-testid=\"column\"]:nth-child(1) {
            padding-right: .35rem;
        }
        [data-testid=\"stHorizontalBlock\"] > [data-testid=\"column\"]:nth-child(2) {
            align-self: flex-start;
        }
    }

    @media (max-width: 899px) {
        .block-container {
            max-width: 760px !important;
        }
        .bs-input-title { font-size: 18px; }
        div[data-testid=\"stRadio\"] > div { flex-wrap: wrap !important; }
    }
    </style>""",
            1,
        )
    return _original_markdown(body, *args, **kwargs)


st.set_page_config = _wide_set_page_config
st.tabs = _editor_tabs_as_columns
st.markdown = _wider_admin_css
st.expander = _organized_expander
st.header = _organized_header
for _name in _WIDGET_NAMES:
    setattr(st, _name, _wrap_widget(_name))

runpy.run_path(str(Path(__file__).with_name("legacy_app.py")), run_name="__main__")
