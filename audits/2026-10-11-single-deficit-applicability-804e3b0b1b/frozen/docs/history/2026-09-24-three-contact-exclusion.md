# 2026-09-24：兩-spoke 三接點的同圖 K5 排除

成果見 [完整證明](../c5_two_spoke_three_contacts.md)。本輪從相鄰 S={b0,b1}
的 (3) 核心出發，保留同圖三接點、六邊形區域與實際 boundary attachments。
兩個 q 禁色的 block palette 差強迫一個 triangle 加三條同 parity bridge
arms；三個 triangle 頂點各有實際 boundary tether，連同 z 的 spokes 給
K5 minor。證明其實排除全部兩-spoke (3)，不需第二拒絕或 T4。

第二三色列仍以同一 boundary 標號核對；其 palette 差只能使用同一 signed
active blocks。沒有以各列獨立 marginals、二接點分類或全圖枚舉代替證明。
18 個 (2,1) 配置仍開放；603 profiles、固定點及既有 artifacts 沒有改寫。

實際驗證：

- `python3 scripts/c5_two_spoke_three_contacts.py --check`：63 個 local states、
  512 次 parity 控制、80 份具名 K5 branch-set 證書、四個第二列 attachment tables。
- `python3 scripts/c5_degree5_two_spoke_sectors.py --check`：原 80 配置重播通過。
  原 24 個保留項目是舊必要篩選的輸出，不代表本輪之後仍有 24 個未解。
- `python3 scripts/c5_unattached_boundary.py --check`：480 改色、5,120 signature
  檢查通過；原 23 個未解同樣是當輪記錄。
- `uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check`：
  108 個局部控制、32 個舊 disk witnesses、7,680 boundary rows、30,720
  fixed-z checks、19,200 deletion checks、384 switches 通過。
- `lake build`：8,823 jobs 通過，只有既有 lint warnings。
- `python3 scripts/check_docs.py` 與 `git diff --check`：通過。

信任層：紙面任意大小證明＋外部 degree-list characterization＋Python 局部
證書。未新增 Lean theorem；build 不形式化本輪 palette 差／minor 論證。
未重跑大 graph catalog、R 系列大覆蓋、3703、完整 deletion audit 或固定點。
研究完成後依使用者要求整理 commit＋push；publication 階段補上 README 入口，
重跑文件檢查與 diff 檢查；研究 replays 與 Lean build 沿用同一工作階段上述通過結果。
發布 SHA 與 clean status 以實際 Git 核對為準。
