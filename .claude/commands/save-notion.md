# /save-notion — Notion 데이터베이스에 영상 요약 저장

요약된 영상 정보를 Notion 데이터베이스에 저장합니다.

## 인자

$ARGUMENTS — 저장할 영상 정보 (없으면 직전에 생성한 요약을 사용)

## 실행 절차

### 1단계: 데이터베이스 확인/생성

1. Notion MCP `notion-search` 도구로 "YouTube 영상 요약" 데이터베이스를 검색합니다.
   - 검색 쿼리: "YouTube 영상 요약"

2. 데이터베이스가 **없으면** `notion-create-database` 도구로 새로 생성합니다:
   - 제목: "YouTube 영상 요약"
   - 스키마 (SQL DDL):
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
   - parent: 사용자의 Notion 워크스페이스 (검색으로 적절한 부모 페이지 확인)

3. 데이터베이스가 **있으면** 해당 데이터베이스 ID를 사용합니다.

### 2단계: 페이지 생성

`notion-create-pages` 도구로 영상 데이터를 저장합니다:

- **properties**:
  - 제목: 영상 제목
  - 채널: 채널명
  - URL: 영상 URL
  - 한줄 요약: 한줄 요약 텍스트
  - 키워드: 키워드 (쉼표 구분)
  - 게시일: 영상 게시일
  - 처리일: 오늘 날짜
  - 상태: "완료"

- **content** (페이지 본문): 전체 요약 내용 (주요 내용 bullet points 포함)

## 주의사항
- 데이터베이스 생성 시 부모 페이지를 찾지 못하면 사용자에게 Notion 페이지 URL을 요청합니다.
- 이미 동일한 URL의 영상이 저장되어 있으면 중복 저장하지 않습니다.
