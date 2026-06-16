# save-notion

YouTube 영상 요약 데이터를 Notion 데이터베이스에 페이지로 저장합니다.

## 전제 조건

- Notion 데이터베이스가 미리 생성되어 있어야 합니다.
- 데이터베이스에 Notion 통합(Integration)이 연결되어 있어야 합니다.
- `yt-monitor-config.json`의 `notion_database_id`가 실제 DB ID로 설정되어 있어야 합니다.

## Notion 데이터베이스 스키마 (최초 1회 수동 생성)

| 속성명 | 타입 | 설명 |
|--------|------|------|
| 제목 | title | 영상 제목 (필수 title 속성) |
| 채널 | select | 채널 이름 |
| Video ID | rich_text | YouTube video ID |
| URL | url | 영상 링크 |
| 게시일 | date | 영상 게시 날짜 |
| 처리일 | date | 파이프라인 처리 날짜 |
| 자막 여부 | checkbox | 자막 추출 성공 여부 |
| 요약 | rich_text | Claude 요약 내용 |

## 입력 파라미터

- `video_data`: summarize-video 스킬이 반환한 객체
- `channel_name`: 채널 이름 (설정 파일에서 전달)
- `notion_database_id`: Notion 데이터베이스 ID

## 실행 순서

1. `notion_database_id`가 플레이스홀더 값(`YOUR_NOTION_DATABASE_ID`)이면 "Notion DB ID가 설정되지 않았습니다" 출력 후 건너뜁니다.

2. `notion-search` MCP 도구로 중복 확인:
   - 검색어: `video_data.video_id`
   - 결과에 해당 video_id가 포함된 항목이 있으면 "이미 저장된 영상입니다" 출력 후 성공으로 처리

3. `notion-create-pages` MCP 도구로 새 페이지 생성:
   - `parent.database_id`: notion_database_id
   - 속성 값:
     - `제목` (title): video_data.title
     - `채널` (select): channel_name
     - `Video ID` (rich_text): video_data.video_id
     - `URL` (url): video_data.video_url
     - `게시일` (date): video_data.published_at
     - `처리일` (date): video_data.summarized_at
     - `자막 여부` (checkbox): video_data.transcript_available
     - `요약` (rich_text): video_data.summary (2000자 초과 시 잘라서 저장)

4. 페이지 생성 성공 시: "Notion 저장 성공: <title>" 출력

5. 실패 시: MCP 오류 메시지를 그대로 출력하고 예외 발생

## 주의사항

- Notion rich_text 필드 최대 2000자 제한 — summary가 초과하면 1997자에서 잘라내고 `...` 추가
- 날짜 형식은 반드시 ISO 8601 (`2026-04-09T07:00:00.000Z`)
