# C₄：geometry 34／join60 兩份原 unary 的完整關係排除

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只新增關閉(CPP-134-1,34,60)、side IDs=(27,1)；九份自身支援配置、
27份完整relation組合、contacts次序／原bridges及逐份2↔3 lift雙射均核對。
未知w完整relation保持符號纖維；不以整側禁色聯集代替逐分量檢查。
連同C₂／C₃合用恰三keys，3500key ledger及原36／140／900表不刪，
其餘3497keys未關閉。以下各輪正文／artifacts保持，現行入口由weak-deletion導覽維護。

2026-10-04。接續 [C₃ §8](c5_mixed_p3_two_frame_ternary_unary.md#8-重播證據界線與停止點)，
固定 **CPP-134-1／geometry 34／side_join_id 60、side IDs=(27,1)**。
**兩份 z-unary 各自的完整原 relation 都與自身附件的色置換對稱矛盾，
故這份固定側接合沒有來源，尤其沒有共同 disk source。**
此排除適用任意分量大小及原 bridges；不需 Gallai、minor 或額外平面性定理。
整側禁色通過的對稱檢查不能替代逐份原分量的對稱檢查。

[Checker](../scripts/c5_mixed_p3_two_frame_two_unary.py)、
[證書](../artifacts/c5_mixed_p3_two_frame_two_unary/observations.json)及
[本輪歷史](history/2026-10-04-mixed-p3-two-frame-two-unary.md)
保存固定身份、全部必要支援配置、完整有序 relation 候選、空 fibres 與驗證範圍。
任意大小結論為紙面 lift 雙射；Python 驗證固定關係與原邊控制，未新增 Lean theorem，0 target。

## 1. 同一原圖、兩份 ownership 與共同色框

沿用 C₃ 的來源前提：M 有限簡單，B=(b₀,…,b₄) 為 induced C5 disk 外框，
q=01012、U={0,1,2,3}，H=M−B 非空連通。M 拒絕 q，刪任一非框邊後接受 q。
相鄰 roots z,w 的完整 degree 均為五，其餘內點完整 degree 為四。
唯一 mixed 原分量仍為 C*=x₀x₁x₂，兩 root 皆接同一原 x₂。

\[
S_0=\{b_0,b_1,b_4\},\quad S_1=\{b_1,b_4\},\quad S_2=\{b_4\},
\qquad \mathcal T_*(q)=\{(3,0,1),(3,0,3)\}.
\tag{1}
\]

原 mixed 禁對仍為 {(1,3),(3,1)}。case ID=86、local ID=134、branch=1，
E_z={1}、E_w={1,3}，兩 root 無 spoke。整側實際支援仍為
A_z={b₁,b₂}、A_w={b₂,b₄}，兩側位於原 J=b₁b₂b₃b₄；原框色為 1–0–1–2。

z 側現有兩份**不同原分量**：

| 原分量 | 有序原 contacts | 自身實際支援 | 指定禁色 |
| --- | --- | --- | --- |
| D₂ | P₂=(u₀,u₁)，互異 | A₂=N_B(D₂)⊆{b₁,b₂} | f₂={0,3} |
| D₁ | P₁=(r₀) | A₁=N_B(D₁)⊆{b₁,b₂} | f₁={2} |

A₂、A₁ 是原圖所決定的集合，目前未指定；只知

\[
A_2\cup A_1=\{b_1,b_2\}.
\tag{2}
\]

D₂、D₁ 是 H−{z,w} 的不同原 components，彼此沒有邊，也沒有通往
w 或 C* 的邊。每份的外部邊只有其原 z-contact 邊及自身框附件。
兩份的所有原內邊、blocks、bridges 及各 bridge 的端點身份均保持。
原 z 的五條 incidences 分別為 zw、zx₂、zu₀、zu₁、zr₀。

w 側仍是原三接點分量 D_w，P_w=(v₀,v₁,v₂)、自身支援 {b₂,b₄}，
完整未知原 relation \(\mathcal T_w(q)\subseteq U^3\) 滿足 f_w={0,2}。
其 tuples／內點 lifts／root-avoidance fibres 保留為同一來源上的未知關係。
原 wx₂、zw、全部 P₃ 附件及原外路 z–x₂–b₄–b₃–b₂–b₁ 全部保留。

## 2. 逐份完整 relation 與全部必要支援配置

對 i=2,1，令 \(\mathcal L_i(q)\) 是原 Dᵢ 全部頂點的完整 proper colorings，
滿足每條原內邊及每份自身 q-框附件。原 z-contact 邊在下一步用來查詢 root 色，
不把 z 的固定色先塞進 relation。定義

\[
\mathcal T_i(q)=\{\phi|_{P_i}:\phi\in\mathcal L_i(q)\},\qquad
f_i(q)=\bigcap_{t\in\mathcal T_i(q)}\{\text{全部 }t\text{ 座標色}\},
\tag{3}
\]
\[
\mathcal T_i[h]=\{t\in\mathcal T_i(q):h\text{ 不出現在 }t\}.
\tag{4}
\]

這是完整有序 relation，並非接點 marginals。非空由原 M−zw 的 q-延拓
限制到每份 Dᵢ 取得；沒有假設原 M 可染。
禁色恰等於接點數，故每個 tuple 必含全部指定禁色，且沒有額外座標：

\[
\varnothing\ne\mathcal T_2(q)\subseteq\{(0,3),(3,0)\},
\qquad \mathcal T_1(q)=\{(2)\}.
\tag{5}
\]

因此 D₂ 的完整 relation 只有三份候選：單獨 {(0,3)}、單獨 {(3,0)}、
或兩者皆有。證書逐份保存完整 tuples 及四個 root pins 的 fibres。
D₂ 的 h=0、3 fibres 為空，h=1、2 fibres 非空；D₁ 的 h=2 fibre 為空，
h=0、1、3 fibres 非空。這些是原局部 relation 的必要資料，不是整圖 root 延拓。

(2) 的全部九份 ordered 必要配置如下；12 表示 {b₁,b₂}，空集合也保留。
表列必要候選沒有替原分量挑選附件，更沒有聲稱任一配置實現。

| A₂ | A₁ |
| --- | --- |
| ∅ | 12 |
| {b₁} | {b₂} |
| {b₁} | 12 |
| {b₂} | {b₁} |
| {b₂} | 12 |
| 12 | ∅ |
| 12 | {b₁} |
| 12 | {b₂} |
| 12 | 12 |

## 3. 原完整 lifts 保留 bridges 的逐分量雙射

取同一色框中的置換 σ=(2 3)，固定色 0、1。對任何上表配置及任何原 Dᵢ，
其自身框附件端只有 b₁、b₂，框色分別為 1、0。因此

\[
\Phi_i:\mathcal L_i(q)\longrightarrow\mathcal L_i(q),\qquad
\Phi_i(\phi)(v)=\sigma(\phi(v))\quad(v\in V(D_i))
\tag{6}
\]

是 involution：

1. 每條原內邊 ab 的不等式 φ(a)≠φ(b) 在 σ 後仍成立。
   **原 bridge 也是這同一條原邊**，兩端在同一完整 φ 中同時交換；
   不斷開 bridge、不各自正規化兩個 blocks、不拼接端點 marginals。
2. 每條原框附件 vbᵢ 的外端色 q(bᵢ) 被 σ 固定，故仍 proper。
3. 原頂點及有序 contacts 沒有換位；σ²=id 給逆映射。

從完整 lifts 投影到原 contact 次序，得到

\[
\sigma\mathcal T_i(q)=\mathcal T_i(q),\qquad
\sigma f_i(q)=f_i(q),\qquad
\sigma\mathcal T_i[h]=\mathcal T_i[\sigma(h)].
\tag{7}
\]

任一原 bridge e=ab 的完整同圖端點投影
\(\{(\phi(a),\phi(b)):\phi\in\mathcal L_i(q)\}\) 亦依 (6) 封閉。
這個推論處理所有實際 bridges；沒有假造未知原圖的 bridge 清單或 lifts。
Python 保存全部 16 份有序邊端色、8 份實際框附件色及 20 份完整 contact
座標域的置換檢查；任意頂點數的 lift 雙射由 (6) 的逐邊證明給出。

σ **只作用於一份 detached unary 的完整染色**。原 q 不改，特別是 b₄=2 不變，
原 P₃、另一份 unary 及 D_w 也不改。D_w 碰 b₄，不能把這個置換套到它。
(7) 的不同 root pins 是局部查詢；沒有把 z 換色後宣稱整份 M 延拓。

## 4. 兩份原分量各自矛盾，原外路與共同平面性保留

D₂ 的指定禁色滿足

\[
\sigma\{0,3\}=\{0,2\}\ne\{0,3\},
\tag{8}
\]

與 (7) 矛盾。更直接地，(5) 中任一原完整 tuple 都有原 lift；(6)
迫出 (0,2) 或 (2,0) 的同圖完整 lift，但這些 tuples 不含指定禁色 3，
不能屬於原 \(\mathcal T_2(q)\)。三份完整候選全部失敗。
等價地，(7) 要求 h=2、3 fibres 雙射，而 (5) 中前者非空、後者為空。

D₁ 的指定完整 relation 為 {(2)}；(6) 迫出同一原分量的 tuple (3)，
直接違反 f₁={2}。其 h=2 空 fibre 與 h=3 非空 fibre 也違反 (7)。
所以兩份分量**各自**已不可能，不需任選其中一份取得整側支援。

九份支援配置 × 三份 D₂ 完整 relation × 一份 D₁ 完整 relation 共 27 份
必要組合全部無 survivor。原外路 z–x₂–b₄–b₃–b₂–b₁、原框環序、
P₃ 全部附件及 w 的原關係均保留；它們不會為 detached Dᵢ 引入新的附件色。
既然固定身份連逐份原 relation 都不能成立，就更不可能把這些原分量與
原外路共同嵌入 disk。這是先於平面性的來源排除，不額外編造 K₅ witness。

## 5. 整側禁色與合併 ternary 為何遺失障礙

整側禁色聯集為 {0,2,3}，在 σ 下確實不變，所以前層對整側 A_z
的必要穩定子檢查可保留 geometry 34。它沒有核對兩份原 ownership。
保留有序 ownership (D₂.u₀,D₂.u₁,D₁.r₀) 時，(5) 的 product tuples
只可能為 (0,3,2)、(3,0,2) 或兩者皆有。σ 後必出現 (0,2,3)、(2,0,3)，
其第三座標已違反原 D₁ 完整 relation；不能以聯集禁色不變來接受它們。
證書保存三份 product relations 及其 σ 像，沒有補入新 tuples 當原 relation。

因此不能把兩份分量合成 C₃ 的單一 ternary，也不能把自身支援任意改配。
原分量的完整 relation／每條原 bridge 必須與同一 ownership 一起保持。

固定負控制進一步建立兩份**不同逐份禁色 ownership 的局部模型**，不是指定來源的替代：
二接點模型為原 edge a₀a₁，每點各接 z、b₁、b₂；單接點模型為兩個 triangles
d,a,b 與 c,e,f，由原 bridge dc 相連，唯一 z contact 為 d。d 只接 z，
c 只接 b₂，a,b,e,f 各接 b₁、b₂。兩模型每個內點完整 degree 均為四，
自身支援各為 {b₁,b₂}，兩條原 bridges 分別為 a₀a₁、dc。

同一 q 下，二接點完整 relation 恰為 {(2,3),(3,2)}，有兩份完整 lifts，
禁色 {2,3}；單接點原 c 強制取 1、d 強制取 0，完整 relation 恰為 {(0)}，
有四份完整 lifts，禁色 {0}。保留兩份 ownership 的完整 product 只有
(2,3,0)、(3,2,0)，共八份聯合 lifts。其整側禁色仍為 {0,2,3}，
但逐份禁色與 join60 指定的 {0,3}／{2} 不同，明標不能接回指定 identity。

控制的兩條原 bridges 另逐份保存四個 root pins 下、刪該 bridge 的完整有序
端點 relation 及完整同一刪邊模型 lifts，共八份 relations、34 份 lifts。
例如單接點模型 z=0、刪 dc 時，完整端點 relation 恰為 {(1,1)}，
四份 lifts 皆保留兩個 triangles 與實際附件；不能用端點 marginals 擬造不同色拼接。
這些刪邊控制只驗證固定模型的原 bridges，不用來替未知來源提供逐邊 minimality。

保留原 context 後控制的 z degree=5、P₃ 點 degree=4；刪 zw、取 z=w=1
有一份完整 context partial witness，P₃=(3,0,3)，D_w 內點保持符號 fibre。
原 zw 仍保存於 edge manifest，該 partial witness 明列省去 zw。
模型中純 N triangle 的相鄰 e,f 與原外路得到五袋
{e}、{f}、{b₁}、{b₂}、(其餘單接點模型頂點∪{z,x₂,b₀,b₄,b₃}) 的 K₅ minor；
證書逐對保存十條實際鄰接邊。因此它是非平面的整側資料負控制，
不是 disk realization，也不是整份 M 的 minimality 證書。

## 6. 重播、證據界線與停止點

```bash
python3 scripts/c5_mixed_p3_two_frame_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_two_frame_two_unary.py --check
python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
python3 scripts/c5_mixed_p3_common_endpoint.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際通過情況及未重跑範圍見[本輪歷史](history/2026-10-04-mixed-p3-two-frame-two-unary.md)。
新證書綁定原 checker／artifact SHA256，沒有重建或篩掉前層資料。
只登記 **(CPP-134-1,34,60)** 完成；原 `36／140／900`、全部其他 joins
及先前稽核快照保持原資料。已有 C₂、C₃ 的固定兩 keys 仍依其原證據成立，
本輪沒有將同一 z 角色的其他 joins 或整份 CPP-134-1 登記完成。

任意大小證明不依賴外部 Gallai／T4；Python 的 27 份必要組合核對不代表
27 份原圖實現。未新增 Lean theorem，既有 `lake build` 不形式化 (6)。
固定 q 來源排除沒有提升成完整 Σ、target 延拓、一般共同出口或 `K∞=K≤5`。
目前停止點及其他保留入口見
[weak-deletion 導覽](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)。
