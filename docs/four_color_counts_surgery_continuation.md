# 計數與手術續進：共同切口的排除力及完整分量的迭代反例

2026-10-29。接續[計數錐／手術驗證](four_color_counts_surgery_verification.md)。
本輪得到一個可具體檢驗的切入點：**兩份外部配對必須共用同一切口側別**。
它能排除一個通過 B5、全部真實交換及逐態 noncrossing 的具名 932 假模型。
同時，真實 disk 反例否定「保存三份全部具名頂點分量就能迭代更新」這個補法。
一般平面 932 排除、有限充分 state 及 4CT 仍 OPEN；沒有新增 Lean 定理。

## 1. 一個比任意邊際更強、仍然不足的反模型

沿用 [B5 face 報告](c5_b5_face.md) 的 R5,12，內點為 `0,…,4`，terminal 為
`e0,…,e4`，spoke 為 `i–ei`，內邊為 `i–(i+2 mod 5)`。
terminal 的指定環序是 `(e0,e1,e2,e3,e4)`。這是同一張帶標號的五角星 5-pole，
**不是此環序的 plane disk**；沒有把必要模型當成平面來源。

新 [checker](../scripts/four_color_counts_face.py) 列舉其完整 Tait 邊染色空間：

- 恰有 30 份完整染色、30 個不同 boundary words；XOR 積分的支援恰為 932。
- 三色對的全部 90 份系統，各自的 boundary pairing 都 noncrossing，cycle counts 皆零。
- 從同圖實際路徑讀取 signed signatures，所得十個正共同權重逐項等於原驗證的 `y=1`；
  全部 180 條標準 B5 等式成立。這次不再分開替每列選 matching。
- 全部 150 條有向單分量交換都是同圖合法交換、可逆且仍在這 30 態內。
  150 份不變系統與 300 份 mixed 更新均符合既有抽象重接公式。
  因為已列盡每態全部分量，歸納可得任意長有限交換歷史仍閉合。

所以，即使加上**共同原圖、真實交換、全部歷史閉合及每態三份 noncrossing 配對**，
也不能補出共同 disk 嵌入。這比單份 B5 可行向量更強地定位了來源缺口。
抽象重接在這裡通過；共同側別／切口幾何未包含於該抽象公式。

### 不依賴 4CT 的非 disk 證明

若上述標記 5-pole 可放入指定 disk，沿外側加入 terminal 環 `ei–e(i+1)`，
便得到平面 Petersen 圖。此圖有 10 點、15 邊、無橋且 girth 為 5。
兩個五環本身沒有短圈；含兩條 spokes 的四圈要求同一對 index 同時相差
`±1` 與 `±2`，不可能；含至少四條 spokes 的圈至少八邊。
因此若平面，Euler 給 `F=7`，每面至少五邊，卻有 `2E=30<5F=35`，矛盾。

證書另以每條邊的最短替代路核 girth／無橋，並列盡 1,024 份 orientable rotations：
genus 1／2／3 分別 40／664／320 份，無 genus 0；五角柱有明確 sphere faces 作正控制。
這個有限拓撲核對與上述紙證分開；都不使用 4CT。

### 固定五環的全部 port orders

獨立 [port-order checker](../scripts/four_color_port_order_obstruction.py) 從普通五環 pole
的同 30 份完整染色出發，核全部 120 個 terminal orders，共 10,800 份雙色系統：

| 指定環序 | 有標號 orders | 模 dihedral 的類數 | boundary 支援 |
| --- | ---: | ---: | ---: |
| 真正沿內五環的 disk order | 10 | 1 | 91 |
| 每態三配對都 noncrossing，但不是 disk order | 10 | 1 | 932 |
| 至少一態有 crossing，且不通過 D | 100 | 10 | 各列另存證書 |

前兩列正是普通五邊形與五角星的次序。這是**一張固定 pole 的完整分類**，
不是一般 C5 來源分類。它顯示保留 terminal 環序與逐系統 noncrossing，
仍不保證原 pole 的三套系統有共同 disk 嵌入。

## 2. 共同切口能排除這個具名假模型

本節沿用[既有 ordered surgery 的共同側別條件](c5_dual_path_surgery.md#2-精確交換公式與共同必要限制)，
新增的是對第 1 節完整反模型的排除證書，**不是首次證明 crosscut 引理**。
精確條件如下。

固定一份 plane near-cubic disk 的 proper Tait 染色。令 S 為一條完整雙色
boundary-to-boundary 路徑，內點都在 disk 內部。沿 S 的路徑順序記切口 ports
`t0,…,t(m−1)`；S 內每點的第三色邊只有一條。
從兩個 mixed 系統各刪 S 的原邊，得到兩份實際外部配對 E1、E2。
它們須滿足同一份側別指派 `σ(ti)∈{0,1}`：

1. 每個未切 boundary terminal 的側別，由 S 兩端切出的 boundary arcs 決定。
2. E1、E2 中每條外部路徑的兩端都在同一側。
3. 在每一側，依 S 的 ports 順序與該側 boundary arc 組成切開後的環序，
   E1 自身 noncrossing，E2 自身也 noncrossing。

**紙面 soundness。** 簡單 S 是 disk crosscut，其補集分兩側。每個 port 的同一條
第三色邊在兩個 mixed 系統中有同一側別。任一外部路徑不穿 S，故不能接通兩側；
同一 mixed 系統的路徑互不相交，故在切開側的環序上不能交錯。
不要求 E1 與 E2 互相不交；兩者可共用第三色邊。也不將此必要條件宣稱為嵌入的充分條件。

新 [shared-cut checker](../scripts/four_color_shared_cut_obstruction.py) 對同一組具名
ports 枚舉全部 `2^m` 份側別，保存每個被拒指派的具體異側或交錯 witness：

| 控制圖 | 完整染色 | 邊界路徑 actions | 僅共同側別已拒 | 尚需側內 noncrossing 才拒 | 通過完整條件 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 五角星、指定原環序，支援 932 | 30 | 150 | 60 | 90 | 0 |
| 普通五環、真 disk 環序，支援 91 | 30 | 150 | 0 | 0 | 150 |

正控制每條路徑恰有一份可行共同側別。這次兩圖均只列舉同圖的完整染色與真實 actions，
沒有擴大 graph catalogue。

### 兩個 ports 的共同側別衝突

取五角星的完整邊色：spokes 為 `11213`，五條內邊依 `i–(i+2)` 的次序為 `33122`。
交換 12 路徑 `e0–0–3–e3`，切口 ports 為 `t0=0,t1=3`。
外部配對分別含：

```text
E13: t0–e4, t1–e1
E23: t0–e2, t1–e4
```

boundary arc `(e1,e2)` 與另一側 `(e4)` 分居兩側，因此 `t0` 同時被迫在 e4 側與 e2 側，矛盾。
只有兩個切口 ports，無需靠側內交錯便可拒絕。
刪掉任一 E 都恢復可行；各 E 獨立挑側別也各自可行，兩者的可行指派交集卻為空。
這正是同一切口、同一第三色原邊不能被拆成兩個邊際 witness 的地方。

**新增排除的範圍：** 第 1 節的具名完整 automaton 通過 B5 與抽象全歷史交換，
卻無法通過本節共同切口條件。這是比該鬆弛更強的來源檢查，尚不是 boundary support 層的
932 排除：其他內部接線未被覆蓋，不能由「這個 t 模型失敗」推出「所有 t 來源失敗」。

## 3. 連全部具名分量分割也不能自我更新

另一個自然補法是把三份 boundary pairings 換成三份**所有具名 dual 頂點**的分量分割。
新 [same-disk checker](../scripts/four_color_surgery_continuation.py) 在既有
`edge_states.json` 的三份完整 survivor tables 中核 491 染色，得到 465 個此種狀態、
26 個碰撞桶；選出同一 `survivor-891` disk 的 table IDs 4、5 作完整反例。
圖有 23 個 primal 頂點、61 條原邊、39 個內三角面及 5 個有標號 dual terminals。
原圖的 oriented sphere faces、色框及原邊身份均保留並重驗。

令 `S(c)` 包含字面 boundary 與三份 spanning pairGraphs 的全部具名頂點分量，
連不活躍 terminal 的孤立點也保存。兩份來源同為 `01023`，具有相同 S、三份 pairing、
cycle counts `(0,0,2)`。共同第一步是交換同一條 12 路徑，端點 `e2,e3`，含同一組
22 條原邊，連有序路徑、原邊色、各舊分量的被切邊數及端點級 cut interfaces 都相同。

交換後 boundary 均為 `01013`，三份 pairing／cycle counts 仍相同，
**全部具名分量分割卻不同**。刪第一條路徑後的 13 retained 系統已揭露差異：
dual vertex 10 在第一份連 e0，第二份連 e1。端點級接口能正確預測這一步的共同 boundary，
卻沒有保存每個內點沿外部 strand 的歸屬。

再在兩份後繼共同執行「交換包含 dual vertex 10 的 13 分量」，
實際 path endpoints 分別為 `e0,e4` 與 `e1,e2`，最後字面 boundary 分別為 `03231`、`01213`。
所有動作均重新核對完整分量與原圖 properness，沒有沿用過時 component。

因此不存在只讀上述 S 與同一具名第一條 path、就能確定更新 S 的函數 U：
本例有 `S(c)=S(d)`，卻有 `S(swap_P c)≠S(swap_P d)`。
這否定的是此候選的確定式充分性；**保留完整同源 fibres 的關係式狀態**未被否定。
原有一步 port-interface 引理仍正確，本例兩份相同的一步 boundary 預測也確實都正確。
控制圖支援是 891，不能把它當成 932 全阻擋來源。

### 只用 boundary-rooted 規則也會分歧

不需要用內點 10 作觀察。從同兩份來源出發，每次都交換「當前包含 terminal e0 的
完整雙色路徑」，共同色對序列取 `13 → 23 → 12 → 13`：

| 步數 | A 的字面 boundary | B 的字面 boundary |
| --- | --- | --- |
| 0 | `01023` | `01023` |
| 1 | `03023` | `03023` |
| 2 | `02132` | `02132` |
| 3 | `01232` | `01232` |
| 4 | `03012` | `03232` |

第二步 cycle counts 已不同，第三步 13 pairing 分別為 `03/12` 與 `01/23`，
第四步連 boundary 色列也不同。八份實際切口均通過共同側別與側內 noncrossing，
每步也都核對精確手術預測及原圖重新積分的 properness。
因此不是動作必須查詢內點身份才造成差異；初始完整分量摘要對這種純 boundary 規則
的未來觀測也不足。

paired BFS 展開 53 對、發現 156 對狀態，完整核完較短前綴，得到最短 pairing
區分長度 3。此最短性只限三個色對、五個 boundary terminals 的完整路徑 selectors，
不涵蓋內部閉圈交換，也不宣稱第四步是任意觀測的最短區分。

## 4. 精確接續命題與停止範圍

本輪保留的切入點是共同切口，而不是再加獨立計數邊際或只記舊分量。
下一個尚缺的窄引理是：從假設的**同一 plane 932 來源**，推出至少一條具名實際
boundary path，其兩份外部配對必違反第 2 節的共同側別／側內 noncrossing 條件。
若能推出，便與 crosscut soundness 矛盾；本輪只對五角星假模型完成這項排除，沒有普遍性證明。

有效接續需要保留 S 的原邊順序、兩份外部接線及同一 port 的第三色原邊身份，
再由 932 的全染色限制推導禁止接線；不能獨立替兩份 E 選不同來源。
要繼續迭代，還需證當前資料能產生下一步 retained 接口；第 3 節表明全部舊分量分割
甚至加一次端點接口，仍沒有這種閉合性。
僅重新描述任意長交換必逃逸仍是原待證命題；新的引理應限定一份可檢驗的接線構形，
給出實際可被迫出現的理由，並明列未覆蓋分支。

本輪沒有新增可約構形、任意大小來源覆蓋、932 排除、B5 以外的普遍計數不等式，
也沒有達成[4CT 主線研究契約](4ct_guide.md#成敗標準與保留範圍)的共同解存在性里程碑。
原 [LOCK-NO-GAIN](ck_d_lock_comparison.md#證據層重播與停止範圍) 限定裁決不變。

## 5. 證據與重播

證據分層：第 1 節的非 disk 論證及第 2 節 crosscut soundness 是紙面推導；
固定圖染色、全 action closure、port orders、側別窮盡與真 disk 反例是 Python 精確有限證書。
沒有新增 Lean theorem；未把舊 Lean 手術定理當作本輪共同切口拓撲的形式化。
外部 B5 ray 完備性沿用 [B5 face](c5_b5_face.md) 的信任說明；本輪具名控制的成立不依賴該完備性。

- [完整 pentagram automaton](../audits/2026-10-29-counts-surgery-continuation/pentagram-automaton.json)
- [全部 port orders](../audits/2026-10-29-counts-surgery-continuation/port-orders.json)
- [共同切口正反證書](../audits/2026-10-29-counts-surgery-continuation/shared-cut.json)
- [同 disk 的完整分量反例](../audits/2026-10-29-counts-surgery-continuation/surgery-partitions.json)

大型 `shared-cut.json` 依[既有封存規則](../audits/README.md#新-checkout-的還原)
保存原始 bytes；新 checkout 先執行 `python3 tools/audit_archive.py restore --artifacts`，
同時還原既有 `edge_states.json` 依賴，再執行下列重播。

```bash
python3 scripts/four_color_counts_face.py --check audits/2026-10-29-counts-surgery-continuation/pentagram-automaton.json
python3 scripts/four_color_port_order_obstruction.py --check audits/2026-10-29-counts-surgery-continuation/port-orders.json
python3 scripts/four_color_shared_cut_obstruction.py --check audits/2026-10-29-counts-surgery-continuation/shared-cut.json
python3 scripts/four_color_surgery_continuation.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --check
```

本輪實際檢查與治理傳播範圍另記[研究紀錄](history/2026-10-29-counts-surgery-continuation.md)。
