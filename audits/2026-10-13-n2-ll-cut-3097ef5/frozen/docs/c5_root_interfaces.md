# Root 介面反例與 triangle context 的篩選

文件整理（2026-09-23）：完整 root／bridge 介面反例仍有效；[路徑化約](c5_triangle_path_reduction.md) 的正結果需要 triangle context。
系列依賴與證據界線見 [全 degree-4／block 導讀](c5_degree4_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文舊停止點與驗證紀錄保留當輪語境；本次未重跑研究 checker。

後續狀態（2026-09-17 文件整理）：[triangle 路徑化約](c5_triangle_path_reduction.md)
已處理本文提出的 triangle context 問題；完整 root 介面的反例仍有效。現況見 [交接](HANDOFF.md)。

2026-09-17。接續 [triangle branches](c5_triangle_branches.md) 的停止點。
**最值得續挖的是 triangle context 下的介面化約，而非任意 disk forcing tree
都等價於兩點 forcer。** 後一命題已被四點路徑否定，甚至把 root 介面降到
單條 bridge 真正能觀察的資訊後，反例仍存在。未新增 Lean theorem。

## 1. 單條 bridge 所需的精確資訊

固定 boundary coloring b，令 S_F(b) 是 rooted branch F 的 root 可取色集。
F 除共用 boundary 外，只以一條邊連到外側頂點 v；沒有其他跨枝邊。
外側可給 v 的顏色恰為

`E_F(b) = {a : 存在 c∈S_F(b)，a≠c}`。

因此 S 為空時 E 為空；S={c} 時 E 是四色去掉 c；|S|≥2 時 E 是全部四色。
固定外側 coloring 後直接選枝 coloring 即得充分性，反向限制 coloring 得必要性。
故每個 boundary row 的「空／singleton 四種／至少兩色」六值資訊已足夠。
兩枝 E 相同即在任何這種染色接合中可互換；**這不保證替換後仍有 disk embedding**。
十個 canonical rows 可由整體顏色置換還原全部 240 rows，色集也必同步置換。

完整 root masks 比這個介面更細。測得有 12 條長枝雖無相同 root masks 的
兩點代表，卻有相同 E 的兩點代表；不能單憑 root masks 不同就斷言
單 bridge 的 relation 不同。

## 2. 一個連 bridge 介面都無法壓成兩點的 disk 枝

固定 q=01012、D=3。內部路徑為 `5–6–7–8`，root=5，boundary neighborhoods：

```
5:{3,4}, 6:{3,4}, 7:{1,4}, 8:{0,1,4}.
```

它本身是 disk，root 加上待接 parent edge 後全部內點 degree=4。
q 下 lists 依次為 `{0,3},{0,3},{0,3},{3}`，root 唯一強迫 0。
注意同 palette 的實際 boundary attachments 可以不同；這是有一個開放 root
的枝，不能直接套用兩端封閉的樹 obstruction 報告中的 attachment 恆定結論。

在依序排列的十個 canonical patterns 下，root 的十六進位 masks 為：

```
patterns: 01012 01021 01023 01201 01202 01203 01212 01213 01231 01232
S masks:     1     9     1     c     a     6     1     1     5     1
E masks:     e     f     e     f     f     f     e     e     f     e
```

最自然的短枝保留 root neighborhood `{3,4}` 與 leaf neighborhood `{0,1,4}`。
對 b=01023，長枝 root 只能取 0，短枝可取 0 或 1；故外側 parent=0 時，
短枝可延拓而長枝不能。長枝此時的 lists 是 `{0,1},{0,1},{0,2},{2}`，
從葉往 root 強迫 `2→0→1→0`，可直接核對。這只是染色側的區分，
不聲稱這個 pinning context 同面。
更強地，checker 對**每個**強迫 0 的 degree-4 兩點 disk forcer，保存至少一個
E 不同的 boundary row；因此換另一種兩點接線也無法修復此反例。
比較範圍是上述 degree／單 bridge 規格，並非所有可能的兩點 gadgets。

## 3. 有界完整路徑測試

只枚舉 2、4、6 點 rooted path forcers，不枚舉一般內部圖。
將 parent edge 視為強迫色 c∈{0,1,2} 的 virtual edge，路徑 edge palettes 為
`c,D,a₁,D,a₂,D,…,D`。Lists 是 root 的 `{D,c}`、每個 a 的一對 `{D,a}`，
以及末端 `{D}`；每個被禁止的 q 色各選一個實際 boundary 鄰居，獨立展開。
這完整覆蓋此 path palette grammar，包含同 palette 的不同 attachments。

| 枝內點數 | lifts | disk |
| --- | ---: | ---: |
| 2 | 32 | 27 |
| 4 | 768 | 77 |
| 6 | 18,432 | 139 |

243 個 disk lifts 共 52 個完整 root signatures、41 個 bridge signatures。
111 個 lifts 無同色兩點 disk root 代表，其中 99 個連 bridge 代表也沒有。
計數保留 boundary 和 root 標號，不是不重複圖同構類數。
每個 disk lift 的全部 240 root masks 同時由 bottom-up recurrence 與
獨立 pinned-root coloring 回溯核對；接受端另保存 boundary-apex rotation。
拒絕端重新枚舉 NetworkX planarity，保存枚舉 hash，未逐例保存 subdivisions。

## 4. 接回既有 triangle 基底

對上一輪 18 個 disk templates 的每個 branch slot，替換成同 q 強迫色的
上述 disk 路徑；另一枝（若有）保留原狀。不先按 signature 合併圖，因幾何
合法性可能不同。800 次替換有 108 次仍為 disk：

- 全部仍只缺 q，保存完整 240-row relation 與逐非外圈邊 minimality。
- 沒有任一新 root signature 存活；只有 4 種 root signatures。
- 所有存活路徑的 word 都只用 root 的同一 palette，長度為 2、4、6。

這是固定 18 contexts、單 slot 替換及指定短路徑 grammar 的有限結論。
不涵蓋同時改兩枝、改 triangle spokes、任意長路徑、分叉樹或多 cycle blocks。
尤其不能把 99 個新 bridge 介面全被此輪 context 排除，提升成一般排除定理。

## 5. 下一個窄問題與重播

建議先證明或反駁：全 degree-4 的 disk minimal q-obstruction 若唯一 cycle
是 triangle，每個外掛 forcing tree 在該 triangle context 中，能否化成
bridge-interface 等價且可同面替換的兩點枝？先處理路徑枝的 palette 切換與
同 palette 異 attachments，找 boundary 不識別的固定 minor 排除；之後才處理分叉。
本輪四點反例可作必要負控制，避免把 standalone disk 條件當成充分假設。

這比繼續增加恆定 tails 長度更能處理缺口，也比立即擴大一般圖枚舉更聚焦。
一般 triangle 加樹的單缺失性、其他 odd cycles、多 blocks、degree≥5、共同
pivotal edge、候選 A 與 K∞=K≤5 均未解。

產物：[checker](../scripts/c5_root_interfaces.py)、
[證書](../artifacts/c5_root_interfaces/observations.json)。
證書以 `witness_path` 指向 §2，`two_point_separators` 為 bridge 比較，
`contexts` 保存每次成功接合的原始 base／branch／path 索引與圖證據。

```bash
uv run --with networkx==3.5 python scripts/c5_root_interfaces.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_branches.py --check
lake build
git diff --check
```

驗證通過：新 checker 逐 byte 重播、triangle checker、`lake build`（8,820 jobs，
僅既有 lint）、147 個本地文件連結、9 個來源／輸入 hashes 與 `git diff --check`。
本輪產物與後續 triangle 路徑枝化約一併發布，沒有背景研究程序。
本報告 §5 的路徑問題已由[後續報告](c5_triangle_path_reduction.md)推進；
最新停止點是 triangle 外掛樹的第一個分叉，見該報告 §7。
