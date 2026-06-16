# /notify-slack — Slack 알림 발송

영상 요약 결과를 Slack #general 채널에 알림으로 전송합니다.

## 인자

- `$ARGUMENTS`: 전송할 메시지 내용 (선택). 없으면 아래 기본 동작을 수행합니다.

## 실행 절차

1. Slack MCP의 `slack_search_channels` 도구로 "general" 채널을 검색하여 channel_id를 확인합니다.

2. `slack_send_message` MCP 도구를 사용하여 메시지를 전송합니다.

3. 메시지 포맷:
   ```
   📊 *증시 유튜브 새 영상 알림*

   *{채널명}* — _{영상 제목}_
   📅 게시일: {게시일}

   *요약:*
   {3-5문장 요약 내용}

   *키포인트:*
   • {포인트1}
   • {포인트2}
   • {포인트3}

   🔗 영상 보기: {YouTube URL}
   ```

4. 전송 성공 시 "Slack 알림이 #general 채널에 전송되었습니다." 출력

## 사용하는 도구

- Slack MCP `slack_search_channels`: 채널 ID 조회
- Slack MCP `slack_send_message`: 메시지 전송

## 주의사항

- 여러 영상을 한 번에 알릴 때는 각 영상을 별도 메시지로 전송합니다.
- 메시지는 Slack 마크다운 형식(*bold*, _italic_, • 불릿 등)을 사용합니다.
- 채널 ID를 한 번 조회한 뒤 이후에는 캐시된 값을 재사용합니다.
