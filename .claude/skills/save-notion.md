# /save-notion — Notion 데이터베이스 저장

영상 요약 결과를 Notion 데이터베이스에 저장합니다.

## 인자

- `$ARGUMENTS`: 저장할 영상 정보 (제목, 채널, URL, 요약, 키워드, 게시일). 없으면 사용자에게 정보를 요청합니다.

## 실행 절차

### 1단계: DB 확인 또는 생성

1. Notion MCP `notion-search` 도구로 "증시 유튜브 모니터링" 데이터베이스를 검색합니다.
   - query: "증시 유튜브 모니터링"
   - query_type: "internal"
   - filters: {}

2. DB가 없으면 `notion-create-database` 로 새로 생성합니다:
   ```sql
   CREATE TABLE (
     "제목" TITLE,
     "채널" SELECT('삼프로TV':blue, '슈카월드':purple),
     "URL" URL,
     "요약" RICH_TEXT,
     "키워드" MULTI_SELECT('주식':green, '투자':blue, '시장':orange),
     "게시일" DATE,
     "처리일" DATE
   )
   ```
   - title: "증시 유튜브 모니터링"

### 2단계: 페이지 생성

3. `notion-create-pages` 도구로 영상 정보를 새 페이지로 저장합니다:
   - parent: { "type": "database_id", "database_id": "{DB_ID}" }
   - pages 배열에 아래 properties 포함:
     - 제목: 영상 제목
     - 채널: 채널명 (삼프로TV 또는 슈카월드)
     - URL: YouTube 영상 URL
     - 요약: 요약 텍스트
     - 키워드: 매칭된 키워드 목록
     - 게시일: 영상 게시일 (date:{게시일}:start 형식)
     - 처리일: 현재 날짜 (date:{오늘날짜}:start 형식)

4. 저장 성공 시 "Notion에 '{영상 제목}' 저장 완료" 출력

## 사용하는 도구

- Notion MCP `notion-search`: DB 검색
- Notion MCP `notion-create-database`: DB 생성
- Notion MCP `notion-create-pages`: 페이지 생성

## 주의사항

- DB가 이미 존재하면 재생성하지 않고 기존 DB를 사용합니다.
- 날짜 형식은 ISO 8601 (예: 2026-04-09)을 사용합니다.
- notion-create-pages 에서 날짜 속성은 `date:{속성명}:start` 형식으로 전달합니다.
