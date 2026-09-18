# 三環共用點鏈：完整二接點介面與四列縮環

2026-09-18，R25。接手 HEAD `e14874d` 與未提交 R24；本輪未 commit／push。
處理 J1–J2–J3 共用點鏈，r12≠r23，兩外臂分別落在末端環私有點。
所有環為奇環；共用點原 list 為 U，各私有非接點為二色 list，
末端接點原 list 為三色。外枝已按既有 forcing-list 正規化。
這是 **fixed-q 紙面介面＋Python 有限控制**，沒有新增來源 minor、
minimality、disk 排除或 Lean theorem。

## 1. 完整有序關係

固定 z=a。兩末端環交回共用點的完整 root 色集為 E1(a)、E3(a)，
由 R23 root 剛性皆至少二色。中間環兩共用點自由，記其有序關係
R2⊆U×U；正確接合為

```
Q(a) = R2 ∩ (E1(a) × E3(a))，可延拓 iff Q(a) 非空。
```

沿中間環兩端點間的兩條 arc 分別做 path transfer，兩個 path relations
取交集就是 R2；checker 等價地固定兩端色後傳遞整個 cycle，且用獨立
暴力 coloring 核對全部 C5 控制。不以兩個邊際投影取代 R2。

## 2. 拒絕的交替 palette 剛性

基本 list 引理：奇環每點 list 至少二色時，不可著色 iff 所有 lists
都是同一二色 S。若相鄰 lists 不同，選定方向及起點，使起點含一色
不在末點 list；先用該色再沿路徑 greedy，末點自動不撞起點。
若所有 lists 相同且至少三色，用三色著色奇環；共同二色則因奇偶性失敗。

把中間環端點 lists 換成 E1(a)、E3(a)，其餘不變，即得：

```
Q(a)=∅ iff E1(a)=E3(a)=S，且 J2 每個私有 list 都是 S，|S|=2。
```

由 [R23 §1](c5_degree5_shared_cycle_roots.md)，E1=E3=S 又等價於
兩末端環所有有效私有 lists 均為 T=U\S。因此拒絕 D 強迫
**T–S–T** 交替 palettes，無需假設中間環的兩個 root 獨立。
末端接點原 list 為 T∪{c}，其中 c∈S，D 列外臂必輸出 singleton c。
外臂的指定 singleton 有唯一反向輸入（R20 path-transfer 性質），
因此 a≠D 時標記 list 不再等於 T。末端至少保留一個未標記 T 點，
其 root 若為二色只能是 S，而此時已不可能；故另外三列均可延拓。
**完整 F={D}**，不是只檢查 D 列。

## 3. 可保持的縮環語義

末端環保留共用點、外臂接點及一個 T 錨點；中間環保留 r12、r23
及一個 S 私有點。在 list 層替成三個 triangles，仍用同一臂 profile。
對任意 a，末端 root 等於 S 的充要條件不變，中間環共同 S 的條件
不變。故四列可延拓布林值及 F 相同，任意子集的環先替換亦成立。
這是任意奇環長及接點位置的紙面論證，不以有限長度驗證代替一般證明。

**R2 與 Q(a) 本身不保持；任意 pinning 亦不保持。**
證書保存來源／目標關係 bitmask（bit 4*x+y 表示有序對 (x,y)）、
一組可區分的 pin，以及實際耦合的 Q 改變。不能將此 list 替換當成
已完成的 graph minor 或完整 Σ 保持。

另有最小控制：中間 triangle lists=[U,U,{0,1}]，兩 root 的各自投影
都是 U；兩末端環私有 lists 都為 {2,3}，交回 E1=E3={0,1}。
兩邊獨立交集皆非空，但精確 Q 為空。因此邊際投影接合給出假陽性。

## 4. 有限控制與重播

[checker](../scripts/c5_degree5_three_cycle_roots.py)、
[certificate](../artifacts/c5_degree5_three_cycle_roots/observations.json)。
C5 中間環四種有序端點位置，三個私有 lists 各取全部 11 種至少二色
子集；每個完整 relation 與暴力 coloring 比對，再測全部 121 組
至少二色端點 lists 的拒絕充要條件。

三環控制採有序長度 (3,3,3)、(5,7,9)、(9,5,7)、(7,9,5)，每組
全部末端接點位置及中間第二共用點位置、六個 S，以及 R20 的 67 個
外臂 profiles 中所有 D 相容組合。核對四種 z 色及全部八種縮環子集。
有限控制域不是全部圖或接線的枚舉；一般結論由 §1–3 證明。
共 5,324 組中間環 relations、644,204 組端點限制、324,120 組四列查詢。
保存查詢 digest、來源與直接依賴指紋；`--check` 唯讀逐 byte 比對。

```bash
uv run python scripts/c5_degree5_three_cycle_roots.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_shared_cycle_minors.py --check
lake build
git diff --check
```

本輪新 checker 已唯讀逐 byte 重播通過，R24 checker 亦通過；
`lake build` 成功（8,822 jobs，僅既有 lint），文件連結與 whitespace 通過。
R15／R17／R19 大覆蓋及 R20／R23 standalone checker 未重跑；
既有研究 scripts／artifacts 未修改，未重跑無變更的 Lean axiom audit。

## 5. 精確停止點

下一步先處理上述三環鏈的 **三個 triangle 正常形**：保留兩個共用點
及末端接點，建立實際 attachments／臂接線、核對 degrees 與逐邊刪除
著色，再尋找可重播的 topology 排除或障礙控制。其後才將任意長環
的 boundary 固定來源 minors 接上。R15 雙環覆蓋不能直接當成三環覆蓋。
其他三環接點位置、一般更多環及 degree-5 分拆仍開放；`K∞=K≤5` 未證。

後續 R26 已完成上述三個 triangle 正常形的實際接線、四列、逐邊刪除
著色及完整有限 topology 覆蓋；見 [R26](c5_degree5_three_triangles.md)。
後續 [R27](c5_degree5_three_cycle_minors.md) 已補完此型任意長來源 minors
及拓撲合成；最新停止點見 [HANDOFF](HANDOFF.md)。
