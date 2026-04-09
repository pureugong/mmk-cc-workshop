# Notion DB에 영상 요약 저장

YouTube 영상 요약 정보를 Notion 데이터베이스에 저장합니다.

## 인자

- `$ARGUMENTS` : 저장할 영상 정보 (제목, 채널명, URL, 요약, 키워드, 게시일 등)

인자가 없으면 사용자에게 필요한 정보를 질문합니다.

## 실행 절차

1. `config/stock-monitor.json`에서 `notion_db_id` 값을 읽습니다.
2. DB ID가 비어있으면 Notion MCP `notion-search`로 "증시 유튜브 요약" 데이터베이스를 검색합니다.
3. Notion MCP `notion-create-pages`를 사용하여 다음 속성으로 페이지를 생성합니다.

## DB 속성 매핑

| 속성명 | 타입 | 값 |
|--------|------|-----|
| 제목 | title | 영상 제목 |
| 채널 | select | 채널명 (한경글로벌마켓 / 한국경제TV / 증시각도기TV) |
| URL | url | YouTube 영상 링크 |
| 요약 | rich_text | AI 요약 내용 |
| 키워드 | multi_select | 관련 키워드 태그 |
| 게시일 | date | 영상 게시일 (ISO 8601) |
| 처리일 | date | 현재 날짜/시간 (ISO 8601) |

## 페이지 본문

페이지 본문(content)에는 전체 요약을 마크다운 형식으로 작성합니다:
- 한줄 요약
- 핵심 포인트
- 언급 종목/지수
- 시장 전망

## 참고

- notion_db_id가 없으면 검색 후 config 파일에 자동으로 업데이트합니다
- 중복 저장 방지: 저장 전 동일 URL이 이미 존재하는지 확인합니다
