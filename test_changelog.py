#!/usr/bin/env python3
"""Code Changelog 테스트 예제"""

from code_changelog_tracker import CodeChangeLogger

# 테스트 로거 생성
logger = CodeChangeLogger(
    "Parking Widget App - 초기 설정",
    user_request="주차 위치 위젯 앱 Code Changelog 기능 활성화"
)

# 파일 생성 기록
logger.log_file_creation(
    "code_changelog_tracker.py",
    """#!/usr/bin/env python3
\"\"\"Code Changelog Tracker\"\"\"
import os
from datetime import datetime
from pathlib import Path

class CodeChangeLogger:
    def __init__(self, project_name, user_request=""):
        self.project_name = project_name
        ...
""",
    "코드 변경 추적 시스템 구현"
)

# 파일 생성 기록 2
logger.log_file_creation(
    "reviews/README.md",
    "# Parking Widget App - 코드 변경 이력\n\n이 폴더에는 AI가 생성한 모든 코드 변경사항이 기록됩니다.",
    "변경 이력 문서화 폴더 README 생성"
)

# 저장 및 빌드
logger.save_and_build()

print("\n" + "="*60)
print("✅ Code Changelog 기능이 활성화되었습니다!")
print("="*60)
print("\n다음 명령어로 문서 서버를 실행하세요:")
print("  cd reviews")
print("  python3 -m http.server 4000")
print("\n그리고 브라우저에서 다음 주소로 접속:")
print("  http://localhost:4000")
print("="*60)
