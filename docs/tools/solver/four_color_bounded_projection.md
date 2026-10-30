# 以有限色域分解一次完整消元

2026-10-29。本輪完成有限域消元的紙面推導、普通 Lean 核心及獨立 Python 原型。
依賴[完整消元契約](four_color_completeness.md)、[完整接口語義](four_color_mathematical_model.md)
與[部分歷史表示](four_color_partial_history.md)。目前接續入口由[四色導覽](../four_color_guide.md)維護。

**結果。** 一次消元不一定要生成一張涵蓋全部接口的巨大表：若消去點有 q 個候選色，
完整投影等於所有至多 q 個桶內因子的子投影之合取。固定一個支援較小的因子可再減少
子投影數。完整歷史仍保留每個接口的全部回填色，最後才選一份共同染色。
本輪也實測到整次消元退步：不能只看第一步表變小，就採用這種表示。

同日後續：[兩步消元候選驗證](../../archive/reports/four-color/four_color_two_step_verification.md)證明保留 Group A 時的
單邊一色瓶頸及 triangle anchor 的 t=2；限定原邊來源的維度界限與反控制另列。
這些紙面推論未接入本頁原型或新增 Lean，既有 anchored 表示本來精確。

## 同一指派下的精確等式

固定有限簡單無向圖、原頂點次序與字面色號 0–3；固定色與全部有效一元因子先合成
消去點 x 的域 D，q=|D|。其餘含 x 的完整因子為 F₁,…,Fₘ，接口為 Y。
對**同一份**完整接口指派 y 定義

\[
M_i(y)=\{c\in D:F_i(c,y|_{\operatorname{scope}(F_i)\setminus\{x\}})\},\qquad
W(y)=D\cap\bigcap_i M_i(y).
\]

桶外因子保持原樣；剩餘變數的同一份共同指派亦須滿足它們，其在 Y 上的限制才是 y。
精確投影是 R(y)⇔W(y)≠∅。
令 R_S 為 D 與 S 中全部原因子的共同消元，則

\[
\boxed{R(y)\iff\bigwedge_{S\subseteq\{1,\ldots,m\},\ |S|\le q}
R_S(y|_{Y_S}),\qquad
Y_S=\bigcup_{i\in S}\operatorname{scope}(F_i)\setminus\{x\}.}
\]

**證明。** 正向直接限制因子。反向若 W(y)=∅，每個 c∈D 都被某個 Fᵢ 排除；
逐色選一個排除因子，所得集合 S 至多 q 個，已使 R_S 在同一 y 下為假，矛盾。
這個證明甚至不要求整個因子索引集有限；可執行原型只處理有限集。

若 q>0，實作只需所有大小恰為 min(q,m) 的子集：較小子集可擴成這個大小，
大子集有共同支援必然使小子集有支援。m=0 時空子集投影為真；D=∅ 時
保留零元假因子。Lean 的一般定理包含空子集，因而也涵蓋空域與空因子索引。
「只列最大子集」及具體表格編碼的實作對應仍由紙證與有限測試核對。

這與任意截取低階邊際不同：子表來自**原因子子集的共同投影**，所有子表仍在同一份
原頂點指派上取合取；不允許各表選不同的邊界指派，再把各自非空當共同可解。

## 固定一個支援小的因子

選定 anchor 因子 a。若所有接口列都滿足 |Mₐ(y)|≤t，則

\[
\boxed{R(y)\iff
\bigwedge_{S\subseteq\{1,\ldots,m\}\setminus\{a\},\ |S|\le t}
R_{S\cup\{a\}}(y|_{Y_{S\cup\{a\}}}).}
\]

若全交集為空，只須為 anchor 仍允許的每個色選一個其他排除因子。
同理可只生成大小 min(t,m−1) 的其他因子子集；anchor 空支援亦會被拒絕。
普通原邊的條件支援至多三色，三角形因子至多兩色，K₄ 因子至多一色；
後兩者是可接續的結構例，本輪原型初始只建立原邊與域因子。

原型對完整 table 逐列分組，求支援數的統一上界；它不以某一列的較小支援
代替整表上界。選 anchor 時最小化子集數，再按範圍大小與穩定身份打破平手。
這個局部選擇沒有整次成本保證，掃描成本明列於 cap_scan_rows。

## 完整 fibres、全解與原子中斷

子投影只表達存在性；各自選到的 x 色可以不同。回填時仍要由完整歷史 bucket
重算 W(y)，保存全部色，包括空 fibre，不能拿子表各自的見證拼接。
完成 k 步後，沿用既有全解契約：

\[
c\in\operatorname{Sol}(P_0)\iff c|_{U_k}\in\operatorname{Sol}(P_k)
\land\bigwedge_{i\le k}[c(x_i)\in W_i(c|_{Y_i})].
\]

每步 R 的精確等式與原完整消元相同，所以可逐步歸納。原型保留完整舊因子引用的
recipe，而非展開歷史 fibre 表；它沒有丟掉邊界列。相同有序 scope 的生成表可以
取完整列交集合併；來源因子身份另外保存。合併表的來源聯集只供追蹤，不能單獨
當作一次「聯集原因子再投影」的推導證書。先找到剩餘問題的一份共同解，再倒序回填。

建構超限時整步不提交，保留上一個完整前綴、剩餘因子與歷史；未完成投影不當空表。
candidate_checks 等於 color_trials＋cap_scan_rows；factor_lookups 另計實際因子查詢
加上 anchor 表逐列掃描。這些是
原型的建構計費，不等於主引擎 checks，也不涵蓋 Python 設定、表合併、序列化、
最後剩餘問題搜尋或回填。保留精確表示不代表已完成判定；limit 仍是不確定。

## 四因子界限是緊的

取 D={0,1,2,3}，四個 mask 分別為 D 去掉一個不同色，即 7、11、13、14。
任意三者交集非空，四者交集為空。這已由平面四葉星形實現：四個葉點依序取
0、1、2、3，中心沒有可用色。它只反駁「本子投影方案降成三因子仍精確」；
不是所有二／三元推理方法的不可行定理，也不是裸星形不可四色。

全部 16 個四色 mask 的相異子族，大小 0–5 共 6,885 份，獨立核對得到 49 份
極小空交族：單元／二元／三元／四元分別 1／25／22／1，唯一四元族即上述極值。
另核 31,056 個 anchor 與 93,168 個有效統一上界。一般量詞由紙證與 Lean 提供，
這些有限數字只分類上述 mask 集族；重複 mask 不改交集。

## 同一原星形的第一步與整次反控制

強制先消 d 葉星形的中心，D 為全部四色。完整投影允許「葉點最多用三色」，
其列數為 A_d=4·3^d−6·2^d+4（d≥1）。每張四葉投影恰 232 列；
bounded 生成 C(d,4) 張，anchored 生成 C(d−1,3) 張。

| 葉點數 | 單張完整表列數 | 全四因子子集列數 | anchor 子集列數 |
| --- | ---: | ---: | ---: |
| 5 | 784 | 1,160 | 928 |
| 6 | 2,536 | 3,480 | 2,320 |
| 8 | 24,712 | 16,240 | 8,120 |
| 10 | 230,056 | 48,720 | 19,488 |

5–10 葉列數由實作核對，0–8 葉另由原邊直接枚舉核對全部解數與投影列數。
10 葉第一步的完整自足 JSON（含原因子、recipe、元資料與統計）為
full 5,063,464 bytes、bounded 516,684 bytes、anchored 207,795 bytes。
這是序列化大小，不是程序 RSS。相同原型的建構計費為
3,844,109／126,214／50,488；未與主引擎優化枚舉比較，不宣稱整體速度倍數。

**第一步收益不能推到整次。** 同樣先消中心、每例 200,000 單位建構預算：
6 葉 full 用 14,642 單位完成全部七點；bounded 與 anchored 都超限，分別只完成
1／2 步。5 葉三者皆完成，full／bounded／anchored 用 3,244／3,484／4,123 單位。
改成葉點先消，6 葉三者皆只需 59 單位完成；目前主引擎的 min-fill 本來就會先選葉點。
因此這裡的高階中心是表示能力的受控例，不能當成現有引擎加速證據。

另有真平面 K₂,ᵈ 的兩步結構反控制：強制先消一個 hub，再消 anchor 葉點，
若第二步仍用原邊作 anchor，d≥5 時候選因子數由 C(d−1,3) 升為 C(C(d−1,3),3)。
d=12 時是 165→735,130；這是簡化合併前的候選數，不是不可避免的儲存下界。
同 scope 合併可降低最後儲存，但原型仍先付出候選生成成本。

## 獨立全解與剩餘投影核對

[完整審核報告](../../../audits/2026-10-29-four-color-bounded-projection-aec8920/report.json)
採直接原邊／固定色 oracle，JSON 重載後逐份核對全部指派，另核對
**剩餘問題恰為原解的存在投影**。後者不可省：完整歷史可能掩蓋過弱的剩餘約束。

| 範圍 | 輸入／狀態 | 完整配色核對 | 剩餘配色核對 |
| --- | ---: | ---: | ---: |
| 全部 0–4 點圖、全部 ≤3 點部分固定色、具名控制及 seed-20261029 的 5／6 點圖 | 1,142 輸入、13,965 表示 | 2,177,691 | 553,560 |
| 小四環與四色封鎖星形，每個建構預算、三模式 | 2,664 狀態 | 2,544,384 | 2,007,048 |

全部相等；合計 16,629 份表示、4,722,075 份完整配色及 2,560,608 份剩餘配色，
11,393 次有解回填逐原邊核對。10 項針對測試另含八葉全部 65,536 份接口、
字面 ID、有效域縮至空、零元假因子、輸入不變及歷史缺失。
正常與 seed-17 重播逐位元組相同，實際檢查收據見下列證據入口。

## Lean、文獻與研究界線

[ColoringBoundedProjection.lean](../../../Math/ColoringBoundedProjection.lean)普通證明包括
exists_small_obstruction、exists_forall_iff_bounded_subfamilies、四色情境、完整 fibre 對應、
anchor 子型及有限域界限銳利性；已匯入 [Math.lean](../../../Math.lean)。
[公理稽核](../../../audits/2026-10-29-four-color-bounded-projection-aec8920/axioms.lean)
列出七個主要定理，僅使用 propext、Classical.choice、Quot.sound。
Python 的最大子集排程、anchor 上界掃描、表格與版本引用仍未逐步形式化。

文獻定位：Dechter–van Beek 的
[*Local and Global Relational Consistency*, §5.1，Theorems 31–32](https://ics.uci.edu/~dechter/publications/r41-local-global-rel-consistency.pdf)
已有有限域大小與關係一致性／DRC 的結果，其證明同樣逐候選色選排除關係。
本輪是對本專案消元契約的推導、形式化及反控制，沒有全球新定理宣稱。
通常 mini-bucket 的不相交分組與此處完整列出的重疊子族有不同規格；
本等價式不授權任選少量子族而仍聲稱精確。

至多四個**因子**不是至多四個**變數**。若各原因子去掉 x 後至多 r 點，
一個子投影可達 4r 點；後續 r 會增加，因子數也可組合膨脹。
沒有一般固定寬度、多項式成本、無搜尋保證或平面必可染結論。
本輪採納為獨立研究表示，未接入主求解器；一般效率及適應式選擇仍 OPEN。

## 證據與重播

- [原型](../../../scripts/four_color_bounded_projection.py)及[針對測試](../../../tools/tests/test_four_color_bounded_projection.py)。
- [獨立重播](../../../audits/2026-10-29-four-color-bounded-projection-aec8920/replay.py)、[獨立 mask／結構控制](../../../audits/2026-10-29-four-color-bounded-projection-aec8920/structure.py)。
- [完整報告](../../../audits/2026-10-29-four-color-bounded-projection-aec8920/report.json)、[檢查收據](../../../audits/2026-10-29-four-color-bounded-projection-aec8920/verification.json)。
- [來源快照](../../../audits/2026-10-29-four-color-bounded-projection-aec8920/source/Math/ColoringBoundedProjection.lean)；report.json 的 source_sha256 逐份列出來源。

```bash
python3 audits/2026-10-29-four-color-bounded-projection-aec8920/replay.py --out /tmp/bounded-projection.json
PYTHONHASHSEED=17 python3 audits/2026-10-29-four-color-bounded-projection-aec8920/replay.py --out /tmp/bounded-projection-seed17.json
cmp /tmp/bounded-projection.json /tmp/bounded-projection-seed17.json
python3 -m unittest discover -s tools/tests -p 'test_four_color_bounded_projection.py' -v
lake build --no-ansi
lake env lean audits/2026-10-29-four-color-bounded-projection-aec8920/axioms.lean
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

輸出須尚不存在，不覆寫保存證據。快照在 source/ 下保留相同相對目錄，從該目錄
執行其中的 replay.py 可重播當輪 Python，而不混用後續來源；Lean 仍需相同鎖定依賴。
本輪檢查與適用前提已完成，接續問題是兼顧後續 scope 與生成／合併成本的表示選擇。
