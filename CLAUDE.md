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

## 커스텀 슬래시 커맨드

YouTube 채널 모니터링 자동화를 위한 커맨드들입니다.

| 커맨드 | 설명 |
|--------|------|
| `/fetch-videos` | 등록된 채널의 새 영상 감지 |
| `/summarize-video <url>` | 영상 자막 추출 + 한국어 요약 |
| `/notify-slack` | 요약을 Slack `#youtube-summary`에 전송 |
| `/save-notion` | 요약을 Notion DB에 저장 |
| `/monitor` | 전체 파이프라인 (감지→요약→Slack→Notion) |

### 스케줄링

매일 자동 실행: `/loop 24h /monitor`

### 설정

- 채널 목록: `config/channels.json`
- 처리 상태: `data/processed_videos.json`

### MCP 의존성

- **Slack MCP**: `#youtube-summary` 채널에 알림 전송
- **Notion MCP**: "YouTube 영상 요약" 데이터베이스에 저장

## 세션 시작 시

세션이 시작되면 `.claude/scripts/check-env.sh` 스크립트가 자동 실행되어 환경 정보를 출력합니다:
- 호스트명, OS, CPU, 메모리, 디스크
- Git, Python, Node, mmk 버전
- 원격 환경 여부
