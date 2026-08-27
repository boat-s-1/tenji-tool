from pathlib import Path
import streamlit as st

_original_file_uploader = st.file_uploader
_original_selectbox = st.selectbox

GROUP_TO_FOLDER = {
    "ichika": "ichika",
    "hatsune": "hatsune",
    "kiina": "kiina",
}
GROUP_LABEL = {
    "ichika": "一果",
    "hatsune": "初音",
    "kiina": "キイナ",
}
VALID_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


class PresetUpload:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"

    def read(self):
        return self.path.read_bytes()

    def getvalue(self):
        return self.path.read_bytes()

    def __bool__(self):
        return True


def _selected_character_group():
    mode = st.session_state.get("bs_input_mode", "🌸 一果")
    if "キイナ" in mode:
        return "kiina"
    if "初音" in mode:
        return "hatsune"
    if "一果" in mode:
        return "ichika"

    family = _original_selectbox(
        "キャラ画像カテゴリ",
        ["一果", "初音", "キイナ"],
        key="bs_character_family_misc",
    )
    return {"一果": "ichika", "初音": "hatsune", "キイナ": "kiina"}[family]


def _character_picker():
    group = _selected_character_group()
    folder = Path(__file__).resolve().parent / "public" / GROUP_TO_FOLDER[group]
    files = []
    if folder.exists():
        files = sorted(
            [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXTS],
            key=lambda p: p.name.lower(),
        )

    options = [p.name for p in files] + ["📤 手動アップロード"]
    if not files:
        options = ["📤 手動アップロード"]

    choice = _original_selectbox(
        f"右上500×900画像（{GROUP_LABEL[group]}）",
        options,
        key=f"bs_character_preset_{group}",
    )

    if choice == "📤 手動アップロード":
        return _original_file_uploader(
            "キャラ画像をアップロード",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"bs_character_upload_{group}",
        )

    selected = folder / choice
    if selected.exists():
        st.image(str(selected), width=140, caption=choice)
        return PresetUpload(selected)

    return None


def patched_file_uploader(label, *args, **kwargs):
    if str(label) == "キャラ画像":
        return _character_picker()
    return _original_file_uploader(label, *args, **kwargs)


st.file_uploader = patched_file_uploader
