# C₅ class 兩點重疊研究導覽

更新：2026-09-30。研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見
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
| 拓撲與多步 | 實際邊、環序、側別及未來接觸範圍須另查；尚無一般充分摘要 | [拓撲界線](c5_two_vertex_overlap.md) §5 |

## 3. 精確停止點與下一個窄問題

一次具名接合的窄問題已完成：A=B=R1023、A `(0,2)` 接 B `(0,1)`
得到完整 140 軌道／3,360 賦色，`π_A=R1016`、`π_B=R1023`，
並由補回框邊的同代表整圖重算確認。另有反向雙射、自由點對、共同
弦／框邊及七個私有內點控制，共六份；所有完整 J、映射及 witnesses 已保存。

下一個窄問題是**沿用這份主例的實際接合圖，分項稽核拓撲**：

1. 分開判斷抽象平面性、指定原 A 框及原 B 框是否可作 disk 外界。
2. 對「兩份原 disk 區域如何重疊」先明列側別及合法性條件；未指定或
   未驗證的項目保持 unknown，不由一般平面性推得合法 disk transition。
3. 保留現有八點 relation，將拓撲證據綁回同一代表、雙射與實際邊。
   單份 witness 的結果不推廣成同 Σ 全部實現的拓撲性質。

完整後繼表尚未產生。其接口要保留原五點投影、八點或另選 frame，
仍須依未來可接觸範圍判定。若丟掉 B 的剩餘三點，要證它們不再被未來接觸。
接合後的五點 relation 未必還是 132 類中的 disk cell；須另查幾何及代表。

任意大小 class 目錄完備性、拓撲摘要充分性、無假路徑的多步同餘、
生成圖類涵蓋與五內點代表命題全部保留；`K∞=K≤5` 未證。

## 4. 閱讀與重播入口

先讀[資料與規格](c5_two_vertex_overlap.md)、[八點接合報告](c5_two_vertex_join.md)與
[接合紀錄](history/2026-09-30-c5-two-vertex-join.md)，再視需要讀
[state language](state_language.md)、[local closure](local_closure.md)、
[cell enumerator](c5_cell_enumerator.md)及[既有 state 導覽](c5_state_guide.md)。

```bash
git status --short --branch
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/c5_two_vertex_join.py --check
```

點對重播只依現有來源 JSON；八點重播另驗四份來源代表與六份接合圖的
完整染色，不做 embedding 或大枚舉重驗。
不得以 1,320 份點對表取代完整 Σ；不得把 `geometry=unknown` 當 disk transition。
