# 2026-09-28：相鄰雙 degree-5 有序色對介面與刪邊

接手 HEAD `d0d4e9d45fe7faa129116a73af7a64517df109c3`，起始工作區乾淨。
本輪未 commit／push，也未開 sub-agents；目前優先序見 [HANDOFF](../HANDOFF.md)。

## 成果

[報告](../c5_adjacent_degree5_interfaces.md) 固定原 H−{z,w} 分量及實際
boundary／root 接線，用同一個接點 tuple 同時避開有序 root 色對。
共鄰點保留一個頂點身份、兩條 incidence；全部 boundary rows 共用原圖。

已給任意大小紙面證明：

- 精確式 `Z=(A_z×A_w)∩⋂R_C∖Δ`，刪 zw 的關係是未扣 Δ 的交集 K。
- root-edge critical iff `∅≠K_q⊆Δ`；每份刪後染色都迫使兩 root 同色。
- degree-4 分量的拒絕列 tightness；有共鄰點的分量接受全部對角。
- 分量內部非 bridge／bridge、C-root 邊、C-boundary spoke 任一被刪，
  整個原 C 區域的 R_C 皆成 U²；證明分四類，不預設單 root 結論適用。
- root-spoke 新色條帶、分量私有非對角色對，以及完整逐邊 minimality 等價式；
  每份刪邊見證另迫使被刪邊兩端同色。
- 固定來源任意多步刪邊精確式，保留分裂前的原分量身份；至多九個開關，
  不作跨來源狀態或小 disk 代表宣稱。

Gallai tree 結構推論單獨依賴外部 degree-choosability 定理，本輪重新核對
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的連通、degree assignment 與不可著色前提。核心接合／刪邊證明僅用初等
染色與生成樹貪婪法，不依賴 Gallai，也不依賴平面性。

## 有限控制與驗證

[標準 Python checker](../../scripts/c5_adjacent_degree5_interfaces.py) 與
[JSON 證書](../../artifacts/c5_adjacent_degree5_interfaces/observations.json)
保存來源程式 SHA256、原圖邊、兩份有序接點序列、共鄰點身份、十個 canonical
rows 的完整接點 tuples／染色見證及全部 240 列的關係。

| 核對項目 | 數量 |
| --- | ---: |
| 固定 degree-4 分量 | 9 |
| base 的獨立 pinned 染色查詢 | 34,560 |
| 逐 boundary row／E_C 刪邊關係 | 19,920 |
| 刪邊後獨立 pinned 染色查詢 | 318,720 |
| 拒絕列刪邊端點同色控制 | 14,832 |
| 全域 S₄ 搬運核對 | 2,160 |
| 兩張固定來源圖的逐列刪邊公式核對 | 53,040 |
| 抽象 minimality 條件代數 | 1,024 |

兩張來源圖核對所有單邊、雙邊及指定較大刪除集合。第一張完整 degree
序列為 (5,5,4,4)，root-edge 刪後有兩個對角色對，但不滿足完整 minimality；
第二張核對兩個原分量的共同接合，僅作代數控制。沒有稱這兩張為 disk／T4
minimal cores。抽象 masks 只核對邏輯條件，亦不聲稱任何圖可實現。
四個負控制分別是共鄰點拆開、marginal 相乘、獨立色框重命名，以及
degree=5 分量的刪邊不全解除，保留 degree=4 假設的界線。

```bash
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

生成器與 `--check` 逐 byte 重播通過，以上有限斷言全部成立。
`lake build` 通過（8,827 jobs），只有既存 AttachmentOrder／SymRelabel
linter warnings；未新增 Lean theorem。文件檢查通過 222 份 Markdown／
2,578 個本地連結；DocGraph 通過 34 份 metadata 文件／83 條關係／
5 families。HANDOFF 為 127 行。`git diff --check` 與四份新增檔案的逐行
whitespace／EOF 檢查通過；新報告公式的一個行尾空格已修正。

沒有重跑已完成的唯一 degree-5 各表、no-spoke／single-spoke／two-spoke
分類、R 系列、雙拒絕 atlas、profiles／閉包、來源圖枚舉或 Lean axiom audit。
`lake build` 與文件檢查不表示新紙面證明已 Lean 化。

## 精確停止點

第一輪介面與 minimality 已完成。下一窄入口是由 root-edge 對角見證、
root-spoke 條帶和各 C 私有色對，限制**同一來源**在指定 p 下的完整關係，
先研究共鄰點分量與只接單 root 分量的互動。
相鄰雙 root 的全部分離、平面可實現性、非相鄰雙 root、degree≥6、
更多高 degree 點、一般單側／共同出口與 K∞=K≤5 仍未證。

## 同日 commit／push 接續

使用者其後要求 `commit + push`。本次發布包含 checker、JSON 證書、報告、
研究紀錄、README、HANDOFF、STATUS 與兩份 degree-5 導讀／介面後續通知，
共 9 檔。上文「未 commit／push」描述研究完成時的狀態。
研究來源與證書未再修改，沿用同一對話已通過的 task-specific `--check`
與 `lake build`；發布前重新檢查文件、DocGraph 及 staged whitespace。
提交訊息為 `Establish adjacent degree-five ordered-pair interfaces`。
實際發布結果以 Git 與本次回覆的 local／tracking／remote SHA 核對為準。
