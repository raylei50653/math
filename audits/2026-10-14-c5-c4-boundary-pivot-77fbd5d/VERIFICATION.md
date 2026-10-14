# 本輪核對與信任範圍

2026-10-14。所有命令在 `/home/ray/developer/ai/math` 執行。
沒有本輪 commit／push，沒有修改舊證書，既有未提交工作保留。

## 1. 主來源橋

```bash
python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/controls/check_transfer.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/controls/check_transfer.py --check
python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/check_independent.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/check_independent.py --check
```

主 checker 與獨立 checker 的普通／seed17 均 PASS。

- 主：132 個既有實圖、528 份完整 C4 fibres（包含空集合）、4×10 計數矩陣、
  1,024 個抽象完整 masks；三支映射為 3／11／11。
- 獨立：五旋轉的 430,080 份 literal support 查詢、1,080 份 cap lifts；
  W5 與刪根二十面體的 144／432 份完整 H lifts，另有空 fibres 及錯誤接邊負控制。
- 獨立證書以 deterministic gzip 保存，17,774 bytes；解壓後完整資料 495,085 bytes，
  沒有裁切原染色集合。
- 主 checker 核對全部八份 frozen input hashes；外部舊 PDF 的實際大小 397,126 bytes
  與 [來源 metadata](external/source.json) 的 SHA-256 一致。
- [diagram.svg](diagram.svg) 通過 XML 解析。示意圖僅展示具名外側 cap。

真正 932／933／941 圖沒有在有限控制中出現；大小排除來自一般來源橋與外部完備範圍。
外部十億級圖枚舉未在本轮重播，沒有新 Lean theorem／本輪 `lake build` 宣稱。

## 2. 旁支 matching 探索

可攜命令及有限域見 [exploratory/REPORT](exploratory/REPORT.md)。
本輪 `uv run --with networkx==3.5 ... --check` 首次因唯讀 uv cache 不能建立鎖而停止：
`Could not acquire lock; Read-only file system (os error 30)`。
改用本機已有唯讀 NetworkX 3.5 套件，沒有重新安裝：

```bash
PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/exploratory/checker.py --check
```

此旁支不參與 K≤22 證明；一般 matching 出口仍 OPEN。
上述 fallback 重播 PASS：79 個實圖、790 個 fibres、1,351 份染色、
2,109 份 matching（868 份 good），以及 3,842 條交換邊。

## 3. 文件核對

正式 docs DocGraph 已通過：96 documents、365 relations、0 errors。
第一次 `check_docs.py` 指出本 VERIFICATION 尚未建立及近期里程碑多一列，已補文件並
將較舊里程碑移出近期表（詳細項目與原證據保留）。收尾重跑 PASS：
`check_docs.py` 核對 679 份 Markdown、8,815 個本地連結及 anchors／index／handoff／近期進度表；
正式 docs DocGraph 為 96 documents、365 relations、12 families、0 errors、0 notes。

全工作樹 DocGraph **FAIL：68 個 duplicate-ID errors**，全部來自保留的 audits／scratch
快照與正式 docs 共用 ID；包括本包的忠實 frozen 文件。
完整輸出保存在 [docgraph-full.log](review/docgraph-full.log)。沒有刪歷史或快照來製造全域 PASS。
正式 docs 通過不代表全工作樹通過。

新連結全部就位後，`git diff --check` 收尾重跑亦 PASS。
