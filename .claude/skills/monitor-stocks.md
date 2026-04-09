# /monitor-stocks — 증시 유튜브 모니터링 파이프라인

한국 증시 유튜브 채널의 새 영상을 자동으로 확인 → 자막 추출 → 요약 → Slack 알림 → Notion 저장하는 전체 파이프라인을 실행합니다.

## 실행 절차

### Phase 1: 새 영상 확인

1. `config/channels.json`을 읽어 채널 목록, 키워드, 설정을 로드합니다.
2. `data/processed-videos.json`을 읽어 이미 처리된 영상 ID 목록을 로드합니다.
3. 각 채널에 대해 YouTube RSS 피드를 조회합니다:
   ```bash
   curl -s "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
   ```
4. RSS XML에서 최신 영상들의 videoId, title, published를 추출합니다.
5. 키워드 필터링: 제목에 설정된 키워드(주식, 투자, 시장) 중 하나라도 포함된 영상만 선별합니다.
6. `data/processed-videos.json`에 이미 있는 video ID는 건너뜁니다.

새 영상이 없으면 "새로운 키워드 매칭 영상이 없습니다." 출력 후 종료합니다.

### Phase 2: 각 영상 처리 (새 영상마다 반복)

각 새 영상에 대해 순서대로 수행합니다:

#### A. 자막 추출 + 요약
1. `mmk youtube metadata <url> -o json` 으로 메타데이터를 가져옵니다.
2. `mmk youtube transcript <url> --format json` 으로 자막을 추출합니다.
3. 자막 내용을 분석하여 한국어 3~5문장 핵심 요약을 생성합니다.
4. 핵심 키포인트 3개를 추출합니다.

#### B. Slack 알림 전송
1. Slack MCP `slack_search_channels`로 "general" 채널 ID를 조회합니다.
2. `slack_send_message`로 아래 형식의 알림을 전송합니다:
   ```
   📊 *증시 유튜브 새 영상 알림*

   *{채널명}* — _{영상 제목}_
   📅 게시일: {게시일}

   *요약:*
   {요약 내용}

   *키포인트:*
   • {포인트1}
   • {포인트2}
   • {포인트3}

   🔗 영상 보기: {YouTube URL}
   ```

#### C. Notion 저장
1. Notion MCP `notion-search`로 "증시 유튜브 모니터링" DB를 검색합니다.
2. DB가 없으면 `notion-create-database`로 생성합니다:
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
3. `notion-create-pages`로 영상 정보를 저장합니다.

#### D. 상태 업데이트
1. 처리 완료된 video ID를 `data/processed-videos.json`에 추가합니다.
   - Read로 현재 목록을 읽고, 새 ID를 추가한 JSON을 Write로 저장합니다.

### Phase 3: 완료 보고

모든 영상 처리 후 아래 형식으로 결과를 보고합니다:

```
## 모니터링 완료

- 확인한 채널: {N}개
- 새로 발견된 영상: {N}개
- 키워드 매칭 영상: {N}개
- Slack 알림 전송: {N}건
- Notion 저장: {N}건
```

## 사용하는 도구

- Bash: `curl` (RSS 피드), `mmk youtube metadata/transcript` (자막/메타데이터)
- Read/Write: config, data 파일 읽기/쓰기
- Slack MCP: `slack_search_channels`, `slack_send_message`
- Notion MCP: `notion-search`, `notion-create-database`, `notion-create-pages`

## 스케줄링

이 스킬을 1시간마다 자동 실행하려면:
```
/loop 1h /monitor-stocks
```

## 주의사항

- mmk 서버 타임아웃 시 한 번 재시도합니다.
- 자막이 없는 영상은 건너뛰고 다음 영상으로 진행합니다.
- Slack이나 Notion 전송 실패 시에도 다른 영상 처리는 계속합니다.
- processed-videos.json은 각 영상 처리 완료 직후 즉시 업데이트하여 중복 처리를 방지합니다.
