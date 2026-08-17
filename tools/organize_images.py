import os
import re
import shutil
from pathlib import Path

BASE_DIR = Path(r"c:\Data\charlotte-ai-os-dev\Travelplan\2026 Germany")
DOCS_DIR = BASE_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "images"
IG_DIR = IMAGES_DIR / "ig"
DRAFTS_DIR = BASE_DIR / "blog" / "drafts"

def main():
    print("=== Starting Image Organization into Day Subdirectories ===")
    
    # 1. Map each Day draft to its referenced images
    day_images_map = {} # 'day-01': ['17869170573551215.jpg', ...]
    
    for draft_file in DRAFTS_DIR.glob("Day-*.md"):
        m = re.match(r"Day-(\d+)", draft_file.name)
        if not m:
            continue
        day_key = f"day-{int(m.group(1)):02d}"
        
        content = draft_file.read_text(encoding='utf-8')
        # find all image references
        imgs = re.findall(r"([A-Za-z0-9_~-]+\.(?:jpg|png|jpeg|heic))", content, re.IGNORECASE)
        # filter out standard names if any
        valid_imgs = []
        for img in imgs:
            if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                valid_imgs.append(img)
        
        day_images_map[day_key] = list(dict.fromkeys(valid_imgs))
        print(f"[{day_key}] Found {len(day_images_map[day_key])} images in {draft_file.name}")

    # Add special cases if needed (e.g. Hallstatt05.jpg for day-02)
    if 'day-02' in day_images_map:
        if 'Hallstatt05.jpg' not in day_images_map['day-02']:
            day_images_map['day-02'].append('Hallstatt05.jpg')

    # 2. Copy photos into docs/images/day-XX/
    copied_count = 0
    mapping = {} # 'images/ig/123.jpg' -> 'images/day-01/123.jpg'
    
    for day_key, img_list in sorted(day_images_map.items()):
        target_dir = IMAGES_DIR / day_key
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for img_name in img_list:
            src_file = IG_DIR / img_name
            dst_file = target_dir / img_name
            
            if src_file.exists():
                shutil.copy2(src_file, dst_file)
                copied_count += 1
                mapping[f"images/ig/{img_name}"] = f"images/{day_key}/{img_name}"
                mapping[f"../images/ig/{img_name}"] = f"../images/{day_key}/{img_name}"
                mapping[f"/docs/images/ig/{img_name}"] = f"/docs/images/{day_key}/{img_name}"
                mapping[f"docs/images/ig/{img_name}"] = f"docs/images/{day_key}/{img_name}"
            else:
                # Check Takeout 02_Hallstatt if present
                takeout_hallstatt = Path(r"C:\Users\aa166\Downloads\Takeout\02_Hallstatt") / img_name
                if takeout_hallstatt.exists():
                    shutil.copy2(takeout_hallstatt, dst_file)
                    copied_count += 1
                    mapping[f"images/ig/{img_name}"] = f"images/{day_key}/{img_name}"
                    mapping[f"../images/ig/{img_name}"] = f"../images/{day_key}/{img_name}"
                    mapping[f"docs/images/ig/{img_name}"] = f"docs/images/{day_key}/{img_name}"
                    print(f"Copied from Takeout: {img_name} -> {target_dir}")
                else:
                    print(f"Warning: {src_file} does not exist!")

    print(f"\nTotal images copied into structured subdirectories: {copied_count}")

    # 3. Update references in HTML files and Drafts
    html_files = list(DOCS_DIR.rglob("*.html"))
    draft_files = list(DRAFTS_DIR.glob("*.md"))
    
    updated_files = 0
    for file_path in html_files + draft_files:
        content = file_path.read_text(encoding='utf-8')
        orig_content = content
        for old_path, new_path in mapping.items():
            content = content.replace(old_path, new_path)
            
        # also replace generic pattern like images/ig/xxx.jpg if we know its day
        for day_key, img_list in day_images_map.items():
            for img_name in img_list:
                content = re.sub(
                    rf'(?:\.\./)?images/ig/{re.escape(img_name)}',
                    lambda m: f"{'../' if m.group(0).startswith('../') else ''}images/{day_key}/{img_name}",
                    content
                )
        
        if content != orig_content:
            file_path.write_text(content, encoding='utf-8')
            updated_files += 1
            print(f"Updated image references in: {file_path.relative_to(BASE_DIR)}")

    print(f"\nCompleted! Updated references in {updated_files} files.")

if __name__ == "__main__":
    main()
