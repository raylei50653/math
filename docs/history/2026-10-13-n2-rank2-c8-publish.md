# 廣義 N2、W5 私人雙環及 C₈ 來源結構整理發布

2026-10-13。使用者授權在三份回覆收齊後整理 commit + push。
起點 BASE 為 `243a125a80e4d8de40957f59d8da0bdbc974cf69`；本次整理三份
研究交付、相連入口與原證據封存，不新增來源枚舉或數學主張。

## 採納範圍與保留界線

| 入口 | 本次採納 | 保留界線 |
| --- | --- | --- |
| [N2-BRIDGE](../archive/reports/c5/excess/n2/c5_excess_two_n2_bridge.md) | 原E4完整來源契約的廣義N2排除：父三列域恰多932，以U4三列移植、五列slack、完整分量刪除witness、unit-U排除及UC3修補接回OL／LL | E-ARC2仍OPEN，保留N1、相鄰零mixed、相鄰單mixed四spokes的mixed12＋unit-unary、相鄰單mixed至多三spokes、相鄰兩mixed；各自core／單-root4例外由父ledger維護。932與ε≥3不是原E-ARC2另項義務 |
| [W5 私人雙環排除](../archive/reports/c5/structure/c5_w5_private_rank2.md) | 指定完整最小來源前提下任取合法全內部W5，ρ(G[P])≥3；四型及全部essential位置紙面覆蓋，theta完備化為974模板，四個實際annulus代表嚴格縮減 | 代表只保完整Σ、不保R³，r′=0或4，減少3或7–10內點。圈秩二無殘留，下一域為ρ=3分類與保Σ縮減；一般代表仍OPEN |
| [C8-STRUCT](../../audits/2026-10-13-c8-struct-243a125/REPORT.md) | 原小C4／C5 cap定理、C8無內弦及cofacial識別排c16-941、c32-941；累計62／70排除。可逆Kempe計數使c15／c20-941各迫零兩個完整fibres，173→171 | 933留c15／c18；941留c04／c07／c15／c18／c20／c30。仍缺同一原H跨三组色對的共同分量、交換、原面及完整計數實現；h≥3、n₅≥9不變 |

上述來源排除由紙面證明、完備化約及明列上游／有限核心承擔。
真正最小933／941及完整目標控制維持 **not triggered**；零觸發不是排除。
三份結果均未新增Lean theorem，外部計數與四色定理信任邊界不變。
一般單側／共同出口與 `K∞=K≤5` 仍未證。

## 原證據與本次核對

三份原隔離包共390個非快取檔案、37,263,415 bytes，原bytes、frozen輸入、
舊manifest、seals及成功／失敗紀錄保存。大型產物依既有格式追加7個路徑、
3個gzip blobs，新增3,743,086 compressed bytes；舊ARCHIVE records保持。
新checkout仍先依[封存說明](../../audits/README.md)還原，再重播原checker。
本次命令與結果見[發布核對](../../audits/2026-10-13-n2-rank2-c8-publication-243a125/REPORT.md)。

- N2主／獨立graphs、mask-free U4均normal／seed17通過；算術、T3防錯與偽q₂證書拒絕通過。原U4兩份checker只讀回歸通過；179份manifest檔案與111份frozen輸入相符。
- W5主／獨立及四代表均normal／seed17通過；974模板、9,973,760完整cells及全部lifts一致。八次破損拒絕、局部C6控制與delivery核對通過；13份frozen BASE輸入相符。
- C8主normal／seed17輸出逐byte相同；四份獨立子證書與最終ledger核對通過，偽完整closure及分類／幾何／可逆計數／frozen-hash負控制拒絕。146個manifest payload與59份frozen輸入相符。
- `lake build`通過，8831 jobs；既有warnings保留，不表示新紙面證明已形式化。
- 文件連結／索引、正式docs DocGraph、56項儲存工具測試、staged大型產物policy與Git whitespace通過。
- 390個原payload從Git index／封存在新目錄逐byte還原，SHA256、大小及mode相符；舊2472個路徑及1540個blob records不改。只stage相連白名單。
- 全工作樹DocGraph仍FAIL：62項保留副本／scratch duplicate-ID；與正式docs PASS分開記錄，沒有刪除歷史來隱藏失敗。

N2／W5部分重播僅有工具transcript及明示為觀察摘要的receipt；沒有把摘要
偽稱原始stdout。C8及原U4回歸另有實際stdout／stderr紀錄。
C8 quotient階段的舊向量與最終171列支援分開解讀：舊U-positive敘述不是
最終c15／c20向量全支援的宣稱，原audit不為發布改寫。
未重跑上游來源大枚舉、全部歷史產物生成或外部大型證書，不宣稱遠端CI通過。

## 文件傳播與發布

Closure scope只含上表明列來源域；本輪新增W5雙環正式入口，原audit保持研究截點。
Updated：N2直接父題、原55各入口的後續狀態、W5／外圈直接consumers、
Kempe導覽、STATUS、README與synthesis的目前N2摘要。
Reviewed-unchanged：HANDOFF的研究線與進行中標記、README其他入口、共通語言、
其他研究線及全部舊歷史快照；沒有新事實的層級不產生diff。
Remaining OPEN：E-ARC2五個具名來源、ρ=3及更高圈秩縮減、C8八份共同實現、
十三內點以上一般來源、R³代表與主命題。
Propagation stop：N2收尾影響目前README／synthesis摘要，窄幅到L3；沒有推升父命題。

僅stage相連白名單。推送後核對HEAD、origin/main與遠端main相等，再確認工作樹。
最終SHA及即時發布狀態以Git與本次回覆為準；原audit的「未commit」保留當時語境。
