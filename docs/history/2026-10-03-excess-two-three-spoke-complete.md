# 2026-10-03：ε=2 t=3 全部分拆整型排除

**後續發布（2026-10-03）**：本輪與後續 t=0 的完整證據包一併整理
提交推送，見 [發布紀錄](2026-10-03-excess-two-degree-six-publish.md)。
下文保留研究當時的未提交語境；即時發布狀態以 Git 為準。

接手基準 `4701f4c`，工作樹乾淨。使用者要求「推進 t = 3」。先讀
HANDOFF、STATUS、Kempe 導覽與 Git，確認當前窄題是唯一 degree-6
root 的 t=3、(2,1) 整型來源；t=1、t=2 已完成全分拆。本輪沿用原
支援與 complete-relation 工具，沒有來源圖 catalogue 搜尋，沒有
commit／push。成果見 [t=3 合成報告](../c5_excess_two_three_spoke_complete.md)。

## 成果、適用前提與證據界線

共同前提是固定完整 Σ 為 933／941 或整圖 D₅ 像、每條非框邊
Σ-critical、induced-C₅ disk 外框、ε=2、唯一完整 degree-6 root，
其餘有效內點完整 degree 四。本輪完成三種原分拆：

| 原分拆 | 排除機制與固定證書 |
| --- | --- |
| (2,1) | 原短支援各跨度≥2，三 spokes 迫 (1,2,2) 扇區；十份具名位置的 55×15 同源 profiles，共 8,250 次十列 mask 比較全無目標 |
| (3) | 延用至少一 spoke 即成立的三接點容量一 K₅；十份 spokes／十個目標的 100 次容量比較都有 named 拒絕列仍有 root 色 |
| (1,1,1) | 延用短支援引理，三份固定原支援需要六段框邊，超出同一嵌入五段；舊三 unary 整型證書亦保留 |

(2,1) 保留兩份原分量、ordered contacts、原支援端點、ownership、
共同嵌入及同一字面色框。每份 span-two envelope 的 ABA／ABC
equality classes 共用於全部十列。Binary 容量二有 55 profiles，
unary 容量一有 15，包括全空 profiles；這是必要域放寬，不宣稱
每份都有 degree-4 或 disk 實現。固定域的 1,800 份 T4 全收資料
至多缺一列：1,440 全收、360 單缺失。刪去跨列共用 profile 約束，
100 份配置／目標查詢各列獨立選禁色均仍有選項，對照完整保存。

本輪不需要 t=2 的 binary 原路徑／首橋局部 residual，也不需要
前序原省略全收或 unary D 身份 screen。Binary 的第二條 root
incidence 只在相容 lifts 的拓撲 contraction 中刪除，原染色
接合依舊保留完整 R_C(b;x,y)、S_V(b;v) 與全部原 root 邊。

Binary 完整七接點 operator 有 2,916 tuples；15,360 singleton
及 115,200 二元素 binary relation 接合與直接完整 tuples 一致。
相同 endpoint marginals 卻有 root projections [3]／[0,1,3] 的
碰撞保留。Ternary 另有 4,096 singleton／129,024 二元素完整
七接點控制；任意 relation 的接合是 ordered-tuple fibers 的聯集，
不能把 marginals 相乘或將 F 當成一般可迭代 state。

獨立審閱另外以全部 24 個 S₄ 置換及 bitsets 重建 8,250 個 profiles，
得到同一零目標結果；核對短支援前提、binary 拓撲刪邊範圍、相容
包絡、三接點 active triangle 的適用範圍、完整接合與 marginal
碰撞，沒有發現阻斷問題。

三接點容量及短支援的任意大小步驟沿用原 Gallai／block palettes
與 K₅ 論證。本輪重讀外部
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
確認它們要求連通圖、degree assignment 及不可著色，不要求整份
來源在每個 row 下都是 minimal obstruction。外部依賴、紙面證明、
Python 固定域與 Lean 狀態分開。

因此同一前提下 **t∉{1,2,3}**。T4 全收又迫 t≤3；本輪新增六份
四／五-spoke 原 boundary T4 witnesses，重核既有上界。因此唯一
degree-6 root 的剩餘入口是 **t=0**，原六接點接合沒有被本輪排除。
無 spoke 時須先核對外部 hub 的連通前提，不直接套至少一 spoke
的短支援／active-triangle K₅。共同 ε≥2 維持，兩個 degree-5 roots、
一般來源、出口與 K∞=K≤5 保留，未新增 Lean theorem。

## 本輪實際重播

兩份新增 checker 在最終 bytes 上跑一般及 hashseed 重播，均通過：

```bash
python3 scripts/c5_excess_two_three_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_binary.py --check
python3 scripts/c5_excess_two_three_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_ternary.py --check
```

本輪另重播直接沿用的紙面控制／前序：

```bash
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_excess_two_three_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
```

沒有重播全部歷史全 degree-4／Gallai 證書、來源 catalogue、舊 t=1／
t=2 全型證書、binary 省略證書、weak-deletion／R-series／Kempe
closure 或 Lean axiom audit。既有證據按原報告範圍沿用，未將其
混稱為本輪完整重驗。`lake build` 通過 8,831 jobs，只有既有
linter warnings，沒有形式化本輪新 topology／紙面結論。

新增 binary artifact 為 838,735 bytes，ternary 為 145,786 bytes；
兩者都低於 1 MB，隨 checker 保留為待提交的證書，不修改大型
artifact MANIFEST 或 `.gitignore` 政策。各證書保存 producer／
直接依賴 scripts 的 SHA256；`--check` 重建並要求完整 bytes 一致。

文件同步更新合成報告、Kempe 導覽、STATUS、README，並在 t=2
合成、t=3 binary 省略及三 unary 報告加後續連結，保留舊正文的
當輪語境。HANDOFF 的研究線與 tags 沒有變化，依治理維持薄索引。
目前精確停止點以 Kempe 導覽為準。

```bash
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

上述檢查通過：MANIFEST 管理的既有大型產物 `ok=116`；新增兩份
小證書由各自 `--check` 核對。文件檢查通過 463 份 Markdown、4,771
個本地連結與 anchors／index／handoff。DocGraph 通過 62 documents、
213 relations、5 families，零 errors／notes；`git diff --check` 通過。
本輪僅執行既有 DocGraph metadata 檢查，沒有調用 Graphify。

## 跨對話接手摘要

> 已完成 933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源、
> ε=2、唯一 degree-6 root 的全部 t=3 三分拆整型排除。先讀
> `docs/c5_excess_two_three_spoke_complete.md` 與本輪紀錄。
> (2,1) 的短支援跨度≥2 迫原 (1,2,2) 扇區，十份 ownership／
> 包絡下的 55×15 同源 S₄ profiles 共 8,250 次全無目標；不需
> 首橋、原省略或 D 身份 screen，逐列獨立對照的 100 查詢仍全有
> 選項。(3) 用三接點容量一及三 spokes 虹彩位置完成 100 比較；
> 三 unary 由六跨度矛盾排除。完整七接點 relations／色框保留，
> 新一般與 hashseed 重播、沿用四份 checker 及 lake build 通過。
> 同前提下 t∉{1,2,3}，T4 又迫 t≤3，唯一 degree-6 只剩 t=0；
> 下一窄題是無 spoke 的原六接點介面，先核對外部 hub 連通前提。
> 共同 ε≥2 不變，雙 degree-5 roots、一般來源／出口與 K∞=K≤5
> 仍保留，未新增 Lean theorem。保留本輪未提交研究，無 commit／push。
