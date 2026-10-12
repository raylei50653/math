# 任務 C：兩外框接點的 C5＋C5 cap 閉合

2026-10-12。隔離研究包；BASE：`bc7c0820e6b5e585869b8a59e04f52da0dad2d33`。
任務來源為凍結的 [任務文件](frozen/docs/tasks/c5_degree5_link_tasks.md)之任務 C。
本包只處理下述具名位置，不依賴任務 A、B 的新成果。

**任務 C 已完成：全部 17,424 組有序 cap pairs 的完整外圈關係均在 K，共有
66 種輸出。** 結合下述原圖適用性與兩向 full lifts，得到：在 BASE 的已採納
前提下，全域最小目錄外來源不可能含有此指定 C5＋C5 cap 位置。
這是此子域的條件排除，不是一般 `K∞=K≤5` 的證明。

## 來源、同色框與計數

原外框固定 `B=(a,b,c,d,e)`，原 degree-5 點為 `v`，循環鄰環
`L=(a,x,c,y,z)`。四個點 `x,y,z,v` 為互異原內點；原 rotation 指定兩 cap
為 `P=(a,b,c,y,z)`、`Q=(a,x,c,d,e)`。原來源是在所有 `Σ∉K` 圖中先最小化
內點、再最大化邊數者，並沿用 BASE 的近三角化正規形。

五個原三角面先給中心 disk；Jordan 分離再給兩個 cap disk，禁止私有頂點的
跨 cap 邊。若兩 cap 私有內點數為 `p,q`，則 `k(G)=p+q+4`，兩 cap 各自均較小，
所以由全域最小性得其完整關係屬於 `K`。更換成凍結 literal representatives
後 `k(H)=k(P')+k(Q')+4≤14`。本包不以 `K≤12=K` 代替這次閉合核對。

每個原外框列 `β=(A,B,C,D,E)`，同時枚舉 `X,Y,Z,V`，要求

\[
(A,B,C,Y,Z)\in R_P,\qquad (A,X,C,D,E)\in R_Q,\qquad
V\notin\{A,X,C,Y,Z\}.
\]

每個有效 joint block 的兩份 cap 完整 fibres 作 Cartesian product，接上相同的
九個具名點，即為完整全圖 fibre。空 block 及十列空 fibres 均有明確語義。
替換的兩向 full lifts 保持相同 pins 與外框列，不主張新舊 fibre 基數相等或雙射。
完整適用性與條件排除證明見 [PAPER.md](paper/PAPER.md)。

## 固定有限域

使用 BASE 上游 cofacial v2 證書與原 checker 指向的 132 份 literal witnesses。
所有引用輸入及 SHA256 見 [INPUTS.json](INPUTS.json)，原證書只讀重播紀錄見
[upstream-replay.log](logs/upstream-replay.log)。凍結來源、具名邊界映射與全部
`132²=17,424` 有序 pair 在計算前凍結於 [DOMAIN.json](controls/DOMAIN.json)。
完整證據為 [certificate.json](controls/certificate.json)，重播程式為
[checker.py](controls/checker.py)，編碼與逐份展開方式見
[controls/README.md](controls/README.md)。

獨立關係實作 [independent_join.py](review/independent_join.py) 不匯入主 checker；
它先展開 24 個色名置換，再作共同指派。完整 pair 表見
[independent_join.json](review/independent_join.json)。關係層重播得到 66 種輸出，
全部在 `K`，完整介面 tuples 合計 657,432。主 checker 另外從 literal 邊集
做全圖 MRV 回溯，與 cap 完整 fibres 的 Cartesian product 逐份比對。
獨立審查也核對所有 pair 的完整 joint digest，兩份實作一致；詳見
[INDEPENDENT.md](review/INDEPENDENT.md)。

| 有限項目 | 實際結果 |
| --- | ---: |
| 有序 cap pairs／外框列數 | 17,424／174,240 |
| 共同 `(X,Y,Z,V)` joint blocks | 657,432 |
| 與 literal DFS 相同的完整全圖 lifts | 2,606,752 |
| 明確保存的空外框列 | 24,082 |
| 各 cap 的具名 proper 色指派 | 每份 240，包含全部空 fibres |
| 輸出關係種類／目錄外 pairs | 66／0 |
| 實際重建圖最多內點／輸出代表最多內點 | 14／5 |
| 兩 cap 同時帶 `ac` 的 pairs | 49 |

每個 pair 保存 actual literal edges、原九點及 private vertices 的 ownership、
cap 到全圖的 label 字典、edge rotation、全部 faces、十列 joints 與接受列的
literal 全圖 witness。所有 cap fibres 已完整保存；每個 joint block 指代其中
**整個** Cartesian product。未列為 block 的共同指派為空，解碼規則沒有選取
單一私有 lift 代替完整 fibre。

嵌入由具名中心骨架的面與兩份 cap 內面逐一接合，核對 Euler、原外框 face、
原 `v` 的循環鄰點及五個三角面，再獨立核對抽象圖平面性。49 組雙 `ac` 先按
各自 cap 的 rotation 放置兩條邊，保留 P 邊、刪除 Q 邊；只刪重複的異色約束，
不改完整著色。新圖在簡單化後仍有原外框及原 star rotation。

全部 66 種輸出的代表索引與 `k_eff` 見 [OUTPUT_RELATIONS.tsv](OUTPUT_RELATIONS.tsv)。
索引為 `DOMAIN.json` 中遞增 mask 目錄的零起算位置；`k_eff` 沿用凍結目錄的
最少內點代表欄位，沒有重做最少性搜尋。每個有序 pair 亦在證書中直接指向其代表。

## 重播、負控制與驗收

一般重播及 `PYTHONHASHSEED=17` 加上 `--seed 17` 的順序擾動重播均通過。
六種破損資料均由同一 checker 拒絕：漏 pair、漏外框列、錯 pair label、
使原 spoke `va` 同色的錯 full lift、錯中心 rotation、漏 cap full lift。
負控制只修改記憶體副本，正式證書保持原樣；重播入口為
[check_negative_controls.py](check_negative_controls.py)，精確結果見
[NEGATIVE_CONTROLS.json](NEGATIVE_CONTROLS.json)。

以下從 repo 根目錄執行；本機 `.venv` 為 Python 3.14.7、NetworkX 3.5。

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python audits/2026-10-12-degree5-c5-c5-cap-dcdad039/controls/checker.py --check
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17 .venv/bin/python audits/2026-10-12-degree5-c5-c5-cap-dcdad039/controls/checker.py --check --seed 17
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python audits/2026-10-12-degree5-c5-c5-cap-dcdad039/review/independent_join.py --check
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python audits/2026-10-12-degree5-c5-c5-cap-dcdad039/review/compare_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python audits/2026-10-12-degree5-c5-c5-cap-dcdad039/check_negative_controls.py --check
```

完整執行紀錄與輸入／工作區漂移核對見 [VERIFICATION.json](VERIFICATION.json)；
13 份凍結輸入的位元組漂移為零，原先 74 份暫存路徑及 index diff 未變，詳見
[CUSTODY.json](CUSTODY.json)。包內檔案雜湊見 [MANIFEST.json](MANIFEST.json)。

| 命題或控制 | 狀態 | 精確意義 |
| --- | --- | --- |
| 全部 17,424 組 C5＋C5 關係閉合 | `triggered and holds` | 有限固定目錄域全數通過 |
| Literal disk、rotation、完整 fibres 與獨立全圖著色相等 | `triggered and holds` | 每 pair 全十列，不是 pair marginals |
| 雙 `ac` 簡化 | `triggered and holds` | 49 個實際正觸發；保留 P 的嵌入邊 |
| 六種破損證書拒絕控制 | `triggered and holds` | checker finding 測試，並非數學反例 |
| 指定位置的原最小來源排除 | 紙面條件定理＋上述有限證書 | 原圖分解、全域最小性與完整關係替換給出任意大小適用性 |
| 933／941 實際最小目錄外來源 | `not triggered` | 未提供或推得任何此類 literal 圖 |

本固定域沒有發現閉合命題的 `counterexample`。

## 依賴與停止點

- BASE 的 132 關係目錄、literal witnesses 與採納的必要 screen，作為上游前提；
  本包不重證目錄的普遍完備性，也不搜尋任意大小圖。
- BASE 的必要 screen／外側 disk 黏合使用四色定理；`K≤12=K` 的上游推導依賴
  外部 Dvořák–Lidický 結果。此次不重播其外部計算證明。
- 真正 933／941（含整圖 D5 像）的最小目錄外來源沒有 literal witness，
  來源控制為 `not triggered`；本分支條件排除須由紙面適用性與非空的全部
  17,424 組有限閉合共同推出，不能由零來源控制推出。
- 本輪沒有新增 Lean theorem，也沒有執行 Lean build；Python 有限核對與紙面
  拓撲證明各有邊界。
- 本包不處理 C4＋C6、只碰一外點、全內部 link，或 degree-5 點是否迫出本位置。
  `paper/PAPER.md` 的 OPEN 清單是相對凍結 BASE 的剩餘範圍；一般十三內點以上
  來源及 `K∞=K≤5` 並未由本包關閉。

收尾時觀測到共用 `docs/tasks/c5_degree5_link_tasks.md` 與 `docs/STATUS.md` 已有
本包之外的並行更新，指向新的 `c5_neartri_boundary_collar.md`，並以 crosscut
結果另行排除此來源位置及 C4＋C6。當時的任務頁仍註記 132² joins 未執行。
本包沒有採用該新結果為前提；本包完成的是原 BASE 明訂的完整有限 cap 命題及
其獨立來源推論。觀測快照與 live/frozen 差異列於 `VERIFICATION.json`，沒有回寫
或撤銷並行共用文件，也不把凍結 BASE 的 OPEN 清單當成新文件的即時狀態。

本輪只在專屬研究包寫入，沒有修改共用文件或舊證書，沒有 commit、push、PR
或外部發布。工作區先前暫存狀態另記於 `WORKSPACE_BEFORE.txt`、`SHARED_BEFORE.json`。
