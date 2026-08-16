import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"c:\Data\charlotte-ai-os-dev\Travelplan\2026 Germany")

# Directories
dirs = [
    BASE_DIR / "plans" / "00_總覽與交通",
    BASE_DIR / "plans" / "01_每日行程",
    BASE_DIR / "plans" / "02_五大基地環線",
    BASE_DIR / "plans" / "03_深度專題",
    BASE_DIR / "plans" / "Archived",
    BASE_DIR / "blog" / "drafts",
    BASE_DIR / "blog" / "prompts",
    BASE_DIR / "tools",
]

for d in dirs:
    d.mkdir(parents=True, exist_ok=True)

# File moves mapping: src_filename -> dest_rel_path
file_moves = {
    # Prompts
    "01. 資訊型貼文Prompt.md": "blog/prompts/01_資訊型貼文Prompt.md",
    "02. 感性貼文Prompt.md": "blog/prompts/02_感性貼文Prompt.md",
    # 00_總覽與交通
    "93-0. 行程v3.md": "plans/00_總覽與交通/00_MASTER_ITINERARY.md",
    "Hallstatt-交通攻略.md": "plans/00_總覽與交通/01_哈修塔特交通攻略.md",
    # 02_五大基地環線
    "93-1. Hallstatt_v2.md": "plans/02_五大基地環線/01_哈修塔特基地與湖區.md",
    "93-2. Wurzburg_v4.md": "plans/02_五大基地環線/02_符茲堡基地與美茵河.md",
    "93-3. Heidelberg.md": "plans/02_五大基地環線/03_海德堡基地與內卡河.md",
    "93-4. Colmar.md": "plans/02_五大基地環線/04_科爾馬基地與亞爾薩斯.md",
    "93-5. Garmisch.md": "plans/02_五大基地環線/05_加米許基地與阿爾卑斯.md",
    # 03_深度專題 (Attraction files)
    "Bamberg.md": "plans/03_深度專題/Bamberg.md",
    "Colmar.md": "plans/03_深度專題/Colmar.md",
    "Frankfurt.md": "plans/03_深度專題/Frankfurt.md",
    "Freiburg.md": "plans/03_深度專題/Freiburg.md",
    "Fussen.md": "plans/03_深度專題/Fussen.md",
    "Garmisch-Partenkirchen.md": "plans/03_深度專題/Garmisch-Partenkirchen.md",
    "Hallstatt-Bad Ischl.md": "plans/03_深度專題/Hallstatt-Bad Ischl.md",
    "Hallstatt.md": "plans/03_深度專題/Hallstatt.md",
    "Heidelberg.md": "plans/03_深度專題/Heidelberg.md",
    "Munich.md": "plans/03_深度專題/Munich.md",
    "Neuschwanstein.md": "plans/03_深度專題/Neuschwanstein.md",
    "Nuremberg.md": "plans/03_深度專題/Nuremberg.md",
    "Rothenburg.md": "plans/03_深度專題/Rothenburg.md",
    "Salzburg.md": "plans/03_深度專題/Salzburg.md",
    "Schauinsland.md": "plans/03_深度專題/Schauinsland.md",
    "Titisee.md": "plans/03_深度專題/Titisee.md",
    "Triberg.md": "plans/03_深度專題/Triberg.md",
    "Wurzburg.md": "plans/03_深度專題/Wurzburg.md",
    "Zugspitze.md": "plans/03_深度專題/Zugspitze.md",
}

for src_name, dest_rel in file_moves.items():
    src_path = BASE_DIR / src_name
    dest_path = BASE_DIR / dest_rel
    if src_path.exists():
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dest_path))
        print(f"Moved: {src_name} -> {dest_rel}")
    else:
        print(f"Skipped (not found): {src_name}")

# Move 2026WinterEurope into plans/Archived/2026WinterEurope
winter_dir = BASE_DIR / "2026WinterEurope"
if winter_dir.exists():
    arch_dest = BASE_DIR / "plans" / "Archived" / "2026WinterEurope"
    if arch_dest.exists():
        shutil.rmtree(str(arch_dest))
    shutil.move(str(winter_dir), str(arch_dest))
    print("Moved: 2026WinterEurope -> plans/Archived/2026WinterEurope")

# Move root Archived/ into plans/Archived/
old_archived = BASE_DIR / "Archived"
if old_archived.exists():
    for item in old_archived.iterdir():
        target = BASE_DIR / "plans" / "Archived" / item.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(str(target))
            else:
                target.unlink()
        shutil.move(str(item), str(target))
    try:
        os.rmdir(str(old_archived))
    except Exception:
        pass
    print("Consolidated: Archived/ -> plans/Archived/")

print("\nOrganization complete!")
