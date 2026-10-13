#!/bin/bash
# 세금 노무 매니저 통합 테스트 스크립트
# 실행: bash run_tests.sh
set -e
BASE="C:/AI_산출물/개발/tax-labor-manager"
echo "=== 1. 정적 검증 (Python) ==="
python3 "\/_verify_v2.py"
echo ""
echo "=== 2. 계산 로직 검증 (Node.js) ==="
node "\/_verify_logic.js"
echo ""
echo "=== 3. 브라우저 호환성 검사 ==="
node -e "const fs=require('fs');const html=fs.readFileSync('\$${BASE}/prototype_20261013/index.html','utf8');const checks=[['DOCTYPE 선언',html.includes('<!DOCTYPE html>')],['반응형 viewport',html.includes('viewport')],['상단 면책 고지',html.includes('disclaimer-banner')],['하단 면책 고지',html.includes('disclaimer-footer')],['localStorage 사용',html.includes('localStorage')]];let pass=0;for(const [n,ok] of checks){console.log((ok?'PASS':'FAIL')+' '+n);if(ok)pass++;}console.log(pass+'/'+checks.length+' 통과');if(pass!==checks.length)process.exit(1);"
echo ""
echo "=== 모든 테스트 완료 ==="
