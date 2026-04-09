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

한국 증시 관련 YouTube 채널의 특정 콘텐츠를 자동 모니터링하여 자막 요약 → Slack 알림 → Notion 저장을 수행합니다.

### 모니터링 대상 채널 및 콘텐츠

| 채널 | 콘텐츠 | 필터 키워드 |
|------|--------|------------|
| 한경글로벌마켓 | 빈난새의 개장전요것만, 김현석의 월스트리트나우 | 개장전요것만, 월스트리트나우 |
| 한국경제TV | 당잠사 | 당잠사 |
| 증시각도기TV | 증시각도기 | 증시각도기 |

### 설정 파일

- `config/channels.json` — 채널, 키워드, Slack/Notion 설정
- `data/processed_videos.json` — 처리 완료된 영상 ID 추적

### 연동 서비스 (확인 완료)

- **Slack**: #경제소식 채널 (MCP `slack_send_message` 사용)
  - 워크스페이스: `theeundol.slack.com`
  - 채널 ID: `C0ARKUFPJJF`
- **Notion**: "증시 유튜브 요약" 데이터베이스 (MCP `notion-create-pages` 사용)
  - DB URL: https://www.notion.so/84678c8444774ef591e75bdf4fdba8db
  - Data Source ID: `460605fe-18f2-4bfe-8534-4f5e265149f0`
  - 스키마: 제목(Title), 채널(Select), 콘텐츠(Select), 요약(Text), URL, 업로드일(Date), 키워드(Multi-select), 처리일시(Created time)

### Claude Code 커스텀 명령어 (`.claude/commands/`)

- `/project:fetch-videos` — YouTube RSS 피드에서 새 영상 감지 및 필터링
- `/project:summarize-video <url>` — 단일 영상 자막 추출 및 요약
- `/project:stock-monitor` — 전체 파이프라인 자동 실행 (감지 → 요약 → Slack → Notion)

### 스케줄 자동화

```
/loop 1h /stock-monitor
```

1시간마다 자동으로 새 영상을 확인하고 처리합니다.

## 세션 시작 시

세션이 시작되면 `.claude/scripts/check-env.sh` 스크립트가 자동 실행되어 환경 정보를 출력합니다:
- 호스트명, OS, CPU, 메모리, 디스크
- Git, Python, Node, mmk 버전
- 원격 환경 여부
