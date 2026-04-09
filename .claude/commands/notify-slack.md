# /notify-slack — Slack 채널에 영상 요약 알림 전송

요약된 영상 정보를 Slack `#youtube-summary` 채널에 전송합니다.

## 인자

$ARGUMENTS — 전송할 메시지 내용 (영상 요약 텍스트). 인자가 없으면 직전에 생성한 요약을 사용합니다.

## 실행 절차

1. Slack MCP `slack_search_channels` 도구로 `youtube-summary` 채널을 검색하여 채널 ID를 확인합니다.

2. Slack MCP `slack_send_message` 도구로 메시지를 전송합니다.

### 메시지 포맷

```
🎬 *새 YouTube 영상 요약*

*제목*: {영상 제목}
*채널*: {채널명}
*URL*: {영상 URL}

📌 *한줄 요약*
{한줄 요약}

📋 *주요 내용*
• {핵심 포인트 1}
• {핵심 포인트 2}
• {핵심 포인트 3}

🏷️ *키워드*: {키워드}
```

## 주의사항
- 채널을 찾지 못하면 사용자에게 올바른 채널명을 확인하도록 안내합니다.
- Slack 메시지는 마크다운 형식(mrkdwn)을 사용합니다.
