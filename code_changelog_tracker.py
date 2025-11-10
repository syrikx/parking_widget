#!/usr/bin/env python3
"""
Code Changelog Tracker
AI가 생성한 모든 코드 변경사항을 reviews 폴더에 기록하고 HTML 뷰어로 확인
"""

import os
import glob
from datetime import datetime
from pathlib import Path


class CodeChangeLogger:
    """코드 변경사항을 추적하고 문서화하는 로거"""

    def __init__(self, project_name, user_request="", reviews_dir="reviews", port=4000):
        """
        Args:
            project_name: 프로젝트 이름
            user_request: 사용자 요구사항
            reviews_dir: 문서 저장 디렉토리
            port: HTTP 서버 포트
        """
        self.project_name = project_name
        self.user_request = user_request
        self.reviews_dir = Path(reviews_dir)
        self.port = port
        self.changes = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # reviews 폴더 생성
        self.reviews_dir.mkdir(exist_ok=True)

    def log_file_creation(self, file_path, content, reason):
        """파일 생성 기록"""
        self.changes.append({
            "type": "creation",
            "file_path": file_path,
            "content": content,
            "reason": reason
        })

    def log_file_modification(self, file_path, old_content, new_content, reason):
        """파일 수정 기록"""
        self.changes.append({
            "type": "modification",
            "file_path": file_path,
            "old_content": old_content,
            "new_content": new_content,
            "reason": reason
        })

    def log_file_deletion(self, file_path, content, reason):
        """파일 삭제 기록"""
        self.changes.append({
            "type": "deletion",
            "file_path": file_path,
            "content": content,
            "reason": reason
        })

    def log_bug_fix(self, file_path, old_content, new_content, bug_desc, fix_desc):
        """버그 수정 기록"""
        self.changes.append({
            "type": "bug_fix",
            "file_path": file_path,
            "old_content": old_content,
            "new_content": new_content,
            "bug_desc": bug_desc,
            "fix_desc": fix_desc
        })

    def log_refactoring(self, file_path, old_content, new_content, refactor_type, reason):
        """리팩토링 기록"""
        self.changes.append({
            "type": "refactoring",
            "file_path": file_path,
            "old_content": old_content,
            "new_content": new_content,
            "refactor_type": refactor_type,
            "reason": reason
        })

    def _generate_markdown(self):
        """변경사항을 마크다운 형식으로 생성"""
        md_lines = []

        # 헤더
        md_lines.append(f"# {self.project_name}")
        md_lines.append("")
        md_lines.append(f"**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append("")

        if self.user_request:
            md_lines.append("## 요구사항")
            md_lines.append("")
            md_lines.append(self.user_request)
            md_lines.append("")

        # 변경사항 요약
        md_lines.append("## 변경 요약")
        md_lines.append("")
        creation_count = sum(1 for c in self.changes if c["type"] == "creation")
        modification_count = sum(1 for c in self.changes if c["type"] == "modification")
        deletion_count = sum(1 for c in self.changes if c["type"] == "deletion")

        md_lines.append(f"- 파일 생성: {creation_count}개")
        md_lines.append(f"- 파일 수정: {modification_count}개")
        md_lines.append(f"- 파일 삭제: {deletion_count}개")
        md_lines.append("")

        # 상세 변경사항
        md_lines.append("## 상세 변경사항")
        md_lines.append("")

        for idx, change in enumerate(self.changes, 1):
            change_type = change["type"]
            file_path = change["file_path"]

            md_lines.append(f"### {idx}. {file_path}")
            md_lines.append("")

            if change_type == "creation":
                md_lines.append(f"**작업**: 파일 생성")
                md_lines.append(f"**이유**: {change['reason']}")
                md_lines.append("")
                md_lines.append("```")
                md_lines.append(change["content"][:500] + ("..." if len(change["content"]) > 500 else ""))
                md_lines.append("```")
                md_lines.append("")

            elif change_type == "modification":
                md_lines.append(f"**작업**: 파일 수정")
                md_lines.append(f"**이유**: {change['reason']}")
                md_lines.append("")
                md_lines.append("**변경 전:**")
                md_lines.append("```")
                md_lines.append(change["old_content"][:300] + ("..." if len(change["old_content"]) > 300 else ""))
                md_lines.append("```")
                md_lines.append("")
                md_lines.append("**변경 후:**")
                md_lines.append("```")
                md_lines.append(change["new_content"][:300] + ("..." if len(change["new_content"]) > 300 else ""))
                md_lines.append("```")
                md_lines.append("")

            elif change_type == "deletion":
                md_lines.append(f"**작업**: 파일 삭제")
                md_lines.append(f"**이유**: {change['reason']}")
                md_lines.append("")

            elif change_type == "bug_fix":
                md_lines.append(f"**작업**: 버그 수정")
                md_lines.append(f"**버그 설명**: {change['bug_desc']}")
                md_lines.append(f"**수정 내용**: {change['fix_desc']}")
                md_lines.append("")

            elif change_type == "refactoring":
                md_lines.append(f"**작업**: 리팩토링 ({change['refactor_type']})")
                md_lines.append(f"**이유**: {change['reason']}")
                md_lines.append("")

        return "\n".join(md_lines)

    def _update_summary(self):
        """SUMMARY.md 업데이트"""
        summary_path = self.reviews_dir / "SUMMARY.md"

        # 모든 마크다운 파일 찾기 (README 제외)
        md_files = sorted(
            [f for f in self.reviews_dir.glob("*.md")
             if f.name not in ["README.md", "SUMMARY.md"]],
            reverse=True  # 최신 파일이 위로
        )

        summary_lines = ["# 변경 이력", ""]

        for md_file in md_files:
            # 타임스탬프 파싱
            filename = md_file.stem
            try:
                dt = datetime.strptime(filename, "%Y%m%d_%H%M%S")
                display_name = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                display_name = filename

            summary_lines.append(f"- [{display_name}]({md_file.name})")

        summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    def _update_index_html(self):
        """index.html 생성 또는 업데이트"""
        index_path = self.reviews_dir / "index.html"

        # 모든 마크다운 파일 찾기 (최신순)
        md_files = sorted(
            [f for f in self.reviews_dir.glob("*.md")
             if f.name not in ["SUMMARY.md"]],
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )

        # 파일 목록을 JavaScript 배열로 변환
        file_list = []
        for md_file in md_files:
            filename = md_file.name
            try:
                if filename == "README.md":
                    display_name = "홈"
                else:
                    dt = datetime.strptime(md_file.stem, "%Y%m%d_%H%M%S")
                    display_name = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                display_name = md_file.stem

            file_list.append(f'{{file: "{filename}", name: "{display_name}"}}')

        files_js = "[" + ", ".join(file_list) + "]"

        # 기본 파일 설정 (최신 파일 또는 README.md)
        default_file = md_files[0].name if md_files else "README.md"

        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>코드 변경 이력</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}

        #sidebar {{
            width: 280px;
            background: #161b22;
            border-right: 1px solid #30363d;
            overflow-y: auto;
            padding: 20px;
        }}

        #sidebar h2 {{
            color: #58a6ff;
            margin-bottom: 20px;
            font-size: 18px;
        }}

        #file-list {{
            list-style: none;
        }}

        #file-list li {{
            margin-bottom: 8px;
        }}

        #file-list a {{
            color: #8b949e;
            text-decoration: none;
            display: block;
            padding: 8px 12px;
            border-radius: 6px;
            transition: all 0.2s;
            font-size: 14px;
        }}

        #file-list a:hover {{
            background: #21262d;
            color: #58a6ff;
        }}

        #file-list a.active {{
            background: #1f6feb;
            color: #ffffff;
        }}

        #content {{
            flex: 1;
            overflow-y: auto;
            padding: 40px;
        }}

        #markdown-content {{
            max-width: 900px;
            margin: 0 auto;
        }}

        #markdown-content h1 {{
            color: #f0f6fc;
            border-bottom: 1px solid #30363d;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}

        #markdown-content h2 {{
            color: #58a6ff;
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        #markdown-content h3 {{
            color: #79c0ff;
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        #markdown-content p {{
            line-height: 1.7;
            margin-bottom: 15px;
        }}

        #markdown-content ul, #markdown-content ol {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}

        #markdown-content li {{
            line-height: 1.7;
            margin-bottom: 5px;
        }}

        #markdown-content code {{
            background: #161b22;
            padding: 3px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            color: #ff7b72;
        }}

        #markdown-content pre {{
            background: #161b22;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            margin-bottom: 15px;
            border: 1px solid #30363d;
        }}

        #markdown-content pre code {{
            background: none;
            padding: 0;
            color: #c9d1d9;
        }}

        #markdown-content strong {{
            color: #f0f6fc;
        }}

        #markdown-content a {{
            color: #58a6ff;
            text-decoration: none;
        }}

        #markdown-content a:hover {{
            text-decoration: underline;
        }}

        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: #0d1117;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #30363d;
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #484f58;
        }}
    </style>
</head>
<body>
    <div id="sidebar">
        <h2>📚 변경 이력</h2>
        <ul id="file-list"></ul>
    </div>
    <div id="content">
        <div id="markdown-content"></div>
    </div>

    <script>
        const files = {files_js};
        const defaultFile = "{default_file}";

        // 사이드바 생성
        const fileList = document.getElementById('file-list');
        files.forEach(item => {{
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = item.name;
            a.onclick = (e) => {{
                e.preventDefault();
                loadMarkdown(item.file);
                updateActiveLink(a);
            }};
            li.appendChild(a);
            fileList.appendChild(li);
        }});

        // 마크다운 로드
        async function loadMarkdown(filename) {{
            try {{
                const response = await fetch(filename);
                const text = await response.text();
                const html = marked.parse(text);
                document.getElementById('markdown-content').innerHTML = html;
            }} catch (error) {{
                document.getElementById('markdown-content').innerHTML =
                    '<h1>오류</h1><p>파일을 불러올 수 없습니다.</p>';
            }}
        }}

        // 활성 링크 업데이트
        function updateActiveLink(activeLink) {{
            document.querySelectorAll('#file-list a').forEach(a => {{
                a.classList.remove('active');
            }});
            activeLink.classList.add('active');
        }}

        // 초기 로드
        if (files.length > 0) {{
            loadMarkdown(defaultFile);
            const firstLink = document.querySelector('#file-list a');
            if (firstLink) updateActiveLink(firstLink);
        }}
    </script>
</body>
</html>"""

        index_path.write_text(html_content, encoding="utf-8")

    def _create_readme(self):
        """README.md 생성"""
        readme_path = self.reviews_dir / "README.md"
        if not readme_path.exists():
            readme_content = f"""# {self.project_name} - 코드 변경 이력

이 폴더에는 AI가 생성한 모든 코드 변경사항이 기록되어 있습니다.

## 문서 확인 방법

### 웹 브라우저로 확인 (권장)

```bash
cd reviews
python3 -m http.server 4000
```

브라우저에서 http://localhost:4000 접속

### 파일로 확인

왼쪽 사이드바에서 날짜별로 변경 이력을 확인할 수 있습니다.

## 변경 이력

최신 변경사항이 맨 위에 표시됩니다.
"""
            readme_path.write_text(readme_content, encoding="utf-8")

    def save_review(self):
        """변경사항을 파일로 저장"""
        if not self.changes:
            print("기록할 변경사항이 없습니다.")
            return

        # 마크다운 파일 생성
        filename = f"{self.timestamp}.md"
        filepath = self.reviews_dir / filename

        md_content = self._generate_markdown()
        filepath.write_text(md_content, encoding="utf-8")

        print(f"✅ 변경사항 저장 완료: {filepath}")
        return filepath

    def save_and_update(self):
        """저장 + SUMMARY 업데이트"""
        filepath = self.save_review()
        if filepath:
            self._update_summary()
            print(f"✅ SUMMARY.md 업데이트 완료")

    def save_and_build(self):
        """저장 + SUMMARY 업데이트 + index.html 업데이트"""
        filepath = self.save_review()
        if filepath:
            self._create_readme()
            self._update_summary()
            self._update_index_html()
            print(f"✅ SUMMARY.md 업데이트 완료")
            print(f"✅ index.html 업데이트 완료")
            print(f"\n🌐 서버 실행: cd reviews && python3 -m http.server {self.port}")
            print(f"📱 브라우저: http://localhost:{self.port}")


def main():
    """CLI 인터페이스"""
    import sys

    if len(sys.argv) < 2:
        print("사용법:")
        print("  python3 code_changelog_tracker.py init    - 초기화")
        print("  python3 code_changelog_tracker.py build   - 빌드")
        print("  python3 code_changelog_tracker.py serve   - 서버 실행")
        return

    command = sys.argv[1]

    if command == "init":
        logger = CodeChangeLogger("Code Changelog", "초기 설정")
        logger.save_and_build()
        print("\n✅ 초기 설정 완료!")

    elif command == "build":
        reviews_dir = Path("reviews")
        if not reviews_dir.exists():
            print("❌ reviews 폴더가 없습니다. 먼저 init을 실행하세요.")
            return

        logger = CodeChangeLogger("Rebuild", "")
        logger._create_readme()
        logger._update_summary()
        logger._update_index_html()
        print("✅ 빌드 완료!")

    elif command == "serve":
        import http.server
        import socketserver

        port = 4000
        if len(sys.argv) > 2:
            port = int(sys.argv[2])

        os.chdir("reviews")

        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🌐 서버 실행 중: http://localhost:{port}")
            print("종료하려면 Ctrl+C를 누르세요.")
            httpd.serve_forever()


if __name__ == "__main__":
    main()
