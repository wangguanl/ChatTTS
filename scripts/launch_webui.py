import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "examples" / "web"))
sys.path.insert(0, str(root))

import gradio as gr

_orig = gr.Blocks.launch


def _launch(self, *args, **kwargs):
    kwargs["inbrowser"] = False
    kwargs.setdefault("server_name", "0.0.0.0")
    return _orig(self, *args, **kwargs)


gr.Blocks.launch = _launch

port = sys.argv[1] if len(sys.argv) > 1 else "8080"
sys.argv = [
    "webui.py",
    "--server_name",
    "0.0.0.0",
    "--server_port",
    port,
    "--custom_path",
    str(root / "models" / "ChatTTS"),
]
import webui

webui.main()