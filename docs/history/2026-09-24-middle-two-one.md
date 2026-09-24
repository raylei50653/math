# 2026-09-24：S={b1,b2} 兩個 (2,1) 次序排除

本輪結果見 [專題證明](../c5_two_spoke_middle_21.md)。接手時工作樹乾淨；
研究階段未 commit／push；後續依使用者要求將 checker、artifact、證明及
README／HANDOFF／STATUS 整包提交發布。提交識別與遠端同步以 Git 為準。
優先序見 [HANDOFF](../HANDOFF.md)。

## 結果與新障礙

兩種禁色次序 (F_C₂,F_C₁)=({2},{3})、({3},{2}) 皆排除。
兩個 z–b4 arcs 都見三色，故不能沿用 S={b0,b1} 的兩色短側論證。
改取另一分量的實際 z–b4 路徑，與 A 所在側的 0、1 boundary 點構成
三個兩兩相鄰的連通外部集合。保持同一個 z=2 查詢：

- palette {3} bridge 的兩側 root 都強迫 3，各須接到全部三色外部，
  兩側加三外部集合直接給 K5。
- 否則 leaf block 是 palette {3,h} odd cycle；保留其餘分量 W，根的完整
  可取色集恰為 {3,h}，迫使 W 接到另兩個外部色。cycle 私有路徑分成兩段，
  加 W 及兩外部集合，再給 K5。

允許內部 odd cycles 的 palette 不含 3，亦允許 cycles 共 cut vertex；
沒有把其餘分量當成獨立 bridge tethers。C₂/C₁ 及共同色框保留，
沒有引用 (3) 排除、四色定理或把 minor 當成 Σ 等價替換。

## 證書與驗證

新增 [checker](../../scripts/c5_two_spoke_middle_21.py) 及
[artifact](../../artifacts/c5_two_spoke_middle_21/observations.json)：
32 個 support／root-set 穩定子控制、19 個 leaf root 控制（包括中央
palette 01 triangle 與三個共點 palette 23 leaf triangles）、兩種次序的
480 列完整分量 relation／直接整圖接合核對、38 個 q 刪邊 coloring，
以及 60 個有明示 branch sets 與原始 adjacency edges 的 K5 證書。
兩個完整 degree／minimality 代數控制也各有直接驗證的 K5 branch sets。
有限 minor 樣本不冒充 degree-four 完整來源或 disk witnesses。

本輪實際通過：

```bash
python3 scripts/c5_two_spoke_middle_21.py --check
python3 scripts/c5_two_spoke_adjacent_21.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

`lake build` 成功（8823 jobs），只重播既有 linter warnings。
未重跑雙拒絕 atlas、3703、R 系列大覆蓋、全 R10 checker 或抽象固定點。
任意大小排除為紙面證明＋外部 degree-list 定理＋既有 connected-exterior
K4 引理；Python 核對局部代數與 minor 證書。沒有新增 Lean theorem，
`lake build` 不表示新 minor 證明已形式化。

## 精確停止點

原 18 個 (2,1) 必要表項已有四個排除，其餘 14 個本輪未分類；
S={b2,b3} 的反射搬運尚待明列。沒有刪改原必要位置表、603 profiles
或固定點。一般單側核心存在性／分離、共同出口與主命題仍未證。
