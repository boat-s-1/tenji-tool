"""BoatStrikers Streamlit UI shell.

The original newspaper generator is kept intact in legacy_app.py.
This shell improves only the editor UI: wide live preview, clear input groups,
and sensible expander defaults. Newspaper generation logic stays untouched.
"""

from pathlib import Path
import runpy
import streamlit as st

_original_set_page_config = st.set_page_config
_original_tabs = st.tabs
_original_markdown = st.markdown
_original_expander = st.expander
_original_header = st.header

_inserted_groups = set()


def _wide_set_page_config(*args, **kwargs):
    kwargs["layout"] = "wide"
    return _original_set_page_config(*args, **kwargs)


def _editor_tabs_as_columns(labels, *args, **kwargs):
    try:
        normalized = [str(x) for x in labels]
    except Exception:
        return _original_tabs(labels, *args, **kwargs)

    if normalized == ["📝 入力・設定", "🖼️ プレビュー・保存"]:
        return st.columns([0.92, 1.08], gap="large")
    return _original_tabs(labels, *args, **kwargs)


def _section_card(title, subtitle="", tone="blue"):
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
    if key in _inserted_groups:
        return
    _inserted_groups.add(key)
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


def _organized_expander(label, *args, **kwargs):
    text = str(label)

    if text == "📌 レース基本情報":
        _ensure_group("common")
    elif text == "📌 一果本命候補":
        _ensure_group("ichika")
    elif text == "⚡ キイナの穴党設定":
        _ensure_group("kiina")
    elif text == "👗 初音の女子戦設定":
        _ensure_group("hatsune")
    elif text == "✨ 速報ステッカー":
        _ensure_group("sticker")

    # Frequently used inputs are open by default; detailed settings stay compact.
    default_open = {
        "📌 レース基本情報",
        "📌 一果本命候補",
        "⚡ キイナの穴党設定",
        "👗 初音の女子戦設定",
    }
    if "expanded" not in kwargs:
        kwargs["expanded"] = text in default_open

    return _original_expander(label, *args, **kwargs)


def _organized_header(body, *args, **kwargs):
    text = str(body)
    # Legacy headings that only acted as separators are replaced with compact cards.
    if text == "一果":
        return None
    if text == "直前情報":
        _section_card("⚡ 直前情報", "展示後に使う共通項目", "slate")
        return None
    if text == "📱 SNS画像ツール設定":
        _section_card("📱 SNS画像", "1マーク展開・SNS投稿画像", "blue")
        return None
    if text == "🏆 グレードレース12R設定":
        _section_card("🏆 グレード12R", "全12R特別専門紙", "slate")
        return None
    return _original_header(body, *args, **kwargs)


def _wider_admin_css(body, *args, **kwargs):
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

runpy.run_path(str(Path(__file__).with_name("legacy_app.py")), run_name="__main__")
