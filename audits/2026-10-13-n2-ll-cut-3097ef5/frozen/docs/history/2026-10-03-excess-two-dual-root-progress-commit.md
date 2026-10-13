# 2026-10-03：ε=2 雙 degree-5 root 九輪進展整理與提交

使用者要求「整理目前進展並 commit，過程中有發現可以記錄」。
接手基準 `722bfa6`，工作目錄 `/home/ray/developer/ai/math`；工作區
包含九輪尚未提交的 checker、報告、研究紀錄與大型產物登錄。
本次核對完整證據包，壓縮 Kempe 導覽的逐輪敘述，同步全線整合頁，
補上後續涵蓋關係與本紀錄，再作本地 commit。提交 SHA 以即時 Git
為準；使用者只要求 commit，本次沒有 push。

## 完成範圍與證據層

共同前提為固定完整 Σ=933／941 或整圖 D₅ 像、每條非框邊刪除
都嚴格擴大 Σ、指定有序 induced-C₅ disk 外框、ε=2。前序已排除
唯一 degree-6 分支，因此本批恰兩個完整 degree-5 roots，其餘有效
內點完整 degree 四。各窄結果另按報告要求相鄰、存在 mixed 或恰
一份原 mixed。原 H−{z,w} 分量、全部原邊、有序 contacts、實際
attachments／supports、ownership、嵌入環序與同一字面色框保持。

| 報告 | 本批完成範圍與固定核對 |
| --- | --- |
| [原 root 刪除](../c5_excess_two_root_deletions.md) | 至少一個刪 root 圖全收，另一個至多缺一列；相鄰 mixed 兩者均全收。64 原雙 triangle 核心／512 接回、400 條件分量 relations、60 刪 root 等式 |
| [原路徑接回 zw](../c5_excess_two_path_edge.md) | 原樹／偶數路徑由共同原框鄰點及原環給 apex K₅；14 固定原路徑／226 接回與 minor、2,260 完整色對查詢 |
| [單 triangle 接回](../c5_excess_two_triangle_edge.md) | 保留原 z,w 的 528 必要正常形，392 T4 全收者仍只有原單缺失；280 同枝 K₅。連同前序完成相鄰 mixed 的 Σ(G−zw)=Ω |
| [原省略身份與雙 spoke](../c5_excess_two_mixed_core_spokes.md) | 196 incidence 配置／7,442 子集核對 proper core 原身份；126 必要正常形／6,068 雙 spoke 接回全無兩候選像 |
| [spoke＋原 unary](../c5_excess_two_mixed_core_spoke_unary.md) | 37,320 目標比較；89,088 同一原支援 transport 比較及 2,640 明示收縮星 subdivisions 全排，含 root 交換 |
| [兩側原 unary](../c5_excess_two_mixed_core_two_unary.md) | 5,700 目標比較；2,184,192 必要支援對比較，386,048 互異查詢保存 proofs／assignments；3,180 雙收縮星 subdivisions 全排 |
| [省略原 mixed](../c5_excess_two_mixed_omission.md) | 344 保留原 roots 的必要核心／3,440 目標比較；9,152 固定支援比較，8,508 跨列衝突，其餘 644 由 188 subdivisions 全排。完成相鄰唯一 mixed 的所有 (4,4) q-core 身份 |
| [單 spoke 原附件化約](../c5_excess_two_mixed_core_single_spoke.md) | 省略圖若拒絕，自己是唯一 degree-5 minimal q-core；666 骨架／58 subdivisions，當輪上界為 933≤4、941≤5，留下四組941附件及 root 交換 |
| [原 leaf 色纖維](../c5_excess_two_mixed_core_leaf_fibers.md) | 相鄰唯一 mixed 分支的八份附件一次整圖搬運到998／1004；完整 (b,a,y,u) joint、同一 unary 雙列 palette 與原圖 K₅ 全排五-spoke 型。450 全圖 joins／7,200 pinned 纖維及24 extracted K₅ 控制；該分支的兩候選總 spokes 都≤4 |

**共同下界仍是 ε≥2，ε≥3 未證。** 任意大小來源化約、外部
degree-list／Gallai 依賴、原 block palettes、實際 tethers、Jordan
及 minor 論證由紙面與報告明列依賴承擔。Python 核對固定必要域、
完整 tuple witnesses／空纖維與具名 minor 邊集；沒有證明抽象
profiles 的 disk 實現。沒有新增 Lean theorem，`lake build` 不將
本批紙面 topology 形式化。一般出口與 K∞=K≤5 仍未證。

## 整理時保留的發現

1. **Σ-critical 與單列 minimality 必須分開。** 原 G 的每條非框邊
   都改變完整 Σ，不保證 G 是任何指定拒絕列的 minimal core。
   (4,4) 全排之後，單 spoke 省略若仍拒絕才迫省略圖自己成為唯一
   degree-5 minimal q-core；原 G 自己為 (5,5) q-core 仍未排除。
2. **有原圖 witnesses 的 marginal 負控制。** 省略 mixed 的 form
   224、row 4 有 core `K={(3,1)}`，原 shared singleton 的完整
   `T_C={(1,1),(3,3)}`。兩 endpoint marginals 都是 `{1,3}`，
   相乘會誤造 contact tuple `(1,3)`，看似能接回原 root 色對；
   實際完整 joint 為空。這份固定控制不帶 disk／Σ-minimal／候選
   實現聲明；不能用 marginals 代替原二接點 relation。
3. **disk 前提有具體負控制。** 原 root 刪除 helper 的第三張固定圖
   有 Σ=958、Σ(G−z)=959、Σ(G−w)=1022，兩側各缺不同 singleton。
   兩原 unary 支援均為五框點，原交錯路徑排除 disk。原 leaf 控制
   也有三張同一 U 在兩列都只取0的實際圖，但各有原圖 K₅；它們
   不反駁明列 disk 前提的排除。
4. **雙列 palette 比較需要同一原 U。** 五-spoke 排除依賴同一
   block incidence 對0／3 membership 的守恆，再沿原 bridges 抽出
   實際 tethers。逐列獨立選禁色不能代替這一步。收縮星只用於
   拓撲 minor，不宣稱保存原染色 relation 或 Σ。
5. **下一入口只是 (3,1) 的選定子型。** 三-spoke 側用掉三條原
   spokes 和 zw，原 mixed incidence 只能是一；一-spoke 側剩三份
   incidence。由這個原 degree 預算可列下表，但沒有新 disk 實現
   或整型排除結論。

| 原 mixed incidence | 一-spoke 側原 unary contacts 分拆 | 本次定位 |
| --- | --- | --- |
| (1,1) | (1,1)：兩份單接點 unary | 選定的下一窄入口 |
| (1,1) | (2)：一份 binary unary | 保留 |
| (1,2) | (1)：一份單接點 unary | 保留 |
| (1,3) | 空：無 unary | 保留 |

上述各型含 root 交換。表只按同一原圖 incidence 分拆，不能獨立
正規化原分量，也不能把「選定子型」讀成全部 (3,1) 已分類實現。

## 本次實際重播與提交產物

九份新 checker 均在 `PYTHONHASHSEED=17`、NetworkX 3.5 的 pinned
環境下以 `--check` 通過，逐 byte 比對既存 observations，沒有重建
或覆寫產物。較早四份不需要 NetworkX，也可使用報告列的 python3。

```bash
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_root_deletions.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_path_edge.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_triangle_edge.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spokes.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings。大型產物 `ok=125`，無 missing／changed／stale。
本批九份 observations 共 **493,240,631 bytes**，均依既有政策放在
本地、由 `.gitignore` 排除；Git 提交其 producer、依賴 helper、
MANIFEST 的 bytes／SHA256／fingerprints／依賴順序，以及報告、
研究紀錄與入口。保留舊 single-spoke 的 [4,5] 當輪證書，新 leaf
證書承擔後續 [4,4]，沒有改寫歷史結果。

文件檢查通過 **485 份 Markdown／4,977 個本地連結**，anchors、
index、HANDOFF 全通過；DocGraph 通過 **62 documents／213 relations／
5 families**，零 errors／notes；`git diff --check` 通過。

本次未重跑各份歷史紀錄的預設 hashseed、全部前序唯一 degree-6
省略／分拆、全 degree-4 分類及 Gallai 有限證書、歷史 catalogue、
weak-deletion／Kempe closure、R-series 或 Lean axiom audit；按原
報告範圍沿用。三份平行唯讀審閱核對九輪前提、數字、source hashes
與同源 relation，未代替 checker 或紙面證明。

README、STATUS、Kempe 導覽、全線整合頁與舊報告後續連結同步。
HANDOFF 的研究線及進行中標記維持，依治理保留薄索引；各輪歷史
中的「未 commit／push」保留當輪語境，本紀錄承擔此次提交狀態。

## 停止點與貼用摘要

即時停止點由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)
維護；本次沒有啟動四-spoke 新搜尋。

```text
工作目錄 /home/ray/developer/ai/math；先讀 docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md 與本整理紀錄，再查即時 Git。九輪雙root bundle
已作本地commit；未push。933/941固定完整Σ、edge-minimal induced-C5 disk
已證ε≥2，唯一degree6的ε=2全排；雙degree5的相鄰mixed刪roots／zw全收。
相鄰唯一mixed的全部(4,4) q-core及五spoke原來源全排，兩候選總spokes≤4。
單spoke／unary省略、原(5,5) q-core及其他雙root來源保留，ε≥3未證。
下一窄入口：四spoke(3,1)+root交換，先取mixed(1,1)+兩單unary子型；
保留原leaf、C、兩unary、實際附件及完整joint色纖維，接回同色原spoke。
同(3,1)的另三份incidence分拆、其他四spoke／較少spokes、多mixed、
no-mixed及非相鄰roots均保留。停止於可證窄排除或具名必要殘留。
九份hashseed17 --check、lake build、artifact及文件檢查通過。
紙面+Python，未新增Lean theorem；一般出口及K∞=K≤5未證，不重開圖枚舉。
```
