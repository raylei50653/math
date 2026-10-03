# 2026-10-02：t=3、(2,1) 原 binary 省略分支排除

接手基準 `bbd900ac88571fc2f0ed6aaea5695677e8b9ff88`。工作樹已有
[三原 unary 排除](../c5_excess_two_three_unary.md)及相連報告／索引修改，
本輪先重播並保留它們。記憶中的 ε=1 停止點已被實際文件與 Git 後續
涵蓋；依 HANDOFF／STATUS／Kempe 導覽選擇 t=3、(2,1) binary 省略分支。
使用 math-research-handoff-publish 流程，未使用 Graphify、子代理、commit 或 push。

## 新成果與適用範圍

[新報告](../c5_excess_two_binary_omission.md)證明：固定完整 Σ 為 933／941
或其整圖 D₅ 像的 edge-minimal C₅ disk 來源，ε=2、唯一 degree-6 root、
t=3、原分量分拆 (2,1) 時，刪除整份原 binary C₂ 必全收 Ω。

同一 G−C₂ 的全 degree-4 單缺失迫原 V 在某列禁 D，從而固定 V 的
D 身份及至少二跨度。C₂ 不需分類或正跨度假設。保留同一原嵌入中的
兩份支援包絡、不交開框邊段及三 spokes 切口，結合兩種既有具名
省略全收限制，固定必要域全空。

- 250 份具名共同包絡，2,030 次 (geometry, target, q₀) 比較。
- 未套雙 spoke／spoke＋V 省略限制前，933 留 280、941 留 210；套後皆零。
- 只用整扇區見色仍留 30 份（10／20），完整逐列選項保存在證書中。
- 65,535 份非空有序 binary relations ×15 份非空 unary relations，
  共 983,025 次完整四接點接合；960 次直接 tuple／spoke 過濾及 176 次穩定子控制。
- 同 marginals 而不同禁色的局部反例保留，未將二接點 relation 降成 marginals。

[證書](../../artifacts/c5_excess_two_binary_omission/observations.json)約 612 KiB，
小於 1 MB，直接保留；包含 checker 與匯入程式 SHA256，紙面依賴另列。
未新增大型 artifact manifest 項目或來源圖枚舉。

任意大小涵蓋是紙面證明；有限 Python 空域證書只負責列出的集合域。
沿用全 degree-4 分類、D 守恆及拓撲引理，未新增 Lean theorem。
該 (2,1) 型所有容量二省略均全收，故無全 degree-4 真子核心；
含 degree-5／degree-6 的核心及一般來源仍保留，共同下界仍 ε≥2。

## 本輪重播

```bash
python3 scripts/c5_excess_two_binary_omission.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_omission.py --check
python3 scripts/c5_excess_two_three_unary.py --check
python3 scripts/c5_excess_two_three_spoke_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新證書兩種 hash seed 均逐 byte 通過。三原 unary、t=3 triangle、雙 spoke
及單接點守恆直接依賴重播通過。Lean build 成功（8,831 jobs），只有既有
AttachmentOrder／SymRelabel lint。未重跑全 degree-4／早期任意大小分類
的全部 topology 模板全集、t=2 spoke＋unary 或全部 ε=1 checkers。
文件檢查通過（432 Markdown／4,433 本地連結）；DocGraph 通過
（62 documents／213 relations／5 families，0 errors／0 notes）；
`git diff --check` 通過。

更新新報告、Kempe 導覽、STATUS、README、整合報告與三原 unary 後續入口。
HANDOFF 研究線及進行中標記未變，依文件治理保留薄索引。接手時既有
未提交成果連同本輪新增成果仍留工作樹；沒有宣稱發布或遠端同步。

## 下一入口及跨對話摘要

下一窄題是 t=2、(2,2)，省略一份 binary 後仍拒絕 singleton 列。
保留剩餘原 triangle 的 (r,x,y)、省略分量的 (u,v) 及全部附件，
比較兩份 binary 省略圖的單缺失與已知雙 spoke 全收；目前排程由
[Kempe 導覽](../c5_kempe_guide.md)維護。

可貼：

> 從 bbd900a 後的未提交工作接續。三原 unary 排除已重播；本輪再完成
> ε=2、唯一 degree-6、t=3、(2,1) 的原 binary 省略分支：Σ(G−C₂)=Ω。
> 250 份共同支援包絡、2,030 次候選比較全排除，983,025 次完整四接點
> 接合控制通過。先讀 docs/c5_excess_two_binary_omission.md 與
> docs/c5_kempe_guide.md；重播 python3 scripts/c5_excess_two_binary_omission.py --check。
> 下一題 t=2、(2,2) binary 省略，保留原五接點及同圖附件。
> 紙面＋Python，未新增 Lean theorem；共同下界仍 ε≥2，未 commit／push。
