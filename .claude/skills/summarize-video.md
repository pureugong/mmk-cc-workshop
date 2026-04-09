# /summarize-video — 자막 추출 + 요약

YouTube 영상의 자막을 추출하고 핵심 내용을 한국어로 요약합니다.

## 인자

- `$ARGUMENTS`: YouTube 영상 URL (예: `https://www.youtube.com/watch?v=VIDEO_ID`)

인자가 없으면 사용자에게 영상 URL을 요청합니다.

## 실행 절차

1. 전달받은 YouTube URL로 `mmk youtube metadata` 를 실행하여 영상 제목, 채널명, 게시일 등 메타데이터를 가져옵니다:
   ```bash
   mmk youtube metadata <url> -o json
   ```

2. `mmk youtube transcript` 로 자막을 추출합니다:
   ```bash
   mmk youtube transcript <url> --format json
   ```

3. 추출된 자막 텍스트를 분석하여 **한국어 핵심 요약**을 생성합니다:
   - 3~5문장으로 핵심 내용 요약
   - 증시/투자 관련 핵심 포인트 강조
   - 언급된 종목, 지표, 전망 등 구체적 정보 포함

4. 결과를 아래 구조화된 형식으로 출력합니다:

```
## 영상 요약

- **제목**: {영상 제목}
- **채널**: {채널명}
- **게시일**: {게시일}
- **URL**: {영상 URL}

### 요약
{3-5문장 핵심 요약}

### 키포인트
- {핵심 포인트 1}
- {핵심 포인트 2}
- {핵심 포인트 3}
```

## 사용하는 도구

- Bash: `mmk youtube metadata`, `mmk youtube transcript` 실행

## 주의사항

- 자막이 없는 영상은 "자막을 추출할 수 없습니다"라고 보고합니다.
- 자막이 매우 긴 경우(1시간 이상 영상), 앞부분 위주로 요약합니다.
- mmk 서버 타임아웃 시 한 번 재시도합니다.
