# 2026-10-02：ε=2 唯一 degree-6 root 的雙 spoke 省略核心排除

後續整理（2026-10-02）：本輪成果的整批發布與最新重播範圍見
[進展整理與發布紀錄](2026-10-02-excess-progress-publish.md)。下文保留當輪研究語境。

基準 `b97b107`。接手時 `main` 比本地 `origin/main` 多一個 commit，
工作樹已有未提交的 941 two-spoke／three-spoke checker、報告、artifact
登錄及相關入口。先重播兩份證書，確認 933、941 的共同 ε≥2 停止點，
再沿 Kempe 導覽選定唯一 degree-6 root 的雙 spoke 條件分支。
使用者要求「確認接手狀態並選方向開始推進」，未要求 commit／push。

成果見[專題報告](../c5_excess_two_double_spoke.md)，目前停止點見
[Kempe 導覽](../c5_kempe_guide.md)。保留原工作樹成果，未改寫舊 checker
或舊 artifact；未使用 Graphify、未開子代理、未查詢或改寫遠端、
未 commit／push。當前發布狀態以 Git 為準。

## 結論與證據邊界

- 明設原 r 的兩條不同 spokes 刪除後仍拒絕某個 singleton 列。
  degree-4 飽和與 H 連通使剩下整張圖就是 minimal q-core。
- T4 迫原 t≤3；全 degree-4 結構的內部 degree 至多三，故 t=3，
  r 正是前輪 148 個 degree-3 標記位置涵蓋的原 triangle／bridge root。
- 保持原 (r,x,y,u) 完整 relation 的任意長尾枝化約，同時保持兩條
  spoke 接回的不等式。82 bases／148 marked roots 共 888 次雙接回，
  全無 933／941 的 D₅ 像；432 個 T4 全收模型只得 958、1020、1022。
- 因此在唯一 degree-6、ε=2 等全部前提下，候選來源刪去任意兩條
  不同原 spokes 必接受全部十列。這不涵蓋其餘 ε=2 來源，也沒有
  提高共同 ε≥2 下界、證明 ε=2 可實現或排除一般來源。

新增 checker 重建原分量的完整染色，與獨立全圖回溯互核；保存原
附件、ownership、完整 tuples、逐 tuple 完整染色見證及操作身份。
兩個接回次序在同一原 relation 取交；省略其他 spoke pair 時可能
增加 tuples，因此另存完整 relation，沒有以原 tuple 子集冒充。
任意大小涵蓋沿用既有分類、外部 degree-list 定理及原首點 transfer；
新 Python 有限證書不提升為 Lean theorem 或接回圖的 disk 實現。

## 實際驗證

以下均通過：

```bash
python3 scripts/c5_941_three_spoke.py --check
python3 scripts/c5_941_two_spoke.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_double_spoke.py --check
lake build
```

新證書核對 8,880 次雙接回列查詢、17,760 次單接回中間列查詢、
44,400 次具名因子省略及 26,640 次具名 spoke-pair 省略查詢。
重新核對 82 個 bases 的 degree、完整 Σ、apex rotation 及逐非框邊
q₄-critical 見證，並從原邊重建全部 148 個標記位置。
前輪重播同時涵蓋 19,200 次單 run／1,920 次兩-run 原首點控制。
Lean build 完成 8,831 jobs，僅既有 AttachmentOrder／SymRelabel lint；
未新增 Lean theorem，亦未重跑 axiom audit。

新 artifact 為 111,144,359 bytes，按 ≥1 MB 政策保留本地，登錄 manifest
及產生的 ignore 清單；只接受本輪新增產物，未重錄既有歷史檔案：

```bash
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_double_spoke/observations.json
```

新 producer 明列 `artifacts/c5_941_two_spoke/observations.json` 為輸入，
manifest 依賴接到該 producer，再接到雙 triangle producer；新 checker
還核對被引用 artifact 的全部 source hashes。

文件與產物檢查均通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

文件檢查涵蓋 423 份 Markdown、4,329 個本地連結；anchors／索引／HANDOFF
皆通過。DocGraph 為 62 documents、213 relations、5 families，零 errors／
notes。Artifact 狀態 `ok=106`，新 producer 的依賴鏈亦已核對。

未重跑帶枝 177,280 大模板全集、雙 triangle 全 lifts、分叉／全
degree-4 分類、path-reduction 獨立生成器、degree-5／sector 系列、
single-spoke／四容量獨立 checker 或 cell enumeration。
其涵蓋性沿用前輪證據；本輪只重播被用到的完整 bases／relation 與新接回域。

報告、Kempe 導覽、STATUS、README 及前輪報告的後續入口同步更新。
全線整合保留原快照並加後續說明。HANDOFF 的研究線／tags 未變，
依文件治理維持薄入口，沒有塞回詳細結果或停止點。

## 接手摘要

> 先讀 `docs/c5_excess_two_double_spoke.md`。933／941 共同 ε≥2 之後，
> 已排除 ε=2、唯一 degree-6 root、刪兩條原 spokes 仍拒絕某列的
> 條件分支。148 個原四接點 marked cores 的 888 次雙接回全無兩候選；
> 因而候選刪任意兩條原 spokes 必接受全部十列。仍是紙面任意大小化約
> ＋Python 固定域證書，未新增 Lean theorem，其餘 ε=2 未排除。
> 重播 `python3 scripts/c5_excess_two_double_spoke.py --check`。
> 下一題固定唯一 degree-6、t=2，明設省略一條原 spoke 及一份原 unary
> 後仍拒絕列；保留原四接點核心及被省略 unary 的原接點 v、附件、
> 實際支援和五接點聯合 relation，先做同源十列及支援必要條件。
> 既有 two-spoke／three-spoke 及本輪成果均未 commit／push。
