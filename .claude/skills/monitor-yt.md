# monitor-yt

한국 증시 YouTube 채널을 모니터링하여 새 영상을 요약하고 Slack과 Notion에 저장합니다.

## 실행 순서

### 1. 설정 파일 로드

`/home/user/mmk-cc-workshop/data/yt-monitor-config.json` 파일을 읽습니다.
파일이 없으면: "설정 파일을 찾을 수 없습니다. data/yt-monitor-config.json을 생성해 주세요." 출력 후 종료.

### 2. 상태 파일 로드

`/home/user/mmk-cc-workshop/data/yt-processed.json` 파일을 읽습니다.
파일이 없으면 `{ "processed_video_ids": [], "last_updated": null }` 로 초기화합니다.

### 3. 채널 순회

설정의 `channels` 배열을 순회합니다. 각 채널에 대해:

**a. `/fetch-channel` 스킬 호출**
다음 정보를 전달:
- `channel`: 현재 채널 객체 `{ name, channel_id }`
- `filter_keywords`: 설정의 `filter_keywords`
- `processed_ids`: 상태 파일의 `processed_video_ids`
- `max_videos`: 설정의 `max_videos_per_channel`

**b. 새 영상이 없으면** "<채널명>: 새 영상 없음" 출력 후 다음 채널로.

**c. 새 영상이 있으면** 각 영상에 대해 다음을 순서대로 실행:

1. **`/summarize-video` 스킬 호출**
   - `video`: fetch-channel이 반환한 영상 객체

2. **`/notify-slack` 스킬 호출**
   - `video_data`: summarize-video 결과
   - `slack_webhook_url`: 설정의 `slack_webhook_url`

3. **`/save-notion` 스킬 호출**
   - `video_data`: summarize-video 결과
   - `channel_name`: 현재 채널명
   - `notion_database_id`: 설정의 `notion_database_id`

4. **상태 파일 업데이트**: 모든 단계 성공 시
   - `processed_video_ids` 배열에 `video_id` 추가
   - `last_updated`를 현재 시각(ISO 8601)으로 업데이트
   - `/home/user/mmk-cc-workshop/data/yt-processed.json` 파일 저장

### 4. 오류 처리

개별 영상 처리 중 오류 발생 시:
- 오류 메시지를 출력하고 해당 영상을 건너뜁니다
- 해당 video_id는 `processed_video_ids`에 추가하지 않습니다 (다음 실행 시 재시도)
- 나머지 영상 처리는 계속합니다

### 5. 완료 요약 출력

```
=== 모니터링 완료 ===
처리 채널: N개
새 영상 처리: M개
실패: K개
마지막 실행: <현재 시각>
```

---

## 스케줄 실행 방법

이 스킬을 1시간마다 자동 실행하려면:
```
/loop 1h /monitor-yt
```

## 수동 실행 방법

```
/monitor-yt
```
