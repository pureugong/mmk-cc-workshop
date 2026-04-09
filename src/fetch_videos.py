#!/usr/bin/env python3
"""YouTube RSS 피드에서 채널별 최근 영상 목록을 가져온다."""

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "channels.json"
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

ATOM_NS = "{http://www.w3.org/2005/Atom}"
YT_NS = "{http://www.youtube.com/xml/schemas/2015}"
MEDIA_NS = "{http://search.yahoo.com/mrss/}"


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def fetch_channel_videos(channel_id, channel_name, max_videos=15):
    """RSS 피드에서 최근 영상 목록을 파싱한다."""
    url = RSS_URL.format(channel_id=channel_id)
    try:
        with urlopen(url, timeout=15) as resp:
            xml_data = resp.read()
    except URLError as e:
        print(f"[ERROR] 채널 {channel_name} ({channel_id}) 피드 가져오기 실패: {e}", file=sys.stderr)
        return []

    root = ET.fromstring(xml_data)
    videos = []

    for entry in root.findall(f"{ATOM_NS}entry")[:max_videos]:
        video_id = entry.find(f"{YT_NS}videoId")
        title = entry.find(f"{ATOM_NS}title")
        published = entry.find(f"{ATOM_NS}published")

        if video_id is None:
            continue

        videos.append({
            "video_id": video_id.text,
            "title": title.text if title is not None else "",
            "published": published.text if published is not None else "",
            "channel_id": channel_id,
            "channel_name": channel_name,
            "url": f"https://www.youtube.com/watch?v={video_id.text}",
        })

    return videos


def main():
    config = load_config()
    max_videos = config.get("max_videos_per_run", 5)
    all_videos = []

    for ch in config["channels"]:
        videos = fetch_channel_videos(ch["id"], ch["name"], max_videos=max_videos)
        all_videos.extend(videos)

    # 게시일 기준 최신순 정렬
    all_videos.sort(key=lambda v: v["published"], reverse=True)

    print(json.dumps(all_videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
