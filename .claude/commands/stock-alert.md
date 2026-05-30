한국 증시 YouTube 채널을 모니터링하여 최신 영상을 요약하고 Slack과 Notion에 저장하는 자동화 커맨드입니다.

## 실행 순서

### 0. 설정 확인 및 Notion DB 초기화

`.claude/config/stock-alert.json` 파일을 읽어 설정을 확인한다.

`notion_database_id`가 비어 있으면 Notion MCP(`notion-create-database`)로 "한국 증시 YouTube 알림" 데이터베이스를 자동 생성한다.

DB 생성 시 다음 컬럼을 포함한다:
- Name (title) — 영상 제목
- VideoID (rich_text) — 중복 방지용 YouTube 영상 ID
- Channel (select) — 채널명
- URL (url) — YouTube 링크
- Summary (rich_text) — 요약 내용
- PublishedAt (date) — 영상 업로드 일시
- ProcessedAt (date) — 처리 시각

생성된 DB ID를 `.claude/config/stock-alert.json`의 `notion_database_id` 필드에 저장한다.

### 1. 최신 영상 목록 조회

다음 명령을 실행하여 후보 영상 JSON 목록을 가져온다:

```bash
python .claude/scripts/youtube_monitor.py
```

결과가 빈 배열(`[]`)이면 "새로운 영상이 없습니다"를 출력하고 종료한다.

### 2. 각 영상 처리

각 영상에 대해 아래 순서로 처리한다:

#### 2a. 중복 확인

Notion MCP(`notion-search`)로 해당 `video_id`가 이미 데이터베이스에 있는지 확인한다.
이미 존재하면 이 영상을 건너뛴다.

#### 2b. Shorts 확인

```bash
mmk youtube videotype <url>
```

결과가 `short`이면 건너뛴다.

#### 2c. 자막 추출

```bash
mmk youtube transcript <url>
```

자막이 없거나 추출 실패 시 해당 영상을 건너뛴다.
자막이 `max_transcript_chars`(기본 8000자)를 초과하면 앞 8000자만 사용한다.

#### 2d. 요약 생성

다음 기준으로 한국어 요약을 작성한다:
- 핵심 포인트 3~5개를 bullet 형식으로
- 오늘의 주요 시장 이슈, 주목할 종목, 전망 위주로 요약
- 간결하고 투자자가 바로 활용할 수 있는 내용

#### 2e. Slack 알림 발송

Slack MCP(`slack-send-message`)로 `slack_channel`에 다음 형식으로 메시지를 발송한다:

```
📺 *[채널명]* 영상 제목
🕐 업로드: YYYY-MM-DD HH:MM (KST)

📝 *요약*
• 핵심 포인트 1
• 핵심 포인트 2
• 핵심 포인트 3

🔗 <YouTube 링크|영상 보기>
```

#### 2f. Notion 저장

Notion MCP(`notion-create-pages`)로 데이터베이스에 다음 데이터를 저장한다:
- **Name**: 영상 제목
- **VideoID**: video_id
- **Channel**: 채널명
- **URL**: YouTube 링크
- **Summary**: 요약 텍스트
- **PublishedAt**: 영상 업로드 일시
- **ProcessedAt**: 현재 시각 (ISO 8601)

### 3. 결과 보고

처리 결과를 요약하여 출력한다:
- 처리된 영상 수
- 건너뛴 영상 수 (중복/Shorts/자막 없음)
- Slack 발송 및 Notion 저장 완료 여부

---

## 자동화 실행

1시간마다 자동으로 실행하려면:

```
/loop 1h /stock-alert
```
