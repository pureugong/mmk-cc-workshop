# /fetch-videos - YouTube 채널에서 새 영상 가져오기

YouTube 채널의 RSS 피드에서 새 영상을 가져와 키워드/콘텐츠 필터링을 수행합니다.

## 실행 절차

### 1. 설정 파일 읽기

`config/channels.json` 파일을 읽어 채널 목록, 콘텐츠 필터, 키워드 목록을 확인합니다.

### 2. RSS 피드 가져오기

각 채널의 RSS 피드를 `WebFetch` 도구로 가져옵니다:
- 한경글로벌마켓: `https://www.youtube.com/feeds/videos.xml?channel_id=UCWskYkV4c4S9D__rsfOl2JA`
- 한국경제TV: `https://www.youtube.com/feeds/videos.xml?channel_id=UCF8AeLlUbEpKju6v1H6p8Eg`
- 증시각도기TV: `https://www.youtube.com/feeds/videos.xml?channel_id=UCdOjVxkj5JA0iDu3_xcsTyQ`

여러 채널의 RSS 피드를 **병렬로** 가져옵니다.

### 3. RSS XML 파싱

RSS 피드는 Atom XML 형식입니다. 각 `<entry>`에서 다음 정보를 추출합니다:
- `<yt:videoId>` → 비디오 ID
- `<title>` → 영상 제목
- `<published>` → 업로드 날짜
- `<link href="...">` → 영상 URL (또는 `https://www.youtube.com/watch?v={videoId}`로 구성)

### 4. 콘텐츠 필터링

각 채널별 `content_filters`에 정의된 키워드가 영상 제목에 포함되어 있는지 확인합니다:
- 한경글로벌마켓: 제목에 "개장전요것만" 또는 "월스트리트나우"가 포함된 영상만 선택
- 한국경제TV: 제목에 "당잠사"가 포함된 영상만 선택
- 증시각도기TV: 제목에 "증시각도기"가 포함된 영상만 선택

### 5. 키워드 필터링 (보조)

콘텐츠 필터를 통과한 영상 중, `keywords`에 정의된 키워드와 매칭되는 항목을 태그로 기록합니다.
(콘텐츠 필터가 주 필터이므로, 키워드는 태그 용도로만 사용)

### 6. 중복 체크

`data/processed_videos.json` 파일을 읽어 이미 처리된 영상 ID를 확인합니다.
이미 처리된 영상은 건너뜁니다.

### 7. 결과 출력

새로 발견된 영상 목록을 다음 형식으로 사용자에게 보여줍니다:

```
## 새로 발견된 영상 (N건)

| # | 채널 | 콘텐츠 | 제목 | 업로드일 | URL |
|---|------|--------|------|---------|-----|
| 1 | 한경글로벌마켓 | 월스트리트나우 | ... | 2024-01-01 | ... |
```

새 영상이 없으면 "새로운 영상이 없습니다"라고 알립니다.
