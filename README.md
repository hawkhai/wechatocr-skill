# WechatOCR Skill

对图片执行 OCR，通过本地 WechatOCR HTTP 服务（`http://127.0.0.1:8811`）识别文字，结果保存为同名 `_wechatocr.json` 文件。
脚本会自动检测并启动推理服务器，无需手动预先运行。

## Requirements

- **OS:** Windows
- **Python:** 3.6+（系统 PATH 中的 `python`，或 easyclaw 内置 Python 3.11.9）
- **WechatOCR 推理服务器：** `infserv64.exe`（自动启动）或手动在 `127.0.0.1:8811` 上预先运行

## File Structure

```
wechatocr-skill\
  wechatocr-skill.bat       # 入口脚本（自动定位 Python）
  wechatocr-skill.py        # 主逻辑
  wechatocr_demo.py         # 简易演示脚本（依赖 requests 库）
  wechatocr\
    wechatocr_serv.exe      # 服务端（demo 脚本使用）
    wechatocr_1-7079.infz   # 模型文件（demo 脚本使用）
    serv\
      runtime\
        infserv64.exe       # 服务端（主脚本使用）← 自动启动
      wechatocr_1-7079.infz # 模型文件（主脚本使用）
```

环境变量 `WECHATOCR_DIR` 可覆盖 `infserv64.exe` 的搜索根目录。

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

1. 检测 `127.0.0.1:8811` 服务是否在线；若未启动则自动启动 `infserv64.exe`，最多等待 10 秒。
2. 对每张图片向服务发送 HTTP 请求（`POST http://127.0.0.1:8811/Infai/Echo`）。
3. 将结果写入与图片同目录的 `<name>_wechatocr.json`。
4. 已有 JSON 文件时自动跳过（除非指定 `--force`）。

## Output JSON Format

结果 JSON 的核心结构如下：

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

### 关键字段说明

| 字段 | 说明 |
|---|---|
| `result.json.ocr_result.single_result` | 识别到的文字块列表 |
| `single_str_utf8` | 文字块的完整识别文本 |
| `single_rate` | 置信度（0～1） |
| `top` / `left` / `bottom` / `right` | 文字块边界框坐标（像素） |
| `one_result[].one_str_utf8` | 单字符识别结果 |
| `one_result[].one_pos` | 单字符位置坐标 |
| `result.infer_time` | 推理耗时（毫秒） |
| `time` | 总耗时（毫秒） |
