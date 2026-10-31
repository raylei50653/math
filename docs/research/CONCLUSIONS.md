# 當前採納結論與研究邊界

整合：2026-10-30。依[精確消元研究契約](4ct_guide.md#精確消元主線的研究契約)及
[10/30 成果整理](../history/2026-10-30-research-results.md)選取接續研究正在使用的結果。

**本頁是目前採納結論的唯一入口與維護位置。** 它保留精確適用範圍、證據層、OPEN 與原完整來源，
不收錄全部歷史局部結論，不作逐輪進展 ledger，也不複寫詳細證明。
其他文件說明問題、方法與閱讀路徑；完整研究報告保存原命題、全部證明、資料與當輪驗證。
歷史成果需要作接續依據時，先對回來源核對前提與證據，再按需提升至本頁或直接引用。

新研究在同輪完成來源核對後，把採納、修正或停止的結論整合至此，隨即封存完整研究報告；
研究檔不長期承擔另一套當前現況。新結果未改變本頁的範圍或邊界時，核對即可，不累加事件紀錄。
證據不足、來源覆蓋未證或量詞不符時保留 OPEN；有限搜尋的 `limit` 是未判定。
歷史報告與重播方式由[封存導覽](../archive/archive_guide.md)查閱。

## 目前主攻與驗收

對固定嵌入的有限簡單平面原圖、完整裸四色域，研究兩中心消去後在共同框點第三步匯合時，
哪些**同一原圖的實際連接與跨 split 身份**會排除抽象上仍存活的阻擋關係。
首個具名候選為原六框 `C₀=(z,a,b,w,c,d)` 上的 `PAIR-C0-D16`；
目前窄義務是用同一對原側圖的全部 fibres，以及交換後的全割要求，迫出不相容接法。
研究對象、下一個工作與驗收程序見[主攻契約](4ct_guide.md#第一個接續工作)。

已採納的停止結論是：僅保留六對邊界分量 traces 與完整交換立方的有限公理 `A_∂`，
存在量化後恰等於完整舊分量分割閉包，新增關係列排除為零。
該有限公理類的加註記搜尋停止；它沒有涵蓋完整原圖公理 `A_src`。
來源與證據：[註記投影](../archive/reports/planar-sources/four_color_three_step_annotation_projection.md)的任意初始關係紙證，
加上固定候選的完整註記／獨立 Python 重播；沒有新增 Lean。

**強度與稀疏化約（2026-10-31）。** 一般 D16 排除恰等於相鄰五度點對的著色可約性：
外圖可四色蘊含 G 可四色。它與相鄰 5–6 點對（七環）的同型命題合取後恰等價 4CT；
七環的 D 殘餘是全部 65 個拒絕型。因此任一 D16 來源的 G 都是不可四色的平面圖。
D16 來源對「刪去 H° 中度至多四的點」及「刪去分隔三角內部」封閉，化約來源滿足 `|F|≥5`、`e(F)≥2|F|−3`；
`|F|≥5` 依賴 4,440 張等號圖的有限窮舉，紙面密度推導先給 `|F|≥4`。
所以若 H° 的每個至少五點誘導子圖都有 `e≤2|F|−4`（例如無三角形或 pseudoforest），就沒有 D16 來源。
這是用整體可染性化約得到的來源類排除，不是關係層增益；二十面體控制使計數界同時取等號。
來源：[強度與稀疏化約](../archive/reports/planar-sources/four_color_d16_strength_sparse_reduction.md)，
紙面推導加 Python 有限證書；上述一般誘導子圖條件含 `|F|≥5` 的計算依賴，無三角形等具名排除不需該窮舉。
Franklin 界只作外部旁註，沒有新增 Lean。

**OPEN：** 稠密化約來源的一般 D16 共同原圖實現／排除、5–6 的另一半、保留新來源限制的消元與回寫契約、
目標來源覆蓋，以及由來源結構推出共同解存在性。來源子類排除不能直接提升為本路線的獨立 4CT 證明。

## 精確求解語義與最後共同回填

對任意有限簡單無向圖、合法部分固定色，完整關係消元在不受資源限制時能判定延伸存在性；
有解時，倒序回填構造同一份共同相容染色。每一步的完整剩餘問題滿足

\[
\operatorname{Sol}(P_i)=\pi_{U_i}\operatorname{Col}_4(G)
\]

（有固定色時取其延伸集合）。等式也容許兩側皆空，故它本身不保證裸平面圖非空。
所有因子共用原頂點身份、有序 scope 與字面色框；保留完整／空 fibres，最後才選共同見證。
各端點可用色、兩兩投影或各自非空不代替完整接合。

消去點有 `q` 個候選色時，一次完整投影等於所有至多 `q` 個原因子的共同子投影之合取。
這些子投影須作用於同一接口指派；回填仍由完整歷史重算共同支援。
四因子不等於四變數，scope、跨步依賴與整次成本可以增長。

**證據：** [完整判定與回寫](../tools/solver/four_color_completeness.md)是演算法紙證；
[接口語義](../tools/solver/four_color_mathematical_model.md)的投影與 fibre 解分解、
[有限域分解](../tools/solver/four_color_bounded_projection.md)有普通 Lean 核心及 Python 有限核對。
這不等於整份 Python 求解器已形式化。
**OPEN：** 一般效率界、Python 實作的完整精化驗證，以及保解語義之外的平面共同存在性。

## 同源平面限制與指定來源還原

**三步來源限制。** 在雙中心完整鄰域、同側六框外圖及所有實際交換分量的來源契約下，
指定雙反轉迫框外**同一分量**循環秩至少二，因而排除框外每分量皆為森林或單圈的 D16 來源。
[原紙證](../archive/reports/planar-sources/four_color_three_step_cross_split_exclusion.md)處理任意大小；JSON 原固定來源類採總秩至多一，
有限控制不承擔較廣量詞。完整同 separator fibres 的重接與[遠端全割準則](../archive/reports/planar-sources/four_color_three_step_remote_cut.md)
提供進一步必要限制；[K₄ 附件裝飾](../archive/reports/planar-sources/four_color_three_step_attachment_decoration.md)則證舊鄰點式單獨無關係增益。
以圈秩或稀疏度界定的子類，已由[稀疏化約](../archive/reports/planar-sources/four_color_d16_strength_sparse_reduction.md#5-稀疏外圖的排除)涵蓋並擴大到無三角形的 H°；
稠密化約來源仍 OPEN。固定框列整份 fibre 通過指定測試，也不足以排除後續逃逸。

**反向剝殼與三支接口。** [合法外環契約下的 `m≥3` 步](../archive/reports/planar-sources/four_color_reverse_shelling_continuation.md)
逐列保非空；裸頂點最小反例的首次失敗可定位於全原點已進入的 `m=2` 後綴。
[指定偶環雙帽反稜柱 `A_n`（偶數 `n≥6`）](../archive/reports/planar-sources/four_color_no_hub_three_branch_continuation.md)
有首次三支來源的全部 proper 整列支援，以及固定根下每個合法耳收口的共同見證保留。
任意弱對偶的條件保留引理不提供一般來源的初始共同支援；普遍不鎖定仍與 4CT 等強。

**小割支援。** [周長界](../archive/reports/planar-sources/four_color_bond_perimeter_small_cuts.md)在球面三角化、最小度五、S34 下
給兩側各至少四點的割至少十；再加 S5，兩側各至少七點的割至少十二，等號迫雙簡單 C₆ 框。
指定[雙 C₆ 來源](../archive/reports/planar-sources/four_color_twelve_cut_c6_sources.md)的七、八及[九點側](../archive/reports/planar-sources/four_color_twelve_cut_nine_side_classification.md)
已有保同一完整對側見證的 C 還原；裸頂點最小反例中的此類十二割只餘兩側至少十點且無框弦來源。
一般十二割、二點八割與一般九割五度三角面仍 OPEN，不能由指定側還原推稱割至少十三。

**證據：** 上述一般來源引理、條件保留與分類為紙證，具名圖、完整 fibres 和有限分支另有 Python 核對；
canonical 存在性及最小反例短環化約沿來源明列的外部定理使用。這批新拓撲結果沒有新增 Lean 形式化。

## Kempe 回返與五參考來源

**封鎖回返。** 對指定有序 C₅ 外界、其餘面皆三角形的原 disk，在指定五步正規化交換及
假設存在的全封鎖 Kempe 分量 K 中，每個回返週期為至少四的偶數，
K 中每個相應固定字面四色邊界 fibre 的完整著色數亦為偶數且至少四。
這排除具名薄 fibre 模型，沒有排除整個 support 932。
在 S34／S5 的原五度星契約下，[週期四接續](../archive/reports/c5/connections/c5_kempe_period4_s5.md)排原鄰點全五度子支；
[六附件接續](../archive/reports/c5/connections/c5_six_attachment_cross_round.md)迫原無弦 C₆ 及完整開側，另有小核心切換與條件逃逸。
交換始終使用完整 `O=G−v`，每次從同一份目標染色重算各色對分量，包含遠端交換。

**五參考。** 保留同一 plane 五葉來源、完整偶補族與全部族對產品，
[單命中來源引理](../archive/reports/c5/connections/c5_five_reference_source_exclusion.md)及[內側回返奇偶](../archive/reports/c5/connections/c5_nonfacial_two_gap_exclusion.md)
迫非面奇環的完整 singleton-hit 聯集至少缺三條原邊。
在非面 C₅、恰三缺、極小普通匹配及完整 Γ 等前提下，
[三缺分類](../archive/reports/c5/connections/c5_nonfacial_three_gap_compatibility.md)排除至少兩個環點直接連端葉的子型；
不能把任選五份代表或單一來源命中當作完整量詞。

**證據：** [封鎖回返](../archive/reports/c5/connections/c5_kempe_blocked_realizability.md)的奇週期排除為紙證，
週期二排除另用精確有限 F2 證書；S5／附件引理及五參考排除為紙證，固定來源與完整轉移由 Python 核對。
沒有新增 Lean。**OPEN：** 合法 S5 的全封鎖週期四、較長偶週期、六附件大核心、七附件以上及一般 Q5；
五參考恰三缺的零／一直接端葉、面環、四／五缺與一般 E932。子類結果不補一般 4CT 存在性。

## Bernhart 計數與六葉來源

古典 Bernhart 是共對角線 6–6 的具名圖；其 D 殘餘與標準 B₈ 最大支援分別為 154 與 76。
「接受 81、D 剩 160」屬另一張 5–5 圖，詳見[身份與基準](../archive/reports/counting/ck_bernhart_benchmark.md)。
[跨 split 稽核](../archive/reports/counting/ck_bernhart_cross_split_audit.md)證原 76 列向量非極端，拆為兩個 full-lift 極射線；
同 `n,y` 的真 plane 來源可有不同普通 PM 表，不能直接把 `y` 當作普通 PM 計數。

目前採納的來源化約以[通用標記](../archive/reports/counting/ck_bernhart_universal_marking.md)為完整依據：
無標記六葉的 `n=μh` 自動唯一決定完整 `y=μk`，包含全部零座標；
固定構件可把任一實際來源變成沒有含標記二邊 bond 的目標來源。
最小來源可化為簡單 3-edge-connected plane cubic core 的同面六邊插葉。
這是條件化約，尚未提供任何符合目標的完整來源；有限 K₆ 錐分離也不證覆蓋全部平面來源。

**證據：** 來源化約為紙證，唯一 lift、秩／整數證書與控制由 Python 精確重播；
外部下界及文獻結果沿原報告分列，沒有新增 Lean。
**OPEN：** 任意大小六葉目標的來源存在性／非實現證明與 r₂ 排除；原 76 列新增必零座標仍為零。
單 split 鎖定無增益的停止範圍不因這些化約改變。

## 幾何晶格與染色週期的獨立實驗

[RSST 接合與斜週期](../archive/reports/planar-sources/rsst_geometric_coloring_periods.md)保留原構形全部邊及接縫位移，
由七個 free completion 構造並精確核對平面週期三角化；Birkhoff diamond 六角例的最小原色週期指數為2，
一格不可能有短紙證。349個偶環來源的固定平衡四邊接法，組合商圖最小指數126個為1、223個為2，
一單元判定與全部SAT見證另有獨立枚舉重播；其中未精選342例未作精確幾何驗證。
原12晶體補全小指數斜晶格後，P01／P05／P09最小指數為3／2／2，其餘為1；P05有兩格斜域。
最小性相對各自**選定**幾何晶格，沒有證明原胞最小或一般指數上界。
逐幾何單步可由全域色號置換表示的染色，其指數至多4，有交換子群紙證及完整120對有限核對。
**OPEN：** 一般接合的週期界、奇環接合與無K₅商圖障礙的結構說明；這些有限結果不提供4CT或Kempe動態回返結論。

## 獨立的完全二分圖交叉數研究

對同一份 good drawing，[局部重畫](../archive/reports/crossing/zarankiewicz_local_redrawing.md)明算完整雙星複製與多星手術，
給出與實際外側相容的改善條件；計數鬆弛通過不表示存在畫法。
[旋轉與超額](../archive/reports/crossing/zarankiewicz_rotation_excess.md)有一份通過所列整數計數、奇偶及雙側重畫條件的
`K₇,₇` 共同張量，卻被四星旋轉相容性排除，建立固定候選的計數／旋轉分離。
旋轉超額、重複類與覆蓋預算只在來源明列的畫法及條件最小反例契約下使用。

**證據：** 外部頂點複製及 Woodall 旋轉下界、此庫紙面推導、Python 精確張量與旋轉／平面化控制分列；
沒有新增 Lean。外部完整證明與形式化沿原報告另列，不作本地已重播成果。
**OPEN：** 全部共同旋轉候選、低交叉畫法的不可避免性、完整外側重畫及本路線的一般下界。
接續次序見[交叉數契約](crossing/zarankiewicz_guide.md#接續工作與驗收)；這條獨立研究線不補 4CT 的共同存在性缺口。
