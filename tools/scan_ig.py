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

print(f"Total posts: {len(posts)}")

# Let's inspect the date range of posts
trip_posts = []
all_years = set()
for p in posts:
    ts = p.get('creation_timestamp', 0)
    dt = datetime.fromtimestamp(ts)
    all_years.add(dt.year)
    title = fix_text(p.get('title', ''))
    # check 2025/2026 or trip keywords
    if dt.year in [2025, 2026]:
        trip_posts.append((dt, title, p.get('media', [])))

print(f"Years found in takeout: {sorted(all_years)}")
print(f"Found {len(trip_posts)} posts in 2025-2026:")
for dt, title, media in sorted(trip_posts, key=lambda x: x[0]):
    preview = title.replace('\n', ' ')[:80]
    print(f"[{dt.strftime('%Y-%m-%d %H:%M')}] ({len(media)} photos) {preview}")
