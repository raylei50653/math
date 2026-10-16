# R6-DOUBLE-W5-101：原來源的雙 W5 障礙完全排除

2026-10-16；研究 BASE：`0b639cf5ffd57e8e394add4e0b56cd60cc2ce38c`。
成果等級 **A**：在指定 no4ct 全域最小、次級最大邊數 C5 來源中，以任意
大小紙面證明排除 101 的雙完整 W5 最大 Tutte 障礙。
原三輪 audit 唯讀，424 個檔案位元組及成員名單均依 BASE 保存核對。

## 1. 新定理與適用範圍

保留原有序框 `(x,y,a,b,c)`、原 `x,y,b` 四度、`r` 六度、合法
`J=U/(s=t)`、`m=[s=t]`、實際球面對偶 D，以及具名原邊
`e=(vw)*, f=(pq)*, g=(mz)*`。令 `X=V(e)∪V(g)`、`H=D-X-f`。

**任取 H 的最大基數 Tutte 違反集 S，其奇 factor-critical 分量不可能
恰有兩個完整 W5。** 結合已獨立重審的
[R6-CHORDED-FIVE](../2026-10-16-r6-chorded-five-c4c3d99/PROOF.md)，
101 普通匹配失敗現在只可能有一個「非完整 W7 的七割分量」最大障礙。
本輪不擴張至一般 110、任意重標對偶圖或一般七割。

完整逐步證明見 [PROOF.md](PROOF.md)，獨立審查見 [REVIEW.md](REVIEW.md)，
前輪逐分量證明重建見 [REVIEW-PRIOR.md](REVIEW-PRIOR.md)。

## 2. 可獨立重用的來源結構

證明先從假設雙輪得到以下任意大小必要條件，再以原來源幾何閉合矛盾：

1. `zpq` 必為單點奇分量；共同非空 `P111` 飽和保留全部匹配的量詞。
2. 原 m 扇區的面字串配合精確曲率，迫全部非 m 頂點達奇偶最低度數。
   兩輪共有 rim 點的唯一候選是 m，但原 v/w 四度旋轉又迫第二個共同點，
   因此兩個完整六點輪鄰域必互不相交。
3. f 另一端若入輪，則原 p=q=5，另一 pq 面頂點同時是原五度輪心。
   既有同來源返回單射卻迫它至少六度。故 f 兩端均單點，p,q 避兩輪且原度六。
4. 任一剩餘配置至少有一輪避開六個具名點，其中心與五個 rim 點全部五度。
   若 m、z 分屬兩輪，實際短扇區的 alpha/beta 接點相交已直接矛盾。
5. 展開這一純五度輪的完整鄰接，得到 11 點、15 個原三角面的 disk，
   外界 Q 是 induced C5。原面字串 `101` 迫 Q 在 m/z 的同一原扇區；
   同時含兩 hub 則與 mz 的兩個強制面矛盾。原來源小 C5 定理迫另一側 W5，
   接成整個 J 全部五度，違反 `d_J(m)≥7`。

這個閉環不依賴 h=3 的舊有限 collar 表。文中保留該表交叉核對所得的
七個中間具名扇區類；它們全被最後一段排除，**不是剩餘 OPEN 配置**。
獨立工作論證及替代 f 入輪排除見 [A/C](RESEARCH-A-C.md)、[B](RESEARCH-B.md)。

## 3. 匹配族、計算與信任層

對同一原圖整個非空 `P111`，每個輪割始終恰跨一次。奇／偶交集的
uncrossing 等式與 e,f,g 的具名邊位置亦保留；它們提供一致性限制，最後
矛盾來自上述完整來源面鄰接，而不是拼接不同 matching witnesses。

本輪計算僅校準有限局部代數／拓撲：

| 證據 | 實際驗證域 | 不代表 |
| --- | --- | --- |
| [check.py](check.py)、[certificate.json](certificate.json) | 原扇區字串算術；W5 全部 32 個 port fibres、21 個空 fibre、11 份內部 matching lifts | 原來源實現、一般拓撲的機器證明 |
| [check_radius2.py](check_radius2.py)、[certificate-radius2.json](certificate-radius2.json) | 具名 11 點／15 面 disk、五種外 facial ear、補外 W5 的 12 點／20 面全五度球面 | 假設來源的數值實例或有限枚舉排除 |
| 任意大小紙面證明＋獨立重建 | 原來源面、完整度數、扇區、曲率、返回定理 | 新 Lean 定理 |

數值原來源覆蓋仍為 `not triggered`，未提供或宣稱 synthetic 圖具來源契約。
原完整染色 fibres、空 fibres、所有合法 r lifts 及邊身份均未變動。

## 4. 精確剩餘 OPEN 與下一入口

* 101 普通失敗：僅剩一個非完整 W7 的七割 factor-critical 分量，
  其他奇分量均單點；原 f 仍連接不同奇分量，整個 `P111` 仍逐割 tight。
* 110：其餘非輪五割、雙五割與非輪七割來源障礙未由本輪排除。
* 普通族非空後的偶補正值、`W110+W101>0`、完整 319 及一般無界命題仍 OPEN。

下一研究入口是原 101 非輪七割的實際割與 factor-critical 內部結構，
保留同一 `P111` 與具名 f 端點；不能直接把七割當完整輪或 disk。
來源接回成本仍 k+5，一般 `K≤22=K≤5` 與固定 r6 的 `k≥25` 不變。

## 5. 驗證、交接及版本狀態

重播、負控制、Lean build、文件驗證與既存失敗的確切範圍見
[VERIFICATION.md](VERIFICATION.md)、[verification-runs.json](verification-runs.json)
及 [MANIFEST.json](MANIFEST.json)。封存 checker 是 custody 驗證，不是紙證檢查器。

已更新 Kempe 導覽、STATUS、直接 C4 父題及 State 活躍入口；README、HANDOFF
的研究線與一般點數界經核對不需修改。原三輪報告／證書完全保留，從現行
索引標示後續涵蓋。影響傳播止於直接父題；一般主命題仍 OPEN。

未 commit、未 push；本任務未明確要求這兩項操作。當前版本以 Git 即時狀態為準。
