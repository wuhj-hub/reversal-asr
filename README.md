# reversal-asr

「财经班长」反转数值系列教学视频 —— **下载 + Whisper 语音转写**（GitHub Actions）。

## 用途
沙箱/本地带宽受限，无法下载 Whisper 模型；改在 GitHub runner（带宽好、可访问 HuggingFace）上：
1. 重新抓取 10 篇文章短链，解析内嵌视频的 `mpvideo.qpic.cn` mp4 源；
2. 用 `faster-whisper`（small，中文）转写；
3. 结果提交到 `transcripts/*.txt`，视频作为 artifact 上传。

## 课程清单
| # | 标题 |
|---|------|
| 01 | 反转数值1 |
| 02 | 反转数值2 |
| 03 | 反转数值3 |
| 04 | 反转数值4之判顶 |
| 05 | 反转数值5 |
| 06 | 反转数值6真假背离 |
| 07 | 反转数值7 |
| 08 | macd预测顶底1 |
| 09 | macd预测顶底2 |
| 10 | 3K加均介入法 |

## 运行
Actions → `reversal-asr` → Run workflow。或本地：
```bash
pip install faster-whisper
python scripts/download_and_asr.py
```

> 仅供学习研究，视频版权归原作者「财经班长」所有。
