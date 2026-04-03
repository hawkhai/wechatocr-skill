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
  wechatocr_serv.exe       # server used by wechatocr_demo.py
  wechatocr_1-7079.infz    # model file used by wechatocr_demo.py
  serv\
    runtime\
      infserv64.exe        # inference server  <- auto-started by main script
    wechatocr_1-7079.infz  # model file used by main script
```

## Demo Script

`wechatocr_demo.py` is a minimal standalone demo (requires `pip install requests`).
It uses `wechatocr/wechatocr_serv.exe` and `wechatocr/wechatocr_1-7079.infz` directly.

```bat
python wechatocr_demo.py
```

## Output JSON Format

结果写入 `<name>_wechatocr.json`，核心结构：

```json
{
  "code": 100,
  "result": {
    "code": 100,
    "infer_time": 114.24,
    "result": true,
    "json": {
      "err_code": 0,
      "ocr_result": {
        "single_result": [
          {
            "single_str_utf8": "测试",
            "single_rate": 0.9959527,
            "top": 133.318756,
            "left": 170.262512,
            "bottom": 183.112503,
            "right": 257.803131,
            "one_result": [
              {"one_str_utf8": "测", "one_pos": {"pos": [{"x": 170.26, "y": 133.31}]}},
              {"one_str_utf8": "试", "one_pos": {"pos": [{"x": 201.52, "y": 133.31}]}}
            ]
          },
          {
            "single_str_utf8": "wechatocr",
            "single_rate": 0.9989884,
            "top": 329.484406,
            "left": 384.572876,
            "bottom": 362.648682,
            "right": 567.91687,
            "one_result": [
              {"one_str_utf8": "wechatocr", "one_pos": {"pos": [{"x": 392.60, "y": 329.54}]}}
            ]
          }
        ]
      }
    }
  },
  "time": 125
}
```

| Field | Description |
|---|---|
| `result.json.ocr_result.single_result` | Array of recognized text blocks |
| `single_str_utf8` | Full text of the block |
| `single_rate` | Confidence score (0–1) |
| `top` / `left` / `bottom` / `right` | Bounding box coordinates (pixels) |
| `one_result[].one_str_utf8` | Per-character recognition result |
| `one_result[].one_pos` | Per-character position |
| `result.infer_time` | Inference time (ms) |
| `time` | Total response time (ms) |

## Requirements

- **OS:** Windows
- **Python:** 3.6+
- **Service:** WechatOCR inference server (`infserv64.exe`) — auto-started if found, or manually pre-run on `127.0.0.1:8811`
