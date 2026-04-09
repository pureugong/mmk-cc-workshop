# Slack 증시 알림 발송

YouTube 영상 요약 정보를 Slack 채널에 알림으로 발송합니다.

## 인자

- `$ARGUMENTS` : 알림 내용 (채널명, 영상 제목, 요약, URL 등을 포함한 텍스트)

인자가 없으면 사용자에게 필요한 정보를 질문합니다.

## 실행 절차

1. `config/stock-monitor.json`에서 `slack_channel` 값을 읽습니다.
2. Slack MCP 도구 `slack_search_channels`로 해당 채널을 찾아 channel_id를 확인합니다.
3. Slack MCP 도구 `slack_send_message`로 아래 형식의 메시지를 발송합니다.

## 메시지 형식

```
*[채널명] 새 영상 요약*

*제목:* 영상 제목
*게시일:* YYYY-MM-DD

---

*한줄 요약*
요약 내용

*핵심 포인트*
- 포인트 1
- 포인트 2
- 포인트 3

*언급 종목:* 삼성전자, SK하이닉스, ...
*키워드:* #코스피 #반도체 #AI

<YouTube URL>
```

## 참고

- Slack 채널명이 설정에 없거나 찾을 수 없으면 사용자에게 확인을 요청합니다
- 메시지는 최대 3000자를 넘지 않도록 요약합니다
