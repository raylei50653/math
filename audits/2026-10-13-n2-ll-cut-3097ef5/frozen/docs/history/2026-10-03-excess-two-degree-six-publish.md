# 2026-10-03：ε=2 唯一 degree-6 分支成果整理與發布

使用者要求「整理目前進展 commit + push」。接手基準 `4701f4c`；
fetch 後 `main=origin/main`，工作區含 t=3／t=0 的四份新 checker、
四份小型 JSON 證書、兩份合成報告、兩份研究紀錄及相關入口更新。
本次整理完整證據包、同步全線整合頁及後續涵蓋關係，完成檢查後
提交推送。提交 SHA 與遠端同步以即時 Git 為準，本紀錄不自含 SHA。

## 完成範圍與證據界線

前提是 933／941 固定完整 Σ（或整圖 D₅ 像）、每條非框邊 Σ-critical、
induced-C₅ disk 外框、ε=2、唯一完整 degree-6 root，其餘有效內點
完整 degree 四。原 H−r 分量、有序 contacts、全部原邊與實際附件、
ownership、同一嵌入的環序及同一字面四色框保持。

| 分支 | 本批完成範圍 |
| --- | --- |
| [t=3 全三分拆](../c5_excess_two_three_spoke_complete.md) | (2,1) 十份具名 span-two 配置／8,250 同源 S₄ profiles 無目標；(3) 的 100 容量比較及 (1,1,1) 六跨度矛盾完成整型 |
| [t=0 全十一分拆](../c5_excess_two_no_spoke_complete.md) | 多分量的真實外部路徑恢復跨度與容量論證；(6) 飽和兩原 K₄ 給 K₅；(4,2) 的 200 查詢先留 7,200 弱 profiles，再由 160 同源原 binary 路徑框弧 K₅ 證書全排 |

連同前序 t=1、2 及 T4 的 t≤3，唯一 degree-6 的 ε=2 分支全部排除。
**同一來源若 ε=2，只剩兩個完整 degree-5 roots。** 共同下界維持
ε≥2，未提高為 ε≥3；雙 roots（含 mixed、相鄰／非相鄰）、一般
來源、一般單側／共同出口與 K∞=K≤5 仍保留。

任意大小來源化約、Gallai／block palettes、實際 tethers、共同支援
與 Jordan 次序由紙面及報告明列外部依賴承擔。Python 核對固定
必要域、具名 minor skeletons、完整 ordered-tuple fibers 與接合；
不證抽象 profiles 的 disk 實現。完整 relation 的 marginal 碰撞
保留，未將各原分量獨立正規化。未新增 Lean theorem。

## 本次實際重播與產物

下列八份 checker 均以 `PYTHONHASHSEED=17`、`--check` 通過，直接
比對保存證書，沒有重新生成或覆寫 observations：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_spoke_reduction.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_spoke_four_two.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_spoke_exterior.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_five_contact.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_ternary_binary.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；不表示新紙面 topology 已形式化。大型產物檢查
`ok=116`，無 missing／changed／stale。

四份新增 JSON 分別為 binary 838,735、ternary 145,786、reduction
369,116、four/two 800,759 bytes，各低於 1 MB，直接隨 producer
提交；其 producer／直接依賴 SHA256 與完整 bytes 由 `--check`
核對。未修改大型產物 MANIFEST、依賴或 `.gitignore` 政策。

本次未重跑全部前序 t=1／t=2、原省略、歷史來源 catalogue、
全 degree-4／Gallai 有限證書、R-series、weak-deletion／Kempe
closure 或 Lean axiom audit；前序證據按各報告範圍沿用。

README、STATUS、Kempe 導覽及全線整合頁同步；舊報告與研究紀錄
加後續連結，保留當輪證據及未提交語境。HANDOFF 的研究線與
進行中標記維持，依文件治理保留薄索引。

文件檢查通過 466 份 Markdown、4,811 個本地連結及 anchors／index／
handoff；DocGraph 通過 62 documents、213 relations、5 families，
零 errors／notes；`git diff --check` 通過。

## 停止點與接手摘要

目前停止點由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)
維護；本次發布沒有推進雙 degree-5 的新研究。

```text
工作目錄 /home/ray/developer/ai/math；先讀 docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md，再讀 t=0／t=3 合成報告與本發布紀錄，查即時 Git。
933/941 固定完整Σ、edge-minimal induced-C5 disk、ε=2、唯一 degree6
的 t=0/1/2/3 全分拆均排除，T4 迫 t≤3，完成整條唯一 degree6 分支。
若 ε=2，只剩兩個 degree5 roots；共同 ε≥2 不變，不能提高為 ε≥3。
八份 hashseed17 checker、lake build、產物及文件檢查通過；紙面+Python，
沒有新增 Lean theorem，沒有證一般出口或 K∞=K≤5。
下一窄入口先核對相鄰雙 degree5 的既有共同分離對兩候選完整Σ的
適用範圍；保留 mixed/no-mixed、原接點、actual supports/ownership、
所有同源完整 relations 與同一字面色框。指定列出口不等於完整來源排除。
停止於可證窄排除或具名必要殘留，不重開來源圖 catalogue。
```
