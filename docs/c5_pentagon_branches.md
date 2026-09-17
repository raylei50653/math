# Cycle-5 接枝限制：整個單環核心被排除

2026-09-17。接續 [triangle 分叉排除](c5_triangle_forks.md)。
原問題是內部唯一 cycle 長度 5 的共同 palette 與接枝位置限制；結果更強：
**全 degree-4 的 C5 disk minimal q-obstruction 不可能有這種內部圖**，
不論外掛樹大小、深度與分叉。此排除不需要接受全部 T4。
這是紙面 minor 化約加 Python 有限 subdivision 證書，未新增 Lean theorem。

## 1. 假設與共同 cycle palette

固定 boundary pattern `q=01012`、未用色 `D=3`。設 G 是相對固定 boundary
的 minimal q-obstruction：q 不延拓到 G，但刪任一非 boundary 邊後可延拓。
假設 G 是 C5 disk，所有有效內點完整 degree=4，內部圖 H 連通且唯一 cycle
為 C5。這裡 boundary C5 與內部 C5 是兩個不同的環。

沿用 [樹核心報告 §2](c5_tree_cores.md)：minimality 排除同一內點有兩條相同
q 色的 boundary spokes，所以 `D∈L(v)`、`|L(v)|=deg_H(v)`。
每條離開 cycle 的 bridge 刪除後，兩側端點可取色集合非空，且必為同一
singleton `{c}`；否則可選不同端點色，把兩側 coloring 拼回原圖。

在 cycle 頂點 v，t 條外接 branches 的強迫色互異且屬於 L(v)。若不在 L(v)，
或與另一枝重複，刪該 bridge 不能改變 cycle 的可延拓性，違反 minimality。
扣掉這 t 色後，剩餘 list `P_v` 恰有兩色，因為 `|L(v)|=2+t`。
外掛樹彼此獨立，因此原圖不可著色正好等價於這個 cycle 的 list 問題不可著色。

一個 cycle 的兩色 lists 若不全相同，必可著色：選相鄰 u,v 使 lists 不同，
先給 u 一個不在 v list 的色，從 u 沿另一方向逐點貪婪染色，最後染 v。
最後 u 的色不在 v list，故 v 最多被另一鄰點排除一色，仍可選。
因此本例各 `P_v` 必是共同的兩色集合 P；同一 P 在奇環上確實不可著色。
Checker 另逐一核對長度 5 的全部 `6^5=7,776` 個兩色 list assignments，
恰有六個共同-palette assignments 不可著色。這是紙面引理的有限控制。

## 2. 吸收非 D 枝，不必分類接枝位置

若一個 forcing tree 在 root 唯一強迫 `c≠D`，它必碰到 c 色 boundary。
否則交換樹內 c、D 不影響 boundary spokes 或樹內 properness，卻改變 root
的強迫色，矛盾。把整棵樹連同 bridge 收縮到其 cycle 頂點，只保留其中
一條 c 色 spoke，刪其餘 spokes，就把「枝禁止 c」變成直接的 boundary 禁色。

### P 含 D

各枝強迫色都不在 P，因此全部不是 D。依上段吸收所有枝後，剩下五個 cycle
頂點，每點 list 都是 P。每個被禁止的 q 色恰留一條實際 boundary spoke。
這已給出一個必要 minor，毋須先限制原來有幾枝、接在哪裡、是否分叉。

### P 不含 D

因為每個原始 L(v) 都含 D，每個 cycle 頂點必有恰一條強迫 D 的 branch。
先吸收其他非 D branches。保留的 D-forcing tree 必碰到全部三個 q 色：
若缺色 a，交換樹內 D、a 就破壞唯一強迫性。
將這棵樹的所有內點收縮為一點，每個 q 色保留一條 spoke，得到 `list={D}`
的一點 forcer，仍由一條 bridge 接到原 cycle 頂點。

最後五個 cycle 頂點的 lists 都是 `P∪{D}`，各掛一個 list={D} 的葉點。
這些收縮只合併內點，不識別 boundary，也不合併不同 cycle 頂點。
所以原圖若 disk，所得 boundary-apex 圖也必平面。
**此處只使用 minor 閉性，沒有宣稱其他 boundary patterns 的 relation 等價。**

## 3. 完整有限排除

枚舉每個 palette，並為每個被禁止的 q 色選一個實際 boundary 鄰居。
q 的三個色類大小為 2、2、1；所有選擇獨立展開，不對 boundary 標號取商。

| 必要 minor | 內點數 | lifts | disk |
| --- | ---: | ---: | ---: |
| P 含 D，全部枝吸收 | 5 | 1,088 | 0 |
| P 不含 D，各保留一點 D-forcer | 10 | 66,560 | 0 |

第一行為 `2^5+2^5+4^5`，第二行為 `4^5·(1+2^5+2^5)`。
合計 **67,648 個 lifts**，由 **56 份共用 K3,3 subdivisions** 覆蓋。
每個 lift 保存 witness index；重播重建真實圖，逐一驗證 witness 邊包含關係。
因此兩種 P 都不能來自 disk 原圖，排除整個指定 cycle-5 核心。

最初的一／二／三枝位置探測引出了這個更小化約；其計數不作本結論的依據，
也沒有保留為另一個需重跑的枚舉。新的證書只含上述兩類必要 minors。

## 4. 直接 corollary：單環 degree-4 核心只剩 triangle

上述紙面 cycle-list 引理也適用其他環長：偶環在共同兩色 list 下可交替染色，
因此 minimal obstruction 的唯一 cycle 必為奇環。

若唯一 cycle 長度為任意 `ℓ≥5`，先作 §2 的同樣吸收，得到長度 ℓ 的同型模板。
保留 cycle 上任意五個依序頂點及其 spokes；P 不含 D 時也保留這五點的
D-forcers。刪其餘 cycle 點的 spokes／外枝，再收縮五段連接路徑的中間點，
保持五個保留點彼此不同。所得正是 §3 的某個 C5 minor，故同樣不可能 disk。
這裡不要求縮圖保存全部 boundary relation；非 disk minor 已足以矛盾。
因此不需要再枚舉 C7、C9 或增加 tails 長度。

所以全 degree-4、內部連通且恰有一個 cycle 的 disk minimal q-obstruction，
其 cycle 必為 triangle。若再接受全部 T4，可套用
[triangle 任意外掛樹結果](c5_triangle_forks.md)，得 `Σ(G)=Ω\{q}`。
這個單缺失 corollary 依賴前輪 triangle 化約及其基底分類；本輪的新有限排除
本身不依賴 T4，也沒有把任意多個 cycle blocks 化成一個 cycle。

## 5. 證書、重播與信任範圍

產物：[checker](../scripts/c5_pentagon_branches.py)、
[證書](../artifacts/c5_pentagon_branches/observations.json)。

生成使用 NetworkX 找 subdivisions；`--check` 不呼叫 planarity search，
而是檢查 K5／K3,3 模型、各路徑真實邊、內點互斥、branch vertices、
全部 lifts 覆蓋、枚舉 digest、八個來源 hashes 與逐 byte 一致性。
每個 palette assignment 另取一個 lift，核對 degree=4、q 不可延拓及
逐非 boundary 邊刪除可延拓；同一 assignment 的其他 lifts 有相同 q lists。

無界外掛樹及較長唯一 cycle 的覆蓋來自 §1–2、§4 紙面證明；有限程式沒有
枚舉無界圖。拓撲 soundness 使用標準 minor 閉性與 Kuratowski 障礙，
未在 Lean 形式化；`lake build` 是既有 Lean 專案的回歸檢查。

```bash
uv run --with networkx==3.5 python scripts/c5_pentagon_branches.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
lake build
git diff --check
```

## 6. 停止點與下一個窄問題

cycle-5 的接枝位置問題已由更強的不可能性封口；同一 minor 論證也排除所有
長度至少 5 的唯一 cycle。全 degree-4 的連通單環情形已歸到 triangle，
但**多個 cycle blocks、degree≥5、共同 pivotal edge、候選 A 與 K∞=K≤5**仍未解。

下一步可固定兩個 triangle blocks，研究連接兩者的 bridge path 與兩端
剩餘 palettes。先區分共用 cut vertex 與以 bridge path 相連的情形；
cycle 側不是 forcing tree，不能直接使用 §2 的樹收縮來聲稱單點／兩點介面。
先找必要 minor 或 disk 反例，保留完整 witness；不要重啟一般圖 catalogue。

驗證通過：新 checker 全量逐 byte 重播、triangle-fork checker、`lake build`
（8,820 jobs，僅既有 lint）、155 個本地文件連結、八個來源 hashes 與
`git diff --check`。沒有背景研究程序；本輪未提交或推送。
