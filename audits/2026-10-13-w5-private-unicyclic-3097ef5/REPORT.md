# W5 私人單環來源排除與僅保 Σ 的嚴格縮減

2026-10-13。BASE `3097ef5be241b7777451a5ef8a663f3987d6b866`。
本地研究交付；沒有 commit、push、PR、issue 或外部留言。

**最強結論：在全部目錄外 disk-C5 來源中先最小化內點、再最大化邊數的完整前提下，
對任意合法全內部 induced W5，私人誘導圖的圈秩至少二。**

本輪先證 `ρ(G[P])≠1`，再接既有私人森林排除得到 `ρ(G[P])≥2`。
contractible 分支由任意大小的紙面面計數矛盾排除；環繞 U 分支先完整化約成
七至十點純環，再核對全部 1,652 個必要模板的完整關係均為 1023。
一般性來自紙面完備化約，不來自搜尋到某大小沒有來源。

環繞 U 的完整必要域另有合法同槽位 prism 代表，`r′=0`、`k′=6`，
保持補中心後完整 Σ，減少 `r=7,…,10` 個內點。此代表**只保 Σ，不保 R³**。
它不宣稱適用於圈秩至少二的來源。

## 1. 凍結、來源核對與信任邊界

[BASE.json](BASE.json) 保存指定 BASE、開始時 HEAD、乾淨工作樹記錄，以及
30 份正式輸入的逐檔 SHA-256、bytes 與 BASE Git blob 相等核對。
所有 frozen bytes 均為 BASE 版本；舊 audit、manifest、失敗證書保持不變。
[來源完整審核](review/forest_review.md) 重新閱讀全部指定報告，
不是只取森林摘要。[最終審閱](review/FINAL_REVIEW.md) 再核對新證明及 checker。

| 前提 | 本輪核對與用途 |
| --- | --- |
| 全部目錄外來源中最小 k，再最大邊數 | 沿用共面正規形；不換成固定 mask 最小或 edge-critical 身份 |
| 簡單、二連通、chordless 原 B、內面三角化 | 原 annulus Euler／面式與 link 旋轉的前提 |
| 整圖共同 D5 像的 Σ=933／941；k≥13 | k 界給 r=k−6≥7；完整 Σ 與模板的 1023 矛盾 |
| 所有原內點完整 degree≥5 | 只對 G 使用；私人圖 degree 可以是一、二或更高 |
| 原內點在 B 上至多兩附件，兩者相鄰 | 核讀 deep-five-wheel REPORT §§2,4 的 C4 cap 與邊界 degree 證明 |
| 所有 C4 有界內部無頂點 | 以原中心 spokes 重證每個私人點在 U 上亦至多兩個相鄰附件 |
| 合法全內部 induced W5 | B/U 十 pins 互異；v 的全部鄰點恰為 U；U 內恰有 v 與五個面；A=G−v 保原空面 |
| 無 occupied triangle／proper C5 cap 結論 | 核讀上游，新的主要結構證明不再額外需要 proper C5 cap 限制 |
| 外部計數定理、4CT、K≤12=K≤5 | 沿用正式来源的信任鏈；本輪沒有重跑外部證書或重證上游普遍定理 |

沒有加入 N2 的 edge-critical、ε=2、兩 root 或 Gallai 前提。
實際最小 933／941 來源從未被合成控制觸發，始終標 **not triggered**。
本輪的來源排除由紙面論證加已證完備的有限核心成立。

## 2. 任意大小、全部分量的結構定理

[完整紙面證明](structure/STRUCTURE.md) 保留原 embedding、唯一環兩側、
原樹枝、其他樹分量、所有 attachments、rotation 與原面。以下只摘要關鍵式。

設 F=G[P]，r=|P|，c 為包含孤立點的分量数，ρ(F)=1。
F 恰有一個單環分量，其他為樹；由 terminal 鄰點最多四個及完整 degree≥5，
先排孤立点。令 p 為 B–U 邊數、a 為全 terminal 三角面數、M 為 BUP 面數、
h 為 PPP 三角面數。直接重算原面及 degree 得

\[
e(F)=r-c+1,\quad M=2(c-1+h),\quad p=a+c-1+h,
\]
\[
\sum_{x\in P}d_G(x)=4r+11-c-p,
\qquad r\le11-c-p=12-2c-a-h.
\]

這些公式與森林公式不同，未把森林的 h=0 默默移植。

**Contractible。** 唯一環內無 B/U；若內有私人樹枝或其他樹，其葉無法接外部
terminal，違反完整 degree；故圈內為空，再由三角化與無額外私人環迫它為
facial triangle，h=1。每個三角根若無枝，其至少三個 terminal 附件在外側
link 迫一個 M 面；若有枝，該枝的葉給一個 M 面。三根供應三份不同 M 面。
其餘 c−1 棵樹各至少再給兩份，故 `M≥3+2(c−1)>2c`，與面式矛盾。
此排除不靠有限模板，也沒有刪枝或把 cycle 當 clique separator。

**環繞 U。** Jordan 分隔給 p=0、h=0，所以 a=0、c=1、M=0。
任何附枝有私人葉而迫 M 面，故也不存在。完整私人圖恰是 C_r，且
`7≤r≤10`。原 B–C、C–U 兩層之外沒有遺漏的樹或附件。
兩層必沿同一份完整 C 指派接合；checker 直接枚舉整個 A 和 G，不拼兩側 marginals。

## 3. 有限核心的完備性及全部清單

每個私人環點在 B/U 各有一或兩個連續鄰點，記其原環前進數
`(dB,dU)∈{(1,0),(0,1),(1,1)}`。`(0,0)` 會使完整 degree 四。
原環每條邊只在 annulus 側有一面，且沒有全 terminal 面，故沿私人環一周
每側恰按原次序前進五次，無跳接、倒退、重用或漏邊。
三字母 B、U、D 的數目精確為 `(r−5,r−5,10−r)`。

| r | 全部 linear words | 完整 capped Σ |
| --- | ---: | --- |
| 7 | 210 | 每份 1023 |
| 8 | 560 | 每份 1023 |
| 9 | 630 | 每份 1023 |
| 10 | 252 | 每份 1023 |
| 合計 | 1,652 | 全部接受十列 |

[templates.json](controls/templates.json) 是全部詞清單及逐圖證據雜湊，
[certificate.jsonl.gz](controls/certificate.jsonl.gz) 保存每圖實際完整原邊、
有向面、rotation、B/U pin map、ownership，以及所有完整 fibres。
由 faces 推回 edges、每 dart 恰一次、每點 link 恰一圈、連通與 Euler=2
核對其指定平面 embedding；補中心後再驗一次。

模板與來源之間是原嵌入的整圖具名同構。B/U 起點可以分別移位，但方向符號
共用；私人環、中心及整份 literal 色名同時搬運。沒有 U 單獨換色。
十個固定 beta 及全部 1024 個 tau cells，由同一全圖 S4 搬運涵蓋全部
240 個 literal proper beta。模板全收十列，搬回任何原框方向後仍全收。

完整來源若屬此域，其 Σ 因而是 1023，這本身是原 C5 的目錄關係，與目錄外身份
矛盾。與 contractible 排除及既有 70 模板森林定理合併，得到 **任意合法 W5 的 ρ≥2**。

## 4. 合法代表、保存強度與縮減量

[代表紙面構造](structure/REPRESENTATIVE.md) 給 r′=0 的 prism annulus：
原 B/U 兩環加五條 b_i u_i，有指定 B 外面、U 空面及五個四邊面。
先在原圖的共同座標構造，再用完整 inverse label map 搬回原 pins。
沒有新識別、隱藏接點或交叉；代表不需保持來源三角化或 degree 條件。

任意 proper beta 都能把 U 染在 `{0,1,2}`，同時避開各 b_i 色：
每點 list 是 `{0,1,2}\{beta_i}`；有三元素 list 時最後染該點，否則使用
相鄰不同二元素 lists 的差集選起色，沿剩餘路徑貪婪完成。中心取色 3。
所以代表紙面上全收 beta，完整 Σ=1023。

兩向 total 染色搬運保 B：前向套上述代表構造，反向按同一 beta 從原模板完整
非空 G fibre 選一份 lift，再搬回原來源 labels。這些函數不必互逆，也不保 U
指派或中心色；正確等式只有 `pr_B R_A³=pr_B R_A′³`。

[保存強度證書](controls/strength.json.gz) 有實際反控制：
`BBDDDUU` 的 beta=`01012`、tau=`01031` 可補中心，prism 卻因原 b0u0 等邊
同色而拒絕该 cell。因此不能把此代表稱為 R³ 相等。

對全部 essential 必要核心，`r=7,…,10→r′=0`、`k=13,…,16→k′=6`，
減少 7–10 個內點。**嚴格减少並保持 Σ 已足以違反全域最小性**；不必先達
r′≤6。本構造恰好更強，但不推廣到一般私人含環來源。
contractible 分支用結構矛盾，沒有需報數的代表縮減。

## 5. 完整有限驗證、反控制與回歸

| 新主域驗證 | 結果 |
| --- | ---: |
| 模板／指定 annuli | 1,652 |
| 十列×全部 tau cells | 16,916,480 |
| 空 cells | 16,448,400 |
| 全 A lifts | 657,580 |
| 全 G lifts | 320,840 |
| Σ=1023 | 1,652 / 1,652 |
| 補充實際圖 | 5；51,200 cells；14,380 A／7,260 G lifts |

主程式從 faces 構圖並用 MRV DFS；[獨立程式](independent/check.py) 由
neighbor intervals 構邊，從所有三字母詞按總和過濾，再按固定變數次序直接
重算 A 與帶實際中心的 G。每個 beta 的接受與拒絕 cells、每一份 full lift 全相同。
[獨立報告](independent/REPORT.md) 另核對由 rotation 走出的指定 faces。

- 主、獨立 normal／PYTHONHASHSEED=17 全量重播一致。
- 刪一份必要 full lift（並同步刪中心 lift）、改一條原邊、只反轉 U 面，
  各被兩套 checker 在第一圖拒絕，共六次；詳見 [反控制](independent/negative/summary.json)。
- 同 Σ 不同 R³：prism 與 triangulated prism，以及必要模板與代表，均有真圖反控制。
- 同 R³ 但 fibre 重數不同：prism 二度私人裝飾使每格恰倍增。
- 較弱前提的 contractible 私人三角環、essential 私人五環均合法，分別違反完整
  degree 或 k≥13／proper C5 cap 前提；它們是結構控制，不是來源命題反例。
- 私人純環 d_F=2 而完整 d_G=5 或 6；兩套程式明算兩者，防止誤套 degree。
- [森林及保存強度回歸](review/regression.json) 八條只讀命令全通過，其中森林
  70 模板 normal／seed17 及獨立完整重算一致；保留其 716,800 cells、全部空格和 lifts。

數學重播與日志：[math-verification.json](math-verification.json)、
[獨立驗證](independent/verification.json)、[補充獨立驗證](independent/strength_verification.json)。
文件、正式 docs DocGraph、既有 Lean 與 diff 檢查見 [final-verification.json](final-verification.json)。
Lean build 只作既有專案回歸，**本輪新紙面證明及 Python 核心未 Lean 形式化**。
沒有重跑上游外部大計算，也沒有擴大處理全工作樹歷史 62 項 duplicate-ID 問題。

## 6. 重播與交付邊界

```bash
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/controls/check.py --check
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/check.py
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/controls/strength.py --check
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/strength_check.py
```

上述命令只讀。`--write` 生成器及驗證日志採 exclusive creation，拒絕覆寫。
保留的 negative fixtures 是故意失敗證據，不能當正常輸入。
[DELIVERY.json](DELIVERY.json) 保存全部新增檔案的 hash／bytes，
[CHANGE_SCOPE.json](CHANGE_SCOPE.json) 保存修改清單與 frozen／舊 audit 零漂移核對。
直接入口更新限 W5 專題、Kempe 導覽及 STATUS；README/HANDOFF 研究線未變。

**精確残留：** 真正最小來源仍未實現；若存在，其每個合法全內部 W5 外的私人圖
必有圈秩至少二，可能同時含多環分量與樹分量。對這個剩餘域，沒有證明
r′<r、r′≤6、R³ 小代表或一般同步化約。本次不聲稱 K∞=K≤5 完成。
下一個可反駁窄命題可固定 `ρ=2` 並先區分「兩個單環分量」與「一個雙環分量」，
重新計算 PPP 面及 attachment 預算；本輪沒有執行該搜索或採納其排除。
