# 五度原星的封鎖分量：完整回返、短週期排除與緩衝區

2026-10-30 後續：[S5 與週期四](c5_kempe_period4_s5.md)給五個共同原面的短路限制、
完整附件五環的來源排除及固定五環對兩輪差異的剛性，另保存有限搜尋與獨立重播；
一般週期四與全封鎖命題仍 OPEN。以下保留 2026-10-29 的證據與停止點。

2026-10-29。研究任務採用逐 **Kempe 著色分量** 的量詞，不假設命題成立。
本輪得到同一三角化 disk 來源的必要條件：指定五步正規化回返的週期全為偶數，
且沒有週期二，因此假設存在的全封鎖分量，每個固定字面五環 fibre 為偶數且至少四份。
它排除 D 容許的具名薄 fibre 模型，沒有排除整個 support 932，也沒有證明一般逃逸。
緩衝區保留完整 O；後面的真圖控制追蹤回返如何改變近處及遠端。

依賴：[D 的精確判準與停止範圍](ck_d_lock_comparison.md)、
[逐 class 計數與限制](c5_kempe_class_counts.md)、
[既有共同切口與迭代反例](four_color_counts_surgery_continuation.md)。
完整證據在 [本輪目錄](../audits/2026-10-29-kempe-realizability/)。

## 1. 圖類、局部族與同一接口

為避免用「真的最小不可四色圖」作空泛圖類，本輪固定可有限檢查的結構必要條件。
令 \(\mathcal G_{\mathrm{str}}\) 為帶固定球面嵌入的有限簡單三角剖分，滿足：

1. 每點度數至少五。
2. 沒有 separating 3-cycle 或 4-cycle。
3. 任一 separating 5-cycle 的兩個開側，至少一側恰有一個頂點。

這些是本輪明列的最小反例必要條件，不聲稱已列盡所有可約構形限制。
不將不可四色性或「所有較小圖可四色」寫入此結構類；兩者若用於反證需另作假設。
Euler 保證此類若非空有五度點。
為排除空著色空間造成的真空通過，正式研究圖類再取
\(\mathcal G=\{G\in\mathcal G_{\mathrm{str}}:
\forall v\text{ of degree }5,\ \operatorname{Col}_4(G-v)\ne\varnothing\}\)。
這項只確保外部有起始分量；最小反例由嚴格較小性滿足它，有限控制則由實際完整著色核對。
它沒有用「存在初始著色能延拓」替代後面的全部分量要求，也不要求 G 不可四色。

主要允許族固定為 \(\mathcal I_5(G)=\{I_v:d_G(v)=5\}\)。
沿原 rotation 命名 \(B=(b_0,b_1,b_2,b_3,b_4)\)，令

\[
I_v=G[\{v\}\cup B],\qquad O_v=G-v.
\]

私有核心恰為 \(\{v\}\)，外部少一個原頂點。上述短環條件使鄰環為 induced C5；
定義本身仍要求兩側保留各自端點間的**全部原邊**，不靠刪弦改變接受集。
兩圖的交集恰為同一帶次序的原 B，聯集恰為 G，無私有跨邊。
\(\operatorname{Ext}_4(I_v)\) 中的 proper B 恰用三色：五環不能只用兩色，
用三色時缺的第四色可給 v。

較廣義合法 disk 分解可寫成非空私有集 X、分隔環 B 及另一側 Y，
\(I=G[X\cup B], O=G[Y\cup B]\)，要求 \(V=X\sqcup B\sqcup Y\)、
X–Y 無邊、兩側全保原邊、\(|O|<|G|\)。本輪**不**把這個未設大小界的全族
當成「局部」族，也不把緩衝區併入 X；主要量詞始終是

\[
\forall G\in\mathcal G\ \exists v\ (d(v)=5)\quad
\forall K\in\operatorname{Comp}(\operatorname{Kempe}_4(O_v)),\quad
\{c|_B:c\in K\}\cap\operatorname{Ext}_4(I_v)\ne\varnothing.\tag{Q5}
\]

Kempe 圖的頂點是完整字面 proper 著色，邊是交換任一色對的一個完整 induced component；
允許不碰 B 的交換。色名商可用作計算，但不取 B 的旋轉／反射商。
全域換色本身可由逐分量交換完成，所以每個 K 對共同 S4 作用封閉。

否定固定 v 只需一個完整封鎖 K；否定 Q5 的 \(\exists v\) 需對同一 G 的
**所有**五度點各給封鎖分量。本輪未找到任何這類反例。
把 \(\forall K\) 改成存在某份初始著色，對合法固定分解便等價於 G 可四色；本輪沒有採取此弱化。

## 2. 「完成至 22 點」的證據核對

[C5→C4 來源橋](c5_c4_boundary_pivot.md) 的 \(K_{\le22}=K_{\le5}\)
指的是 **disk 內點數至多 22**，即總點數至多 27；分類的是整張 disk 的完整邊界關係。
它經新增一點的來源化約，使用外部至多 28 **總點數**的 C4 candidate census，
信任邊界見 [EXTERNAL.md](../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/EXTERNAL.md)。

這不是「22 總點三角剖分的全部五度星、全部 Kempe 分量皆已驗證」。
單一 K 也不必是另一張 disk 的完整著色空間，故不能對 K 套用完整關係 census。
原逐 class 報告已明示這個界線。

本輪重播三項既有有限 checker：132 原來源、528 份完整 C4 fibres、1,024 抽象 supports；
獨立 430,080 字面查詢、1,080 cap lifts；132 個 catalogue witnesses 的逐 class 計數，
另有十分量控制。外部大 census **未重跑**；這 132 witnesses 各自恰一分量，不能當逐分量全域覆蓋。
新成果不是擴大這個枚舉，而是下列完整歷史必要條件。

## 3. 完整著色傳輸與非平凡回返

假設一個 K 完全封鎖；固定字面 \(b^0=(A,B,A,C,D)\)，
\(X_0=\{c\in K:c|_B=b^0\}\)。若起始是其他四色型，以下雙射沿五型循環可到 02 型。

| 步 | 當下色對／root | 當下 component 與 B 的交集 | 字面邊界 | 重色位置 |
| --- | --- | --- | --- | --- |
| 0 | — | — | ABACD | 02 |
| 1 | AD／2 | {2} | ABDCD | 24 |
| 2 | BD／4 | {4} | ABDCB | 14 |
| 3 | BC／1 | {1} | ACDCB | 13 |
| 4 | AC／3 | {3} | ACDAB | 03 |
| 5 | AD／0 | {0} | DCDAB | 02 |

首態的 B、C 單色位置 1、3 必由 BC 路連通，否則交換含 1 的分量立即得到三色框。
AD 的 0–4 原邊連通；若 component(2) 也碰它，AD 的 0–2 路與 BC 的 1–3 路在
disk 中交替且頂點互斥，違反 Jordan 分離。因此交換分量的框交集恰為 {2}。
其餘四步對**當下**著色重作同一論證。每個 component 交換是完整著色的 involution，
在相應兩份固定字面 fibres 之間給雙射；逆交換使用同一色對／root。
全部原圖著色、空／非空 fibres 及 component 身份都沒有投影掉。

末框為 \(\sigma b^0\)，其中 \(\sigma=(A\ D\ B\ C)\)。令

\[
F=f_5f_4f_3f_2f_1,\qquad H=\sigma^{-1}F:X_0\longrightarrow X_0.
\]

H 是有限集合的置換，不能從框回返推出完整著色不變。
其逆為 \(f_1^{-1}f_2^{-1}f_3^{-1}f_4^{-1}f_5^{-1}\sigma\)。
五型完整 fibres 等量只是這個結構的一個推論。
[紙證與全部 120 態 D 模型](../audits/2026-10-29-kempe-realizability/transport/PROOF.md)
另保存每態三個 split 的全部分割核對及所有單 block actions，沒有只挑單份 marginal。

### 純紙面限制：含三角形的來源沒有固定點

若 H(c)=c，每個原頂點的五步六時刻歷史，末色必是 σ(初色)。
逐次容許「不變」或「受當步 transposition 交換」，可能歷史恰為：

```text
AAAAAD  BBBCCC  ADDDDD  CCCCAA  DDBBBB  ADBCAD
```

原邊兩端在六時刻必始終異色。前五類的相容邊恰為按上述順序的 C5，
最後一類孤立。因此原圖映到無三角形的相容圖；只要原圖含一個三角形就矛盾。
六歷史窮盡及相容邊另有精確整數證書。這一步不需要平面性，但需完整同源歷史。

## 4. 原三角面附件與共同填充限制回返週期

**條件式定理。** 對指定有序 C5 外界、其餘所有面皆三角形的有限 disk O，
假設 K 完全封鎖，則 H 的每個週期長度為至少四的偶數。因而每個固定字面四色邊界 fibre
的完整著色數 \(m\ge4\) 且為偶數。不假設這樣的 K 實際存在。

### 同一原附件的紙面奇偶限制

令 w 為原邊 b3–b4 在 O 側三角面的第三頂點。同一 w 必在五步所有時刻同時避開
b3、b4 的當下顏色；其六時刻歷史只有兩種：

```text
初色 A：AAAACC，正規化末色 σ⁻¹(C)=B；
初色 B：BBDDDD，正規化末色 σ⁻¹(D)=A。
```

逐步檢查：前者第一步不能換成與 b4 相同的 D，第四步必由 A 換成 C；
後者第二步必由 B 換成 D，第五步不能換成與 b3 相同的 A，其餘色對不作用於當時顏色。
因此 \(H(c)(w)\) 在 A、B 間交替。所有 H 週期必為偶數；有限 X0 中 w=A、w=B
兩族亦被 H 雙射配對。這項使用原三角面的**同一實際附件**，不是各時刻換一個第三點。
它排除全部奇數 m，超過等量五型的限制，但尚容許週期二。

### 紙面面鏈化約與有限 cocycle 證書

證明的拓撲化約如下，最後使用三份可獨立驗證的有限 F2 證書。
若 \(H^k(c)=c\)，串接 k 輪五步交換，每輪後對**整份**著色作 \(\sigma^{-1}\)。
每個原頂點得到一條長 6k 的時間歷史。各輪內每步容許留色或交換色，
輪間強制同一 \(\sigma^{-1}\)，最後正規化後回到初色。

枚舉全部滿足這些逐點條件的歷史為 \(V(T_k)\)。兩歷史在**每個時刻**都異色才連邊，
任三個兩兩相容的歷史都列為三角面。這是實際分量交換的鬆弛：沒有把逐點留／換
當成分量可獨立指定，也沒有假設每條歷史能實現。
每條原邊映到 \(T_k\) 的邊，每個原三角面映到其三角面；初時刻 properness
保證三頂點不退化。

將 O 的全部三角面在 F2 下相加，內邊各出現兩次而消掉，只餘原 B。
歷史映射即使把不同原面／原邊合併，仍保此鏈等式。故指定五條邊界歷史形成的
\(\gamma_k\) 必為 \(T_k\) 的一條三角面邊界和。

證書反而給一份邊函數 \(z_k:E(T_k)\to\mathbb F_2\)，滿足

\[
\forall \text{相容三角形 }abc,\quad z_k(ab)+z_k(bc)+z_k(ac)=0,
\qquad \sum_{e\in\gamma_k}z_k(e)=1.
\]

任何三角面邊界和在 z 下都為零，與最後一式矛盾。

| k | 全部逐點歷史 | 全部相容邊 | 全部相容三角形 | γ 的 z 值 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 6 | 5 | 0 | 1 |
| 2 | 46 | 195 | 200 | 1 |
| 3 | 309 | 3,611 | 5,324 | 1 |

[history-cocycles.json](../audits/2026-10-29-kempe-realizability/history-cocycles.json)
保存全部歷史、邊及 z 的非零位置；checker 直接逐三角形核和，不需信任高斯消元結果或 rank。
週期二的排除完成定理；k=1、3 證書與上段全部奇週期紙證交叉核對。
因此完整定理的證據層是**紙面化約＋精確有限 F2 證書**；不是已完成 Lean 的純紙面一般定理。
其他 Kempe 交換可以在這條 H 軌道之外提供逃逸；本輪沒有省略它們或證明它們無效。

### 明確排除力與 D 仍開放的部分

具名 **SINGLE-FIBRE-5** 有全部 120 份字面四色框，每框恰一態，無三色態。
每態的三份完整 joint partitions 都符合 D；全部單 block 交換可逆且留在同一個 120 態分量。
這份完整抽象 automaton 已逐 action 保存。其 02-fibre 僅一態，所以 H 必固定它，
與上節含三角形的同源必要條件矛盾。這提供一個 D 容許、而新條件拒絕的**完整傳輸模型**。

更一般具名薄 fibre 候選 **THIN-932(m)** 的五個四色型每個固定字面 fibre 恰 m 份，
三色 fibres 全空；全部奇數 m 及 m=2 均由本節排除。它們的 support 都是 D 存活的 932，
且通過既有逐 class 等量式及非負性；原 B5 必要計數資料也容許正倍數 mt。
後者只引用 [既有特殊 ray](c5_b5_face.md#3-十二條-rays-的完整-support)，
本輪未重新證明 B5 ray 完備性。m=2、3 在此是必要計數／fibre 模型，
沒有另聲稱已構造連通、交換相容的完整 automaton。

這超過五型全支援、等量與單步鎖定，因為約束的是**完整著色回返週期**及共同三角面。
但在只看布林邊界 support 的層次，仍然沒有刪掉 932；沒有得到新的 D-可約構形，
也沒有把「這份薄模型不可實現」提升為「全部平面封鎖分量不可實現」。
既有 [LOCK-NO-GAIN](ck_d_lock_comparison.md#lock-no-gain由交換仍在-b-推出的鎖定已包含於-d)
的單 split 停止裁決保持；本輪使用其範圍外的跨步共同原面資料。

## 5. 緩衝區仍保留全外部

固定 O 與 B0=B，取距離層 \(L_j=\{x\in O:d_O(x,B_0)=j\}\)。
對 r=1、2 定義

\[
A_r=O[B_0\cup L_1\cup\cdots\cup L_r],\quad B_1=L_r,\quad
E_r=O[L_r\cup L_{r+1}\cup\cdots].
\]

此時 O=Ar∪Er，交集為同一有序 B1，全部原邊完整保留；B1 不保證是簡單環。
固定次序用原頂點標號，不能各自重排附件。若某層空，記錄此退化情況，不能假造遠端。

延拓狀態保存 Ar 在 B0、B1 上的**完整聯合關係**，每列保存全部私有內點著色 fibre，
含無延拓的列。與遠端接合只用同一份 B1 assignment。
換色狀態則對同一份完整 O 著色記錄每個色對的全部 components，包括不碰兩界的分量，
以及各 component 在 Ar、Er 的原頂點／原邊、兩界交集及遠端重接。
合成時取 Ar 與 Er 的實際雙色分量在 B1 上的等價閉包；不能把 Ar 中一段鏈直接當全 O 分量。
交換後重算當下兩側及全 O 的 components，不沿用交換前的 connectivity。

本輪三種量詞的處理：觀察 Ar 完全保留 O；限制只換 Ar 並固定 Er 是更強的局部修復
候選；把 Ar 併入 I 則更換了局部族和外部著色空間。後兩種未用來判定 Q5。
H(c)|B0 恢復也不推出 H(c)|Ar 恢復，更不推出全域 Kempe 可達性由有限寬 buffer 決定。

### 真圖定向控制與反控制

[緩衝區完整報告](../audits/2026-10-29-kempe-realizability/buffer/REPORT.md)
與[證書](../audits/2026-10-29-kempe-realizability/buffer/certificate.json)保存原圖、rotation、
全部外部 states、完整 fibres、實際遠端附件與所有分量交換。
逐著色／色對／buffer，將遠端每個完整雙色分量縮成連接其**全部實際附件**的輔助星，
再與 Ar 的原雙色子圖接合；所得在 Ar 的連通分割逐份等於 full-O BFS。
正反向路徑分段即可紙證這項精確接合，不預設 buffer 隔斷鏈。
局部 Ar 與遠端 Er 另各自完整枚舉，逐列驗證 \(R_A\Join R_E=\operatorname{Col}_4(O)\)，
沒有把全 O 的投影冒充全部局部延拓。例如二十面體第一 buffer 有 50 份局部正規化著色，
只有 20 份可接遠端；Errera 第二 buffer 有 260 份，只有 100 份可接遠端。
證書將這兩類表分開，局部 fibre 列全部私有著色，未列的接口 tuple 明定為空 fibre。

| 固定原圖、刪五度點 | 是否在本輪結構類 | 完整外部 S4 states／classes | 一層／兩層遠端重接紀錄 | 指定五步完整回返 |
| --- | --- | --- | --- | --- |
| 二十面體 | 是 | 20／1 | 40／0 | 無 |
| capped-antiprism-6 | 是 | 40／1 | 74／0 | 無 |
| capped-antiprism-7 | 是 | 68／1 | 192／0 | 無 |
| Errera−v0 | 否：separating C5 兩側各六點 | 100／1 | 120／160 | 一個週期四 |

重接以「完整著色、色對、full component」計數；前三圖的兩層 buffer 已含整個 O，
所以該項零不代表一般兩層自足。二十面體的一層反控制完全在結構類內：
state0、色對 {0,2} 的原分量 {1,3,6,8,10,11} 在 buffer 中分成
{1,6,8}、{10,11}，由遠端原點 3 接回。它直接反駁「一層可隔斷分量」，不是封鎖反例。

Errera 的 H 在 buffer 證書索引 16→24→17→25→16；每輪五個交換都是實際完整分量交換。
B0 回復時，第一外層的 {2,6,8,9,13} 全改色，更遠第三／四距離層也改色，
故一／二層 buffer 都未恢復。這證明「框回返⇒緩衝回返」在這個較弱的 δ5／S34 圖類失敗，
不能升格為本輪 S5 類的反例。

[原圖短環與五個定向翻邊控制](../audits/2026-10-29-kempe-realizability/source/PROOF.md)
另保存 Errera 的 20 次真交換、原面、所有短環兩側，以及直接處理其分隔五環的五個合法翻邊。
翻邊後五圖各有 68 個外部 states，均符合本輪結構條件，但未有指定 H 週期。
這只是針對該候選的反控制，不證 S5 排除所有週期四。
[獨立 checker](../scripts/c5_blocked_source_history_review.py)也將真 Errera 的 25 個 disk 三角面
映到 k=4 時間歷史，直接核對其面鏈邊界恰為 γ4；所以不能把 k≤3 的 cocycle 外推成所有 k。

全部控制的完整 Kempe classes 都有三色框。完整封鎖性需另核全分量，
五步都維持四色框只是一段局部可行歷史；本輪既沒有固定 I 的封鎖反例，也沒有否定整個局部族。

## 6. 證據層、重播與 OPEN

一般合法分解、雙射、Jordan 強制、時間歷史投影及三角面鏈等式為紙面論證；
奇週期的原附件排除為純紙面；週期二的排除使用上述精確 F2 證書。
原 22 內點界另有外部 census 依賴，本輪未重跑。
沒有新增 Lean theorem、沒有以 4CT 作 oracle、沒有新增圖枚舉上界。

文獻對照：Tilley, [D-resolvability of vertices in planar graphs (2017), pp.650–651](https://jgaa.info/index.php/jgaa/article/download/paper433/2530/2337)
用 G−v 的「difficult component」描述同類逐分量問題，並將普遍 D-resolvability 列為猜想。
本輪不把其實驗或文中直觀敘述當成定理，也不聲稱已完成全面文獻新穎性審查。

大型 source、buffer JSON 依既有 audit 規則壓縮保存，原 bytes 保留。
新 checkout 先 `python3 tools/audit_archive.py restore --artifacts` 還原本輪及舊依賴，
再執行下列 checker；封存只處理資料保存，不是數學驗證。
實際驗證及文件傳播範圍見 [收尾紀錄](../audits/2026-10-29-kempe-realizability/VERIFICATION.md)
與 [逐命令收據](../audits/2026-10-29-kempe-realizability/verification.json)。

```bash
python3 audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/controls/check_transfer.py --check
python3 audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/check_independent.py --check
python3 scripts/c5_kempe_class_counts.py --check
python3 scripts/c5_blocked_transport_return.py --check
python3 scripts/c5_blocked_history_homology.py --check
python3 scripts/c5_blocked_source_controls.py --check
python3 scripts/c5_blocked_source_history_review.py
uv run --with networkx==3.5 python -B scripts/c5_blocked_buffer_probe.py --check
```

OPEN：S5／實際附件如何限制 H 的較長週期；如何由假設封鎖強迫一條共同切口矛盾；
是否存在任意固定 v 的真全封鎖 K；Q5 的存在局部星量詞；任何擴大的局部族覆蓋。
本輪增加完整回返週期與薄 fibre 排除，不能回寫成一般四色性或全分量逃逸定理。
