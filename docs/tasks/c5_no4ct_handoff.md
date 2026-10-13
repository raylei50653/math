# K∞＝K≤5 無四色定理前提路線：研究交接

2026-10-13。**尚未補完一般 `K∞=K≤5`。** 已完成的是不把四色定理當前提的
`K≤15=K≤5=K132` 替代推導。無界 932／933／941 三支仍須處理。
本交接供接手者繼續研究；後續完整外圈與 C8 去依賴接入亦已完成，不新增數學結論。

工作根目錄 `/home/ray/developer/ai/math`；研究 BASE 為
`6cafdfb02fe5892a49eee21f92aea2369a25c022`。本批發布與驗證由
[整理發布紀錄](../history/2026-10-13-k15-c8-no4ct-publish.md)追蹤；接手時先重新查 Git。

## 1. 先讀這四份權威報告

| 順序 | 來源 | 接手要點 |
| --- | --- | --- |
| 1 | [零內點 cap 下降與恢復 932](../../audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md) | 兩層最小性、三支最小來源、無 4CT 的十二內點界；E932 與 4CT 等價 |
| 2 | [度數依賴修復與 K13–K15 接入](../../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md) | 受限 C4 引理、度數界逐條重證、直接完整球面覆蓋 |
| 3 | [三支完整外圈接入](../../audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md) | 二邊 crosscut、原簡單內圈、共同 h≥3／n5≥9；不採納普遍 C7 可染性 |
| 4 | [C8 三支依賴接入](../../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md) | 相對大小商圖可染性、105 查詢與原八項、932 的 h≥4／n5≥10、h=3⇒k≥19 |

後續報告依序補上先前停止點；各原報告保留當輪語境。
現有共享 [共面正規形](../c5_cofacial_normal_form.md)、[度數界](../c5_saturation_degree_bound.md)
及 K13–K15 權威文仍保留原證明鏈；不能把舊文的普遍前提直接標成已去除 4CT。
本線導覽：[Kempe 導覽](../c5_kempe_guide.md)。

## 2. 接手必須保留的精確契約

圖類為有限簡單 C5 disk，五個邊界點具名且有序，正規化前允許內側 chord，
不預設連通。`Σ(G)` 是固定十列的**完整**四色延伸關係，包含空關係。
只按同一份完整著色的全域 S4 換色取商；D5 搬運必同時搬整圖、原框與所有列。

K 先定義為已有 132 個具體關係及其至多五內點 witnesses，不先假定所有圖已分類。
若有目錄外來源，在**所有 `Σ(G)∉K` 的來源**中先最小化內點數 k，
再最大化邊數。這不是固定 mask 的最小性，也不是 edge-critical／ε／N2 契約。

在此最小来源上，現已取得：

\[
\Sigma(G)\in D_5\!\cdot\{932,933,941\},\qquad k\ge16;
\]
\[
G\text{ 簡單、二連通、chordless-C5、內面全三角},\qquad
d(B)\ge4,\quad d(V\setminus B)\ge5,\quad h\ge3,\quad n_5\ge9.
\]

若完整關係為 932，另有 `h≥4,n5≥10`；若 h=3，只有原八項 933／941
必要條件殘留，且 `k≥19`。十九內點界不能套到 h≥4。

共同對齊時，三支的 singleton support 分別為 `∅,{4},{2,4}`，全部包含 T4。
**分類只對全域最小來源成立**，尚未證任意目錄外圖都只可能是這三類。

## 3. 已完成的證明鏈與不能省略的步驟

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

## 4. 精確停止點與未完成項目

| 義務 | 狀態與界線 |
| --- | --- |
| 任意大小 932 來源排除 | **OPEN**。`不存在 Σ=932 的 disk ⇔ 4CT`；不可再用 wheel＋4CT 提前刪除此支 |
| 任意大小 933／941 來源排除 | **OPEN**。既有具名局部分支結果只在其原完整契約內成立 |
| 一般 `K∞=K≤5` | **OPEN**。主命題自身蘊含 4CT；無循環證明須承擔這部分內容 |
| h≥3、n5≥9 的新三支版本 | **已接入**；932 另有 h≥4、n5≥10，不提高三支共同界 |
| C8 八項分類及其後續大小界 | **已接入**。932 的 h=3 全排，原八項必要條件殘留及 h=3⇒k≥19 保留；無界來源仍 OPEN |
| h≥4 來源與固定寬度剝層 | **OPEN**。一般 separator 轉移已證，下一層 C8／度數／接點前提不自動傳遞 |
| 新論證 Lean 形式化 | **未做**；舊 `lake build` 不代表以上紙面拓撲已形式化 |

共享導覽中的「N2-BRIDGE 已排除含 932 的廣義 N2」限定於原 E4／N2
契約，**不等於一般 932 排除**。原 E-ARC2 域亦不能自動承擔 Q=B 的 932。

## 5. 建議的第一個窄任務

先從 [C8 接入報告 §5](../../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md#5-驗證停止點與後續入口)
及 [剝層定理](../c5_c8_peeling.md) 的同一原 C8、m≥11 出發，保留八份完整
必要上界與全部 actual faces。第一層 RING／PINCH／BRIDGE 已完備；PINCH
首次可在 m=11 進入，不能只沿 RING 推論。下一層度數、無弦及至多雙接不傳遞，
須在具名完整 separator 轉移上證明更強縮減或同圖實現矛盾。

h≥4 是另一項 OPEN 義務，包含一般 932；不把 h=3 的十九內點界套過去。
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

保留的外部信任為 Dvořák–Lidický Corollary 20 的計算證明、plantri 生成完備性
及 C 實作。本輪研究重播了關係／full fibres，未重播外部 cone 證書，亦未重跑
整套 min4 生成。詳見 [球面依賴表](../../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/SPHERE_DEPENDENCIES.md)。

本次交接文件只整理既有結果與待辦，不新增 Lean 或來源排除；不為文件變更重跑
Lean build 或全部球面搜尋。接手研究時建立新的獨占 audit、凍結當時輸入，
保留舊證書；多列論證始終使用原圖、原具名接點、完整 fibres 及同一色框。

各研究輪的正常／seed17、負控制及獨立覆核以四包驗證紀錄為準；
本批發布檢查另見整理發布紀錄。研究線未增減，未改寫舊數學證書。

## 7. 可直接交給下一位 agent

> 接續 `/home/ray/developer/ai/math` 的無四色定理前提路線。先讀本交接與四份
> no4ct 報告。一般 K∞=K≤5 尚未證；K≤15、度數修復及完整外圈／C8 接入已完成。
> 新來源契約為全域最小內點、再最大邊數，保留 932／933／941；C4 代表引理
> 僅在 s<k 成立，相對平面可染性僅在 N≤k+5 成立。共同 h≥3、n5≥9；932
> 必 h≥4、n5≥10；h=3 只留原八項，且 k≥19。先在新獨占 audit 從同一原
> C8 的 m≥11／第一層三型和完整 separator 轉移接續，包含 m=11 可進入的
> PINCH；h≥4 另列 OPEN。不要用 4CT 刪 932，不要把 N2 的具名 932 排除
> 當成一般排除，也不要把第一層 C8 前提傳給下一層或宣稱主命題完成。
> 交付精確紙面論證、有限重播、OPEN 義務與下一個入口；保留並行工作，不自動發布。
