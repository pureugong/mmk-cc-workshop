#!/usr/bin/env python3
"""YouTube RSS 피드를 파싱하여 최신 영상 목록을 JSON으로 출력하는 스크립트."""

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
NAMESPACE = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed-videos.json"
CONFIG_FILE = PROJECT_ROOT / "config" / "stock-monitor.json"


def load_processed():
    if PROCESSED_FILE.exists():
        return json.loads(PROCESSED_FILE.read_text())
    return {"processed": [], "last_scan": ""}


def load_config():
    return json.loads(CONFIG_FILE.read_text())


def fetch_rss(channel_id):
    url = RSS_URL.format(channel_id=channel_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    entries = []
    for entry in root.findall("atom:entry", NAMESPACE):
        video_id = entry.find("yt:videoId", NAMESPACE).text
        title = entry.find("atom:title", NAMESPACE).text
        published = entry.find("atom:published", NAMESPACE).text
        link = entry.find("atom:link", NAMESPACE).get("href")
        entries.append({
            "video_id": video_id,
            "title": title,
            "published": published,
            "link": link,
        })
    return entries


def filter_new(entries, processed_ids):
    return [e for e in entries if e["video_id"] not in processed_ids]


def filter_by_keywords(entries, content_keywords, topic_keywords):
    filtered = []
    for entry in entries:
        title_lower = entry["title"].lower()
        content_match = any(kw.lower() in title_lower for kw in content_keywords)
        topic_match = any(kw.lower() in title_lower for kw in topic_keywords)
        if content_match or topic_match:
            entry["match_type"] = "content" if content_match else "topic"
            filtered.append(entry)
    return filtered


def main():
    config = load_config()
    processed_data = load_processed()
    processed_ids = set(processed_data["processed"])

    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "all":
        channels = config["channels"]
    else:
        channels = [ch for ch in config["channels"] if ch["channel_id"] == mode]
        if not channels:
            channels = [ch for ch in config["channels"] if mode.lower() in ch["name"].lower()]

    all_results = []
    for channel in channels:
        try:
            xml_text = fetch_rss(channel["channel_id"])
            entries = parse_feed(xml_text)
            new_entries = filter_new(entries, processed_ids)
            filtered = filter_by_keywords(
                new_entries,
                channel["content_keywords"],
                config["topic_keywords"],
            )
            for entry in filtered[:config["max_videos_per_scan"]]:
                entry["channel_name"] = channel["name"]
            all_results.extend(filtered[:config["max_videos_per_scan"]])
        except Exception as e:
            print(f"Error fetching {channel['name']}: {e}", file=sys.stderr)

    print(json.dumps(all_results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
