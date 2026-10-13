# 2026-09-28：record 104 的外部路徑接合

接手 HEAD 為 `0f474d8`；工作樹已有前輪 record 110／119 排除的未提交
source、artifact 與文件變更。本輪沿 HANDOFF 的 record 104 入口推進，
保留既有變更與原必要分類／前輪 JSON，未 commit／push。
採 document-first，未使用 Graphify、未開 sub-agents，未重啟來源圖枚舉。

## 結果與停止點

[新報告](../c5_single_spoke_two_two_external.md) 完成另一原分量 C0 的
z–b1 實際路徑，接合 C1 的剩餘 J 與補弧 b1–b2–b3。C1 的相鄰兩個
路徑塊都接 b0、b4；五個連通、不交 branch sets 給十條原邊鄰接，
所以 record 104 及交換名字後的 record 148 都被 K5 minor 排除。

相同相鄰支援對引理套用原三代表，再排除 210 筆／105 型；其中 106 筆
必須用另一分量外部路徑，104 筆也能用 spoke。累計排除 236 筆，原
380 筆剩 144 筆／72 型；剩餘 A/A 54、A/? 30、?/A 42、?/? 18。
原 104 筆條件式雙列延拓中有 50 筆來源被排除、54 筆仍保留；未新增
p 延拓，也未撤回既有條件式定理。

任意大小由既有 palette／bridge 歸納及新原圖集合抽取承擔；Python
控制不是 degree-4 來源 cover。未新增 Lean theorem，一般 (2,2) 分離
及主命題仍未證。完整 source records、接點、lifts、反射與 raw targets
在新 JSON 原樣保存，checker 另核對 witness 的同一反射來源。

下一題 record 15：s=0、支援 (01,0234)、禁色 ({1},{2,3})，p₁ 已證，
p₂ 未決。C1 每塊必見 b3 及 b0、b2 至少一者；需保留逐塊分配、原
bridge 次序與 C0 的 z–b1 路徑，不能任選同色供應點。

## 本輪實際驗證

- `python3 scripts/c5_single_spoke_two_two_external.py --check`：186 局部支援式、
  496 K5 控制、6 負控制；210 新排除、144 剩餘；JSON 與支援表逐 byte 重播通過。
- `python3 scripts/c5_single_spoke_two_two_minor.py --check`：前輪 48 residual rows、
  192 support rows、256 minor controls、26 排除／354 剩餘原證書通過。
- `python3 scripts/c5_single_spoke_two_two.py --check`：原 1,530 必要配置、380 T4
  保留、完整 ordered schemas、接點資料及繼承的來源 relation 控制重播通過。
- `python3 scripts/c5_single_spoke_bridge_path.py --check`：16 tight rows、12 transitions。
- `python3 scripts/c5_single_spoke_branch_palettes.py --check`：16 palette pairs、107 closure
  cases、20 path cases、5 rooted support types。
- `lake build`：8,826 jobs 成功，只有既有 AttachmentOrder／SymRelabel linter warnings。

文件檢查通過：188 頁、2,279 本地連結，含 anchors、STATUS 索引與
150 行 HANDOFF。DocGraph 通過：22 份 metadata 文件、48 relations、
4 families，0 errors／0 notes。`git diff --check` 通過。重播命令：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑 dual surgery、edge-pair coordinates、circulation、雙拒絕 atlas、
R 系列大覆蓋、大圖 catalogue 或全策略閉包；沒有 Lean source 變更，
未另作 axiom audit。未 commit／push，即時發布狀態以 Git 為準。
