# C5 edge-state：switch、區域坍縮與中間相容狀態

2026-09-15。使用者澄清本輪關注 **edge-state 怎麼 switch 和狀態坍縮**。
本輪只沿既有 Errera 與三個 survivor 的具體 routes，沒有新增圖搜尋。
這裡先把「坍縮」具體化為 switch 後指定區域縮小、接口消失；
沒有把它定義成 C5→C3/C4 的圖收縮。

後續已實作 [多候選 joint edge-state](c5_edge_choices.md)，並保存局部 BC switch 的
cycle 消失與區域分裂／合併見證；可從該報告接續。

## 1. Switch 的操作定義

固定完整 embedded disk、顏色 A=0、B=1、C=2、D=3，edge type 為端點 XOR。
給一個實際 maximal `{a,b}` component S，令 k=a xor b：

1. 求實際 cut ∂S，即恰有一端在 S 的邊。
2. 只在 cut 上將 edge type t 改為 t xor k。
3. 重算另外兩組 systems 的 paths/cycles，以及 boundary connectivity。

cut 上不會有 type k；其餘兩種 types 互換。
這兩種 types 組成的 system **整個邊集合及其 components 保留**。
cut 必須是這個 system 的若干完整 paths/cycles 的聯集。
另外兩組 systems 則刪掉部分邊、加入部分邊，重新接線。
checker 保存前後每個 component 的完整 edge indices，及保留邊的交集矩陣；
矩陣是實際邊的對應，不能把計數變少直接稱為圖的拓撲收縮。

指定 S 的 switch 是 involution：同一色對、同一 S 再做一次便回原染色。
所以完整狀態上的這項操作可逆；「坍縮」可以描述所觀察接口的消失，
不表示整張圖或完整染色資訊被不可逆地刪除。

## 2. 已核對的接口坍縮

固定 `errera-0`，起始染色：

```
(0,1,0,2,3,2,3,0,3,1,3,1,1,2,2,0)
```

boundary=ABACD。令 S=Comp_AC(0)、T=Comp_AD(2)。
做 CD component `{5,6,8,10,13,14}` 的 switch。
它的 dual cut 是 βγ system 的 **兩個完整 cycles**，共 20 條邊；
不是任取一條 alternating curve 當作同一 primal move。

| 觀察 | switch 前 | switch 後 |
|---|---|---|
| S | {0,5} | {0} |
| T | {2,10} | {2} |
| C∩S 與 D∩T 的接口 | 邊 (5,10) | 空 |
| boundary | ABACD | ABACD |
| 三組 boundary pairings | 相同 | 相同 |
| 三組 cycle 數 | (0,0,2) | (0,0,2) |
| 是否有一步禁止 singleton | 無 | 無 |

接口消失是因其端點換色後退出新定義的 S、T；原圖邊 (5,10) 沒有被刪除。
這個中間狀態有完整 proper coloring 和同一 verified disk 作見證，
因此是**實際可實現且目前一步相容**，不是只通過抽象 matching 的猜測。
但它已不满足先前由全圖 P⊆{0,2} 推出的接口必要條件，故不能延伸為該全域假設的見證。

接著做 AC `{0}`，再做 AD `{2}`：

```
ABACD --CD(內部 component)--> ABACD --AC{0}--> CBACD --AD{2}--> CBDCD
  相容                         相容             有一步 escape      singleton-1
```

这里「相容」明確限定：當前不是 singleton-{1,3,4}，且任何單一 component move
都不會立即到達它們。第三個狀態本身還不是禁止 singleton，但已有一步 escape。
不能把前兩個相容狀態當作對所有未來 switch 封閉。

## 3. Survivor 的中間狀態與非單調性

同時重播既有五條 survivor routes；共六條 traces、14 次 switches。
每一步保留共同原色框架、完整 edge types、三組 components、cut 和 escape actions。

- survivor-590：相容 → 相容 → 有一步 escape → 禁止 singleton。
- survivor-811／891 的各兩個起點：相容 → 有一步 escape → 禁止 singleton。

590 的 cycle counts 沿路為 `(0,0,0)→(0,0,1)→(1,0,0)→(0,0,0)`。
故「switch 只會消除 cycles」為假；這些數字也沒有提供嚴格下降量。
目前已確認的中間相容狀態逐項存於 `traces[].states[]` 的
`compatible_through_one_move`，不把它們升格為全 class invariant。

## 4. 邊界與後續入口

本輪是固定圖的精確 Python 證書；沒有新增 Lean、一般收縮定理或新的 relation 排除。
若下一步要把坍縮定義成 C5→C3/C4，須另外定義新 terminals、壓縮後的完整對齊
interface relation，以及它如何保留 switch。上述區域縮小沒有自動給出這種操作。

直接接手可從 Errera 的第一步開始：兩個 cycles 的聯合 switch 如何使接口消失，
而所有 boundary pairings 都保持；再檢查更完整的 interface 資料能否導出重接規則。
`c5_edge_incidence.py`／證書已重播，其結果見 [joint incidence 報告](c5_edge_incidence.md)；
與本輪操作 traces、多候選 API 一起整理提交。

```bash
uv run --with networkx==3.5 python scripts/c5_edge_switches.py --check
uv run --with networkx==3.5 python scripts/c5_edge_states.py --check
lake build
git diff --check
```

[checker](../scripts/c5_edge_switches.py)／[證書](../artifacts/c5_cells/edge_switches.json)。
