# 任務 C：weak-deletion 共鄰原 P₃ 的雙扇區與具名殘留

2026-10-04，Git 基準 `0e38127`，工作目錄 `/home/ray/developer/ai/math`。
起始工作樹已有四-spoke 線的未提交檔案與 README／STATUS／manifest
變更；本輪只新增共鄰 P₃ 證據並窄更新相連索引，未覆寫其他研究檔案，
未 commit／push。既有變更亦在本輪期間持續增加。
完整前提、紙面證明與殘留清單見[報告](../c5_mixed_p3_common_endpoint.md)。

## 結果及信任界線

保留唯一 mixed 原 P₃=x₀x₁x₂、P*ᶻ=P*ʷ={x₂}、masks=(0,0,3)
及反向型 (3,0,0)，實際 boundary 鄰點數仍為 (3,2,1)。
復用前層六份色配置，完整 triples={(3,d,a),(3,d,3)}，
F*={(a,3),(3,a)}，{a,c,d}={0,1,2}。

任意 unary 大小的紙面引理：原 x₀ 三-star、x₁ rooted Y，把 S₂ 與
兩完整 root 側支援局部化到長度≤3 的同一 J；原 x₁–x₂–S₂ tether
迫兩 roots 位於 S₂ 同側，triangle collars 給相鄰兩側支援的線序。
d=2 的兩角色全部 source 排除；c=2 只留 used-singleton／pair 型，
singleton 側全在 J 首條框邊；a=2 的部分五型仍留。

固定控制：500 actual attachment triples、112 非空禁對、560 residual
案例、14,000 必要側角色；13,376 次獨立 pinned queries。
114,048 份整側支援候選經必要幾何後，524 案例無支援、36 案例留下
140 份幾何。原每個 retained case 的 25 組角色均保留，共 900 組。
140 geometry rotation 正控制全部重算 dart／faces、Euler=2、C5 外面
及原 triangle 面；骨架不證原 unary／degree／逐邊 minimality 實現。
零 target，無新 Lean theorem，不需 T4／Gallai，不重啟 no-mixed 十五類。

## 重播與實際驗證

新增[checker](../../scripts/c5_mixed_p3_common_endpoint.py)、
[observations](../../artifacts/c5_mixed_p3_common_endpoint/observations.json)、
[rotation inputs](../../artifacts/c5_mixed_p3_common_endpoint/rotation_controls.json)。
兩 JSON 各小於 1 MB，未登錄大型 manifest。
Rotation 輸入由 NetworkX 3.5 探索生成；最終 checker 僅需標準函式庫，
重建全部骨架邊並獨立驗證旋轉，不讀保存的 planar／accept／exclude flags。
新 observations 綁 checker、capacity、base 的 Python SHA 與 rotation SHA。

```bash
python3 scripts/c5_mixed_p3_common_endpoint.py
python3 scripts/c5_mixed_p3_common_endpoint.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_common_endpoint.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_mixed_p3_middle_endpoint.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 一般與 seed=17 逐 byte 重播通過；容量、middle-endpoint、
完整有序介面回歸通過。既有 Lean build 通過 8,831 jobs，保留既有
linter warnings；未改 Lean 檔，這不形式化本輪 Jordan／來源排除。
文件檢查通過 516 份 Markdown／5,316 本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過。Observations 為 891,129 bytes，rotation inputs
為 110,068 bytes；兩者都留在 git 可追蹤範圍，未改大型 manifest。

未重跑：P₃ 對稱／非對稱單獨 checker、no-mixed 十五類及其增長表、
singleton／K2 完成表、R 系列、933／941 excess 控制、atlas／profiles／閉包、
Lean axiom audit。前層容量回歸自身包含既有固定控制，未另外生成新目錄。
HANDOFF 的 active weak-deletion 導覽及研究線標記未變；依 DOCUMENTATION
治理規則只更新所屬 guide 的現況／停止點，未在 HANDOFF 堆疊研究摘要。

## 停止點與貼上式交接

最小交付已達成：任意 unary 大小的窄幾何引理及部分 source 排除，
配原鏈／原附件／完整三點 relation 的固定控制。
共鄰端點線仍留 36 個具名必要案例；沒有指定 target 出口、source
實現證書、完整 Σ、Lean 或一般／共同出口結論。

下一入口 **CPP-134-1／geometry 30／side_join_id 20** 已由 checker
保存並固定核對：S₀=014、S₁=14、S₂=4，E_z={1}、E_w={1,3}，
Az={b₁}、Aw={b₂,b₄}，J=b₁b₂b₃b₄。
z 側原三接點 unary 飽和禁 {0,2,3}，w 側原三接點 unary 禁 {0,2}。
保留原 z–x₂–b₄ 外路，先研究 z 側自身一色支援的飽和三接點來源，
再處理 singleton 側可碰首框邊兩端的其餘型。

> 先讀 docs/HANDOFF.md、docs/STATUS.md、weak-deletion guide §3 及
> docs/c5_mixed_p3_common_endpoint.md。任務 C 已證雙扇區／triangle tether
> 任意 unary 引理，排除 d=2 兩角色，c=2 只留 used-singleton／pair；
> 36 named residual／140 geometry／900 abstract side joins 保留，非來源實現。
> 下一題 CPP-134-1／geometry30／side_join20 的 z-side 原三接點 unary，
> own support={b1}、f={0,2,3}，保留 w-side f={0,2}、原 P3、z-x2-b4 外路。
> python3 scripts/c5_mixed_p3_common_endpoint.py --check。
> 不拆共鄰點、不換 shared singleton、不重啟 no-mixed 十五類。
