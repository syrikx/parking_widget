# Changelog 자동 생성 가이드

parking_widget 프로젝트에서는 모든 코드 변경사항이 자동으로 기록됩니다.

## 🤖 자동 기록 (추천)

### Git 커밋 시 자동 생성

Git hook이 설치되어 있어서 **커밋할 때마다 자동으로 changelog가 생성**됩니다.

```bash
# 평소처럼 파일을 수정하고 커밋만 하면 됩니다
git add .
git commit -m "위젯 크기 변경"

# 커밋 후 자동으로 changelog가 생성됩니다!
# → reviews/YYYYMMDD_HHMMSS.md 파일 생성됨
```

**신경 쓸 필요 없이 평소처럼 커밋만 하면 됩니다!** ✨

### 수동으로 현재 변경사항 기록

커밋하기 전에 현재 변경사항만 먼저 기록하고 싶다면:

```bash
python3 auto_changelog.py "변경 이유 설명"
```

## 📝 수동 기록 (세밀한 제어가 필요한 경우)

특정 파일의 변경사항을 더 자세히 기록하고 싶다면 Python 스크립트 작성:

```python
from code_changelog_tracker import CodeChangeLogger

logger = CodeChangeLogger(
    "프로젝트명 - 기능명",
    user_request="사용자 요구사항"
)

logger.log_file_modification(
    "파일경로",
    "이전 코드",
    "새 코드",
    "변경 이유"
)

logger.save_and_build()
```

## 🌐 Changelog 확인

### 로컬에서 확인
```bash
# 서버가 이미 실행 중입니다
http://localhost:4000
```

### 외부에서 확인
```bash
http://158.247.250.40:8888
```

## 📂 생성된 파일 위치

```
reviews/
├── index.html              # 웹 뷰어
├── README.md               # 홈페이지
├── SUMMARY.md              # 목차
├── 20251110_153635.md      # 변경 이력 1
├── 20251110_161358.md      # 변경 이력 2
└── ...                     # 자동으로 계속 추가됨
```

## 🔧 서버 관리

### 서버 상태 확인
```bash
# 로컬 서버
lsof -ti:4000 && echo "✅ 작동 중" || echo "❌ 중지됨"

# SSH 터널
ps aux | grep "ssh.*8888:localhost:4000" | grep -v grep
```

### 서버 재시작
```bash
# 로컬 서버 재시작
lsof -ti:4000 | xargs kill -9
cd reviews && python3 -m http.server 4000 &

# SSH 터널 재시작
ps aux | grep "ssh.*8888:localhost:4000" | grep -v grep | awk '{print $2}' | xargs kill
ssh -f -N -R 8888:localhost:4000 -p 26320 -i ~/.ssh/id_ed25519 syrikx0@158.247.250.40
```

## ❓ FAQ

### Q: 커밋할 때마다 자동으로 기록되나요?
**A: 네!** Git post-commit hook이 설치되어 있어서 자동으로 기록됩니다.

### Q: 특정 파일만 제외하고 싶어요
**A:** auto_changelog.py 파일에서 제외 조건을 추가하세요:
```python
# 이미 reviews/, __pycache__, build/ 등은 자동 제외됩니다
if any(x in filepath for x in ['test/', 'temp/']):
    continue
```

### Q: Hook을 비활성화하고 싶어요
**A:**
```bash
# Hook 삭제
rm .git/hooks/post-commit

# 또는 임시 비활성화
mv .git/hooks/post-commit .git/hooks/post-commit.disabled
```

### Q: Changelog가 생성되지 않아요
**A:**
1. auto_changelog.py가 있는지 확인
2. Python3가 설치되어 있는지 확인
3. 수동으로 실행해보기: `python3 auto_changelog.py "테스트"`

---

**간단 요약: 평소처럼 git commit만 하면 자동으로 changelog가 생성됩니다!** 🎉
