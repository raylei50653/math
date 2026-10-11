# 2026-10-03：ε≥3 入口的雙 root 刪除與原邊接回

接手基準 `722bfa6`，工作區原先乾淨。使用者要求「推進 ε = 3」。
先讀 HANDOFF、STATUS、Kempe 導覽與 Git，沿用唯一 degree-6 的 ε=2
分支已全排之停止點，把本輪目標定為推進共同 ε≥3：核對雙 degree-5
roots 的完整 Σ 來源，而不把固定 q-core 出口當成來源排除。
本輪沒有 commit／push；成果見 [專題報告](../c5_excess_two_root_deletions.md)，
目前停止點由 [Kempe 導覽](../c5_kempe_guide.md) 維護。

## 任意大小必要化約與窄排除

所有推導保留同一原 G、有序 induced-C₅ disk 框、Σ=933／941 或整圖
D₅ 像、每條非框邊 Σ-critical、兩個完整 degree-5 roots z,w，及其他
有效內點完整 degree 四。原 degree-4 components、共鄰 contacts、
全部 boundary attachments、actual supports、ownership 與共享字面色框保留。

令 δ 表示 zw 是否原邊，m_r 是原 mixed 分量在 r 的總 incidences。
刪 w 的完整 Σ 等於原 unary-at-z 側 S_z 的完整 Σ，交換 roots 同理。
證明固定原 β 和另一 root 色，利用被刪原 contact 的嚴格 list slack
填入整份 mixed／unary-at-w，而不是獨立相乘兩端 marginals。
S_z 的 root degree 為 5−δ−m_z≤4；拒絕則飽和成原全 degree-4 core。
兩側若均拒絕，內部不交的四點實際支援違反同一 disk 環序的交錯路徑。
因此至少一個原刪 root 圖全收，另一個至多單缺失；全拒絕列至多一列
能有任何省略原 root 的 core。這不是一般的全體共同 root 結論。

相鄰且有 mixed 時，δ+m_z、δ+m_w≥2，兩個刪 root 圖均全收，
每份 minimal rejected-row core 都含兩 roots。若某份 core 的兩 roots
都仍 degree 五，則 core=G；不能把「保留兩 roots」改稱兩者仍 degree 五。
舊 no-mixed／單側出口的 q-minimality 不由完整 Σ minimality 自動提供。

相鄰 mixed 的 N=G−zw 有連通有效內部、全 degree 四。如果仍拒絕 q，
飽和使 N 本身就是 minimal q-core，完整 Σ 恰 Ω∖{q}。至少兩份原 mixed
在 N 形成長度至少四的簡單環，不符既有全 degree-4 分類，因此刪 zw 全收。
保留 zw 的雙 root-degree-four core 若仍有 mixed，只能保留一份，且
兩 root contacts 必同為原 {x}；整份 C 可有尾枝，未替換為 singleton。

N 若恰兩個 triangles，原分類直接給六內點、直接 bridge、無外掛樹的
實際圖，沒有縮減兩個 marked endpoints。重建全部 128 份保存的具名
disk 基底，實際 Σ histogram 為 1021:32、1022:64、959:32。對 64 份
q₄=01012 核心的每份八個原內部 nonedges 接回，共 512 份，全部仍
Σ=1022；故原 zw 違反 strict Σ minimality，這個分支排除。

## 固定證書及負控制

[新 checker](../../scripts/c5_excess_two_root_deletions.py) 和
[固定刪 root helper](../../scripts/c5_excess_two_root_deletion_controls.py)
生成 [證書](../../artifacts/c5_excess_two_root_deletions/observations.json)。
512 份接回的 5,120 次完整列查詢保留原 ordered (z,w) relation，
每個 tuple witness 指回同一原基底、同一列的完整染色。逐列與加原 zw
後的直接回溯比對；原全部 edges、附件、components、contacts 及 apex
rotation 保存。所有 512 份接回不限 disk 作放寬，沒有聲稱全部具有 disk 實現。

另核對全部 65,536 份四色二元完整 relations，包括空 relation，與
加入不等色邊的精確過濾公式。Diagonal 與 off-diagonal relation 的相同
marginals 會給空／非空接合，保存為抽象 relation 負控制，不冒稱實際來源。

三張固定 ε=2 圖有 60 次完整刪 root／unary 側等式及 400 份條件原分量
tuples，每次回溯另與 product-coloring 核對。它們不帶候選／disk／minimality
聲明。第三圖完整 Σ=958，兩份刪 root 圖分別 Σ=959、1022，各漏不同
singleton 列；兩 unary 側都碰全部五個框點且內部不交，交錯支援證其
不能是 disk。它具體說明全域「至多一份省略例外」需要 disk 前提。

任意大小的 slack、飽和、交錯支援及 block 分類由紙面與前序依賴承擔。
外部 degree-list／Gallai、原 topology／minor 證據沿用，未新增外部文獻結論
或 Lean theorem；`lake build` 通過不把本輪推導形式化。

## 本輪實際驗證

```bash
python3 scripts/c5_excess_two_root_deletions.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_root_deletions.py --check
python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

新增 checker 兩種 hashseed 及上述三份沿用 checker 均通過；
`lake build` 通過（8,831 jobs，既有 style／unused simp warnings）。
文件檢查通過（468 Markdown、4,839 local links）；DocGraph 通過
（62 documents、213 relations、5 families，0 errors／notes）；大型產物
完整性 `ok=117`，沒有 missing／changed／stale；`git diff --check` 通過。
獨立審閱另確認刪 root slack、原側飽和、全域例外的 disk 前提、
長度至少四的原環，以及六內點具名整圖接回的適用範圍。

證書為 4,451,048 bytes，依既有大型產物規則登錄 MANIFEST 與 generated
ignore 區塊，原 116 份紀錄保留。README 更新 excess 接手入口，STATUS
新增報告與歷史直接索引，Kempe 導覽更新窄停止點，前序 t=0 報告加後續
說明。HANDOFF 的研究線與進行中標記未改，遵守薄索引治理。

未重跑前序唯一 degree-6 全批、no-mixed 共同行為全批、source catalogue、
全部 degree-4／Gallai 控制或 Lean axiom audit；本輪未新增圖 catalogue。
單 triangle canonical bases 的未保存探針不列成果，也不從未保留 z,w
的 tail 化約外推全部接回。

## 接手摘要

```text
工作目錄 /home/ray/developer/ai/math；接手基準722bfa6，本輪未commit/push。
先讀docs/HANDOFF.md、docs/STATUS.md、docs/c5_kempe_guide.md，再讀
docs/c5_excess_two_root_deletions.md；查即時git status。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk，若ε=2只剩雙degree5。
新結果：Σ(G−w)=Σ(原unary-at-z側)，反向同理；至少一份刪root全收，
另一份至多單缺失。全部拒絕列至多一列有任何省略root的core。
相鄰mixed兩個刪root均全收。至少兩mixed迫Σ(G−zw)=Ω。
若G−zw仍拒絕，它本身是全degree4 minimal core；雙triangle原六點分支
64個具名基底×8條原nonedges的512份接回全Σ1022，違反strictΣ minimality。
重播python3 scripts/c5_excess_two_root_deletions.py --check，另hashseed17。
停止於紙面+Python；共同ε≥2仍未提高為ε≥3，未新增Lean theorem。
下一窄題：相鄰、恰一mixed、Σ(G−zw)≠Ω，原degree4樹（偶數頂點路徑）。
保存z,w原路徑位置、完整ordered色對、原附件與共同色框，再分析原zw接回。
既有run/tail relation縮減不保存被刪markers；不可偷推接回後Σ。
單triangle、刪zw全收、no-mixed、非相鄰roots仍保留。
```
