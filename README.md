# WechatOCR Skill

对图片执行 OCR，通过本地 WechatOCR HTTP 服务（`http://127.0.0.1:8811`）识别文字，结果保存为同名 `_wechatocr.json` 文件。
脚本会自动检测并启动推理服务器，无需手动预先运行。

## Requirements

- **OS:** Windows
- **Python:** 3.6+（系统 PATH 中的 `python`，或 easyclaw 内置 Python 3.11.9）
- **WechatOCR 推理服务：** `wechatocr_serv.exe`（自动启动）或手动在 `127.0.0.1:8811` 上预先运行

## File Structure

```
wechatocr-skill\
  wechatocr-skill.bat       # 入口脚本（自动定位 Python）
  wechatocr-skill.py        # 主逻辑
  wechatocr_demo.py         # 简易演示脚本（依赖 requests 库）
  wechatocr\
    wechatocr_serv.exe      # HTTP 服务端（主脚本 & demo 共用）← 自动启动
    wechatocr_1-7079.infz   # 模型文件（两个脚本共用）
    x64\
      infocr64.exe          # 推理后台进程（wechatocr_serv.exe 内部使用）
```

环境变量 `WECHATOCR_DIR` 可覆盖 `wechatocr_serv.exe` 的搜索根目录。

## Usage

```bat
skills\wechatocr-skill\wechatocr-skill.bat [--force] <image_or_dir> ...
```

- 支持格式：`.jpg` `.jpeg` `.png` `.bmp`
- 传入目录时递归处理所有图片
- `--force` / `-f`：覆盖已有的 JSON 结果文件

**演示脚本（需要 `requests` 库）：**

```bat
python wechatocr_demo.py
```

## What It Does

1. 检测 `wechatocr_serv.exe` 是否在运行（via `tasklist`）；若未启动则自动启动，等待 2 秒。
2. 对每张图片向服务发送 HTTP 请求（`GET http://127.0.0.1:8811/Infai/Echo`）。
3. 将结果写入与图片同目录的 `<name>_wechatocr.json`。
4. 已有 JSON 文件时自动跳过（除非指定 `--force`）。

## Output JSON Format

结果 JSON 的核心结构如下：

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

### 关键字段说明

| 字段 | 说明 |
|---|---|
| `result.json.ocr_result.single_result` | 识别到的文字块列表 |
| `single_str_utf8` | 文字块的完整识别文本 |
| `single_rate` | 置信度（0～1） |
| `top` / `left` / `bottom` / `right` | 文字块边界框坐标（像素） |
| `single_pos` | 文字块左上角锚点坐标 |
| `unknown_0` | 保留字段（固定为 `1`） |
| `unknown_pos` | 保留位置字段 |
| `one_result[].one_str_utf8` | 单字符识别结果 |
| `one_result[].one_pos` | 单字符位置坐标 |
| `result.json.task_id` | 任务序号 |
| `result.json.type` | 结果类型标志（固定为 `0`） |
| `result.json.ocr_result.unknown_1` | 图像宽度（像素） |
| `result.json.ocr_result.unknown_2` | 图像高度（像素） |
| `result.infer_time` | 推理耗时（毫秒） |
| `time` | 总耗时（毫秒） |
