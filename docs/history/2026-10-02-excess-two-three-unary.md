# 2026-10-02：三 spokes／三原 unary 共同扇區排除

接手基準 `bbd900ac88571fc2f0ed6aaea5695677e8b9ff88`，當時工作區乾淨。
由 [HANDOFF](../HANDOFF.md)、[STATUS](../STATUS.md)及
[Kempe 導覽](../c5_kempe_guide.md)確認：兩候選均已有 ε≥2，t=3
spoke＋unary 省略的原 triangle 位置已排除，下一題為 path／tail。
本輪採用 math-research-handoff-publish 工作流程；未使用 Graphify，
未開子代理、未提交或推送。

## 成果與證據

[新報告](../c5_excess_two_three_unary.md)直接排除 t=3 三份原 unary，
從而關閉 path／tail 分支。原分量任意大小、實際附件、spoke 與省略
身份全部保留；沒有縮路徑或枚舉圖。

紙面關鍵是：完整 Σ edge-minimality 使每份 unary 在某列為必要因子，
故能放進一份原 degree-4 子覆蓋，進而證它的實際支援至少兩點。
未用色守恆及固定支援穩定子給 ℓ_C≥1+d_C；三條原 spokes 的
共同扇區給逐區跨度預算。六單容量因子的任一拒絕列都有四因子
子覆蓋，同一省略 pair 不能服務兩列，且 pair 不能是兩 spokes。

有限結果：

- 800 個 (spokes, D 身份, target) 比較，兩候選各 400。
- 省略共享與 D 守恆仍有 225 cases：933 為 45、941 為 180。
- 933 的 45 份、941 的 75 份無合法扇區配置；941 其餘 105 份的
  450 個具名扇區配置都被見色／省略共享限制排除。
- 80 份原 spokes／D 身份共 365 份跨度可行配置。
- 15³ 份非空 unary relation 三元組、十種 spoke 色集合，
  共 33,750 份完整四接點接合控制。

抽象殘餘不是來源圖或反例；正是它們表明只用省略共享與 D 守恆不足。
941 的抽象存活 cases 中 60 份僅一個 D 身份、120 份兩個 D 身份，
沒有錯把所有殘餘都當成兩個 D carrier。

證書 [observations.json](../../artifacts/c5_excess_two_three_unary/observations.json)
小於 1 MB，按現行政策直接保留，不新增大型 artifact manifest 項目。
Checker 記錄自身及匯入的共用程式 SHA256；紙面依賴另列於報告。

## 本輪重播

下列均通過：

```bash
python3 scripts/c5_excess_two_three_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_unary.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 兩種 hash seed 逐 byte 一致；原固定色引理局部控制重播通過。
Lean build 成功（8,831 jobs），只有既有 AttachmentOrder／SymRelabel lint。
未重跑全 degree-4／triangle 拓撲模板全集或舊 t=2／t=3 triangle 接回大證書；
本輪任意大小結論沿用其具名紙面分類，沒有新增 Lean theorem。

README、STATUS、Kempe 導覽及相關舊報告補上後續入口。
HANDOFF 的研究線與進行中標記未變，按文件治理保持原薄索引。

## 停止點與下一入口

已完成唯一 degree-6、t=3 的三原 unary 排除，從而完成 t=3
spoke＋unary 省略全收結論。共同 ε≥2 下界未提高，一般來源未排除。

下一窄題：唯一 degree-6、t=3、(2,1) 分拆，省略原 binary C₂
後仍拒絕一列。保留 (r,x,y,v)、原 V、全部附件及三條 spokes，
比較 G−C₂ 與已知雙 spoke／spoke＋unary 省略全收限制。
現行入口由 [Kempe 導覽](../c5_kempe_guide.md)維護。

跨對話可貼：

> 從 bbd900a 後的未提交工作接續。t=3 三原 unary 已由固定省略身份、
> D 守恆及共同扇區跨度排除；800 必要比較、225 抽象存活 cases 幾何
> 細化後為零，33,750 完整四接點接合控制通過。path／tail 缺口已關閉，
> 連同 triangle 完成 t=3 spoke＋unary 省略分支。先讀
> docs/c5_excess_two_three_unary.md 與 docs/c5_kempe_guide.md；重播
> python3 scripts/c5_excess_two_three_unary.py --check。下一題是
> t=3、(2,1)、省略原 binary 後仍拒絕列，保留同源 (r,x,y,v) 與附件。
> 紙面＋有限 Python，未新增 Lean theorem；共同下界仍 ε≥2。
