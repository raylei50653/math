# 可直接發布的最小後續任務：BR-SD-1

工作目錄：`/home/ray/developer/ai/math`。

輸入 BASE：`4dd11f422c6fa49265a412085116b088786d0344`。若執行時 BASE 改變，先記錄並凍結本任務指定輸入的 exact bytes／hashes，再核權威狀態；不可把本輪 conditional 陳述升格採納。

目標：只處理 **無 U、long／真 edge-pair short 的45／54 exact-S身份，實際 sole degree4分量C恰三odd-cycle blocks、恰一條環間bridge**。建立該單bridge到既有R27的 boundary固定實際來源minor，或明列最小失敗原因。不要預設所有開放core二連通。

先讀：`docs/HANDOFF.md`、`docs/STATUS.md`、`docs/c5_excess_two_nonadjacent_unit_core45.md`、`docs/c5_weak_list_cores.md`、`docs/c5_degree5_guide.md`、`docs/c5_degree5_interfaces.md`、`docs/c5_degree5_three_cycle_roots.md`、`docs/c5_degree5_three_cycle_minors.md`、`docs/c5_degree5_shared_cycle_roots.md`、`docs/c5_degree5_long_triangle_roots.md`，以及本輪 REPORT／BRIDGES。本輪 A 尚未通過，引用 SD-A 保持 conditional。

精確來源合同：

1. G 是有限簡單 ordered induced-C5 disk，完整Σ933／941或整圖共同D5像、非框邊Σ-critical；原非相鄰 degree5 roots r/s，其餘有效點完整degree4。`H_G−{r,s}` 恰原L/S兩份完整mixed、無unary；L long，S支援恰一真框邊兩端。
2. 原 e=rb_i 是 r唯一boundary spoke；`V(X)=V(G)`、`E(X)=E(G)−{e}`；**X=M自己**是同一原拒絕literal三色β的inclusion-minimal core。由M原邊核 r完整度4、s完整度5、其他有效點4。G各非框邊保自己的Σ witness；M各retained非框邊保同一β witness。
3. 直接明設並核實M的 `d_H(s)=2`，其原有序contacts p/q各屬L/S，s三條原spokes全留。`C=H_M−s={r}∪L∪S`是同一實際sole component；r的L/S contacts各2，r在C完整內度4。
4. C的全部nontrivial blocks恰三原odd cycles J1,J2,J3及bridges。`J1∩J2={r}`，J3與J1/J2互斥；J2的私有點u和J3的私有點v由**一條原邊 uv**相連，這是唯一環間bridge；u≠r。p/q經原外臂分別到J1/J3的私有點，臂可零長；沒有其他blocks或旁支。所有cycle長度任意奇数。若此精確域在原支援／degree／βminimality下已矛盾，可直接證該矛盾並停止。
5. 保原vertices／edges、ordered/shared contacts、actual attachments/supports、ownership、bridge端點、rotation及同一literal色框。先以原M全部assignments核固定β下四個s色queries，精確 `F_C(β)={D}`；不能只核拒絕D。

工作：

1. 逐前提對照R27，明列唯一缺橋是uv，不重開既有零／一／二環、三共用點鏈或有U限定排除。
2. 在原edges／attachments上構造或反駁 singlebridge 的來源minor。裸收縮uv會使合併點完整度6；須證刪何原附件／吸收何原頂點、實際邊如何實現目標，以及它們對四個s色queries的效果。不得用同palette但不同actual attachment替換。

   另核tight palette障礙：uv的singleton palette `{c}` 使J2/J3二色palettes都避c而相交。即使刪兩B附件降degree，保原palette錨點的merged list仍有slack，可能釋放D；不能直接沿用原palettes當R27的互補相鄰palettes。
3. 目標必進入 **R11定位後R27的正常形／minor合成域**：三odd blocks依次共用兩個相異cutpoints，兩原接點／外臂在兩末端私有點，R25／R26 forcing-list域、T–S–T palettes及actual錨點逐項核回；boundary singleton固定，保原M由T4證得的指定arc區域。給全部非空、連通、互斥branch sets，每條target edge有原edge witness，rotation/minor對照可核。若r移入branch set，保原r角色及全部來源preimages，不假稱它仍是target singleton。
4. 保目標完整degree4/5與全部四個s色可延拓值，再由實際邊重建目標β-minimality／逐邊完整著色，引用R27定位後的minor合成回原M。原M的T4供初始區域定位，**不假稱minor後目標仍接受全部T4**；若改以R27首頁定理對target作黑盒，須另證target T4。這是拓撲反證；不要求或宣稱完整Σ、root relations或full lifts在minor下相等。任何真正的染色接合仍只能使用完整relations／fibres／full lifts和同源preimages。
5. 若用literal controls，逐項標 `triggered and holds`／`not triggered`／`counterexample`，附原圖全部邊、attachments／rotation、完整染色／刪邊witness、全部宣稱的fibres及重播。無actual target source只能報條件適用性或unknown；零觸發不承擔來源排除。固定query/list反例不冒稱disk來源。

成功停止點：完成這個singlebridge域的任意大小原minor／非planarity，或更窄直接來源矛盾；明列消除的identity且不推廣兩bridge、三環其他位置、四環以上、非二連通appendage或一般N45。

失敗停止點：保存最小具名失敗步驟及完整原證據，區分list／四個布林query／full fibres／actual source；停於exact bridge obligation。若只有無觸發控制，報unknown。不得以bare contraction、root marginals或固定β Gallai palettes宣告來源排除。

交付：REPORT.md、逐前提mapping、來源branch sets／完整witness或最小negative control、hash manifest及normal／seed17 read-only重播；有限產物採exclusive-create，失敗生成保留。

權限：只讀權威输入，只寫全新專屬audit目錄，凍結hashes。不得改共享文件／舊證書、commit、push或發布。本任務不包含LIT-SD-A驗收、一般B-E、ε≥3、55或主命題證明。
