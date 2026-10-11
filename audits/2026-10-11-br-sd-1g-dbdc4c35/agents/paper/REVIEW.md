# BR-SD-1g：精確最終 bytes 的獨立數學審查

2026-10-11。獨立 reviewer：`/root/paper`；實際研究 BASE：
`dbdc4c35f785519c8e3cb0260807f0d2feb82469`。
本 reviewer 只寫本專屬 `agents/paper/`，沒有改主證明、mapping、controls、舊 audits 或 canonical。

**裁決：accepted scoped paper exclusion。** 下列精確 bytes 在完整原來源合同內，
已證本題指定兩份原旁支子域不可實現，沒有未處理的數學阻斷 finding。
這是 candidate scoped exclusion 的獨立紙面驗收，正式 canonical 採納仍需後續授權。
完整父身份保持 **OPEN**，完整 OPEN 身份新增無條件關閉數為 **0**。

## 1. 本次接受的精確版本與輸入

| 根層檔案 | SHA256 |
| --- | --- |
| PROOF.md | `14544b9a09b8fd67bb7a8539ab2566a442cc9cae692e71f966afb9a2adbe9d5e` |
| MAPPING.md | `ea752148d9f5f19ea111f5474b058b06c2920e4ebb9a49e87c97f9cb3b6e52c5` |
| REPORT.md | `e0a0401988a24e2e63aa88a8a1ded7a0ce25be29a578363ff3834d550eac0c68` |

機讀接受記錄為 [ACCEPTANCE.json](ACCEPTANCE.json)。
[初步獨立推理](REVIEW.initial.md) 及 [首版完整 proof review](REVIEW.proof-v1.md)
均保留；它們不是以上最終 hashes 的替代品。

實際讀取 frozen N45 canonical §1／§2.11、BR-SD-1a／1c／1e 正式 PROOF、
新主 PROOF／MAPPING／REPORT、獨立 mapping 原稿與最終 custody 裁決、controls 程式與 REPORT。
並直接從本 audit 作者 PDF 擷取印刷 p.5–6，核對 degree assignment 的 ≥ 定義及
Theorem 10 的 blockwise-uniform 完整 union／incident-disjoint palettes。
外部 PDF hash 為 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。

[VALIDATION.final.json](VALIDATION.final.json) 保存本 reviewer 獨立回讀：31 份 frozen inputs
全部 size／SHA 符合 INPUTS pins，根層 33 個 local links 的已有 targets／anchors 正確，exit `0`。
當時只缺本 review／acceptance 與後續 SEAL 的預定 targets；不是未處理的數學引用缺口。
此回讀只驗 frozen bytes／links，沒有冒充 live Git／舊 custody／來源觸發驗證。

## 2. 完整來源映射與舊引理前提

根層合同保同一原 G、完整 ordered induced-C5 disk、Σ933／941 或共同整圖 D5 像、ε=2、
G 的逐非框邊 critical full witnesses、非相鄰 degree5 r/s 及其餘有效 degree4。
X=M 恰 G−e，e 是 r 唯一原 spoke；M 自身同 β 拒絕與 inclusion-minimality、
其全部 retained-edge witnesses 仍明列，沒有從 G critical 性遺傳。
U=0、L long、S actual adjacent pair、原 ownership／attachments／rotation、
p/q 及 s 的三 spokes、sole C／r split22、原骨架與全部 full lifts 也保留。

MAPPING 的符號 degree 表完整覆蓋所有原點類別與 x2 位置／重合。
每個數據仍是同一候選原來源的 `4=d_C+k+t`，不是自行選附件使容量表合法。
W1 與 W2 單接點使原 cycle blocks、uv 及兩外臂 bridges 保持；刪 r/s 後各仍留在 L/S。
W2 的每點 k≤2，故其 degree1 葉已先排除；W1 在 L 的 degree1 葉可需三附件，
不能將 S pair 限制偷用於 L。a3=v 的非空 W2 因 d0+t=4 已飽和而先結構排除。

W1 的唯一接點 x1 刪除後分離非空 W1，故確為 C 割點；J1 triangle 沒有另一
非割點、非 s-contact 的 private witness。r 是多 block 接點；a1 在正長臂為割點，
零長時 a1=p 且其 list 禁 D。J2 的 `w2∈J2−{r,u}` 則完全未被兩份旁支佔用。
因此舊 1e 雙 witness 路線確實不能直接套用，但這不給 actual-source 反例。

W2 在 v/a3 的合法列保持 1c terminal lemma 全部局部前提，直接由舊 lemma 排除。
普通 J3 點或正長臂 off-cycle 點接入，分別失去 block 接入位置或無額外 C 邊前提。
MAPPING 同時正確列出仍保存原短證明讀取點的配置，沒有把已可排除的列包裝為新 OPEN。

## 3. 新證明的關鍵逐步核對

1. 原全部 M 鄰居恰在 C、B 或 s，給每點 `|L^D(y)|≥d_C(y)`，沒有預設 tightness。
   完整 list coloring 的存在等價同一 M／β／s=D 的完整延拓存在；每條原邊都被核對。
   被 effective-H 忽略的原點以自己的合法色因子接回，所有 full-lift 座標保留。
   M 自己拒絕 β 迫 C 不可著色，沒有把別圖或 marginals 的拒絕搬過來。
2. 作者 PDF Theorem 10 適用有限連通 C 的 degree assignment，給真實 maximal blocks 的
   完整 palette union 與交會 palettes 互斥。Bridge 是 K2，palette 非空且大小1；
   triangle／任意奇環 palette 大小2。Wi 非 Gallai block 的情形已在此直接矛盾。
3. 同一 actual pair 的 β 色 A/B 異色，T 為 β 第三已用色，D 未用。
   所有 `S−{q}` lists 都含同一 T/D；q 含 T、禁 D，無需假設 q 原 C-degree1。
   J2 private w2 的 degree2 迫兩原 B 鄰點恰 actual pair；故 `P_J2={T,D}`。
4. S∪{r} 對 L 的唯一原出口是 r，其唯一 incident r 的 S block 是 J2。
   單接點 Wi 不合併原 blocks 或增加出口。恰含 T/D 其中一色的 palette 不可碰 J2
   的任何原點，故不能經 r 逃入 L／W1。
5. 使用包含**全部原 C vertex nodes** 的 block–vertex incidence 樹；非割點是其葉點，
   並非將相交 blocks 直接連成可能含 clique 的圖。從 q 的 T-only incident palette 出發，
   在每 block 選非來點的另一原點。該點在 S−q，缺的另一色須來自不同 incident block；
   互斥使新 palette 恰含另一色。若原點非割點，無下一 block，當場矛盾。
6. 每步選不同出口 vertex／block，在有限樹形成不回頭的 simple path，不能回訪 q，
   不能碰 J2，卻被缺色規則迫無限延續。有限性給真正矛盾；臂長、分支大小、
   x2 接點、m2 及 branch 深處 K4 都不破壞上述推論。

這是任意大小紙面論證，沒有將 finite fixture 的 palette 搜尋提升成全稱證明。
全程只從完整 list union 找提供缺色的**另一** palette；没有從割點含 D 推每份 palette 含 D，
沒有獨立重命名不同 blocks 的色，也沒有以 source minor 或另一 minimal core 代替原 M。

W1 合法路由另核正確：J2 迫 J1 排除 D，x1 的 D 可落在唯一首 W1 block。
m1=1 時首 block 是 bridge；m1=2 在 Gallai 刻畫下是 odd cycle／triangle。
這沒有局部矛盾，且與保留的 cutpoint 負控制相容；主矛盾確實來自同一 S 的追色。

## 4. Findings、controls 與精確信任邊界

首版紙面精度 finding 是：忽略原孤立座標後的 C 投影通常不是 full M lifts 的一對一。
最終 PROOF§3 已改為存在 iff，並明列完整原允許色因子的乘積；此 finding **已解決**。
早期 review 原檔未改寫。最終數學阻斷 findings：**0**。

六個最小三 triangle synthetic fixtures 覆蓋 p/q 零與正長、W1 佔唯一 J1 witness、
W2 接 J3／v／a3／q／臂內點及 m=1/2。它們接受 β，full lifts 數為
`64,224,32,144,32,96`，完整 compatible palettes 全為0；16 個 ordered p/q fibres
含空與 full C/M/G tuples 都保留。這是 `triggered and holds` 的有限校準，
不是完整原來源驗證。其任意大小結論只由以上紙面推理承擔。

controls 所列 counterexamples 只反駁 occupied-witness preservation、cutpoint 強推、
旁支首 block 必含 D、degree／拒絕自動給 M minimality、marginals 等於 full lifts 等局部推論。
已 degree4 再增邊、刪原附件修 degree、錯 actual pair、a3=v 飽和的控制則記原第一矛盾。
primary／independent 正常重播 exit0 與各三種 corrupted certificate 預期 exit1 分開記錄。
初次錯 assertion、失敗 generation 及前版 archive 保留；没有把失敗刪成成功來源證據。

**actual target source count=0；完整來源 finite status=`not triggered`。**
本 reviewer 未收到 actual disk source，也沒有因必要 degree／palette 合法而主張來源存在。
Custody 審查修正的 manifest pins／seal claim findings 屬工具完整性；即使全部 PASS，
亦不代替紙面定理、source witnesses、Lean 或 canonical 採納。本 review 在 root 實際 seal 前完成，
不聲稱自己已驗 root 最終 seal；其後 exact-byte custody 應對回本接受記錄。

## 5. 範圍與停止點

接受量詞只涵蓋 PROOF§1：同一完整原來源的 J1 triangle、任意奇長 J2/J3、
任意原 p/q 臂長、恰兩份有限非空原 W1/W2，唯一接點分別 x1 與 J3／q-arm，
全部合法具名重合、original degrees／attachments／ownership 及 full lifts。
此精確紙面域沒有剩餘 proof obligation；正式採納／上層文件傳播不在本輪授權。
沒有將 proof 只用部分強前提轉成一般多旁支 Gallai tree closure。

完整 N45-S-NOU-LS-PAIR、其他 splits／骨架、多旁支、R31、其他 core／45／54／55、
ε≥3、一般 N45／N2／E、主命題與 `K∞=K≤5` 均仍 OPEN；沒有新增 Lean theorem。
**父身份 OPEN；完整 OPEN 身份新增無條件關閉數＝0。**
