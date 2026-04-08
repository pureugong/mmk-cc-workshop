"""YouTube 영상에서 한국어 자막을 추출하는 스크립트 (yt-dlp 기반)."""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "channels.json"


def load_config(config_path=CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_vtt(vtt_path):
    """VTT 파일을 읽어 순수 텍스트만 추출한다."""
    text_lines = []
    with open(vtt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # 헤더, 빈줄, 타임코드 라인 건너뛰기
            if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                continue
            if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->", line):
                continue
            # VTT 태그 제거
            clean = re.sub(r"<[^>]+>", "", line)
            if clean:
                text_lines.append(clean)
    # 연속 중복 제거 (자동 자막 특성상 같은 줄 반복)
    deduped = []
    for line in text_lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return " ".join(deduped)


def extract_transcript(video_id, max_chars=15000):
    """yt-dlp로 단일 영상에서 한국어 자막을 추출한다.

    Returns:
        (text, source) 튜플. 자막이 없으면 (None, None).
    """
    out_template = f"/tmp/sub_{video_id}"
    vtt_path = f"{out_template}.ko.vtt"

    # 이전 파일 정리
    for p in Path("/tmp").glob(f"sub_{video_id}.*"):
        p.unlink()

    cmd = [
        "yt-dlp",
        "--no-check-certificates",
        "--js-runtimes", "node",
        "--remote-components", "ejs:github",
        "--write-sub",
        "--write-auto-sub",
        "--sub-lang", "ko",
        "--skip-download",
        "--sub-format", "vtt",
        "-o", out_template,
        f"https://www.youtube.com/watch?v={video_id}",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"[WARN] {video_id} yt-dlp 타임아웃", file=sys.stderr)
        return None, None

    if not os.path.exists(vtt_path):
        stderr_msg = result.stderr.strip().split("\n")[-1] if result.stderr else "알 수 없는 오류"
        print(f"[WARN] {video_id} 자막 추출 실패: {stderr_msg}", file=sys.stderr)
        return None, None

    text = parse_vtt(vtt_path)

    # 정리
    os.remove(vtt_path)

    if not text:
        return None, None

    source = "auto"
    if len(text) > max_chars:
        text = text[:max_chars] + "... (truncated)"
    return text, source


def extract_all(videos, max_chars=15000):
    """모든 영상에서 자막을 추출한다. 영상 간 2초 딜레이."""
    results = []

    for i, video in enumerate(videos):
        video_id = video.get("video_id", "")
        title = video.get("title", "")
        print(f"[INFO] ({i+1}/{len(videos)}) 자막 추출: {title}", file=sys.stderr)

        text, source = extract_transcript(video_id, max_chars=max_chars)

        result = {**video, "subtitle_text": text, "subtitle_source": source}
        results.append(result)

        if text:
            print(f"[INFO]   -> {source} 자막 {len(text)}자 추출", file=sys.stderr)
        else:
            print(f"[INFO]   -> 자막 없음", file=sys.stderr)

        # Rate limit 방지 (마지막 영상 제외)
        if i < len(videos) - 1:
            time.sleep(2)

    return results


def main():
    parser = argparse.ArgumentParser(description="자막 추출")
    parser.add_argument("--input", type=str, help="영상 목록 JSON 문자열")
    args = parser.parse_args()

    if args.input:
        videos = json.loads(args.input)
    else:
        videos = json.load(sys.stdin)

    config = load_config()
    max_chars = config.get("processing", {}).get("max_subtitle_chars", 15000)

    results = extract_all(videos, max_chars=max_chars)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
