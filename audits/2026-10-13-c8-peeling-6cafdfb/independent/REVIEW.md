# C8 反覆剝層的獨立覆核

2026-10-13。只在本次隔離目錄的 `independent/` 寫入；未修改上游證據、
原入口、主證明或主校準。覆核版本為同目錄的
`../structure/PROOF.md`、`../TRANSFER.md` 及
`../calibration/certificate.json.gz`。

**結論：採納具名第一層三型、m=10 的完備分類與任意大小完整剝層轉移；
獨立重算全部 m=10 原圖完整 fibres 一致。** 因 m=9 已由 frozen 上游排除，
本輪 m=10 完備候選接回八契約全部 Σ1023，故可採納
`h=3 ⇒ m≥11 ⇒ k≥19`。八項任意大小來源仍 OPEN；一般 h≥4 分支不在此界域。

## 1. 前提核對及任意大小結構

單獨的「每個嚴格內點至多接兩個 C8 點」不足以採納三型。主證明正確保留
原 induced C8、原三角化、C 點 H 度至少四、I 點 H 度至少五，以及
無 occupied C3、C4 cap 空、C5 cap 空或 W5。這些小 cap 事實來源是原
全域最小完整關係來源；本覆核没有把局部 degree 條件當成替代前提。

相鄰雙接點只能是對應原邊的原面第三點 t_i：若另有同接
`c_i,c_(i+1)` 的 x，原三角形包住原 t_i，違反 occupied-C3 排除。
八個 C 點的原 link paths 在 t_i 連接為完整 Q 外面 walk。每個暴露
邊側都對應一個原 C-third-point 三角面，反向原 C-I 邊也見證暴露，
故 `exposed(Q) = original C contacts` 是雙向結論，不只單向附件判準。

在 bounded faces 全為三角面的連通 Q 中，外面同一原點的 occurrences
等於刪去該點後的 components 數。相鄰 t_i 的兩個 link 端點在接合時
合成一次，singleton 一次，正對附件各自產生兩次。因此原 cut vertices
精確是正對雙接點，cut-order 恰二。

兩個不同 antipodal pairs 的 crosscuts 端點交錯，不能同時嵌入。兩個相同
pair 的正對點 x,y 圍成空原 C4；induced C8 排除 C 對角線，迫原 xy
及其兩個 C-third-point 面。刪 C 後 xy 的兩側均 exposed，故 xy 是 Q
bridge。若三個正對點則兩兩都需 bridge，卻成三角形，矛盾。
因此 RING／PINCH／BRIDGE 三型對任意有限大小完備。

每個 terminal disk 除唯一 distinguished cut endpoint 外，boundary 點在
Q 度至少三；若它沒有嚴格內點，三角化 polygon 的兩耳至少一耳不是
该 endpoint，造成 Q 度二矛盾。因此一 pinch 至少 m=11，bridge 至少 m=12。
这是純結構下界；下面真實局部 fixtures 分別達到它們。

主證明新增的 TRIANGULAR-PEEL 引理也成立：刪去某輪全部外面點後，任何
survivor 簡單環內均没有已刪點；其他 survivor component 也不能在該環內
而仍於原連通圖通到已刪外面點。因此 survivor component 的有界面仍是
原三角面。其新暴露邊原本兩側皆是三角面，新暴露側第三點必已刪，
加上孤點例外的直接鄰接論證，得到新外面點恰是接前層的原點。

## 2. m=10 的完備性與來源排除

採納主證明以下窮盡鏈條：

1. PINCH／BRIDGE 被 terminal 下界排除，故只有 RING。
2. 若無非接 C 點，outerplane 耳迫低度；若只有一個非接 C 點，任何
   boundary chord 的空側都有非端點耳，故只能 W9，唯一 singleton 的
   原 H 度卻只有四。兩情形皆排除。
3. 因此恰八個 t_i 加兩個嚴格內點 r,s，沒有 singleton 或正對附件。
4. 有 T chord 時，其每側都需一中心，中心互邊不可能。Euler 及中心
   最低度五迫只有一條正對 chord，兩側各 W5，即 CHORD-4/4。
5. 無 T chord 時 r,s 必有原邊，兩側原面第三點將 T 分成連續兩弧；
   三角化迫完整 fans，最低度五留下 EDGE-3/5、EDGE-4/4 兩類。

固定原 T 標號後，共八個 EDGE-3/5、四個 EDGE-4/4、四個 CHORD-4/4。
兩中心的命名可在整份原圖上一致交換一次；所有 full lifts 重播仍沿
主證書 literal vertex order，沒有逐列或逐 block 重新正規化。

`check_calibration.py` 只讀主證書的 literal edges／faces／vertex order，
不 import 主 generator。它以另一個**固定搜尋次序**重算全部 lifts；次序
在進入搜尋前由已固定頂點及原鄰接決定，不隨色值或分枝改變。
另外從本覆核自己的三個具名 prototype 的旋轉與整圖中心交換辨出全部
16 個 H，獨立用 face dual 切開全部原 C3/C4/C5，逐一驗證空 cap／W5。

| 完整檢查域 | fibres | 空 fibres | full lifts |
|---|---:|---:|---:|
| 16 個 H，全部 274 個具名 C8 色名軌道代表 | 4,384 | 1,500 | 7,408 |
| 16 個 Q，全部 6,564 個 literal T8 proper words | 105,024 | 保留並逐字比對 | 20,832 |
| 16 個 H × 八個原 B–C collars × 十列 | 1,280 | 0 | 75,936 |

所有 lifts（不限 counts 或支援）與主證書逐字相同。128 個接回圖全部
Σ1023，與指定 933／941 完整來源矛盾。因此 m=10 exclusion 的依據是
紙面完備分類及完整原圖染色，不是 target-source 零觸發。

## 3. 完整轉移與具名障礙

採納 T1–T9。其充分性在所有原邊都被檢查：同層原邊由當層 proper pins
檢查，跨層原邊由原 cross-edge kernel 檢查，且任何原邊不越過下一層。
後者可由前層外面角沿被刪頂點及原邊的細管到達 survivor 端點證明。
反向限制把每份 full lift 唯一分到它的下一層指派，故求和實際是互斥
完整 fibre 聯集；没有重計數、另選圖或丟失原附件。

空圖有唯一空 coloring，improper pins 的 fibre 空；這两个終端明確保留。
disjoint components 使用同一 literal 色框的 Cartesian product，articulation
blocks 則使用原同名點的 natural join。若 cut color 未固定，必在同一色值
上求和一次；若已由原邊界指派固定，才可乘兩邊 counts。

`check.py` 獨立構造六個具名原 H，驗證原嵌入的 Euler、全部 halfedge／
rotation、原 C/I degrees、induced C8、C 接點限制、全部小 cap、Q 外面
walk、原 cut vertices，以及其每份固定 C8 指派的完整逐層轉移。
MRV 直接搜尋與原點集合的递迴 natural joins 在全部 274 列逐字相等，
共 **1,644 fibres／3,422 full lifts**；完整 lifts 保存於 `full_lifts.json.gz`。

| 具名局部 fixture | 原圖性質及不能照搬的前提 |
|---|---|
| M10-FAN3 | 兩中心對下一層 T 的附件為四／六；普通 t 的 Q 度三。MULTI-CONTACT、DEGREE-LOSS。 |
| M10-FAN4 | 兩中心各接五個 T 點。MULTI-CONTACT。 |
| M10-CHORD4 | 下一 T8 帶原正對 chord，刪 T 後兩中心分離。CHORD-INHERITANCE、DISCONNECTED-CORE。 |
| M11-PINCH | x 同接 c0,c4；外面 walk 有 x 兩次，兩個 W5 disk 共用同一原 x。OPP-PINCH。 |
| M12-BRIDGE | x,y 同接 c0,c4，原 xy 兩側 exposed；外面 walk 往返 xy。OPP-BRIDGE。 |
| M11-WIDTH | z 只接 c0；Q 外框為九點 `(z,t0,...,t7)`，z 在 Q 度四，兩中心度六／七。WIDTH-9。 |

所有六圖都通過原 C3 空、C4 空、C5 空或 W5 與原 degree 條件。
M11-WIDTH 反駁把第一步之後的 frontier 仍界為八個原點；它沒有證明
任意大小的 frontier 寬度無上界。這六圖皆是**local geometric controls**，
不是任何完整 933／941 全域最小來源；target source status 仍 not triggered。

另保存两个具名負控制：

- **OB-REPEATED-VERTEX-COLOR**：M11-PINCH 左側 x=0、右側 x=1 的兩個
  W5 fibres 分別各有一份完整 lift，若把 walk occurrences 當成兩個點，
  會錯計一份；原同一 x 的 equality delta 使 joint 恰空。
- **OB-SIBLING-MARGINAL**：兩個共享 x 的具名 K4 blocks，左側三個 literal
  葉 pins 迫 x=0，右側迫 x=1；各自有一份完整 lift，但原 joint 空。
  這是 synthetic weakened-join 控制，不是 C8 來源圖。

因此可以任意大小剝層並完整恢復所有原染色，但沒有建立同型 C8 重複規則、
固定八點狀態壓縮或無界來源排除；这些界線與具名障礙已有實圖控制。

## 4. 重播及驗收界線

```bash
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/independent/check.py --check
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/independent/check_calibration.py --check
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/independent/check.py --check --negative
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/independent/check_calibration.py --check --negative
```

默认及 `--check` 只讀，與已保存 certificate／receipts／complete-lifts 對照；
`--negative` 另確認缺一份 literal lift、改一個重複原點名、刪原中心邊等
破壞會被拒絕。正常比較和缺 lift／改重複點名的破壞使用同一個
`compare_expected` validator，由 `expect_rejection` 捕獲真正的
`AssertionError`；刪中心邊則由正常具名類 recognizer 拒絕。
`--write` 僅為本隔離子包的明示重新生成模式。

實際 **normal、PYTHONHASHSEED=17、negative × 两個 checker，共六次重播**
全部 exit 0。每個 negative checker 各捕獲兩個 corruption 的驗證失敗，
沒有把失敗後的非空 marginal 當作通過。逐次 command、exit code、stdout、
stderr 與證據檔 SHA256 見 [VERIFICATION.json](VERIFICATION.json)，原輸出
保留於 `logs/`。上述 immutable 數學產物於完成這六次後停止修改。

任意大小定理的信任來自紙面原面／Jordan／耳／full-fibre 論證；上述有限
重播提供校準與實作覆核。没有新增 Lean 定理，没有用有限零反例證一般型，
也没有將「not triggered」當來源排除。
