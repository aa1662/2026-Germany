# 🧭 德南冬季自駕遊記與旅遊規劃方法論 (Travel & Blog Methodology)

> **版本**：v2.1.0  
> **核心概念**：結合「**3 層敘事網誌模型 (3-Layer Narrative Model)**」與「**Travel OS 自駕實戰工程 (TripQ & TripNG)**」，打造兼具文學共鳴與實戰價值的旗艦級歐洲自駕遊記。

---

## 1. 網誌 3 層敘事模型 (The 3-Layer Narrative Formula)

為了讓讀者沉浸於旅程故事，同時具備「立即可抄作業」的實用性，每篇網誌均遵循以下層次：

```
                    【遊記 3 層黃金架構】
                              │
  [Layer 1: 視覺與現場微光] ➔ Split / Diptych Hero ✕ IG 貼文卡片 ✕ 原生照片網格
                              │
  [Layer 2: 旅人深度散文] ➔ 看圖說故事 (Photo-Guided) ✕ 左右圖文交錯排版 (Story-Split) ✕ 旅後回甘
                              │
  [Layer 3: 隨文 Bento 資訊盒] ➔ 自駕停車 ✕ 拍照機位 ✕ 美食發音 ✕ 虛線地圖 ✕ 避坑警示
```

### 1.1 散文「看圖說故事」核心法則 (Photo-Guided Storytelling)
- **視覺錨點驅動**：深度散文嚴禁流水帳式純文字堆疊。每章節、每段落均以一張具體照片（或一組對比照片）為視覺錨點，由畫面的光影、人物動作、建築細節展開故事。
- **雜誌風左右圖文交錯 (Alternating Story-Split Rhythm)**：
  - 直式照片（4:5）採用「左圖右文 (`.story-split`)」與「右圖左文 (`.story-split.reverse`)」交替穿插，營造頂級雜誌般的節奏感。
  - 橫式大景（16:9）採用「100% 全寬寬幅 (`.fullwidth-landscape-wrap`)」作為章節破題或場景轉換。
  - 手機瀏覽時全自動響應式降級為「圖上文下」單欄流暢佈局，完全維持 CLS = 0。

---

## 2. 前端標準 HTML/CSS 模板庫 (Code Templates)

### 2.1 封面 Hero：時光對照雙聯屏 (Diptych Dual Hero)
```html
<section class="diptych-hero">
  <div class="diptych-grid">
    <div class="diptych-frame">
      <a href="../images/ig/2014-summer.jpg" class="glightbox" data-gallery="diptych" data-title="2014 盛夏">
        <img src="../images/ig/2014-summer.jpg" alt="2014 盛夏">
      </a>
      <div class="diptych-tag diptych-tag-summer">🌱 2014 盛夏 · 舊日光影</div>
    </div>
    <div class="diptych-frame">
      <a href="../images/ig/2026-winter.jpg" class="glightbox" data-gallery="diptych" data-title="2026 寒冬">
        <img src="../images/ig/2026-winter.jpg" alt="2026 寒冬">
      </a>
      <div class="diptych-tag diptych-tag-winter">❄️ 2026 寒冬 · 十二年重遊</div>
    </div>
  </div>
  <div>
    <h1 style="font-family: var(--font-heading); font-size: 2.1rem; color: var(--primary);">
      Day 02：哈修塔特湖畔漫遊 — 夏與冬的十二年對照
    </h1>
    <div class="diptych-quote">
      ✨ 「#哈斯達特 2014夏 VS 2026冬 —— 同一個地點，不同的季節與人生階段。」
    </div>
  </div>
</section>
```

### 2.2 封面 Hero：雜誌風 Split Hero (左圖右文)
```html
<section class="split-hero">
  <div class="split-hero-img-wrap">
    <a href="../images/ig/hero-portrait.jpg" class="glightbox" data-gallery="hero" data-title="薩爾斯堡冬景">
      <img src="../images/ig/hero-portrait.jpg" alt="薩爾斯堡冬景">
    </a>
  </div>
  <div class="split-hero-content">
    <div class="hero-badge-group">
      <span class="badge badge-alpine">📍 慕尼黑 ➔ 薩爾斯堡</span>
      <span class="badge badge-gold">📅 2026/1/26 (一)</span>
    </div>
    <h1 style="font-family: var(--font-heading); font-size: 2.1rem; color: var(--primary);">
      Day 01：莫札特的家，我來過三次了
    </h1>
    <p style="color: var(--text-sub); font-size: 1.05rem;">
      從慕尼黑機場取車南下，重訪音樂之城...
    </p>
  </div>
</section>
```

### 2.3 直式照片雙拼與三拼網格 (Portrait 4:5 Grids)
```html
<!-- 雙拼 Duo -->
<div class="portrait-duo">
  <div class="portrait-item">
    <a href="../images/ig/photo-1.jpg" class="glightbox" data-gallery="gallery-1" data-title="Salzburg (1/5)">
      <img src="../images/ig/photo-1.jpg" alt="Salzburg">
    </a>
  </div>
  <div class="portrait-item">
    <a href="../images/ig/photo-2.jpg" class="glightbox" data-gallery="gallery-1" data-title="Salzburg (2/5)">
      <img src="../images/ig/photo-2.jpg" alt="Salzburg">
    </a>
  </div>
</div>

<!-- 三拼 Trio -->
<div class="portrait-trio">
  <div class="portrait-item">
    <a href="../images/ig/photo-3.jpg" class="glightbox" data-gallery="gallery-1" data-title="Salzburg (3/5)">
      <img src="../images/ig/photo-3.jpg" alt="Salzburg">
    </a>
  </div>
  <div class="portrait-item">
    <a href="../images/ig/photo-4.jpg" class="glightbox" data-gallery="gallery-1" data-title="Salzburg (4/5)">
      <img src="../images/ig/photo-4.jpg" alt="Salzburg">
    </a>
  </div>
  <div class="portrait-item">
    <a href="../images/ig/photo-5.jpg" class="glightbox" data-gallery="gallery-1" data-title="Salzburg (5/5)">
      <img src="../images/ig/photo-5.jpg" alt="Salzburg">
    </a>
  </div>
</div>
```

### 2.4 看圖說故事：左右圖文交錯與全寬大圖 (Story-Split & Fullwidth Landscape)

#### (1) 左右圖文並列（左圖右文 ✕ 右圖左文）
```html
<!-- 左圖右文 Normal -->
<div class="story-split">
  <div class="story-split-media">
    <a href="../images/day-09/photo-left.jpg" class="glightbox" data-gallery="day-09-gallery" data-title="Schloss Philippsruhe · 2026/02/03">
      <img src="../images/day-09/photo-left.jpg" alt="雪中漫步走入巴洛克宮殿" loading="lazy">
    </a>
  </div>
  <div class="story-split-text">
    <p>
      清晨自海德堡出發，車輛沿著 A5 高速公路一路向北...（散文內文緊扣畫面）
    </p>
  </div>
</div>

<!-- 右圖左文 Reverse -->
<div class="story-split reverse">
  <div class="story-split-media">
    <a href="../images/day-09/photo-right.jpg" class="glightbox" data-gallery="day-09-gallery" data-title="Snow Joy · 2026/02/03">
      <img src="../images/day-09/photo-right.jpg" alt="宮殿前漫天飛雪中開懷甜笑" loading="lazy">
    </a>
  </div>
  <div class="story-split-text">
    <p>
      站在宮殿宏偉的門廊前，迎著漫天大雪伸出雙手接住飄落的雪花...（散文內文緊扣畫面）
    </p>
  </div>
</div>
```

#### (2) 100% 全寬寬幅大景 (Fullwidth Landscape)
```html
<div class="fullwidth-landscape-wrap">
  <a href="../images/day-09/landscape.jpg" class="glightbox" data-gallery="day-09-gallery" data-title="Philippsruhe Palace Façade · 2026/02/03">
    <img src="../images/day-09/landscape.jpg" alt="菲利普斯魯厄宮全景大圖" loading="lazy">
  </a>
</div>
```

### 2.5 Google Maps 虛線文字連結 (Osaka Dotted Link)
```html
<li>
  <strong>薩爾斯堡停車場</strong>：導航請設 
  <a href="https://maps.google.com/?q=Altstadtgarage+Salzburg" target="_blank" rel="noopener" class="text-map-link">
    <code>Altstadt Garage (Mönchsberg)</code>
  </a>，電梯直達老街。
</li>
```

---

## 3. Travel OS 自駕與行程工程核心

### 3.1 順重力幾何與冬季時間塊 (Downhill Law & Time-Blocks)
- **冬季日照約束**：16:30 左右天黑。戶外景觀排在 09:30 ~ 15:30；傍晚轉入古城老街、酒館、室內宮殿或藍調時刻攝影。
- **自駕摩擦力控制**：每日行車控制在 1.5 ~ 2.5 小時；長途日設定 Outlet 或景觀餐廳作為緩衝停靠點。

### 3.2 TripNG 冬季避坑壓力測試 (Anti-Traps Protocol)
- **阿爾卑斯雪胎法規**：奧地利/德國冬季強制冬季胎 (M+S / Alpine 標誌)；山區準備雪鏈。
- **跨國通行證 (Vignette)**：進入奧地利高速公路前備妥電子 Vignette。
- **冬季動態封閉避坑**：新天鵝堡瑪麗安橋、國王湖上湖冬季易結冰封閉，備妥替代方案。
