RSST 構形的幾何接合與染色週期
2026-10-31

rsst-periods.html 是對話內互動圖來源；preview.html 是本機瀏覽器檢查用快照。
可選七份構形、15種HNF週期域、原圓盤／平面拼接及兩方向平移。
圖中區分原色重合、全域換色重合，以及不存在單一全域換色。

完整推理、前提、紙證、有限範圍與OPEN：
../../docs/archive/reports/planar-sources/rsst_geometric_coloring_periods.md

atlas.json 保留來源SHA、633筆目錄、349個固定平衡四邊接縫的全部15個週期
判定及完整SAT指派，另保存七份精確有理數幾何、完整接縫身份、120對置換判定。
所有原邊與跨格邊均保留。未精選342例只做組合接縫及染色，未核對精確幾何。
sources/unavoidable.conf 保存完整來源副本，下載網址與SHA在JSON。

固定四邊方案349例中，126個最小原色週期指數1、223個指數2。這是相對
所選幾何晶格的有限結果，不是所有RSST接法的週期界。七份精選圖有精確平面
三角化核對；Birkhoff diamond六角例與#24有一單元K5商證書、二單元四色見證。
商圖的K5不是無限平面圖的K5子圖；原構形本身是有限圓盤。

重播（repository根目錄）：
uv run --with python-sat==1.9.dev17 python work/rsst-periodic-atlas/generate.py
python3 -I work/rsst-periodic-atlas/replay.py
python3 work/rsst-periodic-atlas/build_visual.py

replay.py不依賴SAT，另解析原檔並重建接縫，用獨立DSATUR核對349個一單元
商及選定七例，重播全部已保存SAT。較大商圖與置換對的UNSAT仍是求解器判定，
沒有形式化不可滿足證明檔。幾何計算以Fraction核對，不是Float64面積測試。
沒有使用四色定理作oracle、沒有新增Lean；C5 Kempe回返題保持原界線。

視覺生成只嵌入必要展示資料。更新後由visualize技能的scripts/render.py
把rsst-periods.html匯出為preview.html，再執行：
uv run --with playwright python work/rsst-periodic-atlas/check_visual.py
visual-checks.json保存105個週期展示、200次平移、七份圓盤與響應版面核對。
