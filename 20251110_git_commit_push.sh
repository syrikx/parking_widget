#!/bin/bash
# 변경사항 커밋 및 GitHub push

echo "변경사항 스테이징 중..."
git add -A

echo ""
echo "커밋 생성 중..."
git commit -m "$(cat <<'EOF'
위젯 크기 최적화 및 빌드 스크립트 추가

Android와 iOS 위젯의 최소 크기를 조정하여 더 작은 위젯 크기를 지원하도록 개선했습니다.
또한 빌드 자동화를 위한 스크립트와 changelog 관리 도구를 추가했습니다.

주요 변경사항:
- Android 위젯 최소 크기 40dp로 축소
- iOS 위젯 크기별 반응형 레이아웃 구현
- Flutter 빌드 자동화 스크립트 추가
- Changelog 자동 관리 시스템 추가

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

echo ""
echo "GitHub에 push 중..."
git push origin main

echo ""
echo "완료!"
git status
