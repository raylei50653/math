# 2026-10-03：ε=2 唯一 mixed 的省略原 mixed 全收

接手基準 `722bfa6`。使用者要求「繼續推進 ε ≥ 3」。先讀 HANDOFF、
STATUS、Kempe 導覽、即時 Git 與相關記憶，沿用
math-research-handoff-publish。保留前序未提交 bundle；未用
Graphify 或 sub-agents，未 commit／push。
成果見 [專題報告](../c5_excess_two_mixed_omission.md)，目前停止點
由 [Kempe 導覽](../c5_kempe_guide.md)維護。

## 任意大小結論與完整同源介面

固定完整 Σ=933／941、Σ edge-minimal、induced-C₅ disk、ε=2、
相鄰雙 degree-5 roots，且恰一份原 mixed C。若 C 的原 incidence
是 (1,1)，則 Σ(G−C)=Ω。結合保留 mixed 的全部原省略排除，
任何 minimal rejected-row core 都不能有 (4,4) root degrees。
**共同 ε≥2 不變，未證 ε≥3；未新增 Lean theorem。**
933 拒絕四列，941 拒絕三列；比較始終使用完整 masks 及十列，
沒有依賴對拒絕列數的口頭描述。

反設 M=G−C 拒絕 q，全 degree-4 飽和迫 M 自己是 q-core。
原 zw 是 M 的內部 bridge，原 M−zw 分成兩份 root 側全圖，
其完整 contacts、實際附件、ownership、tuple relations 及 coloring
witnesses 均保存。固定同一 B 後兩側精確接合，再過濾原 zw。
原 C 保持任意大小、原 bridges／旁支，兩個角色 contacts 可以共用
同一原頂點；完整接回檢查 zw、zx、wy 三條原不等式。
只有完整接合後才投影 root pairs 並取得二維禁對 F_C。

逐欄／逐列 slack 及原二接點 lemma 給每份 F_C 至多兩格、每
row／column 至多一格，共 89 份必要選項。固定原實際支援 S，
跨列 S₄ transport 要求同一 local-shape 函數與代表支援 stabilizer
不變性；相衝突查詢保存完整列約束，相容者保存同一 shape assignment。
相容僅是必要代數選項，沒有原 C 實現宣稱。

原兩 roots 是原 bridge 的相鄰端點。對每份原附件恆定 run，保留
roots 為 singleton，未標記區段按零／正奇／正偶縮成零／一／二。
完整 endpoint transfer 的 R_(t+2)=R_t，t≥1，給任意長度傳遞，
而且刪／留 zw 均保留完整 root-pair relation。其他 contacts
各保留自己的完整關係，不把不同長短圖的 contact 座標認作等價。

僅作拓撲反證，把同一原連通 C 收縮為 c，保留原 zc、wc 及
到全部實際 S 的邊；這與原 M 的 branch sets 互斥，能在原 G
共同縮減。星點不被當作 C 的染色替代。全部必要 minor 的
boundary-apex 圖有明示 K₅／K₃,₃ subdivision paths，逐實際邊、
branch 頂點、互斥內點與九／十份鄰接核對。

## 固定必要域、結果與控制

沿用原任意大小分類，保留原 zw 端點後得 344 份必要核心：
160 單 triangle／單 run、64 單 triangle／兩 runs、56 偶數路徑、
64 直接-bridge 雙 triangle；每份完整邊、degree 四、critical
witnesses 與十列 Σ 重算，無新來源 catalogue。

3,440 次目標比較：1,032 個目標接受列在原 M 已空；2,122 個
拒絕列的 K 超過容量；286 個比較進入固定支援，共 9,152 次。
8,508 次跨列衝突，644 次代數相容但同源收縮星非 disk，零殘留。
去掉同一 core／S 的目標重複後共 188 subdivisions：178 K₃,₃、
10 K₅。完整式子與各家族的傳遞見專題報告。

[Checker](../../scripts/c5_excess_two_mixed_omission.py)／
[artifact](../../artifacts/c5_excess_two_mixed_omission/observations.json)
保存兩份原側全圖 relations、完整 joint tuples、逐 tuple witnesses、
全部固定支援函數域、逐查詢 conflicts／assignments 與 subdivisions。
344 原長圖保持同一框／roots／附件及全部收縮 branch sets，
6,880 次刪／留 zw 的完整 root-pair 比較相等；另保存原長圖自己的
全部 contact joint tuples。每家族各取三份最大控制圖，共 1,920
次獨立 pinned 色對回溯，包含空纖維；雙 triangle 為固定原六
內點。最長固定長圖含 B 共 22 點。

20 張原 C 接回完整圖包含 shared singleton／shared edge／不同
contacts 的 edge／path／triangle；200 次完整接合均與原圖回溯
相同，976 次原 C 的完整 relation transport 相同。實際 marginal
負控制為 form 224、列 4，K={(3,1)}，原 shared singleton 的
角色 T_C={(1,1),(3,3)}：marginals 相乘會誤造可接回 tuple，
原完整接合卻為空，附兩部分原圖 coloring witnesses。

## 實際驗證及未重跑範圍

新 checker 以下兩種 hashseed 的逐 byte 重播均通過；lake build
通過（8,831 jobs，僅既有 style／unused simp warnings）：

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
lake build
```

直接容量與原 run 依賴的重播亦通過：

```bash
python3 scripts/c5_mixed_capacity_contacts.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
```

前者的 65,535 非空 tuples、65,431 容量通過者、18 側型及固定
原圖控制均重播相同；後者的 120 palette-switch、20 三-run、
8 第一段重複排除與八份兩-run 正常形均相同。

文件、DocGraph、artifact 狀態與 whitespace 收尾檢查通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

文件檢查為 480 Markdown／4,968 local links，anchors／index／
handoff 全通過；DocGraph 為 62 documents／213 relations／5
families，0 errors／notes；artifact status 為 ok=123，無
missing／changed／stale；git diff --check 通過。

新 artifact 為 56,106,614 bytes，已由 MANIFEST 與 generated ignore
登錄；目前共 123 產物／118 producers。五份大型／小型原輸入
及 adopted scripts 的 hashes 均明列，producer 依賴由 MANIFEST
追蹤。報告、前序後續標記、README、導覽與 STATUS 一併更新；
HANDOFF 的研究線及 tags 沿用，依薄索引規則保持原內容。

未重跑：前序雙 unary／spoke＋unary 全份 checker、177,280
triangle lifts 全分類、triangle fork 全批、全 degree-4 Gallai
合成、唯一 degree-6 全分拆、root 刪除／原 zw 接回全批、一般
來源 catalogue、其他出口及 Lean axiom audit。沿用它們既有
任意大小、外部 degree-list 及有限 topology 信任界線；新
checker 重驗實際採用的原完整邊集與染色，不重證外部定理。

## 跨對話接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留前序未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、Kempe導覽及即時git status，
再讀docs/c5_excess_two_mixed_omission.md及本輪history。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk、ε=2只剩雙degree5。
相鄰mixed刪roots/zw全收；恰一份mixed的(4,4)保留core已全排。
本輪補上只省略原incidence-(1,1) mixed C：Σ(G−C)=Ω。
保留原zw的相鄰roots，344必要核心、3440目標比較、9152固定支援查詢，
8508跨列衝突、644同源非disk星minor，188明示subdivisions全覆蓋。
344長圖、6880完整色對比較、1920 pinned查詢、20原C接回圖完整保存。
所以相鄰且恰一份mixed的任何rejected-row core均不能是(4,4)。
共同下界仍ε≥2，未證ε≥3；沒有新Lean theorem、一般出口或K∞=K≤5。
下一窄入口是(5,4)/(4,5)原單容量因子省略，先處理原spoke子型；
在省略圖自己的唯一degree5完整relation下，同圖接回該原spoke。
G自己仍(5,5) q-core不可套唯一degree5定理；其他來源分支保留。
重播：uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
```
