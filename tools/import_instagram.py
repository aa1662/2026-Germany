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

OUTPUT_DRAFTS_DIR = BASE_DIR / "blog" / "drafts"
OUTPUT_IMAGES_DIR = BASE_DIR / "docs" / "images" / "ig"

OUTPUT_DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def fix_text(s):
    if not s:
        return ""
    try:
        return s.encode('latin1').decode('utf-8')
    except Exception:
        return s

def process_and_save_image(src_path: Path, dest_dir: Path) -> str:
    """Converts HEIC/JPG to web-optimized JPG and resizes if needed."""
    stem = src_path.stem
    dest_filename = f"{stem}.jpg"
    dest_path = dest_dir / dest_filename
    
    if dest_path.exists():
        return dest_filename
    
    try:
        with Image.open(src_path) as img:
            # Convert RGBA/P to RGB for JPG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize if too large
            max_size = 1600
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
            img.save(dest_path, "JPEG", quality=85, optimize=True)
            return dest_filename
    except Exception as e:
        print(f"Error converting {src_path.name}: {e}")
        # fallback copy raw
        dest_raw = dest_dir / src_path.name
        if not dest_raw.exists():
            shutil.copy2(str(src_path), str(dest_raw))
        return src_path.name

with open(POSTS_FILE, 'r', encoding='utf-8') as f:
    raw_posts = json.load(f)

# Filter 2026 Europe trip posts
trip_posts = []
for p in raw_posts:
    ts = p.get('creation_timestamp', 0)
    dt = datetime.fromtimestamp(ts)
    if dt.year == 2026 and dt.month == 2:
        title = fix_text(p.get('title', ''))
        media_list = p.get('media', [])
        trip_posts.append({
            'datetime': dt,
            'timestamp': ts,
            'caption': title,
            'media': media_list
        })

trip_posts.sort(key=lambda x: x['datetime'])
print(f"Europe Trip IG Posts: {len(trip_posts)}")

def classify_post(post):
    text = post['caption']
    if "薩爾茲堡" in text or "莫札特" in text:
        return "Day-01", "薩爾斯堡與哈修塔特抵達", "Salzburg & Hallstatt"
    elif "哈修塔特" in text or "哈斯達特" in text or "Hallstatt" in text:
        return "Day-02", "哈修塔特湖畔漫遊", "Hallstatt"
    elif "班堡" in text or "Bamberg" in text:
        return "Day-04", "班堡老城與煙燻啤酒", "Bamberg"
    elif "紐倫堡" in text or "Nürnberg" in text:
        return "Day-05", "紐倫堡皇帝堡與中世紀走讀", "Nürnberg"
    elif "羅騰堡" in text or "Rothenburg" in text:
        return "Day-06", "羅騰堡童話小鎮", "Rothenburg"
    elif "符茲堡" in text or "Würzburg" in text:
        return "Day-07", "符茲堡主教宮與舊美茵橋白葡萄酒", "Würzburg"
    elif "海德堡" in text or "Heidelberg" in text:
        return "Day-08", "海德堡城堡與內卡河浪漫古城", "Heidelberg"
    elif "哈瑙" in text or "法蘭克福" in text:
        return "Day-09", "哈瑙童話起點與法蘭克福", "Hanau & Frankfurt"
    elif "科爾馬" in text or "Colmar" in text or "霍爾的移動城堡" in text:
        return "Day-10", "科爾馬小威尼斯與亞爾薩斯童話", "Colmar"
    elif "巴塞爾" in text or "Basel" in text:
        return "Day-11", "瑞士巴塞爾與國際清算銀行朝聖", "Basel"
    elif "埃吉桑姆" in text or "Eguisheim" in text:
        return "Day-11", "埃吉桑姆法國最美村莊與酒鄉", "Eguisheim"
    elif "Graseck" in text or "加米許" in text or "Partnachklamm" in text or "帕特納赫" in text:
        return "Day-13", "加米許山莊溫泉與冬季冰瀑", "Garmisch & Partnachklamm"
    elif "天鵝堡" in text or "新天鵝堡" in text or "Neuschwanstein" in text:
        return "Day-14", "新天鵝堡雪景與回憶之旅", "Neuschwanstein"
    else:
        return "Day-Unclassified", "歐洲冬旅隨筆", "Europe Trip"

grouped_days = {}
for post in trip_posts:
    day_id, title_tw, title_en = classify_post(post)
    if day_id not in grouped_days:
        grouped_days[day_id] = {
            'title_tw': title_tw,
            'title_en': title_en,
            'posts': []
        }
    grouped_days[day_id]['posts'].append(post)

for day_id, data in sorted(grouped_days.items()):
    md_filename = f"{day_id}-{data['title_tw'].replace(' ', '_')}.md"
    md_path = OUTPUT_DRAFTS_DIR / md_filename
    
    content = []
    content.append(f"# {day_id}：{data['title_tw']} ({data['title_en']})")
    content.append("\n> 📅 **旅程日期**：2026 冬季 ｜ **地點**：德國 / 奧地利 / 法國 / 瑞士")
    content.append("\n---\n")
    
    content.append("## 📸 第一手 IG 現場隨筆與快照 (Live Feed)")
    content.append("\n*以下為旅途中現場發布之即時紀錄與心情：*\n")
    
    photo_count = 0
    for idx, p in enumerate(data['posts'], 1):
        dt_str = p['datetime'].strftime('%Y-%m-%d %H:%M')
        content.append(f"### 📍 現場筆記 #{idx} ({dt_str})")
        content.append(f"\n```quote\n{p['caption']}\n```\n")
        
        for m in p['media']:
            raw_uri = m.get('uri', '')
            if raw_uri:
                src_photo = TAKEOUT_DIR / raw_uri
                if src_photo.exists():
                    saved_filename = process_and_save_image(src_photo, OUTPUT_IMAGES_DIR)
                    rel_img_path = f"../images/ig/{saved_filename}"
                    content.append(f"![現場實拍 {photo_count+1}]({rel_img_path})\n")
                    photo_count += 1
    
    content.append("\n---\n")
    content.append("## ✍️ 旅人深度散文與回甘筆記 (The Narrative)")
    content.append("\n> 💡 **作者擴寫空間**：請在此處自由補充旅後的心情、文化觀察、與家人同行的趣事或當下未及細述的感動。\n")
    content.append("（在此自由書寫你的深度遊記故事...）\n")
    
    content.append("\n---\n")
    content.append("## 🧭 讀者抄作業：實用攻略 Bento 資訊盒 (Travel OS)")
    content.append("""
| 項目 | 實用情報 | 備註與避坑 (TripNG) |
| :--- | :--- | :--- |
| 🚗 **自駕路況** | 冬季雪胎/雪鏈注意 | 跨國記得備妥 Vignette 通行證 |
| 📍 **必拍機位** | 經典明信片拍攝點 | 建議藍調時刻 (16:30 左右) 抵達 |
| 🍽️ **必吃美食** | 在地特色餐點 | 附德/法語發音與點餐指南 |
| 🏨 **當晚下榻** | 嚴選住宿地點 | 附停車場 (P+R) 座標 |
""")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"Generated Draft: {md_filename} ({photo_count} photos converted to web-ready JPG).")

print("\nAll drafts and web-optimized images generated successfully!")
