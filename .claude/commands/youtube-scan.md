# YouTube 증시 채널 새 영상 스캔

`config/stock-monitor.json` 설정 파일을 읽고, 등록된 유튜브 채널의 RSS 피드에서 새로운 영상을 탐색합니다.

## 실행 절차

1. `python3 .claude/scripts/fetch-rss.py all` 을 실행하여 모든 채널의 RSS 피드를 조회합니다.
2. 설정 파일의 콘텐츠명 키워드와 주제 키워드로 제목을 필터링합니다.
3. 이미 처리된 영상(`data/processed-videos.json`)은 제외합니다.
4. 필터링된 각 영상에 대해 `mmk youtube videotype <url>` 명령어로 Shorts 여부를 확인합니다.
5. Shorts가 아닌 영상만 최종 결과로 출력합니다.

## 출력 형식

각 영상에 대해 다음 정보를 출력합니다:
- 채널명
- 영상 제목
- 게시일
- YouTube URL
- 매칭 유형 (콘텐츠명 / 주제 키워드)

## 참고

- RSS 피드 URL: `https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}`
- 채널당 최대 `max_videos_per_scan`개 영상을 처리합니다 (기본값: 5)
