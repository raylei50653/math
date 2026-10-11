# 2026-10-02：ε=2 t=3 原 triangle 的 spoke＋unary 省略核心排除

後續整理（2026-10-02）：本輪成果的整批發布與最新重播範圍見
[進展整理與發布紀錄](2026-10-02-excess-progress-publish.md)。下文保留當輪研究語境。

基準 `b97b107`。接手時 `main` 比本地 `origin/main` 多一個 commit；
工作樹已有 941 two-spoke／three-spoke、ε=2 雙 spoke 及 t=2
spoke＋unary 的未提交程式、報告與產物登錄。先核對 HANDOFF、STATUS、
文件治理、Kempe 導覽及 Git，依導覽選定 t=3 的原 triangle 窄分支。
記憶中的 ε=1 停止點已由現行工作樹超越，以即時文件及重播為準。

使用者要求「確認接手狀態並選方向開始推進」，未要求 commit／push。
本輪保留既有變更，未改寫原 checker／證書，未查詢或改寫遠端、未
commit／push。沒有使用 Graphify 或子代理；現有文件已足以說明依賴。
本地 tracking ref 不是遠端即時核對，發布狀態仍以 Git 為準。

成果見[專題報告](../c5_excess_two_three_spoke_unary.md)，目前停止點見
[Kempe 導覽](../c5_kempe_guide.md)。

## 新進展與界線

沿用固定完整 Σ 為 933／941（含整圖 D₅ 像）、edge-minimal、T4 全收
的 induced-C₅ disk 前提；ε=2 且唯一 degree-6 root r 有三條原 spokes。
明設省略一條原 spoke e 及一份原 unary V 後，K=G−V−e 仍拒絕列，
並且 r 位於 K 的原 triangle 上。

K 的 degree-4 飽和與前輪 tail transfer 給 118 個必要 bases／398 個
原 triangle degree-2 位置。原 binary C₂ 的 (x,y) 完整關係、原邊 xy、
spokes、色框與 ownership 保持；V、v、rv 與全部實際附件未縮減。
原 V 在每列的完整 endpoint relation 非空，故完整四接點接合得到
「至少兩 root 色必接受；唯一 root 色 a 若被阻斷，則原 S_V 必為 {a}」。

1,194 次接回對兩候選各五像，共 11,940 次比較。前輪兩色存活方法
只能排除 10,686 個，餘下 1,254 個由同源省略限制關閉：

- 1,200 個迫同一 G−C₂ 拒絕兩個不同 singleton 列。但該圖繼承
  disk／T4、內部連通、全 degree-4；若拒絕一列即由飽和傳播成為
  minimal obstruction，完整 Σ 只能缺一列，矛盾。
- 54 個迫省略兩條具名原 spokes 後仍拒絕，違反既有唯一 degree-6
  候選的雙 spoke 省略全收結論。保存原 pair 與原 V 的 singleton 要求。

沒有為不同列虛構可獨立選取的 V，亦未用 D／非 D 色守恆作必要
判定。新增證書只量化所有非空 unary relations 以核對局部算子；
它們的十列任意組合不被宣稱為同圖實現。

任意大小涵蓋及全 degree-4 單缺失沿用紙面分類、外部 degree-list
與既有拓撲證據；新證據為紙面共享省略論證＋Python 固定域計算。
沒有新 Lean theorem、沒有提高 ε≥2、沒有證一般來源排除或共同出口。

## 實際驗證

以下重播全部通過；新增完整 tuple 見證索引後，重新產生新 artifact，
並再次執行新 checker 的預設／另一 hash seed 位元組比對：

```bash
python3 scripts/c5_941_three_spoke.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_excess_two_three_spoke_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_unary.py --check
lake build
```

新 checker 重新核對 80 個無枝必要 supports、其 36 個 T4 全收模型及
82 個既有 bases 的 degree／rotation／q₄-criticality，從原邊重建
全部 398 個標記位置；3,980 次原核心列、11,940 次接回／四接點算子、
179,100 次非空 unary 接合、11,940 次 binary 省略與 35,820 次雙 spoke
省略算子均與完整回溯一致。每份核心 tuple 有完整染色見證，省略後
新增的 tuples 亦索引同一原 C₂ 的完整染色並接回原 root／boundary 色。
原 V 的完整染色由紙面 slack 引理給出，未以自由 endpoint 偽造。

前輪 three-spoke 重播另核對 19,200 次單 run／1,920 次兩-run 原首點
控制；雙 spoke 重播驗證其 888 次接回與原因子省略關係。
Lean build 完成 8,831 jobs，只有既有 SymRelabel／AttachmentOrder lint。
未新增或修改 Lean theorem、未重跑 axiom audit。

新 artifact 是 207,785,595 bytes，依大型產物政策保存於本機、登錄
manifest 及產生的 ignore 清單；只 record 此新增產物：

```bash
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_three_spoke_unary/observations.json
```

Producer 明列 `c5_941_three_spoke/observations.json` 及
`c5_excess_two_double_spoke/observations.json` 為輸入；checker 核對兩者
全部直接 source hashes。既有 artifact 與 producer fingerprints 未重錄。

未重跑 t=2 spoke＋unary 獨立 checker、two-spoke 獨立 checker、原帶枝／
雙 triangle 大模板生成器、分叉與全 degree-4 分類、degree-5／sector
系列、四容量及 single-spoke 全表、cell enumeration。依賴涵蓋沿用原證據；
本輪重播所需 three-spoke bases、tail 控制、雙 spoke 定理固定域及新接合。

專題報告、Kempe 導覽、STATUS、README、原報告後續入口與全線快照
說明同步更新。HANDOFF 的研究線與 tags 未變，依治理保持薄入口。
以下收尾檢查亦通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

文件檢查涵蓋 427 份 Markdown／4,369 個本地連結，anchors／索引／
HANDOFF 均通過；DocGraph 為 62 documents、213 relations、5 families，
零 errors／notes。Artifact 狀態 `ok=108`，新 producer 的兩項直接
依賴及其既有依賴鏈均已登錄。

## 接手摘要

> 先讀 `docs/c5_excess_two_three_spoke_unary.md`。933／941 的共同下界
> 仍為 ε≥2。本輪排除 ε=2、唯一 degree-6 root、t=3，省略原 spoke
> 及原 unary 後仍拒絕、且 root 在剩餘全 degree-4 核心原 triangle 的分支。
> 398 marked roots／1,194 接回的 11,940 比較全排除；兩色存活留 1,254，
> 以同一 binary 省略圖單缺失排除 1,200、既有雙 spoke 省略排除 54。
> 保留原 (r,x,y,v)、V 任意大小與全部附件。紙面＋Python，未 Lean 化。
> 重播 `python3 scripts/c5_excess_two_three_spoke_unary.py --check`。
> 下一題限 t=3 同種省略的 path／tail root：原 G−r 是三份 unary，
> 先研究共享省略身份；若縮路徑，另證原接點關係保持，不能沿用 triangle
> 398 位置涵蓋。既有與本輪成果均未 commit／push。
