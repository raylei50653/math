# 同一狀態的 Kempe 交換系統：720-state 完整殘留證書

2026-10-15。BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
獨占本目錄；原來源、第一輪交付與輸入雜湊見 [INPUTS](INPUTS.json)。

**新增一個比共同計數更強的方法界線：下列交換公理全部同時施加，原22列仍全部保留。**

已構造720個有固定字面色框的 abstract states；每個 state 同時帶六色對的
terminal component partitions，而且保存全部交換後繼。完整驗證包括：

- 同一 complementary pairing 交換前後，兩份partition均不變。
- 每個 component 交換可逆；同一pairing的全部component交換可交換，所有
  子集組合均符合 XOR，直接核對202,752條組合等式。
- 全域S4改色同時搬運state、partition及switch，核對51,840份partition
  搬運與153,216份單步switch搬運。
- 同一色對的全部component交換等於全域該兩色交換；任意跨pairing交換序列
  都在同一720-state系統內有定義。

證書覆蓋原26列必要表經既有固定點留下的**全部22列**，完整外框支持仍為319。
它由18列×24的主層與四個3列×24的小層組成，沒有把不同pairing的獨立
終點witness拼作真圖。每個state的三份partition與所有後繼均明列於
[certificate](certificate.json)，[checker](check.py)可從零重建。

這只建立上述抽象交換公理的一致性，**沒有建立不同色對在同一原邊集合上的
真圖相容性**。沒有保存隱藏頂點、共同原邊incidence、完整collar與來源度數；
因此來源仍是 `not triggered`。作為防誤讀控制，checker更證此支持不可能是
僅含這七pins的任何圖之完整關係：所有可允許原邊只有八條骨架邊，但它還
允許證書外的 `ABABCBD`。這也沒有排除增加內點後的實現。

[PROOF](PROOF.md)明列actual-graph交換定律、hidden components界線與完整構造。
原count證書只承諾row multiplicities；其所選partition decomposition未必S4
協變，不代表舊證書錯誤。本輪重選partition並以完整state id核對。

正常、`PYTHONHASHSEED=17`、兩種損壞證書及exclusive-create負控制均已執行，
詳見 [VERIFICATION](VERIFICATION.md)。原權威輸入與保存證書重播前後不變。

下一個實質義務是加入「全部六色對component來自同一原圖」的共同邊／路徑
身份限制，或真正原collar與degree接線。單靠本輪已驗證的可逆性、同pairing
可交換性、逐state多色對資料及S4協變，不能再縮原22列。

來源319排除、偶補存在、一般主命題、原點數界均未改變；未新增Lean，未commit／push。
