# 2026-10-03：t=1 兩原 unary 省略與三色存活

接手基準 `main@bbd900a`，保留前輪全部未提交成果；未要求或執行
commit／push。先讀 HANDOFF、STATUS、Kempe 導覽及原四 unary 報告，
接續指定的 t=1、(2,1,1,1) 兩原 unary 省略分支。

成果見 [專題報告](../c5_excess_two_single_spoke_two_unary.md)，目前停止點見
[Kempe 導覽](../c5_kempe_guide.md)。研究線與 tag 未變，依治理保留
HANDOFF 薄索引；更新 README、STATUS、導覽、綜述及前報後續連結。

## 結果與證據

933／941 固定完整 Σ、edge-minimal C₅ disk、ε=2、唯一 degree-6
root、t=1、(2,1,1,1) 下，省略任意兩原 unary 必全收。

若省略 U、V 仍拒絕，剩餘同圖 K 是全 degree-4 核心；r 位於原
triangle／bridge 位置，保留 binary A、unary W 及唯一原 spoke。
沿用既有 82 bases／148 marks 的任意大小原接點 transfer，接回原
U、V 時每份至多封鎖一個 root 色。1,480 次目標比較中，444 次由 K
拒絕目標要求接受的 q₄ 排除，其餘 1,036 次均有指定拒絕列留下至少
三個 root 色，故全部排除。不需 D 守恆、新支援幾何或跨列省略配對。

三種原 unary-pair 只需各自命名保留分量 W，並非圖自同構。完整
(r,x,y,w,u,v) 六接點 tuples、原分量、支援與同一色框保持。
137 份字面核心關係的算子各接全部 225 對非空 unary domains，
30,825 次完整接合與 root 投影控制通過；保留全部原 mark／row
索引及原核心完整染色 witness 入口。

直接紙面推論：省略 spoke＋unary 留下內部 degree 四的 root；
省略 binary 留下三條 bridges 的 root，均不符既有全 degree-4
分類。連同兩 unary 分支，七份容量二省略全收，故該型無全 degree-4
minimal rejected-row core。這不排除含 degree-5／degree-6 核心的
來源，也不提高共同 ε≥2。

新增 checker、超過 1 MB 的 artifact 及 MANIFEST／ignore 登錄；
producer 明列原 two-spoke 核心 artifact 輸入。沒有新增來源圖枚舉
或 Lean theorem；未聲稱抽象 unary domains 或完整來源的 disk 實現。

## 實際驗證

```bash
python3 scripts/c5_excess_two_single_spoke_two_unary.py
python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
python3 scripts/c5_941_two_spoke.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_single_spoke_two_unary/observations.json
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新證書雙 seed 逐位元組重播及既有原核心 checker 通過；後者包含
19,200 次單 run 與 1,920 次雙 run 原首點色控制、5,920 次十列接回及
23,680 次具名因子省略查詢。`lake build` 成功（8,831 jobs、既有
linter warnings）；未重跑全 degree-4 分類的全部歷史 topology 模板。
新紙面結論未 Lean 化。

文件檢查通過：442 份 Markdown、4,536 個本地連結；DocGraph 為
62 文件／213 關係、零錯誤。大型 artifact status 為 `ok=112`；
`git diff --check` 通過，前輪未提交成果保留，未 commit／push。

## 當輪停止點與可貼接手摘要

兩原 unary 省略條件分支完成，連同直接分類推論得該型無全 degree-4
真子核心。下一窄題選 t=1、(2,2,1) 的原 binary 省略；只登錄方向，
未啟動該分支計算。

> 在 `/home/ray/developer/ai/math` 先讀 HANDOFF、STATUS、Kempe 導覽及
> git status。基準仍 `main@bbd900a`，前輪未提交成果保留。已完成
> 933／941 固定完整 Σ、edge-minimal disk、ε=2、唯一 degree-6 root
> 下 t=1、(2,1,1,1) 的任意兩原 unary 省略全收。148 個原核心位置、
> 1,480 次比較全排除；30,825 次完整六接點控制通過。由其餘省略的
> 結構分類亦得該型無全 degree-4 真子核心，未排除整型來源。
> 重播 `python3 scripts/c5_excess_two_single_spoke_two_unary.py --check`。
> 任意大小紙面＋Python，未 Lean 化，共同下界仍 ε≥2。下一題為
> t=1、(2,2,1) 的原 binary 省略；保留兩份 binary 的完整有序接點、
> 原 unary、附件、ownership、環序與共用色框。未 commit／push。
