# 2026-09-29：唯一 mixed K2 同端點型，完整關係與原 v-star 來源排除

接手 main@c178cf1，工作目錄為專案根目錄；保留前輪未提交
的三份 shared-endpoint 成果及其文件／證書。先讀 HANDOFF、STATUS、
文件規則，沿 P*ᶻ=P*ʷ={u} 推進；未重開大圖枚舉、未使用 Graphify、
未開 sub-agents、未 commit／push。

## 成果與證據層

[報告](../c5_adjacent_degree5_mixed_edge_same_endpoint.md) 保留原三角形 zwu、
原 uv、u 的一條與 v 的三條 boundary 邊及各 unary 完整有序關係。
q 下 v 強迫 3，u 可用 T={0,1,2}∖{h}；完整 uv-tuples 恰為 T×{3}。
五種 residual 組合及逐邊 minimality 給 240 筆必要正常形。
原 r–u–B 外部路徑 K5 排除含三接點 unary 的 105 筆；135 筆平面必要
資料中 123 筆超框周長，12 筆由五邊飽和與原 v-star 扇區排除。
**整型 disk 來源不存在，不需 T4、0 target 查詢。**

| 控制／證書 | 數目 |
| --- | ---: |
| 每側容量候選／逐類 minimality 比對 | 209／131,043 |
| 必要正常形／三接點 K5 排除 | 240／105 |
| 平面必要正常形／跨度排除／飽和扇區排除 | 135／123／12 |
| 保留原二接點完整 q-schema 計數 | 253,935 |
| q 局部 K2 支援／proper-row 關係控制 | 20／12,000 |
| 獨立 pinned／刪邊 queries | 8,000／56,000 |
| 刪邊兩端同色／完整 uv-tuples 共同色框控制 | 3,290／12,000 |
| 兩算法一致的飽和幾何／來源接合 | 10／120 |
| u 附件與兩 root-spoke 端點候選 | 1,440 |
| 忘掉 v 扇區的假候選／加回後保留 | 4／0 |
| 真正 degree=(5,5,4,…) minimal q-core 控制 | 5 |
| 完整圖 proper-row 接合／逐邊 coloring | 1,200／150 |
| 原 ru 的 K5 skeleton／刪 ru witness 失效 | 80／80 |
| 任意列拒絕公式關係控制 | 12,600 |

省略扇區的四份候選仍有完整 uv-tuples、95×1 個 unary schema 組合，
卻把 u 附件接到 v 三點支援的中點；H−v 連通迫使它位於補弧扇區，
所以這些候選不是同一來源的 disk 實現。不得以獨立支援選擇修補。

任意大小證明為紙面 Jordan／Gallai／來源 minor 論證；Python 重播固定
關係、實際圖控制與必要支援。沒有獨立第二審稿者，未新增 Lean theorem。
本輪 web 讀取外部原文逾時，改下載同一
[Dvořák PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，以 pdftotext
核對第 5–6 頁 Lemma 7 及 Theorem 10；未從有限 skeleton 外推定理。

新增 checker／JSON／逐筆排除表／報告，更新 README、STATUS、HANDOFF、
前序通知、介面導讀及出口失敗核心限制。第八類本身不擴張，未新增空的
第九類。下一窄入口為 P*ᶻ=P*ʷ={u,v} 的原 K4 與實際外部路徑。

## 驗證

下列七個 checker 均實際執行通過，JSON／Markdown byte-identical。
`lake build` 完成 8,827 jobs，僅既有 AttachmentOrder／SymRelabel lint
warnings；本輪沒有修改 Lean，build 不表示新拓撲證明已形式化。
文件檢查通過：263 份 Markdown、2,913 個本地連結，HANDOFF 147 行。
DocGraph：48 份 metadata 文件、141 條關係、5 families，0 errors／0 notes。
`git diff --check` 通過。

前輪 t_w=0、(1,1,1) 報告加入後續通知，其 JSON 僅刷新對應文件的
`inputs_sha256`；與編輯前快照去除該欄後逐欄完全相同。原 shared JSON、
306／288 正常形、9,312 schemas 及此前各輪數學資料保持。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_same_endpoint.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑其餘 shared-endpoint w 分拆／singleton 子類、唯一 degree-5 完成表、
雙拒絕 atlas、R 系列大覆蓋、profiles／閉包及 Lean axiom audit。
一般單側／共同出口與 K∞=K≤5 仍未證，沒有主張全庫研究重驗。
