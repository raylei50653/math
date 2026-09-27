# Single-spoke：單接點未用色守恆與 p₂ 延拓

2026-09-27。接續 [旁支 minor 的停止點](c5_single_spoke_branch_minor.md)、
[外部雙路徑 completion](c5_single_spoke_completion.md) 及
[rooted palette 守恆](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)。
研究優先序見 [HANDOFF](HANDOFF.md)。

**指定 (012,04,234)、禁 3 者二接點的 p₂=01212 必延拓，且可取 z=3。**
單接點 C₁ 在 p₂ 不能禁 3；這一點來自同圖 block palettes 的未用色守恆，
不需新增拓撲分類。114 筆中 source_index 23、28 新增 p₂ 接受：兩列已證
64 → **66**，只證 p₁ 為 18、只證 p₂ 為 30，未決查詢 50 → **48**。
本輪只更新這兩筆，未新增 Lean theorem，也不宣稱全部 single-spoke 已完成。

## 1. 來源、接點與兩份拒絕證書

完整沿用 completion §1：有限簡單 induced-C5 disk 圖，連通有效內點 H，
edge-minimal q=01012 obstruction，唯一完整 degree-5 點 z、唯一 spoke zb0，
其餘內點完整 degree=4；H−z 的接點分拆 (2,1,1)，來源接受 T4。
按 q 禁色命名 C₁、C₂、C₃，實際支援分別為 012、04、234。
C₁、C₂ 各一接點，C₃ 有兩個原有序接點；全部原邊、支援與環序保留。

令 C=C₁，r 為它唯一的 z 接點。已知 F_C(q)={1}。
反設 3∈F_C(p₂)。依 [R10 §2](c5_degree5_interfaces.md#2-gallai-結構tight-lists-與-block-palettes)，
同一 C 的 M=(q,z=1) 與 N=(p₂,z=3) 都是拒絕的 tight degree lists，
各自具有 block palettes Q_K、P_K。既有 connected-exterior K4 排除與
Gallai 結構給 blocks 只有 bridges、odd cycles，大小分別為一色、兩色。
外部 degree-list 定理沿用 R10，沒有在本輪重新證明。

## 2. 單接點固定色引理

更一般地，設同一個有限連通單接點分量的兩份拒絕 lists M、N 具有上述
block palette 證書。若對每個 v≠r，色 d 在 M(v)、N(v) 的 membership
相同，則它在 M(r)、N(r) 的 membership 也必相同。

證明：將 block-cut tree 以 r 為根。對每個 block K，取其遠離 r 的任一
非 parent 頂點 v。從葉 block 向根歸納，v 的所有 child-block palettes
對 d 的 membership 已相同。兩份 lists 都是 incident palettes 的不交聯集，
所以扣除這些 child palettes 後，剩下的 Q_K、P_K 對 d 的 membership
相同。每個 block 都至少有一個這樣的 v，且 v≠r；既有證書保證選點相容。
到 root 時，它的 list 就是所有 incident block palettes 的聯集，故 membership
相同。若 C={r}，拒絕 tight lists 皆為空集，結論仍成立。

此歸納保留原 block tree，容許任意深度、分叉、bridge 長度與 odd-cycle 長度。
它使用兩份**已存在**的拒絕證書，不從任選局部 palettes 推論全圖可實現。
單接點至關重要：第二個接點會使非 root list 因 z 色改變，不能直接套用。

本題 q、p₂ 都沒有使用色 3。對 v≠r，它沒有 z 邊，所以

```
3∈M(v)，3∈N(v)。
```

但 root 在 M 只額外刪去 z 色 1，因此 3∈M(r)；在 N 額外刪去 3，
因此 3∉N(r)，與引理矛盾。故 **3∉F_C₁(p₂)**。
此證明保留 b0、b1、b2 的全部實際接線；不要求 q／p₂ 的其他色 membership
一致，也不將 b0、b2 合併。這個 root 結論本身不需要 C₂／C₃ 的嵌入次序；
原 disk／支援條件仍用於前置結構及下一節的 completion。

同理可得通用充分條件：若兩列在 C 的實際 boundary 支援均未見 d，
第一列禁某 a≠d，則第二列不能禁 d。下一輪可用此條件檢查既有表；
本輪不預先計入其他接受查詢。

## 3. 在原圖取共同 z=3

C₂ 在支援 04 上的 q、p₂ 顏色一致，故 F_C₂(p₂)={2}。
C₃ 的外部雙路徑由 C₁ 通往 b1、C₂ 通往 b4；它們內點分屬不同原分量，
所以 completion 已給 F_C₃(p₂)∩{0,3}=∅。C₃ 的完整二接點關係及兩座標
保持原樣，沒有以兩個 marginals 取代它。

p₂(b0)=0，故 z=3 合法；三個分量都不禁 3。按 F 的定義，每個原分量
各存在一份全部接點避開 3 的完整 tuple 及其內部 coloring。固定同一 p₂、
同一 z=3 後接合即得原 G 的延拓。p₁ 已由原表證明。
這只排除額外拒絕 p₂，不排除此支援型的 q-obstruction 或證明其可實現性。

## 4. 有限重播與證據界線

[checker](../scripts/c5_single_spoke_root_conservation.py) 與
[artifact](../artifacts/c5_single_spoke_root_conservation/observations.json) 保存：

- 2,632 個非 root 固定色遞迴局部核對（每色 658），以及 1,340 個 root
  聯集核對（每色 335）；同一位置的 block 大小一致，palettes 兩兩不交。
- root 在 012 中的全部 8 種實際接線子集；逐一核對兩份 root lists 的色 3
  差異，並標記 tightness，包含已因 slack 不可能的 singleton 情形。
- 繼承 114 筆具名支援及原 placements，只更新 23、28；保存輸入 SHA256、
  completion 的分量身份核對及共同 z=3 witness。

局部核對不是來源圖 cover；任意大小的結論由 §2 的有限 block-tree 歸納承擔。
信任層是紙面證明＋沿用外部 degree-list／既有結構定理＋Python 局部代數。
沒有新增 Lean theorem；`lake build` 通過不表示此歸納已形式化。

```bash
python3 scripts/c5_single_spoke_root_conservation.py --check
python3 scripts/c5_single_spoke_branch_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際驗證见 [研究紀錄](history/2026-09-27-single-spoke-root-conservation.md)。
下一步先將 §2 的通用條件作用於原 114 筆的單接點分量及兩個指定 p，
與既有完整關係／completion 上界合用；只更新可證的接受查詢，反射仍沿用
既有正式搬運，不重枚舉來源。其餘 t=1 分拆、t=0、高 degree／多 degree-5、
一般核心存在／分離、單側／共同出口與 K∞=K≤5 仍保留。
