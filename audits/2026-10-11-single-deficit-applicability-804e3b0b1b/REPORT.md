# 單缺額工具對目前 45／54 身份的適用性 audit

BASE：`4dd11f422c6fa49265a412085116b088786d0344`。本輪只寫此全新專屬目錄，權威輸入唯讀；不 commit、push 或發布。

**結論：本輪沒有把任何目前 OPEN 的完整來源身份無條件關閉。** 已確證的是實際 core 的單缺額翻譯、具名割點障礙，以及兩份新的同源幾何／contact 橋接。若 LIT-SD-A 通過，且對同一實際 core 另有二連通證據，可条件排除「無 U 兩 long」、「無 U long／singleton short」及相鄰兩 mixed 的二連通 45／54 subsets。它們的非二連通部分、其他 derivative／core 身份仍 OPEN；不能把這些 subset 結果報成一般 N45 排除。

選出的最小後續義務是：**無 U、long／真 edge-pair short、三個奇環 block 的接點鏈中，恰一條環間 bridge 的實際來源 minor 橋接**。完整可發布文本在 [NEXT-TASK.md](NEXT-TASK.md)，目前只交付，不發布。這是待證候選，不是本輪已證的來源排除。

## 1. 輸入、authority 及 A 的狀態

先讀 HANDOFF、STATUS、Kempe guide、N45 權威頁、weak list cores、degree5 guide，再沿其具名報告查核。530 份 BASE tracked docs 共 5,296,872 bytes 已先凍結，見 [INPUTS.json](INPUTS.json)；額外 BASE 報告及程式見 [EXTRA-INPUTS-01.json](EXTRA-INPUTS-01.json)、[EXTRA-INPUTS-02.json](EXTRA-INPUTS-02.json)。凍結副本和 live bytes 在凍結時一致。

BASE 文件沒有單缺額／LIT-SD-A 的採納陳述。同時存在另一份生成中的 `2026-10-11-c5-single-deficit-biconnected-5e7a5ffd` audit；本輪觀測並保存其文獻 PDF／txt、download 記錄及 initial receipt 的 bytes，明標 `concurrent-unadopted-observed-bytes`。它們不是 BASE 已採納定理，也不是 A 通過的證據。本輪不修改該目錄、不等待或假設其結論。

直接核對 Cranston–Rabern 的正式論文 [Beyond Degree Choosability (2017)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i3p29/pdf/)，Main Lemma、Theorems 3.6／4.1。原定理的二連通單缺額必要分類還包含 complete／例外族 D；它本身沒有只留下 `d_H(s)=2`。本輪將「N45 圖類中排掉那些例外、故二連通 core 必有 `d_H(s)=2`」稱為 **SD-A 的待驗 conditional contract**。這是為適用性 audit 固定的使用介面，不是補寫或冒稱 LIT-SD-A 已有驗收。精確區分見 [theorem_contract/theorem-contract.md](theorem_contract/theorem-contract.md)。

一般 connected 版本有 cut／lobe 分支（Theorem 3.6）；本輪只記適用障礙，沒有藉它宣稱非二連通來源全排。完整 Σ、paper、finite control、actual source、Lean 是五個不同證據層。本輪沒有新 Lean theorem。

## 2. 原 G、derivative X、真正 M

`B=(b0,…,b4)` 是具名有序 induced C5。G 是原 disk 來源，完整有序 Σ(G)=933／941 或整圖共同 D5 像，每條非框邊 Σ-critical。優先 N2 中，原 r/s 非相鄰且完整度數 5，其餘有效內點完整度數 4；`H_G−{r,s}` 的實際連通分量恰為兩份 mixed，外加已明列的 unary。

X 只描述具體省略操作；M 是同一 literal 原拒絕三色列 β 的 inclusion-minimal obstruction。Σ-critical G 不使任意 X 對 β minimal；保 Σ minimalize 的另一個圖 Y 也不能當作 β-core M。只有明列 **X=M** 或獨立證成此等式時，才能直接使用 X 自身的 β witnesses。β-minimal M 的每條 retained 非框邊都釋放同一 β，因此 M 自身 Σ-critical；逆向推論不成立。

在精確 spoke 身份 `E(M)=E(G)−{rb_i}`、`V(M)=V(G)`，逐原邊計算：

| 頂點 | M 自身原邊的完整 degree | M 自身 boundary／內部 degree |
| --- | ---: | --- |
| r | 4 | `t_r^M=t_r^G−1`；`d_H(r)=5−t_r^G`（無 U 的 N2） |
| s | 5 | `t_s^M=t_s^G`；`d_H(s)=5−t_s^G` |
| 其他有效內點 v | 4 | `deg_piece(v)+1[rv]+1[sv]+|N_B^M(v)|=4`，shared contact 計兩條原邊、單一染色坐標 |

完整 unit unary 省略則只有在其唯一原 contact 是 rx、`X=G−V(U)=M` 時，r 恰失 rx，其餘 retained 點不失原邊；只刪 rx 的 derivative 會把 U 接點降度，不能直接叫它 M。其他 X≠M 身份的 profile 要重新由 M 的原邊核算；沒有 actual source 時標 unknown。

從 **M 自己**的 β-minimality 得到有效 H_M 連通、每點完整度數至少 4、同一頂點 retained boundary 鄰色互異。令 `Lβ(v)=Col−β(N_B^M(v))`；β 未用色 D 屬於每個 list。已證 M profile 是唯一 s 完整度5、其餘4時，

`|Lβ(v)|=d_H(v)`（v≠s），`|Lβ(s)|=d_H(s)−1`。

這才是單缺額輸入。既有 degree4 Gallai 引理已給 `H_M−s` 是 Gallai forest；它不是新工具增加的完整 relation 資訊。[weak list cores §1／4](frozen/docs/c5_weak_list_cores.md) 記錄這些論據。

## 3. 適用性表與具名割點

逐身份表見 [APPLICABILITY.md](APPLICABILITY.md)、[identity_inventory/inventory.md](identity_inventory/inventory.md) 及 [identity_inventory/inventory.json](identity_inventory/inventory.json)。表中 distinction 以原邊計算，沒有用 root 名稱取代 degree。

無 U 的精確 N2 S 身份中，`H_M=H_G`，且 `H_M−s={r}∪P∪Q`、`H_M−r={s}∪P∪Q` 各連通，故 r/s 不是 H_M 割點；**P/Q 內的割點仍 unknown**，沒有 actual 目標圖可命名它們。相反，完整保留 unary U 的 owner root 是契約所迫的具名割點：刪 root 後 U 與其餘 mixed／另一 root 分離。這使 LOW／HIGH／LONG-R／LONG-S 的限定已排身份不滿足二連通前提。已採納結果只比較，不重新開啟。

另一份目前明確殘留 `AD1-M12-b-spoke` 中，真正 degree5 是 a；`H_M−a=(C+b)⊔U`，所以 **a 是割點**，`d_H(a)=3`。`G−au` 則把 u 降3，不是 actual core。相鄰 no-mixed 的保兩 roots 45／54身份保留內部 bridge rs，unique degree5 s 必有 retained side 因子，因此 s 是割點。這兩項是具名契約推論，不是本輪 actual target source 的 finite 反例。

## 4. 二連通無 U 身份可縮到哪裡

以下都先假設實際 H_M 二連通，並將 SD-A 的 `d_H(s)=2` 結論保持 conditional。

### 4.1 兩原接點及實際 block 鏈

原 s 的三條 spokes 全留；兩份 mixed 各恰一原 s-contact，依原 rotation 記為 `p∈P,q∈Q`，p≠q。`C=H_M−s={r}∪P∪Q` 是實際 sole component，全部 C 點在 M 完整 degree4，且 `C−r=P⊔Q`，故 **r 是 C 的具名割點**；這與 r 不是 H_M 割點相容。

H_M 二連通迫 C 的每個割點都分隔 p/q，且 p/q 自己不是 C 割點；否則保留同一個割點刪除後，H_M 仍有不含任何 s-contact 的分支。C 的 block-cut tree 因此是 p→q 的無旁支鏈。既有 R12 的原 tethers／connected exterior 論證排 C 的 K4 block；更大 clique 不合 C 完整 degree4。故這條 Gallai 鏈只有原 bridges K2 與 odd-cycle blocks。

r 兩側各只屬一個 incident block，所以每側原 r-contact 數是 1（bridge）或2（odd cycle）：

| 原 `(k_P^r,k_Q^r)` | 原 `t_r^G` | M retained r-spokes | r 的實際 C 位置 |
| --- | ---: | ---: | --- |
| (1,1) | 3 | 2 | 兩個 bridge blocks 之間 |
| (1,2)、(2,1) | 2 | 1 | bridge 與 odd-cycle block 之間 |
| (2,2) | 1 | 0 | 兩個 odd-cycle blocks 的共用點 |

每個 block 保原 vertices／edges／contacts、actual attachments、ownership、bridges 及 inherited rotation；block 鏈不是 replacement，也沒有保持全部 Σ 或 rooted lifts 的結論。

### 4.2 無 U 的兩 long：同源 star 預算直接阻止內度2

此橋接不需 A，也不需二連通：只暫設原 `t_s=3`。原 `H_G−s={r}∪P∪Q` 連通，所以全部非 s 內點及附件在 B+s-star 的同一面。原 G full B-touch 迫兩個非 spoke 框點在該面的閉框弧，三 gaps 必是1／1／3，全部 P/Q 位於唯一長3面 A。

對原 piece T=P/Q，另兩個小面經原 s-spokes 接到 `s∈H_G−T`，所以在 K_T 中位於含 H_G−T 的 F_T；其框邊屬 ∂F_T。故原盾弧 `σ_G(T)⊆E(A)`。另一 mixed 的原 r–s 路確保兩 piece 各 one-sided；原 long 收費各≥2，且原盾弧互斥。得 `4≤|σ_G(P)|+|σ_G(Q)|≤3`，矛盾。

因此此完整 **無 U 兩 long exact-S 身份本身就有 `t_s≤2`、`d_H(s)≥3`**。SD-A 通過後可條件排它的二連通 subset；剩餘來源若存在，必有內部割點，但目前沒有 actual source 可命名。這重新核了沒有 U 的原 connectedness／star／費用，沒有搬有 U 的 shield profile 或 private covering。

### 4.3 long／singleton short：contact 預算矛盾

4.1 給每份原 piece 的 r-contact≤2、s-contact=1，總 incidence≤3。既有 S04／S3 在同一原 one-sided degree4 piece、原 full B-touch、原 critical-contact 前提下，排 singleton support 成為 blocker；完整 compatibility 為 Col²，與 X=M 的同 β 正值容量欄矛盾。因此 SD-A＋H_M 二連通時，long／short 的 **singleton short subset 条件排除**；剩餘 short 必為真框邊 pair。這是從全部 contact／完整 compatibility 得出的矛盾，沒有用 marginals。

### 4.4 既有 R 系列覆蓋及真正尚缺

M 自己是 disk、接受全部 T4、β-minimal、唯一 degree5 s、三 spokes，C 是原 sole 二接點 degree4 分量。X 自己刪各 s-spoke 的同 β 全圖 witnesses，再限制到 C，給其他三個 s 色的完整 assignments；β 拒絕给 D 色沒有 assignment。因此 **`F_C(β)={D}`**，四個 s 色查詢皆保留。這逐前提接到 R11 及 R 系列，不要求 Σ(M)=933／941。

| 實際 C 的 blocks／兩 contacts | 此次映射後既有覆蓋 | 未增加的主張 |
| --- | --- | --- |
| 0 個 odd-cycle blocks；其餘 bridges | R12 任意樹排除 | 不重新枚舉 |
| 恰1個 odd-cycle block | R13／14 任意大小排除 | 不按 long support 當 cycle 長度 |
| 恰2個 odd-cycle blocks，互斥或共用点 | R22／24 已合成全覆蓋 | 不把 P/Q 各當一個 cycle |
| 恰3個依次共用不同 cutpoints 的 odd cycles，兩接點各经外臂在末端私有點 | R27 既有任意長來源 minor 排除 | 四色 s-query 保持不是完整 Σ／r fibres 保持 |
| 恰3個 odd cycles，至少一段環間 bridge | 目前沒有明列 R27 覆蓋；仍 OPEN | 不能把 bridge 直接收掉後稱 R27 |
| 4個以上 odd-cycle blocks 的接點鏈 | 仍 OPEN | 不展開一般三環／更多環证明 |

R30 中間兩 contacts、R31 同末端兩 contacts 的三環鏈有不在 contacts 路徑上的端環；其共用點會是 H_M 割點。因此它們不在這個二連通 subset 中；**它們的一般非二連通來源缺口沒有被關閉**。對照原 attachments／rotation 的 R31 一般來源 minor 仍待補。

## 5. 其他具名45／54身份與55

N1 sole mixed 的 unit-spoke／整 unit-unary 省略，若確證 X=M、沒有 retained unary、H_M 二連通，SD-A 只收窄到原 s 三 spokes／C 的兩原 s-contacts；不套 N2 的兩 mixed 原盾弧。相鄰 sole mixed 的 spoke 二連通 subset 收窄後落在既有四spoke(3,1)排除，沒有新覆蓋；相鄰 sole mixed 的整 unit-unary 省略仍有原 r 零spoke等條件殘留。

相鄰 **兩** mixed 的45／54 core 保原 rs 及兩份 mixed，唯一 degree5 s 至少有 `rs＋一 P-contact＋一 Q-contact`，故 `d_H(s)≥3`。若實際 H_M 二連通及 SD-A 通過，可直接条件排這個 subset；不需要任何染色 replacement。原 U2 只排44，整個 AD2 45／54身份仍未全排。

55只記適用障礙：若真正 β-minimal M 保兩個完整 degree5 roots，就有 `|Lβ(r)|=d_H(r)−1` 和 `|Lβ(s)|=d_H(s)−1` **兩個缺額**。本輪不處理它們的分類或證明。

## 6. 候選、有限控制與停止點

至多三條橋接候選及選擇理由見 [BRIDGES.md](BRIDGES.md)。最小者只处理一條環間 bridge 到既有 R27 的圖層映射。最弱已知充分輸出是 boundary 固定 actual branch sets、保原M的R11指定區域、目標逐項進入R25／R26 forcing-list正常形域（含T–S–T palettes及實際錨點），再核目標完整degrees、固定 β 的四個 s 色查詢／β-minimality，最後引用R27定位後的minor合成回同一 M。原M的T4只供給初始區域定位，不宣稱目標繼承T4；若改用R27首頁定理作黑盒，須另證其target T4前提。原全 relations／fibres／full lifts 保留為證據，不宣稱 minor 保持它們；若要以目標圖做染色接回，須另證完整介面雙射，不能從 F={D} 取得。

固定 literal controls、完整原圖及所有 proper literal C5 rows 的全部 lifts 見 [literal_controls/controls-report.md](literal_controls/controls-report.md)。每項各標 `triggered and holds`／`not triggered`／`counterexample`。目標來源前提不觸發；這些 toys 不是 actual N45 來源。原圖的同一內部 Gallai／同一有序 root-pair relation 也不能保完整 lifts；保留點投影負控制提供具體 witness。正常／seed17 重播與刻意 corrupted-certificate 拒絕的結果另見 [VERIFICATION.md](VERIFICATION.md)。

**本輪停止於適用性和一份後續任務。** 不採納 A、不更新權威覆蓋、不改共享文件／舊證書；沒有 actual target source、一般 B-E／ε≥3／主命題證明或新 Lean。未重新執行舊大枚舉、R terminal certificates 或 Lean build；既有任意大小論證及其 finite-terminal 信任界照留。
