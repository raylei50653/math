# 四項突破提案的分別驗證

2026-10-29，核對基線 `4476049`。本次驗證四個具體主張，保留
[精確消元主契約](4ct_guide.md#精確消元主線的研究契約)及
[LOCK-NO-GAIN](ck_d_lock_comparison.md)的適用範圍。

| 提案 | 驗證裁決 | 完整來源 |
| --- | --- | --- |
| 七邊割排除 | 紙證成立：全體頂點最小裸平面反例的非平凡邊割至少八。2,520 對雙側一步篩選零存活。原文一項分量斷言過強，但弱化後足以完成證明。 | [七邊割驗證](four_color_seven_cut_verification.md) |
| 兩步瓶頸與 triangle anchor | 瓶頸成立，須在同一指派保留 Group A；原 anchored 表示沒有漏約束。triangle 的 t=2 成立；維度界限只適用於指定原邊來源。四元表拒 24/256，非 12。 | [兩步消元驗證](four_color_two_step_verification.md) |
| Canonical shelling | 可指定反向 canonical ordering，保持剩餘圖單一簡單外環；完整關係遞推成立。圓盤指處理區域，非已消去點的誘導圖；環長可任意大，非空不變量仍缺。 | [剝殼驗證](four_color_shelling_verification.md) |
| 計數錐與跨 split 手術 | 單純非負邊際與 D 等價；即使補成標準 B5 錐，932 仍有十個整數權重的可行證書。手術須完整切開接口，三份邊界 pairing 不足。 | [計數與手術驗證](four_color_counts_surgery_verification.md) |

「八為緊界」只能證明最小度五的二點側估計在八處停止，不能升格為所有邊割方法的
不可能性定理。triangle 的三張表排除四色覆蓋星的指定邊界，不等於排除 C5 的 T4=932。
一般 932 排除、後續多步來源不變量與共同解存在性仍 OPEN。

## 證據與重播

新增四份獨立核對腳本與
[小型 JSON 證書目錄](../audits/2026-10-29-four-fronts-verification-4476049/)。
來源雜湊與實際檢查範圍見[驗證收據](../audits/2026-10-29-four-fronts-verification-4476049/verification.json)。
七邊與計數腳本不需要圖染色 oracle；兩步腳本只讀原邊，另做完整有限搜尋；
剝殼腳本以候選序配合獨立原嵌入核查，只提供幾何證據。
各報告區分一般紙證、外部定理、有限 Python 核對與既有 Lean 的前提。

```bash
python3 scripts/four_color_seven_cut_verification.py --out /tmp/seven-cut.json
uv run --with-requirements requirements.txt python scripts/four_color_two_step_verification.py --out /tmp/two-step-new.json
uv run --with-requirements requirements.txt python scripts/four_color_shelling_verification.py --out /tmp/shelling.json
python3 scripts/four_color_counts_cone_verification.py --out /tmp/counts-cone.json
```

兩步輸出路徑須尚不存在。既有 Errera 手術及 Lean audit 的實跑範圍見計數報告；
新增結構推論尚未 Lean 化，也未修改主求解器。既有 frozen 證據保留，未 commit 或 push。

文件責任：七邊結果由七邊驗證頁承擔，六邊來源保留原證明並連入後續；
兩步候選由獨立驗證頁承擔，原分解定理不變。導覽與 STATUS 更新直接入口，
HANDOFF 的研究線／活躍標記不變。沒有新增可約構形、不可避免性或跨 split closure。

## e1a90fe 基線的四路續進

同日後續分工成果由各權威報告承擔；以上 `4476049` 驗證與 frozen 證據保留。
本輪三份超過1 MB的完整JSON依既有政策封存；新checkout先執行
`python3 tools/audit_archive.py restore --artifacts`，再讀完整fibres或重播各checker。

| 路線 | 續進與仍缺的環節 |
| --- | --- |
| 反向 canonical shelling | [逐列非空與耳朵收口](four_color_reverse_shelling_continuation.md)：`m≥3` 安全，首次失敗只在全頂點 `m=2` 後綴；一般不鎖定仍等強於4CT。 |
| 共同切口／去奇偶 | [P1–P3局部成果](c5_parity_shared_cut_continuation.md)：六項PM式、完整段奇偶重接、五葉C1與至多兩正收益區域；五參考共同排除OPEN。 |
| 非D正控制 | [Bernhart與B₈基準](ck_bernhart_benchmark.md)：正確圖共6–6對角線，D154／B₈最大支援76；5–5另一圖D160／B₈130。古典C還原重播，無新可約性。 |
| 八割／三步來源 | [原面周長與三步控制](four_color_eight_cut_three_step_continuation.md)：三角化短環契約下兩側各至少三點的割≥9；有限多步鬆弛仍留20型，三步空fibre本身可平面。 |

## 從四路成果接續的三項拓撲核對

以下接續保持前輪證書及其hash鎖定報告的原bytes；入口改動前版本見
[本輪來源快照](../audits/2026-10-29-topology-second-continuation-e1a90fe/source-before.json)。

| 新問題 | 權威來源與裁決 |
| --- | --- |
| 能否略過9–11抽象D表 | [小割周長](four_color_bond_perimeter_small_cuts.md)：三角化S34下兩側≥4的割≥10；加S5後兩側≥7的割≥12。完整處理周長五與不連通分支。 |
| 雙偶補參考能否直接迫奇環消失 | [雙參考奇環](c5_two_reference_parity_continuation.md)：雙命中與跨組保留段成立，真disk仍有九環；五參考共同阻斷未解。 |
| Bernhart 76列是否已提供可直接排除的非平面極射線 | [跨split稽核](ck_bernhart_cross_split_audit.md)：原向量非極端，拆成兩個41列lift極射線；同n/y真disk的普通PM表可不同，尚無新座標排除。 |
