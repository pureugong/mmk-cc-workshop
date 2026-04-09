# /check-youtube — 새 영상 확인 + 키워드 필터링

한국 증시 유튜브 채널에서 새 영상을 확인하고, 키워드 필터링을 수행합니다.

## 실행 절차

1. `config/channels.json` 파일을 읽어 채널 목록과 키워드를 로드합니다.
2. `data/processed-videos.json` 파일을 읽어 이미 처리된 영상 ID 목록을 로드합니다.
3. 각 채널에 대해 YouTube RSS 피드를 조회합니다:
   - URL: `https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}`
   - `curl -s`로 가져온 뒤 XML에서 `<entry>` 항목을 파싱합니다.
   - 각 entry에서 `<yt:videoId>`, `<title>`, `<published>` 를 추출합니다.
4. `max_videos_per_check` 설정값만큼 최신 영상만 확인합니다.
5. 키워드 필터링: 영상 제목에 설정된 키워드(주식, 투자, 시장 등) 중 하나라도 포함되어 있는지 확인합니다.
6. 이미 `data/processed-videos.json`에 있는 video ID는 건너뜁니다.
7. 필터링된 새 영상 목록을 아래 형식으로 출력합니다:

```
## 새로운 영상 발견

| 채널 | 제목 | Video ID | 게시일 |
|------|------|----------|--------|
| 삼프로TV | 제목예시 | abc123 | 2026-04-09 |
```

새 영상이 없으면 "새로운 키워드 매칭 영상이 없습니다." 를 출력합니다.

## 사용하는 도구

- Bash: `curl -s` 로 YouTube RSS 피드 조회
- Read: `config/channels.json`, `data/processed-videos.json` 읽기

## 주의사항

- RSS 피드는 최신 15개 영상만 제공합니다.
- XML 파싱 시 `grep`, `sed` 등 쉘 도구를 활용합니다.
- 이 스킬은 `data/processed-videos.json`을 수정하지 않습니다 (읽기만 합니다).
