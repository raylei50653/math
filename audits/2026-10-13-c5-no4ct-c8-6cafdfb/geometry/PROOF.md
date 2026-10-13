# C8 依賴接入：相對大小的小 cap 與共面識別

2026-10-13。只屬本隔離 audit 的紙面依賴修復，不修改共享入口或舊證書。
額外直接輸入逐檔封存於 [INPUTS.json](INPUTS.json)；前序 no4ct、C8-STRUCT
則讀父 audit 的 frozen bytes。下游數值重播結果由父 audit
[結果](../RESULTS.json) 與 [驗證總帳](../VERIFICATION.json) 採納，
本文件的紙面接入不以正常執行、零反例或零 source triggers 代替證明。

**結論：新三支最小來源契約足以恢復原內部 C3／C4／C5 cap、induced C8
及完整 noncrossing quotient 正性；不需要四色定理。** 所需可染性來自
全域最小來源下的有限頂點界，而非把 C8 disk 當成較小 C5 disk。
父 audit 已核對八項原契約、共同上界及 apex／m9／m10 的完整證書，
既有下游鏈亦已接回 `h=3 ⇒ k≥19`。無界三支與一般主命題仍 OPEN。

## 1. 同一全域最小來源

K 是固定 132 個完整 C5 關係及至多五內點 witnesses。反設目錄外來源存在，
在所有有限簡單 C5 disks 中先最小化原內點數 k，再最大化邊數。原有序
外框 B 始終有五個互異點；原圖、附件及完整十列共同搬運後
`Σ(G)∈{932,933,941}`。不是各固定 mask 自己的最小性。

前序 [度數修復](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
及 [完整外圈](../frozen/audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md) 已給：
`k≥16`、G 簡單二連通、B chordless、內面全三角、內度至少五、框度至少四、
無 occupied separating triangle、沒有二邊原框 crosscut，以及實際簡單
內圈 `C_(5+h)`、`h≥3,n5≥9`。這些是同一最小来源的條件結論。

當 h=3，C 為八個互異原內點組成的實際內圈，含五個 apex A 及三個 y 點 Y。
內側 H 包含 G 的全部原內點，故

\[
|V(G)|=k+5,\qquad |V(H)|=k,\qquad m=|V(H)\setminus C|=k-8. \tag{1}
\]

apex 恰接兩個原 B 點、y 恰接一個，H 嚴格內點不接 B。因此
`d_H(A)≥3,d_H(Y)≥4,d_H(H−C)≥5`。不能將 m 當作另一個 C5 來源的內點數。

## 2. 小 cap 的嚴格大小及完整關係替換

令 Q 是原 G 的簡單環，取不含原 B 點於嚴格內部的一側為 cap。令 s 是
cap 嚴格內點數，r 是 Q 上原內點數，e 是 cap 外原內點數。精確地

\[
k=s+r+e. \tag{2}
\]

本輪 C8 chord、短 crosscut、剝層使用的 C4／C5 都完全在原 B 内側，故
分別有 `r=4` 或 `r=5`，從而

\[
s\le k-4<k\quad(C4),\qquad s\le k-5<k\quad(C5). \tag{3}
\]

即使 Q 接觸 B，C4 也不可能只使用 B 點，因 B chordless；異於 B 的 C5
亦至少含一個原內點。此時 r≥1，仍有 s<k。對 Q=B 則不能聲稱這一不等式。
本輪下游只消費完全內部版本，不需要擴大 cap 範圍。

受限 C4 引理已由度數修復證明：對 s<k 的任意有序 C4 disk，沿框邊外加
degree-two dummy 作第五框點，C5 的內點數仍是 s，故完整關係在 K；
16-mask 增廣表給原 C4 關係至多三內點代表。这里不引用任意大小 C4 定理。
C5 cap 直接由 s<k 的全域最小性取得 K 中至多五內點代表。

在原有序 Q、相同 literal 色值下替換完整關係相等的 cap，對每一外側完整
染色，其內側可延伸的真假不變，故保留原 B **全部**十列，包括空 fibres。
替換保持原 Q 名字與外側圖；新私人內點用新名字。若兩側邊重複，平行副本
簡化不影響平面性或 properness。新圖只需屬最初 disk 圖類，不必保有飽和性
或度數界。故 s>3 的 C4 或 s>5 的 C5 可減少原內點，違反全域最小性。
得到 C4 的 s≤3 與 C5 的 s≤5。這是延伸存在性的完整關係保真，不聲稱
替換前後 full lifts 等量或有雙射。

對長 b、s 嚴格內點的三角化 cap，令 q 為框弦數、j 為內點誘導邊數。
Euler 給

\[
\sum_{v\in\operatorname{int}Q}d(v)=3s+b-3+j-q. \tag{4}
\]

嚴格內點没有 cap 外鄰點，故 cap degree 等於原 G degree，至少五。
C4 的 s=1,2,3 時，(4) 右側各至多 4,8,13，皆小於 5s；故 s=0。
C5 若 2≤s≤5，每個嚴格內點須有框鄰點，否則 degree≤s−1≤4。
這些接框邊證明其誘導子圖在繼承嵌入中 outerplane，故 j≤2s−3；
但 (4) 及最低度五又給 j≥2s−2+q，矛盾。因此 C5 的 s 只有 0 或 1。
s=1 時唯一內點接全部五個框點，Euler 迫 q=0，cap 恰為 W5。

無 occupied C3 則沿用原來源已有完整染色及三角形唯一 proper S4 軌道：
若內側有點，清空後任何外側染色可對齊原內側染色接回，完整 Σ 不變且更小。
此步不使用任意圖的可染性。總結：

\[
\boxed{\text{原內部 C3、C4 cap 為空；原內部 C5 cap 為空或一個 W5。}} \tag{5}
\]

## 3. 原具名 C8 必為 induced

若 C 有 chord，其最短環距為 2、3、4。

- 距離 2：短側為空 C3，短弧中點在 H 的內側 sector 已填滿，H-degree=2，
  違反 C 上最低度三。
- 距離 3：短側為空 C4，唯一對角線至少漏掉一個短弧中點；該點 H-degree=2。
- 距離 4：兩側為 C5。空側的 polygon triangulation 至少兩個不相鄰 ears；
  chord 兩端在該 cap 上相鄰，故有一個非端點 ear，H-degree=2。
  因此兩側都必為 W5，各側三個弧中點在 H 的 degree 恰三。
  六個非端點中至少包含一個 y，因 C 有三個 y 而 chord 只有兩端；
  這與 y 的 H-degree≥4 矛盾。

耳引理來自 polygon 三角剖分的對偶樹；長度至少四的 polygon 中，兩個相鄰
環點不能同時為 ears，否則所需對角線交叉。三角形則直接取非指定邊端點的
第三點為 ear。上面的度數都是同一原 embedding 中的完整 sector，
沒有以抽象 support 或另一列染色替代原邊。此證明逐一適用所有 h=3
三支查詢，不以 933／941 或 P 非空為前提。

## 4. 相對 k 的平面圖可染性：真正的 quotient 接點

前序 [dependency 引理 A](../frozen/audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)
不以四色定理為前提，證明：若有不可四色平面圖的頂點數至多 N，則存在
`Σ(D)=932` 的 C5 disk，其內點數 `k(D)≤N−6`。
它從頂點最少的不可四色平面圖出發，在相同頂點集三角化；低度縮減和 Euler
取得五度點，刪該點後的完整 C5 關係為 932。其中「較小平面圖可染」是此
反例選取的最小性，不是待證的普遍四色定理。

**相對大小引理。** 固定 §1 的 k。每個至多 k+5 頂點的 loopless planar
multigraph J 都可四色。

證明：先簡化平行邊，不改可染性且不增加頂點。若不可四色，引理 A 給
`k(D)≤|V(J)|−6≤k−1`，且 932 不在 K。這違反 §1 在**所有**目錄外 C5
來源中的全域 k 最小性。J 本身不必是 C5 disk，也不必嵌入 G。證畢。

這個推論的頂點界不可省略：若把原 G 和外側五輪中心黏合，圖有 k+6 點，
引理 A 只給 k(D)≤k，沒有嚴格下降。故此處沒有提前排除無界 932，也沒有
循環假設四色定理。表中兩種大小須分開：

| 輔助圖／cap | 尺寸 | 合法依據 |
| --- | --- | --- |
| 原內部 C4 cap | s≤k−4 | 相對 C4 代表引理，增廣 C5 仍有 s 內點 |
| 原內部 C5 cap | s≤k−5 | 真正的較小 C5 來源，完整關係在 K |
| H 本身 | 總頂點 k，嚴格內點 k−8 | 平面圖相對大小引理；不是 C5 分類 |
| H 的單對非相鄰識別 | 總頂點 k−1 | 若不可染，932 來源至多 k−7 內點 |
| H 的外側 partition 商圖 | 總頂點 k−8+q，1≤q≤8 | 若不可染，932 來源至多 k+q−14≤k−6 內點 |
| 一般 loopless planar J | 總頂點 N≤k+5 | 若不可染，932 來源至多 N−6≤k−1 內點 |
| 原 G 加外側五輪中心 | 總頂點 k+6 | 只能得 k(D)≤k；本引理不提供矛盾 |

## 5. 同一 H 的全部共面 equality 正性

令 u,v 是 H 同面、互異且不相鄰的點。在該面加 uv 弧並收縮它。原圖沒有
uv 邊，故不會產生 loop；刪平行副本後仍平面，頂點數是 k−1。
§4 給一份完整四色染色，拉回便是同一原 H 上滿足 u=v 的完整染色。
整份染色只用同一全域色框，沒有把各 marginal 分別染色再接合。

更一般地，取 C8 上任一 noncrossing partition π，各 block 都不含相鄰
C8 點。由 induced C8，各 block 是 H 的獨立集。在 C 的外側 disk 各畫
不相交樹，連起同一 block；收縮全部樹。若 π 有 q blocks，商圖總頂點是
`(k−8)+q`。原邊只有兩端落同一 block 才會成 loop，獨立性排除了此事；
樹的輔助頂點全部隨收縮消失。所得 loopless planar quotient 滿足 §4。

將其完整染色拉回，得到同一 H 上在每個 π block 常值的完整染色。
不同 blocks 可以再同色，不能擅加它們兩兩異色。令 x_p 是 H 對固定具名
literal C8 row p 的完整延伸數，共同 S4 正規化後有

\[
\boxed{\sum_{p:\ p\text{ proper on }C,\ p\text{ constant on each }\pi\text{ block}}x_p>0.} \tag{6}
\]

不用除以 orbit size，也不指定某一特定 p 必延伸。91 份 independent
noncrossing partitions 的全部界面列由父 audit 重播，與舊 quotient 表相同；
其中真正新增的普遍接點是 §4 的精確頂點數，而非有限正性測試本身。

舊 c16-941、c32-941 的原 (a1,a4) 位置分別為 (3,7)、(1,5)，皆非相鄰。
各自 274 proper rows 中恰有 74 列令這對同色；與其必要上界 U 的交集皆空。
由 (6) 的單對版本，任一實際 H 的完整關係必含其中一列，立即矛盾。
因此這兩項為整份來源排除，並不限於舊保存的某個正向量。

父 audit 的三支 transfer／Kempe 計算排除全部 35 個 932 h=3 查詢。
结合前輪已排除该分支的 h≤2，并由同一来源的 Euler 公式，得分支特有推論

\[
\boxed{\Sigma(G)=932\Longrightarrow h\ge4,\quad n_5\ge10.} \tag{7}
\]

這不提高 933／941 的一般界；三支共同界仍是 h≥3、n5≥9。
本輪亦核對旧 933／941 的完整 upper、共同 count 修正及上述兩項 quotient，
剩餘八项與舊契約逐項相同：
`c15/c18-933` 及 `c04/c07/c15/c18/c20/c30-941`。
同一組上界的所有 91 個正性測試有非空交集只表示必要條件未排除，
不賦予任何來源圖存在性。

## 6. 下游 apex、內圈與剝層的逐步接入

本輪核讀 [apex 紙面](frozen/audits/2026-10-13-c8-apex-degree-45bc1c3/PROOF.md)、
[m9 紙面](frozen/audits/2026-10-13-c8-followup-6cafdfb/PROOF.md)、
[剝層結構](frozen/audits/2026-10-13-c8-peeling-6cafdfb/structure/PROOF.md)、
[m10 分類](frozen/audits/2026-10-13-c8-peeling-6cafdfb/calibration/PROOF.md) 及
[完整轉移](frozen/audits/2026-10-13-c8-peeling-6cafdfb/TRANSFER.md)。
它們不需要新的一般可染性引理；其繼承的兩個舊入口已由 §§2–5 修復。

**Apex。** 若某 a 的 H-degree=3，induced C8 使它只有一個嚴格內鄰 t。
固定另七點的 literal 指派，且 a 的兩個環鄰同色 c；記同一 H−a 中 t
分別為其他三色 i,j,l 的延伸數為 z_i,z_j,z_l。逐份補回 a 得
`x_i=z_j+z_l,x_j=z_i+z_l,x_l=z_i+z_j`，所以每項不超過另兩項和。
共同色框正規化須保留重複索引的重數。這是完整 lifts 計數式，空圖／空
fibre 也成立，不含可染性假設。由既有 40 份必要支援／有理分離證書排除
所有指定 apex degree3 子域後，五個 apex 全有 H-degree≥4。
其餘所用 `x=Ec` 是可帶符號的 inclusion–exclusion equality span；
`Lx=Vλ,λ≥0` 來自同一 H 的真正 Kempe component swaps，兩者不混淆。
原 Σ 接受 `01232` 提供正計數，不靠四色定理。

**原短弧。** 現在 C 上全部八點 H-degree≥4。若嚴格內點 x 同接 C 環距
二／三的兩點，短弧與兩條原邊形成內部 C4／C5 cap。由 (5) 與 C 無弦，
短弧中點 H-degree 恰三，矛盾。故每個 I 點至多接兩個 C 點，雙接只能
相鄰或正對；八條原 C 邊的面第三點 t_i 互异。若 I 全接 C，Q=H[I]
會是最低度至少三的 outerplane 圖，與低度耳點矛盾，故 m≥9。

**m=9。** 八個 t_i 加一個不接 C 的 r 耗盡 I。原三角面迫標準 C8–T8
環帶；T8 chord 的空側會有 Q-degree2 的非端點耳，因此 T8 無弦，
唯一內圖為 W8。八份原 collar 回接所得完整十列都為 1023，與 933／941
矛盾。父 audit 已重播全部 80 fibres／3,272 full lifts，採納 m≥10。

**第一剝層三型與 m=10。** 無 occupied C3 使相鄰雙接點恰為原 t_i。
所有正對雙接点必使用同一對端點，兩個正對點間由空 C4 cap 迫出 bridge，
不可能有第三個。原 links 的完整外面 walk 遂只有 RING／PINCH／BRIDGE
三型；後两型的每個 terminal disk 都必有嚴格內點，否則有非 distinguished
endpoint 的低度耳，给 m≥11 或 m≥12。於是 m=10 必為 RING；若有一個
單接 exposed 點，唯一更深中心會迫 W9，使該 exposed 點 H-degree4<5。
故原內圈 T8 有兩個更深點，完整分類為 CHORD-55、EDGE-35、EDGE-44 的
4+8+4=16 个具名位置。這是紙面完備分類，不是先截斷枚舉。

將每个候選接回全部八個原 collar，固定同一 B/C/T 名字及色框比較完整
fibres、空 cells、逐份全圖 lifts；既有 128 图均為 Σ1023。
父 audit 已重播其 1,280 外 fibres／75,936 full lifts 以及全部介面資料，
採納 m≥11，故

\[
\boxed{h=3\Longrightarrow k=8+m\ge19.} \tag{8}
\]

**一般剝層。** 完整 separator join 只把同一原圖的全部 literal 指派求和，
重複外面 occurrences 須取同一原點色值，bridge 須保留兩端異色，
空圖終端有恰一份空 lift。此機制對任意有限大小成立且無四色定理前提。
它不傳遞固定 C8、下一層 degree≥4、至多雙接或固定寬度，不能用來關閉
八項無界來源。原七項局部障礙的來源實現界線不變。

## 7. 證據與停止點

[依賴表](DEPENDENCIES.md) 區分直接紙面結論、已重播的固定有限證據與尚未
得到的來源結論。父 audit 驗證總帳保存下游固定證書本輪重播結果；
本文件沒有重跑新的來源搜尋，也没有更換舊 certificates。

所有普遍結論只在 §1 的全域最小／最大邊數來源成立。一般 k≥16 的上游
Corollary 20／plantri 及有限完整染色依賴不因本文件消失；本輪沒有新增
Lean theorem。h=3 的 932 排除不等於無界 932 排除；無界 932／933／941、
一般 `K∞=K≤5`、八項共同來源實現矛盾與固定寬度剝層仍 OPEN。
