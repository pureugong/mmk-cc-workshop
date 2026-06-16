# fetch-channel

YouTube 채널의 RSS 피드에서 최신 영상을 가져와 키워드 필터링 후 반환합니다.

## 입력 파라미터

이 스킬을 호출할 때 다음 정보를 전달받습니다:
- `channel`: `{ name, channel_id }` 객체
- `filter_keywords`: 필터링 키워드 배열
- `processed_ids`: 이미 처리된 video ID 배열
- `max_videos`: 최대 반환 영상 수 (기본값: 5)

## 실행 순서

1. RSS URL을 구성합니다:
   ```
   https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>
   ```

2. curl로 RSS 피드를 가져옵니다:
   ```bash
   curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>"
   ```

3. XML 응답에서 각 `<entry>` 블록을 파싱합니다. 각 entry에서 추출:
   - `<yt:videoId>` → video_id
   - `<title>` → title (CDATA 태그 제거)
   - `<published>` → published_at
   - video_url: `https://www.youtube.com/watch?v=<video_id>` 형태로 구성

4. 필터링 적용 (순서대로):
   a. `processed_ids`에 이미 있는 video_id 제외
   b. 제목(title)에 `filter_keywords` 중 하나라도 포함된 것만 유지 (부분 문자열 매칭)

5. 최신 `max_videos`개만 남깁니다 (RSS는 최신순 정렬).

6. 결과를 다음 구조의 배열로 출력합니다:
   ```json
   [
     {
       "video_id": "VIDEO_ID",
       "title": "영상 제목",
       "published_at": "2026-04-09T07:00:00Z",
       "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
       "channel_name": "채널명"
     }
   ]
   ```

7. 매칭 영상이 없으면 빈 배열 `[]`을 반환합니다.

## 오류 처리

- curl 실패(네트워크 오류 등) 시: 오류 메시지 출력 후 빈 배열 반환
- XML 파싱 이상 시: 가능한 만큼 파싱 후 진행
