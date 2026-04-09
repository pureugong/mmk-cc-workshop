#!/usr/bin/env python3
"""
YouTube RSS 기반 채널 모니터링 스크립트.
.claude/config/stock-alert.json 설정을 읽어 최신 영상 목록을 JSON으로 출력한다.

Usage:
    python .claude/scripts/youtube_monitor.py
    python .claude/scripts/youtube_monitor.py --hours 2
"""
import json
import sys
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen
from urllib.error import URLError
import xml.etree.ElementTree as ET

CONFIG_PATH = ".claude/config/stock-alert.json"
RSS_BASE = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
NS = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def fetch_rss(channel_id):
    url = RSS_BASE.format(channel_id=channel_id)
    try:
        with urlopen(url, timeout=10) as resp:
            return resp.read()
    except URLError as e:
        print(f"[warn] RSS fetch failed for {channel_id}: {e}", file=sys.stderr)
        return None


def parse_rss(xml_bytes, channel_name, keywords, cutoff):
    results = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        print(f"[warn] RSS parse error: {e}", file=sys.stderr)
        return results

    for entry in root.findall("atom:entry", NS):
        # 영상 ID
        video_id_el = entry.find("yt:videoId", NS)
        if video_id_el is None:
            continue
        video_id = video_id_el.text.strip()

        # 제목
        title_el = entry.find("atom:title", NS)
        title = title_el.text.strip() if title_el is not None else ""

        # 링크
        link_el = entry.find("atom:link", NS)
        url = link_el.get("href", "") if link_el is not None else f"https://www.youtube.com/watch?v={video_id}"

        # 발행 일시
        published_el = entry.find("atom:published", NS)
        if published_el is None:
            continue
        try:
            published_str = published_el.text.strip()
            # ISO 8601: 2026-04-09T07:00:00+00:00
            published = datetime.fromisoformat(published_str)
            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

        # 시간 범위 필터
        if published < cutoff:
            continue

        # 키워드 필터 (설정된 경우만)
        if keywords and not any(kw in title for kw in keywords):
            continue

        results.append({
            "video_id": video_id,
            "title": title,
            "url": url,
            "channel": channel_name,
            "published": published.isoformat(),
        })

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=float, help="몇 시간 이내 영상 검색 (설정 파일 기본값 덮어쓰기)")
    args = parser.parse_args()

    config = load_config()
    lookback_hours = args.hours if args.hours else config.get("lookback_hours", 1)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)

    all_videos = []
    for ch in config.get("channels", []):
        channel_id = ch.get("id", "")
        channel_name = ch.get("name", channel_id)
        keywords = ch.get("keywords", [])

        xml_bytes = fetch_rss(channel_id)
        if xml_bytes is None:
            continue

        videos = parse_rss(xml_bytes, channel_name, keywords, cutoff)
        all_videos.extend(videos)
        print(f"[info] {channel_name}: {len(videos)}개 새 영상 발견", file=sys.stderr)

    # 발행일 내림차순 정렬
    all_videos.sort(key=lambda v: v["published"], reverse=True)

    print(json.dumps(all_videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
