# Full k≤3 weak-deletion congruence audit

2026-09-16。接續 [A/B 實驗](c5_disk_weak_successors.md)。
**完整指定刪邊域內沒有找到同 Σ、不同 W 的反例。** 這是 Python 有限計算證據，
加上下述一般紙面匹配論證；未新增 Lean 定理。

**後續 quotient 分析：** [87-state relation-order audit](c5_weak_quotient.md)
直接使用本證書，否定 W=covers 及 TC(W)=inclusion；D5 equivariance 全數通過。
沒有重跑本篇全量 audit。

**後續更新（同日）：** [completion 與 Lean bridge](c5_completion_weak_bisimulation.md)
已分別補上完整紙面 completion 與 Lean 一般 weak-bisimulation／trace theorem。
接受其中明列的 topology、plantri 完備性及本篇 Python 計算信任後，結論可
覆蓋全部 k≤3 production cells；母圖只商內點置換的 transport 見後續 §3.1。
下文保留本次計算的原始域與歷史信任聲明；「completion 未證」是後續之前的狀態。
計算證書及 checker 沒有更動，也沒有重跑。

## 1. 搜尋域與結果

從既有 plantri 5.8 `-P5 -c2 -m2` 產生、固定 C5 boundary 標號的全部
726 張 k=0..3 triangulated parents 出發，枚舉每張母圖全部非外圈邊子集。
五條外圈邊與全部頂點保留；允許孤立內點與非三角化後代，嵌入由母圖繼承。
**不宣稱這等同所有 k≤3 cells；completion lemma 仍未證。**

| k | 母圖 | raw states | 不同具名圖 | transitions |
| --- | ---: | ---: | ---: | ---: |
| 0 | 5 | 20 | 11 | 20 |
| 1 | 21 | 672 | 212 | 1,680 |
| 2 | 105 | 26,880 | 5,324 | 107,520 |
| 3 | 595 | 1,218,560 | 164,096 | 6,702,080 |
| 合計 | 726 | 1,246,132 | 169,643 | 6,811,300 |

raw state 是 `(parent, retained-edge mask)`，不同母圖的相同後代可能重複。
「不同具名圖」以 `(k, 完整邊集)` 去重，**沒有再商內點置換**；因此不是同構類數。
母圖僅商內點置換，不商 boundary 的 D5 作用；後代不按 Σ 剪枝。
全部 raw states、全部單邊刪除 transitions 均被檢查。

整個域有 **87 個 Σ、0 個 weak-exit collision classes**。檢查跨全部母圖、
全部後代及不同 k；不只比較根或同 k 的圖。相同具名圖在不同母圖格中的 Σ、W
亦逐一核對一致。87 個 relation 的數量沒有超過上一輪單邊域，這不構成飽和定理。

## 2. 語義與判準

保留完整有序 boundary relation，以共同 S4 色置換的 10 個 orbit bits 編碼，
不使用 pair projections，不重命名 boundary 位置。

\[
G\xrightarrow{\tau}H\iff G\to H\ \land\ \Sigma(G)=\Sigma(H),
\qquad
W(G)=\{\Sigma(Y)\ne\Sigma(G):G\xRightarrow{\tau}X\to Y\}.
\]

strict transition 的 action label 是目標 Σ。具體刪邊身分、silent 步數與成本不在
observable 中；採 divergence-insensitive weak bisimulation。刪邊域是有限 DAG，
也不存在無限 silent divergence。

本輪全域驗證

\[
\forall G,H\in D,\quad \Sigma(G)=\Sigma(H)\Longrightarrow W(G)=W(H).
\]

**紙面匹配論證：** 定義 `G~H iff Σ(G)=Σ(H)`。G 的 silent step 可由 H 零步
匹配。若 G strict 到 Σ=s，則 s∈W(G)=W(H)，所以 H 有 `τ*;strict` 到同 Σ=s
的狀態，target 再次落入 ~。交換 G、H 得反向匹配。域對刪邊封閉，因此這個
論證可反覆使用，證明 ~ 在 D 上為 weak bisimulation；全部有限 observable
traces 相等隨之成立。**本輪不枚舉 traces，也不逐圖對執行一般 bisimulation。**

這是有限域中的結論；一般的 **Weak deletion congruence conjecture**：
「固定有序 C5 disk graphs 在 interior-edge deletion 下，ker(Σ) 為 weak
bisimulation」仍是候選命題，未被本輪證明。此處 interior-edge 指非外圈邊，
包含 boundary chords 與 boundary–interior spokes。

## 3. 計算與獨立核對

對每張母圖依 mask 數值遞增計算，所有單邊子 mask 都較小：

\[
W(G)=\{\Sigma(H):G\to H,\Sigma(H)\ne\Sigma(G)\}
\cup\!\bigcup_{G\to H,\Sigma(H)=\Sigma(G)}W(H).
\]

每個 mask 的 Σ 有兩種獨立計算：

1. 各邊的相容內點賦色 bitset 做交集 DP。
2. 對每個 boundary orbit 枚舉全部 `4^k` 內點賦色，記錄滿足的最大邊 mask，
   再向所有子集做 existential OR propagation。

兩者逐 mask 相等。由共同色置換不變性，10 個 representatives 決定全部 240 個
合法 boundary rows；這輪沒有另對每張圖跑 240 次 backtracking。

每條刪邊均核對 relation 單調性。W 也有**全狀態獨立核對**：對每個 Σ=s，
只在該類 submask 上放入 direct strict exits，再用 subset-zeta OR 聚合所有
子集的出口；最後在 Σ=s 的每個 mask 與 W DP 比較。單調性保證同 Σ submask
與來源間所有中間圖也同 Σ，所以這正是 silent closure 出口的定義。
此外，每個母圖根直接枚舉所有同 Σ submasks 及其 strict edges，再核對一次。

證書的 `sigma_variants` 保存各 Σ 的全部 W variants、raw multiplicities、
各 k 計數與代表 `(parent, mask)`；本輪每類恰一種 variant。
`parent_tables` 保存每個完整 `[sigma_by_mask, W_bitsets_by_mask]` 表的 SHA-256，
不把 125 萬筆重複表全部存入 JSON。`--check` 重算所有表與結果，再逐 byte 比對
證書。如果有碰撞，checker 會保存兩圖完整邊集、區分出口與可重播刪邊路徑；
本輪 `witnesses=[]`。

## 4. 重現與停止點

- [Checker](../scripts/c5_weak_deletion_audit.py)
- [證書](../artifacts/c5_weak_deletion_audit/observations.json)
- [輸入母圖](../artifacts/c5_disk_deletions/observations.json)

```bash
uv run --with networkx==3.5 python scripts/c5_weak_deletion_audit.py --check
lake build
git diff --check
```

來源 SHA-256 綁定輸入及相依程式；重新展開每份已保存 plantri rotation system，
驗證幾何與全部 boundary-fixed parents 一致。plantri 生成完備性仍是外部依賴；
Python 計算與紙面匹配論證都不是 Lean kernel 證明。

本輪停止於完整 k≤3 指定 deletion-domain audit。下一個有界問題可選 k=4
反例搜尋，或分析何種 boundary constraints 結構能推出 W 只依賴 Σ；
**本輪沒有啟動 k=4，也沒有泛化 A/B 的兩因子分解。**

驗證完成：`--check` 全量重播逐 byte 一致、`lake build`（8,819 jobs，僅既有 lint）、
文件連結與 whitespace 檢查均通過。checker、證書與文件隨本次提交發布，沒有背景工作。
