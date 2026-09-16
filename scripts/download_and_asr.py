# -*- coding: utf-8 -*-
"""财经班长「反转数值」系列视频：下载 + Whisper 语音转写
在 GitHub Actions runner 上运行（带宽好、可访问 HuggingFace）。
"""
import os, re, subprocess, time, sys

LINKS = [
    ("01_反转数值1", "XqniDjmE6Kf1JK2OrGHkuA"),
    ("02_反转数值2", "gs6njBfFBGHo7iwd8FwWgg"),
    ("03_反转数值3", "AybmM6Ds1096mKayTB8N1w"),
    ("04_反转数值4之判顶", "3iodDor4TCbCpg_v4jtEZw"),
    ("05_反转数值5", "99JfpUa7DMgtE79X8D8fSA"),
    ("06_反转数值6真假背离", "NvvtI2y-761NVK5bEsVg0g"),
    ("07_反转数值7", "sbpEn_LwCBt7Vb3pxVYzmg"),
    ("08_macd预测顶底1", "p7L7akGjm-EPCsFs1S7Z_Q"),
    ("09_macd预测顶底2", "cpIuPOC_1OVplJb6GfeWAg"),
    ("10_3K加均介入法", "kzGoaA8J-eMTwa6biBg21A"),
]
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")
OUT, TR = "videos", "transcripts"
os.makedirs(OUT, exist_ok=True)
os.makedirs(TR, exist_ok=True)


def get_mp4(sid):
    url = f"https://mp.weixin.qq.com/s/{sid}"
    r = subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, url],
                       capture_output=True, text=True)
    h = r.stdout.replace("\\x26amp;", "&").replace("\\x26", "&").replace("&amp;", "&")
    urls = re.findall(r'https?://mpvideo\.qpic\.cn/[^"\' <\\]+\.mp4[^"\' <\\]*', h)
    seen, out = set(), []
    for u in urls:
        b = u.split("?")[0]
        if b not in seen:
            seen.add(b); out.append(u)
    return out


# ---------- 1) 下载 ----------
for name, sid in LINKS:
    fp = f"{OUT}/{name}.mp4"
    if os.path.exists(fp) and os.path.getsize(fp) > 50000:
        print("skip", name); continue
    cands = []
    for attempt in range(4):
        cands = get_mp4(sid)
        if cands:
            break
        print("retry", name, attempt, flush=True)
        time.sleep(10)
    if not cands:
        print("NO MP4:", name, flush=True); continue
    subprocess.run(["curl", "-sL", "-m", "300", "-e", "https://mp.weixin.qq.com/",
                    "-A", UA, cands[0], "-o", fp], check=False)
    print("downloaded", name, os.path.getsize(fp) if os.path.exists(fp) else 0, flush=True)

# ---------- 2) 转写 ----------
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
try:
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    print("ASR model ready (small)", flush=True)
except Exception as e:
    print("ASR init failed:", e, flush=True)
    model = None

if model:
    for name, _ in LINKS:
        vp = f"{OUT}/{name}.mp4"
        tp = f"{TR}/{name}.txt"
        if not os.path.exists(vp) or os.path.exists(tp):
            continue
        try:
            segs, _ = model.transcribe(vp, language="zh", beam_size=5, vad_filter=True)
            text = "".join(s.text for s in segs)
            open(tp, "w", encoding="utf-8").write(f"# {name}\n\n{text}")
            print("transcribed", name, len(text), flush=True)
        except Exception as e:
            print("ASR error", name, e, flush=True)

print("ALL DONE")
