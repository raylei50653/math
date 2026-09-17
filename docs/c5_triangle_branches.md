# Triangle block 的 forcing branches：兩尾仍可同面

後續狀態（2026-09-17 文件整理）：root 介面的限制見 [介面反例](c5_root_interfaces.md)；
任意長路徑及外掛樹分叉已由 [路徑化約](c5_triangle_path_reduction.md) 與
[分叉排除](c5_triangle_forks.md) 處理。以下保留本輪結果；現況見 [交接](HANDOFF.md)。

2026-09-17。接續 [degree-4 樹核心](c5_tree_cores.md)。
這輪選擇 triangle block 的接枝問題，沒有擴大一般 k=5 圖枚舉。
**值得續挖的是 block 與 forcing tree 之間的完整染色介面。**
有限測試否定「triangle 最多只能接一條 forcing branch」；另一方面，
minor 化約把任意大小的單 triangle 核心限制到至多兩個接枝位置。
下述條件式結構結論是紙面化約加 Python／NetworkX 有限檢查，未進 Lean。

## 1. 任意大小的單 triangle 核心：接枝位置限制

假設 G 是 C5 disk minimal q-obstruction，全部有效內點完整 degree=4，
內部圖 H 的唯一 cycle 是 triangle。固定 q=01012，未用色 D=3。
則 triangle 的剩餘共同 palette 包含 D，且 triangle 對外的 tree edges
至多兩條；若有兩條，它們在不同 triangle 頂點。
這裡只限制離開 triangle 的邊，不聲稱外掛樹內部沒有分叉。

證明的染色部分如下。任一 triangle–tree bridge 切開後，兩側在各自端點
可取色的集合都非空，而原圖不可著色，故兩集合必是同一 singleton {c}。
這使用逐邊 minimality，不要求 triangle 側也是樹。

在 triangle 頂點 v，外接 branches 強迫的顏色都在 L(v)，且互異。
若顏色不在 L(v)，刪該 bridge 不能釋放任何顏色；若兩 branches 強迫同色，
刪其中一條也不能釋放任何顏色，都違反 minimality。
若 v 有 t 條 tree edges，則 |L(v)|=2+t；扣掉這 t 個色，剩兩色。
三角形的三個兩色 lists 不可著色 iff 它們是同一個兩色集合 P
（直接由三集合相異代表判準）。故各 tree edge 的強迫色不在 P。

若 D∉P，因 D 原在每個 L(v)，三個 triangle 頂點都必有強迫 D 的 branch。
保留這三枝，將各枝壓成一點 D-forcer；其他 branch 的強迫色若是 c，
可把整枝收縮到 v 並保留一條 c 色 spoke。該枝必接觸 c 色 boundary：
否則交換枝內 c、D 就破壞唯一強迫性。
刪多餘 spokes 後得到 §2 的 no_D 模板，全部非 disk，矛盾。

若 D∈P，各外接 branch 強迫 c≠D，可用前報 §3 的樹壓縮化為兩點
c-forcer；不需要保存其完整 relation。若同一頂點接兩枝，保留這兩枝，
其他枝收縮成所需 spoke，得到 two_same 模板，全非 disk。
故每點至多一枝。若三點各有一枝，得到 three 模板，也全非 disk。
只剩零、一、兩個不同接枝位置。

這是 boundary 不識別的 minor 操作。排除端目前由 NetworkX planarity
重播檢查，**沒有逐例保存 Kuratowski subdivision**；其信任強度不同於
前報逐路徑證書。結論不依賴 T4；要推出單缺失仍有下一節的資訊缺口。

## 2. 完整 canonical templates 與意外存活者

對 P={D,a}，每條 c-forcing branch 用兩點：第一點 list={D,c}，
葉點 list={D}。每個禁止的 q 色選一個實際 boundary 鄰居，完整展開。
對 P 不含 D，保留三個單點 D-forcers。固定 triangle 標號及接枝位置；
可由 triangle automorphism 對齊位置，表中計數含等價重複。

| 模板 | lifts | disk | 接受全部 T4 |
| --- | ---: | ---: | ---: |
| 一枝 | 832 | 16 | 16 |
| 同一頂點兩枝 | 4,096 | 0 | 0 |
| 不同頂點兩枝 | 10,496 | 2 | 2 |
| 三點各一枝 | 160,768 | 0 | 0 |
| palette 不含 D、三個 D-forcers | 1,088 | 0 | 0 |

18 個 disk templates 全都只缺 q。checker 保存其完整 240-row relation、
逐非外圈邊 q-criticality 與 apex rotation；每組 list assignment 另有一個
完整 criticality 核對，其他 lifts 在 q 下使用完全相同 lists。
所有 177,280 個 lifts 均重新計算 planarity；拒絕端只保存計數和有序枚舉
SHA256，`--check` 會重跑全部模板，而非只信任 hash。

兩枝存活者的一個具名例子，內點為 5..11：

```
triangle: 56, 57, 67
branches: 58, 89, 6-10, 10-11
boundary neighborhoods:
5:{1}, 6:{2}, 7:{1,2}, 8:{1,4}, 9:{0,1,4},
10:{2,4}, 11:{2,3,4}
```

它有七個內點，超出上一輪五內點 cyclic probe；不是「所有七內點」分類。
兩個 templates 互換兩枝顏色與相應標號，不能當成兩種獨立機制。

## 3. 可保存 relation 的局部增長，及不能做的壓縮

在上述 canonical 兩枝存活者，將每個 tail 的第一個 {D,c} 點換成
任意正奇數個點的路徑，所有點保持相同的兩個實際 boundary 鄰居，
末端仍接原來的 {D} 葉點。
對任意 boundary coloring，這段奇數路徑有同一可用色集 S，|S|≥2。
[odd-join 報告](c5_odd_join_cores.md) 的 odd-path transfer 恆等式
表明：固定兩端顏色後，1、3、5、… 個中段點的可延拓性完全相同。
故**任意這種奇數替換保存完整 boundary relation**；不只是保存 q 的 lists。

checker 另對兩個基底各測 (1,3)、(3,1)、(3,5)、(5,3) 的尾長，
八張長圖全為 disk、保持完整 240 rows、且逐邊 q-critical。
這些 disk／minimality 是八張圖的有限驗證；本輪未給任意長度的
局部 embedding 增長證明，不把 relation 恆等式升格為無界 disk 家族證明。

相反，§1 把任意 forcing tree 壓成兩點，只保持 minor 和指定 q 下的
強迫色。所得小圖即使只缺 q，也不能推出原圖只缺 q：對別的 boundary
pattern，原樹可能有不同的 root 可取色集合。這正是下一步該補的介面。

## 4. 下一步與停止點

先固定一個接枝 root，記錄每個 proper boundary coloring 下的 root
可取色集合，即 240 rows × 4-bit masks；按整體顏色置換可等價壓成
10 representatives × 4-bit masks。這個介面在透過一條 bridge 接合時充分：
triangle 側只需知道它能否為枝端選到不同於 triangle 頂點的顏色。
應先比較實際 disk forcing trees 與兩點 forcer 的介面，尋找差異或證明
在這裡的 embedding／degree 限制下必相同，再嘗試 relation-preserving 化約。

本輪沒有解決一般 triangle 加任意樹的單缺失性、較長 odd-cycle blocks、
多個 cycle blocks、degree≥5 核心、共同 pivotal edge 或候選 A。
不再只增加 canonical tails 的長度；下一步測 root-color 介面是否足夠壓縮。

重播：

```bash
uv run --with networkx==3.5 python scripts/c5_triangle_branches.py --check
uv run --with networkx==3.5 python scripts/c5_tree_cores.py --check
lake build
git diff --check
```

產物：[checker](../scripts/c5_triangle_branches.py)、
[證書](../artifacts/c5_triangle_branches/observations.json)。

驗證通過：新 checker 逐 byte 重播、tree checker、`lake build`（8,820 jobs，
僅既有 lint）、144 個本地文件連結與 `git diff --check`。八張長圖另核對
264 次非外圈單刪。本輪產物與 odd-join／tree／triangle 三輪成果一併納入本次發布提交。
