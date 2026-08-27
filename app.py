"""BoatStrikers Streamlit UI shell.

The original newspaper generator is kept intact in legacy_app.py.
This shell only changes the editor layout so input and preview are visible
side by side on desktop, then executes the original application.
"""

from pathlib import Path
import runpy
import streamlit as st

_original_set_page_config = st.set_page_config
_original_tabs = st.tabs
_original_markdown = st.markdown


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


def _wider_admin_css(body, *args, **kwargs):
    if isinstance(body, str) and ".block-container" in body:
        body = body.replace("max-width: 760px;", "max-width: 1680px;")
        body = body.replace(
            "「入力・設定」で編集し、「プレビュー・保存」で画像を確認します。",
            "左で入力しながら、右のプレビューをリアルタイム確認できます。",
        )
        body = body.replace(
            "@media (max-width: 600px) {",
            """
    @media (min-width: 900px) {
        .block-container {
            max-width: 1680px !important;
        }
        [data-testid=\"stHorizontalBlock\"] > [data-testid=\"column\"]:nth-child(2) {
            align-self: flex-start;
        }
    }

    @media (max-width: 899px) {
        .block-container {
            max-width: 760px !important;
        }
    }

    @media (max-width: 600px) {""",
        )
    return _original_markdown(body, *args, **kwargs)


st.set_page_config = _wide_set_page_config
st.tabs = _editor_tabs_as_columns
st.markdown = _wider_admin_css

runpy.run_path(str(Path(__file__).with_name("legacy_app.py")), run_name="__main__")
