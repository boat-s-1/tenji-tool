from pathlib import Path
import runpy
import uuid

import streamlit as st
import character_picker_bootstrap  # noqa: F401

# ui_shell.py uses keyed containers to keep inactive input groups mounted while
# hiding them with CSS. Streamlit rejects a duplicated user key within one run,
# so make only those internal bs_hidden_* container keys globally unique.
_original_container = st.container


def _safe_container(*args, **kwargs):
    key = kwargs.get("key")
    if isinstance(key, str) and key.startswith("bs_hidden_"):
        kwargs["key"] = f"{key}_{uuid.uuid4().hex}"
    return _original_container(*args, **kwargs)


st.container = _safe_container

runpy.run_path(str(Path(__file__).with_name("ui_shell.py")), run_name="__main__")
