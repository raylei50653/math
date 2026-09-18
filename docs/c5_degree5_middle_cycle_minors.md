# 中間二接點三環鏈：任意長來源 minors 與拓撲合成

2026-09-18，R30。接手 HEAD `e14874d` 與未提交 R24–R29。
**兩個不同私有接點都在中間環的共用點三奇環鏈，任意環長與外臂長度
可縮到 R29 的 C3–C5–C3 正常形，因此在下述前提下排除。**
這是紙面構造＋Python 有限來源證書，未新增 Lean theorem；一般三環仍未排除。

前提沿用 R28／R29：唯一 degree-5 點 z 有三條 boundary spokes，其餘
有效內點完整 degree=4，來源為接受全部 T4 的 C5 disk minimal
q-obstruction；分量的三環滿足 J1∩J2={r12}、J2∩J3={r23}、
J1∩J3=∅、r12≠r23。兩條外臂分別進入 J2 的不同私有點 p1,p2。
先沿用三-spoke 區域定位及 forcing-list 正規化；外枝由既有
單 bridge 強迫色化約處理。本輪來源控制從該正規化圖開始。

## 1. 保留四標記與 palette 錨點

固定 q=(A,B,A,B,C)、D=3。R28 完整接合判準強迫三環的有效 palettes
為 T–S–T，其中 T=U\S。兩個接點原 list 為 S∪{ci}，ci∈T；
臂在 z=D 時強迫 ci。共用點 list 為 U，其他私有點為其環的二色 palette。

每個末端環保留共用點及任意兩個私有 T 點，縮成 C3。中間環保留
r12、r23、p1、p2，以及任一其他私有 S 點。四標記互異，原奇環
長至少五，所以第五個點必存在；縮後為 C5。

對每個環，依來源循環次序記保留點 v0,…,v(m−1)，m=3 或 5。
將 vi 至 v(i+1) 的開 arc 內點全部收進 vi 的 branch set，刪除這些
內點的 boundary attachments 及私有 D 葉，保留 vi 的 attachments。
arc 的末條邊實現目標相鄰保留點之邊。每段長度只須為正，**不要求
逐段為奇數**；來源環及目標環總長皆奇數即可供 list 判準使用。

兩環在共用點分配的 arc 聯集仍連通，且只在該共用點相交。
各 branch set 恰含一個保留點；所有集合非空、互斥、連通。
兩個共用點不合併，兩接點不合併，boundary 與 z 均為 singleton。
每個環可分別縮減，三環任意順序的合成 branch sets 相同。

旋轉目標中間環使 r12 位於 slot 0，r23 位於其餘四個 slots 之一；
依 slot 順序命名兩接點，其臂隨接點一起搬運。未標記的第五點為 S
錨點。這恰落在 R29 的 12 個具名位置域，不改變 boundary 標號或
同色 spoke 的實際端點。末端 C3 的兩個私有點均保留 T attachments。

## 2. 外臂縮減與真正來源 minor

沿用 R27 的閉色段縮減，但固定核心現在有九個環點（C3–C5–C3），
不是七個。臂序列 w=(D,…,c) 的相鄰不同色對對應二色 list 臂點。
若 wi=wj、i<j，替換為 w[:i]+w[j:]。以 p0=z,p1,… 為實際臂點列，
保留 pi，將 pi+1,…,pj 收進其 branch set，刪除被吸收點的 attachments
及私有 D 葉；保留 pi 的原 attachments。其餘臂點重編號時，實際
boundary 端點與 D 葉來源一併搬運，不能重新選擇接線。

每步嚴格縮短，終止於四色不重複的簡單序列。終色 D 的臂可全部收進 z；
兩臂同時收進 z 時聯集仍連通。故 boundary 固定，但不要求 z 的
最終 branch set 為 singleton。縮臂不吸收任何環點，所有四標記與
palette 錨點保持分離。最終圖的 lists、臂序列及實際接線均屬 R29 域。

## 3. 四列、degrees、minimality 與非 disk 合成

每個中間圖的共用點仍有四條環邊；接點為兩環邊、一臂邊、一禁色
attachment；其他私有環點與臂點為兩骨架邊、兩禁色 attachments。
D 葉 degree=4，z 有三 spokes 與兩臂邊，degree=5。

任意子集縮環後仍保留所有接點與固定 palette 錨點。依 R28 的
Q(a)=R2(a)∩(E1(a)×E3(a)) 接合判準，四種 z 色的可延拓布林值保持。
縮臂後 D 仍輸出原終色 c；輸出該指定 singleton 的反向輸入唯一，
其他 z 色不會再同時形成 T–S–T 拒絕條件。因此每階段完整 F={D}。
這不聲稱 Q(a)、任意 pinning、完整 Σ 或所有 T4 rows 保持。

每階段 q 不可著色。刪除碰到 degree-4 分量的任一邊，沿用 R11
分量解除引理，在 z=D 時可延拓；刪 z 的 boundary spoke 則釋放其
非 D 色，該列已可延拓。因此重新得到每階段的逐邊 minimality，
不以「minor 自動保持 minimality」為理由。有限控制另直接保存並核對
每條非 boundary 邊刪除後的完整 q-coloring。

在最終圖加一個接全部五個 boundary 點的 apex。從其實際 R29 模板
的已存 subdivisions 中挑出適用者，直接驗證路徑邊、branch 模型和
內部互斥。將 subdivision 收成 K3,3 minor，再與來源→目標的 branch
sets 合成；apex 對應來源 augmentation 的單獨 apex。逐條驗證來源
實際邊，得來源 augmentation 的 K3,3 minor。若來源是 C5 外邊界 disk，
此 augmentation 必 planar，矛盾。

任意長度結論來自上述一般 branch-set 構造、R28 判準及 R29 全部正常形
覆蓋。下一節的有限來源控制核對實作，不是任意長度的枚舉證明。

## 4. 有限來源控制與重播

[checker](../scripts/c5_degree5_middle_cycle_minors.py)、
[certificate](../artifacts/c5_degree5_middle_cycle_minors/observations.json)。
按 12 位置×6 palettes×兩臂各自 2 終色分成 288 桶，每桶選一個
seed；隨位置與桶交替選最短／最長臂。每個 palette／終色桶跨位置
均測兩種選擇。加入前綴或後綴閉段，後一型另加 D 前綴閉段，涵蓋
整條 D→D 臂與內部閉段。縮後依實際簡單序列重新定位 R29 模板。

三環長度採 (5,7,9) 或 (7,11,5)。中間五段分別為 (1,2,1,2,1)
及 (2,1,3,2,3)，包括偶數 arc；末端三段亦混用奇偶長度。
每個來源直接核對全部八個縮環子集、十二個逐步 minor、六種縮環
順序的合成相等，再逐步縮兩臂，驗證 boundary singleton 與環點分離。
所有圖階段均查四列 F、degrees、q 拒絕及全部非 boundary 邊刪除著色。

生成與 `--check` 都禁用 NetworkX planarity APIs；只使用 R29 已存路徑。
記錄載入本地程式 hashes 及 R29 artifact hash，並驗 R29 的程式指紋。
`--check` 唯讀重建全部本輪證書，逐 byte 比對 JSON。數字與實際驗證
見 [STATUS §34](STATUS.md#34-r30-中間二接點三環鏈來源-minors)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_middle_cycle_minors.py --check
lake build
git diff --check
```

R29 全部 19,693,824 接線覆蓋與 R28 standalone checker 本輪未重跑；
引用既有覆蓋及紙面判準，直接核對本輪每個使用的 subdivision。
R27／R26、R15／R17／R19 大覆蓋亦未重跑；未修改既有 scripts／artifacts。
Lean build 不代表本輪紙面 minor 或拓撲證明已形式化。

## 5. 精確停止點

R27 末端各一臂鏈型與本輪兩個不同中間接點鏈型已排除。
下一個窄問題是同一共用點鏈的**同末端兩個不同私有接點**：沿 R28
保留兩接點與共用點的 C3–C3–C3 目標，建立實際接線及完整四列／
minimality，再找完整拓撲覆蓋或具體障礙。不能直接刪無接點末端環，
也不能引用 R26 的末端各一臂拓撲域作此新位置的覆蓋。

末端與中間、同點會合的圖層排除、環間 bridge 三環型、其他分拆 (2)
及一般三環仍開放。一般 degree-5／degree≥5、單側／共同出口、候選 A、
weak-deletion congruence 及 `K∞=K≤5` 仍未證。本輪未 commit／push。

後續 [R31](c5_degree5_same_terminal_triangles.md) 已完成同末端不同二接點的
C3–C3–C3 簡單臂正常形接線與拓撲覆蓋；此型任意長來源 minors 仍待補完。
