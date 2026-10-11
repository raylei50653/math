# 補償型升高是否必要：完整閉包刪邊檢查

2026-09-15。沿用 [策略落地](c5_strategy_safe.md) 的 survivor-811、兩個 seeds 所生成
的 5,952 個完整原色染色、同一 Goal 與 boundary-root grammar。
**本輪是固定圖 Python 證書，未 Lean 化，沒有跨圖策略定理。**

## 1. 判定結果

從完整閉包的 47,616 條 boundary-root component-labeled 有向邊中，刪掉全部
`sort(cycle_vector[target] - cycle_vector[source]) == [-1,0,2]` 的 **984 條**。
不是只刪先前 B₃／B₂ 的 24 條；反向的 `[−2,0,1]` 操作仍可用。

| K | 初始 χ≤K | 原勝集 | 禁補償型升高勝集 | 新失敗起點 | 門檻內刪邊 |
|---|---:|---:|---:|---:|---:|
| 3 | 3,912 | 2,664 | 2,616 | 48 | 408 |
| 4 | 5,112 | 5,112 | 5,112 | 0 | 864 |

因此 **W₄ⁿᵒᶜᵒᵐᵖ = W₄，但 W₃ⁿᵒᶜᵒᵐᵖ ⊊ W₃**。
門檻 4 可以全程避開此類操作；若要維持門檻 3，部分起點確實需要它。
初始超過 K 者沒有被當成刪邊造成的失敗；未改 seeds 或重新定義初始化範圍。

保留的勝態也可能需要繞路。下表是新最短距離減去原最短距離：

| K | +0 步 | +1 步 | +2 步 | +3 步 | 新最短距離最大值 |
|---|---:|---:|---:|---:|---:|
| 3 | 2,544 | 72 | 0 | 0 | 8 |
| 4 | 4,848 | 192 | 48 | 24 | 6 |

這是重新計算的界，沒有沿用舊宏路徑的步數界。

## 2. 真正的必要性 witness

門檻 3 刪邊後，從 **state 3022** 能到的集合 R 恰是上述全部 **48 個新失敗起點**。
R 全為 χ=2，沒有 Goal；對所有剩餘安全有向操作封閉。
原圖在門檻 3 內離開 R 的 **96 條邊全是被禁止的補償型升高**。
所以任何從 3022 出發、峰值≤3 的成功路徑都必須用這類操作。

原成功路徑甚至只有一步：

```text
3022 → 3489 (Goal)
χ: 2 → 3
cycles: (1,0,1) → (0,0,3)
action: BD@4
Δcycles: (-1,0,2)
preserved system: types {1,3}
```

必要性依據是完整封閉集合及全部出口，不是這條正例本身。
證書 `thresholds["3"].witness` 保存 R、96 條被刪出口及原成功路徑；
`thresholds["3"].lost` 保存全部新失敗索引。
門檻 4 則仍可成功，所以 3022 在禁補償規則下的最小成功峰值由 3 變成 4。
具體可用 `AD@1` 一步到 1027（Goal），cycle 向量 `(1,0,1)→(1,2,1)`，
χ 由 2 跳到 4。這也提醒：本輪只禁止指定補償型升高，並非限制所有升高都為普通 +1。
索引綁定來源證書 SHA-256，完整染色及操作在來源 `states`／`transitions` 查回。

## 3. 普通出口推論與較弱的一般引理

先前 240 條低出口的精確分布是：

| 區域 | 普通 `(1,0,0)` 排列 | 補償 `(2,-1,0)` 排列 |
|---|---:|---:|
| B₃ | 168 | 24 |
| B₂ | 48 | 0 |

使用者指出的普通出口存在性，已可由舊計數及連通性推出，並非需要本輪搜尋才能知道。
兩區任一起點均可等高到達一個普通出口，再接舊證書的不返回受控成功續接。
**這段推論只限制離開 B 的一步，未限制後綴。** 本輪 §1 才檢查全程禁用。

較弱的存在性引理（紙面證明，未 Lean 化）：設 B 為 `{χ≤k}` 中一個連通、
無 Goal、每點 χ=k 的分量，操作可逆。若存在一個 e∈B 的指定好出口 e→t，
χ(t)=k+1，且 t 有不返回 B、峰值≤k+1 的有限成功續接，則每個 s∈B
都有「等高有限路徑→指定好出口→外部成功」路徑，且最小成功峰值為 k+1。

證明：連通性給 s 到 e 的有限 B 內路徑，等高性控制其峰值，再串接出口與續接。
峰值≤k 的路徑不能離開該 sublevel 分量，也不能在無 Goal 的 B 成功，故下界 k+1。
不必假設每個狀態直接有好出口、所有出口都好，或先給跨圖統一的等高步數界 L。
若 B 有限，可另得依賴 |B| 的簡單路徑界；這與跨圖統一小常數界是不同問題。

## 4. 一組完整系統保留，另兩組共用 cut

四色編碼為 F₂²，令邊型 t(uv)=c(u) XOR c(v)，交換色對 a,b，p=a XOR b。
對 maximal Kempe component S，cut 邊型改為 t XOR p，非 cut 邊型不變。
cut 不含型別 p：否則 cut 外端點也在該色對，違反 component 的極大性。
令其餘非零型別為 r,s，則 cut 上僅 r,s 對調，故

```text
D_{r,s}(c') = D_{r,s}(c)
```

這是相同 dual 頂點／邊集合的相等，因而完整 components 相同。
其餘兩組透過同一 cut 耦合重接；不能把它們當作獨立增量，也不能由 +2、−1
直接推斷哪個消失 cycle 造成哪兩個新生 cycle。

checker 重算每個 state 的三組有序 systems，逐條回放 47,616 條 rooted 邊，
核對由交換色對決定的 preserved system 完整相等。
`banned_edges` 保留有序 delta、preserved_system、source、target 與 edge_index；
排序只用於篩選，沒有丟棄 system 身分。

## 5. 驗證與接手

每個 K 保存完整 rank、policy、勝集及安全失敗補集；核對 policy 合法且 rank 下降，
失敗補集無 Goal 且對全部剩餘安全邊封閉。另用 NetworkX **有向圖**反向最短路獨立核對
全部距離。刪邊後不假設可逆性。來源 hashes、完整染色 swap 與 ordered cycle counts
亦核對；`--check` 重算並逐 byte 比較。

實作：[c5_strategy_no_comp.py](../scripts/c5_strategy_no_comp.py)。
證書：[strategy_no_comp.json](../artifacts/c5_cells/strategy_no_comp.json)。

```bash
uv run --with networkx==3.5 python scripts/c5_strategy_no_comp.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_barriers.py --check
lake build
git diff --check
```

下一題應依目標門檻選擇：若採 K=4，研究已存在的禁補償策略之結構理由；
若追求最小峰值，先分析 R 的 96 條強制補償出口及其重接條件。
不再把舊 24 條任意正例當成必要性候選的唯一入口。
本輪停止在這個判定與 witness，沒有擴新圖或主張一般 cycle≤4。

新 checker 與 barriers checker 的 `--check`、`lake build`（僅既有 lint）、
文件連結及 `git diff --check` 通過；程式、證書與報告隨本次交接一併提交。
