# 共面識別與最小反例正規形：隔離研究報告

2026-10-12。固定 BASE：`ab0862485b30b12b538c734271f354630afa8e26`。
完整輸入及原工作樹狀態見 [INPUTS.json](INPUTS.json)。本輪輸出只在本目錄；
沒有採納到共享狀態文件，也沒有 commit 或 push。

## 結果

本輪得到一條一般的最小反例正規形引理，並在現有有限前提與已發表文獻下推出

\[
\boxed{K_{\le12}=K_{\le5}=K,\quad |K|=132.}
\]

這是**紙面論證＋固定關係空間的有限核對＋外部定理**，沒有枚舉六至十二內點圖，
尚未 Lean 化。一般 \(K_\infty=K_{\le5}\) 仍然 OPEN；若有新關係，最小來源
至少有十三個內點。

完整證明見 [紙面報告](paper/cofacial_normal_form.md)。三步骨架如下。

1. **聯集封閉目錄的最小來源。** 完整關係滿足
   \(\Sigma(G)=\Sigma(G/(u=v))\cup\Sigma(G+uv)\)。在所有目錄外來源中，先最小化
   內點數，再最大化簡單邊數。合法共面識別會減少一個內點，故 quotient 在目錄中；
   若加邊結果也在目錄中，聯集封閉性會迫使原圖在目錄中。因此 extremality 排除
   所有至少一端為內點的共面缺邊。
2. **簡單三角面正規形。** 刪除不影響完整關係的離散分量及割點枝塊，最小性迫使
   圖二連通。若一個長面含內點，已存在的對角線可能在面外；另一條共面邊，或經
   外側 apex 的路徑，會在該側圓盤連接交錯端點，違反平面分離性。所有內面因此
   為三角形。剩餘候選全收 T4，沒有邊界 chord，排除全邊界長面。
3. **文獻的有界推論。** 正規形保持最小內點數 \(k\)，其對偶有 \(2k+4\) 個頂點。
   Dvořák–Lidický Corollary 20 排除少於三十個對偶頂點的計數反例。兩候選的
   singleton support 包含於 \(\{2,4\}\)，而 \(01232\) 可延伸，迫使計數參數
   \(m=x_{24}>0\)，與該定理給出的 \(m\le0\) 矛盾。因此 \(k\le12\) 全被排除。

第 1 步是可重用的母題：只需聯集封閉的完整關係目錄及合法 equality/disequality
分解，不需對每個 mask 另證一份縮減規則。第 2 步沒有新增 hub、內點或平行邊。
第 3 步的外部定理及精確引用範圍見 [EXTERNAL.md](EXTERNAL.md)。

這套來源選擇是 global minimum interior / maximum edges；不能套用舊研究中
另一種 edge-minimal／edge-critical source 的 deficiency、Gallai 等前提。

## `01232` 的額外資訊

不必先最大化邊数，只要在所有目錄外來源中內點最少，就有：每份 `01232` 完整
延伸中，任意共面且至少一端為內點的不同頂點均異色。933 另有同樣的 `01231`
結論。interior–boundary 識別也是合法操作：保留原 boundary label、C5 框邊與
環序，刪除新產生的內側平行 copy。

有限表為

| 原目標 | 目錄內子關係 | 全部子關係缺少的原目標列 |
| --- | --- | --- |
| 933 | 165 | `01231`、`01232` |
| 941 | 165、424、429 | `01232` |

D5 搬運對整圖及完整色框共同作用，沒有逐列或逐分量獨立重命名。

## 有限證書與反控制

[目前 checker 與命令](controls/README.md)／[v2 證書](controls/certificate.v2.json)：

- 獨立重算全部十個 pattern、132 個 witness 的延伸關係與 apex 平面性。
- 全部 8,778 組含對角無序聯集仍在目錄中。
- 重播有限必要 screen：1023 → 153 → 142，目錄外正是十個帶標號候選；它們
  全收 T4，singleton support 為一點或不相鄰兩點。
- 兩個代表的完整目錄子關係及二十次 D5 搬運，得到十個不同目標。
- 小控制保留十列全部 full lifts，包括空 fibres；quotient pullback 恰等於 Eq，
  加邊恰等於 Diff。Eq 與 Diff 作為關係可以重疊。
- 兩對各別安全但共同 fibre 為空的反控制，阻止把不同著色的見證拼接。
- normal／seed17 byte-identical；破損空列插入不合法 lift 會被拒絕；exclusive-create
  阻止覆寫；凍結輸入未變。

[重接控制](review/rewire_controls.json) 保存同一具名小 disk 的原邊、rotation、
有向面及十列完整 lifts。對一個有兩內點的三角面圖：

| 操作 | 完整關係變化 | 固定 `01232` |
| --- | --- | --- |
| 刪 `0–6`，加另一對角線 `4–5` | 567 → 854 | 原有全部延伸均保留 |
| 刪 `2–6`，再識別內點 `5` 與框點 `3` | 567 → 774 | 原有全部延伸可下降 |

這是「只保某個完整著色／某個 fibre 就能保 Σ」的 **counterexample**；來源
關係為 567，沒有觸發固定 933／941 或最小目錄外前提。

## 證據層與保留邊界

| 項目 | 狀態 |
| --- | --- |
| 有限目錄聯集封閉、子關係、見證、screen 分類 | triggered and holds |
| 小圖 Eq/Diff identity | triggered and holds |
| 獨立見證合併、只保 `01232` 的一般重接充分性 | counterexample |
| 具體 933／941 source、最小目錄外 source | not triggered；未提供、未聲稱實現 |
| 一般共面完備性及最小反例三角面正規形 | 紙面證明；不能由零 target 控制取代 |
| 任意 disk 至多十二內點沒有新關係 | 紙面＋有限前提＋外部 Corollary 20 的推論 |
| 一般五內點代表定理、十三內點以上排除 | OPEN |
| 新 Lean 定理、外部論文計算證書重播 | 未做 |

沒有使用「五內點枚舉已完備」作為新的邏輯前提：132 個具體小 witness、必要
screen 的普遍 soundness 及本輪聯集封閉檢查已足以得到有界等式。必要 screen
的普遍 soundness 仍依賴原紙面 Kempe／disk 黏合論證與 4CT；有限重播只驗證其
mask 分類，並不形式化這些拓撲前提。

## 接續的精確問題

最小反例已可選為簡單、二連通、chordless-C5 近三角化圖。在這個正規形中，
`01232` 的共面異色條件退化為三角形的 properness；不能繼續靠直接共面合併。

已補出一條接續用的窄引理。設內邊 `e=st` 兩側三角形的 opposite vertices 為
`u,v`，其中至少一個是內點。令 `D=G−e`，在同一份完整 `D` 染色中記錄
`A=[s≠t]`、`B=[u≠v]`，並令 `J_e(p;A,B)` 為完整 lifts 的四格 fibre。
對上述全域內點最小的目錄外來源，

\[
J_e(01232;1,0)\ne\varnothing
\Longrightarrow
\exists p\notin\Sigma(G):J_e(p;0,0)\ne\varnothing.
\]

理由是 `Q=D/(u=v)` 減少內點、仍接受 `01232`，故在目錄內卻不可能是原關係的
子關係；必有新增列。該列的完整 lift 拉回 D 後同時滿足 `u=v` 與 `s=t`，後者
來自原邊不能接回。因此存在一份**同一新增列、同一完整著色**的二色四邊形見證。
詳見 [共同關係與窄引理](review/rewire_analysis.md)。它不保證不同原邊的新增列
可以同時或獨立分配。

下一步只研究**刪一條內邊後的完整十列四格關係**：先分清新增的 lifts，再比較
另一對角線或識別條件。要封口，須從 933／941 及 global minimality 推出同一
原圖中逐列所需的完整可延伸條件；上述 567 控制必須被候選引理的前提明確排除。
目前沒有證明任意三角面最小來源都存在保持完整關係的合法重接。

這輪沒有改 Lean source，未重跑 `lake build`、大圖 catalogue DFS、舊 N2／N45
稽核或外部論文的生成計算；不據本輪結果更動那些原有證據的狀態。

整合者的獨立重播、凍結輸入與原工作樹狀態核對見
[ROOT_REPLAY.json](ROOT_REPLAY.json)。紙面獨立審查見
[PROOF_REVIEW.md](controls/PROOF_REVIEW.md) 與 [重接審查](review/rewire_analysis.md)。
