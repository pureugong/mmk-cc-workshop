---
name: save-notion-insight
description: 생성된 교육 인사이트를 Notion 데이터베이스에 저장합니다. notion-create-pages MCP 도구를 사용합니다.
---

# save-notion-insight

생성된 교육 인사이트를 Notion 데이터베이스에 저장하는 스킬입니다.

## 설정

- **Data Source ID**: `d63781b2-859b-4f27-b213-9d48bc1e5c46`
- **Database**: 일일 교육 인사이트
- **Parent Page**: 교육 인사이트 허브 (`33db50b9-e469-8191-affb-fcb84d85bb36`)

## 실행 방법

1. `notion-create-pages` MCP 도구를 사용합니다.
2. `parent`에 `data_source_id`를 지정합니다.
3. 아래 스키마에 맞춰 properties를 설정합니다.

## 데이터베이스 스키마

```sql
CREATE TABLE (
  "제목" TITLE,           -- 인사이트 제목 (예: "2026년 교육과정 개편 방향")
  "날짜" DATE,            -- 오늘 날짜 (ISO-8601: "2026-04-09")
  "교육방향" RICH_TEXT,    -- 교육 방향 인사이트 내용
  "학부모/학생 관점" RICH_TEXT, -- 학부모/학생 관점 인사이트
  "선생님 관점" RICH_TEXT,  -- 선생님 관점 인사이트
  "출처" URL,             -- 출처 URL
  "카테고리" SELECT,       -- 정책/트렌드/입시/교육과정/교육환경
  "상태" STATUS           -- 시작 전/진행 중/완료
)
```

## 페이지 생성 예시

```json
{
  "parent": {
    "type": "data_source_id",
    "data_source_id": "d63781b2-859b-4f27-b213-9d48bc1e5c46"
  },
  "pages": [{
    "properties": {
      "제목": "인사이트 제목",
      "date:날짜:start": "2026-04-09",
      "교육방향": "교육 방향 인사이트 내용...",
      "학부모/학생 관점": "학부모/학생 관점 내용...",
      "선생님 관점": "선생님 관점 내용...",
      "출처": "https://example.com/article",
      "카테고리": "트렌드",
      "상태": "완료"
    },
    "content": "## 교육의 방향\n\n내용...\n\n## 학부모/학생 관점\n\n내용...\n\n## 선생님 관점\n\n내용..."
  }]
}
```

## 주의사항

- 날짜 필드는 반드시 `date:날짜:start` 형식으로 expanded property 사용
- 카테고리는 정해진 값 중 하나만 선택: 정책, 트렌드, 입시, 교육과정, 교육환경
- 상태는 저장 완료 시 "완료"로 설정
