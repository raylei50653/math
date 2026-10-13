# 任務 K′：單點對角 Kempe 轉運與 root-to-chain joint incidence

2026-10-04；分支 `task-kprime-diagonal-transport`，基準
`main @ 2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`。
任務入口：[Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口)；
前序：[任務 K 的語意、控制與缺口](c5_kempe_transport.md)、
[S935 校準](c5_shield_calibration.md)、[定理 B](c5_unary_shield_budget.md#4-定理-bhub-原則)。
本輪只新增 checker、本報告與本任務 artifacts；不修改導覽、STATUS、README、HANDOFF，
不 commit、不 push。

**結論：觸發停止條件，K′ 未決；沒有完成固定 933／941 來源排除。**
L1 有 2,112／2,304 筆一致指派。補上 Jordan 側別的紙面引理後，L2 仍有
**933：192 筆，941：384 筆**，全部為兩條對角鏈都斷開。
Σ=1012／935 的控制各有 192 筆 L2 指派；`P1-witness-001` 及 S935 的兩份實際
四色拒絕見證均逐點重現，沒有控制被排除。

具名停止指派為 [KD933-0001](../artifacts/c5_kempe_diagonal_transport/KD933-0001.json)
及 [KD941-0001](../artifacts/c5_kempe_diagonal_transport/KD941-0001.json)。
最小八頂點 disk 實現嘗試窮舉 500 個接法，得到 10 張滿足 degree、T4 及
Σ-critical 的 disk 圖，沒有完整 Σ=933／941 的圖。
這既不證明存活指派不可實現，也不構成圖層反例。
依停止規則不擴大 P、不增加私有頂點、不研究較少顏色或其他 root 型。

[Checker](../scripts/c5_kempe_diagonal_transport.py)；
[摘要與完整分組結果](../artifacts/c5_kempe_diagonal_transport/observations.json)；
[全部逐筆指派](../artifacts/c5_kempe_diagonal_transport/assignments.jsonl)；
[逐點控制](../artifacts/c5_kempe_diagonal_transport/controls.json)；
[八頂點實現嘗試](../artifacts/c5_kempe_diagonal_transport/bounded_realization.json)。

## 1. 前提、字面語意與證據層

G 為有限平面 disk 圖，指定外邊界 B=(0,1,2,3,4) 是 induced C₅。
P={p}，N(p)={a,b,z,w}，ab 是框邊；z,w 是相鄰、完整 degree 5 的內部 roots。
p 的完整 degree 為 4。按 p 的 rotation 命名 roots，使其循環順序為
(a,b,z,w) 或反向，對角對為 (a,z)、(b,w)。框與 root 名稱保留同一份染色與嵌入。

ψ 是 G−P 的合法四色染色，q=ψ|B 不在完整 Σ(G) 中。
ψ(a)=α、ψ(b)=β、ψ(z)=c_z、ψ(w)=c_w 四色互異，故 p 的 list 為空。
兩條對角鏈的色對 {α,c_z}、{β,c_w} 互補。
下文所有 components、root ownership 與 blocks 均取自**同一 ψ、同一 split**。
block 定義為實際 component 與 B 的交集；component 若不碰框，block 為空。

Σ mask 的第 i 位對應 [cells.json](../artifacts/c5_cells/cells.json) 的 `pattern_order[i]`。
所有合法字面框列共 240 份。本輪逐份枚舉，不做 D₅ quotient，也不以 S₄
quotient 減少枚舉；只在查詢 mask 時對整列作一次共同 S₄ 正規化。
933 的拒絕索引為 {1,3,4,6}，941 為 {1,4,6}，1012 為 {0,1,3}，935 為 {3,4,6}。

固定來源若另有每条非框邊 Σ-critical，則確實存在這種拒絕見證：
刪除任一 p 的接線 e，取 G−e 的新增框列 q 及其完整染色；限制到 G−p 即為 ψ。
若 ψ 可延拓 p，q 就已在 Σ(G)，矛盾。因此 ψ(N(p)) 必為四個不同顏色。
有限表只檢查必要條件，**q′∈Σ 不反推這份 ψ′ 能延拓**；其界線沿用任務 K §1。

| 證據層 | 本輪內容與界線 |
| --- | --- |
| 紙面 | §2 的引理 1–6，包括存在性方向與 L2 disk 側別；沒有證明剩餘指派可實現或不可實現 |
| 外部定理 | 只用經典 Jordan curve theorem 與 disk 連通外側；未使用四色定理 oracle，不依賴 hub／Gallai 新推論 |
| Python | 全部字面列、框邊、root 色序、完整 π 與 endpoint blocks；兩套 partition 生成器逐集合相等；三份實際控制與有限八頂點圖的完整 Σ／刪邊／rotation |
| Lean 普通證明 | 沒有新增 theorem；紙面引理未形式化，未執行 `lake build` |
| Lean `native_decide` | 沒有新增證書 |

## 2. 必要条件與 Jordan 側別引理

**引理 1（對角不並聯）。** (a,z) 的 {α,c_z} component 與 (b,w) 的
{β,c_w} component 不能同時連通。

*證明。* 若 a,z 連通，在該實際 component 中取一條簡單 a–z 路徑 Q。
Q 位於 G−p，因此 J=Q∪{zp,pa} 是平面嵌入中的簡單 Jordan 曲線。
p 的循環順序迫 pb、pw 的初段在 J 的不同側。
互補色對的 b–w component 與 Q 的頂點互斥，也不含 p，不能穿越 J。
若 b,w 連通就矛盾。∎

**引理 2（斷開端點的兩次交換）。** 若 a,z 不連通，分别交換 a 所在的
{α,c_z} component 或 z 所在的 component，得到的 ψ′ 都能延拓 p，故各自的
**字面**框列 q′ 必在 Σ(G) 中。b,w 對稱。

*證明。* 每次交換一個完整雙色 component 都保持 G−p 合法。
交換 a 的 component 時 z 不動，a,z 均取 c_z，b,w 仍取 β,c_w；缺色 α 可給 p。
交換 z 的 component 時 a,z 均取 α，缺色 c_z 可給 p。
四種鄰色原本互異，且另一對色完全不在交換色對內，所以其他鄰點不受影響。
由同一 ψ′ 的這個直接延拓得到 q′∈Σ(G)。逆向沒有被使用或證明。∎

**引理 3（斷開端點的非空、不同 blocks）。** 一條對角鏈斷開時，其兩端
components 的框 blocks 都非空且互不相同。

*證明。* a 的 component 自含框點 a，非空。若 z 的 component 不碰框，交換它
會保持 q′=q∉Σ(G)，卻由引理 2 得到 G 的合法延拓，矛盾。
斷開的兩個 components 頂點互斥，故其非空 blocks 互斥、不同。b,w 同理。∎

**引理 4（連通一側的 ownership）。** 若 a,z 連通，z 的 block 正是 block(a)，
而 b,w 必斷開，對 b,w 套用引理 2、3。若 b,w 連通則對稱。

*證明。* component ownership 的定義給出相同 block；引理 1 排除另側連通。∎

**一致指派（L1）。** 固定 (q, 有向框邊 ab, (c_z,c_w), π)，其中 π 是該 split
所有碰框 components 的完整 noncrossing partition，且框邊若兩端顏色屬同一對，
兩端強制在同一 block。各 root 指派到其色對的一個 block（指到 a／b 的 block
就是「同鏈」）。先容許空 root block，再由引理 3 刪去。
只允許三種情形：兩鏈均斷開、只有 a–z 連通、只有 b–w 連通。
每個斷開對的兩次必需交換均須送到 Σ 內；共有四次或兩次。
π 及 root ownership 必須共同指定，不能拼接各自存在的 marginals。

**引理 5（L2：disk 的連通對角側別）。** 若 a,z 連通，w 的 {β,c_w}
component 不碰 B；若 b,w 連通，z 的 {α,c_z} component 不碰 B。
因此題設拒絕見證中，兩條對角鏈必須都斷開。

*證明。* 仍取引理 1 的 J。**J 整體位於閉 disk 中**，disk 外部是連通的無界區域
且不碰 J。任何不在 J 上的框點都可由 disk 外側通往無窮遠，故全在 J 的無界外側。
b 顏色屬互補色對，不在 J 上，故 b 在外側；p 的交替 rotation 因而使 w 在內側。
w 的整個互補色 component 與 J 頂點互斥，不能穿越 J，全部留在內側。
它不能碰 B∖J；也不能碰 J∩B，因那裡全屬另一色對。因此其 block 為空。
這與引理 1 所迫 b,w 斷開以及引理 3 所迫 w block 非空矛盾。對稱情形同理。∎

J 可以碰到其他框點；證明不把某條簡單 a–z 路徑的框接點假定為整個 block(a)。
L2 在此刪除 L1 中全部單連通情形，兩鏈都斷開時不另造不存在的閉曲線。
該引理只需 disk、四色與 rotation，不使用 degree 5、T4 或 criticality。

**引理 6（存在性方向）。存在這樣的 P ⇒ 存在一致指派；且有 L2 指派。**

*證明。* 從同一 ψ 的兩個互補色對抽取所有碰框 components 與其完整 blocks，形成 π。
每個框點恰屬一個 block；每個 block 顏色屬其中一對。
若有四個循環交替的框點分屬兩個不同 blocks，兩個互斥連通 subgraphs 中的路徑
就違反 disk 的 Jordan 分離，因此 π noncrossing。
同一色對內的框邊本身連接兩端，故框邊強制 ownership 條件成立。
各 root 的實際 component 給出它在這份 π 中的 block；空 block 由引理 3 排除，
連通情形依引理 4 處理。引理 1–4 保證 L1 全部必需交換在 Σ 中，
引理 5 再保證 L2。若只假設 P 存在而未指定 ψ，§1 的 Σ-critical 接線提供 ψ。∎

這是唯一的檢查方向。不證「存在一致指派 ⇒ 存在 P」、不證 root-to-frame
接線與 zw 能同時在 disk 實現，也不從表中 q′∈Σ 推論特定 ψ′ 的 extension fibre。

## 3. 有限域、逐筆資料與完整結果表

對四個 masks 各自逐份窮舉所有字面拒絕 q、五條 a=i,b=i+1 mod 5 的框邊、
剩餘兩色的兩種 (c_z,c_w)、該 split 的全部相容 π、兩 roots 的全部 block 選擇。
空 root block 也計入初始選擇，再依紙面引理刪除；沒有額外來源刪除規則。

五個固定方向足夠：每條無向框邊選其循環方向，再依 p rotation 命名對角 roots。
若原先方向反轉，同時交換 (a,b) 及 (z,w) 即得到同一配置；兩 roots 都有 degree 5，
兩種剩餘色序均已枚舉。這只固定命名方式，不是對框做 D₅ quotient。

只 import `c5_kempe_screen.py` 的純生成／正規化函數及
`c5_kempe_transport_table.py` 的純 partition、block swap、disk embedding 函數；
不呼叫它們的 `report`、`build`、screen、目錄搜尋或外側四色 oracle。
遞迴與 restricted-growth 生成器逐集合核對所有相容 π，Bell 數 1,1,2,5,15,52 也核對。
圖層完整 Σ 使用小圖有限回溯染色，再以同一 S₄ 置換展開完整有序列，沒有外部 oracle。

| Σ | 字面拒絕 q | (q,ab,root色,π) 數 | 含空 block 指派 | 非空指派 | L1 | L1：a–z連通 | L1：b–w連通 | L1：均斷 | L2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 933 | 96 | 2496 | 16896 | 6336 | 2112 | 960 | 960 | 192 | 192 |
| 941 | 72 | 1872 | 12672 | 4752 | 2304 | 960 | 960 | 384 | 384 |
| 1012 | 72 | 1872 | 12672 | 4752 | 1728 | 768 | 768 | 192 | 192 |
| 935 | 72 | 1872 | 12672 | 4752 | 1728 | 768 | 768 | 192 | 192 |

四個 masks 共保存 7,872 筆 L1 存活指派，其中 960 筆也在 L2 存活。
`assignments.jsonl` 每筆均保存完整字面 q、完整 π、split、root 色、四端點 block ownership、
連通狀態、每次必需交換的字面 q′、共同正規化列與 index，以及 L2 去留理由。
L2 並未另存為獨立簡化投影，而是同一完整紀錄的 `L2=true` 子集。

下表是**完整分組結果**；每個向量依框邊 `01,12,23,34,40` 排列。
顯示索引只為分組：每列加總該代表的全部 24 份字面 S₄ 色名置換，實際計算沒有 quotient。
每個向量的和與上表總數逐一相符。完整逐字面資料仍以上述 JSONL 為準。

| Σ | q index／代表 | 五框邊 L1 存活 | 五框邊 L2 存活 |
| --- | --- | --- | --- |
| 933 | 1／01021 | 168,168,120,48,168 | 24,24,24,0,24 |
| 933 | 3／01201 | 96,48,48,96,96 | 0,0,0,0,0 |
| 933 | 4／01202 | 48,48,96,96,96 | 0,0,0,0,0 |
| 933 | 6／01212 | 120,168,168,168,48 | 24,24,24,24,0 |
| 941 | 1／01021 | 240,240,120,120,240 | 48,48,24,24,48 |
| 941 | 4／01202 | 120,48,168,168,168 | 24,0,24,24,24 |
| 941 | 6／01212 | 120,168,168,168,48 | 24,24,24,24,0 |
| 1012 | 0／01012 | 168,168,168,120,48 | 24,24,24,24,0 |
| 1012 | 1／01021 | 96,96,48,48,96 | 0,0,0,0,0 |
| 1012 | 3／01201 | 168,48,120,168,168 | 24,0,24,24,24 |
| 935 | 3／01201 | 168,120,48,168,168 | 24,24,0,24,24 |
| 935 | 4／01202 | 48,48,96,96,96 | 0,0,0,0,0 |
| 935 | 6／01212 | 120,168,168,168,48 | 24,24,24,24,0 |

## 4. 雙向正控制：逐點實際重現

這裡的「雙向控制」是題目指定的正控制與目標排除檢驗；並不表示存在性引理有反方向。
controls artifact 從原圖重新抽實際 chains，驗 G−P 染色、degree、p rotation，
重算完整 Σ，找到表中唯一相同的指派，並直接保存交換後的完整 G 染色。
P1 的四份交換另外與任務 K 的原 `kempe_swaps` 字面 ψ′、頂點、q′、index 逐項相等。

| 控制 | 表中唯一指派 | q；(a,b,z,w,p)；root 色 | π；(a,z,b,w) blocks |
| --- | --- | --- | --- |
| P1-witness-001 | KD1012-0001 | 01012；(0,1,5,6,7)；(2,3) | (04,1,2,3)；(04,2,1,3) |
| S935-q3-psi0 | KD935-0003 | 01201；(3,4,6,7,5)；(2,3) | (0,1,23,4)；(23,0,4,1) |
| S935-q6-psi0 | KD935-0008 | 01212；(3,4,6,7,5)；(3,0) | (04,1,2,3)；(3,1,04,2) |

| 控制 | 端點 | 色對／block | 字面 q′ | index | p 可用色 |
| --- | --- | --- | --- | ---: | ---: |
| P1 | a | 02／04 | 21010 | 6 | 0 |
| P1 | z | 02／2 | 01212 | 6 | 2 |
| P1 | b | 13／1 | 03012 | 2 | 1 |
| P1 | w | 13／3 | 01032 | 2 | 3 |
| S935-q3 | a | 02／23 | 01021 | 1 | 0 |
| S935-q3 | z | 02／0 | 21201 | 1 | 2 |
| S935-q3 | b | 13／4 | 01203 | 5 | 1 |
| S935-q3 | w | 13／1 | 03201 | 5 | 3 |
| S935-q6 | a | 13／3 | 01232 | 9 | 1 |
| S935-q6 | z | 13／1 | 03212 | 9 | 3 |
| S935-q6 | b | 02／04 | 21210 | 0 | 2 |
| S935-q6 | w | 02／2 | 01012 | 0 | 0 |

三份控制全部兩鏈斷開，四次字面交換都在其實際完整 Σ 內，且直接延拓 p。
S935 的 q index4=01202 沒有 G−P 見證，原 artifact 也保存空 witness 清單，沒有造出控制。
S935 的兩份真實四色見證全數重現，未漏掉第二份。

## 5. 具名存活與小規模 disk 實現嘗試

兩份具名指派都取 q=01021、a=0、b=1；不把表中存活稱為反例。

| 指派 | (c_z,c_w) | π | (a,z,b,w) blocks | 所需色對 |
| --- | --- | --- | --- | --- |
| KD933-0001 | (3,2) | (0,1,2,34) | (0,2,1,34) | 03／12 |
| KD941-0001 | (2,3) | (0,1,23,4) | (0,23,1,4) | 02／13 |

| 指派 | 端點 | 色對／block | 字面 q′ | index |
| --- | --- | --- | --- | ---: |
| KD933-0001 | a | 03／0 | 31021 | 8 |
| KD933-0001 | z | 03／2 | 01321 | 8 |
| KD933-0001 | b | 12／1 | 02021 | 0 |
| KD933-0001 | w | 12／34 | 01012 | 0 |
| KD941-0001 | a | 02／0 | 21021 | 3 |
| KD941-0001 | z | 02／23 | 01201 | 3 |
| KD941-0001 | b | 13／1 | 03021 | 2 |
| KD941-0001 | w | 13／4 | 01023 | 2 |

所有目標 indices 在各自 Σ 中，π noncrossing，兩條對角都斷開。
保存的 JSON 亦含全部 literal tuples，不僅上述 mask 或交換 index。

**實際嘗試域。** 只取頂點 0,…,7，P={7}、roots z=5,w=6。
固定框五邊、zw 與 p 到 {a,b,z,w} 的四邊；由 root degree 5，兩 roots 各恰有三個框鄰點。
每框邊有 C(5,3)²=100 個接法，五框邊共 500 個，不做圖同構或 D₅ quotient。
這是能容納該設定的最小頂點數，沒有加其他 root，也沒有擴大 P。

這個實現嘗試要求內部碰齊五框點、H−P 連通；後者在這個域由原 zw 自動成立。
碰齊五框點沿用固定來源 (S) 的已證基本結構，見
[盾弧報告 §1](c5_unary_shield_budget.md#1-前提與記號)；八頂點域完整性限定於此條件。
加暫時 apex 鄰接 B 篩 disk，移除後保存 rotation、所有面與指定外面 C₅。
逐圖計完整有序 Σ，逐非框邊重算 Σ(G−e) 並保存新增列與延拓 witness。
所有內點 degree 為 (5,5,4)，T4 與 criticality 都實際核對。

| 階段 | 接法／圖數 |
| --- | ---: |
| 全部命名接法 | 500 |
| 碰齊五框點 | 275 |
| 通過 disk 嵌入 | 10 |
| T4 全收且每條非框邊 Σ-critical | 10 |
| Σ=935／942／956／997／1012 | 各 2 |
| Σ=933／941 | 0／0 |

兩份具名候選亦逐張檢查相同框邊下的外部 ψ 與目標 Σ；兩張 a=0 圖的 ψ 都不合法，
完整 Σ 也均不符目標。搜尋未逐圖限制對角 rotation，沒有重現候選的實際 π 或 joint incidence；
它是一個安全的較寬接線測試域，所有圖已在完整 Σ 層失敗。
全部 10 張 disk 圖、完整 Σ、11 條非框邊的完整刪邊關係及嵌入均保存在
`bounded_realization.json`。完整固定 933／941 已在關係層失敗，故沒有成功實現。
不能從此八頂點域推論任意大小不可實現；本輪按停止條件止於此，不再加點。

## 6. 剩餘缺口與停止界線

紙面必要引理完整，包括任意此種實際拒絕見證的 joint ownership 抽取，以及 L2 側別。
有限表仍保留 933 的 192、941 的 384 筆，因此不能寫成
「固定 933／941 下單點、四色、相鄰 degree-5 roots 的短支援 one-sided mixed 不存在」。

仍須處理同一 disk 中 p rotation、zw、全部實際 root attachments 與 π 的聯合可實現性，
並保持完整 Σ、T4、criticality 與 degree。π 上的 root block 指派只是必要 incidence，
沒有編碼全部內部路徑或來源 graph 的 extension fibres。
局部實現且完整 Σ 改變仍不是固定來源反例。

本輪不證 K′、猜想 S、ε≥3、一般出口或 `K∞=K≤5`。
|P|≥2、少於四色、非相鄰 roots、其他 root 接線均未研究。
下一步交由整合者評估具名資料；本任務停止，不擴大研究域。

## 7. 重播、實際 exit code 與新增檔案

生成只以 `open('xb')` exclusive-create 新建六份計算產物；任一既有產物都會拒絕生成，
不覆寫。`--check` 重算全部六檔，逐 byte 相等才通過；validation log 為獨立實際執行紀錄。

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/c5_kempe_diagonal_transport.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/c5_kempe_diagonal_transport.py --check
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=17 .venv/bin/python scripts/c5_kempe_diagonal_transport.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`PYTHONDONTWRITEBYTECODE=1` 避免 import 產生快取檔；它不改變計算內容。
首次生成嘗試曾 exit 1：S935 的 rotation 格式是 records 清單，P1 則是字典；
控制讀取尚未兼容前者。修正新 checker 的格式讀取後，生成 exit 0，控制全存活。
失敗發生在任何產物寫入之前，沒有覆寫歷史或新產物。

本節下方列實際最終驗證紀錄。`git diff --check` 只涵蓋 tracked diff；
另檢查新增 source/report 的 whitespace。未執行 `lake build`，本輪沒有 Lean 變更。

新增檔案：

- `scripts/c5_kempe_diagonal_transport.py`
- `docs/c5_kempe_diagonal_transport.md`
- `artifacts/c5_kempe_diagonal_transport/observations.json`
- `artifacts/c5_kempe_diagonal_transport/assignments.jsonl`
- `artifacts/c5_kempe_diagonal_transport/controls.json`
- `artifacts/c5_kempe_diagonal_transport/KD933-0001.json`
- `artifacts/c5_kempe_diagonal_transport/KD941-0001.json`
- `artifacts/c5_kempe_diagonal_transport/bounded_realization.json`
- `artifacts/c5_kempe_diagonal_transport/validation.json`

| 命令 | exit code | 實際結果 |
| --- | ---: | --- |
| 初次生成（修正前） | 1 | S935 rotation 格式未兼容；未寫入產物 |
| 生成（修正後） | 0 | exclusive-create 新建六檔；933／941 的 L1/L2 分別 2112/192、2304/384 |
| `--check` | 0 | `CHECK OK`；六份計算產物逐 byte 相等 |
| `PYTHONHASHSEED=17 … --check` | 0 | `CHECK OK`；同樣六檔逐 byte 相等 |
| `python3 scripts/check_docs.py` | 1 | 只有新報告未被 STATUS 直接索引；無 missing path／anchor |
| `python3 tools/docgraph check` | 0 | 62 documents、213 relations、5 families；0 errors、0 notes |
| `git diff --check` | 0 | 無輸出；tracked diff 為空 |
| 新 source 的 `git diff --no-index --check` | 1 | 無 whitespace 診斷；exit 1 表示存在新增檔案差異 |
| 新 report 的 `git diff --no-index --check` | 1 | 無 whitespace 診斷；exit 1 表示存在新增檔案差異 |

實際輸出保存於 [validation.json](../artifacts/c5_kempe_diagonal_transport/validation.json)。
文件檢查**未通過**；依本任務禁止修改 STATUS 的要求交由整合者索引。
validation 保存上述實際檢查快照；最後再檢查正文加入驗證紀錄後的文件狀態。
獨立 restricted-growth／正規化／noncrossing／swap 枚舉逐集合核對四份完整指派表，與 checker 相同。
所有既有文件與歷史證書均保持原樣，HEAD 保持基準；未 commit、未 push。

最後正文驗證：`check_docs.py` exit 1，仍只有本報告未索引（546 Markdown files，5813 local links）；
DocGraph exit 0，仍為 62／213／5、0 errors／0 notes；`git diff --check` exit 0。
新增報告的 `git diff --no-index --check` exit 1，無 whitespace 診斷。
分支與 HEAD 最終核對為 `task-kprime-diagonal-transport @ 2ddc6b4`；
工作樹只有本任務上述九份新增檔案，既有 tracked 檔案沒有變更。
