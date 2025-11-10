#!/usr/bin/env python3
"""
자동 Changelog 생성기
Git의 변경사항을 감지하여 자동으로 changelog를 생성합니다.
"""

import subprocess
import sys
from datetime import datetime
from code_changelog_tracker import CodeChangeLogger


def get_git_diff():
    """Git diff를 가져옵니다 (staged + unstaged)"""
    try:
        # Staged changes
        staged = subprocess.run(
            ['git', 'diff', '--cached', '--name-status'],
            capture_output=True,
            text=True,
            check=True
        )

        # Unstaged changes
        unstaged = subprocess.run(
            ['git', 'diff', '--name-status'],
            capture_output=True,
            text=True,
            check=True
        )

        return staged.stdout + unstaged.stdout
    except subprocess.CalledProcessError:
        return ""


def get_file_diff(filepath, staged=False):
    """특정 파일의 diff를 가져옵니다"""
    try:
        cmd = ['git', 'diff']
        if staged:
            cmd.append('--cached')
        cmd.append(filepath)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def get_last_commit_message():
    """마지막 커밋 메시지를 가져옵니다"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "변경사항"


def parse_diff_and_log(commit_message=""):
    """Git diff를 분석하여 changelog에 기록"""

    diff_output = get_git_diff()
    if not diff_output:
        print("변경된 파일이 없습니다.")
        return False

    # 프로젝트명 추출 (현재 디렉토리 이름)
    import os
    project_name = os.path.basename(os.getcwd())

    # 커밋 메시지가 없으면 마지막 커밋 메시지 사용
    if not commit_message:
        commit_message = get_last_commit_message()

    # Logger 생성
    logger = CodeChangeLogger(
        f"{project_name} - 자동 변경 기록",
        user_request=commit_message
    )

    # 변경된 파일 분석
    changes_logged = False
    for line in diff_output.strip().split('\n'):
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) < 2:
            continue

        status = parts[0]
        filepath = parts[1]

        # reviews 폴더는 제외
        if filepath.startswith('reviews/'):
            continue

        # Python 캐시, 빌드 파일 등 제외
        if any(x in filepath for x in ['__pycache__', '.pyc', 'build/', '.git/', 'node_modules/']):
            continue

        try:
            if status.startswith('A'):
                # 새 파일 추가
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                logger.log_file_creation(
                    filepath,
                    content[:500],  # 처음 500자만
                    f"새 파일 추가: {commit_message}"
                )
                changes_logged = True
                print(f"  [추가] {filepath}")

            elif status.startswith('M'):
                # 파일 수정
                diff = get_file_diff(filepath)
                logger.log_file_modification(
                    filepath,
                    "이전 버전 (git diff 참조)",
                    "새 버전 (git diff 참조)",
                    f"파일 수정: {commit_message}"
                )
                changes_logged = True
                print(f"  [수정] {filepath}")

            elif status.startswith('D'):
                # 파일 삭제
                logger.log_file_deletion(
                    filepath,
                    "삭제된 파일",
                    f"파일 삭제: {commit_message}"
                )
                changes_logged = True
                print(f"  [삭제] {filepath}")

        except Exception as e:
            print(f"  경고: {filepath} 처리 중 오류: {e}")
            continue

    # 변경사항 저장
    if changes_logged:
        logger.save_and_build()
        return True
    else:
        print("기록할 변경사항이 없습니다.")
        return False


def main():
    """메인 함수"""
    print("=" * 60)
    print("🤖 자동 Changelog 생성기")
    print("=" * 60)
    print()

    # 커밋 메시지 인자로 받기
    commit_message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    if not commit_message:
        print("커밋 메시지를 입력하세요 (Enter로 건너뛰면 마지막 커밋 메시지 사용):")
        commit_message = input("> ").strip()

    print("\n📝 변경된 파일:")
    success = parse_diff_and_log(commit_message)

    if success:
        print("\n" + "=" * 60)
        print("✅ Changelog가 자동으로 생성되었습니다!")
        print("=" * 60)
        print("\n🌐 확인: http://localhost:4000")
        print("🌐 외부: http://158.247.250.40:8888")
    else:
        print("\n변경사항이 없어 changelog를 생성하지 않았습니다.")


if __name__ == "__main__":
    main()
