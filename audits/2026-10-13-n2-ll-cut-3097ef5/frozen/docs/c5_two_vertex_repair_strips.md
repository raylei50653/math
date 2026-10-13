# 不含舊核心的同 class 來源：私有路徑奇偶定理

**2026-09-30 後續：**[完整四接點輪環替換](c5_two_vertex_repair_rings.md)
已給任意層數、無密封 clique 補片且私有圖含環的同 class 骨架，超出本報告
的整來源路徑族；新局部化約仍保十五組 repairs／r*=4。加入輪環化約後的
其餘骨架與必要分類仍未完成。下文保留本輪證明及控制。

2026-09-30。接續[密封 clique 補片](c5_two_vertex_repair_patches.md)，本輪
跨過「必須含原具名核心」的限制。指定下述完整接線的路徑族中，A 的
兩臂長皆偶數、B 的路徑長為奇數，**充要**於來源仍為 R127／R167。
加長任一段後，兩來源合成不再含保持框點及 ownership 的舊核心副本，
連非誘導子圖副本也沒有；所有私有點最低度數四，不能開始度數三消去。
兩方向仍恰有十五組極小 repairs，r*=4。

這是任意有限路徑長的紙面證明，加上十個17／21／29點圖的
[Python checker](../scripts/c5_two_vertex_repair_strips.py)／
[完整證書](../artifacts/c5_two_vertex_overlap/repair_strips.json)。
沒有外部染色定理、Lean theorem 或 `native_decide`，也未完成全部同 class
來源的必要分類。這些圖可以用本輪新證明的奇偶路徑化約回舊骨架；
**未**證明化約後仍為其他骨架的全部代表。現況見[導覽](c5_two_vertex_overlap_guide.md)。

## 1. 來源族及完整附件

沿用共同色框 D={0,1,2,3} 及

```text
U=(x,l,y,m,n,p,q,r)=(a0,a1,a2,a3,a4,b0,b2,b4)
(s,t)=(x,y) 正向；(s,t)=(y,x) 反向。
```

令 L,R≥2、K≥1，均為整數。兩來源只有 x、y 共享，所有私有點互異。
下列就是全部邊，不能遺漏或另加附件。

| 來源 | 原框及完整私有接線 |
| --- | --- |
| A(L,R) | 原框 x–l–y–m–n–x；私有路徑 z₀–⋯–z_{L+R}；x 接全部 z；y 接 z₀,…,z_L；m 接 z_L,…,z_{L+R}；另有 l–z₀、n–z_{L+R} |
| B(K) | 原框 p–s–q–t–r–p 及弦 q–r；私有路徑 w₀–⋯–w_K；p、q 各接全部 w；另有 r–w₀、s–w_K |

舊核心正是 L=R=2、K=1，其中 A 路徑為 h9,h5,h7,h6,h8，B 路徑為 v,w。
新合成圖有 `L+R+K+10` 點、`3(L+R+K)+20` 邊。
除 z_L 度數五外，所有私有點度數四。因此加長得到無上界的有限來源族，
任何保留 U、只刪私有度數至多三點的次序都沒有第一步。

## 2. 完整來源 relation 的任意長度公式

先用一個 elementary path fact：固定可用色集 Q，若 |Q|=2，長度 d 的
proper path 端點相同 iff d 偶數。若 |Q|≥3 且 d≥2，任意指定的兩端
顏色都能連成 proper path。後者的長度二情形選異於兩端的中間色；
由長度 d 到 d+1，先選異於末端的倒數第二色，再用歸納假設。這裡的
長度是邊數，所有色仍在共同的 D 中。

**A 路徑公式。** 原框 proper 時，y≠m，且完整延拓條件恰為

\[
x=y\quad\lor\quad x=m\quad\lor\quad
\left[(l=m\Longleftrightarrow L\text{ 偶})\land
      (n=y\Longleftrightarrow R\text{ 偶})\right]. \tag{A}
\]

最後一支在 x,y,m 互異時使用。此時 z_L 被迫取第四色 k。
左臂只用 D∖{x,y}={m,k}，故 z₀ 在 L 偶時為 k、奇時為 m。
框邊已令 l∈{m,k}，邊 l–z₀ 恰給左邊條件。右臂同理只用 {y,k}，
邊 n–z_{L+R} 恰給右邊條件。這也直接構造充分方向。

若 x=y，先處理右臂：Q=D∖{x,m} 有兩色。框邊給 n∈Q，選擇
z_L∈Q，使長度 R 的交替路徑末端異於 n。左臂可用三色 D∖{x}，
其起點可選任一異於 l 的色，再以 L≥2 的 path fact 接到 z_L。
全部邊都正常。x=m 時交換左右，以右臂的三色 path fact 完成。
因 y≠m，以上情形窮盡所有 proper 原框染色，證明 (A) 雙向。

**B 路徑公式。** 原框及弦 q–r proper 時，完整延拓條件恰為

\[
p=q\quad\lor\quad (r=s\Longleftrightarrow K\text{ 偶}). \tag{B}
\]

若 p≠q，全部 w 共用兩色 D∖{p,q}；框邊及弦使 r、s 也在這兩色中。
兩端各被迫取異於 r、s 的色，奇偶 path fact 即得 (B)。若 p=q，
全路徑有三色，兩端各仍有至少兩個選擇；K=1 時能選異色兩端，
K≥2 則由 path fact 延拓。再次得到必要及充分性。

因此在**本節完整接線族內**，R_A=R127 iff L、R 都偶；R_B=R167 iff K 奇。
必要性也不是從有限控制外推：取互異 x,y,m 及第四色 k，l 在 m,k 中
二選一、n 在 y,k 中二選一，四種奇偶要求能逐一區分；B 取 p≠q，
依 r=s 或 r≠s 區分兩種長度。按原目錄的 pattern order，有限重算為：

| L parity／R parity | A class | K parity | B class |
| --- | ---: | --- | ---: |
| 偶／偶 | R127 | 奇 | R167 |
| 偶／奇 | R191 | 偶 | R271 |
| 奇／偶 | R575 | — | — |
| 奇／奇 | R319 | — | — |

Class 編號及八個奇偶控制的完整關係存於證書；任意長度結論由 (A)、(B)
負責。checker 的 path recurrence 依具名接線構造全圖染色，不查 class
mask 或已知 J；另以原邊回溯獨立核對所有 `4^5` 來源及 `4^8` 共同賦色。

## 3. 舊核心確實不存在，且局部四接點不保真

固定原框點及來源 ownership，假設 A 舊核心嵌入 A(L,R) 為子圖。
l 的唯一私有鄰點迫使舊 h9 映到 z₀；n 的唯一私有鄰點迫使舊 h8
映到 z_{L+R}。舊核心的五個私有點形成長度四的簡單路徑，新來源的
整個私有誘導圖卻是單一路徑，故兩端距離迫 L+R=4。在 L,R≥2 下
只能 L=R=2。這已排除非誘導副本，亦排除只靠刪點留下舊核心的可能。

同理 B 的 r、s 各只有一個私有鄰點，舊 v,w 必映到 w₀,w_K；
舊邊 v–w 只能在 K=1 存在。只要任一來源加長，完整舊核心便不存在。
有限 checker 另外窮盡保持邊界及 ownership 的私有點單射，驗證此結論，
沒有只查原標號缺了一條邊。此處不排除 minors、邊收縮或其他化約。

**不能把 (A)、(B) 升格為任意固定四接點替換。** 取兩個 hub h₀,h₁，
皆接 u,v，並有邊 uv；將 uv 改為三邊路徑 u–a–b–v，a,b 也接兩 hub。
固定 `(h₀,h₁,u,v)=0011`，舊邊拒絕，新圖卻有完整染色 `001123`。
證書重算兩份完整四接點關係，確認新關係嚴格較大。
本輪保留的是整個來源的五框關係，容許其私有點重新染色；不能保持
任意新增的私有觀察點，亦不能把這個局部替換任意接入其他來源。

## 4. 完整可用外框及 repairs

從舊來源的兩份整圖 rotations 施工。A 左臂選 h9–h5，右臂選 h6–h8，
B 選 v–w；各邊的兩個 incident 三角面有不同 hub。將邊 uv 改為長度 d
的私有路徑，所有新點接兩 hub，原兩個三角面就被各 d 個三角面取代。
A 的 d 分別取 L−1、R−1，B 取 K。施工在兩面聯集的 disk 內，保存
其四條邊界邊及其餘面；這對所有上述長度成立，不只是控制圖。

因而兩個混合框

```text
C₁=(x,n,m,y,q)，C₂=(s,l,t,r,p)
```

都仍可作整圖外界；限制 rotation 到各來源亦保留原 C₅ 外面。
U 誘導邊沒有改變，全部候選五環仍恰為舊五條。把舊圖各被替換邊
沿新私有路徑走，得到固定 U 的舊圖 subdivision。三個不可用框的
兩條交錯、不相交原路徑亦各自變為 subdivision，仍不相交且內部避開
該框，故仍排除整圖外界。全部可用框因此**恰為** {C₁,C₂}。
此處不推論任何尚未指定的兩來源 disk 相對區域政策。

在 L、R 偶且 K 奇時，(A)、(B) 保持完整來源 relations，兩來源只共享
x,y，所以共同色框內的自然接合 J 也完全不變。完整可用框族相等再給
P 相等；不是僅從 J 相等推論 P。來源報告的十一份稀疏 U 補全可用
§2 的路徑構造延拓，全部改動 U 點集合不變，故三種 exact rejectors
與兩類覆蓋皆保留。套用[共同 lemma](c5_two_vertex_common_repair.md)，得到

```text
A={x,l,y,m}，T={s,t,p,q}，B={s,p,q,r}
𝓔={S⊆U : |S|=4, {q,r}⊆S}∖{B}
全部 inclusion-minimal repairs：{A,B} 及 {A,T,E}，E∈𝓔。
```

共十五組，A 是唯一 forced scope。W_A 仍通過全部至多三點投影但不在
J，四點修復已充分，故 r*=4。兩方向各有 J/P/Δ=60/114/54 個全域 S₄ 軌道，
r=0,…,4 的殘留為54,54,16,16,0。

每個新來源仍為原框內的三角剖分。因此還可在這些新骨架外使用
[完整 clique 補片引理](c5_two_vertex_repair_patches.md#1-完整附件的一份染色延拓引理)：
保留新 induced 骨架、完整密封附件、一份染色及整圖保框證書，即保留
同樣的 J/P/repairs。這是既有引理的推論，並未在本輪重枚舉此類補片。

## 5. 有限控制、重播及停止點

兩方向各核對下列五組參數：

| (L,R,K) | 全圖點／邊 | 不含哪側舊核心 |
| --- | --- | --- |
| (4,2,1) | 17／41 | A |
| (2,4,1) | 17／41 | A |
| (2,2,3) | 17／41 | B |
| (4,4,3) | 21／53 | A、B |
| (6,8,5) | 29／77 | A、B |

十圖共14,400份構造完整延拓、110份稀疏補全，逐一核對原邊、完整來源
及 J/P、全部70個四點 scopes、十五組 repairs、arity 下界及全部五個框的
肯定／否定證書。結構 verifier 自行從實際邊抽取整條私有路徑及全部附件，
不讀 class、repair 或 witness 答案。另有八個奇偶控制、十二項結構負控制
及 §3 的固定端點反例。artifact 小於1 MB，完整存檔；`--check` 逐 byte
比較而不改寫。實際執行見[本輪紀錄](history/2026-09-30-c5-two-vertex-repair-strips.md)。

```bash
python3 scripts/c5_two_vertex_repair_strips.py
python3 scripts/c5_two_vertex_repair_strips.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_strips.py --check
python3 scripts/c5_two_vertex_repair_patches.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

**本輪停止點。** 指定完整接線的路徑族已作任意長度的必要且充分奇偶
分類；加長圖不含舊核心，仍維持全部 repairs，故「含舊核心＋密封補片」
也不是必要條件。下一窄題是**去掉密封 clique 補片，並以已證的整來源
奇偶路徑化約後，仍留下其他骨架的同 class disk 代表**。未證全部代表
都能作這些化約；來源必要分類、一般接合政策、多步摘要、一般出口與
`K∞=K≤5` 仍未完成。沒有新增 Lean 形式化。
