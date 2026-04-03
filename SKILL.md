---
name: wechatocr
description: "OCR images via local WechatOCR HTTP service"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["python3"] },
        "install": [],
        "version": "1.1.0",
      },
  }
---

# WechatOCR

对图片执行 OCR，通过本地 WechatOCR HTTP 服务（`http://127.0.0.1:8811`）识别文字，结果保存为同名 JSON 文件。
脚本会自动启动推理服务器（`infserv64.exe`），无需手动预先运行。

## Usage

```bat
skills\wechatocr-skill\wechatocr-skill.bat [--force] <image_or_dir> ...
```

The batch wrapper locates Python automatically (system `PATH` → two easyclaw fallback paths) before running the script.

## What It Does

1. Checks if the WechatOCR HTTP service is already running on `127.0.0.1:8811`.
2. If not, locates `infserv64.exe` (see **Server Discovery** below) and starts it as a detached background process, then waits up to 10 s for it to become ready.
3. Accepts one or more image files or directories as arguments.
4. For each image (`.jpg` `.jpeg` `.png` `.bmp`), calls the local WechatOCR service and writes the OCR result to `<name>_wechatocr.json` alongside the image.
5. Skips files whose result JSON already exists (override with `--force` / `-f`).
6. If `wechatocr/serv/wechatocr_1-7079.infz` exists under the resolved base directory, it is passed to the service as the model path.

## Server Discovery

The script looks for `infserv64.exe` at `<base>/wechatocr/serv/runtime/infserv64.exe` where `<base>` is tried in this order:

1. `WECHATOCR_DIR` environment variable (set this to your WechatOCR distribution root).
2. The skill directory itself (`skills\wechatocr-skill\`).

Expected layout inside the distribution / skill folder:

```
wechatocr\
  wechatocr.exe          # CLI client (optional)
  serv\
    runtime\
      infserv64.exe      # inference server  <- auto-started
    wechatocr_1-7079.infz  # model file
```

## Requirements

- **OS:** Windows
- **Python:** 3.6+
- **Service:** WechatOCR inference server (`infserv64.exe`) — auto-started if found, or manually pre-run on `127.0.0.1:8811`
