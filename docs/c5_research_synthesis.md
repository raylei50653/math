# C₅ 全線進展與高階假設整合

**後續整理（2026-10-03）**：933／941 的固定完整 Σ、edge-minimal
C₅ disk 來源均已證 ε≥2。最新 ε=2 成果限於唯一 degree-6 root，
保留同一原分量、全部原附件、具名有序接點、實際支援及共同色框。

| 分支 | 後續完成範圍與保留界線 |
| --- | --- |
| t=1 全七分拆 | [整型來源全部排除](c5_excess_two_single_spoke_complete.md)；共同[短支援引理](c5_short_support_singleton.md)、五葉 active tree、原 binary 路徑及四接點固定末端區塊涵蓋任意大小來源 |
| t=2、(2,1,1)／四 unary | 前者的原 binary／兩 unary 省略證書保留，後由同一短支援引理六跨度排除整型；[四 unary](c5_excess_two_four_unary.md)則由固定三點支援排除整型 |
| t=2、(2,2) 與 t=3、(2,1) | [雙 binary](c5_excess_two_two_binary.md)與 [binary 省略](c5_excess_two_binary_omission.md)均已完成全部容量二省略全收，無全 degree-4 真子核心；兩份整型來源仍保留 |
| t=3 spoke＋unary 省略 | [三原 unary 共同扇區](c5_excess_two_three_unary.md)完成 path／tail，連同原 triangle 位置關閉整份條件分支 |

上述為任意大小紙面論證＋Python 固定必要域證書，未新增 Lean theorem，
未提高共同下界至 ε≥3。兩個 degree-5 roots、其他 ε=2 及一般來源、
一般出口與 K∞=K≤5 仍保留。現況與下一窄題見 [Kempe 導覽](c5_kempe_guide.md)，
本批重播與發布範圍見 [發布紀錄](history/2026-10-03-excess-progress-publish.md)。
下文保留 `b97b107` 當輪的跨線快照及實驗提案，其「未解」依後續成果閱讀。

2026-10-02，基準 `4565735`。這是跨線研究快照與實驗提案，
依當前 [HANDOFF](HANDOFF.md)、八份導覽及原報告整理。
各線即時停止點仍由各自導覽維護；本頁不改變其研究排程。

**整體判斷：目前已建立相當完整的關係語義、低超額核心結構與有限證書工具，
主要缺口集中在同一來源上多個拒絕列的相容性，以及幾何／操作能否隨關係一起保留。**
主命題 `K∞=K≤5`、一般單側／共同出口、多步充分 state 均仍未證。
下面把已完成推導、有限觀察與新假設分開。

## 1. 究竟要證什麼

指定有序 C₅ 為 disk 外框，其餘頂點私有。Σ(G) 是全部可延拓的 boundary
四色染色，僅按**共同** S4 色名置換取軌道，不先商掉框點的 D₅ 位置。
合法 C₅ 有十個 patterns，其中五個使用三色、五個使用四色（T4）。
目標

\[
K_\infty=K_{\le5}
\]

表示每個可實現的完整 Σ 都有至多五個內點的 disk 代表。
它不要求每個原圖都能靠指定的局部改寫縮小，也不要求 minimal obstruction
的原圖大小有界。後者已有無界家族；「小代表」與「小原核心」必須分開。
精確定義見[研究目標](c5_boundary_relations.md)。

目前有兩種主要工作方式：

- **來源排除／出口：** 保留同一原圖及各拒絕列的 minimal cores，利用
  degree、完整接點關係、actual supports、環序和原路徑，排除來源或證指定列延拓。
- **接合／替換／state：** 精確計算共同關係 J，判斷可用 disk 框族，
  修復投影遺失的資訊，再詢問同摘要是否足以支援後續操作。

兩者共用關係代數與幾何工具，但沒有現成定理把「修復成功」直接變成
「一般出口存在」或「主命題成立」。

## 2. 各研究線目前完成到哪裡

| 研究線 | 已有的實質結果 | 仍需處理的範圍／證據層 |
| --- | --- | --- |
| [State、grammar、枚舉](c5_state_guide.md) | k≤5 catalogue 共132個具名Σ、24個D₅軌道；固定較小grammar另有87類；關係接合及部分grammar語義已有Lean | k=6、7為reduced搜尋及獨立重現，非原邊宇宙精確窮舉；未得所有disk完備性或一般state充分性 |
| [全degree-4](c5_degree4_guide.md) | T4全收、disk minimal q-obstruction、所有有效內點完整degree=4時，Σ=Ω\{q}；任意block tree已合成到路徑／triangle正常形 | 任意大小紙面證明＋外部degree-list定理＋有限證書；完整Gallai／minor／disk鏈未Lean化 |
| [Degree-5／R系列](c5_degree5_guide.md) | 指定三-spoke來源的零／一／二奇環及部分三環位置有任意長排除；唯一degree-5全部核心另已完成指定相鄰雙列分離 | 分離不等於完整來源分類；R31同末端不同二接點的任意長來源minor、其他三環／更多環仍開放 |
| [Sector／3903、3703](c5_sector_3903_guide.md) | 指定sector的雙拒絕分類排除3903等四目標，3703三拒絕另已完成；早期交換分支被更強分類涵蓋 | 均有特定degree、disk、b0接線前提；十二列投影不等於完整Σ；603抽象profiles未因此重算 |
| [Weak-deletion／出口](c5_weak_deletion_guide.md) | 唯一degree-5、相鄰雙root唯一mixed singleton／K2、no-mixed十五類，均由來源排除或指定雙列分離接回條件式出口 | 一般單側及共同出口未證；更大／多mixed、degree≥6、多root／非相鄰root仍保留 |
| [Kempe／計數／候選來源](c5_kempe_guide.md) | 同圖換色更新、六維循環流／十二生成元；933的ε≥2；941的ε=1已收窄到t=2、3及唯一binary原分量 | 933、941一般來源未排除；分別的orbit分解不能補出同染色相容性；一般connectivity／repair策略未證 |
| [兩點重疊](c5_two_vertex_overlap_guide.md) | 六個具名接合圖、全部U上候選框、J/P差集；兩私有核心r*=4、唯一最少兩份及各15組極小repairs；多種任意大小同class來源族 | 只涵蓋具名圖與指定族；框拓撲、全部來源必要分類、一般class-pair後繼與多步摘要仍開放 |
| [Lean](lean_guide.md) | Root、BoundaryDegree及grammar／enumerator等基礎；新CommonRepair 27、SealedFourPort 22、NamedRepair 34個普通theorems | 抽象repair、D₁₃密封替換與兩具名核心已接入；來源族端到端、全部可用框、一般拓撲及外部degree-list尚未全部接通 |

表中的132與87有不同的研究域；不能把87當132的替代全集。
「唯一degree-5全部分離」與「R31來源minor仍缺」也不矛盾：前者只需要
接受指定target rows，後者要求更強的原圖結構排除。

### 2.1 最接近主命題的剩餘候選

[Kempe screen](c5_kempe_screen.md)把1,023個非空masks篩成153個；
再用外側已知cell相容性留下142個。比既有132多出的十個具名masks，
分成933及941兩個D₅軌道：T4全收，但可延拓的三色singleton位置為
單點或不相鄰兩點。若證明T4全收必有相鄰兩個可延拓singleton，
這條既有條件式路線可導向主命題。

**此screen的外側相容性使用四色定理4CT。** 本頁沿用其明示依賴，
沒有把它當4CT的無循環證明，也沒有用4CT作新搜尋oracle。
一般adjacent-singleton引理、拓撲橋接與有限分類信任仍須分開。

近期的真正橋接是[四容量子覆蓋](c5_excess_one_subcovers.md)：
把weak-deletion累積的單列minimal-core結構，搬回933／941的**同一完整Σ來源**。
不是把幾份獨立圖的lists相加。

| 固定Σ的edge-minimal disk來源 | 目前已知 | 下一個可判定小域 |
| --- | --- | --- |
| 933 | ε=Σ內點(deg−4)≥2 | ε=2的root／mixed配置；不能直接套ε=1單root論證 |
| 941 | ε≥1；ε=1時只有一個degree-5 root、一份binary分量及三份單容量因子；t=1已排除 | t=2、(2,1)，再t=3、(2)；所有十列共用原接線及省略身份 |

相鄰的**缺失**singleton兩列（出口候選A），與相鄰的**可延拓**singleton
位置（主命題候選引理）是兩個不同陳述。

## 3. 可整合成什麼共同框架

我建議以「**同源完整關係＋臨界預算＋具名幾何證書**」組織後續研究。
這是研究框架，並非已完成的一條普遍定理。

| 層 | 保留的資料 | 已經發揮的作用 |
| --- | --- | --- |
| 關係 | 同一原分量的完整有序tuples、共同色框、具名接點與完整fibres | 精確root消去、八點natural join、來源等價與投影repair |
| 臨界性 | 每個拒絕列的minimal core、原邊刪除見證、省略因子身份 | 禁色容量、D/O/κ預算、兩個core不能任意獨立選擇 |
| 幾何 | 原attachments、ownership、共同環序、原外部路徑、合法框族 | 跨度≤5、來源K5 minor、框可用性與密封替換 |
| 操作 | 允許刪哪些邊、交換哪個原分量、未來可接觸哪些點 | 決定出口與多步後繼；尚不能只從前三層的粗摘要推出 |

這解釋多條研究為何收斂到相似現象：單一邊際看起來可行，放回同圖、
同接線、同環序後才衝突。no-mixed十五類的共同式
`D+O+κ=degree−4`、樹骨架κ=0、雙root的`m+s+a≤5`，
P₃與941的六跨度排除，以及兩框各自可延拓卻無共同延拓，都屬於這種
相容性問題；但各式仍只在原證明的前提下使用。

特別值得保留的兩個方向：

1. **把任意大的圖換成有限的可觀測關係。** 輪環、雙扇、D₁₃顯示原圖形狀
   可以持續變複雜，邊界關係仍相同。有限關係分類可能比完備的局部改寫分類容易。
2. **把局部可行性提升成同源相容性。** 計數cone、pair marginals、分開的
   Kempe splits、各框的獨立延拓，均有明確資訊缺口；下一個lemma應指定
   哪一份共同見證或幾何連接使它們必須相容。

## 4. 本輪初驗：四點統一假設需要修正

先試較強說法「所有C₅來源都能由全部四點投影重建」。
新[階數報告](c5_relation_arity.md)與[完整證書](../artifacts/c5_relation_arity/observations.json)
得到：

| 最小來源投影階數 | class數 |
| ---: | ---: |
| 2 | 11 |
| 4 | 101 |
| 5 | 20 |

二十個五階類分成四個D₅軌道。已用原邊集重新核對它們的完整Σ，保存
共100份四點restriction的原圖延拓。例R511只拒絕`01232`，但這個拒絕列
的五個四點restrictions都能各自延拓。故**普遍四階來源假設已否定**。

可以保留、而且已有初等紙面證明的是：

\[
\boxed{r^*(J,P)\le d(J)\le
\max\{d(\Sigma_A),d(\Sigma_B)\}\le5,\qquad J\subseteq P.}
\]

這只要求精確兩來源接合與共用色框。另有`T4⊆Σ ⇒ d(Σ)≤4`，
已檢查全部32個T4全收的抽象masks。兩個既有私有核心來源R127／R167
也都是四階，故其接合的四階上界不用逐個來源替換族重新證。
六個原接合的實際r*仍為四個0、兩個4，與舊證書相同。

此初驗提供三個判斷：

- 未來若找接合r*=5，至少一側必出自上述二十類；可避開大部分class pairs。
- T4四階性連933／941都滿足，因此只是語義結構，不能充當disk排除。
- 同來源Σ與同接點雙射已決定J；再證同一合法框族才決定P與全部repairs。
  不需要先證所有圖都可縮回某個共同原核心。

這是本輪新做的有限初驗；其他來源排除結果以原報告為準，沒有全線重驗。

## 5. 三個可反駁的高階假設

### H1：ε=1無法承擔獨立singleton支撐

**候選陳述。** 固定Σ∈{933,941}及其D₅位置的edge-minimal disk source，
必有ε≥2。這裡minimal指刪任何非框邊都改變完整Σ，並非同一列q的minimal。

933部分已證；941只剩t=2、3。因此這個假設是把「多個單列core」的
局部理論合成「同一來源所有拒絕列」的第一個自然層級。
它仍遠弱於排除兩候選的任意ε來源。

**初步支持：** 不同拒絕列的可省略單容量因子身份不能重用；
unary的未用色D身份不能跨列交換；941 t=1的共同三葉支援已迫六跨度。
**未完成：** t=2的兩條spokes可能改變支援成本，不能照搬t=1計費。

**實驗：** 固定同一binary原分量及全部附件，先分「q₀/q₁都省略spoke」
與「一列省略unary」，核對十列關係及原省略身份。
反例必是同一具名disk source的完整Σ與刪邊見證；必要色角色表存活不算反例。
若沒有反例，第一步只要求完成t=2排除，不提前宣稱ε≥2。

### H2：no-mixed的分離機制可沿degree-5 root樹合成

**候選陳述。** M為T4全收的C₅ disk minimal q-obstruction；
所有有效內點degree為4或5，R為非空degree-5點集，M[R]為樹；
H−R每個原分量只接一個root。則M接受singleton位置與q相鄰的兩個三色列。

這精確保留no-mixed、原分量及T4前提，不包含有環root骨架、mixed、degree≥6。
若成立，在來源另有相鄰雙缺失時可用既有接合定理擴大單側出口可處理類。
它不自動提供共同出口。

**初步支持：** |R|=1由唯一degree-5結果涵蓋；|R|=2由相鄰雙root
no-mixed完成。任意root樹已有source κ=0與邊標色的緊list描述。
**真正缺口：** source邊標色不能直接搬到target，兩側root的五邊跨度證明
也不能對多root各自複製後相加。

**實驗：** 先做三root路徑，逐側保留完整半樹端點訊息及一份共同環序，
而非把三份單root禁色邊際獨立拼起來。輸出target異色接合見證或同圖
來源矛盾；有限支援未發現反例只支持這個三root域。
弱化版本可先增加「每root至多一份不能跨列搬運的原分量」前提，
但此條件在一般樹也須另證，不能沿用雙root界當作已知。

### H3：完整Σ可能決定weak-deletion的第一個可見出口

**候選陳述。** 若G、H都是指定有序C₅ disk圖，且Σ(G)=Σ(H)，
則在保留框邊及全部頂點、允許先silent刪邊再第一次strict enlargement
的語義下，W(G)=W(H)。兩圖的私有內點數可不同。

這是既有[weak quotient](c5_weak_quotient.md)觀察的普遍化，
不是本輪新證的結論。它若成立，會把多種同class來源族與出口研究直接接上；
配合逐目標的證明仍需另外確定W的內容。

**初步支持：** 封存k≤3域的87個observed relations有一致的W。
**反向壓力：** 完整Σ相等只保證外部延拓行為；刪邊會打開原先密封的內部。
非同面控制已顯示disk前提關鍵；固定Kempe摘要也已出現同state不同後繼。
後者不是H3的直接反例，但足以禁止從靜態替換定理推出H3。

**實驗：** 選既有同class的兩個小代表或一次密封替換前後，對一個指定
出口τ保存完整minimal-obstruction族／critical-edge判定。
不只比較Σ、J或repair形狀，也不以找到一條路徑代替完整W。
若失敗，保留同Σ不同W的兩張disk圖及不可達證書；轉向保留具名臨界
obstruction資料的摘要，而不是再增加未說明語義的mask位元。

## 6. 什麼值得先做，什麼可以等實驗

以下是本輪建議順序，不替換各線導覽的既定停止點。

| 優先方向 | 為何值得做 | 最小完成／停止條件 |
| --- | --- | --- |
| 941 ε=1的t=2 | 直接延伸最新同源core工具；可先驗H1的最窄分支 | 完整原關係＋共同支援的來源排除，或一份無法排除的具名必要配置 |
| mixed P₃共端點 | weak-deletion當前窄缺口，與同源幾何框架相容 | masks=(0,0,3)及反向型；保留原P₃與(3,2,1)實際附件，不能換成singleton |
| 五階來源的少量兩點接合 | 新初驗已把可能r*=5的來源縮到20類／4軌道 | 明列實際合法框族後的完整r*，或附原圖延拓的五階下界見證 |
| 三root no-mixed路徑 | 檢查雙root機制究竟能否沿樹合成 | 只報三root域，不從有限表宣稱任意root樹 |
| 同class不同實現的W比較 | 直接測H3，判斷靜態語義能否升為刪邊動態摘要 | 完整出口判定／反例，不只一條成功操作歷程 |
| Lean具名D₁₃替換接線 | 把既有局部定理接回原U上的J／指定框P，成本邊界清楚 | 端到端具名relation保持；disk框族仍另證 |

不建議立刻重啟更大k圖枚舉，或以「找到更多等價補片」作為所有來源
可化約的替代證據。若目標是repair不變，式(1)與框族證書已提供較直接接口；
若目標是K∞=K≤5，仍應追蹤933／941的同源矛盾，而非把靜態階數當幾何判準。

## 7. 本輪產物、重播與證據邊界

新增[階數推導與初驗](c5_relation_arity.md)、
[checker](../scripts/c5_relation_arity_audit.py)及
[127 KB級證書](../artifacts/c5_relation_arity/observations.json)。
只從既有132份關係、20個五階原圖、六個接合圖與其具名框證書做重播；
沒有新增class pair、拓撲普遍性或Lean theorem。

```bash
python3 scripts/c5_relation_arity_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_relation_arity_audit.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

執行結果、Lean build及未重驗範圍見[本輪紀錄](history/2026-10-02-c5-research-synthesis.md)。
全部新假設留待後續驗證；其中普遍四階來源說法已在本輪明確淘汰。
