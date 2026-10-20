# 完整 r6／941 三輪進展整理與發布

2026-10-19。使用者已明確要求「整理目前進展並 commit + push」。本次將
BASE `13dc5ff163045c85b5c82dde438eb5f275dab999` 後的三輪相連研究證據、
直接導覽與驗證紀錄一起發布。原報告所記「沒有 commit／push」保留為
各輪封存時的歷史狀態，不改寫任何已封存數學證據。

## 1. 本次交付的進展

量詞固定為完整 r6、原 `(p,h)=(p,ell)` 五度位置、原完整支持恰941的
同一任意大小真來源；原附件、所有私有點、完整 stars／旋轉、原短圈
定理與全域最小性均保留。不加入 active-f matching 假設。

| 輪次 | 已證結果 | 原證據 |
| --- | --- | --- |
| 原 c 四度與商圖計數 | 排 c=4，得 c≥5、q≥6、共同 C10 induced；兩接受合計 `a1+a2=2Aa>0`，兩重色洩漏合計 `U1+V1+U2+V2=Ab>0`，成功候選若存在必唯一 | [quotients](../2026-10-19-r6-941-quotients-13dc5ff/REPORT.md) |
| 低度與接受零分支 | n=5⇒a≥7、c=5⇒q≥7；原圖 dist(t,R)、dist(L,s)≥3；定位接受零的實際二色連接義務；兩份精確整數控制證既有必要計數條件仍不足 | [acceptance](../2026-10-19-r6-941-acceptance-13dc5ff/REPORT.md) |
| 原 cap、同染色分量與五圖支持 | 五個私有共鄰排除、另四組原圖距離界；完整接觸60→46格，四接觸僅兩型且全圖至多一點；c=5 的 H1 支持恰1022，五圖共同支持僅八個必要型；接受零的同染色分量型及三邊路原五度輪已分類 | [chains](../2026-10-19-r6-941-chains-13dc5ff/REPORT.md) |

原有序框始終為 `(x,y,a,b,c)`。c=5 的 H1 明確是
`(G-c)+qx+ux`，新有序框 `(x,y,a,b,q)`，完成內點數 k−1；新框列
不冒充原框列。五種補片的「五邊形」僅為組合索引，虛擬閉邊 bx
不是原邊，也未加入任何 Hi；實際操作從刪 c 後的七圈外面開始。

每個 cap product 都固定同一完整核心著色，含空 fibres 與全部 lifts。
五圖的共同支持假設同時約束同一核心向量；八個存活型不是八份實現。
獨立整 cap 回溯已核對14,766份完整 fibres、10,784份 lifts及147,660格
字面係數；新一輪發布重播另保存在 [replays](replays/receipts.json)。

## 2. 精確停止點

同一接受候選的三拒絕仍未完成：

```
(a1>0 and T1=U1=V1=0) or (a2>0 and T2=U2=V2=0).
```

嚴格較小 bad、單獨 n=5／c=5 排除、一般 allK 來源實現、普遍位置存在、
其餘完整319、`W110+W101>0`、`omega_e=0` 與一般 K∞ 均仍 OPEN。
H1 的1022與其他比較的1023皆在 K132；尚不供較小 bad。C11 的四個
短路邊界未被必要介面排除，不能宣稱最短二色路至少五邊。
本次沒有新 Lean theorem；一般 K≤22、固定 r6 的 k≥25 不變。

下一個窄入口是以指定原 L／R 五度輪的完整關係處理三邊路，或在原
c=5 的同一核心上合用 H1=1022及五圖八型。現行排程與入口維護於
[Kempe 導覽](../../docs/c5_kempe_guide.md)，直接索引見
[STATUS](../../docs/STATUS.md)。README／HANDOFF 的研究線與使用方式未變。

## 3. 發布範圍與證據保全

[SOURCE_FILES.json](SOURCE_FILES.json)逐份記錄三輪原 audit 與兩份直接
導覽共244份檔案、9,794,270 bytes 的當前 SHA256。發布驗證、暫存與
提交前後都核對此清單。
本次不修整已封存檔案、失敗證書、原始 log 或舊 routing 快照。
錯誤 C11 零索引探索、修正前 source／certificate gzip 及原始失敗收據
全部保留，正式修正版本與其效力邊界亦保留。

僅暫存三個 audit、直接 STATUS／Kempe guide 與本發布目錄。沒有納入
其他研究線、工具或 Lean 原碼變更。發布前獨立唯讀審查確認原來源契約、
封存 SHA、換框與成本、OPEN 邊界及相連範圍，未見阻斷問題。

## 4. 驗證與重播

三個正式根 checker 各跑正常與 `PYTHONHASHSEED=17`，包含原負控制；
逐對核對 stdout 相同，並核對所有原輸入與輸出 SHA 零漂移。命令、
退出碼、時間與輸出 hash 見 [replays/receipts.json](replays/receipts.json)。
另以故意損壞的 chains seal 確認 checker 拒絕 SHA 漂移。

發布工程檢查包括 `lake build`、文件、docs 範圍 DocGraph、全樹
DocGraph 基準比較、實際暫存索引的生成產物政策及 whitespace 檢查。
工程收據及完整範圍見 [checks.json](checks.json)。全樹 DocGraph 的
歷史例外按原72項 error multiset 比較，不將既有失敗誤報為全樹通過。
工具與 Lean 原碼未改動，不重跑無關單元測試；build 成功不代表本輪
紙面幾何與 Python 介面已形式化。
