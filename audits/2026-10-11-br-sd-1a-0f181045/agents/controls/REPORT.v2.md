# BR-SD-1a：獨立有限 list／原邊校準

## 結果與嚴格範圍

本 checker 核過 **31,296** 個具名 tight degree-list assignments；全部保存完整逐點列表與完整 coloring tuple，全部可著色。最小 `C-333-arms-00` 的 **31,104** 列是完整枚舉，另兩個較大／正臂圖各核 96 個明列 ranks。這是有限 list／原邊校準，**不是任意大小紙面定理的有限證書，也沒有 actual BR-SD-1a target disk source**。

- 有限 degree-list 控制：`triggered and holds`。
- unused-D、原鄰居／原邊重建及 full-lift 控制：`triggered and holds`。
- removed-D 負控制：`triggered and holds`；撤去具名 w1 的 D-presence 後確實不可著色，並不是來源合同的反例。
- actual BR-SD-1a disk／拒絕來源：`not triggered`；target source 數 0，不以零觸發承擔來源排除。

三個 synthetic M 僅供實際逐邊語義校準。其 ordered induced C5 frame、proper literal 三色 beta、內點 degree 4／5 與指定 C 形狀已核；**disk embedding 未供／未宣稱**，Sigma-criticality、所有身份／ownership／rotation 未供，beta-refusal 與 beta-minimal core 明確為 false。

## 原 C 邊與有限域

顏色按 literal 順序 `A,B,C,D`，certificate mask 的第 i bit 表示此顏色；D 的 index 為 3。所有 row 為 `[逐原點list masks, 逐原點完整color tuple]`，順序由同一 fixture 的 `vertex_order` 明定；不是 marginals，也没有独立重新规范化组件。

| C | 原 odd cycles | 外臂長 | 完整 tight list 域大小 | 本輪核查 | 結果 |
|---|---:|---:|---:|---:|---|
| C-333-arms-00 | 3 / 3 / 3 | 0 / 0 | 31,104 | 全部 31,104 | 全部 colorable |
| C-533-arms-00 | 5 / 3 / 3 | 0 / 0 | 1,119,744 | 96 個 ranks | 全部 colorable |
| C-333-arms-11 | 3 / 3 / 3 | 1 / 1 | 221,184 | 96 個 ranks | 全部 colorable |

域的精確定義：每點列表大小恰為其從原 C 邊計算的 degree_C，w1、w2 的列表均含 D；其他列表沒有額外假設。尤其 s-contact 的列表在此抽象枚舉中沒有強制排 D，故此控制域比 beta-derived D 列表域寬。較大圖只抽樣，不宣稱完整域已全部檢查。抽樣公式為 `rank_i = floor(i * (total-1) / 95)`（0≤i≤95），全部具名 ranks、全部逐點 options 留在證書。

最小圖原 edges：J1 是 `r-a1-a2-r`，J2 是 `r-u-b1-r`，J3 是 `v-c1-c2-v`，唯一環間原 bridge 是 `u-v`。J1／J2 同一 r，u、v 各保其原私有點身份。5-cycle 控制將 J1 改為 `r-a1-a2-a3-a4-r`。正臂控制新增原 edges `a1-p1`、`c1-q1`，兩個 s-contact 分別是 `p1`、`q1`；零臂則是 `a1`、`c1`。

每圖的完整原邊、全部 blocks、arms、逐點原鄰居及每個點刪除後的全部 components 都留在證書。原 blocks 另以 Tarjan edge-block 演算法從原邊重建，不能只以提供的 block 名稱假定。原 C 割點以每點刪除後的連通分量數直接重建：零臂為 r/u/v，正臂再含 a1/c1。

從原資料逐點選取 w1=a2、w2=b1，兩點均非 C 割點、非 s-contact、degree_C=2；所有原 C／s edges 明列。對每列 degree-list，若假設存在 blockwise-uniform 的拒絕證書，其 J1、J2 palette 分別被兩個 private w 的列表強制，而且兩者交集含 D。這個必要條件核了每列；實際可著色結論另外由不讀舊 solver 的直接 vertex backtracking 找到完整 coloring，並逐原邊驗證。

三個控制的 backtracking nodes 總數分別為 287,564／1,098／1,056。此統計是 checker 的搜索節點計數，不是外部一般定理證明。

## 撤去 D 的具名負控制

同一 `C-333-arms-00` 的 block palettes：

- J1 = {A,B}
- J2 = {C,D}
- 原 bridge uv = {A}
- J3 = {B,C}

r 的兩 cycle palettes 互斥且聯集是四色；u 的 J2／bridge palettes、v 的 bridge／J3 palettes 也互斥。逐點列表按 incident block palettes 的聯集定義，恰有原 degree_C 大小。

| 原點 | 完整列表 |
|---|---|
| r | A,B,C,D |
| a1,a2 | A,B |
| u | A,C,D |
| b1 | C,D |
| v | A,B,C |
| c1,c2 | B,C |

兩個 s-contact a1/c1 的列表均排 D；w1=a2 是 noncut、noncontact，卻沒有 D。這正是 deliberately removed 的前提：在 actual unused-D beta-derived 原列表中，noncontact a2 必保留 D。負控制沒有這個來源性。它保存逐點全部原鄰居、各 incident palettes、完整列表及 empty 完整 coloring fibre；獨立 backtracking 窮盡後為空（33 個 nodes）。不可把此 list-only 拒絕當 actual disk source。

## 同一 synthetic M 原邊的 list／full lift

每個 C 都使用同一 ordered frame `B0..B4` 及 beta = `(A,B,A,B,C)`。從原 M 邊補 boundary attachments 至 r 完整度 4、s 完整度 5、其他 C 點完整度 4；s 保原兩 C contacts，以及原 B0/B1/B4 三 spokes。原 G 額外 spoke r-B2 明列，刪此同一原 edge 得 X=M。這些補邊不是合同來源存在性主張。

每個 C 點的全部原 M 鄰居、實際 B attachments 與 beta 色、s 原邊有無、M/C degrees 及 `L^D=Col-beta(N_B)-{D if original s edge}` 都完整保存。逐點核 `|L^D| >= degree_C`，w1、w2 均含 D。

四 s queries 使用固定 beta 的 C-B 與原 s-C 限制，暫不施加 s-B spokes；證書保全部完整 C coloring fibres。再次施加原 s-B 後，只能 s=D，其完整 M-beta lift fibre 都恰有 **32** 個完整全圖 tuples，逐原 M 邊核過；並另保存一個完整全圖 assignment 及全部原邊的兩端色 witness。

| C | s=A | s=B | s=C | s=D | 原完整 M-beta lifts |
|---|---:|---:|---:|---:|---:|
| C-333-arms-00 | 56 | 16 | 32 | 32 | 32 |
| C-533-arms-00 | 56 | 16 | 32 | 32 | 32 |
| C-333-arms-11 | 128 | 128 | 32 | 32 | 32 |

因此三個 synthetic M 都不拒絕 beta，明確沒有進入 target 合同。此部分只核同一原邊／unused-D 語義及完整 assignments，沒有只核四個布林值便宣稱來源等价。

## 重播與完整產物

唯一程式 `checker.py` 使用 Python stdlib，不 import 舊證書或 repo solver。寫入以 `open('xb')` exclusive-create，正常／seed17／損壞證書均保留。每次 `--check` 先直接核所有 row 的完整 lists／assignment／原邊，再完全重新計算預期證書，要求 canonical bytes 相等。

從工作目錄 `/home/ray/developer/ai/math` 執行：

```sh
python3 audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.seed17.json
python3 audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.corrupted.json
```

前兩條 exit 0；第三條預期 exit 1。新一代生成用 `--write --certificate <尚不存在的新檔>`，不可覆寫原證書。實際 seed17 generation／checks、normal check 與 corruption check 完整 commands、環境 seed、stdout／stderr／exit code 留在 `replay-log.json`；各 log 另存獨立檔。

normal、seed17 各 **1,388,989 bytes**，完全 byte-equal，SHA256：

`7379e65f205108360fa5afb910dc85f78f257bc99837a09eb71ba724b77888e8`

損壞證書把最小圖第一列第一個 coloring entry 由 0 改為非法色 index 9，保持 JSON 可解析；完整 witness 檢查拒絕，exit 1。此損壞證書及 failure log 保留，沒有刪除／修補。`HASHES.json` 列本目錄其他所有交付檔的 exact bytes／SHA256（manifest 不自雜湊）。

此子工作只寫本 agents/controls 專屬目錄；未改 authority／共享／舊檔，未 commit／push。任意大小紙面證明、外部定理依賴與 target 身份採納由主 audit 分別核查；本有限產物沒有擴充那些 claim。

代次說明：本 REPORT.v2.md 為已核準確的文字代次；原 REPORT.md 保留，其中負控制原色誤寫 1，實際 replay-log.json 是 0。本代次只修正此文字，不變更 checker 或任何證書。
