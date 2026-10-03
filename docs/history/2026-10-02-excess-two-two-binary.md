# 2026-10-02：t=2、(2,2) 原 binary 省略與同框第二核心排除

接手基準 `bbd900a`。使用者要求確認接手狀態並選方向開始推進，未要求
commit／push。接手時已有三原 unary 與 t=3 binary 省略兩組未提交成果，
及 README／STATUS／Kempe 導覽等修改；全部保留，於其停止點接續。
記憶中的 ε=1 停止點已過時，本輪以即時文件及工作樹為準。

成果見 [專題報告](../c5_excess_two_two_binary.md)，現況與下一入口見
[Kempe 導覽](../c5_kempe_guide.md)。研究線未增減，HANDOFF 保持薄索引。

## 本輪結論

933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，若 ε=2、唯一
完整 degree-6 root、t=2、原分量接點分拆 (2,2)，則省略任一原 binary
必全收十列。任意大小部分沿用全 degree-4 分類及原有序接點 tail
transfer；Python 只重播固定必要核心及接合，不作新來源圖枚舉。

- 118 bases／398 原 root 位置；兩候選五像共 3,980 比較。
- 完整 binary 禁色必要域及同一省略圖至多缺一列先剩 90 個。
- 12 個無枝核心的明確 apex K₃,₃ subdivision 排除其中 54 個。
- 剩 36 個皆為 941，迫出同一原 C 的另一全 degree-4 核心。
- 24 個沒有符合原 spokes 與拒絕列的第二核心；最後 12 個的 2,376 次
  同框接合全不符目標，差異列均核對完整五接點 relation 及全圖染色。

不是整份 (2,2) 來源排除；未提高 ε≥2，未新增 Lean theorem。
一般來源、共同出口與 K∞=K≤5 仍未證。

## 實際驗證

本輪執行：

```bash
python3 scripts/c5_excess_two_two_binary.py
python3 scripts/c5_excess_two_two_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_binary.py --check
python3 scripts/c5_excess_two_binary_omission.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_941_three_spoke.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_two_binary/observations.json
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 重播原 398 個位置、完整 binary relations、十列原三接點
接合及逐 tuple 原染色，核對帶枝／雙 triangle 的 rotations、degree、
逐邊 criticality。941 three-spoke 重播另含原 tail-root 控制。
`lake build` 成功（8,831 jobs，既有 linter warnings）；不代表新紙面
拓撲已形式化。未重跑其他研究線或無界大小枚舉。
新 checker 兩種 hash seed 均逐位元組重播通過；文件檢查涵蓋 434 份
Markdown／4,453 個本地連結，DocGraph 為 62 文件／213 關係，零錯誤；
artifact status 為 `ok=109`，`git diff --check` 通過。

探索中使用 networkx 3.5 查看固定無枝核心的 apex 障礙；正式 checker
只核對明示 K₃,₃ 九條路徑，無第三方 planarity oracle。
大證書以 MANIFEST／producer 保存重建資訊。未 commit／push。

## 當輪停止點

指定省略分支完成。下一窄題選 t=2、(2,1,1)，同時省略兩份原 unary
後仍拒絕的分支：沿用 398 個核心，保持原 (r,x,y,u,v)、spokes、
分量 ownership 及全部附件，先比較完整接合、D 身份與具名省略全收。
目前排程以導覽為準。
