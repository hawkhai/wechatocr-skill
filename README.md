# WechatOCR Skill

**[English](#english)** | **[中文](#中文)**

---

<a id="english"></a>

## English

> **[切换到中文版 →](#中文)**

Perform OCR on images via a local WechatOCR HTTP service (`http://127.0.0.1:8811`). Results are saved as `<name>_wechatocr.json` alongside each image. The script auto-detects and starts the inference server — no manual setup required.

### Requirements

- **OS:** Windows
- **Python:** 3.6+ (`python` on system PATH, or bundled Python 3.11.9)
- **Service:** `wechatocr_serv.exe` (auto-started) or manually pre-run on `127.0.0.1:8811`

### File Structure

```
wechatocr-skill/
  wechatocr-skill.bat       # Entry script (auto-locates Python)
  wechatocr-skill.py        # Main logic
  wechatocr_demo.py         # Minimal demo (stdlib only, no third-party deps)
  wechatocr/
    wechatocr_serv.exe      # HTTP service (shared by main & demo) <- auto-started
    wechatocr_1-7079.infz   # Model file (shared by both scripts)
    x64/
      infocr64.exe          # Inference backend (internal worker of wechatocr_serv.exe)
```

Set env var `WECHATOCR_DIR` to override the search root for `wechatocr_serv.exe`.

### Usage

```bat
skills\wechatocr-skill\wechatocr-skill.bat [--force] <image_or_dir> ...
```

- **Formats:** `.jpg` `.jpeg` `.png` `.bmp`
- **Directories:** recursively processes all images
- **`--force` / `-f`:** overwrite existing JSON result files

**Demo script (stdlib only, no third-party deps):**

```bat
python wechatocr_demo.py [image_path]
```

### How It Works

1. Checks if `wechatocr_serv.exe` is running (via `tasklist`); starts it automatically if not, then waits 2 s.
2. Sends an HTTP request for each image (`GET http://127.0.0.1:8811/Infai/Echo`).
3. Writes results to `<name>_wechatocr.json` in the same directory as the image.
4. Skips images whose result JSON already exists (unless `--force` is specified).

### Output JSON Format

<details>
<summary>Click to expand example JSON</summary>

```json
{
  "code": 100,
  "result": {
    "infer_time": 215.32,
    "success": true,
    "ocr_response": {
      "err_code": 0,
      "task_id": 1,
      "type": 0,
      "ocr_result": {
        "single_result": [
          {
            "single_str_utf8": "测试",
            "single_rate": 0.995952785,
            "top": 133.318756,
            "left": 170.262512,
            "bottom": 183.112503,
            "right": 257.803131,
            "single_pos": {"pos": [{"x": 170.262512, "y": 133.318756}]},
            "bold": 1,
            "text_block_origin": {"pos": [{"x": 172.824081, "y": 139.7939}]},
            "one_result": [
              {"one_str_utf8": "测", "one_pos": {"pos": [{"x": 170.262512, "y": 133.318756}]}},
              {"one_str_utf8": "试", "one_pos": {"pos": [{"x": 201.527023, "y": 133.318756}]}}
            ]
          },
          {
            "single_str_utf8": "wechatocr",
            "single_rate": 0.99898845,
            "top": 329.484406,
            "left": 384.572876,
            "bottom": 362.648682,
            "right": 567.91687,
            "single_pos": {"pos": [{"x": 384.808441, "y": 329.484406}]},
            "bold": 1,
            "text_block_origin": {"pos": [{"x": 359.526978, "y": 325.792694}]},
            "one_result": [
              {"one_str_utf8": "wechatocr", "one_pos": {"pos": [{"x": 392.600281, "y": 329.542114}]}}
            ]
          }
        ],
        "image_width": 771,
        "image_height": 479
      }
    }
  },
  "time": 219
}
```

</details>

#### Field Reference

| Field | Description |
|---|---|
| `code` | RPC status code (`100` = OK) |
| `result.success` | Whether OCR succeeded (`true` / `false`) |
| `result.infer_time` | Inference time (ms) |
| `result.ocr_response.err_code` | OCR engine error code (`0` = success) |
| `result.ocr_response.task_id` | Task sequence number |
| `result.ocr_response.type` | Result type — only `0` currently observed |
| `result.ocr_response.ocr_result.image_width` | Image width (px) |
| `result.ocr_response.ocr_result.image_height` | Image height (px) |
| `result.ocr_response.ocr_result.single_result` | Array of recognized text blocks |
| `single_str_utf8` | Full text of the block |
| `single_rate` | Confidence score (0.0–1.0) |
| `top` / `left` / `bottom` / `right` | Bounding box coordinates (px) |
| `single_pos` | Top-left position of the **first character** |
| `bold` | Bold flag — `0` = normal, `1` = bold |
| `text_block_origin` | Origin position of the **entire text block** |
| `one_result[].one_str_utf8` | Per-character recognized text |
| `one_result[].one_pos` | Per-character start position |
| `time` | Total response time (ms) |

### OpenClaw Installation

```bash
git clone https://github.com/hawkhai/wechatocr-skill
# Then install via OpenClaw: clone → verify → register
```

After installation, the skill is available at `~/.openclaw/skills/wechatocr-skill/`.

### Quick Test

```bat
skills\wechatocr-skill\wechatocr-skill.bat test.png
```

Expected result — 2 text blocks recognized:

| Text | Confidence |
|------|------------|
| 测试 | 99.6% |
| wechatocr | 99.9% |

---

<a id="中文"></a>

## 中文

> **[Switch to English →](#english)**

对图片执行 OCR，通过本地 WechatOCR HTTP 服务（`http://127.0.0.1:8811`）识别文字，结果保存为同名 `_wechatocr.json` 文件。脚本会自动检测并启动推理服务器，无需手动预先运行。

### 环境要求

- **操作系统：** Windows
- **Python：** 3.6+（系统 PATH 中的 `python`，或内置 Python 3.11.9）
- **推理服务：** `wechatocr_serv.exe`（自动启动）或手动在 `127.0.0.1:8811` 上预先运行

### 文件结构

```
wechatocr-skill/
  wechatocr-skill.bat       # 入口脚本（自动定位 Python）
  wechatocr-skill.py        # 主逻辑
  wechatocr_demo.py         # 简易演示脚本（纯标准库，无第三方依赖）
  wechatocr/
    wechatocr_serv.exe      # HTTP 服务端（主脚本 & demo 共用）← 自动启动
    wechatocr_1-7079.infz   # 模型文件（两个脚本共用）
    x64/
      infocr64.exe          # 推理后台进程（wechatocr_serv.exe 内部使用）
```

环境变量 `WECHATOCR_DIR` 可覆盖 `wechatocr_serv.exe` 的搜索根目录。

### 使用方法

```bat
skills\wechatocr-skill\wechatocr-skill.bat [--force] <图片或目录> ...
```

- **支持格式：** `.jpg` `.jpeg` `.png` `.bmp`
- **传入目录：** 递归处理所有图片
- **`--force` / `-f`：** 覆盖已有的 JSON 结果文件

**演示脚本（纯标准库，无第三方依赖）：**

```bat
python wechatocr_demo.py [image_path]
```

### 工作流程

1. 检测 `wechatocr_serv.exe` 是否在运行（via `tasklist`）；若未启动则自动启动，等待 2 秒。
2. 对每张图片向服务发送 HTTP 请求（`GET http://127.0.0.1:8811/Infai/Echo`）。
3. 将结果写入与图片同目录的 `<name>_wechatocr.json`。
4. 已有 JSON 文件时自动跳过（除非指定 `--force`）。

### 输出 JSON 格式

<details>
<summary>点击展开示例 JSON</summary>

```json
{
  "code": 100,
  "result": {
    "infer_time": 215.32,
    "success": true,
    "ocr_response": {
      "err_code": 0,
      "task_id": 1,
      "type": 0,
      "ocr_result": {
        "single_result": [
          {
            "single_str_utf8": "测试",
            "single_rate": 0.995952785,
            "top": 133.318756,
            "left": 170.262512,
            "bottom": 183.112503,
            "right": 257.803131,
            "single_pos": {"pos": [{"x": 170.262512, "y": 133.318756}]},
            "bold": 1,
            "text_block_origin": {"pos": [{"x": 172.824081, "y": 139.7939}]},
            "one_result": [
              {"one_str_utf8": "测", "one_pos": {"pos": [{"x": 170.262512, "y": 133.318756}]}},
              {"one_str_utf8": "试", "one_pos": {"pos": [{"x": 201.527023, "y": 133.318756}]}}
            ]
          },
          {
            "single_str_utf8": "wechatocr",
            "single_rate": 0.99898845,
            "top": 329.484406,
            "left": 384.572876,
            "bottom": 362.648682,
            "right": 567.91687,
            "single_pos": {"pos": [{"x": 384.808441, "y": 329.484406}]},
            "bold": 1,
            "text_block_origin": {"pos": [{"x": 359.526978, "y": 325.792694}]},
            "one_result": [
              {"one_str_utf8": "wechatocr", "one_pos": {"pos": [{"x": 392.600281, "y": 329.542114}]}}
            ]
          }
        ],
        "image_width": 771,
        "image_height": 479
      }
    }
  },
  "time": 219
}
```

</details>

#### 关键字段说明

| 字段 | 说明 |
|---|---|
| `code` | RPC 状态码（`100` = 成功） |
| `result.success` | OCR 是否成功（`true` / `false`） |
| `result.infer_time` | 推理耗时（毫秒） |
| `result.ocr_response.err_code` | OCR 引擎错误码（`0` = 成功） |
| `result.ocr_response.task_id` | 任务序号 |
| `result.ocr_response.type` | 结果类型 — 目前仅观察到 `0` |
| `result.ocr_response.ocr_result.image_width` | 图片宽度（像素） |
| `result.ocr_response.ocr_result.image_height` | 图片高度（像素） |
| `result.ocr_response.ocr_result.single_result` | 识别到的文字块列表 |
| `single_str_utf8` | 文字块的完整识别文本 |
| `single_rate` | 识别置信度（0.0～1.0） |
| `top` / `left` / `bottom` / `right` | 文字块边界框坐标（像素） |
| `single_pos` | 该行**第一个字符**的左上角坐标 |
| `bold` | 粗体标记 — `0` = 普通，`1` = 粗体 |
| `text_block_origin` | **整个文本块**的起始位置（左上角坐标） |
| `one_result[].one_str_utf8` | 单字符识别文本 |
| `one_result[].one_pos` | 单字符起始位置坐标 |
| `time` | 总耗时（毫秒） |

### OpenClaw 安装

```bash
git clone https://github.com/hawkhai/wechatocr-skill
# OpenClaw 流程：克隆 → 验证 → 注册
```

安装完成后，技能位于 `~/.openclaw/skills/wechatocr-skill/`。

### 快速测试

```bat
skills\wechatocr-skill\wechatocr-skill.bat test.png
```

预期结果 — 识别到 2 段文字：

| 文字 | 置信度 |
|------|--------|
| 测试 | 99.6% |
| wechatocr | 99.9% |
