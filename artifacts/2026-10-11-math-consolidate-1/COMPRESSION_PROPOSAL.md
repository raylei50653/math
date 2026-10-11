# MATH-CONSOLIDATE-1：Compression proposal

固定HEAD：`8c56b76922a1c7ac4c011096f2041b49c4a67cc8`。**本輪只交提案，既有文件實際減少0；沒有覆寫canonical。**

## 結論與兩個分開的提案

**A：保守引用精簡。** 下列9段具體替換以現存原audit／review為引用目標；完整branch合同、量詞、source身份、OPEN、更正／信任界都保留。全部原canonical的99個不同Markdown連結目標仍在preview；R1把36個原入口組成緊湊表而不丟正式採納來源。此方案不需要新增production共同lemma檔。

**B：數學證明組織。** [COMMON_LEMMAS](COMMON_LEMMAS.md)提出12個局部interface記錄與GA導入，配每端點的actual-graph應用表。可減少重做接合／恢復／slack／degree-cover／palette-incidence／LD的證明；必須先review這些精確陳述及branch mapping，再另授權文件重構。若新建共同lemma production檔，新增全文成本須加入，不能直接沿用A的淨節省。

Canonical已是權威索引，原source proofs大多在frozen audits。本輪不建議刪任何原定理或原witness；可做的是縮短證明路線、集中共用介面和減少重複敘述。

## 可重算的before／after

| 分母／項目 | before | A preview after | 本輪實際 after | 解讀 |
| --- | ---: | ---: | ---: | --- |
| 焦點端點定理 | 13 | 13 | 13 | 不合併不同來源合同 |
| 前置+SD subset排除記錄 | 7 | 7 | 7 | 本inventory總20筆；scope保持 |
| 合成corollaries | 4 | 4 | 4 | 與端點分開，不升格全域closure |
| canonical §2索引bundle rows | 33 | 33 | 33 | slash labels不是獨立定理數 |
| 新採納helper／Lean／完整OPEN關閉 | 0 | 0 | 0 | 新索引名稱不是採納 |
| family投影nodes | 77 | 77 | 77 | 計數圖見DAG ledger；不是全repo定理數 |
| 選定最短路線的依賴edges | 183 | 183 | 183 | 實際前提與外部trust不刪 |
| 主文alternative route edges | 3 | 0 | 3（原文未改） | 1c兩條獨立機制、HIGH1 supporting MAP移成引用；含alternatives的呈現為186→183 |
| canonical全文行數 | 800 | 763 | 800 | preview減37，4.6% |
| canonical UTF-8 bytes | 71,077 | 69,804 | 71,077 | preview減1,273，1.8% |
| canonical Unicode code points | 44,777 | 44,175 | 44,777 | preview減602，1.3%；不是中文分詞數 |
| prose-like paragraphs | 76 | 77 | 76 | 依下面精確正則；不是任意Markdown paragraph語義 |
| whitespace-normalized exact duplicate paragraph excess | 0 | 0 | 0 | **沒有逐字重複段落可直接delete** |
| 選取的重疊／分類敘述區段 | 9 | 9個短引用／精簡區段 | 9個原區段 | 是人工比對的semantic motif，非9個逐字duplicate |
| 原canonical不同Markdown link targets | 99 | 99全部保留（可另加） | 99 | 導航成本未冒充被刪前提 |
| 四份BR frozen PROOF | 693行 | 693行 | 693行 | freeze：0減少，0搬移 |
| canonical LONG §2.9/2.10 | 74行／6,005 bytes | 同樣74行／6,005 bytes | 同樣74行／6,005 bytes | A沒有改LONG文字；B僅列可共用機制 |

family edge分母是本輪建出的兩種呈現投影；不是宣稱repo先前已有一份186-edge機器proof DAG。它不計歷史工具依賴，也不將每個block/pin展成新lemma。必要DAG已獨立檢查無環；細粒度61 LONG labels另有原記錄對照。

## 重複判定與實際減少／單純搬移

| 項目 | 性質 | 可安全處置 | 計數誠實性 |
| --- | --- | --- | --- |
| LOW1/LOW2/HIGH1/HIGH2的assignment接合／filter | 同一操作，actual分量和contacts不同 | 原合同不动，引用原完整JOIN/RESTORE；B可引用C1/C2加映射 | A省的是重複證明摘要，actual application四支仍留 |
| BR重述合同1–3、5 | 同一source macro、分支4不同 | R6/R7引用完整1a合同，明說只替換4；1g完整八项原文不改 | 条件移动至同頁既有合同引用；邏輯前提沒有減少 |
| BR原M list/degree/Gallai步驟 | 同一方法、Z精度有歷次更正 | R8保原M formula與full-Z乘積並引用1g原PROOF；B可共同LD+GA | source-specific原witness/J2 barrier仍在 |
| 1c三條路線 | 共用末端lemma已覆蓋全部合法接點 | R9保degree篩查、完整terminal與原負控制；另兩route引用 | 是真正縮短主證明分類；原分類／proof bytes未删 |
| HIGH1-MAP與最終G-lift | supporting兼容性結論 vs主排除 | 最終路線不必走完整MAP；原MAP statement／proof留source | 降低reader必走的route數，不刪已採命題 |
| 原proof/controls搬至「共同文件」 | frozen歷史證據 | 不做 | 搬移或複製不計為研究內容減少 |
| 六份本輪synthesis | 新交付索引／展開合同／提案 | 留本目錄供審查 | 會增加repo文件量；不把這個增量隱藏在canonical節省數 |

A假設未來只套下列替換、引用已有source，則既有文本集合的byte減少是1,273。若連本輪六份提案一起計入，現況是純新增，沒有淨縮短。B若新建production lemma檔，淨變化為`刪除的重複原文bytes − 新lemma全文bytes − 新映射／引用bytes`；本輪未選定production路徑或完成該重構，**不填假估值**。

## 九段具體替換（只供審查）

全部行號與sha相對固定HEAD。區段彼此不重疊，使用原行號由後向前替換。下列文字就是preview用的完整replacement，不是概略建議。

### R1：原12–46行

原來源鏈壓成表；保全部入口與量詞finding。原35行／2538 bytes，replacement 14行／2557 bytes。

```markdown
既有交付、獨立審查、封存與正式採納入口如下；每支完整合同、證明及finding見§2／4。

| 批次 | 原來源／稽核／採納 |
| --- | --- |
| S/U | [U 原交付](../audits/2026-10-09-n45-u/REPORT.md)、[SU-A](../audits/2026-10-09-n45-su-a/REPORT.md)、[SU-J](../audits/2026-10-09-n45-su-j/REPORT.md)、[監督採納](../audits/2026-10-09-n45-su-supervision/REPORT.md) |
| PG/PR/PC | [PG](../audits/2026-10-09-n45-pg/REPORT.md)、[PR](../audits/2026-10-09-n45-pr/REPORT.md)、[PC](../audits/2026-10-09-n45-pc/REPORT.md)、[PGA 幾何稽核](../audits/2026-10-10-n45-pga/REPORT.md)、[PA 紙面稽核](../audits/2026-10-10-n45-pa/REPORT.md)、[PCA 工具稽核](../audits/2026-10-10-n45-pca/REPORT.md)、[本輪監督採納](../audits/2026-10-10-n45-p-supervision/REPORT.md) |
| SS | [SS](../audits/2026-10-10-n45-u-ss/REPORT.md)、[SSA 紙面與覆蓋稽核](../audits/2026-10-10-n45-ssa/REPORT.md)、[SSG 幾何／改色](../audits/2026-10-10-n45-ssg/REPORT.md)、[SSC 封存稽核](../audits/2026-10-10-n45-ssc/REPORT.md)、[SS 監督採納](../audits/2026-10-10-n45-ss-supervision/REPORT.md) |
| LOW1 | [LOW1](../audits/2026-10-10-n45-s-low1/REPORT.md)、[L1A 紙面](../audits/2026-10-10-n45-l1a/REPORT.md)、[L1R 原圖與完整關係](../audits/2026-10-10-n45-l1r/REPORT.md)、[L1C 封存](../audits/2026-10-10-n45-l1c/REPORT.md)、[LOW1 監督採納](../audits/2026-10-10-n45-low1-supervision/REPORT.md) |
| LOW2 | [LOW2](../audits/2026-10-10-n45-s-low2/REPORT.md)、[L2A 紙面與覆蓋](../audits/2026-10-10-n45-l2a/REPORT.md)、[L2R 原圖與完整關係](../audits/2026-10-10-n45-l2r/REPORT.md)、[L2C 封存](../audits/2026-10-10-n45-l2c/REPORT.md)、[LOW2 監督採納](../audits/2026-10-10-n45-low2-supervision/REPORT.md) |
| HIGH1 | [HIGH1](../audits/2026-10-10-n45-s-high1/REPORT.md)、[H1A 紙面](../audits/2026-10-10-n45-h1a/REPORT.md)、[H1R 原圖與完整關係](../audits/2026-10-10-n45-h1r/REPORT.md)、[H1C 封存](../audits/2026-10-10-n45-h1c/REPORT.md)、[HIGH1 監督採納](../audits/2026-10-10-n45-high1-supervision/REPORT.md) |
| HIGH2 | [HIGH2](../audits/2026-10-10-n45-s-high2/REPORT.md)、[H2A 紙面／覆蓋](../audits/2026-10-10-n45-h2a/REPORT.md)、[H2R 原圖／完整 lifts](../audits/2026-10-10-n45-h2r/REPORT.md)、[H2C 工具／封存](../audits/2026-10-10-n45-h2c/REPORT.md)、[HIGH2／HIGH3 監督驗收](../audits/2026-10-10-n45-high23-supervision/REPORT.md) |
| HIGH3 |  |

HIGH2未用色恢復只採proper三色γ；原過寬量詞finding與各原worker／封存bytes保留。
```

### R2：原197–201行

LOW1 actual sole-C、完整join及原filter引用。原5行／547 bytes，replacement 3行／344 bytes。

```markdown
H_X=H_G；r完整degree4、s完整degree5；C=H_X−s={r}∪U∪P∪Q是實際sole C，三個原s-contacts互異。
[LOW1完整接合](../audits/2026-10-10-n45-s-low1/REPORT.md)給全literal γ／全pins的restriction–union雙射，
保同一r坐標、shared單坐標、全部assignments及空fibres；原G只加r≠γ(b_i)的spoke filter。
```

### R3：原223–227行

LOW2雙contacts/原cycle及full fibres保留。原5行／509 bytes，replacement 3行／342 bytes。

```markdown
r在X／C完整degree4且無框或s鄰，s完整degree5；C={r}∪U∪P∪Q是實際sole C，U原cycle全留。
[LOW2完整接合](../audits/2026-10-10-n45-s-low2/REPORT.md)在同一r色下同時施加兩U-contact限制，
保全literal γ／全pins、shared單坐標、全部assignments及空fibres；原G只加r≠γ(b_i)的spoke filter。
```

### R4：原258–261行

HIGH1接合與MAP/最後G-lift分清。原4行／408 bytes，replacement 4行／413 bytes。

```markdown
H_X−s的實際分量是C={r}∪P∪Q與U，contacts=(2,1)。
[HIGH1完整接合](../audits/2026-10-10-n45-s-high1/REPORT.md)保全literal γ／全pins、r色／空fibres與isolated factors，
恢復G只加r≠γ(b_i)；X自身minimality／slack給private cover，局部N-diagonal給F_C={β(b_j)}、F_U={D}。
BASE (2,1)指定列延拓只屬X；原G排除另由下列K₃,₃／ARC／三色G-lift路線承擔。
```

### R5：原290–292行

HIGH2 all-proper γ join/filter保留。原3行／284 bytes，replacement 3行／281 bytes。

```markdown
H_X−s的實際分量是C={r}∪P∪Q與U，contacts=(2,2)。
[HIGH2完整接合](../audits/2026-10-10-n45-s-high2/REPORT.md)保全部proper γ、全pins、r色及空fibres；G只加r≠γ(b_i)。
X自身minimality／incident-edge witnesses及N-diagonal給C/U禁色角色(1,2)。
```

### R6：原497–500行

1c只因式分解1a合同1–3、5；下一個三odd-block bullet完整留下。原4行／426 bytes，replacement 3行／342 bytes。

```markdown
- 完整沿用 BR-SD-1a 合同1–3、5，逐項保同一原G、完整Σ／ε／degrees及G witnesses、原U=0／L long／S actual pair、
  exact-S的X=M=G−e、自身同一proper三色β的拒絕／minimality／retained-edge witnesses與全部原資料。
  只替換下列合同4，不從G繼承X minimality，不改proper三色量詞。
```

### R9：原515–520行

1c全合法接點直接terminal，兩獨立機制引用。原6行／519 bytes，replacement 2行／271 bytes。

```markdown
原完整degree先排非法接點；其餘所有接點均保下列未改J3／q-arm的terminal前提，直接矛盾。
原[PROOF§4–5](../audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md)的雙witness／J2 routing保留為獨立機制，不列為本支最短必要依賴。
```

### R7：原555–560行

1e同source合同引用，保其獨立branch4及W ownership。原6行／613 bytes，replacement 3行／341 bytes。

```markdown
- 完整沿用 BR-SD-1a 合同1–3、5（含同一原G、完整Σ／ε／degrees／G witnesses、原U=0／L long／S actual pair、
  exact-S的X=M=G−e、自身同一proper三色β的拒絕／minimality／retained-edge witnesses、原p/q及三s-spokes）。
  只替換下列合同4，不從G繼承X minimality；全部原資料照留。
```

### R8：原652–660行

1g原list formula/full ignored product保留，引用完整證明。原9行／837 bytes，replacement 5行／517 bytes。

```markdown
**採納的紙面推論：** 同一β的未用色D與pair外第三已用色T保持原字面身份。
[1g PROOF§2](../audits/2026-10-11-br-sd-1g-dbdc4c35/PROOF.md)的原M lists
`L^D(y)=Col∖(β(A(y))∪{D:sy∈E(M)})`有degree下界；完整lift含effective-H外原允許色乘積。
M拒β故C不可著色，經[外部Gallai刻畫](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)得incident-disjoint palettes；
只投影省略原座標不宣稱bijection。以下J2屏障仍使用全部incident palettes。
```

## 機械重建／核對

下面JSON是完整replacement集合。可讀取本提案的JSON fence，驗sha並在**記憶體**重建preview；不寫canonical、不跑歷史audit工具。

```json
{
  "source": "docs/c5_excess_two_nonadjacent_unit_core45.md",
  "sha256": "ec80d3f0b053d6c7776b9b7fc0fdfa8432e0e4aef69feb052d3b69e53aa76be8",
  "replacements": [
    {
      "id": "R1",
      "start": 12,
      "end": 46,
      "replacement": "既有交付、獨立審查、封存與正式採納入口如下；每支完整合同、證明及finding見§2／4。\n\n| 批次 | 原來源／稽核／採納 |\n| --- | --- |\n| S/U | [U 原交付](../audits/2026-10-09-n45-u/REPORT.md)、[SU-A](../audits/2026-10-09-n45-su-a/REPORT.md)、[SU-J](../audits/2026-10-09-n45-su-j/REPORT.md)、[監督採納](../audits/2026-10-09-n45-su-supervision/REPORT.md) |\n| PG/PR/PC | [PG](../audits/2026-10-09-n45-pg/REPORT.md)、[PR](../audits/2026-10-09-n45-pr/REPORT.md)、[PC](../audits/2026-10-09-n45-pc/REPORT.md)、[PGA 幾何稽核](../audits/2026-10-10-n45-pga/REPORT.md)、[PA 紙面稽核](../audits/2026-10-10-n45-pa/REPORT.md)、[PCA 工具稽核](../audits/2026-10-10-n45-pca/REPORT.md)、[本輪監督採納](../audits/2026-10-10-n45-p-supervision/REPORT.md) |\n| SS | [SS](../audits/2026-10-10-n45-u-ss/REPORT.md)、[SSA 紙面與覆蓋稽核](../audits/2026-10-10-n45-ssa/REPORT.md)、[SSG 幾何／改色](../audits/2026-10-10-n45-ssg/REPORT.md)、[SSC 封存稽核](../audits/2026-10-10-n45-ssc/REPORT.md)、[SS 監督採納](../audits/2026-10-10-n45-ss-supervision/REPORT.md) |\n| LOW1 | [LOW1](../audits/2026-10-10-n45-s-low1/REPORT.md)、[L1A 紙面](../audits/2026-10-10-n45-l1a/REPORT.md)、[L1R 原圖與完整關係](../audits/2026-10-10-n45-l1r/REPORT.md)、[L1C 封存](../audits/2026-10-10-n45-l1c/REPORT.md)、[LOW1 監督採納](../audits/2026-10-10-n45-low1-supervision/REPORT.md) |\n| LOW2 | [LOW2](../audits/2026-10-10-n45-s-low2/REPORT.md)、[L2A 紙面與覆蓋](../audits/2026-10-10-n45-l2a/REPORT.md)、[L2R 原圖與完整關係](../audits/2026-10-10-n45-l2r/REPORT.md)、[L2C 封存](../audits/2026-10-10-n45-l2c/REPORT.md)、[LOW2 監督採納](../audits/2026-10-10-n45-low2-supervision/REPORT.md) |\n| HIGH1 | [HIGH1](../audits/2026-10-10-n45-s-high1/REPORT.md)、[H1A 紙面](../audits/2026-10-10-n45-h1a/REPORT.md)、[H1R 原圖與完整關係](../audits/2026-10-10-n45-h1r/REPORT.md)、[H1C 封存](../audits/2026-10-10-n45-h1c/REPORT.md)、[HIGH1 監督採納](../audits/2026-10-10-n45-high1-supervision/REPORT.md) |\n| HIGH2 | [HIGH2](../audits/2026-10-10-n45-s-high2/REPORT.md)、[H2A 紙面／覆蓋](../audits/2026-10-10-n45-h2a/REPORT.md)、[H2R 原圖／完整 lifts](../audits/2026-10-10-n45-h2r/REPORT.md)、[H2C 工具／封存](../audits/2026-10-10-n45-h2c/REPORT.md)、[HIGH2／HIGH3 監督驗收](../audits/2026-10-10-n45-high23-supervision/REPORT.md) |\n| HIGH3 |  |\n\nHIGH2未用色恢復只採proper三色γ；原過寬量詞finding與各原worker／封存bytes保留。\n"
    },
    {
      "id": "R2",
      "start": 197,
      "end": 201,
      "replacement": "H_X=H_G；r完整degree4、s完整degree5；C=H_X−s={r}∪U∪P∪Q是實際sole C，三個原s-contacts互異。\n[LOW1完整接合](../audits/2026-10-10-n45-s-low1/REPORT.md)給全literal γ／全pins的restriction–union雙射，\n保同一r坐標、shared單坐標、全部assignments及空fibres；原G只加r≠γ(b_i)的spoke filter。\n"
    },
    {
      "id": "R3",
      "start": 223,
      "end": 227,
      "replacement": "r在X／C完整degree4且無框或s鄰，s完整degree5；C={r}∪U∪P∪Q是實際sole C，U原cycle全留。\n[LOW2完整接合](../audits/2026-10-10-n45-s-low2/REPORT.md)在同一r色下同時施加兩U-contact限制，\n保全literal γ／全pins、shared單坐標、全部assignments及空fibres；原G只加r≠γ(b_i)的spoke filter。\n"
    },
    {
      "id": "R4",
      "start": 258,
      "end": 261,
      "replacement": "H_X−s的實際分量是C={r}∪P∪Q與U，contacts=(2,1)。\n[HIGH1完整接合](../audits/2026-10-10-n45-s-high1/REPORT.md)保全literal γ／全pins、r色／空fibres與isolated factors，\n恢復G只加r≠γ(b_i)；X自身minimality／slack給private cover，局部N-diagonal給F_C={β(b_j)}、F_U={D}。\nBASE (2,1)指定列延拓只屬X；原G排除另由下列K₃,₃／ARC／三色G-lift路線承擔。\n"
    },
    {
      "id": "R5",
      "start": 290,
      "end": 292,
      "replacement": "H_X−s的實際分量是C={r}∪P∪Q與U，contacts=(2,2)。\n[HIGH2完整接合](../audits/2026-10-10-n45-s-high2/REPORT.md)保全部proper γ、全pins、r色及空fibres；G只加r≠γ(b_i)。\nX自身minimality／incident-edge witnesses及N-diagonal給C/U禁色角色(1,2)。\n"
    },
    {
      "id": "R6",
      "start": 497,
      "end": 500,
      "replacement": "- 完整沿用 BR-SD-1a 合同1–3、5，逐項保同一原G、完整Σ／ε／degrees及G witnesses、原U=0／L long／S actual pair、\n  exact-S的X=M=G−e、自身同一proper三色β的拒絕／minimality／retained-edge witnesses與全部原資料。\n  只替換下列合同4，不從G繼承X minimality，不改proper三色量詞。\n"
    },
    {
      "id": "R7",
      "start": 555,
      "end": 560,
      "replacement": "- 完整沿用 BR-SD-1a 合同1–3、5（含同一原G、完整Σ／ε／degrees／G witnesses、原U=0／L long／S actual pair、\n  exact-S的X=M=G−e、自身同一proper三色β的拒絕／minimality／retained-edge witnesses、原p/q及三s-spokes）。\n  只替換下列合同4，不從G繼承X minimality；全部原資料照留。\n"
    },
    {
      "id": "R8",
      "start": 652,
      "end": 660,
      "replacement": "**採納的紙面推論：** 同一β的未用色D與pair外第三已用色T保持原字面身份。\n[1g PROOF§2](../audits/2026-10-11-br-sd-1g-dbdc4c35/PROOF.md)的原M lists\n`L^D(y)=Col∖(β(A(y))∪{D:sy∈E(M)})`有degree下界；完整lift含effective-H外原允許色乘積。\nM拒β故C不可著色，經[外部Gallai刻畫](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)得incident-disjoint palettes；\n只投影省略原座標不宣稱bijection。以下J2屏障仍使用全部incident palettes。\n"
    },
    {
      "id": "R9",
      "start": 515,
      "end": 520,
      "replacement": "原完整degree先排非法接點；其餘所有接點均保下列未改J3／q-arm的terminal前提，直接矛盾。\n原[PROOF§4–5](../audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md)的雙witness／J2 routing保留為獨立機制，不列為本支最短必要依賴。\n"
    }
  ]
}
```

```python
from pathlib import Path
import re, json, hashlib
from collections import Counter
proposal = Path('artifacts/2026-10-11-math-consolidate-1/COMPRESSION_PROPOSAL.md').read_text()
data = json.loads(re.search(r'```json\n(.*?)\n```', proposal, re.S)[1])
source = Path(data['source']).read_text()
assert hashlib.sha256(source.encode()).hexdigest() == data['sha256']
lines = source.splitlines(keepends=True)
spans = sorted(data['replacements'], key=lambda x: x['start'])
assert all(x['end'] < y['start'] for x,y in zip(spans,spans[1:]))
preview = lines[:]
for r in reversed(spans):
    preview[r['start']-1:r['end']] = [r['replacement']]
preview = ''.join(preview)
metric = lambda s: (len(s.splitlines()), len(s.encode()), len(s))
assert metric(source) == (800,71077,44777)
assert metric(preview) == (763, 69804, 44175)
urls = lambda s: set(re.findall(r'\[[^\]]+\]\(([^)]+)\)',s))
assert urls(source) <= urls(preview)
def prose_like(s):
    ps=[re.sub(r'\s+',' ',p.strip()) for p in re.split(r'\n\s*\n',s)
        if p.strip() and not p.lstrip().startswith(
        ('#','|','- ','1.','2.','3.','4.','5.','6.','7.','8.','```'))]
    counts=Counter(ps)
    return len(ps),sum(n-1 for n in counts.values() if n>1)
print('source',metric(source),prose_like(source))
print('preview',metric(preview),prose_like(preview))
```

## 四類審查決策

**可安全精簡：** A的九段；C1/C2/C3/C4已審機制與各自完整graph應用、BR LD/GA、1c原TERM短路線。通過review之後仍須另授權寫canonical。

**需要新證明：** 一般可恢復Δ-fibre非空、跨接口或多接點W、完整多W/source分類、失actual pair後TERM/PB、撤U或任意minimality繼承。1a/1e private-D不使用pair的局部步驟已知；更弱source註冊需要scope/adoption review，不能自行改既有定理合同。

**不可合併：** 13個端點與各原合同；LOW/HIGH/LONG的不同contacts／owners、BR不同W配置、β／source／G/X身份、三個BASE active分類與原hub供給。

**仍OPEN：** 完整N45-S-NOU-LS-PAIR、未涵蓋split22或其他splits、未覆蓋多旁支及Gallai接線、R31、其他cores／原55、一般N2/E/ε≥3及主命題；不把subset排除記成父closure。一般restorable fibre非空OPEN，完整K_LONG下Δ非空已證。
