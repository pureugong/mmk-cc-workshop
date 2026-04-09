#!/usr/bin/env python3
"""처리된 영상 상태 관리.

사용법:
  python3 src/state.py filter   # stdin으로 영상 목록 JSON을 받아 새 영상만 stdout으로 출력
  python3 src/state.py mark <video_id> [<video_id> ...]  # 처리 완료 마킹
  python3 src/state.py list     # 처리된 영상 ID 목록 출력
"""

import json
import sys
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parent.parent / "data" / "processed_videos.json"


def load_state():
    if not STATE_PATH.exists():
        return {"processed": []}
    with open(STATE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


def filter_new(videos, state):
    """이미 처리된 영상을 제외한 새 영상만 반환."""
    processed = set(state["processed"])
    return [v for v in videos if v["video_id"] not in processed]


def mark_processed(video_ids):
    """영상 ID를 처리 완료 목록에 추가."""
    state = load_state()
    existing = set(state["processed"])
    for vid in video_ids:
        if vid not in existing:
            state["processed"].append(vid)
    save_state(state)
    return len(video_ids)


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "filter":
        videos = json.loads(sys.stdin.read())
        state = load_state()
        new_videos = filter_new(videos, state)
        print(json.dumps(new_videos, ensure_ascii=False, indent=2))

    elif command == "mark":
        if len(sys.argv) < 3:
            print("사용법: python3 src/state.py mark <video_id> [...]", file=sys.stderr)
            sys.exit(1)
        video_ids = sys.argv[2:]
        count = mark_processed(video_ids)
        print(f"{count}개 영상 처리 완료 마킹")

    elif command == "list":
        state = load_state()
        for vid in state["processed"]:
            print(vid)

    else:
        print(f"알 수 없는 명령: {command}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
