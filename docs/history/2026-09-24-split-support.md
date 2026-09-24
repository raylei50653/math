# 2026-09-24：split-support 相鄰 (2,1) 完整列分類

研究報告：[完整列關係](../c5_two_spoke_split_support.md)。當前優先序見
[HANDOFF](../HANDOFF.md)，此頁保存本輪範圍，發布狀態以即時 Git 為準。

## 結果與覆蓋

在既有 S={b3,b4} split-support 假設下，兩種 C₂／C₁ 禁色次序皆有
完整逐列 F_A、F_D 及 Z_G 公式，Σ=Ω\{q}。所有 tuple 查詢保留原接點
次序與共同色框，沒有相乘同分量的 endpoint marginals。
S={b4,b0} 僅用既有 rho／pi 形式化反射搬運，不另作圖分類。

任意大小化約引用既有 degree-four 結構結果：有 cycle 且 singleton
boundary 未接內點的 minimal core，必為 triangle 或兩 triangles 加
直接 bridge。A 以 D 的實際 z–b1 路徑 padding，保持 A 的全部點與接線。
D 若在 merged row 禁掉兩個未用色，則 D∪{z} 本身成為另一個全 degree-four
minimal core；不是把 C₂、C₁ 合併分析。

固定域新證書：

- A：1,850 個 degree/support 接線，950 個 q 拒絕，64 個 disk；其餘
  886 個 q 拒絕端保存 K5／K3,3 subdivision，接受端保存 apex rotation。
- 64 個 A forms 含 12 個單接點、52 個雙接點；共 15,360 個完整列關係，
  每列另核對四個 simultaneous hub queries 與整個 tuple 的反射。
- D：9＋243 個 actual-graph 接線全量保留 q／p 的完整二接點 tuples，
  無一同時給 F_D(q)={3}、F_D(p)={2,3}。
- 全部 240 labeled rows：216 接受、24 為 q orbit；四個既有未反射
  source controls 的全部 F／Z 與新公式相同。
- 沿用 18 個 canonical tail bases，逐一重查都有 singleton boundary
  attachment；保留依賴 artifacts 的 SHA256。

新 checker 的生成使用 NetworkX 尋找 topology 證書；`--check` 使用標準
函式庫逐一檢查已存 rotation／subdivision，不呼叫 planarity oracle。

## 驗證

本輪已執行並通過：

```bash
uv run --with networkx==3.5 python scripts/c5_two_spoke_split_support.py
python3 scripts/c5_two_spoke_split_support.py --check
python3 scripts/c5_two_spoke_reflection.py --check
lake build
```

另已通過以下沿用依賴的重播：

```bash
uv run --with networkx==3.5 python scripts/c5_multi_odd_cycles.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
```

Fork checker 重播 90,112 個 lifts／88 個 subdivision；two-triangle checker
重播 16,000 個 lifts／649 個 subdivision；path reduction 與 arbitrary-cycle
控制均通過。18 個 tail bases 的 singleton attachment 由新 checker 重查；
原 177,280 個 triangle-branch topology search 未重跑。K4 與更早 triangle-tree
定理仍是沿用依賴，沒有把本輪重播宣稱為全部舊證明重新審計。

新 Lean 使用普通 `decide`，不是 `native_decide`；只證有限列公式與反射
邏輯，不代表任意大小 disk 分類已形式化。`lake build` 通過 8,825 jobs；
修正新檔註解後另通過 `lake build Math.TwoSpokeSplitSupport`。
原有 AttachmentOrder／SymRelabel lint 保留，新檔無新增 lint。

兩份 axiom audit 均通過：

```bash
lake env lean Math/TwoSpokeSplitSupportAudit.lean
lake env lean Math/TwoSpokeReflectionAudit.lean
python3 scripts/check_docs.py
git diff --check
```

全部所列新／搬運 theorem 僅有 `propext`、`Classical.choice`、`Quot.sound`，
無 `sorryAx` 或 native-decide axiom。文件檢查通過 153 份 Markdown／2,001
個本地連結、anchors、索引及 136 行 HANDOFF；`git diff --check` 通過。


## 停止點與未改動範圍

相鄰表項：六項不存在、四項皆單缺失。因此第二缺失核心只剩八個
非相鄰 (2,1) 表項待分離，另有 t≤1／更高 degree 等一般核心缺口。
Order II 的一般實現性仍未證，已非單缺失分類的前提缺口。
一般單側出口、共同 pivotal edge、R31 來源 minor 與 K∞=K≤5 未證。
603 profiles、固定點與舊 artifacts 未修改。本輪未 commit／push。
