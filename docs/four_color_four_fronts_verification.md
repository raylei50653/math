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
