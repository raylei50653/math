# 2026-10-30 研究成果整理

本次整理基準為 `e1a90fe`，收錄其後 10/29–10/30 的研究報告、腳本、完整證書與原驗證紀錄。
各題的命題、前提與 OPEN 裁決仍由下列專題來源承擔；本頁保存這次跨線整理及提交範圍。
成果保存與接續方向分成兩個 commit；本次使用者只要求 commit，沒有推送遠端。
原研究文件中的「未提交／待收」保留當輪語境，當前成果沿本頁與專題後續連結查閱，提交狀態以 Git 為準。

## 已取得的結果與界線

| 研究線 | 本批成果 | 尚未涵蓋 |
| --- | --- | --- |
| 反向剝殼與無 hub 收口 | [反向剝殼](../archive/reports/planar-sources/four_color_reverse_shelling_continuation.md)證合法 `m≥3` 步逐列保非空；在裸平面頂點最小反例契約下，首次失敗只能在全原點已進入的 `m=2` 後綴。[共同 hub](../archive/reports/planar-sources/four_color_saturated_hub_continuation.md)、[雙錐](../archive/reports/planar-sources/four_color_no_hub_bipyramid_continuation.md)、[最小度五環帶](../archive/reports/planar-sources/four_color_no_hub_min5_continuation.md)及[指定首次三支來源](../archive/reports/planar-sources/four_color_no_hub_three_branch_continuation.md)各有完整共同見證的條件保留結果。 | 上述無 hub 具名整圖來源仍有古典或明列 C 還原；一般初始共同支援及普遍不鎖定未證，後者仍與 4CT 等強。 |
| 三步共同來源與註記 | [原附件](../archive/reports/planar-sources/four_color_three_step_source_invariant.md)排除具名交錯來源；[完整關係控制](../archive/reports/planar-sources/four_color_three_step_relation_control.md)證 ALT 與平面 twin 的核心表及完整 fibres 相同。[共同外側交換](../archive/reports/planar-sources/four_color_three_step_shared_exterior.md)和[註記投影](../archive/reports/planar-sources/four_color_three_step_annotation_projection.md)補實際通道與跨列重播，量化有限 traces／交換立方後恰回舊分量分割閉包。 | 新增關係列排除為 **0**；有限註記公理已停止。完整共同原圖跨 split 實現限制及一般存在性仍 OPEN。 |
| 小割與十二割 | [周長推論](../archive/reports/planar-sources/four_color_bond_perimeter_small_cuts.md)在三角化、最小度五及 S34 下證兩側各至少四點的割≥10；再加 S5，兩側各至少七點的割≥12，等號給雙簡單 C₆ 框。[七點](../archive/reports/planar-sources/four_color_twelve_cut_w5_ear_reduction.md)、[八點](../archive/reports/planar-sources/four_color_twelve_cut_eight_side_classification.md)、[九點側](../archive/reports/planar-sources/four_color_twelve_cut_nine_side_classification.md)均有保同一對側見證的 C 還原。 | 裸平面頂點最小反例的此類十二割只餘兩側至少十點、無框弦來源。一般十二割、二點八割及九割五度三角面仍 OPEN。 |
| 封鎖 Kempe 回返 | [完整回返](../archive/reports/c5/connections/c5_kempe_blocked_realizability.md)排奇週期與週期二，封鎖 fibre 必偶數且≥4。[S5 接續](../archive/reports/c5/connections/c5_kempe_period4_s5.md)排原鄰點全五度分支；[差異附件](../archive/reports/c5/connections/c5_d2_attachment_separation.md)迫固定原分隔環長≥6。[恰六附件](../archive/reports/c5/connections/c5_six_attachment_cross_round.md)迫原無弦 C₆ 及完整開側，小核心可獨立切換，首次指定步失敗有條件逃逸。 | 未迫一般失敗；六附件大核心、七附件以上、合法 S5 的週期四、較長偶週期、全封鎖分量及 Q5 均 OPEN。Errera 不滿足 S5，合法兩輪前綴亦非封鎖反例。 |
| 五參考共同奇環 | [局部匹配](../archive/reports/c5/connections/c5_parity_shared_cut_continuation.md)、[雙參考](../archive/reports/c5/connections/c5_two_reference_parity_continuation.md)、[共同輪轉](../archive/reports/c5/connections/c5_five_reference_common_rotation.md)與[來源排除](../archive/reports/c5/connections/c5_five_reference_source_exclusion.md)補同一來源限制。[二缺邊排除](../archive/reports/c5/connections/c5_nonfacial_two_gap_exclusion.md)將非面奇環的 singleton-hit 缺邊界提高至三；[恰三缺邊](../archive/reports/c5/connections/c5_nonfacial_three_gap_compatibility.md)在極小來源下迫唯一側字及五種命中，完整 Γ 排除雙直接端葉子型。 | 恰三缺的零／一直接端葉、四／五缺及一般五參考／E932 仍 OPEN；真 disk 九環與舊共同切口負控制保留。 |
| Bernhart 計數與來源 | [基準](../archive/reports/counting/ck_bernhart_benchmark.md)區分 6–6 圖的 154／76 與另一 5–5 圖的 160／130；[跨 split](../archive/reports/counting/ck_bernhart_cross_split_audit.md)將原 76 列拆為兩個 41 列 full-lift 極射線。[原邊交會](../archive/reports/counting/ck_bernhart_retained_intersection.md)、[端點](../archive/reports/counting/ck_bernhart_endpoint_ray_continuation.md)、[標記分離](../archive/reports/counting/ck_bernhart_marked_separation.md)及[bond 構造](../archive/reports/counting/ck_bernhart_marked_bond_existence.md)之後，[通用標記](../archive/reports/counting/ck_bernhart_universal_marking.md)將剩餘義務化為無標記六葉 `n=μh` 的來源存在性；`h` 唯一決定完整 lift，最小來源有簡單 3-edge-connected cubic core 的同面六邊插葉正規形。 | 通用構件的 ×12 與 diamond 的 ×2 都是條件構造，未給實際目標反例；原 76 列新增必零座標仍為 **0**。全部任意大小來源及 r₂ 仍 OPEN。 |
| 完全二分圖交叉數 | [局部重畫](../archive/reports/crossing/zarankiewicz_local_redrawing.md)建立完整整星帳目；[旋轉超額](../archive/reports/crossing/zarankiewicz_rotation_excess.md)保存 `K₇,₇,C=79` 的共同整數張量，其通過所列計數、奇偶及重畫條件，卻被兩側旋轉提升排除；另有超額預算與完整平面化正負控制。 | 固定張量排除未排空所有候選；一般不可避免性及本路線完整下界仍 OPEN。外部完整證明與形式化不計為本地重播。 |

## 證據與本次核對

本批成果分為紙面論證與 Python 固定域／完整來源核對；**未新增 Lean 定理**。
既有精確消元的 Lean 語義不代替本批平面拓撲論證。Bernhart 的 K₆ 分離核對作者有限資料；
28 cubic 點下界依賴外部 computer-assisted 引理，完整文獻 closure 未在本地重播。
本次整理沒有新增研究枚舉，也沒有重跑 P4 的完整 12–24 點來源分類或 Lean build。

本次實際重播見[發布證據目錄](../../audits/2026-10-30-research-results-e1a90fe/README.md)：
C₅ 面限制、D₂／六附件獨立重播、二／三缺邊、三步註記、九點側獨立核對、三支完整支援、
Bernhart 標記與來源化約，以及交叉數的精確算術、旋轉與平面化控制。
原大枚舉及其當輪收據保持原 bytes；本次以 SHA256 清單核對保存，不宣稱重新完成那些計算。

九點側重播讀入 gzip 容器，因此輸入檔 hash 與原 raw JSON 收據不同；解壓內容一致，
143,360 份完整 fibres、54 格紙表與 2,232 份縮圖染色等其餘欄位全部相等。
三支來源重建輸出與既存解壓證書逐 byte 相同；完整空 fibres 亦保留。

大型原始證書使用既有 ARCHIVE 保存；新 checkout 先依
[還原說明](../../audits/README.md#新-checkout-的還原)執行 `python3 tools/audit_archive.py restore --artifacts`。
本次核對既有 ARCHIVE records 不變，並核原始 bytes、壓縮 blobs 及新增路徑；沒有新增產物例外。
文件、工具測試、正式 docs／全樹 DocGraph、實際 Git index 產物政策與 whitespace 的實際結果
記於證據目錄，不以局部通過代稱全域通過。

本次 17 項有限重播、515 項工具測試、文件連結／索引、正式 docs DocGraph、
ARCHIVE／artifacts 核對及 Git index 產物政策通過。
全樹 DocGraph 仍有歷史快照的 72 項 duplicate-id；staged whitespace 另報原六附件 reviewer
末尾一個空白行。該腳本 hash 綁定原重播證書，本次保留原 bytes，明記此項未通過，未新增例外。

## 文件範圍

新增報告、相關導覽、直接 consumers 及 STATUS 一併保存；HANDOFF 新增交叉數研究線，
4CT 仍是唯一活躍標記。舊 933／941、W7、J1／J2、完整 319 及一般 K≤22 邊界沒有改變。
本頁不另定研究優先序；目前主攻與第一個工作由
[4CT 研究契約](../research/4ct_guide.md#精確消元主線的研究契約)維護，其他線由各專題來源承擔。
