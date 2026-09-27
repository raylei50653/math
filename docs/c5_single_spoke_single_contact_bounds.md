# Single-spoke：剩餘單接點上界與 root 接線分類

2026-09-27。接續 [二接點上界分類](c5_single_spoke_two_contact_bounds.md)
留下的 16 個 `open_queries`；研究優先序見 [HANDOFF](HANDOFF.md)。

**16 個查詢全部關閉。** 未知單接點分量均有 `F_C(p)⊆{3}`：12 個 p₁
查詢可固定 **z=2**，4 個 p₂ 查詢可固定 **z=0**。因此原表 114 筆全部
接受兩個指定 target。這是上界及延拓分類，不是 `F_C(p)={3}` 的斷言，
也不證明 19 支援型可實現、完整單缺失或一般 single-spoke 出口。

## 1. 前提與保留資料

沿用 [completion §1](c5_single_spoke_completion.md#1-前提與保留的完整關係)：
有限簡單 induced-C5 disk，連通有效內部 H，edge-minimal q=01012
obstruction，唯一完整 degree-5 點 z，唯一 spoke zb_s，其餘內點完整
degree=4，H−z 分拆 (2,1,1)，來源接受 T4。C₀ 保持原有序二接點，
C₁、C₂ 各有一個原 root。各分量、actual supports、全部邊及 placements
都沿用原表，沒有把二接點的完整 relation 換成 marginals。

16 筆各只有一個單接點分量 C 的 target 上界未知；它在 q 禁 3，支援
為 1234（p₁）或 0124（p₂）。兩列在該支援都不用色 3。
前置 R10／既有 K4 排除給 bridges、odd cycles 的 Gallai block tree；
拒絕時為 tight degree lists，具有 incident palettes 的不交聯集證書。
此處沿用外部 degree-list 定理，不新增外部定理或圖枚舉。

## 2. 未用色在單 root 的禁色角色守恆

**引理。** 同一單接點分量 C、root r，若 a∈F_C(q)、d∈F_C(p)，
且色 c 在 q、p 的 actual support 都未出現，則

```
a=c  ⇔  d=c.
```

證明：比較同圖兩份拒絕 lists M=(q,z=a)、N=(p,z=d)。每個 v≠r
沒有 z 邊，兩份 lists 都含 c。將原 block-cut tree 以 r 為根，沿用
[root 守恆引理](c5_single_spoke_root_conservation.md#2-單接點固定色引理)：
從葉 block 向根，取非 parent 頂點，從 list 扣去已決定的 child palettes。
兩份 lists 的 c membership 相同，child palettes 對 c 相同，故 parent
palette 對 c 也相同。既存證書保證同一 block 不同選點一致。
最後 root 的 incident palettes 聯集對 c 相同，因此 M(r)、N(r) 對 c
相同。root 的實際 boundary 鄰點都不用 c，故兩者分別在 a≠c、d≠c
時含 c，得到結論。若 C={r}，兩份 tight lists 為空，也給同一結論。

歸納保留任意深度、分叉、odd-cycle 長度及中間 bridges。這裡使用同一
守恆引理的另一方向：舊 sweep 用 a≠c 排除 d=c，本輪用 **a=c 迫使 d=c**。
取 a=c=3 即得 **F_C(p)⊆{3}**，不需要其他分量的路徑或新 minor。

## 3. 實際 root 接線的完整局部分類

令 A=N_B(r)⊆S_C。原 root 只有一條 z 邊且完整 degree=4，所以
`deg_C(r)=3−|A|`。本輪 |S_C|=4；若 deg_C(r)=0，由 C 連通得 C={r}，
其 actual support 應等於 A，與 |A|=3 矛盾。因此 **|A|≤2**。

| root boundary 邊數 | deg_C(r) | incident block degree 大小 |
| ---: | ---: | --- |
| 0 | 3 | 1+1+1 或 1+2 |
| 1 | 2 | 1+1 或 2 |
| 2 | 1 | 1 |

1 表示 bridge、2 表示任意 odd cycle 在 r 的 degree 貢獻；不是圖大小上界。
所有 root 邊仍是來源原邊，不把 C 的全支援當作 r 的直接鄰點。

每種四點支援的 16 個 A 子集分成：

- |A|=4：超過 degree 預算，一個子集。
- |A|=3：孤立 root 無法提供四點 actual support，四個子集。
- |A|≤2 且 q(A) 重色：q slack，違反 q 拒絕，一個子集。
- q(A) 異色但 p(A) 重色：target slack，直接得 F_C(p)=∅，一個子集。
- 其餘九個：root tightness 尚可能，§2 給 F_C(p)⊆{3}。

| S_C / target | q 重色 pair | target slack pair | 其餘可保留 A |
| --- | --- | --- | --- |
| 1234 / p₁=01021 | {1,3} | {1,4} | ∅、四個 singleton、{1,2}、{2,3}、{2,4}、{3,4} |
| 0124 / p₂=01212 | {0,2} | {2,4} | ∅、四個 singleton、{0,1}、{0,4}、{1,2}、{1,4} |

若任一非 root 頂點也有 target 同色的兩條 boundary 邊，同樣由 slack
給 F_C(p)=∅。不需要列舉那些接線，因 §2 已涵蓋全部剩餘來源。
九個 root 候選不是九種 disk 正常形，也不宣稱每個候選可實現或必禁 3。

## 4. 全部 16 筆的同色框接合

下表支援依 q 禁色角色遞增排列；a₀ 是二接點分量的 q 禁色。
每對 index 只交換兩個單接點分量名字，artifact 仍各別保存原 placements。

| s | 支援（依 q 角色） | a₀ | target | source_index | 若拒絕則 C 必禁 | 可固定 z |
| ---: | --- | ---: | --- | --- | --- | ---: |
| 0 | 01 / 04 / 1234 | 1 | p₁ | 2,7 | {2,3} | 2 |
| 0 | 01 / 04 / 1234 | 2 | p₁ | 12,19 | {2,3} | 2 |
| 1 | 01 / 04 / 1234 | 0 | p₁ | 32,43 | {2,3} | 2 |
| 1 | 01 / 04 / 1234 | 2 | p₁ | 54,66 | {2,3} | 2 |
| 4 | 23 / 34 / 0124 | 0 | p₂ | 106,126 | {0,3} | 0 |
| 4 | 04 / 01 / 1234 | 0 | p₁ | 110,132 | {2,3} | 2 |
| 4 | 04 / 01 / 1234 | 1 | p₁ | 139,159 | {2,3} | 2 |
| 4 | 23 / 34 / 0124 | 1 | p₂ | 153,174 | {0,3} | 0 |

其餘兩分量的已知完整關係投影與 spoke 都不阻擋最後一欄。未知 C 的
F 上界只有 3，故該欄 z 色也不被 C 禁。固定原 target 與同一 z 色後，
在每個原分量選一個所有接點避開 z 色的完整 tuple 及其 coloring，再接合。
二接點分量的两座標一直來自同一 coloring；沒有獨立乘接點 marginals。

另有獨立的容量核對：C 是單接點，R_C(p) 非空（root 在未刪 z 色的
lists 有一色 slack，按生成樹向 root 貪婪著色）。若 R 有至少兩種 root
色，F=∅；若 R 只有一色，F 是該 singleton。因此 |F|≤1，已不能同時
禁表中兩色。此較弱論證也關閉全部查詢，但只有 §2 給上述固定 z witness。

反射沿用既有全圖／完整 relation 搬運；不重枚舉反射來源。
`Tp₁=21010`、`Tp₂=02012` 的字面列與 z 色 π(z) 一起保存，不把它們
悄悄換成另一個 target 而仍固定 q。

## 5. 重播、證據與停止點

[checker](../scripts/c5_single_spoke_single_contact_bounds.py) 與
[artifact](../artifacts/c5_single_spoke_single_contact_bounds/observations.json)
保存輸入 SHA256、16 筆繼承記錄、兩組各 16 個 root 接線子集、所有候選
z 色的 tightness／membership 核對，以及全部 15 個非空 unary relations
的容量核對。其中 12 個符合 F⊆{3}，僅是必要關係選項，未證可實現。
另重播既有 root induction 的 2,632 個非 root 及 1,340 個 root 局部核對。
任意大小覆蓋由 §2 歸納承擔，不由這些有限局部檢查承擔。

信任層：紙面任意大小證明＋沿用外部 degree-list／既有結構＋Python 局部
代數與表接合。沒有新增 Lean theorem；`lake build` 不形式化本輪歸納。
原 sweep／二接點 artifacts 保持不變，新表為 **114 both、0 open_queries**。

```bash
python3 scripts/c5_single_spoke_single_contact_bounds.py --check
python3 scripts/c5_single_spoke_two_contact_bounds.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
python3 scripts/c5_single_spoke_root_sweep.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際驗證見 [本輪紀錄](history/2026-09-27-single-spoke-single-contact-bounds.md)。
(2,1,1) 的既有 114 筆指定雙列查詢已完成；其餘 t=1 分拆 (4)、(3,1)、
(2,2)，t=0、高 degree／多 degree-5、一般核心存在／分離、一般單側／共同
出口及 K∞=K≤5 仍保留。未從指定兩列延拓推論完整 Σ 或全部單缺失。
