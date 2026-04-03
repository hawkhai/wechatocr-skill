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
脚本会自动启动推理服务器（`wechatocr_serv.exe`），无需手动预先运行。

## Usage

```bat
skills\wechatocr-skill\wechatocr-skill.bat [--force] <image_or_dir> ...
```

The batch wrapper locates Python automatically (system `PATH` → two easyclaw fallback paths) before running the script.

## What It Does

1. Checks if `wechatocr_serv.exe` is already running (via `tasklist`).
2. If not, locates `wechatocr_serv.exe` (see **Server Discovery** below), starts it as a background process, and waits 2 s for it to initialise.
3. Accepts one or more image files or directories as arguments.
4. For each image (`.jpg` `.jpeg` `.png` `.bmp`), calls the local WechatOCR service and writes the OCR result to `<name>_wechatocr.json` alongside the image.
5. Skips files whose result JSON already exists (override with `--force` / `-f`).
6. If `wechatocr/wechatocr_1-7079.infz` exists under the resolved base directory, it is passed to the service as the model path.

## Server Discovery

The script looks for `wechatocr_serv.exe` at `<base>/wechatocr/wechatocr_serv.exe` where `<base>` is tried in this order:

1. `WECHATOCR_DIR` environment variable (set this to your WechatOCR distribution root).
2. The skill directory itself (`skills\wechatocr-skill\`).

Expected layout inside the distribution / skill folder:

```
wechatocr\
  wechatocr_serv.exe       # HTTP service on 8811 <- auto-started by wechatocr-skill.py & wechatocr_demo.py
  wechatocr_1-7079.infz    # model file (shared by both scripts)
  x64\
    infocr64.exe           # inference backend   (internal worker spawned by wechatocr_serv.exe)
```

## Demo Script

`wechatocr_demo.py` is a minimal standalone demo (requires `pip install requests`).
It uses `wechatocr_serv.exe` and `wechatocr/wechatocr_1-7079.infz` directly.

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
    "infer_time": 212.64,
    "result": true,
    "json": {
      "err_code": 0,
      "task_id": 1,
      "type": 0,
      "ocr_result": {
        "single_result": [
          {
            "single_str_utf8": "测试",
            "single_rate": 0.9959527,
            "top": 133.318756,
            "left": 170.262512,
            "bottom": 183.112503,
            "right": 257.803131,
            "single_pos": {"pos": [{"x": 170.262512, "y": 133.318756}]},
            "unknown_0": 1,
            "unknown_pos": {"pos": [{"x": 172.824081, "y": 139.7939}]},
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
            "single_pos": {"pos": [{"x": 384.808441, "y": 329.484406}]},
            "unknown_0": 1,
            "unknown_pos": {"pos": [{"x": 359.526978, "y": 325.792694}]},
            "one_result": [
              {"one_str_utf8": "wechatocr", "one_pos": {"pos": [{"x": 392.60, "y": 329.54}]}}
            ]
          }
        ],
        "unknown_1": 771,
        "unknown_2": 479
      }
    }
  },
  "time": 218
}
```

| Field | Description |
|---|---|
| `result.json.ocr_result.single_result` | Array of recognized text blocks |
| `single_str_utf8` | Full text of the block |
| `single_rate` | Confidence score (0–1) |
| `top` / `left` / `bottom` / `right` | Bounding box coordinates (pixels) |
| `single_pos` | Top-left anchor position of the text block |
| `unknown_0` | Reserved field (always `1`) |
| `unknown_pos` | Reserved position field |
| `one_result[].one_str_utf8` | Per-character recognition result |
| `one_result[].one_pos` | Per-character position |
| `result.json.task_id` | Task sequence number |
| `result.json.type` | Result type flag (always `0`) |
| `result.json.ocr_result.unknown_1` | Image width (pixels) |
| `result.json.ocr_result.unknown_2` | Image height (pixels) |
| `result.infer_time` | Inference time (ms) |
| `time` | Total response time (ms) |

## Requirements

- **OS:** Windows
- **Python:** 3.6+
- **Service:** WechatOCR server (`wechatocr_serv.exe`) — auto-started if found, or manually pre-run on `127.0.0.1:8811`
