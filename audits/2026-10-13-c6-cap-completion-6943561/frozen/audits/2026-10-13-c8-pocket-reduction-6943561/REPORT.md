# C8 共同 gadget：六至八新點的 pocket 化約

2026-10-13。Git BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`。
接續使用者指定的 [前輪報告](../2026-10-13-c8-joint-gadgets-6943561/REPORT.md)。
直接輸入來自當時工作樹，已凍結在本獨占包；未提交的舊 audit 不被宣稱
已存在於 BASE。詳見 [INPUTS](INPUTS.json)。

**六至八新點的未覆蓋域已再收窄：同一 C8 空側、只識別原 boundary pins
的合法共同 gadget，七、八新點皆能化回既有 signed 五點域；六新點只需
保留一個 C6 無弦 cap，六私人點在 cap 內均度至少五。**
其私人核心再分為六點 maximal outerplane 型或含 deep W5 中心型。
這是拒絕 U 方法的結構化約，沒有新來源排除；八項及主命題仍 OPEN。

## 1. 精確域與不變的來源契約

沿用全域最小目錄外 C5 來源的 k；本 h=3 分支有 k≥19。原 H 恰有 k
個總頂點，外面是同一具名 induced C8，所有至多 k+5 點的 loopless
planar 圖可四色。八份 U 保留原 274 rows、具名接點與 literal 色框。

本輪只处理同一 exterior disk 中共同可畫的 boundary-pin 識別與普通
圖邊限制。識別淨省 d、收縮後私人點 a 的預算為 `a−d≤5`；不操作其他
原 H 點，不把別的原面或 list constraints 當作已覆蓋。更一般的 scaffold
重構接口見 [獨立紙面覆核](review/PROOF_REVIEW.md)。

引用前輪 signed 五點完備域時仍保留 plantri 完備性依賴。本輪没有重新
生成該 334,512 圖域或重播其兩億份 lifts；使用其 frozen 結論。新的
pocket 拓撲、C4 單向強化與 degree-four 化約由紙面證明負責。

## 2. 為何七、八新點不再是新缺口

[完整證明](theory/PROOF.md)把原 C8 商環保留為 plane cactus，digons 的
兩條平行原環邊仍保留。其 d+1 個 pockets 長度至少二，總和恰為八。
不同 pockets 的私人點互異，全部 joins 固定在同一原 row 上。

C2／C3 的 proper boundary 指派只有一個 S4 orbit，相對可染性給每份
指定 row 延伸，故可清空私人點。C4 在 **s<k** 下的七個完整 masks 各
含 W4 或一條對角線的完整關係，所以為了空交拒絕可強化成至多一點。
C5 在 s<k 下有原 K132 的至多五點精確代表。

| 識別淨省 d | pocket 長度 | 替代後私人點上限 |
| ---: | --- | ---: |
| 1 | 3+5 | 5 |
| 1 | 4+4 | 2 |
| 2 | 2+2+4 | 1 |
| 2 | 2+3+3 | 0 |
| 3 | 2+2+2+2 | 0 |

替代 pieces 按原 pin map 展開回 C8，再同點集三角化；同 block 新 chord
標 Eq，其餘標 Diff，收縮後不產生 loop。得到的完整關係包含於原 gadget
關係，且在既有 signed 五點域內。該域與每份 U 相交，故原 gadget 亦相交。

因此唯一尚需處理的高點型是 **d=1、a=6、2+6**，六私人點全部在 C6
pocket。若 digon 有私人點，清空後 C6 已至多五點。這不把各 gadget
的成功列合併，也不證 U 是真正來源的完整關係。

## 3. 六點 C6 再縮為兩個私人核心型

C6 cap 可以在同點集三角化。私人點度至多三可刪；四度點可刪並在原
露出面內識別一對沒有邊的鄰點。其商圖染色能在**同一 row**接回原 v，
並且只剩四或五私人點；兩個 boundary neighbors 合併時也保留全部原
C8 names 與 pin map。原 H 的 C8 induced 性使原 H 不產生 loop。
所以這些候選均回到已測域。

任何 C6 boundary chord 又切成 C3+C5 或 C4+C4，使用上述代表也能降到
至多五點。因此下一域只需 C6 無弦、六私人點全度至少五的三角化 cap。
這些度數是 **輔助 cap 的不同鄰點數**，不是未證的下一層原 H 度數。

[核心獨立覆核](review/CORE_REVIEW.md)確認 Euler 計帳給 `eII+eIB=21`、
`eII≥9`，再分兩型：

1. 每私人點都接 C6：私人核心繼承 outerplane drawing，迫 `eII=9`、
   `eIB=12`，每個私人點的 cap-degree 恰五；核心是六點 maximal
   outerplane graph，核心最大度至多四。
2. 至少一私人點不接 C6：它恰接其他五私人點，原 rotation 給 deep
   W5。鄰環外側可有 chord，尚未證 induced，亦未證中心唯一。

這兩型的全部實際接線與完整 cap relations 尚未分類／排除。外圈平均
度四不能改成逐點最低度四；不能直接 cone 後套十三點 min5 球面控制。

## 4. 小型完整控制與下一輪具名介面

[證書](controls/CERTIFICATE.json.gz)及 [逐項結果](controls/RESULTS.json)
保留完整 tuples 與空 fibres：

- 全部 Bell(8)=4,140 partitions 中合法者 91；另一份 set-block 枚舉及
  獨立 rotation face walks 核對全部 pocket profiles。
- C4 七份具體代表共 588 literal fibres；在全部 84 proper 指派上核對
  所選較強關係包含。這裡保存的是代表的 lifts，不是假造未知原 pocket
  的 full lifts，也不聲稱原／替代 counts 相等。
- 四個正對 Eq 接點、49 組有序 C4 代表，共 196 控制；直接全圖與同列
  pocket join 比較全部 53,704 fibres，其中 45,896 空，19,592 full lifts。
  包含四份 (14,14) 的六私人點控制；1,568 個 U 查詢全部非空。
- 下一域的八個短 Eq 恰為 `b_i=b_(i+2)`。每份保留 92 個原 canonical
  C8 rows 與 2,196 literal rows，轉到全部 31 個 C6 rows，保存完整
  原 row preimages、digon pin 色值及共同 colour bijection。每份 U
  的空 preimage fibres 均明列；不能只留下 C6 support mask。

C6 長 pocket 的具名順序是
`(b_i,b_(i+3),b_(i+4),b_(i+5),b_(i+6),b_(i+7))`。
原 `b_(i+1)` 仍存在於 digon，與 shared pin 異色；私人 tuple 必依此
literal frame 還原。這套介面足供下一輪在兩個六點核心型上核對完整
gadget，沒有聲稱已取得未知原 H 的 C6 full lifts。

[独立 checker](controls/independent_check.py)不 import producer，使用
另一份 partition 枚舉、directed-edge face walks、全圖 `4^a` 指派及
literal-to-canonical 重建；正常、seed17 與實際破損證書控制的命令及
出口碼見 [VERIFICATION](VERIFICATION.json)。

## 5. 證據與停止點

紙面：pocket/cactus 重構、C4 子關係、低度四及 boundary chord 化約、
六點私人核心二分。有限：上述 91 partitions、具體 C4 代表及同列 full
joins、完整 C8→C6 preimages。既有 plantri 依賴：引用 signed 五點域的
無拒絕結論。原來源：沒有新增 exclusion 或 realization，目標未觸發。
Lean：未新增形式化，未跑舊 build 充當本輪驗證。

全部九份 frozen 輸入未漂移，八份即時數學輸入未漂移；共享交接文件有
並行更新，已分別記錄其 live hash，本輪仍使用 frozen 版本，見
[INPUT_DRIFT](INPUT_DRIFT.json)。新工作只寫本包；未修改前輪 audit、
共享文件或舊證書，沒有 commit／push。

**下一個窄任務：只檢查八個短 Eq 的具名 C6、六私人點、無弦、最低度五
cap，從六點 maximal outerplane 核心與 deep W5 核心兩型出發，逐份保留
實際 attachments、rotation、完整 fibres 及原 C8 pullback。**
這一步若仍無拒絕，才可進一步宣稱此 boundary-pin-only gadget 方法的
全部預算域已用盡；本輪尚未得到該結論。其他原 H 點識別、其他原面
以及原圖幾何收緊 U 仍是另外的 OPEN 入口。

八項仍保留；無界 932／933／941 與一般 `K∞=K≤5` 均 OPEN。
