# 圈秩二有限核心與代表的獨立重算

BASE：`243a125a80e4d8de40957f59d8da0bdbc974cf69`。
[check.py](check.py) 不 import 主 checker，也不 import 代表程式。
最後正常與 `PYTHONHASHSEED=17` 兩次完整執行均 exit 0，輸出逐 byte 相同；
指令、UTC 起始時間、耗時及 log SHA-256 見 [verification.json](verification.json)。

## 1. 獨立算法與完備參數核對

主程式逐位置選合法字母，再取所需 terminal triangles 的排列；獨立程式
先從四字母 Cartesian product 篩完整 degree，再從 B/U/P 的 Cartesian
product 篩 region 配額，最後核對兩環總前進量各五。得到同一組 974 個
完整參數 keys，拒絕缺項、重項與額外項。

原邊獨立由每個私人點的 B/U 鄰點 interval、backbone 邊、diamond 五條
核心邊及 B-U cross edges 重建，沒有由主程式的面資料產生邊。
逐圖比對全部 literal 邊、十個 pins、私人 labels、分量及 degree 資料。
再獨立沿 rotation 的 darts 走出所有面，核對指定 B 外面、U 空內面、
Euler、連通性、單一 vertex link 所給的完整面分解，以及補中心後的面。
私人 degree 與完整 G-degree 分開計算。

染色以固定 vertex 次序的 DFS，直接分別枚舉 A 和實際含中心的 G；
主程式使用動態 MRV，兩者沒有共用求色函數。所有十個 beta 代表、每列
全部 1024 tau 格（含空格）、每個完整 A lift 及 G lift 均逐一相等。
沒有只比 masks、計數、獨立 marginals，亦沒有只由 A 的投影代替直接 G DFS。

| (c,r,a) | 模板數 |
|---|---:|
| (1,7,0) | 42 |
| (1,7,1) | 88 |
| (1,7,2) | 104 |
| (1,7,3) | 52 |
| (1,8,0) | 141 |
| (1,8,1) | 136 |
| (1,8,2) | 58 |
| (1,9,0) | 172 |
| (1,9,1) | 64 |
| (1,10,0) | 70 |
| (2,7,0) | 12 |
| (2,7,1) | 20 |
| (2,8,0) | 15 |
| 合計 | 974 |

總計 9,973,760 cells，其中 9,762,297 空格；344,416 個完整 A lifts、
167,814 個完整 G lifts。Σ 分布精確為 1023：970 份，639：2 份，
959：1 份，1021：1 份。不能把此結果改寫為「全部模板 Σ=1023」。

## 2. 四份實際代表與嚴格縮減

另獨立重建 prism 的兩個 C5、五條 matching 邊及五個 quadrilateral 面。
另外三份 r′=4 diamond 代表仍以原鄰點 interval 重建全部邊；四份代表
均核对實際面、rotation、十 pin map、U 空面與補中心圖。
固定次序 DFS 重算四代表的 40,960 格，包括 40,028 空格、1,059 個 A lifts
及 551 個 G lifts，與封存代表證書逐份相等。

對全部 974 份模板的每一 beta row，checker 核對來源與所選代表的空／非空
一致，以及兩方向 selector 確實是該 **同一 literal beta** 下的完整 G lift。
每個非空 fibre 上取這份固定 selector，就是該方向的 total map；空 fibre
沒有輸入。它保每個 B pin，但容許 U 和中心的顏色改變。這只證完整 Σ
保存，不是 R³ 保存、fibre 等勢或保中心色。

每項另核對 r′<r、k=r+6、k′=r′+6 及減少數：四份例減少 3 內點，
其餘分別減少 7（314 份）、8（350 份）、9（236 份）、10（70 份）。
Σ=639、959、1021 分別使用 r′=4 代表；Σ=1023 使用 r′=0 prism。
保存強度證書中「Σ 相同但 R³ 不同」的實際 beta/tau cell、空／非空與
完整非空 lift 也已核對，狀態為 `counterexample`。

## 3. 紙面與有限驗證邊界

本 checker 驗證 **紙面已界定的全部有限必要模板**，不自行證明來源的
無界覆蓋。任意大小的四型覆蓋、環位置排除及原 rotation 的 strip 分解
分別見 [TOPOLOGY.md](../structure/TOPOLOGY.md) 與
[STRUCTURE.md](../structure/STRUCTURE.md)。獨立讀核這兩個證明後，
原面計數及 diamond contour 的兩次 B/U 切換可給出所用參數域，沒有
把有限沒有反例外推為無界命題。

四份較小合法代表與原 pin map 搬運相接，保 Σ 且減內點，故在完整
全域最小來源前提下排除最後 theta 域。此結論不要求代表繼承來源的
最小 degree、三角化或目錄外身份。

真正最小 933／941 來源仍為 **not triggered**。紙面排除與模板完整驗證
不能記成實際來源已觸發；既有外部 K≤12 的信任邊界沒有重新證明，
本包沒有新增 Lean theorem。

本 checker 的 `--certificate` 及 `--representatives` 可指定反控制輸入；
`--limit 1` 先完整檢查首圖資料，僅略過最後全域覆蓋與代表驗證，故損壞
首圖的拒絕可定位於原邊、pin、面或 full-lift 核對，不須依賴提早 EOF。
反控制的雙 checker 執行結果由本包 controls 負責保存。

```bash
python3 -B audits/2026-10-13-w5-rank2-243a125/independent/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank2-243a125/independent/check.py
```
