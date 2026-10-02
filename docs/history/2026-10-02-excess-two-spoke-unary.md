# 2026-10-02：ε=2 t=2 的 spoke＋原 unary 省略核心排除

後續整理（2026-10-02）：本輪成果的整批發布與最新重播範圍見
[進展整理與發布紀錄](2026-10-02-excess-progress-publish.md)。下文保留當輪研究語境。

基準 `b97b107`。接手時 `main` 比本地 `origin/main` 多一個 commit，
工作樹已有未提交的 941 two-spoke／three-spoke、ε=2 雙 spoke 排除，
以及相關報告、產物登錄及入口更新。先讀 HANDOFF、STATUS、文件治理
及 Kempe 導覽，再選其指定的下一個窄分支。使用者要求「確認接手狀態
並選方向開始推進」，未要求 commit／push。

成果見[專題報告](../c5_excess_two_spoke_unary.md)，目前停止點見
[Kempe 導覽](../c5_kempe_guide.md)。沿用原工作樹，未改寫既有 checker
或證書；未使用 Graphify、未開子代理、未查詢或改寫遠端、未 commit／push。
即時發布狀態以 Git 為準，本地 tracking ref 並非遠端即時核對。

## 結論與證據邊界

- 固定 933／941 的 edge-minimal induced-C₅ disk source、ε=2、唯一
  degree-6 root r、t=2，另明設省略一條原 spoke 及一份原 unary V 後
  仍拒絕列。剩餘全 degree-4 核心的原 r 必為 triangle／bridge 位置，
  由前輪 82 bases／148 個 marked roots 涵蓋。
- 原 V 在全部 proper boundary colorings 都可染：唯一原接點 v 有
  一單位 list slack，spanning-tree 貪婪染色即可。保留 V 的全部附件、
  支援、ownership 和原 relation，不分類或縮減 V。
- 原五接點 relation 是同一四接點 tuple、原 V endpoint 色 d 及
  r≠d 的精確接合。若核心接回 spoke 後 root 有至少兩色，任一非空
  原 unary relation 都不能阻斷。這是完整染色拼接，不是獨立端點
  marginals 或不同列的自由色集合實現假設。
- 592 次 spoke 接回、兩候選各五個 D₅ 像的 5,920 次比較全部排除：
  3,052 次已拒絕候選要求接受的列，2,868 次兩 root 色迫要求拒絕的列接受。
  因此在本輪全部前提下，省略任一原 unary 和任一原 spoke 必全收 Ω。

新證書的五接點 kernel 是接合算子，限制最後一欄到原 S_V(b) 才得到
來源 relation。Kernel 的每份核心染色及四種 v 色的見證都有保存；
未給定的原 V 內部染色由紙面 slack 引理提供，沒有偽造其附件或染色。
所有十五份非空 unary relation 的逐列控制是全稱局部核對，並不聲稱
其任意十列組合可由同一原 V 實現。

必要 mask 區間的聯集為 `{942,958,1006,1012,1014,1020,1022}`，
沒有兩候選的任何像；也不宣稱這七個值都可實現。放寬域含三拒絕，
故沒有沿用前輪「至多兩個相鄰拒絕」的較強觀察。
任意大小涵蓋沿用全 degree-4 分類、外部 degree-list、原 finite topology
及 tail transfer；沒有新增 Lean theorem 或提高 ε≥2 下界。

## 實際驗證

以下均通過：

```bash
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_941_two_spoke.py --check
python3 scripts/c5_excess_two_spoke_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_spoke_unary.py --check
lake build
```

新 checker 重驗全部 82 bases 的 degree、apex rotation、q₄-criticality，
及從原邊重建的 148 個標記位置；1,480 次原核心列關係、5,920 次
spoke 接回列關係、5,920 次五接點算子與獨立完整回溯，以及 88,800 次
非空 unary relation 接合均通過。逐候選存排除列及按 v 色的 tuple 索引。
前輪 two-spoke 重播另涵蓋 19,200 次單 run／1,920 次兩-run 原首點控制。
Lean build 完成 8,831 jobs，僅既有 SymRelabel／AttachmentOrder lint；
未新增 Lean theorem 或重跑 axiom audit。

新 artifact 為 66,817,546 bytes，依 ≥1 MB 政策登錄 manifest 及產生的
ignore 清單；只接受新增產物，不重錄既有歷史檔案：

```bash
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_spoke_unary/observations.json
```

Producer 明列原 `c5_941_two_spoke/observations.json` 為輸入；新 checker
核對該 artifact 的全部直接 source hashes。依賴鏈接回既有 two-spoke
producer 及其原始來源；未使用新 planarity oracle。

文件、產物及 whitespace 檢查均通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

文件檢查涵蓋 425 份 Markdown、4,346 個本地連結；anchors／索引／
HANDOFF 皆通過。DocGraph 為 62 documents、213 relations、5 families，
零 errors／notes。Artifact 狀態 `ok=107`，新 producer 的依賴鏈已核對。

未重跑 three-spoke checker、帶枝大模板全集、雙 triangle 全 lifts、
分叉／全 degree-4 分類、path-reduction 獨立生成器、degree-5／sector
系列、single-spoke／四容量 checker 或 cell enumeration。
涵蓋性沿用原證據；本輪重播所需 four-port bases／relations 及新接合域。

報告、Kempe 導覽、STATUS、README、前輪報告的後續入口與全線快照
說明同步更新。HANDOFF 的研究線／tags 未變，依治理維持薄入口。

## 接手摘要

> 先讀 `docs/c5_excess_two_spoke_unary.md`。933／941 的 ε≥2 之後，
> ε=2、唯一 degree-6 root、t=2、省略一條原 spoke＋一份原 unary
> 仍拒絕列的條件分支已排除。148 marked cores／592 接回的 5,920 次
> 候選比較全排除；關鍵是完整五接點接合及兩 root 色存活，原 unary
> 的任意大小／全部附件保持。紙面＋Python，未 Lean 化，共同下界仍 ε≥2。
> 重播 `python3 scripts/c5_excess_two_spoke_unary.py --check`。
> 下一題限 t=3 的同種省略，並先明設 r 在剩餘全 degree-4 核心的原
> triangle 上；由 three-spoke 的 118 bases／398 個 degree-2 triangle
> 位置接續，保留 (r,x,y,v)。r 在 path／tail 的情形另留，不能直接
> 當成同一涵蓋。前輪及本輪成果皆未 commit／push。
