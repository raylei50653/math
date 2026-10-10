# N45-H3G：原 X 的 no-spoke 幾何與外部信任稽核

日期：2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
**裁決：`holds under stated hypotheses`，只作候選，尚未由監督採納。**
對全部 K1–K13 的任意大小來源，指定 HIGH3 身份不存在；矛盾在原
X=G−e 的 K5 minor，不藉省略邊 e，也不將 X 的 coloring 提升為 G 的 coloring。
沒有新增充分前提或數學 gap；這份裁決不涵蓋 HIGH2、long、原55、其他省略／core、
一般 N2／E、ε≥3 或核心存在性。

## 1. 權限、凍結與精確來源

指定目錄以 exclusive create 建立；未修改 shared、舊 audit、parent、sibling 或 HIGH2。
未再委派、commit、push、PR 或送外部訊息。HIGH2 在製內容未讀。
[全部契約](frozen/dispatch/common-contract.md)、[task](frozen/dispatch/n45-h3g-task.md)與
[14 項 pins](frozen/dispatch/inputs.json)均凍結；[實際 pin 核對](pin-verification.json)
證明 8 current／6 BASE 的 live/blob、parent frozen 及本目錄副本 SHA256 全吻合。
HANDOFF／STATUS 與 Git status 只作 routing/context 閱讀，不提升為新數學 authority。

數學依據是本目錄凍結的 BASE
[no-spoke §§1–3、5](frozen/base/docs/c5_no_spoke_exterior.md)、
[degree5 interface §§1–4](frozen/base/docs/c5_degree5_interfaces.md)、
[三接點 §§1–4](frozen/base/docs/c5_single_spoke_three_one.md)、
[tree component §1](frozen/base/docs/c5_degree5_tree_components.md)，
以及 current [N45 §1](frozen/current/docs/c5_excess_two_nonadjacent_unit_core45.md)。
下文將 no-spoke 文件中稱為 G／z／C 的物件映到本次 X／s／U；
本次 C={r}∪P∪Q 是它的另一原分量，不混淆兩種 C 記號。

## 2. CORE 與 COMPONENT：前提在 X 自己成立

量詞為每一滿足 K1–K13 的有限簡單 disk G、其指定 e=rb_i、拒絕 literal β、
原 roots／contacts／attachments／rotation 及全部 lifts。K10 直接給 X 自己
是 β inclusion-minimal obstruction；不能從 G 的 Σ-criticality 遺傳這件事。
只有 e 被刪，故 d_X(r)=4、d_X(s)=5，其餘有效原內點完整 degree4。
孤立原內點仍存在，其四色 free factors 保留，不屬於有效 H_X。
刪除 spoke 不改內部邊，因此 H_X 仍連通、外框仍 induced C5、原 disk 嵌入限制到 X。

β 是 G 的拒絕列；current N45 §1 明列 933／941 缺失皆為 singleton 三色列，
包括 933 的 q2。一次共同 D5 將 singleton 位置搬到 4，再一次共同 S4 將
三個使用色與未使用色搬到 q=01012 的共用四色情境。作用於整圖、全部列、
pins、contacts、relations、fibres 與 full lifts；不各自正規化 U／P／Q，
亦不刪去搬運後的 q2 資料。三色 proper C5 每色最多出現兩次，故 multiplicities
為 (2,2,1)，上述共同搬運成立。以下可直接留在 β 的 literal 色框證明；
搬運只用來核 BASE 的 q 前提，β 不必是 U 盾中點。

P、Q 連通且各有 r incidence；r∪P∪Q 因而連通。K5／K7 排除 U 與 r、P、Q
之間的所有內邊。故 H_X−s 恰為 C={r}∪P∪Q 與 U，兩份均完整保留。
s 在 P、Q 各一原 contact，在 U 恰三個相異原 contacts sx1,sx2,sx3；
其 actual component incidence 為 (2,3)，且 N_B^X(s)=∅。

## 3. 同列完整接合與 U 至少兩禁色

固定 β，色集 A4={0,1,2,3}。對 D=C,U，以全部實際 B 附件定義
L_D(v)=A4\β(N_B^X(v))，R_D 為同一 D 的全部合法 list-coloring 在具名有序
s-contacts 的完整 tuple 集，F_D=⋂_{t∈R_D}set(t)。這個投影只用於共同 s 色，
不取代十列完整 R／fibres／full lifts；沒有改任何 coloring 或 contact identity。

每個 D 點完整 degree4，未指定 s 色時 |L_D(v)|≥deg_D(v)，在每個 contact
至少多一色。連通 strict-slack 貪婪論證給 R_D 非空。因此 |F_C|≤2、|F_U|≤3。
固定同一 s 色 a 後，兩分量的完整 assignments 恰可拼合；全部 s 色的精確集合
是 A4\(F_C∪F_U)。X 拒絕 β 且 s 無 spoke，故 F_C∪F_U=A4，從而
**|F_U|≥2**。兩份 F 均非空真子集；X 自己的 minimality 亦給各份 private color。
在此兩分量／容量前提，至少兩色已由拒絕與完整接合推出。

對任一 d∈F_U，M_d(v)=L_U(v)\{d} 在 contacts，其他點為 L_U(v)。
|M_d(v)|≥deg_U(v)，但 U 不可 M_d-color；strict-slack 因而迫每點等號。
外部鄰居的 literal 顏色全相異；特別是各 contact 的 boundary 顏色避開 d。

## 4. 避 U 的 s–B 原路與 K4 hub

選 P 的唯一 s-contact y 及任一原 r-contact a；P 連通，取 P 內簡單 y–a 原路。
可有 y=a，這保留 shared contact 的一個原頂點，並非合併 identity。
**Q_ext = s–y–(P 內路)–a–r–b_j** 為 X 原簡單路，r b_j 是 K9 保留的 spoke。
其內部在 C，與 U 完全不交，並且到 b_j 前不碰 B。
這直接核 BASE no-spoke §2；不用被省略的 r b_i，也不新增 s spoke。
若不用這条特定 spoke，BASE §2 的另一原分量 actual B attachment 亦足夠。

固定 d∈F_U。Gallai palettes 的精確外部信任見 §7。若 U 有 K4 block J，
J 的每點已有三個 clique 鄰居，完整 degree4 恰留一條外接邊：直達 B／s，
或是 U 中的 bridge 進入分支 W。不同 J 點的 W 不交且不返回另一 J 點。
刪一 bridge 後兩側 endpoints 均有 slack，可各自著色；原 U 被拒絕迫兩側
endpoint 色集為同一 singleton。若 W 不碰 B∪{s}，其 lists 全為 A4，
全域 S4 換色使 endpoint 可取全部四色，矛盾。因此四點各有一條原 tether
到 B∪{s}，內部在 U、互不相交並避開 J。

B∪{s}∪V(Q_ext) 加上四 tethers 去掉 J 起點後的部分構成同一連通 hub O_J。
五 bags 是 J 的四 singleton 與 O_J；十邻接為六原 clique 邊及四原 tether 首邊，
全部屬 E(X)，給 K5 minor。與 disk 平面性矛盾，所以 U K4-free。
這正核 BASE no-spoke §3／tree component §1 的外部 hub，沒有假設 s 有 spoke。

## 5. 兩拒絕 lists 迫唯一 active triangle、三 arms 與三 tethers

選任意相異 a,b∈F_U。兩份 tight lists 滿足
1_(M_a(v))−1_(M_b(v))=1_{v∈{x1,x2,x3}}(e_b−e_a)。
同一原 U 的 vertex–block incidence matrix 各欄線性獨立：依 leaf block
private vertex 消欄，再歸納。外部 palettes 對 a,b 之外的 membership 相同，
在 a,b 只可能不變或交換；active block 的 sign 為 ±1。
同一點的 incident palettes 互斥，故正、負 active block 至多各一。
contacts 恰接一個正 block；非 contacts 恰接零個或正負各一個。

全部 active blocks 的完整 incidence forest 只有三个葉，恰為 x1,x2,x3。
每個非空 tree 至少兩葉，故 forest 恰一棵；葉公式 3=2+Σ(deg−2) 迫
恰一個 degree3 block-node，其餘 block-node degree2。Gallai、U K4-free
與平面性因而給一個原 triangle v1v2v3，及三條原 bridge arms A_i
由 v_i 到 x_i。各 arm 包括端點，允許零長 v_i=x_i；三 arms 在 triangle 外
互不相交且無其他 active 分支。沿 arm sign 每一步反轉，三臂長同 parity。
這是有限樹的任意大小論證，不是以有界臂長控制外推。

每個 v_i 有兩 triangle 邊，加一 arm 首邊（非零長）或已用的 s-contact（零長），
完整 degree4 恰留一條邊。它直達 B，或經 inactive bridge 進入旁支 W_i。
另一 cycle block 需兩條額外邊，故不可能；所有 contacts 已在 arms 上，
所以 W_i 不含 s-contact，也不能通往 C、返回其他 active 點或與另 W_j 相交。
若 W_i 無 B 附件，U−W_i 在 v_i 有 strict slack，而 W_i 用全 A4 lists
在 bridge 根有 slack；分別貪婪著色，再對 W_i 整體 S4 換色即可拼回 M_a，矛盾。
所以每個 v_i 有一條真實 boundary tether T_i；其內部在 W_i，三條內部互不相交，
避開所有 arms、s 與 C。終點可是同一 B 點。這完整核 BASE 三接點 §3／no-spoke §5。

## 6. 五個連通互斥原 K5 bags 與十對鄰接

Z={s}，V_i=V(A_i)（含 v_i,x_i），
O=B∪⋃_i(V(T_i)\{v_i})∪(V(Q_ext)\{s})。
V_i 非空連通，即使零臂仍有單點；各 V_i 互斥。
O 的 B 為連通原 C5，各 tether 與 Q_ext 的非 s 部分都接到 B；O 非空連通。
其 U 內點在 inactive 旁支，其 Q_ext 內點在 C，因此 O 與 Z、各 V_i 均互斥。

| bag pair | 保留的 X 原邊 |
| --- | --- |
| V1–V2 | v1v2 |
| V1–V3 | v1v3 |
| V2–V3 | v2v3 |
| Z–V1 | sx1 |
| Z–V2 | sx2 |
| Z–V3 | sx3 |
| V1–O | T1 首邊 |
| V2–O | T2 首邊 |
| V3–O | T3 首邊 |
| Z–O | Q_ext 首邊 sy，y∈P⊂C |

完整十對原鄰接證 K5 minor。K9 的 e=rb_i 不在任何 bags 的所需邊中；
retained rb_j 只用於 O 的連通性。minor 中可合併 B，但只反證平面性，
不改寫 boundary-state／Σ 或完整 coloring relation。任意長 arms／旁支與零長臂均涵蓋。
結論是 BASE no-spoke §§2–3、5 對 HIGH3 的直接適用：指定 (3,2) 身份不存在。

## 7. 外部信任與證據分層

Primary source: [Dvořák, List coloring and Gallai trees (2018)](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf).
The frozen [PDF](frozen/external/gallai.pdf) and [trust record](external-trust.json) bind its bytes.
Lemma 7, PDF page 5, applies to connected degree-list graphs and supplies tightness from noncolorability.
Theorem 10, PDF page 6, supplies Gallai blocks and blockwise uniform palettes, including their
disjointness at shared vertices and union to each list. Both hypotheses were checked above.
We trust these external results; no local Python or Lean proof of them is claimed.
The strict-slack argument is also reproduced directly in §§3–5. No T4, second rejection,
Four Color Theorem, or Corollary 11 is used.

| 證據層 | 本次狀態 |
| --- | --- |
| 任意大小 paper | K1–K13 內 no-spoke 原 K5 route 成立，候選未採納 |
| 外部 Gallai | 上述具名 primary 文獻信任，PDF 凍結 |
| 抽象有限算術／minor controls | 四個具名 skeletons；每個 `triggered and holds`；非來源 |
| finite source | 未建立、未執行，無 source trigger 數 |
| source realizability | 未建立；被排身份不可實現的結論來自 paper 前提 |
| Lean | 無新 theorem；lake build 未跑 |
| 一般分類／核心存在性 | 未證，沒有擴張此候選 scope |

完整量詞、使用的 K 項、BASE 章節與殘留見 [獨立裁決](independent-judgment.json)。
[proof witness](proof-witness.json) 保留 symbolic bag schema 與四個固定抽象 skeletons；
skeletons 的邊是 witness 用的保留原邊子圖，未補足所有 degrees／contacts／lifts，
且本身非平面，因此不是 HIGH3 來源。控制只核 bags／十鄰接的機械敘述。

## 8. 實際重播、custody 與停止點

[只讀 verifier](verifier.py) 核14 pins、external PDF hash、精確 immutable payload manifest、
各 claim 必要欄位、固定 skeleton bags 及本 REPORT 的本地 file links／whitespace。
它不計算完整 Σ、不枚舉 disk 來源，也不裁決上述任意大小 paper 推論。

```sh
python3 -B audits/2026-10-10-n45-h3g/verifier.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h3g/verifier.py --check
python3 -B audits/2026-10-10-n45-h3g/verifier.py --check --negative-control
```

normal 與 seed17 實跑 exit 0，stdout byte-for-byte 一致；各自完整 stdout／stderr／exit／argv
保存在 `receipt-normal.json`、`receipt-seed17.json`。負控制在記憶體移去唯一 Z–O
witness 邊，實跑 exit 2，finding `H3G-NEGATIVE-ZO-REMOVED`，
保存在 `receipt-negative.json`；原 witness 不改，該控制是 `counterexample`
於這份被破壞的 witness，不宣稱修改後整圖平面。最後 pins 只讀復核 receipt 另存。

`manifest.json` 完整列 immutable payload；只排 exact top-level manifest、delivery
及四份 receipt metadata，nested 同名檔仍屬 payload。每份 receipt 綁 manifest 與 verifier hash，
`delivery.json` 再綁全部 receipts。未覆寫失敗證書；未出現需修訂的失敗版本。
只核本次 authored REPORT 的 file links／whitespace，凍結原文件的歷史 links 原樣保留。
未跑全工作樹 inventory、DocGraph、lake 或無關枚舉；dispatch 提醒的歷史缺檔、E4 provenance
與 DocGraph 62 duplicates 未修改，亦未宣稱本次重新核證它們。

精確停止點：完成 N45-H3G 既有 BASE route 的独立候選裁決，交監督與其他獨立稽核交叉驗收。
不自行採納 HIGH3，不讀 HIGH2，不研究新 P/Q shield 分類，不繼續一般 N2／E。
