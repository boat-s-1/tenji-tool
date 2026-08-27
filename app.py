from pathlib import Path
import runpy
import uuid

import streamlit as st
import character_picker_bootstrap  # noqa: F401

# ui_shell.py uses keyed containers to keep inactive input groups mounted while
# hiding them with CSS. Streamlit rejects a duplicated user key within one run,
# so make only those internal bs_hidden_* container keys globally unique.
_original_container = st.container
_original_columns = st.columns


def _safe_container(*args, **kwargs):
    key = kwargs.get("key")
    if isinstance(key, str) and key.startswith("bs_hidden_"):
        kwargs["key"] = f"{key}_{uuid.uuid4().hex}"
    return _original_container(*args, **kwargs)


def _preview_wide_columns(spec, *args, **kwargs):
    # Keep all existing column layouts unchanged except the main editor split.
    if isinstance(spec, (list, tuple)) and len(spec) == 2:
        try:
            if abs(float(spec[0]) - 0.92) < 1e-9 and abs(float(spec[1]) - 1.08) < 1e-9:
                spec = [3, 7]
        except (TypeError, ValueError):
            pass
    return _original_columns(spec, *args, **kwargs)


st.container = _safe_container
st.columns = _preview_wide_columns

runpy.run_path(str(Path(__file__).with_name("ui_shell.py")), run_name="__main__")
