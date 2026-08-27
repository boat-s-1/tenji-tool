"""BoatStrikers Streamlit UI patch.

This file is imported automatically by Python at startup when the repository
root is on sys.path (the normal Streamlit Cloud execution model).  It changes
only the editor layout; the newspaper generation code in app.py is left
untouched.
"""

try:
    import streamlit as st
except Exception:
    st = None


if st is not None:
    _original_set_page_config = st.set_page_config
    _original_tabs = st.tabs
    _original_markdown = st.markdown

    def _wide_set_page_config(*args, **kwargs):
        # Keep every existing app.py option, but give the editor enough room
        # for input + live preview side by side on desktop.
        kwargs["layout"] = "wide"
        return _original_set_page_config(*args, **kwargs)

    def _live_preview_tabs(labels, *args, **kwargs):
        """Replace only the main Input/Preview tabs with two columns.

        Any other st.tabs() call in the application keeps normal Streamlit
        tab behavior, so existing features remain unchanged.
        """
        try:
            normalized = [str(x) for x in labels]
        except Exception:
            return _original_tabs(labels, *args, **kwargs)

        if normalized == ["📝 入力・設定", "🖼️ プレビュー・保存"]:
            return st.columns([1.03, 0.97], gap="large")
        return _original_tabs(labels, *args, **kwargs)

    def _responsive_markdown(body, *args, **kwargs):
        # app.py currently limits the entire screen to 760px.  Increase only
        # that existing rule; newspaper HTML/CSS itself is not modified.
        if isinstance(body, str) and ".block-container" in body:
            body = body.replace("max-width: 760px;", "max-width: 1540px;")
            body = body.replace(
                "「入力・設定」で編集し、「プレビュー・保存」で画像を確認します。",
                "左側で入力し、右側のプレビューを確認しながら編集できます。",
            )
            body = body.replace(
                "@media (max-width: 600px) {",
                """
    @media (min-width: 1050px) {
        .block-container {
            max-width: 1540px !important;
        }
    }

    @media (max-width: 1049px) {
        .block-container {
            max-width: 760px !important;
        }
    }

    @media (max-width: 600px) {""",
            )
        return _original_markdown(body, *args, **kwargs)

    st.set_page_config = _wide_set_page_config
    st.tabs = _live_preview_tabs
    st.markdown = _responsive_markdown
