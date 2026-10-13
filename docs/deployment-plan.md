# 세금 노무 매니저 — 배포 계획 (2주차)

## 1. 배포 원칙

- **무료 배포**: 스파크 결정에 따라 "정적 HTML/CSS/JS 단일 파일 및 GitHub Pages 배포 구조로 개발비 0원 원칙을 충실히 준수"하라고 요구함.
- **결제·외부 API는 제외**: PG 결제 연동 및 외부 API 키 발급은 대표이사 결재 후 진행. 현재는 정적 파일 배포만.
- **배포 대상**: GitHub Pages (github.io) 무료 호스팅.

## 2. 배포 파일 구조

```
tax-labor-manager/ (GitHub Repository 루트)
├── index.html          ← 핵심 정적 파일 (42,821B, 단일 파일)
├── README.md           ← 프로젝트 문서
├── docs/
│   ├── payment-design.md   ← 2주차 결제 모듈 설계안
│   └── deployment-plan.md  ← 본 문서
├── .gitignore
└── prototype_20261013/
    └── index.html      ← 1주차 정본 (면책 고지 탑재, 버전 보관용)
```

## 3. GitHub Pages 배포 방법

### 3-1. 사전 준비 (미확인 항목 — 실제 실행 전 검증 필요)

| 항목 | 상태 | 비고 |
|------|------|------|
| GitHub 계정 | 미확인 | 대표이사 본인 계정 또는 10조조직 계정 필요 |
| tax-labor-manager 리포지토리 생성 | 미확인 | Public 권장 (GitHub Pages Free는 Public 리포지토리) |
| GitHub Pages 브랜치 설정 | 미확인 | `main` 브랜치 / 루트 디렉토리 선택 필요 |

> ⚠️ **주의**: 결제 모듈 도입 시점에만 서브도메인/커스텀 도메인 설정 검토. 현재는 `https://<username>.github.io/tax-labor-manager/` 기본 URL 사용.

### 3-2. 배포 명령어 (배포 승인 후 실행)

```bash
# 1. 리포지토리 복제 또는 초기화
git clone https://github.com/<username>/tax-labor-manager.git
cd tax-labor-manager

# 2. 파일 복사 (정적 파일만 배포용 루트에 배치)
cp prototype_20261013/index.html ./index.html

# 3. 커밋 및 푸시
git add .
git commit -m "feat: 1주차 세무 일정 DB + 세금 계산기 + 알림 기능 완료 (면책 고지 포함)"
git push origin main

# 4. GitHub Pages 설정 (웹 UI에서 수행)
# Settings → Pages → Source: main branch / / (root) → Save
```

### 3-3. 배포 후 검증 체크리스트

- [ ] `https://<username>.github.io/tax-labor-manager/` 접속 → 200 OK
- [ ] 브라우저 알림 권한 요청 버튼 정상 동작
- [ ] 부가세/종합소득세 계산기 정상 동작 (5개 계산 항목 모두)
- [ ] 세무 일정 목록 정상 표시 (32개 기본 일정)
- [ ] 법적 면책 고지 상단·하단 고정 확인 (5개 문구)
- [ ] 캘린더(.ics) 내보내기 다운로드 정상 동작
- [ ] 사업자등록번호 입력 없음 확인 (개인정보 최소화)

## 4. 무료 호스팅 대안

| 플랫폼 | 무료 한도 | 장점 | 단점 |
|--------|----------|------|------|
| **GitHub Pages** | ∞(Public 리포지토리) | Git 연동, HTTPS 자동, 도메인-custom 가능 | 정적 파일만, 100MB 리포지토리 제한 |
| Vercel | 100GB/월 | SPA 라우팅, 글로벌 CDN | 정적/SSR 지원, 복잡도↑ |
| Netlify | 100GB/월 | 드롭 배포, 폼 처리 내장 | GitHub Pages보다 복잡 |
| Cloudflare Pages | 500회/일 빌드 | 글로벌 CDN | 빌드 제한 있음 |

**결정**: GitHub Pages 선택 (스파크 "GitHub Pages 배포" 언급, 비용 0원, 정적 파일 최적화)

## 5. 결제 모듈 도입 시 배포 변경 사항 (예정)

결제 모듈 도입 시 (대표이사 결재 후):
- `index.html`에 결제 프록시 서버 호출 코드 추가
- 결제 프록시 서버 (Node.js)는 Vercel 또는 Render Free tier에 배포
- DB는 Supabase (Free tier) 사용
- 기존 GitHub Pages의 `index.html`은 정적 파일로 유지, 결제 API 호출만 추가

> 📌 현재 시점에서는 결제 모듈 설계안(`docs/payment-design.md`)만 작성하고 배포하지 않는다.
