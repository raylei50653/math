# 45／54 單缺額適用性表

BASE `4dd11f422c6fa49265a412085116b088786d0344`。所有目標均無本輪 actual source，finite target status 均 **not triggered**；以下是具名前提內的 paper applicability。所有「A＋二連通」結果都 conditional。完整逐項 G／X／M、原邊計算法、missing premises 及 file:line 見 [17項 inventory.json](identity_inventory/inventory.json) 和 [inventory.md](identity_inventory/inventory.md)。

共同原來源 G：ordered induced-C5 disk、完整Σ933／941或整圖D5像、Σ-critical、原roots5/5、其餘有效點4；每列／pins／attachments／rotation使用同一原圖與字面色框。以下 `4/5/4` 表示 **M 自己** r=4、唯一s=5、全部其他有效內點=4；只在保留原邊的精確等式 X=M 及其自己的 β-minimality 成立時可填此欄。一般 X≠M 的degree仍unknown。`t_s` 是M保留且原G未失的s-spokes數，`d_H(s)=5−t_s`；不可把完整度5當內度5。

| 原身份／G | derivative X／真正 M | M 原邊完整degree profile | H_M 二連通證據／具名割點與s內度 | 定理前提／可縮減範圍 | 缺少橋接 | 既有覆蓋 |
| --- | --- | --- | --- | --- | --- | --- |
| **N2無U、long L／真pair short S** | `X=G−rb_i=M`，同β minimal，L/S全留 | 4/5/4 | 連通；r/s不是H割點，內部割點unknown；無二連通來源證書 | A＋bic：s內度2／原三spokes，各piece一s-contact；C是兩contacts之間K4-free Gallai鏈；r-splits11/12/21/22 | 三oddblocks環間bridge／≥4oddblocks；全原attachments及fibres不可由鏈名稱反求 | OPEN；C≤2oddblocks已有R12/14/22/24，三環直接共用鏈已有R27 |
| **N2無U、long／singleton short** | 同前 | 4/5/4 | r/s非H割點；內部cuts unknown | A＋bic：各piece r≤2/s=1，short总≤3；S04／S3與βminimal衝突，条件排此subset | A／實際bic；nonbic仍OPEN | 此完整身份仍OPEN |
| **N2無U、兩long** | 同前，P/Q全留 | 4/5/4 | r/s非H割點；內部cuts unknown；原star重新證 `d_H(s)≥3`（亦原r≥3） | 原同源長3面容不下兩份≥2盾弧；A＋bic迫s內度2，条件排此subset | A／實際bic，或nonbic支完整source-level處理 | 此完整身份仍OPEN |
| N2其他derivative／core | X省略身份未給，實際M⊆X須另核 | **unknown** | βminimal M才給連通；bic／s／具名cuts unknown | 適用unknown，不從G/X degrees填M | M原邊、全部省略及同βwitness | N45§1不含此類；OPEN |
| N1 sole mixed、spoke省略 | `X=G−rb_i=M` 須逐source證；sole C與side factors全留 | 4/5/4（精確身份內） | retained U的owner割點；無U仍內部cuts unknown | A＋bic只縮s三spokes／sole C兩原s-contacts | bic及完整sole C mapping；不借N2盾弧 | mixed22無44core也仍可45/54；OPEN |
| N1 sole mixed、整unit U省略 | `X=G−V(U)=M`，unique rx | 4/5/4 | retained U owner割點；無retained U則内部unknown | A＋bic同上 | 自身M minimal／bic；N2整U排除不能套N1 | OPEN |
| AD1相鄰sole mixed、spoke省略 | doc已證若X拒β則`X=G−rb_i=M` | 4/5/4 | retained U owner割點；無U時 `d_H(s)=1+m_s`；内部unknown | A＋bic迫m_s1／s三spokes；原總spokes≤4，落原(1,3)型 | 一般nonbic／其他profile不受此縮減 | 此bic型已有四spoke(3,1)排除，新增涵蓋0 |
| AD1相鄰sole mixed、整unit U省略 | `X=G−V(U)=M`，保rs/C，unique rx | 4/5/4 | retained U owner割點；其餘bic unknown | A＋bic：s三spokes、m_s1；原r-spokes0/1；r1落既有ternary | r0／原mixed31＋r-unitU仍僅條件收窄 | 整身份OPEN |
| **AD1-M12原b-spoke省略** | `X=G−bb_i=M`；真正s=a、r=b；C/U全留 | b4/a5/其餘4 | **a割點**；`H−a=(C+b)⊔U`；`d_H(a)=3` | 二連通前提不觸發 | 不可刪a–U後稱M（U接點降3） | 此b-spoke身份明列保留；a-spoke／整U省略已有全收 |
| AD2相鄰兩mixed、單側unit省略 | spoke或整unit U省略；actual `X=M`须核，保rs及兩mixed | 4/5/4 | retained U owner割點；無U bic unknown；**s內度≥3** | A＋實際bic：直接與s內度2矛盾，条件排subset | A／實際bic；nonbic未處理 | U2只排44；45/54整身份OPEN |
| AD0相鄰no-mixed、單側unit省略且保兩roots | 保原rs，actual X=M須核 | 4/5/4 | **rs是bridge、s是割點**；s内度≥2、有retained side因子 | 二連通前提不觸發 | 保原bridge／两侧full lifts；不扩一般no-mixed | U1只排44；45/54仍OPEN |
| 比較：N45-U-LP／SS | `X=G−V(U)=M` unique rx，L/S全留 | 4/5/4 | sole C；自身契約s-spokes≤2／内度≥3；bic未證 | 即使A+bic另矛盾，也没有新增覆蓋 | 沿既有原同源mapping | **限定已排，不重開** |
| 比較：N45-S-LOW1/2 | `X=G−rb_i=M`，完整U@r/P/Q | 4/5/4 | **r是H割點**；s內度3 | bic前提不觸發 | 不把H−s sole C當bic | 限定已排 |
| 比較：N45-S-HIGH1/2/3 | 同上，完整U@s | 4/5/4 | **s是H割點**；s內度3/4/5 | bic前提不觸發 | C/U完整接合及恢復e屬舊證明 | 限定已排 |
| 比較：N45-S-LONG-R/S | 同上，完整U/L/S、K1–K12 | 4/5/4 | U@r則r割點；U@s則s割點；s內度≥3 | bic前提不觸發 | 不搬有U盾弧或private covering到無U | 限定已排 |
| 55：原M=G、兩roots仍5 | M自己βminimal仍須另給 | **5/5/4** | 本輪不處理 | r與s各list deficit1，**兩個缺額**；單缺額不適用 | 僅記此障礙 | 未擴張 |

來源定位：N45權威頁§1／2／3；E4 REPORT§3.4／4.3／6；AD1原省略表和single-spoke自minimal證明；mixed12報告§2；AD2報告§1；AD0報告§1。全部已在本輪凍結，逐行引用在 inventory。

二連通 C 鏈的R30-middle／R31-same-terminal反向對照：那些contacts位置留下無contact端支，原共用點就成H割點，因此不屬bic subset；一般R31來源minor缺口仍OPEN。三oddblocks含非零環間bridge、或≥4oddblocks，不能直接叫R27。

無actual source時，表中的具名owner割點是**假設合同內的圖論推論**；未知的P/Q内部割點仍unknown。二連通target有限觸發數0不能用來排來源。此表不採納A或任何新全來源排除。
