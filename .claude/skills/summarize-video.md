# summarize-video

YouTube 영상의 자막을 가져와 한국 주식시장 관점에서 요약합니다.

## 입력 파라미터

- `video`: `{ video_id, title, video_url, published_at, channel_name }` 객체

## 실행 순서

1. mmk CLI로 자막을 가져옵니다:
   ```bash
   mmk youtube transcript <video_url>
   ```

2. 자막 가져오기 결과 처리:
   - 성공 (자막 텍스트 반환): 3단계로 진행
   - 실패 (오류 또는 빈 결과): `transcript_available: false`로 설정하고 4단계로 이동

3. 자막이 있는 경우 — Claude가 직접 요약합니다:
   - 한국 주식/증시 채널 영상임을 고려하여 투자자 관점에서 분석
   - 다음 내용을 중심으로 핵심 포인트 추출:
     - 주요 종목 및 지수 언급
     - 거시경제 이슈 (금리, 환율, 글로벌 시장 등)
     - 시장 전망 및 매매 전략
     - 특이 이슈나 주목할 뉴스
   - 불릿 포인트 3~5개로 구성, 한국어로 작성
   - 각 포인트는 50자 이내로 간결하게

4. 자막이 없는 경우: 제목 기반으로 간단한 메모 생성
   - 예: "• 자막 없음 — 제목: <title>"

5. 다음 구조의 객체를 반환합니다:
   ```json
   {
     "video_id": "VIDEO_ID",
     "title": "영상 제목",
     "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
     "channel_name": "채널명",
     "published_at": "2026-04-09T07:00:00Z",
     "summary": "• 요약 포인트 1\n• 요약 포인트 2\n• 요약 포인트 3",
     "transcript_available": true,
     "summarized_at": "<현재 시각 ISO 8601>"
   }
   ```

## 주의사항

- 요약 전체 길이는 500자 이내로 제한
- 민감한 투자 조언(특정 종목 매수/매도 권고)은 그대로 요약하되 "요약 내용입니다" 형태로 중립적으로 표현
