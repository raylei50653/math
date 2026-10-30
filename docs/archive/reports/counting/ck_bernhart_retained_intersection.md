# Bernhart 兩個 41 列子靶：共同原邊的 retained 交會奇偶

2026-10-29 後續：[共同端點補證與 r₂ 來源研究](ck_bernhart_endpoint_ray_continuation.md)
已補依原 rotation 的推離規則及邊界修正，核清本頁原未涵蓋的 16＋2,992 組。
下文保存首輪範圍；完整 RIP 以後續報告為準。r₂ 取得全來源六葉封口必要條件，
全部正偶比例來源排除仍 OPEN，新增必零座標仍為 0。

2026-10-29，接續 [跨 split 語意稽核](ck_bernhart_cross_split_audit.md)及
[共同切口契約](../four-color/four_color_counts_surgery_continuation.md#2-共同切口能排除這個具名假模型)。
本輪新增一條使用共同第三色原邊與原 rotation 的必要條件，並為兩個 lift 各給一份
真平面、完整具名的**局部染色控制**。控制只符合所選字的三份 signatures，
其完整計數向量不是該射線。兩條射線的所有正比例實現仍未排除，76 列沒有新增必零座標。

## 1. 問題、量詞與本輪達到的層級

沿用原證書的兩個 primitive full-lift 極射線 \(r_1,r_2\)，各有 41 個正 n、46 個正 y。
待排除的是：存在同一實際 plane near-cubic disk，其**全部**染色計數為
\((y,n)=\lambda r_i\)，其中 \(\lambda>0\)。單份染色或單份接線不是這項來源存在性。

本輪在具名切口資料上證一條必要式，且能拒絕一份保留相同計數觀測的非平面 rotation。
這是帶原邊／rotation 的 extension 層檢查；沒有證明將它投影回 \((y,n)\) 後，
可從兩條射線或整個 B₈ 殘餘面再排除一點。

| 完成標準 | 本輪狀態 |
| --- | --- |
| 排除指定 lift 射線的全部正比例來源 | OPEN；僅排除下述具名局部接線作為完整射線來源 |
| 在整個 76 列殘餘面證某座標必零 | OPEN；新增必零列 0 |
| 排除全部阻擋、證可約 | OPEN |

原分解只分解選定 lift，不宣稱兩條射線涵蓋整個殘餘面。
即使第一級日後成立，也不能直接刪掉該射線的 41 個 n 座標。

## 2. 一條共同原邊交會必要式

固定同一 proper Tait 染色、同一有向 plane near-cubic disk，及完整雙色 \(ab\)
boundary-to-boundary 原路徑 S。刪去 S 的原邊後，保留兩個 mixed 系統
\(E_{ac},E_{bc}\) 的**全部**路徑及閉圈；各 cut port 仍帶原頂點、原第三色邊身份。
使用同一嵌入決定共同側別及切開兩側的 boundary orders，不另替兩個系統選側別。

取同一側內的一個 retained 分量 \(P\in E_{ac}\) 與 \(Q\in E_{bc}\)。
若兩者都是路徑，要求四個端點互異。定義 \(\epsilon(v)=+1\) 表示原頂點的
逆時針色序為 \((a,b,c)\)，反序為 \(-1\)。則

\[
\boxed{\quad
 \sum_{e=uv\in E(P)\cap E(Q)}[\epsilon(u)=\epsilon(v)]
 \equiv \operatorname{Alt}_{\partial D}(P,Q)\pmod 2.
 \quad}\tag{RIP}
\]

右側是 P、Q 的端點在該側**真實切開環序**中是否交錯。若其中至少一個分量是
內部閉圈，右側為零。兩路徑有共同端點的分支不在本式範圍內；不能默認其推離規則。

**紙面證明。** 兩個系統的共同邊只能為第三色 c 邊。proper trivalence 保證：若兩個
分量共用一個內部頂點，它們就同時使用該點唯一的 c 邊。c 邊彼此不相接；
四端點互異又排除了共同邊止於 cut port 的情況。因此可在每條共同 c 邊各取一個
互不相交的細 ribbon 鄰域，鄰域外兩分量不相交。

對共同邊 uv，鄰域邊界有 \(a_u,b_u,a_v,b_v\) 四個附件 darts。
其中 \((a_u,a_v)\)、\((b_u,b_v)\) 交錯，恰等價於
\(\epsilon(u)=\epsilon(v)\)：沿 uv 收縮 ribbon，兩端同色序得到交錯附件，
反色序得到不交錯附件。將重合邊在其鄰域內微擾，該處交叉數的奇偶就是此指標。
全部鄰域相加得到左側。disk 中兩條 proper arcs 的交叉奇偶等於端點交錯指標；
閉圈與另一閉圈／proper arc 的交叉數為偶數，故得式 (RIP)。
整張圖反向或交換 a、b 都會同時翻轉全部 epsilon，不改此式。

這使用的是共同原 c 邊的**逐邊交集**及兩端 rotation，超出 B₈ 保存的資料。
它也超出只核各 E 自身 noncrossing 的檢查：不同 mixed 系統的路徑可以相交，
但交會須由共同原邊承擔正確奇偶。不能把兩個 E 的邊名當成獨立資源。
此式是必要條件，不是共同平面嵌入或多步狀態充分性的定理。

## 3. 兩條射線的具名入口與局部真來源

兩條射線在字 \(w=11111111\) 均有 \(n_w=1\)、\(y_\varnothing=1\)。
三個 splits 各只有以下一個正 signature，所以每個正比例來源的每份該字染色都必有
這些配對，不受比例大小影響。

| 子靶 | 12、13 的共同唯一 signature | 23 |
| --- | --- | --- |
| \(r_1\) | S1849：05 / 12 / 34 / 67，全部 sign −1 | S0：空配對 |
| \(r_2\) | S1913：07 / 14 / 23 / 56，全部 sign −1 | S0：空配對 |

以下用一張明確畫出的圖補齊**局部控制**的接線，而不把它說成由射線唯一迫出。
取 14 環 \(v_0\ldots v_{13}\)，原邊 i 為 \(v_iv_{i+1\bmod14}\)，
i 偶時染 2、奇時染 3；三條內弦原邊 14、15、16 分別為
\(v_3v_6,v_1v_8,v_9v_{12}\)，全染 1。
邊界葉 \(e_0\ldots e_7\) 依序接
\(v_0,v_2,v_4,v_5,v_7,v_{10},v_{11},v_{13}\)，原邊 17–24，全染 1。
內弦不交錯，所有葉向外，給定的 rotation 是同一個 disk 畫法。
此圖的上述完整染色符合 \(r_2\) 的三份入口 signatures。
將葉標號同時加四（mod 8）即得 \(r_1\) 的具名局部控制。

### r₂ 的一條完整切口

交換 12 路徑

```text
e0 – v0 – v1 – v8 – v9 – v12 – v13 – e7
原邊序：17, 0, 15, 8, 16, 12, 24
ports：t0=v0, t1=v1, t2=v8, t3=v9, t4=v12, t5=v13
各 port 的共同第三色原邊：13, 1, 7, 9, 11, 13
```

原邊 13 同時接 t0、t5，必須保存這個重複身份。完整 retained 接線如下，兩份均無閉圈。

| 系統 | 端點 | 有序原邊 |
| --- | --- | --- |
| E13 | t0–t5 | 13 |
| E13 | t1–e1 | 1,18 |
| E13 | t2–e4 | 7,21 |
| E13 | t3–e5 | 9,22 |
| E13 | t4–e6 | 11,23 |
| E13 | e2–e3 | 19,3,14,5,20 |
| E23 | t0–t5 | 13 |
| E23 | t1–t2 | 1,2,3,4,5,6,7 |
| E23 | t3–t4 | 9,10,11 |

共同側別為 \((1,0,0,0,0,1)\)。側 0 的環序可取
\((t1,t2,t3,t4,e6,e5,e4,e3,e2,e1)\)，側 1 為 \((t0,t5)\)。
交換後 13 配對為 16 / 23 / 45、23 配對為 07，符合 r₂ 的該字要求。
r₁ 的控制將以上所有 boundary 標號同時加四，其切口為 34；證書依較小 boundary
端點起走，故將這條原路徑及 ports 同時反向列出，仍保留相同原邊身份。
這提供兩條射線各一個完整可重播的局部入口，沒有填入任何虛構的未知原圖邊。

### 共同原邊奇偶的具體檢查

取表中 E13 的 e2–e3 路徑及 E23 的 t1–t2 路徑；四端點互異，均在側 0。
其共同第三色原邊恰為 3、5，端點不交錯。兩條共同邊各貢獻一次局部交會，
故 \(1+1\equiv0\) 符合 (RIP)。只反轉非切口頂點 v3 的 rotation，
保留圖、染色、原路徑、ports、全部 retained 邊表與上述側別／環序，
左側變為 1，右側仍為 0。這份 ribbon extension 被拒，原 matching-only 檢查看不見此差異。
它不是該底圖沒有其他平面嵌入的證明，原來的平面 rotation 就是正控制。

## 4. 可排除的是這份接線，不能排除整條射線

上述控制的另一條 12 路徑 14，交換後實際 13 配對為 07 / 23 / 56，
但 r₂ 在其後繼字只允許 05 / 23 / 67。因此若把這份完整局部控制當成
r₂ 全計數來源中的一份染色，同圖合法交換會給出零權重 signature，矛盾。
r₁ 同時重標後有相同失敗；該路徑變為 05。

這是排除一份具名接線延伸的同源 witness；它不證所有其他原路徑長度、內部閉圈、
第三色邊身份及 retained 接線都產生此後繼。局部控制的完整 n、y 也不等於任一射線。

若實際來源有非空 cubic interior，兩條射線的比例另必為偶整數：
\(n_{11111111}=\lambda\) 是整數；在此字的任一染色中，23 系統覆蓋全部內點，
為非空偶閉圈聯集。同時交換全部 2、3 是無不動點 involution，保持該 boundary 字，
故 \(\lambda\in2\mathbb Z_{>0}\)。這只排除奇數比例，沒有排除全部正比例。
內部為空的八葉 pole 最多有四條原邊，完整染色數至多 \(3^4=81\)，
而任一射線的 literal word 總質量為 \(261\lambda\)、且 \(\lambda=n_{11111111}\)
為正整數，所以空內部也不能實現射線。

另外，「單色字的兩套配對永遠相同，便迫全支援在該配對上同色」這條捷徑不成立。
一個紙面反控制是六環 v0…v5，加內弦 v2v5，葉 e0…e3 分別接 v0、v1、v3、v4。
六條環邊依序染 232323，內弦與四葉邊全染 1。單色字的全部染色只有這份及其
2↔3 交換；兩份的 12、13 配對均為 01 / 23。但同一圖把六條環邊染為 123123、
內弦染 1、四葉邊染 2323，也是 proper Tait 染色，並不在 01 / 23 上同色。
原 23 圈有朝內與朝外的第三色附件，不能把整圈當成沒有內外差別的 plane vertex 收縮。
本控制直接逐頂點核三色即可，不依賴新枚舉或 4CT。

**精確下一個缺口：** 對任意同源正比例實現，從已迫出的 signatures 與同圖交換，
證必有一條具名路徑的兩份實際 retained 系統違反 (RIP)、共同側別，或後繼 signature 支援。
本輪沒有覆蓋這個全稱量詞，沒有普通 PM 替代，也沒有僅新增三 split 聯合邊際。

## 5. 證據層與重播

式 (RIP)、偶比例界及量詞區分為紙面論證。Python 保存兩個完整 lift 的選定入口、
兩份真平面局部控制的原圖／rotation／完整染色、原路徑與兩份 retained 接線，
另有 rotation 正負控制；未新增 Lean，未改主求解器或舊證書。
局部四條切口另核 40 組交會條件、明列 16 組共同端點未涵蓋；既有 wheel／stack
控制核 7,124 組，另有 2,992 組共同端點未涵蓋。這些固定圖檢查不構成一般來源覆蓋。

- [局部來源與射線後繼核對程式](../../../../scripts/ck_bernhart_ray_local_witnesses.py)
- [局部來源完整證書](../../../../audits/2026-10-29-bernhart-retained-parity/ray-local.json)
- [共同原邊奇偶程式](../../../../scripts/ck_retained_intersection_parity.py)
- [rotation 正負控制證書](../../../../audits/2026-10-29-bernhart-retained-parity/rotation-controls.json)
- [驗證及治理紀錄](../../../history/2026-10-29-bernhart-retained-parity.md)

大型 rotation 證書依[封存規則](../../../../audits/README.md#新-checkout-的還原)保存原 bytes；
新 checkout 先執行 `python3 tools/audit_archive.py restore --artifacts` 再重播。

```bash
python3 scripts/ck_bernhart_ray_local_witnesses.py --check audits/2026-10-29-bernhart-retained-parity/ray-local.json
python3 scripts/ck_retained_intersection_parity.py --check audits/2026-10-29-bernhart-retained-parity/rotation-controls.json
```

本輪未 commit／push；既有單 split `LOCK-NO-GAIN` 與古典 Bernhart C 還原的量詞不變。
