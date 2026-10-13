# 共同識別／異色弦／face hubs 的獨立覆核

範圍僅為父包 `quotients/certificate.v2.json.gz` 的指定 grammar；不是全部
預算內 quotient gadgets，亦不把普通 cap 的全生成結果外推到此族以外。

每份圖先取原具名 C8 的 noncrossing dissection，將每條弦指定為 equality
或 inequality；每個長度至少四的 dissection face 可選放一個接該 face
全部原點的私人 hub。hubs 無彼此的邊。equality 弦是識別用的 scaffold，
不是要求 proper 的原邊；縮掉每個 scaffold 連通分量，保留原 C8 邊、
inequality 弦及 hub edges。若任何原 inequality 變成 loop，就整份拒絕。
原 boundary map `0..7` 及 `8+j` 第 j 個 hub 的 identity 全部保留。

原 C8 induced 是 no4ct source 的紙面輸入，所以這些 equality 不會把 H
中的隱藏 boundary chord 變成 loop。所有操作在同一 exterior disk；原
dissection 面的 hubs 先同時畫入，再縮 equality scaffold，即證共同平面性。
若縮去 d 個原點、加入 a 個 hub，整份 H quotient 為 `k−d+a` 點；本族
每份皆滿足 `a−d≤5`，故相對可染性作用於一份共同完整圖。

[signed_check.py](signed_check.py)沒有 import producer。它按接觸固定 base
edge 的唯一 polygon face 遞迴分解原八邊形，獨立重建全部 903 份 dissections。
每個 face 由其原有序頂點確定，再獨立選 equality 標記及 hubs；以 graph
connectivity closure 重建 quotient blocks。這和 producer 的「枚舉全部
弦子集、逐弦 split face、union-find」是不同的 domain construction。

重建得 24,418 份原 grammar choices，其中 8,652 份產生 inequality loop；
剩下 15,766 份與證書的具名 grammar keys 一一對應，沒有遺漏或重複。
每份都逐 row 實際建立 quotient graph，先在同一 quotient block 固定原
boundary literal colors，再由全圖 adjacency 進行私人 hub DFS；依序
比對完整 hub tuples 與所有空 fibres。沒有只重算 relation masks。

| 覆核量 | 數量 |
| --- | ---: |
| 合法具名 gadgets | 15,766 |
| 固定原列 fibres | 4,319,884 |
| 空 fibres | 3,801,275 |
| 完整私人 hub lifts | 578,038 |
| 不同完整 boundary relations | 3,284 |

八份 U 的最小交集依序為 `2,2,1,3,1,2,3,2`（查詢順序為
c04-941、c07-941、c15-933、c15-941、c18-933、c18-941、c20-941、c30-941）。
checker 同時核對 producer 指定的 minimum witness ID 與全部原交集 row
indices。沒有新增來源排除。singleton 交集給對該實際來源的正 fibre
必要條件；不自動給共同 source contradiction。

負控制包含：交換兩個原 boundary 名字；識別 `0=2=3` 使原 C8 邊 `2-3`
成 loop；把 literal full fibre 填入非法 hub 顏色。三者皆必被拒絕。
正常及 `PYTHONHASHSEED=17` 結果保存於 [signed_result.json](signed_result.json)
及 [signed_result.seed17.json](signed_result.seed17.json)。兩份 receipt 保存
完整證書 SHA256、上述全量統計、最小交集及負控制原因。

另已紙面覆核 [共同計數／交換錐論證](../review/COUNT_REVIEW.md) 的固定互補
色對 orbit、NC 分量、G8 平均與 `2^h/8` 係數；它提供必要數值條件，沒有
把抽象 NC patterns 宣稱為來源。其精確矩陣證書及實際圖控制由該子包
checker 負責，本覆核沒有將這兩層當作 Lean 形式化。
