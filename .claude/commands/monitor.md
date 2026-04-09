# /monitor — YouTube 채널 모니터링 전체 파이프라인

등록된 YouTube 채널에서 새 영상을 감지하고, 자막 추출 → 한국어 요약 → Slack 알림 → Notion 저장까지 자동으로 실행합니다.

## 실행 절차

### 1단계: 새 영상 감지

```bash
python3 src/fetch_videos.py | python3 src/state.py filter
```

결과를 JSON으로 파싱합니다. 새 영상이 없으면 "새 영상이 없습니다. 모니터링을 종료합니다." 메시지를 출력하고 종료합니다.

### 2단계: 각 새 영상 처리

새 영상 각각에 대해 다음을 순서대로 실행합니다:

#### a. 메타데이터 조회
```bash
mmk youtube metadata {video_url}
```

#### b. 자막 추출
```bash
mmk youtube transcript {video_url}
```
자막이 없으면 해당 영상은 건너뛰고 다음 영상으로 진행합니다.

#### c. 한국어 요약 생성
자막 내용을 분석하여 다음을 생성합니다:
- 한줄 요약
- 주요 내용 3-5개 bullet point
- 키워드 3-5개

요약은 반드시 **한국어**로 작성합니다.

#### d. Slack 알림 전송
Slack MCP `slack_search_channels` 로 `youtube-summary` 채널 ID를 조회한 뒤,
`slack_send_message` 로 아래 형식의 메시지를 전송합니다:

```
🎬 *새 YouTube 영상 요약*

*제목*: {제목}
*채널*: {채널명}
*URL*: {URL}

📌 *한줄 요약*
{한줄 요약}

📋 *주요 내용*
• {포인트 1}
• {포인트 2}
• {포인트 3}

🏷️ *키워드*: {키워드}
```

#### e. Notion 저장
1. Notion MCP `notion-search` 로 "YouTube 영상 요약" 데이터베이스를 검색합니다.
2. 데이터베이스가 없으면 `notion-create-database` 로 생성합니다:
   ```sql
   CREATE TABLE "YouTube 영상 요약" (
     "제목" title,
     "채널" rich_text,
     "URL" url,
     "한줄 요약" rich_text,
     "키워드" rich_text,
     "게시일" date,
     "처리일" date,
     "상태" select('완료', '검토 필요')
   );
   ```
3. `notion-create-pages` 로 영상 데이터를 저장합니다.

#### f. 처리 완료 마킹
```bash
python3 src/state.py mark {video_id}
```

### 3단계: 결과 보고

모든 영상 처리 후 결과를 요약하여 보여줍니다:

```
✅ 모니터링 완료

처리된 영상: N개
건너뛴 영상: M개 (자막 없음)

| # | 채널 | 제목 | 상태 |
|---|------|------|------|
| 1 | 채널1 | 제목1 | ✅ 완료 |
| 2 | 채널2 | 제목2 | ⏭️ 자막 없음 |
```

## 스케줄링

이 커맨드를 주기적으로 실행하려면:
```
/loop 24h /monitor
```

## 주의사항
- `config/channels.json` 에 채널이 등록되어 있어야 합니다.
- Slack MCP와 Notion MCP가 연결되어 있어야 합니다.
- `mmk` CLI가 설치되어 있고 토큰이 설정되어 있어야 합니다.
