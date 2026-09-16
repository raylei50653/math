# Weak deletion 的候選定理：相鄰 singleton 與出口規律

2026-09-16。接續 [87-state quotient](c5_weak_quotient.md)，僅讀既有證書。
**找到可具體陳述、零有限反例的候選式；沒有證明它們對任意內點數成立。**
沒有跑 k=4，也沒有重播 deletion audit。

最值得先證的是下述**相鄰雙 singleton 完全釋放**。它不需要未知的
「所有 realizable relations」作右端，也不只是重述 Σ-congruence。

## 1. 首選候選：相鄰雙 singleton 完全釋放

以下先在共同 S4 的十個 orbit patterns 上書寫，等價於其完整有序 rows 的聯集。
Ω 是全部合法 C5 patterns；T4 是五個四色 patterns；p_i 是唯一 singleton
在 boundary 頂點 b_i 的三色 pattern。令

\[
P(G)=\{i:p_i\in\Sigma(G)\}.
\]

**候選命題 A（一般 ordered-C5 disk graphs，尚未證）：** 如果

\[
T_4\subseteq\Sigma(G),\qquad
P(G)=\mathbb Z/5\mathbb Z\setminus\{i,i+1\},
\]

則在保留外圈邊與全部頂點的刪邊語義下，

\[
\boxed{W(G)=\{\Omega\setminus\{p_i\},\;
                    \Omega\setminus\{p_{i+1}\},\;\Omega\}.}
\]

這要求三種 first strict exit 都存在：只放回其中一個 pattern，以及一起放回兩個。
由 relation 單調性，右端已窮盡可能的 strict supersets；**困難只有三種出口的存在性**。

有限證據是五個 D5 位置、15 條 weak edges 全數符合；這五種來源都在 k=3 出現。
五個位置屬於同一 D5 orbit，不是五個獨立結構案例。
例如證書座標 `943` 的缺失 patterns 為 `p_0,p_1`，出口是
`959,1007,1023`。整數只是索引，不放入命題本身。

先證這一例比立即猜測全部 inclusion order 更合適：它只涉及兩個不可延拓
boundary patterns，且沒有未枚舉的中間 relation 或高 k realizability 問題。
這裡的「相鄰雙 singleton」指**兩個缺失的三色 patterns**；
不等同既有 Kempe 路線中「存在相鄰可實現 singleton」的引理。

### 紙面已能證的基底與下一個缺口

若只缺一個 orbit，`Σ(G)=Ω\{p}`，則一般地 `W(G)={Ω}`：
刪盡非外圈邊會得到 Ω，沿此路徑必有 first strict step；單調性使其目標只能為 Ω。
這不依賴 k≤3 或 plantri，是紙面推導，未新增 Lean theorem。

對缺兩個 orbit，這個論證只保證三個目標中至少有一個；不足以證 A。
可把剩餘工作寫成具體 edge-critical 問題：對每種釋放型態
`(p_i,p_{i+1})=(1,0),(0,1),(1,1)`，找一張可經 silent deletion 到達的 H，
及一條非外圈邊 e，使 `H-e` 對兩個 boundary patterns 的可延拓性恰為該型態。
H 可以因型態而不同，不能假定兩種 boundary fibers 共用同一個完整 coloring。
一般圖上如何由平面性與相鄰位置保證這三種 critical-edge 型態，正是待證缺口。

## 2. 支持 A 的較廣有限規律

在本次 R=87 個 observed relations 上：

\[
T_4\subseteq\sigma
\quad\Longrightarrow\quad
W(\sigma)=\{\tau\in R:\sigma\subsetneq\tau\}.
\]

16 個來源、50 條邊，零差異。含 Ω 的空出口情形；其中五個單缺失狀態
屬於上述一般基底，五個雙缺失狀態給出 A，另五個三缺失狀態各有六個出口。
因此這並非要求每個 missing-pattern 子集都能獨立放回：某些子集產生的 relation
不在 R。不可把右端擅自改成全部布林 supersets。

另按原證書 `by_k` 檢查 R≤k，沒有借用 k=3 新 relation 補低 k 的目標：

| k 上限 | observed relations | 含 T4 的來源 | 此類 weak edges | 差異 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 11 | 1 | 0 | 0 |
| 1 | 22 | 1 | 0 | 0 |
| 2 | 52 | 6 | 5 | 0 |
| 3 | 87 | 16 | 50 | 0 |

若要提出更強的一般猜想，可把 R 換成同一 k 上限內的全部 realizable relations。
但這同時引入高 k 的 realization 問題；本輪**優先保留 A 為下一個證明目標**，
不以 16-state 成功宣稱一般 upper-cone theorem。

## 3. 兩條全域候選規律

**候選 B：一個 weak exit 足以釋放任意指定 pattern。** 對任何非 Ω 的 G，

\[
\boxed{\bigcup_{\tau\in W(G)}\tau=\Omega.}
\]

87-state 資料的全部 86 個非 Ω 來源通過。
量詞是 `∀p∈Ω ∃τ∈W(G), p∈τ`，不是存在同一出口放回全部 patterns。
例如 165 的兩個出口 `431,757` 聯集為 Ω，但 Ω 本身不是它的 weak exit。
這條猜想禁止某個 pattern 必須先經過另一個 visible enlargement 才能被放回。

**候選 C：分支出口沒有共同新增 pattern。** 若 `|W(G)|≥2`，則

\[
\boxed{\bigcap_{\tau\in W(G)}\tau=\Sigma(G).}
\]

全部 56 個分支來源通過。也就是每個原先缺失的 pattern，至少能在一個
first strict exit 中繼續保持缺失。它不要求任意兩個 patterns 可獨立操作。

B、C 都不是單調性或已知 weak bisimulation 的形式推論。
抽象 relation DAG `1→3→7` 違反 B；
兩條路徑 `1→7→15`、`1→11→15` 組成的 DAG 違反 C。
這些 DAG 都嚴格增加 relation，也可令每個 relation 僅有一個具體狀態而使
Σ-congruence 平凡成立。它們不是本研究的 disk-graph 反例，只用來辨識證明缺口。

## 4. 30 個單出口來源的 intrinsic 描述

以下三類 **只由 boundary patterns 定義**，不讀 W 來選取，共得到 30 個 relations：

1. 排除恰一個三色 pattern：5 個。
2. 排除一個四色 pattern q，另可排除零、一或兩個使 q 的唯一同色 diagonal
   仍同色的三色 patterns：`5×4=20` 個。
3. 固定四個 boundary 頂點，排除恰好在它們上用滿四色的 patterns：5 個；
   每個這類 relation 缺兩個四色 patterns，不缺三色 patterns。

在 87-state 上，這個 family **恰等於** `{σ:W(σ)={Ω}}`，全部 87 個 membership
比較通過。可保留為**候選 D 的充分條件**：任意 G 若 Σ(G) 屬於此 family，
則 `W(G)={Ω}`。對未知 relation universe 暫不主張逆向分類完備。

其中 10 個只缺單一 pattern，已有 §1 的一般紙面論證；其餘 20 個尚需結構證明。
這提供了可從簡單基底逐步推進的路線，不只是列出 30 個證書整數。

## 5. 反例控制與這些候選式的能力限制

保存了以下失敗測試及全部 witness：

- 將 §2 的 T4 改成「包含全部三色 patterns」：11 個來源失敗。
- 要求任意兩個缺失 patterns 都可「放回第一個、保留第二個」：220 個
  `(σ,p,q)` 失敗。最小 witness 是 165 的 patterns 1、3，兩者總是一起被放回。
- 只建立所有已出現 release masks `τ\σ` 的共用字典，再容許符合字典的
  inclusion pairs：多出 215 條錯誤邊。release mask 本身不足以決定出口。

這些成功候選式仍**未決定整個 W**：對真實 quotient 額外加入
`165→167` 的完整 D5 orbit，共 10 條邊，得到 235-edge 抽象 DAG，
它仍符合 §2、B、C、30-state 精確分類及 D5 equivariance。
這個可重播的 nonuniqueness witness 只表示規則不足，不宣稱新 DAG 可由 disk graphs 實現。
因此本輪進展是找到幾個可明確嘗試證明的窄問題，而非解出全部 relation-only dynamics。

## 6. 產物、驗證與停止點

- [候選式 checker](../scripts/c5_weak_candidates.py)。
- [完整逐項結果與反例控制](../artifacts/c5_weak_candidates/observations.json)。

```bash
python scripts/c5_weak_candidates.py --check
python scripts/c5_weak_quotient.py --check
lake build
git diff --check
```

輸入和分析程式均綁定 SHA-256；原 quotient 及封存 deletion 證書沒有更動。
只在 87 個 relation 上計算集合與布林條件，未做 graph enumeration，未讀取 k=4 資料。
證據沿用既有有限 audit 的信任邊界；上述一般候選 A–D 都沒有新 Lean 證明。
候選式從同一份 87-state 資料歸納並回測，沒有獨立的域外驗證。

驗證通過：兩個小 checker 的 `--check`、`lake build`（8,820 jobs，僅既有 lint）、
本次文件連結與 whitespace 檢查。

下一個窄問題是證 A 的三種 critical-edge 型態，先從相鄰雙 singleton 著手；
本輪停止於候選式及完整有限核對，不自動擴展枚舉。
