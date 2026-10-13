# 三支的前提推進：no4ct 全內部五輪、C8 端部與 h=4 九環

2026-10-13。BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`；起始 Git clean。
本輪只寫此獨占 audit；19 份直接權威輸入及 frozen bytes 見 [INPUTS](INPUTS.json)。
共享研究文件、舊證書及其他並行工作均保留。

**本輪完成三項可供後續來源研究使用的前提。** 在包含 932 的新全域最小來源
契約下重新接入全內部 induced W5；收窄 C8 的 PINCH／BRIDGE 子型；建立
h=4 的完整 C9 幾何與必要介面，排除全部 W5 弦側，保留 84 項同圖實現義務。
全部新推導不把四色定理當前提；無界三支與 `K∞=K≤5` 仍 OPEN。

## 1. 共同契約與需要先修復的前提

來源是所有有限簡單 disk-C5 的 Σ∉K132 圖中全域最小內點 k、再最大邊數
者；不是固定 mask 最小性，也沒有 edge-critical、ε、N2 或 P 非空前提。
保留原有序 B、原 rotation、所有 actual edges、共同 literal 四色名稱及完整
延伸關係。D5 只能同時搬整圖與全部列。

目前共同已有 k≥16、B induced、內面三角化、框度≥4、內點度≥5、h≥3、
n5≥9；932 另有 h≥4／n5≥10，h=3 另有 k≥19。
依據為 frozen [no4ct 交接](frozen/docs/tasks/c5_no4ct_handoff.md)。

| 必須先處理的前提 | 本輪處理 | 後续仍須遵守的限制 |
| --- | --- | --- |
| 小 cap 代表能否在 932 上使用 | 對每個原 C4／proper C5 證介面含原內點，因而 s<k；重新證 cap 空／W5 | 不能提升成任意大小 C4 小代表 |
| 全內部 induced W5 是否依賴舊 exterior／4CT screen | 按原框接點及 Euler 重證三支的共同存在定理 | 不承繼私人圈秩≥5或一般 annulus 小代表 |
| C8 剝層后的原端部、chords／共享接點 | s_side=0 端部恰為具名 W5，建立完整 C6 原接點 kernel；排除全部 s=0 的 PINCH／BRIDGE | 原 x 只用同一色值；bridge xy 保留異色；下一圈 degree／contact 上界仍需新證 |
| h≥4 的第一個新介面 | h=4 原 C9 幾何二分與 435 份完整必要查詢；全部弦側排除 | 84 項僅為必要殘留；h≥5 另列 OPEN |

## 2. 三支共同的全內部五輪

[W5 紙面證明](w5/PROOF.md)與[依賴表](w5/DEPENDENCIES.md)逐一保留
受限 C4 的 s<k。原框恰有五個雙接 apex，第一層 L1 大小 D_B−15。
令 X=Σ_{內點 degree≥7}(degree−6)，h1 為 L1 中 degree≥6 點數；h1 與框超額
h=D_B−20 是不同參數。精確 identity 為

\[
n5^{deep}=1+X+h1\ge1.
\]

故三支的每份全域最小來源均有中心及五鄰環全在原內部的 induced W5，
B／U 十個原 pins 互異。這接通具名五輪路線；一般保完整 Σ 的縮減仍未取得。

## 3. C8 端部可以精確處理的子型

[端部證明及完整 kernel](terminals/PROOF.md)處理同一原 C8 第一剝層。
PINCH／BRIDGE 的每個 terminal boundary 長 5+s_side；若 s_side=0，耳點
論證迫非空，加原 proper-C5 小 cap 引理使它恰為原 W5。

因此 s=0 的两端無任意大小後繼，完整局部來源恰為 PINCH m=11 或 BRIDGE
m=12。回接八個原 h=3 collars、四份正對位置、兩種端部，共 64 份 paper
分類控制；全部完整 Σ=1023。保存 640 份 B-row fibres、61,752 個整圖 full lifts；
literal C6 端部 kernel 另保存全部 4,096 份指派與 744 個 lifts。
核對使用直接全圖 DFS 及按同一原 endpoint 的分塊 join，非各側單獨非空。

故對實際八份 h=3 最小來源：p>0⇒s≥1，PINCH m≥12、BRIDGE m≥13。
RING 的 s=0、m≥11 另可證其原 T8 induced：短弦會給低度耳，正對弦則
兩側都須 W5，迫 m=10 而已被上游排除。這個修復僅限 s=0；不給一般
boundary degree≥4或 at-most-two contact。

## 4. h=4 的 C9 前提與 932 精確入口

[幾何證明](c9/geometry/PROOF.md)不預設 C9 induced。原小 cap 與
A degree≥3／Y degree≥4 給：可能的弦只會切出 W5，其三个短弧中點皆是
原 apex；兩條弦會需要六個不同 apex，故最多一條。

[完整介面](c9/finite/PAPER.md)保留 70 份具名 e、75 份可能弦側及三目標：
全部 225 份弦側查詢排除，因此新來源结论为 **h=4⇒原 C9 induced**。
餘下 induced 210 項排除 126，保留 84（932／933／941 各 20／26／38）。
932 的 h=4 原 e 只可能是两個不相鄰 2，或三個連續正項 {2,1,1}；因而
其五個原框點 degree 皆在 4..6。一般 h≥5 不承繼此上界。

保存 C9 annulus 全部 574,000 fibres（530,845 空）、48,450 full lifts，以及
820 個原列、232 份 independent noncrossing equality partitions、435 份
完整必要支援／刪列／quotient ledger。原未知 H 仍須提供同圖 lifts 或同圖
計數矛盾；必要向量不是來源圖。詳見 [採納界線](c9/geometry/ADOPTION.md)及
[完整結果](c9/RESULTS.json)。

## 5. 驗證、停止點與下一窄問題

本包 [verify.py](verify.py)重播 frozen 輸入、主 checker、獨立 C9 checker 與
端部直接／分塊全 lifts；正常、PYTHONHASHSEED=17及負控制的實際結果
見 [VERIFICATION](VERIFICATION.json)。W5 與 C9 topology 為紙面證明，
有限 checker 不形式化任意大小 disk／Jordan 論證。

下一窄問題有兩個具體入口：h=3 應從保留端部原名字的 s≥1 PINCH／BRIDGE
或 induced s=0 RING 接回八份原完整支援；h=4 應從 [84 項 ledger](c9/RESULTS.json)
推進同一 H 的 C9 apex degree／共同計數義務，优先 932 的 20 項。
不得照搬 C8 的 274 維 counts 或每點至多雙接。

Closure scope：以上共同 W5 前提修復、C8 窄端部排除及 h=4 C9 原幾何／
完整必要介面。Updated：僅本 audit。Remaining OPEN：八項 h=3 無界來源、
84 項 h=4 同圖實現、h≥5、一般五輪縮減／固定寬度剝層、無界 932／933／941、
K∞=K≤5、以上新證明 Lean 化。未 commit／push；未重跑外部 cone 證書、
球面生成或 Lean build。
