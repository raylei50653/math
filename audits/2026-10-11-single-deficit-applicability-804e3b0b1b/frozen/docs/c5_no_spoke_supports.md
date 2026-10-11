---
docgraph:
  id: c5.no-spoke-supports
  family:
    - c5
    - c5.no-spoke
  requires:
    - c5.no-spoke-exterior
    - c5.single-spoke-cores
    - c5.single-spoke-completion
    - c5.single-spoke-single-contact-bounds
---
# No-spoke：環狀實際支援與 (2,1,1,1) 指定雙列分離

後續（2026-09-28）：[首橋與固定框弧](c5_no_spoke_first_bridge.md) 已關閉最後
12 個指定查詢；來源排除仍 500 筆，保留 116 筆全部接受雙列、0 查詢未決。
唯一 degree-5 全部分支已接回條件式出口；必要型可實現性、完整 Σ 與 Lean
形式化仍未完成。下列數字及停止點保留各原輪語境。

後續（2026-09-28）：[原外部路徑 K5](c5_no_spoke_path_minor.md) 已在 q 下
排除 record 599 及 500 筆來源；其餘 116 筆新增 104 個延拓，現為
108 筆雙列已證、12 個查詢未決。下文與原 artifact 保留當輪 616 筆
及 record 599 停止點的語境；(2,1,1,1) 的 48 筆結論不變。

2026-09-28。接續 [外部連通與兩個保留分拆](c5_no_spoke_exterior.md)；
研究優先序見 [HANDOFF](HANDOFF.md)。

**t=0、(2,1,1,1) 的 T4-accepting minimal q-core 必接受
p₁=01021、p₂=01212。** 四個禁色角色的實際支援只剩兩種必要配置，
保留二接點分量的任一角色與三個單接點分量的具名身份，共 48 筆。
這完成該分拆的指定分離，可接回條件式單側出口；不是來源不存在或
完整 Σ／可實現性分類。

同一環狀次序引理也把 (2,2,1) 化為 1,952 筆必要支援，T4 排除後剩
616 筆，其中 268 筆已證雙列。其餘仍保留，沒有完成此分拆。
證據為任意大小紙面化約、外部 degree-list 定理、既有 degree-4 completion
與 Python 有限表；沒有新增 Lean theorem。

## 1. 前提與完整關係

沿用 [前報告 §1](c5_no_spoke_exterior.md#1-同一來源與完整禁色覆蓋)：
有限簡單 induced-C5 disk，框 B=(b0,…,b4)，有效內部 H 非空連通，
edge-minimal q=01012 obstruction；唯一完整 degree-5 點 z 沒有 boundary
spoke，其餘內點完整 degree=4。H−z 的原分量 Cᵢ、五個具名接點、全部
原附件、bridges、嵌入與 tuple 座標保留。每個分量的 actual support 為
Sᵢ={j:N(bⱼ)∩Cᵢ≠∅}，不是可用支援的超集。

本輪在指定 p 分離時另假設來源接受全部 T4。幾何化約與 §2 不需 T4。
Rᵢ(b) 是同一 Cᵢ 的完整有序接點關係，Fᵢ(b) 是所有 tuple 色集的交集。
未指定 z 色時，接點提供 slack，故 Rᵢ(b) 非空、|Fᵢ(b)|≤|Pᵢ|，且

```
b 延拓原圖 ⇔ U \ ⋃ᵢFᵢ(b) 非空，  U={0,1,2,3}。
```

這裡的接合先固定同一 b、同一 z 色，再各選一份完整 tuple 及其 coloring。
不乘 endpoint marginals，也不將支援表當作可迭代的完整關係 state。

沿用前報告的外部連通與 K4 排除，各 Cᵢ 都是 K4-free Gallai tree。
拒絕 lists 的 tightness 及 blockwise palettes 使用外部
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪已核對原文；此外部定理不算作 Python 或 Lean 證明。

## 2. 每份支援至少兩點，且有環狀區塊次序

固定 q 在 Sᵢ 上的每個色置換都保持整個 Rᵢ(q)，所以保持 Fᵢ(q)。
若 |Sᵢ|=1、該點色為 a，另外三色形成同一 orbit；因 Fᵢ 非空且容量≤2，
只能有 Fᵢ={a}。但此時固定 z=a 的所有外部色只有 a。
tightness 使每點最多一個外鄰居，故 deg_C(v)≥3；有限 K4-free Gallai
tree 的 leaf block 卻有 degree≤2 的非 cut 點，矛盾。singleton C 也明顯
不可能。因此 **|Sᵢ|≥2**。更一般地，每個 a∈Fᵢ 都須滿足
|q(Sᵢ)∪{a}|≥2，checker 逐色核對。

**環狀次序引理。** 可按原 z-contact 區塊的環序排列各分量，並把每個
Sᵢ 提升為整數集 Tᵢ，使某個起點 a∈{0,…,4} 下有

```
min T₀=a， max Tᵢ ≤ min Tᵢ₊₁， max T_last ≤ a+5，
Tᵢ mod 5 = Sᵢ，  max Tᵢ−min Tᵢ > 0。
```

分量標號固定；選 C₀ 作第一塊只消去環序的起讀位置。等號保留不同分量
共用同一 bⱼ 的可能，並不複製框點或更換其顏色。

證明：刪去 z 的小開圓盤，原 contact 邊終於內圓周，得到 annulus。
每個 Cᵢ 加截短 contact 邊及實際 boundary 邊，連通且碰內外兩圓周。
在每個 bⱼ 的小鄰域分開入射邊端，仍把它們記作同一原框點。
不同分量的這些連通集合兩兩不交。

若某 C 的 contact 區塊夾住另一 D，取 C 中連接兩 contact 的簡單路徑，
與其兩條 z 邊成 Jordan 曲線。曲線全在原 disk 內，B 在同一外側；
被夾在無 B 側的 D 無法連到 B，矛盾。故各 contact 成一個環狀區塊。
對外圓周同理：在 C 中連接兩條實際 boundary 邊的路徑是 disk crosscut；
不含 z 的一側不能包含任何另一分量的 boundary 附件，否則該分量到 z
的原路徑必穿越 C。因此各分量的外圓周附件也成同序的環狀區塊。
兩圓周的次序須相容，否則分別在兩個分量中取 contact-to-boundary
路徑，會形成交錯且不相交的 crosscuts。這些 Jordan 論證保留任意
block 數、旁支與臂長。共享 bⱼ 的入射次序在其小鄰域分開後適用同證。

各區塊從第一個實際支援到最後一個實際支援的閉弧，其開邊段兩兩不交；
選 C₀ 第一個端點為起點即得上述提升。一份支援的兩次同點端位只會在
整圈跨度時出現；其餘至少兩個正跨度分量排除此事。因此每份 Sᵢ 的
不同框點恰各提升一次，跨度總和≤5。

checker 用「依次提升整數區間」生成，另用「所有 cyclic hull 的框邊
mask 互斥」獨立重算同一有限域。三分量有 480 份、四分量有 360 份
幾何支援 tuple；每份恰一個以 C₀ 起讀的區塊序。
這不是來源 disk 實現證明。每個二接點的兩種內部方向均保存；五個
具名原接點沒有被收縮成三或四個虛擬接點。

## 3. (2,1,1,1) 的四型縮成兩型

依前報告，四份 Fᵢ(q) 恰為不同 singleton。以 a 命名禁 a 的分量 C_a，
仍另記哪個 C_a 有二接點。C₃ 的支援必見 q 的 0、1、2：少一色 h 時，
交換 h、3 會違反 F₃={3} 的不變性。因此 C₃ 的跨度至少二，另外三份
至少一；總跨度≤5 迫使大小恰為 2+1+1+1、沒有間隙。

C₃ 必佔三個連續框點且三色皆見；可能為 234、340、401。若為 340，
b4 在該弧內部，其他三分量不能碰 b4；但 F₂={2} 迫使 C₂ 碰 b4，
矛盾。所以 C₃ 只有 234 或 014，C₂ 相應為 04 或 34；C₀、C₁ 佔另
兩條框邊。這給以下四種實際支援，不是獨立任選每份支援。

| 型 | S₀ / S₁ / S₂ / S₃ | T4 控制 |
| --- | --- | --- |
| I | 01 / 12 / 04 / 234 | 保留 |
| I′ | 12 / 01 / 04 / 234 | 必拒絕 01213 |
| II | 12 / 23 / 34 / 014 | 保留 |
| II′ | 23 / 12 / 34 / 014 | 必拒絕 01023 |

兩份拒絕見證只用全分量換色：I′ 在 01213 的四份禁色依序為
{2},{1},{3},{0}；II′ 在 01023 為 {0},{1},{3},{2}。均覆蓋 U，
與 T4 acceptance 矛盾，與二接點是哪個角色無關。

每型有四種二接點角色及 3! 種具名單接點排列，所以原 96 筆排除 48，
保留 I、II 的 48 筆。不能將此數字稱為圖的數目。

## 4. 兩型的 p₁、p₂ 延拓

| 型 | p₁ 可固定的 z 色 | p₂ 可固定的 z 色 |
| --- | ---: | ---: |
| I | 2 | 3 |
| II | 3 | 0 |

I 的 p₁：四份支援均有相容色置換，禁色依序為 0、1、1、3，故可取 z=2。
II 的 p₂：同理禁色為 2、1、2、3，故可取 z=0。

I 的 p₂：C₀、C₁、C₂ 分別禁 0、1、2。若 C₃ 是單接點，p₂ 在 234
只見 1、2，未見色 0、3 可互換；容量≤1 迫使兩者都不在 F₃(p₂)，
故取 z=3。II 的 p₁ 同理：前三份禁 0、2、1，C₃ 在 014 未見 2、3，
若是單接點便不禁 3。這先完成 36 筆雙列及另外 12 筆的一列。

剩 I／p₂、II／p₁ 且 C₃ 二接點，共 12 個具名查詢。
對 I，在**另一原分量 C₁** 內取原 contact 到實際 b1 鄰點的簡單路徑，
加首末邊得 z–b1；在 **C₂** 內同樣取 z–b4。兩路除了 z 外不交，
避開 C₃ 及其他 boundary 點，恰滿足
[外部雙路徑 completion](c5_single_spoke_completion.md#1-前提與保留的完整關係)。

該引理的局部前提只有：C 二接點、S_C⊆1234、F_C(q)∈{{0},{3}}，以及
上述兩條實際外部路徑。其證明保留整個 C，再收縮外部路徑得到 z 的
兩條 spokes；不使用原圖已有 spoke、原 z degree、或外部只有兩個分量。
故這裡直接適用，得到 F₃(p₂)∩{0,3}=∅。C₀ 仍作原獨立分量參與最後
接合，沒有被替換成 spoke，亦沒有改動任何原 Rᵢ。

II 的 p₁ 由既有全圖反射搬運：ρ(i)=3−i、π=(0 1)，Tq=q，
Tp₁=21010=(0 2)p₂。II 的角色與支援反射成 I；在反射來源先用 p₂
引理，再以整份 relation 的全域色置換 (0 2) 得 Tp₁ 的禁色界，最後
搬回原圖。原 F₃(p₁) 不含 2、3，故仍取 z=3。
不是只把 target 正規化而固定其餘色框。

**任意大小結論至此完成。** 收縮外部路徑與既有 degree-4 結構定理的
來源覆蓋仍為紙面證明；既有 3,492 接線的完整 ordered tuples 本輪全部
重播。有限接線不是任意大小覆蓋的替代證明。

## 5. (2,2,1) 必要表與停止點

對前報告的 48 份具名禁色覆蓋，套 §2 的支援穩定子、外部至少兩色與
環狀次序，得到 1,952 筆必要表；1,336 筆有具體 T4 拒絕列，保留 616。
所有判定均由同一份 actual support 上的全分量換色取得。

未知 Fᵢ(p) 保留為**整份集合的候選**：容量≤接點數，且在未見色的
置換下不變；單接點另用
[未用色角色守恆](c5_single_spoke_single_contact_bounds.md#2-未用色在單-root-的禁色角色守恆)。
若 c 在 q、p 支援都未見，q 禁 a、p 禁 d 必有 a=c ⇔ d=c。
對符合局部前提的二接點分量，再用 §4 的外部路徑引理；兩條路徑須來自
不同的其他原分量，只有一個其他分量同時碰兩端時不作判定。

將整份 F 候選接合：若無任何選擇可覆蓋 U，證 p 延拓；若已知的精確
F 已覆蓋 U，記為 `reject`；其餘為 `unresolved`。保留的 F 候選只是
必要上界，不斷言它們或它們的任意組合可在來源圖實現。

| p₁ / p₂ 判定 | 筆數 |
| --- | ---: |
| accept / accept | 268 |
| accept / unresolved、unresolved / accept | 各 116 |
| unresolved / unresolved | 32 |
| accept / reject、reject / accept | 各 10 |
| reject / unresolved、unresolved / reject | 各 26 |
| reject / reject | 12 |

共 788 個接受查詢、348 個未決查詢及 96 個條件式拒絕查詢。
最後一類的意義是「若此 necessary support 型有來源，則該列拒絕」；
**不是已找到反例**。未完成的指定分離查詢合計 444，仍可能由來源
非平面性或跨列 palette 相容性排除。外部 completion 新增 28 個接受查詢，
未改写前序 single-spoke artifacts。

下一窄入口固定為新表 **record 599（zero-based）**：

```
接點分拆 (2,2,1)
(F₀,F₁,F₂)(q) = ({0,1},{0,2},{3})
(S₀,S₁,S₂) = (012,04,234)
p₁ 已可取 z=2；p₂ 仍未決。
```

在 p₂，F₁={0,2}；單接點 C₂ 的未用色守恆給 F₂⊆{3}，而支援只見
1、2 的色對稱又排除 3，故 F₂=∅。若仍拒絕 p₂，必有
F₀(p₂)={1,3}，逐接點解除給原有序關係恰為 {(1,3),(3,1)}；q 下
原關係恰為 {(0,1),(1,0)}。下一步須比較**同一 C₀、原接點與完整
012 附件**的兩份拒絕，保留 C₁ 通 b4、C₂ 通 b2／b3／b4 的實際路徑。
不把原二接點禁兩色情形塞進只允許 q 單禁色的 completion。

## 6. 證書與重播

[checker](../scripts/c5_no_spoke_supports.py)、
[JSON](../artifacts/c5_no_spoke_supports/observations.json) 保存：

- 兩種獨立幾何枚舉一致、全部 2,048 筆必要記錄、T4 拒絕見證，
  664 筆保留記錄的兩個 target；各具名分量、支援、整數提升及五接點環序。
- 每列的相容色置換、完整 F 候選、容量接合、可固定 z 色與實際路徑
  來源。每筆都有反射支援及字面 transported targets，不合併 tuple 座標。
- 全部 15 份非空 unary、65,535 份非空 binary 關係的容量、接合與反射；
  {(0,3),(3,0)} 的 marginal 乘積失真負控制。
- 重播原 root 歸納局部核對與全部 3,492 份 degree-4 completion 接線；
  交錯支援及把同一分量誤當兩條不交路徑的負控制。

輸入 SHA256 綁定前序 artifacts 及實際使用的 checker；前序檔只讀。

```bash
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑項目見 [本輪紀錄](history/2026-09-28-no-spoke-supports.md)。
`lake build` 不形式化本輪環狀拓撲、外部路徑抽取或指定分離。
一般單側／共同出口、degree≥6、多 degree-5 及 `K∞=K≤5` 仍未證。
