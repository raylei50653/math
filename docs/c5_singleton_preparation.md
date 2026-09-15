# Singleton 出口的等高可達性限制與 B₂ 準備策略

2026-09-15。接續 [四度 singleton 局部出口](c5_local_exit.md)。
**邊界障礙、局部 cycle 界與下述條件式染色引理為紙面證明，未 Lean 化。
區域覆蓋、前置操作形成 guard、後綴 χ 不增為固定圖 Python 證據。**

## 1. 推進結果

沿用原 5,952 個完整染色與 boundary-root grammar，沒有擴圖或重搜閉包。

1. 在全部 936 個 `χ=2` 非 Goal 狀態中，等高轉移形成 20 個連通分量。
   四度 singleton 的直接成功出口只覆蓋其中兩個 48-state 分量，且每個狀態已有
   直接出口。其餘 840 個狀態不能僅靠等高操作到達這種出口。
2. 舊 B₂（含 84、531）有 72 個狀態，恰是一個未覆蓋的等高分量。
   它的 boundary 全是 `(A,B,C,A,B)` 型。單頂點改色要直接成功，只能改位置 0 或 4；
   固定圖的四度 boundary 頂點是 1、3，因此此處有純 boundary 層的阻礙。
3. B₂ 的每個起點仍有唯一合法的四度 boundary singleton 操作：在位置 1
   將 B 換成未用色 D。全部都 `χ:2→4`，隨後可接 **2–3 步 χ 不增、且不返回 B₂**
   的成功後綴。全程避開指定禁用型 `[-1,0,2]`。
4. 後綴抽成兩個分支的固定規則，使用完整來源的 component connectivity guard，
   不查 state ID／Goal 表來選操作。48 個來源走兩步後綴；另外 24 個先做一次
   B/C 交換形成 guard，再走相同兩步規則。全部 72 條路徑、240 步已回放。

這給 B₂ 一個較易描述的峰值 4 策略。舊證書已知 B₂ 可用峰值 3 成功，
因此這不是最小峰值的改進，也不將此規則宣稱為一般 K=4 定理。

## 2. 等高操作不能擴大直接出口的覆蓋

先從來源完整染色重新列出全部 maximal-component actions，篩選：

- component 是 boundary 上的一個四度頂點；
- 單頂點改色後的 boundary 達到既有 Goal：三色且唯一色位置在 `{1,3,4}`。

這個來源判定不查目標 ID 或 Goal 表。符合的恰是上一輪 96 個來源。
再取所有 `χ=2` 非 Goal 狀態，保留完整 boundary-root 等高邊，得到下表。
所有等高邊均核對同 pair、同 component 的反向邊存在；禁用增量總和為 +1，
不會刪除等高邊。**這裡可用無向分量；一般禁補償轉移圖仍是有向圖。**

| 項目 | 結果 |
|---|---:|
| χ=2 非 Goal 狀態 | 936 |
| 等高分量 | 20 |
| 含四度 singleton 直接成功出口的分量 | 2 |
| 能等高到達此出口的狀態 | 96 |
| 不能等高到達此出口的狀態 | 840 |

上述數字只針對這個明確的直接出口 predicate。未排除其他直接成功操作，
也未排除先升降再到達 singleton 出口。完整狀態未按顏色置換或 boundary pattern 合併。

## 3. B₂ 的純 boundary 障礙

**紙面引理。** 對 proper C5 boundary `(A,B,C,A,B)`，其中 A、B、C 相異，
只改一個位置且仍 proper，若結果的唯一色位置在 `{1,3,4}`，必為下列兩種：

| 改色 | 結果 | 唯一色位置 |
|---|---|---:|
| 位置 0：A→C | `(C,B,C,A,B)` | 3 |
| 位置 4：B→C | `(A,B,C,A,C)` | 1 |

**證明。** 位置 1 的兩鄰居分別為 A、C，所以改色只可用未用色 D，結果有四色。
位置 3 的兩鄰居分別為 C、B，同理只能改用 D。位置 2 若改色，唯一色位置仍為 2。
位置 0 與 4 的可用新色各為 C 或 D：C 給表中結果，D 給四色。證畢。

固定圖 boundary degrees 為 `(10,4,6,4,7)`。因此在 B₂ 中，四度 singleton
改色不可能直接成功。checker 另外遍歷全部 240 個 proper labeled boundary assignments，
回放單點改色表；表中 10 個共同色正規型只供展示，不拿來合併完整研究狀態。

## 4. 將 singleton 改作受控準備步

對 B₂ 來源取 A=c(0)、B=c(1)、C=c(2)，D 為未用色。每個來源的頂點 1
degree=4，鄰居只用 A/C，因此 `{1}` 是 maximal BD component。

```text
(A,B,C,A,B) --BD@1, component={1}--> (A,D,C,A,B)
```

四邊 dual fan 的計數證明不依賴「交換後立即 Goal」。只需一次共同色角色指定，
將 root 舊色設為 0、新色設為 3、左／右鄰色分別設為 2／1，就得到上一輪同一公式：

```text
ordered Δcycles = (0, R_X-L_X, L_Y-R_Y).
```

故三個系統中一個完整保留、另兩個各增減至多 1；任何符合前提的 singleton
準備步都不會是 `[-1,0,2]` 型，且 χ 增量≤2。
在本 B₂ 的 72 個實例，角色化增量全部是 `(0,1,1)`，所以 χ 恰從 2 到 4。
`singleton_source` 僅讀來源圖與染色，保留四邊 path、retained blocks、owner 布林值；
交換與目標 cycle counts 於其後獨立回放。

## 5. 兩步後綴的來源 connectivity guard

現在固定一個完整來源 c，boundary 為 `(A,D,C,A,B)`，四個色角色相異。
令 `S=Comp_AB(0)`。boundary 上的 `3–4–0` 是 AB 連通 path，
所以 S 的 boundary trace 必為 `{0,3,4}`。

交換 S 後的 boundary 為 `(B,D,C,B,A)`。下一步希望做 AC@4，且不要連帶交換位置 2。
可以直接從**交換前的來源**預測這個 AC 誘導圖的頂點集：

```text
W = {v : c(v)=C}
    ∪ {v : c(v)=A 且 v∉S}
    ∪ {v : c(v)=B 且 v∈S}.

guard(c) := 2 與 4 在 G[W] 的不同連通分量。
```

**條件式染色引理，紙面證明。** 若 guard(c)，則依次交換 AB@0、AC@4，
必到 `(B,D,C,B,C)`，即 singleton-1。

**證明。** AB swap 只將 S 中 A、B 互換，故交換後使用 A 或 C 的頂點集合
恰為 W。由 guard，AC@4 的 component 不含位置 2；boundary 上只有 2、4 用 AC，
因此此 component 的 boundary trace 恰為 `{4}`。最後將位置 4 的 A 變為 C，
得到所列結果。兩次均為 maximal-component swap，保持 properness。證畢。

這個引理不需要平面性，**也不保證兩步的 χ 不增**。局部四邊 cycle 界適用於
前一個 singleton 準備步，不能自動套到此處的兩個大 component。

### 在固定 B₂ 上如何選分支

對 singleton 準備後的完整來源，採以下規則：

1. 若 guard 成立：做 AB@0，再 AC@4。
2. 若 guard 不成立：先做 BC@2。這批 24 個實例的 BC component trace 全是 `{2,4}`，
   boundary 因而成為 `(A,D,B,A,C)`。按新的 boundary 同時重命名 B/C，重新算 guard；
   全數成立，再套用同一兩步規則。

`tail_guard` 用來源 S 和 G[W] 計算 predicate，沒有讀取目標染色、目標 cycle counts
或 Goal 表。`structural_tail` 只按此 predicate 選操作，不依賴 state ID 或搜尋 rank。
兩分支的 role map 始終共同作用於整份來源，不分別正規化三套系統。

## 6. 後綴的 cycle 與路徑證據

在 B₂ 的 72 個來源，第一分支 48 個、第二分支 24 個：

| 分支 | 個數 | 全程高度 | 操作總數 |
|---|---:|---|---:|
| guard 直接成立 | 48 | `2→4→3→2` | 3 |
| 先做 BC@2 形成 guard | 24 | `2→4→3→3→2` | 4 |

所有後綴步驟 χ 不增，故其增量總和≤0，不可能是總和 +1 的禁用型。
每條路徑都不返回 B₂；末態雖回到 χ=2，但已是 Goal。

具體原色路徑：

```text
84 → 94 → 536 → 2034 → 1696
χ: 2 → 4 → 3 → 3 → 2
pair@root: BD@1, BC@2, AC@0, AB@4    （原色 A/B/C/D=0/1/2/3）

531 → 588 → 2142 → 3894
χ: 2 → 4 → 3 → 2
原色 pair@root: (2,3)@1, (0,2)@0, (0,1)@4
```

checker 在既有圖上獨立求「χ≤4、χ 不增、排除 B₂」的反向最短路，保存完整 rank/policy；
再以 NetworkX 有向圖距離核對。來源 guard 規則產生的後綴長度，逐起點等於這個
**指定 singleton 準備後、指定後綴限制下**的最短長度。
這不代表從原起點出發全域最短，也不代表峰值 4 必要。

## 7. 下一個可攻的缺口

已經把 B₂ 的後綴拆成一個一般的來源染色引理與兩項固定圖事實：

1. guard 失敗時，BC@2 的 trace 為 `{2,4}`，且交換後 guard 成立。
2. 所選大 component 操作的 χ 不增，對應表中的 `4→3→2` 或 `4→3→3→2`。

下一步可從失敗 guard 的 G[W] 連通路徑與 BC cut 的交互作用入手，尋找上述兩項
的共同來源充分條件。不能把 24/24 的修復或 72/72 的 cycle 表當作一般存在性引理。
840 個未被直接出口覆蓋的 χ=2 狀態也未因此全部處理；本輪準備策略只涵蓋指定 B₂。

## 8. 重現與信任界線

- [checker](../scripts/c5_singleton_preparation.py)
- [證書](../artifacts/c5_cells/singleton_preparation.json)：20 個等高分量、240 個 boundary
  assignments 的檢查摘要、72 個原始 singleton cut audits、來源 W／components、完整
  宏操作路徑、獨立後綴 rank/policy；所有原 state IDs 由來源 hashes 綁定。

```bash
uv run --with networkx==3.5 python scripts/c5_singleton_preparation.py --check
uv run --with networkx==3.5 python scripts/c5_local_exit.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_barriers.py --check
lake build
git diff --check
```

本輪沒有新增 Lean、圖、閉包搜尋或 Goal 定義；沒有跨圖 K=4 或 `K∞=K≤5` 證明。
程式、證書與報告隨本次交接一併提交。

驗證：上述三個 checker 的 `--check`、`lake build`（僅既有 lint）、新文件連結、
`git diff --check` 與新檔 whitespace 檢查通過。來源 guard 對預測 AC 誘導圖的
完整分量也與實際 AB swap 後的 maximal components 獨立核對。沒有待完成驗證或背景工作。
