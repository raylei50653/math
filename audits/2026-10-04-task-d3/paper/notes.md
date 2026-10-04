# D₃：C／C₂ 紙面前提與來源排除的獨立核對

2026-10-04。結論：**在原報告明列的有限、簡單、disk、同一原分量及完整 degree 前提下，C₂ §§2–5 的任意大小來源排除 PASS；未發現邏輯缺口。** C §§1–4 的完整 P₃ 化約、雙扇區及唯一框色分支也通過紙面核對。這份記錄不取代另一層獨立有限圖／完整 fibres 稽核。

本次只讀原報告、其依賴及 D₂ 整合記錄，不修改原文件、checker、artifacts 或歷史。所讀文件及外部 PDF 的 SHA256 記於 [source_metadata.json](source_metadata.json)。C₂ 文件與 observations 均與 D₂ `successor_baseline_final.json` 同 hash；C 原 observations 與 D₂ `baseline.json` 同 hash。C 的原正文與更新前綴分別保留其輪次語境。

## 1. 外部 Gallai 定理的適用前提

直接讀取 [Dvořák, List coloring and Gallai trees](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) 的 PDF 文字及第六頁影像。Lemma 7 位於 PDF 第五頁；Theorem 10 位於 PDF 第六頁。它要求連通圖及各頂點 list 大小至少為圖內 degree；若不可染，圖為 Gallai tree，lists 由 block palettes 組成，相交 blocks 的 palettes 互斥。此處沒有採用後續要求一般 critical graph 的 Corollary 11。

C₂ [§1](../../../docs/c5_mixed_p3_one_color_ternary_unary.md#1-固定同一來源與原-unary-身份) 的 D 是 H−{z,w} 的原連通 unary，三個原接點互異；外部只有 z、b₁，無 D–w、D–C* 或其他分量邊。Az={b₁} 加上無 root spoke 與唯一原 unary，給 D 的自身實際支援恰 {b₁}。因此對每點 v，p(v)=[vz∈E]、s(v)=[vb₁∈E] 都是 0／1，完整 degree 四給 d_D(v)=4−p(v)−s(v)≥2。

固定 z=0，外部色 0 與 q(b₁)=1 互異，故 M₀(v)=U∖({0:p(v)=1}∪{1:s(v)=1}) 的大小恰為 d_D(v)。0∈f_D(q) 使 D 不可 M₀-染，因此 Theorem 10 的連通 degree-assignment 前提完全符合。這是對原 D 的查詢，無需把 (0,w) 宣稱為原整圖可用 root pair；也不由固定小圖的染色結果推論任意大小。

## 2. 原 K₄ 的 tether 與 exterior connectivity

C₂ [§3](../../../docs/c5_mixed_p3_one_color_ternary_unary.md#3-原外路使-d-的-k₄-block-不可能) 保留原 zx₂、x₂b₄，所以 X=B∪{z,x₂} 原連通且與 D 不交。這是舊 connected-exterior K₄ 引理的必要補件；單用無 spoke 的 B∪{z} 不能替代 X。

若原 K₄ block K 存在，K 每點已用三條 clique 邊，完整 degree 四恰留一個方向。直接外邊只能往 z／b₁；若往 D−K，因只剩一條方向且所有 Gallai blocks 為 clique／odd cycle，该方向只能是 bridge。不同 K 頂點的外側分量互不相交，否則外側連路使 K 不再為原 block。

刪該 bridge 後，兩個連通側各沿用同一 M₀：所有點 list 大小至少為新 degree，bridge 端點多一個 list 色。有限連通图可由該 slack 頂點反向生成樹貪婪染色，兩側端點可取色集都非空。若可選不同色便能拼回不可染 D，故兩端可取色集只能是同一 singleton。若外側不碰 z／b₁，該側所有 lists 為 U，完整染色可任意 S₄ 置換，端點不可能只取一色，矛盾。

因此每個 K 頂點都有一條實際原 tether 到 X；各 tether 在 X 之前互不相交。把 X 與去除 K 端點的 tether 尾段收進同一 connected hub，K 四點維持 singleton，得到原邊 K₅ minor。共享 X 終點合法；未把互斥要求誤套到 hub 內。K₅ block 則每點內 degree 已為四，連通 D 只能等於它而無原三接點；更大 clique 直接違反 degree 四。

## 3. 葉數化約與原 triangle 等式

C₂ [§4](../../../docs/c5_mixed_p3_one_color_ternary_unary.md#4-葉-block-計數迫原圖恰是三接點-triangle) 在排除 K₄ 以上後只剩 bridges／odd cycles。若 block-cut tree 多於一個 block，有限樹有至少兩個 leaf blocks；cut nodes 的 degree 至少二，兩個葉都是真正含 private vertices 的 blocks。

leaf bridge 的 private endpoint 內 degree 一，與 d_D≥2 衝突。leaf odd cycle 至少有兩個互異 private vertices，其 d_D=2 迫 p=s=1。兩個葉的 private vertex 集互不相交，故需要至少四個原 z 接點，與 |P_D|=3 衝突。D 遂只有一個 odd-cycle block；每點都是原接點且有原 b₁ 附件，有限簡單圖的 odd cycle 最短為三，故 D 恰為三個原接點的 triangle。這是原頂點／原邊等式，沒有事先替換成 triangle gadget。

其完整有序三接點關係為 (0,2,3) 的六份排列；z=0／2／3 留下兩色 triangle palette 而拒絕，z=1 留下三色而接受。這核對全部禁色 {0,2,3}，沒有使用三個獨立 marginals。

## 4. 原 Q 與 K₅ subdivision

C₂ [§5](../../../docs/c5_mixed_p3_one_color_ternary_unary.md#5-原外路補上第十條-k₅-鄰接) 的 branch vertices 為 u₀,u₁,u₂,z,b₁。九條直接原邊來自 triangle 與三條 z／b₁ attachments；第十個 branch pair 使用 Q=z–x₂–b₄–b₃–b₂–b₁。

Q 是 simple path，四個內點互異且均不在 branch vertex 集中；其他九條路徑無內點，故十條路徑的 interiors 兩兩互斥。zx₂、x₂b₄ 與三條框邊全由原 source 前提給出。九加五共十四條原邊即可取成 subdivision 子圖；其他原 P₃／w／框邊仍存在，選 witness 子圖不等於刪去它們於原 source。等價 minor 的 Z={z,x₂,b₄,b₃,b₂} 原連通，Z 到 {b₁} 的實際 witness 是 b₂b₁。

## 5. C 的短扇區與唯一色分支

C [§1](../../../docs/c5_mixed_p3_common_endpoint.md#1-原-source-前提與完整三點關係) 的拒絕 P₃ lists 大小至少為 1／2／1。不可染恰要求兩端單色且不同、中點恰為這兩色；因第一端含未用色 3，完整 triples 才化約為 {(3,d,a),(3,d,3)}，共鄰點仍只有同一變數 x₂，F*={(a,3),(3,a)}。可用對角及非空非對角配原容量界給五個 residual 型；未額外加入 target、Σ 或 933／941 前提。

各 unary 的完整禁色非空且至多三，若無實際框附件，其禁色對 S₄ 不變只能為空或 U，矛盾。因此各 unary 皆有實際 B 支援。x₀、x₁ 的直達 B 原邊及所有 unary 的實際外接路都在原 z–x₂–w triangle 外側，遂使開內側空。

C [§3](../../../docs/c5_mixed_p3_common_endpoint.md#3-任意-unary-大小的雙扇區與-tether-引理) 的 x₀ 三-star 由 H−x₀ 連通把全部原 remainder 放進同一 I；三個互異框附件使 |I|≤3。保留 x₀x₁ 加兩條 x₁ spokes 得 rooted Y，H−{x₀,x₁} 連通又把兩整側圖與 S₂ 放進同一 J。x₁–x₂–S₂ 的 crosscut 加原 zw 邊使兩 root 同在 S₂ 一側。空 triangle 的外側 collars 與兩連通 root 側圖的互斥性使其支援在同一 linear lift 依次排列；可共享框端點，不能重用開框邊。上述紙面拓樸仍依賴原 disk 嵌入；rotation 正控制只驗證保存 skeleton 的正例。

d=2 時，d 同時在 S₀ 且被一個 pair 側見到，J 是該 unique d 端點旁 outer Y 區，兩個互異 S₁ 附件限制 |J|≤2。d–c／d–c–a／d–a–c 的逐型跨度矛盾成立。c=2 時，S₀／S₁／S₂ 共享唯一 c 點，非零 J 必為 middle Y 區，proper 字串只剩 a–d–c 或 a–d–a–c；pair／pair 與 pair／unused-singleton 都重用開框邊，所以只留 used-singleton／pair，singleton 側自身支援限首條框邊。a=2 未被此論證排盡。

## 6. 排除粒度與信任界線

C₂ 排除的鍵恰為 CPP-134-1／geometry 30／side_join_id 20，side roles (8,1)，各一份原三接點 unary、均無 spoke；f_z={0,2,3}，f_w={0,2}。C 的原 case 86 仍保留全部 25 個 side_join_ids，geometry IDs 30–35 仍六份，含 geometry 34／side_join 20；原 36 cases／140 geometries／900 role joins 沒有被 C₂ 改寫。

C₂ 報告／歷史／weak-deletion 導覽均明寫只關閉該側接合，沒有排除整個 case 或 geometry 30 的所有 side joins。本稽核沒有把同一單框點紙面引理的可能幾何後果搬成 geometry 31–33 的新增排除判定；這些身份保持原 ledger。geometry 34 的 Az={b₁,b₂} 允許非接點同碰兩框點而內 degree 二，所以這份單框點葉數計費不能直接搬去下一型。

任意有限 unary 大小的排除由 Gallai 外部定理與原 degree／bridge／leaf／disk 紙面論證承擔；保存的 pinned lists、刪邊染色、K₄ 控制及 K₅ 路徑屬固定 Python 證據。w 的完整 ternary relation 仍未知；f_w={0,2} 只保證 w=1 的完整避色 fibre 非空，九份 source projection witnesses 仍是 partial witnesses。未聲稱完整來源實現、逐邊整圖最小性、target 延拓、一般出口、K∞=K≤5 或 Lean 形式化。本次未研究 C₃ geometry 34，也未執行 lake build／全倉數學重播。

紙面 notes 的七個 local links／anchors 最終通過；首輪兩個 K₄／K₅ anchor 用了 ASCII 數字，修復紀錄保留於 source metadata。另一次全倉文件 checker 實跑通過（523 Markdown／5,414 links），未把該文件檢查當作數學或 Lean 驗證。
