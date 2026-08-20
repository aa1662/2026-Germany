import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_SUPPORTED = True
except ImportError:
    HEIF_SUPPORTED = False

BASE_DIR = Path(r"c:\Data\charlotte-ai-os-dev\Travelplan\2026 Germany")
TAKEOUT_DIR = Path(r"C:\Users\aa166\Downloads\Takeout\Instagram")
POSTS_FILE = TAKEOUT_DIR / "your_instagram_activity" / "media" / "posts_1.json"
if not POSTS_FILE.exists():
    POSTS_FILE = TAKEOUT_DIR / "your_instagram_activity" / "media" / "posts.json"

def fix_text(s):
    if not s:
        return ""
    try:
        return s.encode('latin1').decode('utf-8')
    except Exception:
        return s

def process_and_save_image(src_path: Path, dest_dir: Path) -> str:
    dest_dir.mkdir(parents=True, exist_ok=True)
    stem = src_path.stem
    dest_filename = f"{stem}.jpg"
    dest_path = dest_dir / dest_filename
    
    if dest_path.exists():
        return dest_filename
    
    try:
        with Image.open(src_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            max_size = 1800
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            img.save(dest_path, "JPEG", quality=88, optimize=True)
            return dest_filename
    except Exception as e:
        print(f"Error converting {src_path.name}: {e}")
        dest_raw = dest_dir / f"{stem}.jpg"
        shutil.copy2(str(src_path), str(dest_raw))
        return f"{stem}.jpg"

with open(POSTS_FILE, 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Targets:
# Day 12: Graseck (2026-02-17 23:59:13)
# Day 13: Neuschwanstein (2026-02-20 00:55:40)
# Day 14: Partnachklamm (2026-02-20 20:52:45)

target_posts = {}
for p in posts:
    ts = p.get('creation_timestamp', 0)
    dt = datetime.fromtimestamp(ts)
    title = fix_text(p.get('title', ''))
    if "Graseck" in title:
        target_posts['Day-12'] = p
    elif "很久很久以前，來過天鵝堡" in title or ("天鵝堡" in title and "馬車" in title):
        target_posts['Day-13'] = p
    elif "冬季冰瀑奇景" in title or "帕特納赫峽谷" in title:
        target_posts['Day-14'] = p

print(f"Found target posts: {list(target_posts.keys())}")

for day_key, p in target_posts.items():
    day_folder = BASE_DIR / "docs" / "images" / day_key.lower()
    media_list = p.get('media', [])
    print(f"\nProcessing {day_key} ({len(media_list)} media items)...")
    converted_files = []
    for m in media_list:
        raw_uri = m.get('uri', '')
        if raw_uri:
            src_photo = TAKEOUT_DIR / raw_uri
            if src_photo.exists():
                fn = process_and_save_image(src_photo, day_folder)
                converted_files.append(fn)
                print(f"  Saved {day_key} image: {fn}")
            else:
                print(f"  Missing file: {src_photo}")
