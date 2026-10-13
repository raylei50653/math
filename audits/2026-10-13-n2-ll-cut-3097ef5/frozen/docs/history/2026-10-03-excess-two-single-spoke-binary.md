# 2026-10-03：t=1 原 binary 省略與完整六接點接合

接手基準 `main@bbd900a`，保留前輪未提交成果；未要求或執行
commit／push。先讀 HANDOFF、STATUS、Kempe 導覽及前輪報告，
接續 t=1、(2,2,1) 原 binary 省略。成果見
[專題報告](../c5_excess_two_single_spoke_binary.md)，目前停止點見
[Kempe 導覽](../c5_kempe_guide.md)。研究線與 tag 未變，依治理保留
HANDOFF 薄索引，更新 README、STATUS、導覽、綜述與前報後續入口。

## 結果

933／941 固定完整 Σ、edge-minimal C₅ disk、ε=2、唯一 degree-6
root、t=1、(2,2,1) 下，任一原 binary 省略必全收。核心留下三種
root 色時，任取被省略原 binary 的完整染色，其兩接點無法全部封鎖。
完整六接點接合保留兩份原 binary 的有序 relation 與原 unary。

- 82 bases／148 marks／1,480 份原十列 relations 重新核對。
- 1,480 次目標比較全排除；444 次由 q₄ 衝突，1,036 次由三色存活。
- 137 份字面算子，2,192 次 singleton、16,440 次二元素 relation 控制。
- 16,576 個有序 binary 色對到原核心 tuple／染色 witness 的 lifts。
- 三個容量二身份（兩份 binary 各自省略、spoke＋unary）全收，
  故同型無全 degree-4 真子核心；未排除整型或提高共同 ε≥2。

任意 relation 涵蓋由逐 tuple 的 union 恆等式負責，未枚舉全部
65,535 個非空 relations。任意大小核心涵蓋沿用原分類與接點 transfer；
無新增來源圖枚舉、支援幾何、跨列省略配對或 Lean theorem。

## 驗證

下列指令實際通過：

```bash
python3 scripts/c5_excess_two_single_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_single_spoke_binary.py --check
python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
python3 scripts/c5_941_two_spoke.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 完成 8,831 jobs，只有既有 lint warnings。原核心 checker
重播 19,200 次單 run、1,920 次雙 run 原首點控制；未重跑全 degree-4
分類／外部 degree-list 的全部歷史拓撲證據。新 artifact 已登錄
MANIFEST、producer 及原核心輸入依賴；既有產物未重新生成。

本輪停止於指定 binary 省略及上述同型推論。下一窄題記為 t=1、
(1,1,1,1,1) 整型來源，從同源四容量子覆蓋與原 root 的 bridge／cycle
結構開始；本輪未啟動。一般來源、兩 degree-5 roots、出口與 K∞=K≤5
均保留，新增結論未 Lean 化。
