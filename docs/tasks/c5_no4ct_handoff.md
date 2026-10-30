---
docgraph:
  id: c5.no4ct-handoff
  family: [c5, c5.minimal-source, c5.no4ct]
  verified_by:
    - audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md
    - audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md
    - audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md
    - audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md
    - audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md
    - audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/REPORT.md
---

# K∞＝K≤5 無四色定理前提路線：研究交接

2026-10-14。**尚未補完一般 `K∞=K≤5`。** 已完成的是不把四色定理當前提的
`K≤22=K≤5=K132` 推導：[C5→C4 完整來源橋](../archive/reports/c5/structure/c5_c4_boundary_pivot.md)
將三支共同的 y0=y1=0 轉為具名 C4 對角拒絕，接外部完整 ≤28 點計算。
本地化約不用 4CT，外部生成與計算信任另列；本輪未重播該枚舉。無界三支仍須處理。
同日已採納 **T1-CROSSCUT：原 no4ct 全域最小來源下 `h=3⇒p=0`**；
全部 PINCH／BRIDGE 已排除，不限制單接點數及兩側內點數，第一剝層只留 RING。
權威入口為 [C8 剝層](../archive/reports/c5/structure/c5_c8_peeling.md)，證明與完整重播見
[一般正對切口採納審查](../../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md)。

工作根目錄 `/home/ray/developer/ai/math`；研究 BASE 為
`6cafdfb02fe5892a49eee21f92aea2369a25c022`（原四包）；T1-CROSSCUT 的凍結 BASE 為 `77fbd5d`。
原四包發布與驗證由
[整理發布紀錄](../history/2026-10-13-k15-c8-no4ct-publish.md)追蹤；接手時先重新查 Git。

2026-10-13 歷史里程碑（研究 BASE=`d521163`）：[T1](../../audits/2026-10-13-c8-terminal-s1-d521163/REPORT.md)
曾證 h=3、p>0⇒s≥2，PINCH k≥21／BRIDGE k≥22；其剩餘分支現由 T1-CROSSCUT 全部排除，原證書保留。
[T2](../../audits/2026-10-13-c9-932-source-d521163/REPORT.md)
證完整932、h=4的五 apex 均 d_H≥4、d_G≥6，九個原面第三點互異，k≥18；
[T3](../../audits/2026-10-13-w5-no4ct-bridge-d521163/REPORT.md) 接通三支任取合法全內部 W5 的 ρ≥5。
本頁採納指定來源結論；原報告及凍結 seals 保持當輪內容，
[本批驗證與發布範圍](../history/2026-10-13-t123-no4ct-publish.md)另記。

## 1. 先讀這四份權威報告

**K≤22 的新捷徑：** 下表替代鏈第1份給三支最小來源，第2份§§3–4給度數及面結構，
再讀 [C5→C4 證明](../../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/PROOF.md)
及 [外部完整計算界線](../../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/EXTERNAL.md)。
這條新鏈不以 K13–K15 球面枚舉或 C8／W5 分支為前置；以下保存各既有分支的閱讀路由。

本頁負責兩鏈的閱讀路由、替代鏈契約與停止點；各命題的證明仍由下列權威
專題及 audit 報告承擔。原鏈的 4CT 前提與替代鏈的相對大小引理分開保留。

### 原證明鏈：保留普遍 exterior screen 的 4CT 前提

| 讀序／權威入口 | 真正使用的前置與結論 | 證據入口 |
| --- | --- | --- |
| 1. [Kempe／外側 screen](../archive/reports/c5/structure/c5_kempe_screen.md)及 [count-cone 翻譯](../archive/reports/c5/structure/c5_count_cone_bridge.md) | 原完整關係的 Kempe 必要性；4CT 給外側黏合非空，留下 933／941；primal／dual 計數翻譯及 Cor20 的嚴格 `<30` 界 | [screen 證據](../../artifacts/c5_cells/kempe_screen.json)、[外部界線](../../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/EXTERNAL.md) |
| 2. [共面正規形](../archive/reports/c5/structure/c5_cofacial_normal_form.md) | K 的小 witnesses／聯集封閉、全域最小 k／再最大邊數與原 screen，給不增 k 的近三角正規形；Cor20 得 K≤12 | [完整紙面及有限核對](../../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/REPORT.md) |
| 3. [最小來源度數界](../archive/reports/c5/structure/c5_saturation_degree_bound.md) | 原 screen 給普遍 C4 三內點代表；正規形／K≤12／全域最小性給邊界≥4、內部≥5、n5≥6 | [凍結證據與覆核](../../audits/2026-10-12-c5-saturation-degree-bound/REPORT.md) |
| 4. [全內部 W5／A–C 交付](../archive/reports/c5/degree5/c5_degree5_link_reductions.md)與 [完整外圈](../archive/reports/c5/structure/c5_neartri_boundary_collar.md) | 兩個結構分支承接度數界；全內部 induced W5 的 cap／原框計數論證，及外圈 crosscut／共同計數給 h≥3、n5≥9 | [W5 紙面報告](../../audits/2026-10-12-c5-deep-five-wheel-01a12ffa/REPORT.md)、[原外圈證據](../../audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/REPORT.md)與[最後 C7 共同計數排除](../../audits/2026-10-13-c7-joint-kempe-19209f4c/REPORT.md)；A／B／C 各自證據由專題表定位 |
| 5. [K13](../archive/reports/c5/structure/c5_k13_collar.md) → [K14](../archive/reports/c5/structure/c5_k14_sphere.md) → [K15](../archive/reports/c5/structure/c5_k15_sphere.md) | 原 K13 外圈分支再用 [C8 apex](../archive/reports/c5/structure/c5_c8_apex_degree.md)；K14／K15 由相應較小階數界、度數與 cone 接完整球面根圖，得 K≤15 | 三份專題的 primary／independent 證書及生成來源；[球面依賴表](../../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/SPHERE_DEPENDENCIES.md)另核對全部根點覆蓋 |

第 4 列是平行閱讀的結構分支，不表示 W5 是外圈定理的前置。
第 5 列是原報告的逐階敘事；替代鏈採用完整球面域的另一條接入證明。

### 替代證明鏈：四份權威報告

| 順序 | 來源 | 接手要點 |
| --- | --- | --- |
| 1 | [零內點 cap 下降與恢復 932](../../audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md) | 兩層最小性、三支最小來源、無 4CT 的十二內點界；E932 與 4CT 等價 |
| 2 | [度數依賴修復與 K13–K15 接入](../../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md) | 受限 C4 引理、度數界逐條重證、直接完整球面覆蓋 |
| 3 | [三支完整外圈接入](../../audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md) | 二邊 crosscut、原簡單內圈、共同 h≥3／n5≥9；不採納普遍 C7 可染性 |
| 4 | [C8 三支依賴接入](../../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md) | 相對大小商圖可染性、105 查詢與原八項、932 的 h≥4／n5≥10、h=3⇒k≥19 |

若只核對 **K≤15**，讀第 1 份 → 第 2 份 §§3–6 →
[球面依賴表](../../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/SPHERE_DEPENDENCIES.md)
→ K13／K14／K15 的完整球面證據即可：受限 C4 給三支共同度數，
外加 cone 後 `k+6=19,20,21`，每個五度 root 都核對十列完整關係。
這條接入不使用第 3／4 份的 h／C8 分類。接續無界來源研究時，才再依序讀
第 3／4 份的 `s<k` 接合、`N≤k+5` 商圖、完整外圈與 C8 剝層。

DocGraph 中各專題的 `requires`／`derives_from` 記原證明鏈的實際前置；
`related` 連向本替代交接，避免把兩個證明分支合成必須同時成立的依賴。
本頁是路由，未反向宣告專題為自己的數學前提。`verified_by` 僅為外部證據
路徑標籤，DocGraph 不檢查其檔案內容／定理 soundness，也不編碼兩鏈的選擇。
未有 metadata 的前置由正文連結核對；零反向邊不表示不存在依賴。

後續報告依序補上先前停止點；各原報告保留當輪語境。
現有共享 [共面正規形](../archive/reports/c5/structure/c5_cofacial_normal_form.md)、[度數界](../archive/reports/c5/structure/c5_saturation_degree_bound.md)
及 K13–K15 權威文仍保留原證明鏈；不能把舊文的普遍前提直接標成已去除 4CT。
本線導覽：[Kempe 導覽](../archive/guides/c5_kempe_guide.md)。

## 2. 接手必須保留的精確契約

圖類為有限簡單 C5 disk，五個邊界點具名且有序，正規化前允許內側 chord，
不預設連通。`Σ(G)` 是固定十列的**完整**四色延伸關係，包含空關係。
只按同一份完整著色的全域 S4 換色取商；D5 搬運必同時搬整圖、原框與所有列。

K 先定義為已有 132 個具體關係及其至多五內點 witnesses，不先假定所有圖已分類。
若有目錄外來源，在**所有 `Σ(G)∉K` 的來源**中先最小化內點數 k，
再最大化邊數。這不是固定 mask 的最小性，也不是 edge-critical／ε／N2 契約。

在此最小来源上，現已取得：

\[
\Sigma(G)\in D_5\!\cdot\{932,933,941\},\qquad k\ge23;
\]
\[
G\text{ 簡單、二連通、chordless-C5、內面全三角},\qquad
d(B)\ge4,\quad d(V\setminus B)\ge5,\quad h\ge3,\quad n_5\ge9.
\]

若完整關係為 932，另有 `h≥4,n5≥10`；若 h=3，只有原八項 933／941
必要條件殘留；原剝層給 `k≥19`，現共同 C4 界提高為 `k≥23`；T1-CROSSCUT 再給 `p=0`，只剩 RING。
這裡 p 是原 C8 嚴格內點中正對雙接點的數量；結論不適用於任意非最小來源。
舊十九內點界限定 h=3；新的二十三內點界來自 C4 來源橋，適用全部三支及所有 h。

共同對齊時，三支的 singleton support 分別為 `∅,{4},{2,4}`，全部包含 T4。
**分類只對全域最小來源成立**，尚未證任意目錄外圖都只可能是這三類。

## 3. 已完成的證明鏈與不能省略的步驟

**新增有界終點：** 完成下列第1–4步後，可直接由 C5→C4 接外部4-candidate完整枚舉，
得 K≤22；後列球面／外圈成果仍各有獨立結構價值，不是此新大小界的必需前置。

1. **空關係與十個低候選的下降。** 零內點外側 cap 黏合給至多 k+5 點的
   不可四色平面圖。由其存在性取全域最少頂點的不可四色平面圖，三角化、
   用初等低度縮減及 Euler 找五度點；刪點產生完整關係 932 的 C5 disk，
   內點至多 k−1，違反目錄外來源的全域 k 最小性。
   這一步允許更換圖和邊界，因為用途是最小反例下降；它不是保原 Σ 的替換。
2. **932 必須保留。** 932 的外側 wheel 有一內點，只得到新來源內點至多 k，
   沒有嚴格下降。一般 cap 大小 h 的公式為 `k(D)≤k+h−1`。
3. **共面正規形與十二內點界。** K 的二元聯集封閉，加上共面 Eq／Diff
   分解與最大邊數，給近三角正規形。三支皆有 `P⊆{2,4}`、`x24>0`，
   故計數參數 m>0；外部 Corollary 20 在 k≤12 給 m≤0，排除之。
4. **度數界已實際修復。** 舊「任意 C4 都有三內點代表」依賴普遍 screen。
   新版只證：若 C4 cap 有 s<k 個內點，增廣邊界 dummy 後仍有 s 內點，
   由最小性進入 K，有限表給三內點代表。四度點例外恰有 `k=s+t+3`，
   可用兩個 cap 代表重建至多 `3+5+3=11` 內點的同關係來源。
   **不得刪掉 s<k，也不得恢復成任意大小 C4 定理。**
5. **直接球面接入 K≤15。** 原框外加一個 cone，得到 k+6 點、最小度五的
   球面三角剖分。對 19／20／21 點完整域刪每個五度 root，全部關係是 1023∈K。
   此路不消費 h≥3、n5≥9 或 C8 八項來源分類。
6. **完整外圈三支接入。** 二邊 crosscut 的兩側恰有 `k=s+t+1`，故受限 C4
   引理和較小 C5 witness 可在同一色框接回。h≤2 的 63 項查詢加最後 C7
   同圖計數矛盾全排，得到共同 h≥3、n5≥9；不採納「任意 C7 關係不能含於 U」。
7. **C8 相對大小修復。** 若至多 N 點的平面圖不可四色，下降引理給至多
   N−6 內點的 932 disk。因此本最小來源下 `N≤k+5` 的 loopless planar graph
   可染；原 H 的商圖恰有 k−1 或 k−8+q≤k 點，足以修復 cofacial 步驟。
   全部 105 查詢排 97、留原八項，932 迫 h≥4、n5≥10。原 cap 的 s<k
   亦接回 apex／內圈／剝層，m=9、10 的完整來源排除給 h=3⇒k≥19。
8. **T1-CROSSCUT 排除所有正對點。** 任取原正對點 x，以原路徑
   `c_i–x–c_(i+4)` 切出兩個固定 C6；全部未知內部留在原兩片，單 x
   外側亦覆蓋 BRIDGE。八份原 collar／完整 target × 四個正對位置的
   32 項共同 literal 轉移與 512,568 個安全矩形全部矛盾；保留兩片
   同一完整支援的直積及 full-fibre 接合，並用必要 Kempe 條件收縮。
   這是任意大小來源覆蓋加完整有限判準，不是有界來源搜尋或普遍 4CT。

## 4. 精確停止點與未完成項目

| 義務 | 狀態與界線 |
| --- | --- |
| 任意大小 932 來源排除 | **OPEN**。`不存在 Σ=932 的 disk ⇔ 4CT`；不可再用 wheel＋4CT 提前刪除此支 |
| 任意大小 933／941 來源排除 | **OPEN**。既有具名局部分支結果只在其原完整契約內成立 |
| 一般 `K∞=K≤5` | **OPEN**。主命題自身蘊含 4CT；無循環證明須承擔這部分內容 |
| 三支共同等價目標 | **改寫已證，命題 OPEN**。[等價表述](../reference/c5/c5_equivalent_formulations.md)：四列延拓 (E) ⇔ 偶補匹配 (M) ⇔ `K∞=K≤5`；DLM 受限 D₄ ⇔ (E) ∧ R5 |
| h≥3、n5≥9 的新三支版本 | **已接入**；932 另有 h≥4、n5≥10，不提高三支共同界 |
| C8 八項分類及其後續大小界 | **已接入**。932 的 h=3 全排，原八項必要條件殘留及 h=3⇒k≥19 保留；無界來源仍 OPEN |
| h=3 的全部 PINCH／BRIDGE | **已排除**；[T1-CROSSCUT](../../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md) 證 p=0，不限 s 或兩片內點數；一般 RING 仍 **OPEN**。剝層自身給k≥19，當前另接C4共同k≥23 |
| 932、h=4 的原接點 | [T2](../../audits/2026-10-13-c9-932-source-d521163/REPORT.md)五apex下界及三接點／距四全排保留；[第五輪](../../audits/2026-10-23-three-mask-round5-cb8f859/932/REPORT.md)再得s≥1、深點d≥2、Q長至少10。真弦兩側皆深點，端點C contacts間距≥3；Q仍可有弦，一般s≥1來源OPEN，共同k≥23不變 |
| no4ct 私人圈秩0至4 | **已接通三支**；[T3](../../audits/2026-10-13-w5-no4ct-bridge-d521163/REPORT.md) 對任取合法W5得ρ≥5；一般縮減仍OPEN |
| h≥4 來源與固定寬度剝層 | **OPEN**。一般 separator 轉移已證，下一層 C8／度數／接點前提不自動傳遞 |
| 新論證 Lean 形式化 | **未做**；舊 `lake build` 不代表以上紙面拓撲已形式化 |

共享導覽中的「N2-BRIDGE 已排除含 932 的廣義 N2」限定於原 E4／N2
契約，**不等於一般 932 排除**。原 E-ARC2 域亦不能自動承擔 Q=B 的 932。

## 5. 建議的第一個窄任務

新方向先讀 [C4 來源橋](../archive/reports/c5/structure/c5_c4_boundary_pivot.md)及[四連通 T／T0 化約](../archive/reports/c5/structure/c5_c4_triangle_core.md)。
後者已將原 b 四度分支壓到同一 T0 的兩個具名三角面色集合差異，
另一支保留 T 的 b 出口；兩支仍 OPEN。原 b0、b1、b3 皆四度子支中，
較小 R 的完整 C4 關係已縮至 mask13；[JOINT6續進](../../audits/2026-10-14-c4-mask13-joint6-fdd3e22/REPORT.md)
補上ABCB的CD／BD完整fibre分解，高p,q子域有k≥28。
[返回單射與多型遞迴](../../audits/2026-10-14-c4-c5-recursion-fdd3e22/REPORT.md)
已排除原r五度；r六度時s,t≥6，較小C5支持經[相對共面識別](../../audits/2026-10-14-cofacial-fibres-676b102/REPORT.md)
縮為恰319。[低p/q真實來源續進](../../audits/2026-10-14-lowpq-source-676b102/REPORT.md)
再以同一T0兩個實際面的三點共同商圖證p=5⇒a≥6、q=5⇒c≥6；
保留七接點ABABCBC與ABABCAB各自非空的完整fibre，舊計數證書原樣保留。
[共同W與原內圈續進](../../audits/2026-10-14-r6-lowpq-3953c85/REPORT.md)另證r6p5的ell-v、ell-w原非邊與反射側對應結論，
固定三框點四度支由原collar無弦與私人圈秩≥2得到k≥ceil((3h+16)/2)，故k≤27⇒h≤12。
續攻r6p5及反射的共同延拓，原[來源表](../../audits/2026-10-14-lowpq-source-676b102/classification/SOURCE_TABLE.md)
其餘degree、旋轉與預算條件保留；完整319、高r低p/q及一般T／T0仍OPEN，高p,q的k≥28條件界不變。
[獨立有限枚舉](../../audits/2026-10-14-r6-319-enumeration-676b102/REPORT.md)另在同一固定框度數支排r6的k=23、24，
給條件式k≥25；k≤27的r6續進限25≤k≤27，不宣稱一般K≤24。
嚴格下降仍須核對完成成本與目錄外壞性。
保留六個原接點與同份完整染色，
不能把一步 Kempe 受阻或兩面各自的可行投影當成無界延拓的結論。
[共同 Tait／匹配判準](../../audits/2026-10-14-c4-tait-lock-review-fdd3e22/REPORT.md)
把 T／T0 兩支精確化為指定對偶邊異色，亦即偶補完美匹配恰含一邊；
整個 edge-Kempe 類鎖定仍不能代表全部完整染色鎖定。無界來源排除及合法最小性接回 OPEN。

C8 方向先讀 [T1-CROSSCUT](../../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md)
的任意來源覆蓋與雙 C6 完整接合，再由 [C8 剝層](../archive/reports/c5/structure/c5_c8_peeling.md) 接續
**RING（p=0）**：保留同一原 C8、原八份具名 collar／完整 target、原面及
全部 separator fibres，研究同一 H 的完整支援或合法嚴格縮減。
一般 RING 仍 OPEN，剝層自身給 h=3⇒k≥19，當前共同 C4 界為 k≥23；下一層度數、無弦及接點前提
不自動傳遞。PINCH／BRIDGE 的 s≥2 逐級任務已由一般定理涵蓋。

另一窄入口是 [T2](../../audits/2026-10-13-c9-932-source-d521163/REPORT.md) 的完整932、h=4：保留20份
較高度數來源。[第二輪原三接點全排](../../audits/2026-10-23-three-mask-round2-cb8f859/932/REPORT.md)已給所有內點至多兩個C9 contacts；
[第四輪群平均OR接合](../../audits/2026-10-23-three-mask-round4-cb8f859/932/REPORT.md)已排全部距四接點，每原collar只餘零pair。
[第五輪原Q接續](../../audits/2026-10-23-three-mask-round5-cb8f859/932/REPORT.md)以完整環帶排全部s=0，得s≥1、至少兩深點；真弦兩側皆深點且端點C contacts間距≥3。
下一步保同一原Q、可變single contacts與全部空band，追完整relation或合法原弦cell回填；不能把Q當induced，也不能因proper Q row沒有環帶lift便從原J刪掉。原C6／C7未平均counts仍只rank≤2／3，第四輪只對unused-color群和使用folded rank-one。
T2 自身給此支 k≥18，當前亦有共同 C4 界 k≥23；h≥5 及 h=4 的933／941另列，
不套用 h=3 十九內點界。
[T3](../../audits/2026-10-13-w5-no4ct-bridge-d521163/REPORT.md) 已完成私人低圈秩的三支接入；接續義務
是ρ≥5來源的合法嚴格縮減，不需再補森林至圈秩四的橋接引理。
保持受限 C4 的 `s<k`、相對平面可染性的 `N≤k+5`，不把 source-relative
商圖引理提升成普遍可染性。指定 transfer=941 的 C7 計數矛盾亦不等於任意
C7 關係不能含於 U。不以擴大有限 graph 搜尋代替無界論證。

若改攻完整 adjacent-singleton 命題，必須包含 `P=∅`，並清楚標示此支含 4CT
難度。不得只解 933／941 後宣稱無循環主命題完成。

## 6. 證據與可重播命令

目前有限證據：132 個完整關係 witnesses、十份零內點 cap、8,778 組聯集；
C4 全部 16 masks、七份小代表及全部具名指派；球面域合計 288 份嵌入、
4,021 根圖、40,210 列、845,866 份完整 lifts，所有根圖 Σ=1023。

驗證紀錄：[下降與正規形](../../audits/2026-10-13-c5-no4ct-dependency-6cafdfb/VERIFICATION.json)、
[度數及球面接入](../../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/VERIFICATION.json)、
[完整外圈](../../audits/2026-10-13-c5-no4ct-collar-6cafdfb/VERIFICATION.json)、
[C8 接入](../../audits/2026-10-13-c5-no4ct-c8-6cafdfb/VERIFICATION.json)。
C8 保留 95,900 annulus fibres（85,320 空）及 12,180 full lifts；下游 m=9 的
8 圖／3,272 lifts、m=10 的 128 圖／75,936 lifts 亦完整接入。
凍結輸入各在四包的 `INPUTS.json`；C4 完整證書為 gzip，使用下列 checker 讀取。

```bash
cd /home/ray/developer/ai/math
git status --short
git rev-parse HEAD
uv run --with networkx==3.5 python audits/2026-10-13-c5-no4ct-dependency-6cafdfb/check.py --check
uv run --with networkx==3.5 python audits/2026-10-13-c5-no4ct-degrees-6cafdfb/check_c4.py --check
python3 -B audits/2026-10-13-c5-no4ct-collar-6cafdfb/verify.py --check
python3 -B audits/2026-10-13-c5-no4ct-c8-6cafdfb/verify.py --check --negative
python3 -B audits/2026-10-13-k13-collar-50d5474/check.py --check
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/check.py --check
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/check.py --check
```

本批新增檢查入口（完整重播及沿用界線見各 `VERIFICATION.json`）：

```bash
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/verify.py --check
python3 -B audits/2026-10-13-c9-932-source-d521163/verify.py --check --negative
python3 -B audits/2026-10-13-w5-no4ct-bridge-d521163/evidence.py
python3 -B audits/2026-10-13-w5-no4ct-bridge-d521163/verify_delivery.py
```

T1 此整合入口只查 custody 與證書一致性；完整著色重播另見其報告。
T3 沿用舊完整染色 receipts，不以接入 checker 冒充重枚舉。

T1-CROSSCUT 的目前採納入口使用凍結輸入，不要求已更新的研究導覽仍等於 BASE：

```bash
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --check
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --replay
```

`--check` 核對 custody／已存結果；`--replay` 另獨立重算全部 64 項核對，
不覆寫原證書。audit 原 `verify_review.py` 保持歷史凍結審查入口，
不能要求已採納新結論的文件 bytes 與 `77fbd5d` 相同。主結論只需其中
32 項單 x 切口；另一 32 項 BRIDGE 是額外控制。未新增 Lean theorem。

保留的外部信任包括 Dvořák–Lidický Corollary 20 的計算證明、plantri 生成完備性
及 C 實作。新增 K≤22 另引用 Dvořák–Lidický–Mohar §2 的完整4-candidate計算，
本輪未重播；[來源與依賴核對](../../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/EXTERNAL.md)分開記錄。
原球面研究重播了關係／full fibres，未重播外部 cone 證書，亦未重跑
整套 min4 生成。詳見 [球面依賴表](../../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/SPHERE_DEPENDENCIES.md)。

本次交接採納已完成的 T1-CROSSCUT 審查並更新待辦，不新增 Lean；實際驗證見
[採納記錄](../../audits/2026-10-14-t1-crosscut-review-77fbd5d/ADOPTION.md)，未重跑全部球面搜尋。
接手研究時建立新的獨占 audit、凍結當時輸入，
保留舊證書；多列論證始終使用原圖、原具名接點、完整 fibres 及同一色框。

各研究輪的正常／seed17、負控制及獨立覆核以四包驗證紀錄為準；
各批發布檢查另見相應整理發布紀錄。本次採納保留舊數學證書與歷史失敗紀錄。

## 7. 可直接交給下一位 agent

> 接續 `/home/ray/developer/ai/math` 的無四色定理前提路線。先讀本交接與四份
> no4ct 報告，再讀 C5→C4 來源橋。一般 K∞=K≤5 尚未證；新橋接外部完整計算
> 得 K≤22=K≤5、共同 k≥23；外部十億級枚舉未由本輪重播。
> 新來源契約為全域最小內點、再最大邊數，保留 932／933／941；C4 代表引理
> 僅在 s<k 成立，相對平面可染性僅在 N≤k+5 成立。共同 h≥3、n5≥9；932
> 必 h≥4、n5≥10；h=3 只留原八項。T1-CROSSCUT 已證 h=3⇒p=0，
> 全部 PINCH／BRIDGE 排除，不限 s 或兩片內點數。新方向為具名C4的度四外點
> 與ABCB延拓；一般大小仍OPEN。C8的RING與完整separator研究也保留原target。
> 932、h=4的五apex均d_H≥4、d_G≥6且k≥18，20項較高度數來源仍OPEN；
> 三支任取合法W5的ρ≥5已接通。一般RING與其餘h≥4仍OPEN。不要用 4CT 刪 932，不要把 N2 的具名 932 排除
> 當成一般排除，也不要把第一層 C8 前提傳給下一層或宣稱主命題完成。
> 交付精確紙面論證、有限重播、OPEN 義務與下一個入口；保留並行工作，不自動發布。
