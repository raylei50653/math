# 去除四色定理前提的適用範圍：任意邊界的頂點預算與代表大小界線

2026-10-13。BASE `6943561`；完整 SHA、直接輸入與雜湊見 [INPUTS](INPUTS.json)。
使用者要求檢查目前「移除四色定理」技巧能否更廣使用。本輪只寫本隔離包，
保留既有未提交 `2026-10-13-c5-no4ct-frontier-6943561` 工作。

**可以推廣的是有頂點預算的存在染色與完整接合非空性，介面不限 C5 或 C8。**
本輪抽出任意長邊界、共同平面 gadgets 的精確條件；同時證明「任意長邊界
均有固定五內點完整關係代表」不可成立。新測試的 2,274 份 C8 caps 沒有
多排除原八項必要條件殘留。一般 `K∞=K≤5` 及無界 932／933／941 仍 OPEN。

## 1. 最弱契約與可重用引理

K 僅是已有 132 個具體 C5 完整關係；`932=T4∉K`。反設目錄外來源存在，
令 k 是**所有有限簡單 C5 disk 目錄外來源**的最小內點數。不是固定 mask
最小性，也不把 N2／edge-critical／非空 singleton support 加入前提。
以下一般引理不需要同 k 最大化邊數、近三角化、度數界或 `k≥16`。

沿用 frozen [原始下降引理 A](frozen/audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)：
若有 N 點不可四色平面圖，就有完整關係為 932、內點數至多 N−6 的 C5 disk。
其證明只用最小不可染反例、低度縮減、Euler 及合法共面識別，不引用 4CT。
因此

\[
\boxed{J\text{ 無 loop 且平面},\quad |V(J)|\le k+5
\quad\Longrightarrow\quad J\text{ 可四色}.}
\]

反之，若這樣的 J 不可染，下降會給少於 k 內點的 932 來源，違反同一最小性。
J 可以是其他邊界長度的 disk、商圖或完全不同的平面輔助圖。

這是既有 [C8 相對引理](frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md)
的明確通用接口；本輪沒有把既有引理冒稱首次證明。

## 2. 比原 C8 更廣的適用域

精確證明見 [任意邊界 cap](cap/PROOF.md) 與 [共同 gadget／separator](transfer/PROOF.md)。

| 使用情形 | 足夠條件 | 真正保證 |
| --- | --- | --- |
| 任意 C_b disk A，s 個私人內點；外接 h 個內點 cap | `s+b+h≤k+5` | 同一具名边界的完整關係交集非空 |
| 原內部環包住全部原內點，內側 A 有 k 個總頂點 | 外接 cap 有 `h≤5`；環長 b 任意 | 每一份合法 cap 都有一份相容的 A 完整染色 |
| 一般 n 點圖 H，新增 a 點並保留原邊地合法識別淨減 d 點 | `n+a−d≤k+5`，整體仍平面且無 loop | 一份同時滿足全部附加限制的原 H 完整染色 |
| k 點內圖，任意長簡單 facial cycle | 在其空側加一 hub | 有一份完整染色令該 cycle 至多使用三色 |
| 多個面／separator 共同條件 | 所有 gadgets 同時可畫入，合計點數在預算內 | 同一份完整染色；不能只逐件證可畫入 |

一般 cap 的下降公式是

\[
\Sigma_Q(A)\cap\Sigma_Q(F)=\varnothing
\quad\Longrightarrow\quad
\exists D:\ \Sigma(D)=932,\ k(D)\le s+b+h-6.
\]

若 Q 上 r 個點是原內點、Q 外另有 e 個原內點，則 `k=s+r+e`，
cap 預算寫成 `b+h≤r+e+5`。Q 完全內部時就是 `h≤e+5`。
所以不限於 C8 的 induced 性或指定 apex 結構；那些條件只在特定後續構造中需要。

对同一 literal 邊界列 p，完整延伸數為 x_p、y_p，則

\[
\#\mathrm{Col}_4(A\cup_Q F)=\sum_p x_p y_p>0.
\]

全部空 fibres 保留。若只列 S4 正規化 rows，精確計數須乘各 row 的 orbit size；
非空性不受正權重影響。不同 cap 各有相容列是 `∀F∃p`，不能換成 `∃p∀F`。

還有一個真正跨邊界的抽象版本：若先對含 C5 在內的多個邊界目錄共同
最小化**總頂點數**，且 C5 目錄不含 932，則每個零內點 cap 都不能拒絕
該共同最小來源。輸出 C5/932 必須仍在同一最小性宇宙內，才可作下降矛盾。
本輪未建立新的 C_b 目錄；不能事後把這個新契約套到固定 C_b 最小性。

## 3. 完整關係的小代表不能不分邊界長度

[獨立界線論證](review/SCOPE_REVIEW.md) 給一個無 4CT 的任意大小族，
並由 [第二份審查](cap/REPRESENTATIVE_LOWER_BOUND_REVIEW.md) 核對代表可改弦的情形。
取外框 C_{4t}，依序分成 t 段 `(a_i,b_i,c_i,d_i)`；每段加弦 `d_i a_i`，
在切下的 C4 內放一個接其四點的 hub。各片可同時畫入原 disk。
每段分別選 literal row

\[
P=0201,\qquad Q=0131.
\]

全部 `2^t` 個獨立選擇都有完整延伸。若保留**全部邊界關係**的任一代表
只有 m 個內點，這些選擇不能共用同一內點指派：取兩列不同的一段，
混合出 `0231`，原 hub 已無色可用；但代表的內點指派不變、每條邊仍 proper，
會錯誤地接受該列。

這裡也涵蓋代表新增 boundary chords：所有允許出現的 boundary edges
必在上述全部接受列都 proper，其兩端可取顏色集合互不相交，故混合仍 proper。
不是只比較原圖的邊。由 `4^m` 種可能內點指派，得到

\[
\boxed{4^m\ge2^t,\qquad m\ge\lceil t/2\rceil.}
\]

例如 `t=11` 的 C44 來源，任何同具名邊界、保完整關係的代表至少六內點。
這排除了與邊界長度無關的統一常數代表界；不反駁固定 C5 的五內點猜想，
也沒有排除各固定 b 存在隨 b 增長的代表上界。

任意預著色延伸亦不受相對可染性保證：W4 可以四色，但外框 `0123`
的完整 fibre 為空。[有限反控制](review/scope_controls.py) 同時核對此點與
上述來源族在 `t=2,3,4` 的全部指定 P/Q 列、hub lifts、兩兩混合。
任意 t 的下界由紙面證明提供，不由有限控制外推。

## 4. 實際測試原八項殘留

由 frozen 原 [C8 結果](frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json)
取得八個具名必要上界 U，並核對全部 274 個 row 的順序。
[caps_check.py](caps_check.py) 生成以下**明確有限族**：

- C8 全部 903 份不交叉弦集合，含 132 份 polygon triangulations。
- 每個長度至少四的分割面可選加一個接該面全部點的 hub；三角面 hub
  不改延伸關係，故不加入此族。
- 所有弦、分割面、hub 名字、274 個固定 literal rows 的完整 hub tuples
  與空 fibres 全部保存；沒有獨立改色框。

共 2,274 份 cap，私人內點 0／1／2／3 的份數為 903／1,059／300／12，
全部落在五點預算內。這**不是**所有至多五內點的 cap，尤其沒有相鄰 hubs。
證書 [caps_certificate.json.gz](caps_certificate.json.gz) 含 623,076 個 fibres，
470,831 個為空，169,446 份完整 lifts。

| 必要條件殘留 | 2,274 份 cap 中最小 `|U∩Σ(cap)|` |
| --- | ---: |
| c04-941、c07-941 | 2 |
| c15-933、c18-933 | 4 |
| c15-941、c18-941、c20-941、c30-941 | 4 |

18,192 個 cap／query 測試均未得空交集：**本族沒有新增來源排除**。
U 是原圖完整關係的必要上界；`U∩Σ(cap)≠∅` 不保證真正來源的關係也相交，
更不給來源可實現性或一份符合所有既有計數式的向量。

[獨立 checker](review/independent_caps.py) 不 import producer；以基邊所在面的
遞迴分解重建全部 dissections，並用原邊 DFS 重建完整 lifts，另核對所有
cap 關係的共同交集為空。
後一項直接展示 `∀cap∃row` 不能提升成 `∃row∀cap`。

## 5. 證據層、重播及剩餘義務

- 紙面：相對大小轉用、任意 C_b cap、共同 gadget 預算、代表內點下界。
- 有限控制：本輪 cap 全 fibres、八份原 U 交集、獨立重建及反控制。
- 既有紙面輸入：沿用原 932 編碼證明；本輪新一般化不需要 Corollary 20 或 plantri。
  原 `K≤15` 的外部依賴仍保留，本輪未重跑那些證書或球面生成。
- Lean：沒有新增形式化，也未以既有 Lean build 代表這些紙面結果。

本輪另直接核對 [Dvořák–Lidický 原文](https://arxiv.org/html/1907.04066v2)
§1.1 的完整延伸計數接合式；其 §3 研究的猜想強於四色定理。
本文的相對頂點預算與 C_{4t} 代表下界是上述紙面推導，未當作該論文的結論。
這次查核不構成完整文獻優先權搜尋。

```bash
python3 -B audits/2026-10-13-no4ct-generalization-6943561/caps_check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-no4ct-generalization-6943561/caps_check.py --check --negative
python3 -B audits/2026-10-13-no4ct-generalization-6943561/review/independent_caps.py --check
python3 -B audits/2026-10-13-no4ct-generalization-6943561/review/scope_controls.py --check
```

實際執行結果以 [VERIFICATION](VERIFICATION.json) 及各子包 receipt 為準。
主 cap checker、獨立 cap checker、W4／長邊界控制的正常及 seed17 唯讀
重播均通過；主證書三項破損控制均被拒，W8 控制亦通過。11 份 frozen
輸入與其即時來源 hash 漂移皆零。正式 docs 檢查及正式 DocGraph 通過；
全工作樹 DocGraph 仍因歷史 frozen／scratch 重複 IDs 報 62 errors，列為
FAIL，沒有刪除歷史資料或將其改報通過。新報告本地連結與 whitespace 通過。

原 G 加外側五輪中心有 `k+6` 點，仍恰超出預算；不能用此法免費排除 932。
完整關係保真、任意預著色、list constraints、非平面商圖與固定寬度剝層
都不是存在染色引理的自動推論。W5 一般小代表仍須完整關係替換證明。

後續較有針對性的問題是：為八份 U 找到一份**同時可平面實現**、預算內且
與 U 不相容的外側 gadget，或證明其他同圖完整計數矛盾。不要只把已測試
的獨立 caps 交在一起，亦不要把本輪有限無排除解讀為全部 caps 無效。

Closure scope：本輪精確條件引理、C_{4t} 下界與指定 cap 族控制完成；
無界主命題沒有 closure。
Updated：僅本隔離包。
Reviewed-unchanged：no4ct 交接、Kempe 導覽、STATUS；現有 C8 八項、大小界及
主命題 OPEN 狀態未變，未把探索包自動發布為共享依賴。
Remaining OPEN：無界 932／933／941、一般 `K∞=K≤5`、八項真正來源排除、
一般 W5 小代表與新論證 Lean 化。
Propagation stop：核對 L1 後停；沒有 commit／push，也未改舊證書或並行工作。
