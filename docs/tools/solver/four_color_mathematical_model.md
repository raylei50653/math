# 著色程式的完整解空間與接口語義

2026-10-26。接續[精確消元的完備性紙證](four_color_completeness.md)、
[按需完整接口](four_color_local_information.md#2026-10-26按需查詢局部接口)及
[全部回填選項的保留](four_color_retention.md)。目前接續入口見[四色導覽](../four_color_guide.md)。

本頁將程式使用的關係、fibres 與按需答覆接到同一個完整解空間，並將其中的
投影、解分解與有限次消元寫成[Lean 核心](../../../Math/ColoringElimination.lean)。
全程保留同一原圖、原點身份、字面色框與完整接口。這裡的新增結果是精確語義及核心形式化；
有限終止與資源限制仍依原紙證，Python 與此模型的逐步對應尚未形式化。

## 原問題是一份共同指派

設有限簡單無向圖為 `G=(V,E)`，`C={0,1,2,3}`。每點有效域 `D_v⊆C` 已納入固定色：
未固定時為 `C`，固定為 `a` 時為 `{a}`；一般候選域也可直接與之相交。
定義完整指派的合法性

\[
K_G(c)\ \Longleftrightarrow\
\bigl(\forall v\in V,\ c(v)\in D_v\bigr)
\ \land\ \bigl(\forall uv\in E,\ c(u)\ne c(v)\bigr),
\qquad c\in C^V.
\]

`Sol(G,D)={c:K_G(c)}` 是求解器要保留的對象。傳播保留全部解，意指這個集合逐份相等，
不只是傳播前後恰好都非空；固定色無延伸則是指定 `D` 下此集合為空。
不要求平面性。`V=∅` 時只有空指派 `ε`，空圖有一份解。

若 `V=X⊔Y`，用 `a⊕b` 表示將 `X` 指派與 `Y` 指派按原點身份合併。定義

\[
F_X(b)=\{a\in C^X:K_G(a\oplus b)\},\qquad
R_X=\{b\in C^Y:F_X(b)\ne\varnothing\}.
\]

`R_X` 是完整剩餘關係，`F_X(b)` 是該**同一份**剩餘指派的完整 fibre。
若要把 `Y` 再縮成較小接口，必須另證所有私有點的外接約束都經過該接口。
僅憑一批 `source_edges` 不能忽略當時的域或外側派生限制。

## 解分解定理：每份完整解恰好是一份接口與其 fibre 成員

對任何完整關係 `K`，不只著色關係，都有一一對應

\[
\boxed{\operatorname{Sol}(K)\ \cong\
\coprod_{b\in C^Y}F_X(b).}
\]

正向將完整解限制到 `Y` 與 `X`；反向合併同一 `b` 與它的 fibre 成員。
分拆再合併逐原點恢復原色，合併再分拆也不變，故兩映射互逆。
空 fibre 貢獻零份解；不同接口列的 fibre 互不混接。
這比「有解當且僅當投影非空」多保存了每份解的身份。

若單步消元前的約束寫成 `Q(b)∧B(a,b)`，其中 `Q` 完全不依賴 `X`，則

\[
\exists a\,[Q(b)\land B(a,b)]
\quad\Longleftrightarrow\quad
Q(b)\land\exists a\,B(a,b).
\]

因此可用 `R(b)⇔∃a B(a,b)` 替換整個 bucket，並保存
`W(b)={a:B(a,b)}`。不能把含被消去點的原因子留在 `Q`，也不能給不同 bucket 因子
各選不同的 `a`。逐點消元的 `X` 是單點，`W(b)` 因而至多四色；4-bit 表示恰好無損。

## 一次完整消元紀錄如何編碼全部解

固定一次完成的執行，消元順序為 `x₁,…,xₙ`。第 `i` 步的歷史完整接口為
`Y_i⊆{x_{i+1},…,xₙ}`，全部支援色為 `W_i(y)`。
各步之間可有保留全部解的傳播；保存後的歷史 `W_i` 不再改寫。
將 `W_i` 視為 `C^{Y_i}` 上的總映射：未列入已保存完整表的接口列，包括當時域外的列，
一律取空集合。此約定只是將已禁止的指派補成明確的空支援。
令 `τ` 表示最後全部零元因子皆為真。則對每份原圖完整指派 `c`，

\[
\boxed{K_G(c)\quad\Longleftrightarrow\quad
\tau\ \land\ \bigwedge_{i=1}^{n}
\bigl[c(x_i)\in W_i(c|_{Y_i})\bigr].}
\]

證明在單步使用更強的等式：`s` 是消元前的解，恰好當 `s` 的剩餘限制是
消元後的解，且被消去色落在該限制的 `W_i` 中。可靠傳播不變更剩餘解集合；
由 `i=1` 反覆代入到最後的唯一空指派，就得到上式。
反方向沿 `i=n,…,1` 接回同一剩餘指派，也逐步恢復全部原約束。

這個只含歷史與 `τ` 的公式適用於完整且正確保存的整次消元紀錄。中途判否或 `limit`
的部分紀錄單獨一般不足以編碼全部解；`τ=false` 也不能省略。現行程式在空接口取得非空
支援時可立即卸下零元真因子，空支援則立即判否，與此語義一致。

2026-10-27補充：[部分歷史原型](four_color_partial_history.md)保留剩餘問題 `P_k` 後，
將 `τ` 換成 `c|U_k∈Sol(P_k)`，合取只取已完成的前 `k` 步，即可精確表示全部原解。
歷史 fibre 也可用當時 bucket 因子的重算規則表示，不必存展開表；缺失且無法重建
的限制仍不可省略。這是附有剩餘狀態的新原型，未改稱主求解器的部分輸出已具此契約。

求一解只需先確認 `τ`，再依已確定的**整列** `c|Y_i` 任取一個 `W_i` 成員。
非固定色即使已只剩一個選項，也可一直等到這個倒序階段才寫入。
保存每列一個支援足以求一解；保存全部支援才具有上述全部解的編碼保證。

### 計數必須沿共同接口求和

由解分解定理，有限時有

\[
|\operatorname{Sol}(K)|=\sum_{b\in C^Y}|F_X(b)|.
\]

對完整逐點紀錄也可沿倒序的相容支援作巢狀求和；每條完整回填分支計一次。
不可以將任選一條成功分支上遇到的 `|W_i|` 直接相乘，因為不同後綴的支援數可能不同。

例如原邊只有 `xy,xz`，先消去中心 `x`，則

```text
W_x(y,z) = C \ {y,z}；W_y(z) = C；W_z(ε) = C。
```

`y=z` 有4列、每列3個 `x` 色；`y≠z` 有12列、每列2個，故原圖恰有
`4×3+12×2=36` 份染色。沿 `y=z` 的分支相乘會得48，沿 `y≠z` 則得32。
此例也說明邊界表列數、一次回填的選項數與完整染色數是不同量。
本輪只補這項數學語義，未將主程式改成計數器或均勻抽樣器。

## 完整表與按需查詢的共同物件

取同一份有效域與原因子分配，以及一份已核對的根袋樹或袋森林。要求每個原因子
scope 完整落在所屬袋中、每份原因子分配恰一次、所有原點皆被覆蓋，且同一原點
所在的袋形成連通子樹。不同根的原點集合互不相交。
填補邊僅建立分解，不增加異色限制。

對袋 `t`，令 `V_t` 是其整棵子樹的原點聯集，`S_t` 是與父袋的完整有序交集，
`A_t` 是整棵子樹分配的全部原因子。定義

\[
R_t=\{\sigma\in C^{S_t}:\exists c\in C^{V_t},\
c|_{S_t}=\sigma,\ c\text{ 滿足 }A_t\text{ 及全部有效域}\}.
\]

根接口為空。若 `L_t(b)` 表示袋列 `b` 滿足本袋原因子及有效域，則

\[
\boxed{\sigma\in R_t\quad\Longleftrightarrow\quad
\exists b\in C^{B_t}:\
b|_{S_t}=\sigma\ \land\ L_t(b)\ \land\
\bigwedge_{u\text{ 為 }t\text{ 的孩子}} b|_{S_u}\in R_u.}
\]

正向限制同一份子樹解即可。反向對同一 `b` 取得各孩子的完整子樹見證；
袋連通性保證孩子私有點互不重疊，任何共同原點都已經過袋 `t` 的相應接口。
故各見證在交集上同色，可以合併；原因子覆蓋保證沒有未核對的跨區約束。

這給出兩種求值方式的精確等價：自底向上建立完整 `R_t`，與逐列完成布林詢問
`Q_t(σ)`，都計算同一個 `σ∈R_t`。各根的 `Q_t(ε)` 皆真，恰好當整圖有解。
已完成快取只是 `1_{R_t}` 的部分查詢；未查 key 不代表空 fibre，也不代表可以延伸。
肯定答覆保存一個相容見證即可回填一解，否定答覆則須窮盡該列全部候選。

**逐表等同的前提。** 此比較固定同一因子分配及有效域；不能直接把現行
`solve_constraints` 每份中間表都叫作上述靜態 `R_t`。主引擎可能已收到外側的域收縮
或派生因子，且消元順序也可能不同。若要逐表比較，須停用這些上下文改變，或將
當時的 `source_domains`、`input_relations` 全部放進待比較的問題。
兩種精確程序的最終有解／無解語義仍以同一份 `K_G` 為準。

## 完整接口失去支援的增量形式

2026-10-27新增[支援流失傳播](four_color_support_loss.md)。上次完成半連接後設
`π_I(L)=π_I(R)=S`，其後只刪列成 `L′⊆L`、`R′⊆R`。定義
`Δ_L=S∖π_I(L′)`、`Δ_R=S∖π_I(R′)`，則新共同支援精確為
`S′=S∖(Δ_L∪Δ_R)`。左側只刪接口落在`Δ_R`的完整列，右側對稱，
恰好等於重新做完整半連接；全部私有座標及全域共同解保留。
這裡的差量是「最後支援消失」，不是被刪列的投影。

支援差量與對側刪列等價式已另增Lean核心。Python原型保留完成訊息，
仍以當前完整投影發現差量，未持續維護支援重數。同40例完整輸出與delta相等，
但原排程接口檢查增加2.25%，資訊分區增加2.14%；語義改寫不代表效率一定改善。

## Lean 核心、來源對照與驗證邊界

命名空間為 `ColoringElimination`；一般關係與 fibres 使用同一顏色型別，
`FourColoring` 另特化成 `Fin 4` 的原邊及部分固定色模型。

| 數學義務 | Lean 宣告 | 與程式的對照 |
| --- | --- | --- |
| 完整投影恰好保留非空 fibre | `eliminate_iff_nonempty_fibre` | 缺列代表指定域乘積內的空 fibre |
| 完整解與接口／完整 fibre 一一對應 | `solutionEquiv`、`join_restrict` | 同一字面接口的分拆與合併 |
| 固定接口下回寫支援可恢復解 | `reconstruct` | 歷史 witness map 的完整列查詢 |
| 有解存在性與投影存在性相同 | `satisfiable_iff_eliminate` | 消元不改可滿足性 |
| bucket 與其餘因子共用同一剩餘指派 | `eliminate_bucket_iff` | 合併全部含消去點的因子 |
| 全解相等的傳播可安全接續投影 | `eliminate_congr` | 各傳播規則仍須另證其前提 |
| `Fin n` 上任意有限次精確消元 | `reduceAll_iff_exists` | 固定座標次序的關係語義 |
| 全部原邊與固定色的四色特化 | `reduceAll_fourColoring_iff` | 同時滿足全部原約束的一份解 |
| 完整接口支援隨刪列單調縮小 | `interfaceSupport_mono` | 支援必須來自同一完整列 |
| 新共同支援等於扣掉兩側流失支援 | `common_support_after_losses` | 上次完成的共同S與兩側最新投影 |
| 依對側流失支援刪列等同完整半連接 | `semijoin_by_lost_support` | 原列私有座標完整保留；Python快取另核對 |

`reduceAll` 是命題值語義，沒有執行有限列舉、證明 Python 終止或處理工作預算。
任意有限原點可經雙射編成 `Fin n`；這項編碼與動態 min-fill 排程的實作對應尚未
在此檔形式化。本頁多步歷史 fibres 的合取式與袋樹接合式仍為紙證，沒有把它們
冒稱已由 `reduceAll_iff_exists` 逐行驗證。

實作入口為 [`four_color_constraints.py`](../../../scripts/four_color_constraints.py) 的
bucket／witness map，與 [`four_color_local_messages.py`](../../../scripts/four_color_local_messages.py)
的分解核對、完整接口詢問及最後回填。子樹共同換色快取另外遵循
[保域群與逆換色契約](four_color_local_symmetry.md)，不准各表獨立改色框。

本輪另以[獨立原邊重播](../../../audits/2026-10-26-four-color-mathematical-model-8d28acc/replay.py)
核對7張具名小圖、兩種bucket枚舉及子構造開／關，共28份完整消元紀錄；
21,844份完整指派的原邊／固定色判定與歷史fibres合取逐份相等。
空圖、孤點、固定外側限制均涵蓋；另三份無解或超限紀錄明確拒絕套用完整合取式，
中心先消的36／48／32計數控制也獨立核對。
[保存報告](../../../audits/2026-10-26-four-color-mathematical-model-8d28acc/report.json)
與正常／seed-17重播逐位元組相同。這是有限實作證據，未代替任意輸入的形式化精化。

本輪 Lean 使用一般 kernel 證明；公理稽核及實際執行紀錄見
[驗證收據](../../../audits/2026-10-26-four-color-mathematical-model-8d28acc/verification.json)。
重播命令如下：

```bash
lake build --no-ansi
lake env lean audits/2026-10-26-four-color-mathematical-model-8d28acc/axioms.lean
python3 audits/2026-10-26-four-color-mathematical-model-8d28acc/replay.py --out /tmp/coloring-model.json
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

**仍OPEN。** Python 到關係模型的逐步精化、一般局部免消元判定與普遍效率界尚未證明。
要證明平面最小反例的完整接口不可能全部阻塞，仍需來源結構定理；同輪
[六跨邊必要條件](../../archive/reports/planar-sources/four_color_six_edge_cuts.md)當時只收緊此義務；2026-10-29後續
[hub 輪圈紙證](../../archive/reports/planar-sources/four_color_six_cut_exclusion.md)已排除裸平面全體頂點最小反例的非平凡六邊割。
同日[雙側七邊割驗證](../../archive/reports/planar-sources/four_color_seven_cut_verification.md)進一步將下界提高為八。
八邊以上與932仍OPEN；新增拓撲論證不在本頁Lean涵蓋範圍，亦沒有將平面必可染寫入上述任何前提。
