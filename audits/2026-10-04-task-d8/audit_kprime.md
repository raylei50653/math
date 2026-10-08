# D₈ 子稽核：K′ §2 引理 1–6

基準 `integrate-kprime-e3 @ 2ac279b`；獨立 worktree
`/home/ray/developer/ai/math-task-d8`。本子稽核只新增本檔，不改被稽核報告、
checker 或歷史 artifacts，不 commit／push。普通與 seed17 重播由主稽核彙整。

**本項總 verdict：成立。** 在 K′ §1 明列的同一 disk、同一 ψ、同一 split、
`q∉Σ(G)` 與 `p` 的交替 rotation 前提下，引理 1–6 的必要方向有效。
未找到會撤回 L2 篩選或存在性抽取的缺口。這個 verdict 不證 K′ 來源排除：
原報告已保存 933 的 192 筆、941 的 384 筆 L2 存活指派，且明列 K′ 未決。

下列行號指 [K′ 原報告](../../docs/c5_kempe_diagonal_transport.md) 在本基準的
固定 bytes；checker 行號指
[原 checker](../../scripts/c5_kempe_diagonal_transport.py)。

## 1. 前提與六個引理逐格 verdict

| 項目／原引用 | Verdict | 具體核對理由 |
| --- | --- | --- |
| §1：L32–41，固定圖與染色 | 成立 | `B` 是指定 disk 邊界；`p` 是內點且完整鄰集是 `{a,b,z,w}`；四個鄰色互異；`(a,b,z,w)` 或反向 rotation 使 `(a,z)`、`(b,w)` 是交替的對角對。互補雙色 components 全從同一 `G−p,ψ` 抽取；block 是其實際 `C∩B`。 |
| §1：L48–51，critical 接線提供 ψ | 成立 | 任一 `p` 接線是非框邊。Σ-critical 給 `G−e` 新收、而 `G` 拒絕的同一字面框列；限制其完整染色到 `G−p` 有效。若 `N(p)` 不含四色，直接給 `p` 一個缺色即可延拓到 `G`，矛盾。此處是圖的實際存在性方向，未以 mask 中接受一列反推特定染色能延拓。 |
| 引理 1：L63–70 | 成立 | 連通 `a,z` 的實際双色 component 含簡單 `a–z` 路徑 `Q`；`Q` 不含 `p`，加 `az` 的兩條 `p` 接線得到簡單 Jordan 曲線 `J`。交替 rotation 使 `pb,pw` 初段在不同側。另一色對的 `b–w` 路徑不含 `p` 且與 `Q` 頂點互斥；平面嵌入中它不能穿越 `J`，所以不可同時連通。並未用 degree 5、T4 或 criticality。 |
| 引理 2：L72–80 | 成立 | 交換完整 component 保持 `G−p` 的合法性。斷開時交換 `a` 所在 component 不動 `z`，兩點同取 `c_z`，另兩鄰色不受影響，缺色 `α` 可給 `p`；交換 `z` 所在 component 對稱。交換得到的是此份實際染色的完整延拓，故其字面框列在 Σ 中。沒有使用接受列的逆向推論。 |
| 引理 3：L82–87 | 成立 | 框端 component 自含 `a` 或 `b`。若對應 root component 不碰框，引理 2 的該次實際交換保持被拒絕的 `q`，却延拓到 `G`，矛盾。斷開 components 頂點互斥，所以非空 blocks 也互斥；不是只要求兩個 block 名稱不同。 |
| 引理 4：L89–92 | 成立 | `a,z` 連通就是同一實際 component，框交集完全相同；引理 1 迫另一側斷開，再套引理 2、3。此处沒有把「有相同投影」當成同一 component。 |
| 引理 5：L102–115 | 成立 | `J⊂閉 disk`，所以 `B∖J` 全在 `J` 的無界側；`b` 不在 `J`，`pb` 因而在無界側，交替 rotation 迫 `pw` 與 `w` 在有界側。`w` 的互補色 component 與 `J` 完全互斥，留在有界側；它既不能碰無界側的 `B∖J`，也不能碰另一色對的 `J∩B`。其 block 為空，與引理 1、3 矛盾。詳見 §2 的逐步核對。 |
| 引理 6：L117–129 | 成立 | 從同一 ψ 的所有碰框 components 抽完整 partition 與 root ownership；互斥連通 subgraphs 的框接點不可交替，故 π noncrossing。框邊本身給同色對端點 ownership。實際交換由引理 1–4 保證，L2 由引理 5 保證。沒有各 component 獨立色名正規化、marginal 拼接、反向可實現性或圖層 extension fibre 主張。詳見 §3。 |

## 2. 引理 5：Jordan 側別逐步核對

| 步驟／原文 | Verdict | 核對 |
| --- | --- | --- |
| 5.1，L106：`J` 整體位於閉 disk | 成立 | `Q` 是 disk 嵌入中的原邊簡單路徑，`pa,pz` 也是原邊；全部均在指定閉 disk 中。`Q` 可能還碰其他框點，不影響此事。 |
| 5.2，L106–107：disk 外部連通且不碰 `J` | 成立 | 開 disk 外側是連通的無界區域，與閉 disk 內的 `J` 不交。任一 `v∈B∖J` 的小外側鄰域可從 `v` 接到此外部，因此 `v` 在 `R²∖J` 的無界 component。這沒有假設 `J∩B={a}`。 |
| 5.3，L108：`b` 位於無界側 | 成立 | `Q` 只含 `{α,c_z}` 的頂點，`b` 色為另一色對的 `β`；`b≠p`，故 `b∉J`。由 5.2 得無界側，`pb−{p}` 不能跨 `J`，其初段也在無界側。 |
| 5.4，L108：rotation 迫 `w` 在有界側 | 成立 | 在 `p` 的小圓盤中，`pa,pz` 是 `J` 的兩條半邊，`pb,pw` 交替，故分在兩個局部側。已知 `pb` 初段在無界側，`pw` 初段便在有界側；整條 `pw−{p}` 与 `J` 不交，所以 `w` 位於有界側。 |
| 5.5，L109：整個互補 component 留在有界側 | 成立 | 其中每個頂點屬 `{β,c_w}`，與 `Q` 頂點不交，且不含已刪除的 `p`。平面原邊不能與 `J` 穿越，因此這個連通 subgraph 完全包含在同一有界 component 中。 |
| 5.6，L110：它不碰框 | 成立 | 框點若不在 `J`，由 5.2 是無界側；若在 `J`，則屬 `{α,c_z}`，不能屬互補 component。兩種情況覆蓋全部 `B`。 |
| 5.7，L111：與拒絕見證矛盾 | 成立 | 引理 1 迫 `b,w` 斷開；引理 3 在 `q∉Σ(G)` 的背景下迫 `w` block 非空，與 5.6 矛盾。對稱交換兩個對角對可得另側不能連通。 |

**精確依賴註記。** L115 的「只需 disk、四色與 rotation」須在 §1 的拒絕見證
背景下閱讀。5.1–5.6 的純側別／空 block 結論確實不需拒絕性；5.7 的
「所以兩鏈均斷」還使用 `q∉Σ(G)`（經引理 3）。degree 5、T4、criticality 均
沒有進入這段；criticality 只可在尚未給 ψ 時提供 §1 的拒絕見證。這是顯式
依賴整理，不是已找到反例或前提偷換。

## 3. 引理 6：完整 π 的抽取與 noncrossing

| 步驟／原文 | Verdict | 核對 |
| --- | --- | --- |
| 6.1，L119–120：全框 partition | 成立 | 互補色對覆蓋四個顏色，兩套誘導雙色 subgraphs 頂點互斥。每個框頂點在且僅在一個實際 component 中；保留全部非空 `C∩B`，所以形成整個 `B` 的 partition。component 名稱不在抽取時被逐份正規化。 |
| 6.2，L121–122：π noncrossing | 成立 | 假設兩個不同 blocks 有循環交替的四個框點 `a,b,c,d`，分別在互斥連通 subgraphs `A,D`。取 `A` 的簡單 `a–c` 路徑；若它碰到其他框點或沿框邊行走，在與 `D` 不交的細小鄰域內把除端點外的部分推入開 disk，得到與 `D` 不交的簡單 crosscut。`b,d` 位於兩段不同的框弧，Jordan 分離迫 `D` 的 `b–d` 路徑與此 crosscut 相交，矛盾。這補出原文所引用的標準 disk Jordan 步驟；不需假定原路徑只有兩個框接點。 |
| 6.3，L123：框邊 ownership | 成立 | 同一色對的框邊在 `G−p` 的該雙色誘導 subgraph 中仍是實際邊，故兩端在同一 component，不能抽成兩個 blocks。 |
| 6.4，L124–125：root block 與交換 | 成立 | 每個 root 只指派到自己的實際 component 的框交集。空 blocks 用引理 3 排除；相同 blocks 意味同一 component（不同 components 的非空框交集不可能相等），所以同鏈狀態與引理 4 相符。每次交換是實際完整 component 的交換。 |
| 6.5，L125–126：L1、L2 存在 | 成立 | 引理 1 排除雙連通；引理 2–3 供全部必要交換及非空 blocks，得到 L1；引理 5 排除單連通，得到 L2。若 ψ 尚未指定，critical 接線提供它。這只推存在必要指派，不推抽象指派能在原圖實現。 |

## 4. 對照 checker 的範圍

| Checker 引用 | Verdict | 核對 |
| --- | --- | --- |
| `c5_kempe_diagonal_transport.py:30–31,58–71` | 成立 | 逐份枚舉 240 字面 proper 框列、五個指定框方向、剩餘兩色的兩個 root 色序。查 Σ 時才對整列一次共同 S₄ 正規化。沒有先做 D₅ quotient 或對兩側各自改色名。 |
| `c5_kempe_transport_table.py:45–60`；`c5_kempe_screen.py:41–45` | 成立 | π 先由兩色對的完整 partitions 合併，再對同一 π 檢查交替四點與所有同色對框邊 ownership。`combinations(sorted(owner),4)` 的交替所有權正好是圓周 noncrossing 的四點定義；五框方向沒有把 π 拆成 marginals。兩套 generator 的集合相等屬有限組合域檢查，不能代替引理 6 的拓撲論證。 |
| 原 checker L73–105 | 成立 | `a,b,z,w` 的 ownership 共同從固定 π 選定；空 root block 先計入再由引理 3 刪除；相同 block 表示連通；雙連通用引理 1 刪除。每個斷開對都要求兩次字面 block swap 收入 Σ，L2 正好保留雙斷開。沒有要求未必必要的反向延拓。 |
| 原 checker L113–122 | 成立 | 每筆保留字面 q、split、完整 π、四 endpoint blocks、連通狀態、每次必要交換與 L2 理由。全體抽象指派保留同一色框和 joint ownership 的必要資料，但仍沒有編碼全部原圖 root attachments、`zw` 路徑或實際 extension fibres；原報告 L128–129、268–270 明列此限制。 |
| 原 checker L163–222 | 成立 | 控制從同一原 `G−p` 與 ψ 重新算全部實際 chains；核對原鄰集、`ab,zw`、degree 與 rotation；以完整 π 和全部 ownership 找唯一指派，接著交換原 chain 並直接驗完整 `G` 染色。這是圖層正控制，而非只驗 mask membership。 |
| 原 checker L225–244、308–350 | 成立 | 1012 的 `P1-witness-001` 與 935 的兩份拒絕 ψ 都被重抽並要求 L2 存活。建表仍有 933／941 存活；輸出明寫 `Neither fixed-source exclusion nor Kprime is proved`。普通及 seed17 的實際 exit code 另由主稽核記錄。 |

## 5. 缺口清單與影響範圍

本項沒有發現必須保存的失敗重現，也沒有要求撤回 E3「(i) 完成」的結果。
K′ 原有的未決部分仍保留：必要 π／ownership 存活不保證在同一 disk 內同時
實現 `p` rotation、`zw` 和全部 root attachments；八頂點有限搜尋沒有找到目標
Σ 不能升格為任意大小不可實現。這些是原報告既有的停止界線，並非本次新增缺口。

引理 5 的依賴註記與引理 6 的路徑內推說明可作閱讀上的補證方向；兩者均可由
原本明列的前提完成，不改任何被稽核文件，也沒有將拓撲引理冒稱為 Python 或
Lean 證書。
