# 2026-10-03：ε=2 原路徑接回 root 邊的 K₅ 排除

接手基準 `722bfa6`；工作樹已有上一輪原 root 刪除／雙 triangle 接回的
未提交 bundle，完整保留。使用者要求「繼續推進 ε ≥ 3」。先讀 HANDOFF、
STATUS、Kempe 導覽、原 root 刪除報告與 Git，選定其窄停止點：相鄰
degree-5 roots，恰一份原 mixed，N=G−zw 仍拒絕 singleton 列，N 的
全 degree-4 內部為樹／偶數頂點路徑。本輪沒有 commit／push。
成果見 [專題報告](../c5_excess_two_path_edge.md)，當前接手點由
[Kempe 導覽](../c5_kempe_guide.md) 維護。

## 任意長度原圖排除

沿用原 N 的 minimality／飽和與全 degree-4 樹分類；q 搬至 01012 時，
兩端附件為 L={0,1,4}、R={2,3,4}，單 run 的全部實際附件為 {1,4}
或 {2,4}，兩 runs 則依序為這兩組，並包含整條路徑的反向型。
原同 palette 附件恆定性把二／四／六內點基底的共同 b₄ 鄰點帶回
每個原頂點；每點亦至少有一份 B∖{b₄} 原附件。

接回原 nonedge zw 形成內部環。保留原 z、w 位置與整段原 z–w 路徑，
五份 K₅ branch sets 為 {z}、原中間路段、{w}、{b₄}、{apex,b₀,b₁,b₂,b₃}。
首末路徑邊與原 zw 使前三份兩兩相接；共同 b₄ spokes、其餘原附件及
apex-b₄ 給另外七條接線。五份都連通、非空且互不相交，因此直接在
原 boundary-apex 圖給 K₅ minor，與 disk 矛盾。

這個任意大小推導不壓縮原 z,w markers，不需先證舊 run transfer 保存
兩個指定點的 relation。有限染色控制另外保留完整有序色對與見證。
樹／路徑分支整型排除；前輪雙 triangle 已排除，所以刪 zw 仍拒絕的
相鄰 mixed 只剩單 triangle 加原樹枝。共同 ε≥2 尚未提高成 ε≥3。

## 固定完整關係證書

[Checker](../../scripts/c5_excess_two_path_edge.py)／
[artifact](../../artifacts/c5_excess_two_path_edge/observations.json) 先重建全部
16 份保存的 disk 路徑基底；由實際邊集重算 Σ histogram 為 894:4、
1018:4、1022:8，再按重算 T4 選出八份，不以舊 Sigma flag 作 oracle。
這八份是具名基底 lifts：二份空 word、四份單 run、二份兩 runs。
原 apex rotations、degree、q-critical witnesses 與所有附件均核對。

空 word 保留原二點；四份單 run 各用長度二、六；兩份兩 runs 各用
(2,2)、(4,6)，共十四份固定原路徑，全部原 nonedges 的接回共 226 份。
每份接回保存原 contacts／components／ownership、實際支援、原環與
全部 K₅ branch sets；checker 直接核對十條原接線及原集合連通性。

2,260 次十列查詢保存完整 ordered (z,w) relation，每個 tuple 都指向
同一原路徑、同一列的完整 coloring witness。動態傳遞保留兩個 marker
座標，與獨立完整回溯比較，再以加回原 zw 後的直接回溯核對同 tuple
異色過濾。沒有把兩端 marginals 或獨立 S₄ 正規化拿來接合。

固定接回 histogram 為 266:35、592:35、830:8、894:21、990:14、1016:8、
1018:21、1022:84；84 份仍接受 T4 的接回全保持 Σ=1022，亦全帶 K₅。
不將這些固定染色數字外推任意長度；來源排除由原附件覆蓋與原環 minor 負責。

## 本輪實際驗證

```bash
python3 scripts/c5_excess_two_path_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_path_edge.py --check
python3 scripts/c5_excess_two_root_deletions.py --check
uv run --with networkx==3.5 python scripts/c5_tree_cores.py --check
uv run --with networkx==3.5 python scripts/c5_odd_join_cores.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

新 checker 的兩種 hashseed、原 root 刪除 checker、tree／odd-join checker
均通過逐 byte 重播；`lake build` 通過（8,831 jobs，只有既有 style／
unused simp warnings）。文件檢查通過（470 Markdown、4,860 local links）；
DocGraph 通過（62 documents、213 relations、5 families，0 errors／notes）；
大型產物完整性 `ok=118`，沒有 missing／changed／stale；`git diff --check`
通過。人工覆核原附件族、原 marker 不相鄰、五份 branch sets 的互斥／
連通、全部十條原接線與任意長度證據界線。

證書為 2,475,798 bytes；依既有大型產物規則登錄 MANIFEST／generated
ignore，原 117 份紀錄保留，新總數 118。README 維護 excess 接手入口，
STATUS 新增專題／歷史直接索引，Kempe 導覽把下一窄題改為單 triangle，
前輪 root 刪除報告加後續連結。HANDOFF 的研究線及進行中 tag 未變，
依薄索引治理保持原內容。

未重跑唯一 degree-6 全批、no-mixed／mixed 出口全批、source catalogue、
單 triangle 全批、全 degree-4 Gallai 合成或 Lean axiom audit；沒有新增
一般圖 catalogue、外部文獻 oracle、Lean theorem 或來源實現結論。

## 接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留上一輪未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、c5_kempe_guide與即時git status，
再讀docs/c5_excess_two_path_edge.md及前輪c5_excess_two_root_deletions.md。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk，若ε=2只剩雙degree5。
新增：相鄰mixed，Σ(G−zw)≠Ω時，原全degree4樹／偶數路徑分支整型排除。
八份T4路徑基底與原run附件恆定性迫每個原內點接singleton框點b4、
也接另一框點。原zw形成原環；原z、中間原路段、w、b4、外側apex+其餘B
直接給原boundary-apex圖的K5 minor，不壓縮兩個markers。
14份固定原路徑、226份原nonedge接回全有K5；2260完整有序色對查詢通過。
重播python3 scripts/c5_excess_two_path_edge.py --check，另hashseed17。
紙面+Python，未新增Lean theorem，共同ε≥2仍未提高為ε≥3。
下一窄題：相鄰恰一mixed，Σ(G−zw)≠Ω，原degree4單triangle加原樹枝。
保存z,w在原triangle／原枝的位置、原attachments、contacts、完整色對及同一色框。
未保留這兩點的tail縮減不能直接提供原zw接回後的完整Σ。
刪zw全收、no-mixed、非相鄰roots與原unary側例外仍保留。
```
