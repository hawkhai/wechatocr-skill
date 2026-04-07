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
  wechatocr_demo.py         # 简易演示脚本（纯标准库，无第三方依赖）
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

**演示脚本（纯标准库，无第三方依赖）：**

```bat
python wechatocr_demo.py [image_path]
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

### 关键字段说明

| 字段 | 说明 |
|---|---|
| `result.success` | OCR 是否成功（`true` / `false`） |
| `result.ocr_response.ocr_result.single_result` | 识别到的文字块列表 |
| `single_str_utf8` | 文字块的完整识别文本（UTF8格式整行文本） |
| `single_rate` | 单行识别置信度（0.0～1.0） |
| `top` / `left` / `bottom` / `right` | 文字块边界框坐标（像素） |
| `single_pos` | 该行**第一个字符**的左上角坐标 |
| `bold` | 粗体标记 — `0` = 普通，`1` = 粗体 |
| `text_block_origin` | **整个文本块**的起始位置（左上角坐标） |
| `one_result[].one_str_utf8` | 单字符识别文本 |
| `one_result[].one_pos` | 单字符起始位置坐标 |
| `result.ocr_response.task_id` | 任务序号 |
| `result.ocr_response.type` | 结果类型 — 目前仅观察到 `0` |
| `result.ocr_response.ocr_result.image_width` | 原始图片宽度（像素） |
| `result.ocr_response.ocr_result.image_height` | 原图片高度（像素） |
| `result.infer_time` | 推理耗时（毫秒） |
| `time` | 总耗时（毫秒） |

## OpenClaw 安装

> 用 git 下拉 https://github.com/hawkhai/wechatocr-skill 并安装一下 这个技能。

> 好，先读一下 find-skill 或 create-skill 的安装流程，再按步骤来。这是从外部 git 仓库导入，按导入流程走。先克隆仓库，再验证，再注册。克隆成功，文件结构正常。先看一下 SKILL.md 和 _meta.json 确认结构，再跑验证脚本。结构完整，跑验证脚本再注册。验证通过，开始注册。✅ 安装完成！
> 
> 整个流程走完：
> 1. 克隆 https://github.com/hawkhai/wechatocr-skill ✓
> 2. 验证 结构检查通过 ✓
> 3. 注册 安装到 C:\Users\Administrator\.easyclaw\skills\wechatocr-skill\ ✓
> 
> WechatOCR Skill 🔍 现在可以使用了。它的功能是通过本地 WechatOCR HTTP 服务（127.0.0.1:8811）对图片做 OCR 识别，自动启动 wechatocr_serv.exe，无需手动预先运行。用法：
> ```bat
> skills\wechatocr-skill\wechatocr-skill.bat [--force] <图片或目录>
> ```

## 技能使用

> 用 wechatocr-skill 技能 ocr 一下图片 <https://github.com/hawkhai/wechatocr-skill/blob/main/test.png>，看看上面都有什么文字？

> 先下载图片，再用 WechatOCR 识别。已经输出结果了，读取 JSON。OCR 结果出来了，图片上共识别到 2 段文字：
> 
> | 文字 | 置信度 |
> |------|--------|
> | 测试 | 99.6% |
> | wechatocr | 99.9% |
> 
> 识别置信度都接近 100%，结果非常准确。这张图就是 WechatOCR 技能的测试图，上面写的是 "测试" 和 "wechatocr"。
