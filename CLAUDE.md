# Claude Code 워크샵 스타터

강의 실습용 Claude Code 워크샵 스타터 프로젝트입니다.

## 프로젝트 목적

이 프로젝트를 fork하여 Claude Code 웹에서 바로 자동화 바이브 코딩을 시작할 수 있습니다.

## mmk CLI

mmk (Magic Meal Kits)는 YouTube 자막 추출, 메타데이터 조회 등을 지원하는 CLI 도구입니다.

**중요: 현재 토큰은 YouTube 전용입니다. `mmk youtube` 명령어만 사용하세요.**
`mmk notion`, `mmk paymint` 등 다른 명령어는 권한이 없어 실패합니다 (403 insufficient_scope).

### 설정

```bash
export MMK_SERVER="https://magic-meal-kits-r7fpfharja-uw.a.run.app"
export MMK_TOKEN="<강사가 제공한 토큰>"
```

### 사용 가능한 명령어

```bash
# YouTube 자막 추출
mmk youtube transcript <youtube-url>
mmk youtube transcript <youtube-url> --format json
mmk youtube transcript <youtube-url> --format srt

# YouTube 메타데이터 조회
mmk youtube metadata <youtube-url>

# YouTube 영상 타입 확인 (일반 영상 vs Short)
mmk youtube videotype <youtube-url>
```

### 사용 불가 명령어 (토큰 권한 없음)

- `mmk notion ...` — 사용 불가
- `mmk paymint ...` — 사용 불가
- `mmk threads ...` — 사용 불가

## 증시 유튜브 모니터링 자동화

한국 증시 관련 유튜브 채널을 자동 모니터링하여 자막 추출 → 요약 → Slack 알림 + Notion 저장하는 시스템입니다.

### 커스텀 슬래시 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/youtube-scan` | RSS 피드에서 새 영상 탐색 및 필터링 |
| `/youtube-summarize <url>` | 영상 자막 추출 및 AI 요약 |
| `/notify-slack` | 요약 내용을 Slack 채널에 알림 발송 |
| `/save-notion` | 요약 내용을 Notion DB에 저장 |
| `/stock-monitor` | 전체 파이프라인 오케스트레이터 (위 4개 통합) |

### 1시간 자동화

```
/loop 60m /stock-monitor
```

### 설정 파일

- `config/stock-monitor.json` — 채널 목록, 필터 키워드, Slack/Notion 설정
- `data/processed-videos.json` — 처리 완료 영상 ID 추적 (중복 방지)

### 모니터링 대상 채널

- **한경글로벌마켓**: 개장전요것만, 월스트리트나우
- **한국경제TV**: 당잠사
- **증시각도기TV**: 미국시황, 한국시황, 증시각도기

### Notion DB

- DB명: "증시 유튜브 요약"
- 속성: 제목, 채널(select), URL, 요약, 키워드(multi_select), 게시일, 처리일
- Notion MCP `notion-create-pages` 사용

### Slack 알림

- Slack MCP `slack_send_message` 사용
- 채널명은 `config/stock-monitor.json`의 `slack_channel`에서 설정
- **주의**: Slack에서 채널을 먼저 생성한 후 채널명을 설정 파일에 입력해야 합니다

## 세션 시작 시

세션이 시작되면 `.claude/scripts/check-env.sh` 스크립트가 자동 실행되어 환경 정보를 출력합니다:
- 호스트명, OS, CPU, 메모리, 디스크
- Git, Python, Node, mmk 버전
- 원격 환경 여부
