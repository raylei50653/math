# 原 N2-55：兩邊盾弧的低接點 mask 同步化約

2026-10-11。權威輸入只取本 audit 的 [BASE](../BASE.json) 與 `../frozen/`。
本稿保留同一原圖、字面有序框、原 pieces／contacts／ownership／attachments／
rotation、完整 relations／空 fibres／full lifts。沒有來源搜尋、Graphify、commit 或 push。

**任意大小紙面結論：** 一份沒有 shared contact、接線總數 `k≤3`、actual support
恰為兩邊盾弧 A 的原 piece，若其三列 diagonal rejection mask 非空，則該 mask
只能是 `Eq(A)` 或 `Diff(A)`。兩份原 pieces 的兩邊盾弧若邊互斥，而且一份為 Eq、
另一份為 Diff，便有同一列完整 diagonal 接回。此結果排除 `(ℓ,u)=(1,1)` 中的
這個限定子域；其餘同類 mask 的同步仍 OPEN。

另獨立核對 [兩份低接點 long 的拓撲排除](../review/root_topology.md)：
完整 `(2,0)` 中兩份 long 都 `k≤3` 已可由原 K₅ minor 排除，不需要本 mask 分類。
本稿沒有關閉完整原55、N2 或 E-ARC2，也没有新增 Lean theorem。

## 1. 精確前提及字面 mask

完整來源契約沿用凍結 `docs/c5_excess_two_n2_diagonal_three_row.md` §1。
在其中固定

```
I={0,1,3}; D=3;
q0=01212; q1=01202; q3=01021.
```

本節 C 可以是原 unary，也可以是原 mixed；在 mixed 情形只看沒有 shared contact
的 C。因此每個原 contact 恰接一個 root，同 pins `(D,D)` 時仍是同一原 lists，
沒有合併 roots。假設 `2≤k_C≤3`，actual support 是原两邊盾弧
`A=(a,b,c)` 的完整三點集合。定義

```
Eq(A)={i∈I:q_i(a)=q_i(c)};
Diff(A)=I\Eq(A).
M_C={i∈I:C 在相同原 D pins 下沒有完整 lift}.
```

對 unary，pins 是其原 owner=D；對 mixed，是原 `(r,s)=(D,D)`。
qᵢ proper，故 qᵢ(a)≠qᵢ(b)≠qᵢ(c)（相鄰異色）；Eq 時 A 用兩色，Diff 時 A 用三色。
Eq／Diff 都非空。

使用的已採納原圖結構是：C 連通、blocks 是 bridges／奇環；每個 leaf block
有私有 root-contact；每個奇環至多一個普通私有點；全部 H 內度二點的實際框邊
附件單射。普通私有點指不是 C 割點且不接任何 root 的原點。
這些依賴均是 BASE 內凍結文件的原圖結果。

## 2. 單一拒絕列即足夠的無界 block-tree 覆蓋

固定任一 `i∈M_C`。原 lists

```
L_i(v)=[4]\(q_i(N_B(v)) ∪ {D:v是原contact})
```

是 degree assignment。不可染使它們 tight，且各 bridge 有單色 palette、
各奇環有二色 palette，同點 incident palettes 互斥，聯集為 Lᵢ(v)。
特別是 D 在 Lᵢ(v) 中恰當且僅當 v 不是 contact。

每個 H 內度二點恰接一條原框邊。其附件只能是 A 的兩條邊，附件單射因此給
**C 中這種原點至多兩個**。不把不同點合併，也不只計不同色。

對任何奇環 K，各割點的環外分支可各選一個不同私有 contact；再加環內私有
contacts 及至多一個普通私有點，得 `|K|≤1+k≤4`。故每個環都是 triangle。
若 triangle 含 contact，其 palette 不含 D，所以不可能含普通私有點。
它的三個 vertices 都是割點或私有 contacts，三個 terminal directions 至少耗三個
不同 contacts；割點自己再是 contact 就需第四個。因此 k=3 時 contacts 均為私有，
且此 triangle 的每個環外方向恰有一個 contact。

多block C 的 block-cut tree 有兩或三個 leaves。含 contact 的 leaf triangle
有兩個私有 contacts。若有三個 leaves，它們只能都是 bridges，每個私有端是
contact、在 H 中內度二，便需三條不同原框邊，矛盾。故只剩兩個 leaves。
這個計數不限制鏈長；以下直接由兩個實際附件邊的容量排除全部中間 blocks。

### 2.1 單一 block

Singleton 沒有 shared contact 時不能是 mixed，也不符合 k≥2。
單一 bridge 的兩端都必為 contacts，k=2；兩端各接一個不同原框邊，故恰用 A 的
兩條邊。單一 triangle 若含 contact 和普通私有點，D 的 palette 成員矛盾；
若全為三個 contacts，其三個框点附件必同色才能拒絕。但 actual support=A
包含相鄰框點，proper row 排除此情形。

### 2.2 兩個 bridge leaves

兩個原私有 contact 端點已耗盡 A 的兩條附件邊。任何普通兩bridge割點，或無contact
triangle 的普通私有點，都會是第三個 H 內度二點，因此不可能出現在兩端之間。
無contact triangle 若無普通私有點就有三個割點，需三個環外 contacts，也不可能
落在只有兩leaves的 block-cut path 上。

若有含contact triangle，它有兩個割點及一個私有 contact，三個 contacts 已用盡。
兩個 bridge leaves 只得直接鄰接這個 triangle，否則中間會有上述第三個附件點。
triangle palette 不含 D，而兩個不接root的環割點 lists 含 D，故兩個 incident
bridges 的 palette 都只能為 D；這與 leaf contact 的 bridge palette 是已用色矛盾。

所以只剩：單一 bridge（k=2），或三點 path `p–w–q`（k=3、三點全為contacts）。

### 2.3 一個 triangle leaf、一個 bridge leaf

triangle leaf 的兩個私有點 x,y 均為 contacts；bridge leaf 的私有端 p 是第三個
contact，沒有額外 contact。triangle 的 cutpoint z 不接root。
其餘 block-cut path 只含 bridges 及無contact普通 triangles。

每個普通兩bridge割點、每個普通triangle私有點都是 H 內度二點。
原端 p 已占一條附件邊，故 path 最多再有一個這樣的原點。

* 沒有額外點：僅原 bridge `z–p`。z 的 triangle palette 不含 D，而 list 含 D，
  故 bridge palette 為 D，與 p 的已用色 palette 矛盾。
* 恰有普通兩bridge割點 w：保留完整原圖形 `triangle xyz` 加 `z–w–p`；共五點。
* 恰有普通triangle私有點 t：給原 vertices 清楚的名稱，保留 `triangle x1 x2 z`、
  `triangle z w t`，另有 `w–p`；共六點。
  兩個 triangles 必須直接共享原 z。若有 bridge 先連 leaf triangle 的 z 到普通
  triangle 的另一割點，該 bridge 在 z 端必取 D，而普通 triangle palette 因其普通
  私有點必含 D，互斥性矛盾。另一端 w 必直接連 p，否則還有第二個額外附件點。

兩個 triangle leaves 需至少四個 contacts，已排。這完成任意大小的窮盡；
不是從有限 motif 枚舉外推。

## 3. 四份保留原座標的非空 mask 形狀

令原框邊 `ab`、`bc` 的已用色缺色為 `T_i(ab)`、`T_i(bc)`。
兩者相同恰當且僅當 `i∈Eq(A)`；不同恰當且僅當 `i∈Diff(A)`。

| 原圖形 | k | H內度二點 | 非空 mask |
| --- | ---: | --- | --- |
| 單bridge，两端均contacts | 2 | 两端各附一条 A 邊 | Eq(A) |
| 三點path，三點均contacts | 3 | 兩端各附一条 A 邊 | Diff(A) |
| leaf triangle 加兩bridge tail | 3 | tail 中点 w 及contact端 p | Eq(A) |
| leaf triangle 直接共享普通triangle，再接leaf bridge | 3 | 普通triangle私有 t 及contact端 p | Diff(A) |

第一形的两个 lists 是單色 T(ab)、T(bc)，bridge 不可染恰為两色相同。
第二形的中點有一個原框點附件 h。两端 leaf palette 若相同则不能成为中點的
互斥 incident palettes；若不同，中點附件的色必為第三色。三色的 A 中，这唯一
逼定 actual h=b。若 h≠b，mask 為空；若 h=b，所有且僅所有 Diff rows 都拒絕。

第三形在 w 處的兩 bridge palettes 必為 `{D,T_i(e)}`，故兩不同原框邊的 T 相同，
也就是 Eq row。原 triangle 的三个框点附件必须同色。Eq row 在 A 中只有中點一类，
與兩端同色另一类，因此 actual triangle 附件只能是「全部中點」或「全部属于兩端」
才能有任一拒絕。兩種都在所有 Eq rows 同色，所得 mask 恰為 Eq(A)。
這裏保留全部原 triangle 頂點及附件，沒有把三點先合併。

第四形普通triangle的palette為 `{D,T_i(f)}`，leaf bridge palette為 `T_i(e)`。
兩者在 w 處互斥，故只能是 Diff row。w 的 actual 框點附件必為中點 b；
leaf triangle 的兩個 contact 附件必為 `T_i(f)` 色，其 actual 點唯一是 f 對邊的
那個弧端點。所有 Diff rows 由同一原附件滿足這些條件，所得 mask 恰為 Diff(A)。
上述 palette 條件本身也給完整 degree-list obstruction；其他 rows 若不可染又會
由同一窮盡推得同樣條件，因此確定完整 mask，而非只得到 mask 的上界。

**定理 M-LOW-ARC。** 在§1局部前提內，`M_C∈{∅,Eq(A),Diff(A)}`。
非空 mask 的四形如上；原非空 pieces 大小分別為2、3、5、6。
命題僅分類 diagonal；完整 off-diagonal relations 仍保留且沒有由 mask 反推。

## 4. 原同列同步的新限定排除及精確 residual

五份字面兩邊盾弧的 mask 如下；a,b,c 均是同一原有序框點，沒有逐件 D₅ 正規化。

| A | Eq(A) | Diff(A) |
| --- | --- | --- |
| 012 | {3} | {0,1} |
| 123 | {0} | {1,3} |
| 234 | {0,1} | {3} |
| 340 | {1} | {0,3} |
| 401 | {3} | {0,1} |

五份邊互斥的無序 arc pairs 是 `(012,234)`、`(012,340)`、`(123,340)`、
`(123,401)`、`(234,401)`。直接由表可得：每份 pair 上一個 Eq mask 與一個
Diff mask 的聯集都是 I 的真子集。若任一 mask 為空，也因另一為 I 真子集而有出口。

在完整 `(ℓ,u)=(1,1)` 來源內，已採納盾弧預算給 U、long L、short S 的原盾弧
恰長 `(2,2,1)`，U／L actual supports 都是兩邊弧。U 已知 k=2或3。
若 L 有 shared contact，其 mask 為空，沿用已採納排除。否則若 `k_L≤3`，
定理 M-LOW-ARC 適用兩份原 pieces。兩份 mask 不同類，或任一為空，就選同一個
`i∈I\(M_U∪M_L)`。原 r=s=D 避開全部spokes，原short S 由 N-diagonal 完整接回；
U、L 亦各有同一列完整 lifts。所有原分量互斥，原邊和自由孤立四色因子全接回，
違反指定原拒絕列。

**推論 M-MIXED-TYPES。** `(1,1)` 的無sharedcontact low-contact long 子域，只需
保留兩份非空同類 mask。Eq／Eq 要覆 I 只剩 `(012,234)` 或 `(234,401)`；
Diff／Diff 在上述五個邊互斥 arc pairs 上都可能覆 I。
这些七個是必要模板，不是七份來源或完整 joint counterexamples。
一般 `(1,1)` 及 k_L≥4 均仍 OPEN。

完整 `(2,0)` 中兩份 long 都 `k≤3` 已由另一原圖拓撲證明排除；見§5。
所以不能把本表的同類 mask controls 宣稱為該子域的原來源。

## 5. 對原 topology 證明的獨立核對

已逐字核對 `../review/root_topology.md` 的兩個命題，採納範圍只在 BASE 的完整契約。

T-SAME-EDGE 的中央 biconnected block 包含原 r,s 及全部 mixed 頂點。
對原附件頂點 v，兩點 fan 的兩個端點可分別取 r,s；截到首次碰原 roots 後，
所有中間點都屬同一原 C。另一原 mixed C′ 給內部互斥的 r–s path。
五袋 R、S、X、Y、Z 中，R 是 r 加另一條 path 的內點，Z 是經 v path 的內點
加連通補框弧 `B−{a,b}`，原附件 vh 把兩部分接起。五袋互斥，十對鄰接全由
原spokes／path首末邊／原框邊給出；K₅ minor 完整有效。

T-TWO-LOW-LONG 的計數 `10=k_P+k_Q+t_r+t_s`，搭配每root至多兩個框附件，
逼 `k_P=k_Q=3,t_r=t_s=2`。盾弧 `(2,3)` 的唯二可用端點不相鄰，與兩個
相鄰root框附件矛盾；盾弧 `(2,2)` 的三个可用端點只有一對相鄰，恰為剩餘原框邊。
兩roots因此都接同一邊兩端，而原long有該pair之外的實際附件，T-SAME-EDGE 適用。
有sharedcontact的情形先由完整 diagonal 接回，沒有把不同列的存在性拼接。

因此完整 `(2,0)` 的存活必要條件改為：**至少一份原long k≥4**。
這是任意大小紙面排除，與有限 motif controls、來源實現、Lean 分開。

## 6. 校準、負控制與本稿停止點

[signatures.py](signatures.py) 驗證 BASE 全部13份 frozen 文件 bytes／SHA，然後只計
五份字面 arc signatures 與20份 mask 聯集。没有圖枚舉或來源生成。
[observations.json](observations.json) 保存五份arc、五份邊互斥pair及全部聯集／空出口。
其中10份混類mask controls都是 `triggered and holds`；兩份 Eq／Eq、五份 Diff／Diff
覆 I，是「任意真子集自動同步」的抽象反控制 `counterexample`，並非來源。

另一 worker 的 [controls](../controls/observations.json) 用保留原座標的完整十列16-pin
fibres 校準四形；800份 actual attachments controls 與45份完整 exemplars 皆與本分類相容。
無有限完整 N2-55 target source，本稿來源層是 `not triggered`，紙面推論承担無界結論。
本稿只依賴它作有限校準，不以它證明 block-tree 完備性。

曾提出的兩個較強猜測已撤回並保留此記錄：tailtriangle 只能把三個triangle附件放在
弧端點是錯的（全放中點也給 Eq mask）；剩一條附件邊會迫 short S 为 singleton shared
也是錯的（兩contacts＋一普通私有點的原triangle只耗一條附件邊）。兩者均未用於結論。

```bash
python3 -B audits/2026-10-11-n2-long-mask-sync/synchrony/signatures.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/synchrony/signatures.py --check
```

正常及 seed17 重播實際 bytes／SHA 相同，精確 receipt 見 `verification.json`。
本 worker 不修改 shared docs，不執行發布，也不把成功 lake build 說成本稿 Lean 化。
原 `(1,1)` 的同類mask模板、long k≥4、完整原55／N2／E-ARC2 仍 OPEN。
