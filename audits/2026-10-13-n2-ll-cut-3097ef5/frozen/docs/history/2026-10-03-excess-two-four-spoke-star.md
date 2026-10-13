# 2026-10-03：四-spoke binary 原 star 的同源扇區排除

接手使用者指定的原 a-spokes=012、b-spoke=0、S_C=012、S_U=234，
基準 `b63a0965434d68a28292994638b2c98e848585b8`，工作目錄
`/home/ray/developer/ai/math`。保留前輪 singles／binary 的未提交成果；
本輪未要求也未執行 commit／push。

## 結果與本輪證據

[新報告](../c5_excess_two_mixed_core_four_spoke_star.md)與
[checker](../../scripts/c5_excess_two_four_spoke_binary_star.py)先關閉指定
入口：原連通 C 與 a 都接 b₀、b₁、b₂，加外側 apex 給 K₃,₃ minor。
所以不需在這份不可能的原支援上推導跨列 palette 等式。

更強的原 star 必要條件：同一原 W=H−a（b、整份 C、整份 U）
連通，S_C∪S_U∪{s} 必包含於原 a 的一份閉框弧扇區。既有
116／256 份具名必要域分別排除 84／192 份，保留 **32／64** 份。
所有殘留只含 K pair schedules；941 的 24 份 singleton／pair
schedules 全在本輪排除內。沒有完成 binary 整型排除或 ε≥3。

每份排除有可重播的八點 minor、K₃,₃ branch 頂點及九條路徑。
原 C 已違反扇區的 268 份另保存 C-only minor；212 份三共同鄰點
型使用九條直接邊。372 次 root 交換保存完整 query assignments；
3,720 次整體 D₅ topology 搬運核對。原 frame、候選、support、
完整 schemas、lifts、原 assignment／來源身份全部保留。
收縮只用於 topology，沒有把原完整 relation 換成 hub 顏色。

24 張新原完整 degree 圖包括 x=y＋bridge／triangle 旁支及長度
2、4、6 的 C 偶數 path；U contacts 不同，保留其長度 1、2、4
的 path。保存 actual attachments 與整份 C／U coloring tuples，
C 在 q=01021 恰為對角 pair；核對 connected branch sets、九個
原鄰接與 W 收縮的 exact edge image。這是固定圖證書，未稱
候選 Σ、criticality 或 disk。未開來源圖枚舉，未新增 Lean theorem。

## 實際驗證與產物

新 checker 以 `PYTHONHASHSEED=17` 及預設 seed 各作 byte-check。
原 binary checker 用前輪已記錄的唯讀 networkx 3.5 cache 重播：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check
python3 scripts/c5_excess_two_four_spoke_binary_star.py --check
PYTHONHASHSEED=17 PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f python3 scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

原 binary 重播包含 720 次完整 joint、11,520 pinned 纖維、144 份
同色省略等式，以及原 `(2,2)` 的完整數學 payload／support table
核對。它仍保存一項 docs hash 漂移；原 byte-check 的差異未修正，
原產物未改寫。新 checker 保存這份 inherited audit，重算 audit
由上述原 binary 重播承擔，兩者分開標示。

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings，未形式化本輪紙面 topology。本輪未重跑前序
singles、全線九份雙 root checker、唯一 degree-6 各分拆、歷史
catalogue／Gallai／R-series／weak-deletion 或 Lean axiom audit。
文件檢查通過 491 份 Markdown／5,032 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
產物 status 為 `ok=128`，無 missing／changed／stale；`git diff --check` 通過。

HANDOFF 的研究線與 tag 未變，維持薄索引；README、Kempe 導覽、
STATUS、全線整合及前序 binary 報告同步後續入口。新 observations
按大型產物政策留在本地，MANIFEST 保存 bytes／digest、producer
與依賴，沒有覆寫前序證書。

新 observations 為 **9,453,034 bytes**，SHA256
`650d8fdf6f9e97bae8761a85f974afc407c313dbbee20ece2e566b7b418b3a89`。

## 停止點與跨對話摘要

```text
cwd=/home/ray/developer/ai/math；先讀docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md及docs/c5_excess_two_mixed_core_four_spoke_star.md。
保留b63a096上的前輪未提交工作樹，本輪未commit/push。
原入口a-spokes012、b-spoke0、S_C012、S_U234已由原C/a/apex的K3,3排除。
同一H-a=b+C+U的連通star扇區條件，將933/941必要域116/256縮至32/64，
含root交換；276逐域subdivisions、372 root交換、3720 D5 topology核對。
24固定完整degree圖保存C/U完整tuples與minor提升；保留x=y/原旁支。
殘留全含K pair schedule，原C精確對角pair／偶數bridge仍沿用。
下一入口a=6,b=5,a-spokes012,b-spoke2,S_C04,S_U234；
原933 frame4/941 frame12、domain24，q01021的C/K pair及U禁1。
W support0234在閉框弧2340；尚未證同圖跨列palette或來源實現。
原binary重播720 joints/11520 pinned fibres與舊two_two完整數學payload/table；
一項舊docs hash漂移仍保存，未覆寫原artifact，未新增Lean theorem。
新重播：PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check。
binary整型、ε≥3、一般出口、K∞=K≤5仍未證。
```
