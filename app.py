from pathlib import Path
import runpy

import character_picker_bootstrap  # noqa: F401

runpy.run_path(str(Path(__file__).with_name("ui_shell.py")), run_name="__main__")
