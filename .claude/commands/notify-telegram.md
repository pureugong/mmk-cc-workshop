# /notify-telegram - Telegram 알림 전송

요약된 영상 정보를 Telegram DM으로 전송합니다.

## 입력

사용자가 전송할 메시지 내용을 제공합니다. 인자: $ARGUMENTS

## 실행 방법

1. `config/channels.json` 에서 `telegram_bot_token`과 `telegram_chat_id`를 읽습니다.
2. 값이 비어있으면 사용자에게 설정을 요청합니다.
3. `curl`로 Telegram Bot API를 호출하여 메시지를 전송합니다.

## 메시지 형식

```
*[채널명] 새 영상 요약*

*제목:* {title}
*발행일:* {date}

*한줄 요약:*
{summary}

*핵심 포인트:*
{key_points}

*시장 영향:*
{market_impact}

[원본 영상 보기]({video_url})
```

## 전송 방법

```bash
curl -s -X POST "https://api.telegram.org/bot{telegram_bot_token}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "{telegram_chat_id}",
    "text": "위 형식의 메시지",
    "parse_mode": "Markdown"
  }'
```

## 주의사항

- 메시지는 Telegram Markdown 형식을 사용합니다.
- `parse_mode`는 `"Markdown"`을 사용합니다.
- Telegram Markdown에서 특수문자(`_`, `*`, `` ` ``, `[`)는 이스케이프 처리가 필요할 수 있습니다.
- 메시지 길이가 4096자를 초과하면 분할 전송합니다.
