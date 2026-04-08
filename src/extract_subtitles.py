"""YouTube 영상에서 한국어 자막을 추출하는 스크립트 (youtube-transcript-api 기반)."""

import argparse
import json
import sys
import time
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

CONFIG_PATH = Path(__file__).parent.parent / "config" / "channels.json"


def load_config(config_path=CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_transcript(video_id, max_chars=15000):
    """youtube-transcript-api로 단일 영상에서 한국어 자막을 추출한다.

    Returns:
        (text, source) 튜플. 자막이 없으면 (None, None).
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=["ko"])
        text = " ".join(snippet.text for snippet in transcript.snippets)
        if not text.strip():
            return None, None
        source = "auto"
        if len(text) > max_chars:
            text = text[:max_chars] + "... (truncated)"
        return text, source
    except Exception as e:
        print(f"[WARN] {video_id} 자막 추출 실패: {e}", file=sys.stderr)
        return None, None


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
