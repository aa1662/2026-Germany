import json
from datetime import datetime
from pathlib import Path

def fix_text(s):
    try:
        return s.encode('latin1').decode('utf-8')
    except Exception:
        return s

takeout_dir = Path(r"C:\Users\aa166\Downloads\Takeout\Instagram\your_instagram_activity\media")
posts_file = takeout_dir / "posts_1.json"
if not posts_file.exists():
    posts_file = takeout_dir / "posts.json"

with open(posts_file, 'r', encoding='utf-8') as f:
    posts = json.load(f)

for p in posts:
    ts = p.get('creation_timestamp', 0)
    dt = datetime.fromtimestamp(ts)
    if dt.year == 2026 and dt.month == 2 and dt.day >= 17:
        title = fix_text(p.get('title', ''))
        media = p.get('media', [])
        print('='*60)
        print(f"POST TIMESTAMP: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"TITLE:\n{title}")
        print(f"MEDIA ({len(media)} items):")
        for m in media:
            uri = m.get('uri', '')
            media_ts = m.get('creation_timestamp', 0)
            media_dt = datetime.fromtimestamp(media_ts)
            print(f"  - {uri} (taken: {media_dt.strftime('%Y-%m-%d %H:%M:%S')})")
