# 运行命令

- 项目：ChatTTS
- 生成时间：2026-09-08
- 运行方式：直接运行（Gradio WebUI）
- 硬件评估：**满足** — 官方 FAQ：30 秒音频至少 4GB 显存；本机 RTX 4080 16GB，启动前约 1353MiB/16376MiB 占用、剩余约 15GB，内存约 31.8GB（空闲约 15.7GB），磁盘 E: 空闲约 687GB。

## 环境准备

```powershell
# 国内镜像（官方 pypi.org / huggingface.co 探测超时）
$env:UV_INDEX_URL = 'https://pypi.tuna.tsinghua.edu.cn/simple'
$env:HF_ENDPOINT = 'https://hf-mirror.com'
$env:HF_HUB_DISABLE_XET = '1'

# Python 3.11（README 推荐；勿用过新的系统 Python）
uv venv --python 3.11 .venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
uv pip install -e .

# 清华源默认会装到 CPU 版 torch，需再装 CUDA 轮子（本机验证：2.9.1+cu126）
uv pip install "https://download.pytorch.org/whl/cu126/torch-2.9.1%2Bcu126-cp311-cp311-win_amd64.whl"
uv pip install "https://download.pytorch.org/whl/cu126/torchaudio-2.9.1%2Bcu126-cp311-cp311-win_amd64.whl"

# 模型权重（避开官方默认的 GitHub rvcmd；HF 需关 Xet 否则可能 401）
hf download 2Noise/ChatTTS --local-dir .\models\ChatTTS
```

## 启动

- 推荐：`pwsh -NoProfile -File .\start.ps1`
- 说明：启动后按提示选择服务；**不要默认全开**。默认选项为 **webui**。菜单：`webui` / `cmd`。
- 自动化：`-Service webui|cmd`；WebUI 可加 `-Port <起点>`

等价手动命令（webui）：

```powershell
$env:HF_ENDPOINT = 'https://hf-mirror.com'
$env:HF_HUB_DISABLE_XET = '1'
$env:Path = "E:\Programs\ffmpeg-master-latest-win64-gpl\bin;$env:Path"
.\.venv\Scripts\python.exe examples\web\webui.py --server_name 0.0.0.0 --server_port <端口> --custom_path .\models\ChatTTS
```

默认建议端口起点：`8080`（占用则由 `start.ps1` 顺延）。

等价手动命令（cmd）：

```powershell
$env:PYTHONUTF8 = '1'
.\.venv\Scripts\python.exe examples\cmd\run.py --source custom --custom_path .\models\ChatTTS "Hello, this is a ChatTTS test."
```

## 验证

1. 浏览器打开 `http://127.0.0.1:<实际端口>/`，页面标题含 ChatTTS。
2. 在 Input Text 输入中文或英文短句，点生成，能播放/下载音频且无 CUDA OOM。
3. 或 CLI：`examples\cmd\run.py` 退出码 0，并生成 `output_audio_*.mp3`。

本机已验证：WebUI `http://127.0.0.1:8080/` HTTP 200；CLI 生成 `output_audio_0.mp3`（约 32KB）。

## 备注

- 端口：本机验证实际为 `http://127.0.0.1:8080/`；`start.ps1` 从 8080 起探测占用后顺延。
- 镜像：PyPI → `pypi.tuna.tsinghua.edu.cn`；HF → `hf-mirror.com`（`HF_HUB_DISABLE_XET=1`）；PyTorch CUDA 轮子直连 `download.pytorch.org/whl/cu126`。
- ffmpeg：`E:\Programs\ffmpeg-master-latest-win64-gpl\bin`。
- 未使用 Docker（纯 Python + Gradio，官方推荐直接安装）。
- 官方 `source=local` 会从 GitHub Release 拉 `rvcmd`，本机读超时易失败；已改为 HF 镜像落到 `models\ChatTTS`，由 `start.ps1` 以 `--custom_path` 加载。
- `scripts\launch_webui.py` 关闭 `inbrowser`，避免无交互会话卡住。
- Linux 专属可选依赖（vLLM / TransformerEngine / FlashAttention / pynini）本机 Windows 不装；文本规范化 WARN 可忽略。
- 模型许可：CC BY-NC 4.0，仅学术/非商用。
