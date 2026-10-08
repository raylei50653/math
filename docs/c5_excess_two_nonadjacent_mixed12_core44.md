# ε=2 非相鄰唯一 mixed12／21：U3 的兩-root (4,4) 身份排除

**後續（2026-10-08，U4完成）。** [非相鄰兩mixed的U4](c5_excess_two_nonadjacent_two_mixed_core44.md)
現亦全排，固定完整Σ933／941下兩-root44身份全部完成。
下文保留U3當輪停止點；單-root例外、45／54／55及ε≥3仍保留。

2026-10-08。接續 [U3 mixed11](c5_excess_two_nonadjacent_one_mixed_core44.md)、
[E4 的 N1-22-44](../artifacts/c5_excess_two_e4/REPORT.md#3-n1-主攻22-mixed-加-44-core-整類排除)
與 [C44″](../artifacts/c5_excess_two_c44pp/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

**結論。** 在下列完整來源前提下，sole mixed 的原 incidence12／21
不可能有保留兩個原 roots、兩者自身 degree 均四的 minimal 拒絕列 core。
連同既有 mixed11 及 mixed22 排除，U3 的兩-root44身份完成。
這不排除 N1 完全沒有44 core 的來源；單-root例外、45／54／55 core、U4
及 ε≥3 均保留。

容量一分支由任意大小紙面 star-face／slack 證明承擔；容量二分支由
既有全 degree-4 分類固定為六內點，再用完整同框有限接回排除。
沿用外部 degree-list／Gallai 及上游 topology 分類的信任範圍，未新增 Lean theorem。

## 1. 完整前提與原省略身份

G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框。
完整 Σ(G) 是933／941或整圖D₅像，每條非框邊都Σ-critical。
ε=2；原 roots z,w 不相鄰、完整 degree 五，其餘有效內點完整 degree 四；
H=G−B 連通、碰齊五框點，T4全收。C 是 H−{z,w} 的唯一原 mixed，
原 incidence 為 z側一、w側二。w的兩個contacts互異，z-contact可與其中一個共用。
root交換同時搬運全部原圖與色框，涵蓋21。

取拒絕列q的minimal core M，假設z,w都保留且degree_M均四。
[原飽和／省略分類](../artifacts/c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類)
給：整份C、全部原內邊、contacts與框附件保留；每側只省略一條原spoke，
或整份capacity-one原unary。C separating，不能給它one-sided盾弧，也不能
虛構避開C的內部z–w外路。

M繼承disk與T4；沿用[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)，
其內部只有path、單triangle加不分叉路徑枝、或兩個互斥triangles加一條直接bridge。
所有內部degree至多三。w及兩個原C-contacts形成原triangle。

### 1.1 兩份原unary不能都接z

T4迫原spoke數t_r≤3；z的mixed incidence一迫至少一份z-unary。
[盾弧定理A](c5_unary_shield_budget.md#3-定理-a全圖至多兩份-unary-分量)
給全圖unary≤2。若兩份都接z，w沒有unary，故t_w=3。
同一原H−w=C∪{z}∪全部z-unary連通，必落在B加原w三-spoke star的一個內面。
但兩份原unary盾弧為(2,2)或(2,3)，支援等於各盾弧的全部頂點，
兩份支援的聯集是整個B。一個三-spoke star面至多見四個框點，矛盾。
這也排除「保留一份unary，另省略一份unit-unary」的同root身份。

因此恰一份原U_z；原U_w至多一份。令k_r為各側原unary容量，沒有U_w時k_w=0。
原degree給k_z=4−t_z、k_w=3−t_w。
省略spoke時，M的內部degree為1+k_z、2+k_w；省略unary時其容量必一。
故只剩

\[
k_z\in\{1,2\},\qquad k_w\in\{0,1\}.
\]

以下各步保存同一原U_z、U_w、C及完整附件，不以小圖取代未知原relation。

## 2. k_z=1：原star的兩面迫同一非相鄰pair

此時t_z=3。M中的z只有一條C邊及至多一條U_z邊，兩鄰點分屬不同原piece，
不能形成通過z的triangle。
雙triangle分類的六個內點全部在triangles上，所以M只能有w的那個triangle。
整份C保留；刪除w破壞這個唯一cycle，故原C是tree，且|C|≥2。

### 2.1 原U_w存在

兩份unary的盾弧若為(2,3)，只留兩個可用框點，不足z的三條不同spokes。
故均長二。一次共同搬運原圖後寫成

\[
\sigma_{U_z}=012,\quad\sigma_{U_w}=234,\quad N_B(z)=\{0,2,4\}.
\]

W=C∪{w}∪U_w原連通，避開z及z-star，含U_w全部實際支援234；
所以它在z-star的234面。兩份原盾弧的內點1、3不被C或roots碰到，
因而S_C⊆{2,4}、N_B(w)={2,4}。取得實際非相鄰pair {p,q}={2,4}，
兩roots的原spokes都含p,q。沒有聲稱原H−z連通；使用的是同一原W。

### 2.2 原U_w不存在

此時t_w=3。原A=C∪{z}∪U_z連通，落在原w-star的同一個面F。
F至多見四框點，必包含U_z的至少三點支援及全部三條z-spokes。
U_z盾弧的內點禁止z接觸；若F僅三點，或U_z支援有四點，
F中至多剩兩點可作z-spokes。因此F恰見四個連續框點，U_z盾弧恰長二。

按實際環序記F的框弧為v₀v₁v₂v₃，剩餘框點為v₄。
w-spokes是{v₀,v₃,v₄}；U_z盾弧只可能v₀v₁v₂或v₁v₂v₃，
z-spokes恰為F的四點去掉該盾弧內點。
同一原W=C∪{w}連通，落在z-star的v₃v₄v₀面，因為它含w的全部三spokes。
C同時在F及這個z-star面，其實際框附件只能在

\[
S_C\subseteq\{v₀,v₃\}=\{p,q\}.
\]

p,q在五框上非相鄰，且同時是兩roots的spoke端點。
此處只是兩個原star面的附件限制，未收縮任何原路徑或修改原contacts。

## 3. 重色列接回整份原圖

由S_C⊆{p,q}及原degree四，每個C點的degree_H至少二。
C是tree、恰有三條原root incidence，故

\[
\sum_{v\in C}\deg_H(v)=2(|C|−1)+3=2|C|+1.
\]

|C|≥2迫某個v有degree_H(v)=2，其兩個不同actual框附件恰為p,q。
不必先分類C的長度或把它改成K₂。

完整來源共同搬到canonical933／941時，指定拒絕列01212、01202、01021
的重色pairs為{13,24}、{03,24}、{02,14}，覆蓋全部五個非相鄰框pair。
故有一個仍被G拒絕的字面β，使β(p)=β(q)。全部原附件與拒絕列一起搬運。

沿用[list-slack貪婪引理](c5_excess_two_nonadjacent_one_mixed_core44.md#4-重色列的完整原圖延拓)：
連通圖每點list大小至少內部degree，且某點有嚴格slack，便可由生成樹逆序著色。
固定同一β，先分別染完整原側{z}∪U_z與{w}∪U_w（沒有U_w時只有w）。
非root點均有degree lists；兩roots的spokes含重色p,q，所以

|L_z(z)|≥2>1，且沒有U_w時|L_w(w)|≥2>0，有U_w時|L_w(w)|≥3>1。

因此兩份整側都有完整染色。固定所得實際pins a=f(z)、b=g(w)，
再對原C全部頂點給lists：原degree四保證|L_C(u)|≥degree_C(u)，
上面找到的v因兩個actual框鄰點重色而有嚴格slack。
生成樹貪婪法給整份原C的lift；與兩份整側染色拼回同一G，延拓拒絕β，矛盾。
允許a=b；原圖沒有zw，不可加上root不等式。

這關閉k_z=1全部spoke／unit-unary省略身份及任意大小原unary。
沒有相乘contacts的marginals，也沒有拿縮圖著色冒充原圖著色。

## 4. k_z=2：六內點雙triangle的完整接回

U_z不可能被省略，z只能省略spoke。U_z兩contacts與z給第二個原triangle。
[雙triangle分類](c5_two_triangle_blocks.md#1-範圍與結果)迫M恰六內點、
直接bridge、沒有外掛樹。bridge必為原z–x；另一triangle是wxy，
w是非bridge點，整份原C恰為edge xy，整份U_z亦恰為edge。
w沒有保留unary；原w側只有省略spoke（t_w=3），或省略整份unit U_w（t_w=2）。

[Double checker](../scripts/c5_excess_two_nonadjacent_mixed12_double_core44.py)
從既有雙triangle artifact的64份q=01012 disk minimal cores重建完整同框染色。
每份核心有4份mixed12標記：z選任一bridge端點，w選對側兩個非bridge點之一，
合計256份。原來源、拒絕q、完整Σ與所有附件只共同搬運一次。

| 原省略身份 | 完整必要查詢 | 結果 |
| --- | ---: | --- |
| z-spoke／w-spoke | 256×4×3=3,072份接回；30,720十列查詢 | 完整Σ與全部10份目標D₅ masks無交集 |
| z-spoke／unit U_w | 1,024份G−U_w kernel×10目標=10,240 | 5,248份在目標接受列已有空kernel；4,992份在拒絕列須禁止至少兩種w色 |

雙spoke的完整Σ分布為1022×1,920、830×384、1016×384、958×192、1020×192。

unit U_w的判據使用**同一完整kernel**可取得的w色，先由全圖染色算完整root fibres，
才投影。原U_w唯一contact在刪接點邊後有slack，整份原U_w的contact relation非空；
它每列最多禁止一個w色。因此kernel空時不能新增接受列，kernel有兩種w色時
不能把該列全部拒絕。所有10,240份查詢已由這兩項排除。
跨列相同支援／S₄一致性與新的topology反證均**未觸發**；忽略這些條件只放寬必要域。
沒有將未知原U_w替換為singleton圖。

## 5. 補充有限控制、重播與信任範圍

[Single checker](../scripts/c5_excess_two_nonadjacent_mixed12_single_core44.py)
另保存單triangle的336份root-marker正常形與3,584份接回計畫。
這是既有18單run／8雙run域上的補充有限控制；§§2–3的任意大小排除
使用原star與slack，不依賴這份marker控制或新的縮圖relation聲稱。
實際數字、subdivisions與獨立重播範圍見[研究紀錄](history/2026-10-08-u3-mixed12-core44.md)。

[Double證書](../artifacts/c5_excess_two_nonadjacent_mixed12_double_core44/observations.json)
保存完整原core邊、apex rotations、附件、原Uz/C ownership、ordered contacts、
全部字面root fibres（含空者）、全圖witnesses及原spoke過濾。
[獨立auditor](../scripts/c5_excess_two_nonadjacent_mixed12_double_core44_audit.py)
不import primary，另重建列／D₅、原圖染色與全部接回判據。
固定控制不聲稱有完整Σ933／941來源，也不負責上游分類的任意大小證明。
兩份大JSON依MANIFEST重建；double生成只需標準函式庫，single首次生成
subdivisions需NetworkX 3.5，既有證書的`--check`不呼叫planarity search。

```sh
python3 scripts/c5_excess_two_nonadjacent_mixed12_double_core44.py
uv run --with networkx==3.5 python scripts/c5_excess_two_nonadjacent_mixed12_single_core44.py
```

```sh
python3 scripts/c5_excess_two_nonadjacent_mixed12_double_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_mixed12_double_core44.py --check
python3 scripts/c5_excess_two_nonadjacent_mixed12_double_core44_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_mixed12_double_core44_audit.py --check
python3 scripts/c5_excess_two_nonadjacent_mixed12_single_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_mixed12_single_core44.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

上游全部degree-4／triangle／topology枚舉、ES／ER搜尋與LC額外targets／axioms
沒有重新稽核；lake build只驗既有Lean專案。有限接回加上明列紙面分類
關閉指定來源身份，並非一般來源實現判定、ε≥3或猜想E的任意大小證明。

**精確停止點：U3的兩-root44身份完成。** mixed11由前輪、mixed22由E4、
mixed12／21由本頁涵蓋；其餘incidence由原44分類排除。
完整Σ下的44殘留只剩U4。N1單-root例外及完全無44 core的45／54／55來源、
E5新證明要求、一般出口與K∞=K≤5仍保留。
