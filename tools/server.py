#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Travel OS - 本機動態伺服器與視覺化編輯 API
Zero-dependency Python 3 HTTP Server with Visual Editing & Image Swapping APIs.
"""

import os
import sys
import json
import shutil
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# 定位專案根目錄與 docs 資料夾
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
PORT = 8000


class TravelOSEditorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # API: 列出所有可用頁面 (天數、文章、時間表)
        if path == "/api/list-posts":
            self.send_json(self.get_posts_list())
            return

        # API: 列出指定天數的所有圖片
        if path == "/api/list-images":
            folder = query.get("folder", ["day-01"])[0]
            self.send_json(self.get_images_list(folder))
            return

        # API: 讀取指定檔案內容
        if path == "/api/load-post":
            rel_file = query.get("file", ["blog/day-01-blog.html"])[0]
            self.send_json(self.load_post_file(rel_file))
            return

        # 預設靜態檔案服務
        super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # API: 儲存文章
        if path == "/api/save-post":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                data = json.loads(post_body.decode("utf-8"))
                result = self.save_post_file(data.get("file"), data.get("html"))
                self.send_json(result)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        # API: 還原備份檔
        if path == "/api/restore-backup":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                data = json.loads(post_body.decode("utf-8"))
                result = self.restore_backup_file(data.get("file"))
                self.send_json(result)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        self.send_error(404, "API endpoint not found")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def get_posts_list(self):
        blog_files = sorted(list((DOCS_DIR / "blog").glob("*.html")))
        schedule_files = sorted(list(DOCS_DIR.glob("day-*.html")))

        blogs = []
        for bf in blog_files:
            rel = bf.relative_to(DOCS_DIR).as_posix()
            blogs.append({
                "file": rel,
                "name": bf.stem.replace("-blog", "").upper(),
                "type": "blog"
            })

        schedules = []
        for sf in schedule_files:
            rel = sf.relative_to(DOCS_DIR).as_posix()
            schedules.append({
                "file": rel,
                "name": sf.stem.upper(),
                "type": "schedule"
            })

        # 圖片目錄清單
        image_dirs = []
        img_root = DOCS_DIR / "images"
        if img_root.exists():
            for d in sorted(img_root.iterdir()):
                if d.is_dir():
                    image_dirs.append(d.name)

        return {
            "success": True,
            "blogs": blogs,
            "schedules": schedules,
            "image_folders": image_dirs
        }

    def get_images_list(self, folder):
        target_dir = (DOCS_DIR / "images" / folder).resolve()
        if not target_dir.exists() or not str(target_dir).startswith(str(DOCS_DIR / "images")):
            return {"success": False, "images": [], "error": "Folder not found"}

        image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
        images = []
        for f in sorted(target_dir.iterdir()):
            if f.is_file() and f.suffix.lower() in image_extensions:
                rel = f.relative_to(DOCS_DIR).as_posix()
                images.append({
                    "filename": f.name,
                    "rel_path": rel,
                    "url": f"/{rel}",
                    "size_kb": round(f.stat().st_size / 1024, 1)
                })

        return {"success": True, "folder": folder, "images": images}

    def load_post_file(self, rel_file):
        target_file = (DOCS_DIR / rel_file).resolve()
        if not target_file.exists() or not str(target_file).startswith(str(DOCS_DIR)):
            return {"success": False, "error": "File not found"}

        has_backup = target_file.with_suffix(target_file.suffix + ".bak").exists()
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "success": True,
            "file": rel_file,
            "has_backup": has_backup,
            "html": content
        }

    def save_post_file(self, rel_file, html_content):
        if not rel_file or not html_content:
            return {"success": False, "error": "Missing file or content"}

        target_file = (DOCS_DIR / rel_file).resolve()
        if not str(target_file).startswith(str(DOCS_DIR)):
            return {"success": False, "error": "Invalid file path"}

        # 1. 建立自動備份檔 (.bak)
        bak_file = target_file.with_suffix(target_file.suffix + ".bak")
        if target_file.exists():
            shutil.copyfile(target_file, bak_file)

        # 2. 寫入新內容
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return {
            "success": True,
            "file": rel_file,
            "message": f"儲存成功！已自動備份至 {bak_file.name}",
            "backup_file": bak_file.name
        }

    def restore_backup_file(self, rel_file):
        target_file = (DOCS_DIR / rel_file).resolve()
        bak_file = target_file.with_suffix(target_file.suffix + ".bak")
        if not bak_file.exists():
            return {"success": False, "error": "No backup file found"}

        shutil.copyfile(bak_file, target_file)
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "success": True,
            "file": rel_file,
            "message": "已成功從備份檔還原！",
            "html": content
        }


def main():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, TravelOSEditorHandler)
    print(f"============================================================")
    print(f"🇩🇪 Travel OS Local Server & Visual Editor Running!")
    print(f"🌐 Website Preview : http://localhost:{PORT}/")
    print(f"✏️ Visual Editor   : http://localhost:{PORT}/editor.html")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
        httpd.server_close()


if __name__ == "__main__":
    main()
