# 증시 유튜브 모니터링 전체 파이프라인

한국 증시 관련 유튜브 채널을 모니터링하여 새 영상의 자막을 추출, 요약하고 Slack 알림 + Notion DB 저장을 수행하는 오케스트레이터입니다.

## 자동화 사용법

```
/loop 60m /stock-monitor
```

위 명령으로 1시간 간격 자동 실행이 가능합니다.

## 실행 절차

### Phase 1: 새 영상 스캔
1. `config/stock-monitor.json` 설정 파일을 읽습니다.
2. `python3 .claude/scripts/fetch-rss.py all` 을 실행하여 모든 채널의 RSS 피드에서 필터링된 새 영상 목록을 가져옵니다.
3. 각 영상에 대해 `mmk youtube videotype <url>` 을 실행하여 Shorts를 제외합니다.
4. 새 영상이 없으면 "새 영상 없음"을 출력하고 종료합니다.

### Phase 2: 자막 추출 및 요약
5. 각 신규 영상에 대해:
   a. `mmk youtube metadata <url>` 로 메타데이터를 조회합니다.
   b. `mmk youtube transcript <url>` 로 자막을 추출합니다.
   c. 자막 내용을 아래 구조로 요약합니다:
      - 한줄 요약
      - 핵심 포인트 (3-5개)
      - 언급 종목/지수
      - 시장 전망
      - 키워드 태그

### Phase 3: Slack 알림
6. 각 요약에 대해 `config/stock-monitor.json`의 `slack_channel`에 해당하는 Slack 채널을 찾습니다.
7. Slack MCP `slack_send_message`로 요약 메시지를 발송합니다.
8. 메시지 형식:
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
*언급 종목:* 삼성전자, SK하이닉스
*키워드:* #코스피 #반도체
<YouTube URL>
```

### Phase 4: Notion 저장
9. `config/stock-monitor.json`의 `notion_db_id`로 Notion 데이터베이스를 확인합니다.
10. Notion MCP `notion-create-pages`로 각 영상의 요약을 저장합니다.
    - 속성: 제목, 채널(select), URL, 요약(rich_text), 키워드(multi_select), 게시일, 처리일
    - 본문: 전체 요약을 마크다운으로 작성

### Phase 5: 이력 업데이트
11. 처리 완료된 영상 ID를 `data/processed-videos.json`에 추가합니다.
12. `last_scan` 타임스탬프를 현재 시간으로 업데이트합니다.
13. processed 목록이 500개를 초과하면 오래된 것부터 제거합니다.

## 최종 출력

처리 결과를 요약하여 출력합니다:
- 스캔한 채널 수
- 발견된 새 영상 수
- 요약 완료된 영상 수
- Slack 알림 발송 수
- Notion 저장 수

## 참고

- 각 Phase에서 오류가 발생하면 해당 영상을 건너뛰고 다음 영상을 처리합니다.
- 모든 처리가 완료된 후 한 번에 `processed-videos.json`을 업데이트합니다.
