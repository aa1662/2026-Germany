# 🇩🇪 2026 德國南部冬季 15 天自駕之旅 ✕ 沉浸式圖文遊記 (Travelogue & Travel OS)

> **專案定位**：以「**深度個人圖文網誌 (Editorial Blog)**」為主體，融合「**現場 IG 隨筆速記**」與「**旅人深度散文**」，並以「**實用 Travel OS 知識庫**」為最強後盾（隨文 Bento 資訊盒）的雙核心旅遊系統。

---

## 📌 專案架構導覽 (System Architecture)

```
2026 Germany (專案根目錄)
│
├── 📜 專案治理與方法論
│   ├── README.md                      # 專案總覽、發布導引與系統架構
│   ├── AGENTS.md                      # AI Agent 協作規範與 SSoT 知識庫維護準則
│   └── METHODOLOGY.md                 # 3 層敘事網誌與自駕旅遊方法論
│
├── 📝 blog/ 網誌創作與故事中心 (Editorial Center)
│   ├── drafts/                        # 15 篇深度網誌 Markdown 草稿 (IG隨筆 + 旅後擴寫)
│   └── prompts/                       # 社群與圖文 Prompt 範本庫 (資訊型 / 感性型)
│
├── 🧭 plans/ 實用旅遊情報庫 (Travel OS - SSoT 資料來源)
│   ├── 00_總覽與交通/                 # 15天總行程主表、交通攻略、過路費與自駕法規
│   ├── 01_每日行程/                   # 15天詳細時間表 (Day 01 ~ Day 15)
│   ├── 02_五大基地環線/               # 哈修塔特、符茲堡、海德堡、科爾馬、加米許五大基地
│   ├── 03_深度專題/                   # 20+ 份單一城市與景點深度指南 (羅騰堡、新天鵝堡等)
│   └── Archived/                      # 歷史版本草稿與參考資料歸檔
│
├── 🛠️ tools/ 自動化工具與管線
│   ├── import_instagram.py            # IG Takeout 圖文自動萃取與草稿注入腳本
│   └── organize_workspace.py          # 專案目錄重整與維護腳本
│
└── 🌐 docs/ 前端展示層 (GitHub Pages 發布目錄)
    ├── index.html                     # 雜誌風 Bento Home (高光照片牆 + 15天導覽)
    ├── day-01.html ~ day-15.html      # 每日行程與景點頁面
    ├── guide-*.html                   # 五大區域深度指南頁面
    ├── blog/                          # 深度圖文網誌發布頁
    ├── css/style.css                  # 現代雜誌風 + Bento Grid 樣式表
    └── js/main.js                     # 德法發音引擎、燈箱預覽、手風琴折疊與導覽互動
```

---

## 📖 文章三層黃金架構 (3-Layer Narrative Model)

每篇發布的遊記均包含以下三層有機結合：
1. **第 1 層：視覺衝擊與 IG 現場隨筆 (Live Feed & Mood)** — 原汁原味還原旅行當下的冷冽空氣、第一眼震撼與即時心境。
2. **第 2 層：深度旅人散文與回甘筆記 (The Deep Narrative)** — 事後沉澱撰寫的文化觀察、同行趣事、心靈感受與散文隨筆。
3. **第 3 層：隨文嵌入的實用攻略 Bento 盒 (Practical Travel OS)** — 包含自駕路線避坑、景點冬季開放時間、德法語真人發音、Google Maps 導航一鍵跳轉。

---

## 🛠️ 開發與發布方式

- **本地預覽**：直接以瀏覽器開啟 `docs/index.html`，或使用 VS Code Live Server / Python HTTP Server。
- **線上發布**：專案透過 GitHub Actions / GitHub Pages 自動將 `docs/` 目錄部署上線。
