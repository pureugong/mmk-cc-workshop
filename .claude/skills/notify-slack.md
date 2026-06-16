# notify-slack

요약된 YouTube 영상 정보를 Slack 채널에 전송합니다.

## 입력 파라미터

- `video_data`: summarize-video 스킬이 반환한 객체
  - `title`, `video_url`, `channel_name`, `published_at`, `summary`
- `slack_webhook_url`: Slack Incoming Webhook URL (설정 파일에서 전달)

## 실행 순서

1. 다음 형식으로 Slack Block Kit 메시지 JSON을 구성합니다:

   ```json
   {
     "blocks": [
       {
         "type": "header",
         "text": {
           "type": "plain_text",
           "text": "📺 <channel_name>"
         }
       },
       {
         "type": "section",
         "text": {
           "type": "mrkdwn",
           "text": "*<<video_url>|<title>>*"
         }
       },
       {
         "type": "section",
         "text": {
           "type": "mrkdwn",
           "text": "<summary>"
         }
       },
       {
         "type": "context",
         "elements": [
           {
             "type": "mrkdwn",
             "text": "게시일: <published_at> | 🔗 <video_url>"
           }
         ]
       }
     ]
   }
   ```

2. curl로 Slack Webhook에 POST합니다:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" \
     -X POST \
     -H 'Content-Type: application/json' \
     -d '<JSON_PAYLOAD>' \
     '<slack_webhook_url>'
   ```

3. HTTP 응답 코드 확인:
   - 200: 성공 → "Slack 전송 성공: <title>" 출력
   - 그 외: 실패 → 상태 코드와 함께 오류 메시지 출력 후 예외 발생

## 주의사항

- JSON 페이로드 내 title이나 summary에 큰따옴표(`"`)나 백슬래시(`\`)가 포함된 경우 이스케이프 처리
- summary가 2900자를 초과하면 2900자에서 잘라내고 `...` 추가
- `slack_webhook_url`이 플레이스홀더 값(`hooks.slack.com/services/YOUR/...`)이면 전송 없이 "Slack 웹훅 URL이 설정되지 않았습니다" 출력 후 건너뜁니다
