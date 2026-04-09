# /stock-monitor - 증시 유튜브 모니터링 자동화

한국 증시 관련 YouTube 채널을 모니터링하여 새 영상을 감지하고, 자막 추출 → 요약 → Slack 알림 → Notion 저장까지 자동으로 수행합니다.

## 스케줄 실행

이 스킬은 `/loop 1h /stock-monitor` 명령으로 1시간마다 자동 실행할 수 있습니다.

## 실행 절차

### 1단계: 설정 로드

`config/channels.json` 파일을 읽어 전체 설정을 로드합니다:
- 채널 목록 및 RSS URL
- 콘텐츠 필터 (채널별 특정 프로그램명)
- 키워드 목록
- Slack 채널 ID: `C0ARKUFPJJF` (#경제소식)
- Notion data_source_id: `460605fe-18f2-4bfe-8534-4f5e265149f0`

### 2단계: 새 영상 감지 (RSS 피드)

각 채널의 RSS 피드를 WebFetch로 **병렬** 가져오기:
- `https://www.youtube.com/feeds/videos.xml?channel_id=UCWskYkV4c4S9D__rsfOl2JA` (한경글로벌마켓)
- `https://www.youtube.com/feeds/videos.xml?channel_id=UCF8AeLlUbEpKju6v1H6p8Eg` (한국경제TV)
- `https://www.youtube.com/feeds/videos.xml?channel_id=UCdOjVxkj5JA0iDu3_xcsTyQ` (증시각도기TV)

각 `<entry>`에서 `<yt:videoId>`, `<title>`, `<published>`, `<link>` 추출.

### 3단계: 필터링

**콘텐츠 필터** (주 필터 - 제목에 포함 여부):
- 한경글로벌마켓 → "개장전요것만" 또는 "월스트리트나우"
- 한국경제TV → "당잠사"
- 증시각도기TV → "증시각도기"

**중복 체크**: `data/processed_videos.json`에서 이미 처리된 video ID 제외.

**키워드 매칭**: 제목에서 `["증시", "전망", "시황", "경제", "금리", "환율", "물가", "기준금리"]` 매칭 → 태그용.

새 영상이 없으면 "새로운 영상이 없습니다. 다음 체크 시간에 다시 확인합니다."라고 출력하고 종료.

### 4단계: 자막 추출 및 요약 (영상별)

각 새 영상에 대해:

1. **자막 추출**:
   ```bash
   mmk youtube transcript <youtube-url>
   ```

2. **요약 생성** (아래 형식):
   ```
   ## 📊 [영상 제목]
   **채널**: [채널명] | **날짜**: [업로드일]

   ### 핵심 요약
   - (3~5줄 핵심 내용)

   ### 주요 포인트
   1. ...
   2. ...

   ### 언급된 종목/지표
   - 종목, 지수, 경제 지표 리스트

   ### 투자 시사점
   - 시사점 1~2줄
   ```

   요약 원칙: 한국어, 수치 구체적 포함, 전문 용어 유지, 영상 내용 기반만.

### 5단계: Slack 알림 전송

Slack MCP 도구 `slack_send_message`를 사용하여 `#경제소식` (C0ARKUFPJJF) 채널에 전송합니다.

**메시지 형식**:
```
📺 *증시 유튜브 새 영상 요약*

*[채널명] - [콘텐츠]*
> [영상 제목]
> [업로드일]

*핵심 요약*
- ...

*주요 포인트*
1. ...

*언급된 종목/지표*: ...

🔗 [영상 보기](youtube-url)
```

여러 영상이 있으면 각각 별도 메시지로 전송합니다.

### 6단계: Notion 저장

Notion MCP 도구 `notion-create-pages`를 사용하여 저장합니다.

**parent**: `{"type": "data_source_id", "data_source_id": "460605fe-18f2-4bfe-8534-4f5e265149f0"}`

**properties**:
- `제목`: 영상 제목
- `채널`: 채널명 (한경글로벌마켓 / 한국경제TV / 증시각도기TV)
- `콘텐츠`: 콘텐츠명 (개장전요것만 / 월스트리트나우 / 당잠사 / 증시각도기)
- `요약`: 핵심 요약 텍스트 (간략 버전)
- `userDefined:URL`: YouTube URL
- `date:업로드일:start`: 업로드 날짜 (ISO-8601)
- `키워드`: 매칭된 키워드 JSON 배열

**content**: 전체 요약 내용 (마크다운)

### 7단계: 처리 완료 기록

`data/processed_videos.json` 파일을 업데이트합니다:
- `processed` 배열에 처리된 video ID 추가 (최대 200개 유지, 오래된 것부터 제거)
- `last_checked`를 현재 시각(ISO-8601)으로 업데이트

### 8단계: 완료 보고

처리 결과를 사용자에게 요약 보고합니다:
```
✅ 증시 유튜브 모니터링 완료
- 확인된 채널: 3개
- 새 영상 발견: N건
- 요약 완료: N건
- Slack 전송: ✅
- Notion 저장: ✅
- 다음 체크: /loop 1h /stock-monitor
```
