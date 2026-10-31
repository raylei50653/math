不規則三角形晶體與染色週期圖鑑
2026-10-31

開啟 preview.html 看 12 種週期晶體；開啟 color-preview.html 觀察四色頂點
染色。兩份都是可直接用瀏覽器開啟的獨立匯出頁，不需伺服器；晶體與染色
資料已內嵌，展示框架的工具提示與圖示套件會從 CDN 載入。
triangle-crystals.html、color-periodicity.html 是對話內展示的可編輯來源。
這個圖鑑是有限標本實驗，不更改專案既有的四色證明研究裁決。

幾何與資料

crystals.json 保存 12 個不規則的平面週期三角化標本。每個面頂點保留
(motif_vertex_id, lattice_dx, lattice_dy)，跨單元邊不因取模而遺失。
generate.py 以固定種子產生、先固定 8 位小數座標，再做 Delaunay 三角化。
5×5 與 7×7 複製範圍結果一致，並核對每邊反向雙面、頂點 link、Euler、
面積、度數總量、非退化及整個週期點集的空外接圓。這些為 Float64 數值檢查。
標示的是選定的重複單元，沒有宣稱它一定是最小原胞或完整同構分類。

染色結果與界線

color_periods.py 對每個晶體測試 (p,q) = (1,1),(2,1),(1,2),(2,2),(3,1),(1,3)。
colorings.json 保存全部 72 個指定週期判定與 188 份合法染色見證；
顏色陣列為 colors[y][x][motif_vertex_id]，所有原邊與跨單元邊均核對異色。
SAT 建構整個無限平面的週期染色；UNSAT 只排除該指定週期，沒有否定其他
週期或非週期染色。UNSAT 為求解器判定，沒有附形式化不可滿足證明檔。
每個 SAT 週期保存至多三份去除全域色號置換的染法，不是全部染法枚舉。

P01：1×1、2×1、1×2、3×1 不可行；2×2、1×3 可行。
P05：1×1、2×1、1×2 不可行；2×2、3×1、1×3 可行。
P09：1×1 不可行，其他五種測試週期可行。
其他九種：六種測試週期都可行。
P05 的 3×1 與 P09 的 2×1 染法可展示「平移後整體換色」與「原色重合」的差異。
每份見證另記完整平移對稱及色號置換，軸向週期矩形不必等於最小斜向週期域。
六種矩形測試沒有窮盡任意平移子晶格，也不建立所有染色的最小週期。
各標本都有實際奇數鄰點環，局部排除三色；現有四色見證因此給出各標本色數為 4。
生成、染色與這些限定不依賴四色定理，沒有新增 Lean 證明。

從 repository 根目錄重播

uv run --with scipy==1.18.1 --with numpy==2.4.3 python work/periodic-triangle-atlas/generate.py
uv run --with python-sat==1.9.dev17 python work/periodic-triangle-atlas/color_periods.py
python3 work/periodic-triangle-atlas/build_color_visual.py

固定依賴下原始資料 SHA256：
crystals.json  c2f058276c21b92831b8a63671c90833b1f589577b1140c0e26d5c29aa22ce55
colorings.json d5063641a18d2b7c1b2b8dd7d954fd186460ecab542f5f1415a4a174071565fd

build_color_visual.py 只更新兩份來源內嵌資料。獨立展示頁是另外匯出的快照，
若更新來源，須重新匯出；本次快照與來源內嵌資料已逐份核對一致。
有安裝 visualize 技能的環境，可將 VISUALIZE_RENDERER 設為該技能的
scripts/render.py 路徑後重新匯出：

python3 "$VISUALIZE_RENDERER" "$PWD/work/periodic-triangle-atlas/triangle-crystals.html" "$PWD/work/periodic-triangle-atlas/preview.html" --force
python3 "$VISUALIZE_RENDERER" "$PWD/work/periodic-triangle-atlas/color-periodicity.html" "$PWD/work/periodic-triangle-atlas/color-preview.html" --force

瀏覽器檢查使用 Playwright，優先尋找 chromium 或 google-chrome；也可設定
TRIANGLE_ATLAS_CHROMIUM 指向本機瀏覽器。沒有系統 Chromium 時先安裝
Playwright 的 Chromium。檢查會開啟已保存的獨立展示快照，截圖只保留本機：

uv run --with playwright python -m playwright install chromium
uv run --with playwright python work/periodic-triangle-atlas/check_visual.py
uv run --with playwright python work/periodic-triangle-atlas/check_color_visual.py

核對範圍包含 12 種晶體選取、72 種週期展示、度數／週期框切換、兩格與三格
換色平移、渲染色號與原見證逐點一致、320–780px 版面與 JavaScript 錯誤。
