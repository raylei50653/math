# C₅ class 兩點重疊研究導覽

更新：2026-10-02。研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見
[STATUS](STATUS.md)，共通規則見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

任選兩個 C₅ class，各選兩個邊界頂點，以明確雙射識別；研究重疊造成的
完整染色狀態。拓撲線判斷實際接法、側別及可施工位置；狀態線依同一
接合圖更新 relation。Class 固定具名邊界，不省略接點對應。

使用者已澄清這是**兩個 class 的兩點重疊**。不改成單一 C₅ 加邊、
整框五點接合或 C₅→C₆→C₅ 路徑黏合；不從一般大枚舉重新開始。

## 2. 項目現況

| 項目 | 現況與證據 | 入口 |
| --- | --- | --- |
| 可用 class | 既有 132 類完整 Σ／24 個 D₅ 軌道；87 類另有豐富查詢，為子集 | [資料與規格](c5_two_vertex_overlap.md) §2 |
| 兩點接口 | 1,320 份投影已保存並重播；695 強迫異色、625 自由、0 強迫同色 | [artifact](../artifacts/c5_two_vertex_overlap/pair_interfaces.json)、[checker](../scripts/c5_two_vertex_overlap.py) |
| 一次染色相容 | 在精確兩點共享、私有內部互斥、S₄ 換色不變的前提下，兩點型別交集非空 iff 可染；目前目錄全部容許異色 | [紙面推導](c5_two_vertex_overlap.md) §3–4；未新增 Lean theorem |
| 八點共同後繼 | 具名 evaluator、六份完整 relation／雙側回投影及同圖核對已完成；主例 140 軌道，完整後繼表未完成 | [八點接合](c5_two_vertex_join.md)、[artifact](../artifacts/c5_two_vertex_overlap/eight_point_joins.json) |
| 主例拓撲 | 同一八點十邊圖的 36 組環序與 24 份外面配置全核對；兩原框各自可作整圖外界，四種 disk 區域關係均有見證；未 Lean 化 | [主例拓撲稽核](c5_two_vertex_join_topology.md)、[artifact](../artifacts/c5_two_vertex_overlap/reference_topology.json) |
| 私有內點原框 | 指定十五點三十五邊圖平面，兩來源各在自己的 disk 內且內部互斥；兩組原路徑排除 A、B 作整圖外界，完整 J 仍 60 軌道；未 Lean 化 | [私有內點拓撲](c5_two_vertex_private_topology.md)、[artifact](../artifacts/c5_two_vertex_overlap/private_topology.json) |
| 反向私有內點原框 | 反向指定圖亦平面、來源 disk 可內部互斥、兩原框皆被交錯原路徑阻斷；完整 J 與正向各有 16 個獨有 patterns；保存一個混合 C₅ 外面，未 Lean 化 | [反向拓撲](c5_two_vertex_private_reverse_topology.md)、[artifact](../artifacts/c5_two_vertex_overlap/private_reverse_topology.json) |
| 反向混合外框 relation | `(a0,a4,a3,a2,b2)` 的完整 R255／8 軌道／192 賦色及全部原 J 纖維已核對；等於既有單內點 disk 代表，替換須密封其餘點，未 Lean 化 | [混合框報告](c5_two_vertex_mixed_frame.md)、[artifact](../artifacts/c5_two_vertex_overlap/mixed_frame_relation.json) |
| 反向第二混合外框 relation | `(a0,b4,b0,a2,a1)` 的完整 R1022／9 軌道／216 賦色及原 J 纖維全核對；等於既有雙內點 disk 代表，與 R255 非 D₅ 等價；替換須密封其餘點，未 Lean 化 | [第二混合框](c5_two_vertex_second_mixed_frame.md)、[artifact](../artifacts/c5_two_vertex_overlap/second_mixed_frame_relation.json) |
| 兩混合框共同拉回 | 完整拉回為 114 軌道，較原 J 多 54；補回 b2–b4 仍多 16，加入兩條四點條件恰還原 J；完整差集、分別延拓及原邊拒絕全保存，未 Lean 化 | [拉回與修復](c5_two_vertex_mixed_pullback.md)、[artifact](../artifacts/c5_two_vertex_overlap/mixed_frame_pullback.json) |
| 全部三點投影與四點下界 | 56 份三點投影各等於誘導原邊關係；加到兩框後仍多 16 軌道／384 賦色，保存 896 份三點延拓；原 U 無輔助變數的局部合取修復所需最大 arity 恰為四，未 Lean 化 | [三點投影報告](c5_two_vertex_ternary_projections.md)、[artifact](../artifacts/c5_two_vertex_overlap/ternary_projections.json) |
| 四點投影最少個數與全部最小組合 | 70 scopes／八種排除集合及 2,415 配對全核對；最少兩份，唯一組合為 `(a0,a1,a2,a3)` 與 `(a2,b0,b2,b4)`；三份唯一性見證／192 份原圖延拓保存，未 Lean 化 | [最小修復報告](c5_two_vertex_quaternary_repairs.md)、[artifact](../artifacts/c5_two_vertex_overlap/quaternary_repairs.json) |
| 全部 inclusion-minimal 四點修復 | 固定 P、原 U 的全部十五組分類完成：一組二份、十四組三份；三個完整排除類組合、44 份不可省見證與逐組完整 relation 相等核對保存，未 Lean 化 | [全部極小修復](c5_two_vertex_minimal_repairs.md)、[artifact](../artifacts/c5_two_vertex_overlap/minimal_repairs.json) |
| 六例 local-repair transport | 全部二十條 U 上五環中十四條可作整圖外界；四例 P=J、r*=0，正反向私有內點例 r*=4、各十五組極小修復；八十八份不可省見證，repair 公式相同但完整具名排除資料不由頂點雙射搬運，未 Lean 化 | [跨例報告](c5_two_vertex_repair_transport.md)、[artifact](../artifacts/c5_two_vertex_overlap/repair_transport.json) |
| 共同 repair lemma | 三種完整 rejector witness 與兩類覆蓋等式充要刻畫全部極小修復；三個極大失敗集合及五條前提獨立性已證，六圖前提重播通過，四例 P=J 保留為退化支；紙面＋Python，未 Lean 化 | [共同 lemma](c5_two_vertex_common_repair.md)、[artifact](../artifacts/c5_two_vertex_overlap/common_repair.json) |
| Repair 來源充分條件 | 具名私有核心的色數證明及每例十一份構造補全推出 W／C；保核心的度數三消去及外框證書推到任意大小指定族，r*=4；兩原框可用給獨立退化 lemma；後續已證消去條件非必要，全部代表未分類，未 Lean 化 | [來源定理](c5_two_vertex_repair_sources.md)、[artifact](../artifacts/c5_two_vertex_overlap/repair_sources.json) |
| 不能逐點消去的密封補片 | 完整 clique 附件＋一份染色可延拓全部核心染色；原來源三角剖分使保核心 disk 擴張自動具此附件；任意大小度數五補片族與六個21／33／51點控制保持十五組 repairs、r*=4，證明舊消去條件非必要，未 Lean 化 | [補片定理](c5_two_vertex_repair_patches.md)、[artifact](../artifacts/c5_two_vertex_overlap/repair_patches.json) |
| 不含舊核心的同 class 路徑族 | 完整接線族中 A 兩臂偶長、B 奇長充要保持 R127／R167；加長後無保持框點及 ownership 的舊核心副本，私有最低度數四，仍保十五組 repairs／r*=4；十圖14,400份延拓、八奇偶控制，紙面＋Python，未 Lean 化 | [奇偶定理](c5_two_vertex_repair_strips.md)、[artifact](../artifacts/c5_two_vertex_overlap/repair_strips.json) |
| 舊補片／路徑之外的輪環骨架 | 四輪星與四環帶加中心的完整四接點關係相等；任意層數同 class 族無密封 clique 補片、私有圖含環且無舊核心副本，保十五組 repairs／r*=4；八圖11,520份延拓，必要分類仍未完成，未 Lean 化 | [輪環定理](c5_two_vertex_repair_rings.md)、[artifact](../artifacts/c5_two_vertex_overlap/repair_rings.json) |
| 輪環逆化約之外的偶長雙扇 | 四輪星與偶長雙扇的完整四接點 relation 相等；任意大小同 class 族無密封 clique 補片、私有圖含環且無私有度數五點，三種舊縮減皆無起點；保十五組 repairs／r*=4，八圖11,520份延拓，未 Lean 化 | [雙扇定理](c5_two_vertex_repair_fans.md)、[artifact](../artifacts/c5_two_vertex_overlap/repair_fans.json) |
| 輪環及雙扇之外的非對稱 disk | 十三點 D₁₃ 與四輪星完整四接點等價；反覆替換給任意大小同 class 族，私有四度點只成孤點及配對，輪環與雙扇均無起點；完整 J/P、十五組 repairs／r*=4 保留，未 Lean 化 | [D₁₃ 定理](c5_two_vertex_repair_caps.md)、[artifact](../artifacts/c5_two_vertex_overlap/repair_caps.json) |
| 一般拓撲與多步 | 其餘代表、指定接合政策及未來接觸範圍須另查；尚無一般充分摘要 | [拓撲界線](c5_two_vertex_overlap.md) §5 |

## 3. 精確停止點與下一個窄問題

目前最前沿是[十三點非對稱四接點 disk D₁₃](c5_two_vertex_repair_caps.md)：
它與四輪星的具名四接點 relation 相等，可接回任意外部上下文。
反覆替換得到任意大小的 R127／R167 disk 來源，無密封 clique 補片、
兩側私有圖含環；私有四度點只成孤點及配對，每點至多鄰接一個私有
五度點，因此輪環及偶長雙扇均無縮減起點。新 D₁₃ 規則可處理這一族，
保留完整 J/P、全部可用框、十五組 repairs 及 r*=4。
加入 D₁₃ 後的其他骨架、統一結構條件與全部代表必要分類仍未完成。
其依據為[共同 repair 充要 lemma](c5_two_vertex_common_repair.md)及
[六例 transport audit](c5_two_vertex_repair_transport.md)。下表保留原六圖的完整基準。
可用 frame 統一定義為原 U 上、可作整張接合圖 disk 外界的全部 C₅；
二十條候選逐條有證書，十四條可用、六條由原交錯路徑阻斷。
正向私有內點例新增同一原圖的 rotation，補齊其兩條混合五框。

| 固定案例 | J／P／Δ 軌道 | r=0,…,4 的殘留 | r* | 全部極小 repairs |
| --- | --- | --- | ---: | --- |
| reference、reference_reverse、shared_chord_frame_edge | 140／140／0 | 0,0,0,0,0 | 0 | 唯一空集合 |
| free_pairs | 152／152／0 | 0,0,0,0,0 | 0 | 唯一空集合 |
| private_interiors、private_interiors_reverse | 60／114／54 | 54,54,16,16,0 | 4 | 一組二份、十四組三份 |

全部 r=0,…,8 已算；後四階殘留均為零。非平凡兩例均以 P 單獨為基底，
原 `U=(a0,a1,a2,a3,a4,b0,b2,b4)`、共同色框及所有原內點／原邊不變：

```text
A = (a0,a1,a2,a3), 唯一 forced scope
T = (a0,a2,b0,b2)
B_forward = (a0,b0,b2,b4)
B_reverse = (a2,b0,b2,b4)
E_family = 所有含 {b2,b4} 的四點 scopes，排除該例 B
全部極小 repairs = {A,B} 以及 {A,T,E}（十四個 E）
```

每例七十 scopes 按完整排除集合成八類，全部類子集合與具名展開已核對；
兩例共八十八份逐項不可省見證及各階下界延拓保存。四個空 repair 加
三十個非空 repair 都逐一掃全部 `4^8`，直接查詢關係並與 J 作集合相等比較。
兩例只有兩個八點雙射能搬運 repair 家族，均不能搬運完整 J、P 或排除資料。
不能把共同公式當成原圖或完整關係同型。

**抽象 lemma 已完成。** 在 J⊆P 及每個候選條件保留 J 下，三種 exact
rejector witnesses `{A}`、`{B,T}`、`{B}∪𝓔`，加上 `F_A∪F_B=Δ` 與
每個 E 的 `F_A∪F_T∪F_E=Δ`，充要刻畫全部 repairs 為上述模板的上閉包。
反向由三個極大失敗集合導出 witnesses；每例三個 witnesses 即可統一
證明44次刪除不可省。新證書重驗六圖、六個 witness、30份覆蓋等式及
384份接受 scope 原圖延拓，另有五個前提獨立性控制。
四例 P=J 使用獨立退化 lemma，唯一極小 repair 為空集合。

**來源充分條件已推進。** A 的五內點路徑及 B 的兩相鄰內點，保留完整附件，
以可用色構造證明精確來源 relation；每例十一份補全給全部 scopes 的三種
exact rejectors，色數論證給兩類覆蓋。指定 induced 核心、密封私有點的
度數至多三消去、來源 ownership 及兩混合框 rotation，保證任意有限大小
G 的完整 J/P 與核心相同，因而保留十五組極小 repairs；W_A 另直接給 r*=4。
兩原框皆可用時，任意大小的精確兩來源分解給 P=J，仍獨立保留空 repair。
新證書核對原六圖、兩個二十一點增大控制、5,760份構造延拓及十二項負控制。

**不能逐點消去的來源已推進。** G−H 的完整分量若只接核心的至多三點
clique，一份全圖染色可逐分量換色對齊同一份核心染色，保持全部具名核心。
原 A／B 核心的十三／七個內面皆為三角形，因此保核心的來源 disk 擴張
自動滿足此附件條件。配合保框 rotations，全部十五組 repairs 及 r*=4 保留。
八面體／二十面體及巢狀補片給兩方向各21、33、51點控制；新增點最低度數
四或五，任何保核心度數三消去都無法開始。8,640份構造延拓、66份稀疏補全、
完整 J/P、十二項負控制及兩個附件反例均通過。任意大小來自施工及紙面引理。

**不含舊核心的來源已推進。** 兩來源的整條私有路徑保留全部實際附件，
雙 hub 異色時的二色交替及同色時的三色延拓，給任意長度精確公式。
加長圖的原框端點附件與私有距離排除任何保持框點及 ownership 的舊核心
子圖副本；私有最低度數四，度數三消去亦無起點。整圖 rotations 可在兩個
相鄰三角面內延伸，三個不可用框的交錯路徑則沿 subdivision 保留，故全部
可用框恰為原兩框。十個17／21／29點控制、14,400份構造延拓、110份稀疏
補全、八種奇偶、十二項結構負控制及一個固定四接點反例均核對。

**舊補片／路徑之外的骨架已推進。** 在原 A 的 h5 或 B 的 v 作輪環
替換，任意有限層數保持完整四接點及來源 relation。每個來源三角形仍為
面；刪至多三點 clique 後各分量皆含框點，故無密封私有補片可先刪。
私有三角形阻止套用整來源路徑前提，框點的私有共鄰數則排除舊核心
單射。八個19／23／35點圖的全部可用框、完整關係、11,520份構造延拓、
88份稀疏補全及十二項結構負控制均核對。局部四接點等價不保留中心色。

**輪環逆化約後的骨架已推進。** 偶長雙扇完整四接點關係等於四輪星；
奇長則交換 `0121`／`0123` 的接受狀態，關係大小相同仍不等價。
在 A 的 h5、B 的 v 選用指定私有 hub 替換，兩側擴張後的私有度數
只有四或至少六，既有輪環所需四個密封度數五點不存在；加上所有
三角形皆為面及私有三角形，三種舊縮減規則都無起點。新雙扇逆化約
可帶回原骨架。八個17／19／25點控制、11,520份完整延拓、88份稀疏
補全、六種局部長度及十四項結構負控制通過；中心色仍須密封。

**輪環及雙扇化約後的骨架已推進。** D₁₃ 的四色框由原邊迫出內點
四色鄰域而拒絕，其餘三型有明列完整延拓。反覆在指定四度中心替換，
私有四度誘導圖始終只含孤點及單邊，且每點至多鄰接一個私有五度點，
故兩種局部逆化約都無第一步。全部外框由面替換及原 spoke subdivision
另行保留。八個23／31／47點圖、11,520份延拓、88份稀疏補全及十六項
結構負控制保存；任意大小結論為紙面證明，未證改寫完備性。

**下一個窄問題：加入 D₁₃ 化約後的局部四接點實現或統一結構條件。**
密封 clique 補片、整來源奇偶路徑、輪環、偶長雙扇及 D₁₃ 都是充分
規則；其餘不可化約來源及可統一這些實現的條件仍待處理。須保留
實際附件、ownership、共同色框及全部可用框；未證全部代表可如此
化約、正常形唯一性，亦未比較容許先擴張再縮減的任意改寫序列。
舊度數三條件及「含原核心＋補片」條件皆已確定不是必要條件。
僅完整 J 相等仍須另查可用框；不由共同公式或原圖反向推論 transport。
本輪未搜尋新 class pair，未新增 Lean theorem。

六圖的 U 上五框可用性已窮盡，但未分類其所有嵌入、指定來源 disk
重疊政策或允許未來接觸的範圍。一般 class-pair 後繼表、局部條件表／
輔助變數模型、多步摘要充分性、完整 Σ 及 `K∞=K≤5` 均保留。
五點 relation 替換仍須密封其餘點，不能拼接分別存在的框延拓。

## 4. 閱讀與重播入口

先讀[資料與規格](c5_two_vertex_overlap.md)、[八點接合報告](c5_two_vertex_join.md)、
[主例拓撲稽核](c5_two_vertex_join_topology.md)與
[私有內點拓撲](c5_two_vertex_private_topology.md)，再讀
[反向拓撲](c5_two_vertex_private_reverse_topology.md)與
[第一混合框](c5_two_vertex_mixed_frame.md)、
[第二混合框](c5_two_vertex_second_mixed_frame.md)、
[兩框共同拉回](c5_two_vertex_mixed_pullback.md)與
[全部三點投影](c5_two_vertex_ternary_projections.md)、
[四點最小修復](c5_two_vertex_quaternary_repairs.md)與
[全部極小修復](c5_two_vertex_minimal_repairs.md)與
[六例 transport audit](c5_two_vertex_repair_transport.md)與
[共同 repair lemma](c5_two_vertex_common_repair.md)及
[來源充分條件](c5_two_vertex_repair_sources.md)及
[密封補片定理](c5_two_vertex_repair_patches.md)及
[私有路徑奇偶定理](c5_two_vertex_repair_strips.md)及
[完整四接點輪環替換](c5_two_vertex_repair_rings.md)及
[完整四接點偶長雙扇替換](c5_two_vertex_repair_fans.md)及
[十三點非對稱四接點 disk](c5_two_vertex_repair_caps.md)；最新發布核對見
[共同 repair 與來源替換族發布紀錄](history/2026-10-02-c5-two-vertex-repair-publish.md)，
D₁₃ 當輪驗證見[研究紀錄](history/2026-09-30-c5-two-vertex-repair-caps.md)，
較早發布見[發布整理與驗證紀錄](history/2026-09-30-c5-two-vertex-publish.md)。再視需要讀
[state language](state_language.md)、[local closure](local_closure.md)、
[cell enumerator](c5_cell_enumerator.md)及[既有 state 導覽](c5_state_guide.md)。

三點與四點證書超過 1 MB，依 [README 大型 artifacts 規則](../README.md#python-產生器與大型-artifacts)
只在 Git 保存生成器及 [manifest](../artifacts/MANIFEST.json)。新 clone 若尚未
重建，先依序執行下列兩個生成器；其餘本線證書直接隨 Git 保存。

```bash
python3 scripts/c5_two_vertex_ternary_projections.py
python3 scripts/c5_two_vertex_quaternary_repairs.py
python3 tools/artifacts.py status
```

以下為只讀重播；`--check` 會重算並逐 byte 比對既存證書：

```bash
git status --short --branch
python3 scripts/c5_two_vertex_repair_fans.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_fans.py --check
python3 scripts/c5_two_vertex_repair_caps.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_caps.py --check
python3 scripts/c5_two_vertex_repair_rings.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_rings.py --check
python3 scripts/c5_two_vertex_repair_strips.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_strips.py --check
python3 scripts/c5_two_vertex_repair_patches.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_patches.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_transport.py --check
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_join_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_join_topology.py --check
python3 scripts/c5_two_vertex_private_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_topology.py --check
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_second_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_second_mixed_frame.py --check
python3 scripts/c5_two_vertex_mixed_pullback.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_pullback.py --check
python3 scripts/c5_two_vertex_ternary_projections.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_ternary_projections.py --check
python3 scripts/c5_two_vertex_quaternary_repairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_quaternary_repairs.py --check
python3 scripts/c5_two_vertex_minimal_repairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_minimal_repairs.py --check
```

點對重播只依現有來源 JSON；八點重播另驗四份來源代表與六份接合圖的
完整染色。主例拓撲 checker 遍歷該圖環序／外面；正反向私有內點 checker
各核對一份平面見證、兩份對所有嵌入有效的原框阻斷及完整染色；
反向 checker 另直接重播正反向原圖的完整 J 差集。兩個混合框 checker
各驗完整纖維、原圖十內點延拓及單／雙內點代表；第二框另驗 D₅
位置作用與三項 verifier 擾動。拉回 checker 重建原 J、完整拉回與差集，
核對全部拒絕證明、分別延拓、八份條件子集合及五項 verifier 擾動。
三點 checker 重建同一 J，核對全部 56 份投影、16 份殘留軌道的
896 份三點延拓及其 21,504 份具名換色、兩份四點修復與六項 verifier 擾動。
四點 checker 重建同一 J，核對 70 份完整投影、全部 2,415 配對剩餘集合、
三份唯一性見證的 192 份延拓／4,608 份具名換色及九項 verifier 擾動。
極小修復 checker 沿用並重驗上述投影／三份見證，枚舉八類完整排除集、
展開十五組具名修復、逐份核對 44 份刪除殘留及見證，並對每組掃描
完整 `4^8` 賦色域；另有九項負控制。
本輪實際重播範圍見紀錄。
六例 transport checker 另逐條驗全部候選五框、重建六份 J/P/Δ、
計算完整 arity ladder 與全部極小 repairs；各種區域配置與來源大枚舉未重驗。
共同 lemma checker 從同一原圖重建 J/P，先核對完整 witness／覆蓋前提，
再比較既有修復分類，保存三個極大失敗集合與完整殘留；不新增圖論普遍性結論。
來源 checker 獨立驗核心原邊、來源 ownership、消去次序與完整 rotations，
再比較構造公式、原圖完整染色及稀疏補全；任意大小推論由紙面歸納負責。
補片 checker 自行抽取完整密封分量及 clique 附件，核對一份染色與 rotations；
再以原邊回溯六個不能逐點消去的增大圖，重建 J/P、全部 repairs 及完整補全。
奇偶 checker 從原邊抽取兩條完整私有路徑，獨立核對來源、全部 J/P 及 repairs，
另以保持框點的子圖搜尋排除舊核心；有限控制不取代任意長度的紙面證明。
輪環 checker 另驗完整四接點等價，逆序核對所有局部附件，窮盡 clique 切口
及其完整分量；新任意層數結論仍由紙面證明負責，不是必要分類。
雙扇 checker 核對偶／奇長的完整四接點關係，從全部實際鄰域逆序核對
新規則；另列私有度數，獨立阻斷既有輪環逆化約，驗完整外框及 repairs。
任意大小與三種舊縮減無起點的結論由紙面證明負責，未證改寫完備性。
D₁₃ checker 另核對完整九內點附件、局部面表及三行延拓，從最終圖
的私有度數／誘導邊獨立排除輪環與雙扇，保存真正輪環及雙扇的正控制；
仍由紙面歸納負責任意層數，不宣稱最小反例或全部代表分類。
不得以 1,320 份點對表取代完整 Σ；不得把 `geometry=unknown` 當 disk transition。
