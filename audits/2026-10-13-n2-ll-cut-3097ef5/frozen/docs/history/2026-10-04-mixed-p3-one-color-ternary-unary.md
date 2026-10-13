# C₂：一色支援三接點 unary 的原 triangle 與外路 K₅ 排除

2026-10-04，Git 基準 `0e3812712b68f57927df86f30a07bb8074e090f9`。
工作目錄 `/home/ray/developer/ai/math`；起始已有多輪四-spoke／共鄰 P₃
研究與索引未提交變更。本輪只新增這份 C₂ 證據及相連索引，未 commit／push。
完整前提與任意大小證明見[報告](../c5_mixed_p3_one_color_ternary_unary.md)。

## 結果與精確來源身份

固定 **CPP-134-1／geometry 30／side_join_id 20**；case ID=86、local ID=134、
branch=1、side IDs=(8,1)。原 S₀=014、S₁=14、S₂=4，完整 P₃ triples
為 {(3,0,1),(3,0,3)}，禁對 {(1,3),(3,1)}。原側角色：z、w 均無 spoke，
各一份三接點 unary；f_Dz={0,2,3}、f_Dw={0,2}，E_z={1}、E_w={1,3}。
geometry 30 的自身支援為 A_z={b₁}、A_w={b₂,b₄}，J=b₁b₂b₃b₄。

原 degree 四與單一實際框點使 d_D(v)=4−[vz]−[vb₁]≥2；內度二的點
必同時是原 z 接點與 b₁ 鄰點。固定一個拒絕色 z=0 即給不可染 degree
assignment；Gallai 定理、原 z–x₂–b₄ 連通外部與 K₄ minor 排除，
再由兩個 leaf odd-cycle blocks 至少耗四個接點，迫原 D 恰為三接點
triangle。保留原 z–x₂–b₄–b₃–b₂–b₁ 後，得到 K₅ subdivision。

局部 triangle 本身的內點 degree 都為四、完整禁色正是 {0,2,3}；九條
相關邊逐條刪除後都解除全部禁色。故不是把局部 degree／edge-criticality
說成不存在：矛盾是它們與原外路無法共同嵌入 disk。

此處只關閉一份原側接合。前層 36 cases／140 geometries／900 role joins
保持原 artifact，零 profile 刪除；未排除整個 CPP-134-1、geometry 30 的
其他 side joins、w 原 unary 或下一個雙框點自身支援型。
零 target，不查 T4，未新增 Lean theorem，未證完整 Σ 或一般／共同出口。

## 證據與完整 witnesses

新增[checker](../../scripts/c5_mixed_p3_one_color_ternary_unary.py)與
[observations](../../artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json)。
新證書為 108,522 bytes，小於大型 manifest 門檻，直接可追蹤。
它綁定自身 checker、common-endpoint／capacity／base scripts、前層
observations 與 rotation inputs 的 SHA256，前層來源 SHA 亦重新核對。

- 保存完整原入口、共同色框、P₃ 六條附件、兩份 triples 與原 root join；
  讀回 geometry 30 的原 rotation 正控制，重算 darts／faces。
  該收縮骨架 root degrees=(3,4)，不冒充來源原 degree=(5,5)。
- 四種原點身份、16 個 pinned-list 控制；forced triangle 保存六個有序
  接點 tuples、三個拒絕 palettes、色 1 的 slack 及所有原接線。
- 九次 unary 邊刪除、36 份局部完整染色；其中 27 份對應原拒絕色，
  刪邊兩端均同色。另保存九份原 B、P₃、zw／wx₂ 與 D 的 partial
  colorings，z=0、w=1、P₃=(3,0,3)。D_w 保留具名完整未知 relation；
  w=1 避色 fibre 非空由原 f_Dw={0,2} 保證，未捏造它的 tuples／內點。
- 32 份 K₄／原外路 tether minor 控制，驗證五組 branch sets 連通、
  互不相交與十對原邊鄰接。它們是 route 控制，不是 degree/minimality 來源。
- 兩份具名 K₅ subdivisions 分別使用原框弧 b₄b₃b₂b₁ 及 b₄b₀b₁；
  同時保留外路 z–x₂–b₄。逐條核對 path、interior disjointness、原邊
  與 branch degree 四／subdivision 內點 degree 二，不用 planarity oracle。

任意 unary 大小、block 數與 bridge 長度屬紙面論證；外部依賴為
[Dvořák Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪 live 讀原文核對 connected degree assignment 前提，未用 critical-graph
corollary／T4。Python 與既有 Lean build 不重證此一般外部定理或來源抽取。

## 重播與實際驗證

```bash
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
python3 scripts/c5_mixed_p3_common_endpoint.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 逐 byte 重播（一般／seed=17）與前層共鄰 checker 通過。
既有 Lean build 通過 8,831 jobs，保留既有 linter warnings；未改 Lean 檔。
DocGraph 通過 62 documents／213 relations／5 families，零 errors／notes；
`git diff --check` 通過。新報告、歷史、weak-deletion guide 與前層共鄰
報告的本地 links／anchors 及新報告／歷史的直接 STATUS 索引均通過。
首次全域文件檢查掃描 521 份 Markdown／5,402 本地連結，有七個 missing-path
errors，全部指向本輪以外兩條四-spoke 線正在新增的歷史檔：
`history/2026-10-04-excess-two-four-spoke-mixed12-01-12.md` 與
`history/2026-10-04-excess-two-four-spoke-mixed22-short-face.md`。
缺失來自 STATUS、Kempe guide 與兩份四-spoke 報告；本輪未改寫它們或
建立空白替代檔。隨後本輪連結核對時全域已增為 522 份 Markdown／5,410
本地連結，只剩三個其他線 missing-path errors；當時未把全域文件檢查写成通過。
其他線完成其歷史檔後，最終 `check_docs.py` 通過 523 份 Markdown／5,414
本地連結，anchors／直接索引／HANDOFF 均通過；DocGraph 與 whitespace
亦再次通過。保留這段失敗／完成時間順序，不將其他線落盤算成本輪成果。

未重跑：capacity 的全表 standalone checker、其他 P₃ 對稱／非對稱／中點端點
standalone checker、no-mixed 十五類、singleton／K₂ 完成表、R 系列、
933／941 excess、atlas／profiles／閉包及 Lean axiom audit。
新 checker 的原入口驗算仍重用完整介面 pinned solver 及 capacity join；
未宣稱上述全部控制已重新驗證。
HANDOFF 的 weak-deletion 研究線與 tag 不變，依文件治理只更新其 guide。

## 停止點與貼上式交接

C₂ 所指定的一份原三接點身份已 source 排除，沒有未決的 unary bridge。
下一入口是 **CPP-134-1／geometry 34／side_join_id 20**：同一原 P₃、
完整 triples、side IDs=(8,1)、兩側禁色及三接點身份；自身支援改為
A_z={b₁,b₂}、A_w={b₂,b₄}。它的原 geometry identity 保存在新 artifact。
非接點可同時碰兩框點而內度二，原單框點葉數論證不能直接套用；本輪未研究。
目前入口以[weak-deletion §3](../c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)為準。

> 先讀 docs/HANDOFF.md、docs/STATUS.md 與 weak-deletion guide §3。
> C₂ 已排除 CPP-134-1／geometry30／side_join20：z 原 unary own support={b1}、
> f={0,2,3}、三接點；degree 四＋Gallai＋原外路 K4 排除＋leaf budget
> 迫原 D 就是 triangle，z-x2-b4-b3-b2-b1 給 K5 subdivision。
> 完整六 tuples、九刪邊／36 local witnesses、兩 subdivisions 均保留，
> 前層36/140/900不刪；這只是固定身份 source 排除，非 target／Lean／出口。
> 下一題 CPP-134-1／geometry34／side_join20，Az={b1,b2}、Aw={b2,b4}，
> 原兩側三接點、f={0,2,3}/{0,2}、完整 P3 與 w 未知原 relation 一起保留。
> python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check。
