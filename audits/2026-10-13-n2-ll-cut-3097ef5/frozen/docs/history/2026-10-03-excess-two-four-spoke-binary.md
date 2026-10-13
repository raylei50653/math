# 2026-10-03：四-spoke (3,1) 一原 binary 的 marked-leaf 必要化約

接續使用者交接的 [兩單接點 unary 排除](../c5_excess_two_mixed_core_four_spoke_singles.md)，
推進所選 mixed-(1,1) 加一原 binary unary。接手基準
`b63a0965434d68a28292994638b2c98e848585b8`，工作目錄
`/home/ray/developer/ai/math`；main 比 origin/main 多一份既有提交，
且工作樹保留前輪 singles 的 checker、報告、產物政策與文件修改。
本輪保留這些變更，未要求也未執行 commit／push。

## 本輪結果與證據界線

[新報告](../c5_excess_two_mixed_core_four_spoke_binary.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_binary.py)及
[joint helper](../../scripts/c5_excess_two_four_spoke_binary_joint_controls.py)
保持固定 933／941 完整 Σ、每條非框邊 Σ-critical、有序 induced-C₅
disk、相鄰唯一 mixed、ε=2 的原圖前提。三-spoke 側 a、一-spoke
側 b，原 C incidence-(1,1) 與原 U incidence-2，含 root 交換。

完成的任意大小必要步驟：

- 原 contact 邊 critical witness 與原 b–a–b_h 路徑，排除 U 的
  全部空／單點／框邊支援；兩 contacts 始終同一原 U。
- 同色 spoke 省略的原 K=C∪{a} 是 t=1、(2,2) minimal core。
  原 leaf slack 迫 F_K⊆L，完整 K schemas 的最大 invariant 原 C
  反像給精確的 relation-algebra 相容性判準。
- 若 K 禁兩色，原 C 完整 relation 必恰為對角 pair；原 x–y
  path 是偶數長原 bridge path，含 x=y、長度零的情形。

沿用完成的 `(2,2)` 102 份來源保留 IDs，整圖反射成 196 份
records。80 份具名附件、200 份同色原省略 queries；每個省略的
原 C support 都要同時給 S_K=S_C∪保留 a-spokes，同一字面列
還要有共同完整 schema。關係反像後共有 376／776 份同源域，
原 U 短支援分別排除 260／520 份，保留 **116／256** 份。
全部殘留有原 K／U 共同 lifts；本輪此層零新增排除。

933 的 116 份、941 的 232 份只含 K pair queries；941 另 24 份
在不同原列分別要求 K singleton／pair。數字是具名必要域，
不是 graphs、完整十列 joint 模型或 disk witnesses，整型尚未排除。

保存兩候選共同具名入口：a=6、b=5，a-spokes=012、b-spoke=0，
S_C=012、S_U=234。q=01021 的必要完整 C={(2,2),(3,3)}、
K={(2,3),(3,2)}、U={(1,2),(1,3),(2,1),(3,1)} 接合拒絕。
此 witness 只承擔單一原列的必要 relation algebra；下一步應研究
原偶數 bridge／root cycle 與同圖跨列 palettes。

另有 24 張原完整度數圖，含 root 交換、C singleton／edge／triangle、
U 的兩種 edge／偶數 path／triangle。720 次整圖接合及 11,520 次
pinned (b,a) 的完整 (y,u,v) 纖維，與獨立回溯一致；144 份同色
spoke 等式一致。保存 C 的共鄰 contact 假接合，以及原 binary
U={(2,3),(3,2)}、b=2 的 marginal 假接合。這些圖不聲稱候選
Σ、criticality 或 disk；每份完整 tuple 有原圖 coloring witness。

## 前序原表的文件 hash 漂移

`PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_two_two.py --check`
在本輪**失敗**。重算完整 `run()` 並逐欄比較 JSON，唯一差異為
`inputs/docs/c5_single_spoke_cores.md`：

- 原記錄 SHA256：`45ce7c44289d8738cab19d3cc8ac679fb4637c97727a45efcf69ce8467bf5c1b`。
- 目前文件 SHA256：`5f37ffbd6f0f9ba4c279fc37fc5eb7eadfd0ce234076aeb27f5094f429bc2310`。

全部數學 payload、1530 原 records、完整 relation schemas、支援、
數字、源圖 controls 及整份 `support_table.md` 都相同。本輪未修改
該 cores 文件，也未覆寫原 16,148,688-byte artifact；避免連鎖重寫
完整前序 source／target 證書。完成的 residual-locality `--check`
通過，仍檢查它保存的原 102 records 與原 base 的字面相同。

新 checker 加入可重播的 `inherited_base_replay_audit`：重算原
完整數學 payload 及 table，斷言只有 docs provenance 有差異，保存
兩份 hashes 與原 artifact digest。因此新證書的通過包含這份數學
payload 核對，**不表示前序 byte-check 已通過或 hash 已修正**。

## 實際重播與本地環境

本環境 `uv run --with networkx==3.5` 首次因全域 cache 只讀而未啟動。
使用既有唯讀 cache 的精確 networkx 3.5 套件，設定
`PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f`，執行
下列 `python3` 形式；沒有安裝或修改全域套件。報告保留可攜的 uv
重播命令，實際環境差異在本節明列。

新 checker 以 `PYTHONHASHSEED=17` 與預設 seed 各作 byte-check；
完成的 residual-locality、短支援定理、前輪 singles 與 `lake build` 也重播。
Lean 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel linter
warnings；未新增 Lean theorem，不形式化本輪紙面 topology。

本輪實際通過的 checker 命令如下；新 binary 的兩次重播都包含
`inherited_base_replay_audit` 的完整數學 payload／table 比較：

```bash
PYTHONHASHSEED=17 PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f python3 scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f python3 scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
PYTHONHASHSEED=17 PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f python3 scripts/c5_excess_two_mixed_core_four_spoke_singles.py --check
PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_residual_locality.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

本輪未重播全部九份雙 root checker、唯一 degree-6 各分拆、歷史
catalogue／Gallai／R-series／weak-deletion／Kempe 或 Lean axiom audit。
原表的 source exclusions 按完成報告沿用，另重播最終來源表與原
base 數學 payload；不把這份核對寫成整線重驗。

新 observations 留在本地，依大型產物政策由 `.gitignore` 排除，
MANIFEST 記錄完整 bytes／digest、producer／依賴順序。報告、README、
STATUS、Kempe 導覽、全線整合及前輪 singles 的後續連結同步。
HANDOFF 的薄索引與研究線 tag 未改變。

新 observations 為 **18,888,946 bytes**，SHA256
`385799e64e72ea57f089c48bda48e55b02d8bcca5301e79dcd8ceaa11720b052`。
artifact status 為 `ok=127`，無 missing／changed／stale。
文件檢查通過 489 份 Markdown／5,019 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過。原 cores 文件及原 base artifact 保持接手 bytes，
原表 byte-check 的單一 provenance 差異仍明列於前節。

## 停止點與跨對話摘要

**完成 binary 的必要化約，整型尚未排除。** 共同 ε≥2 與前輪
兩單接點 unary 排除不變。其他 incidence 分拆、四-spoke／較少
spokes、單省略、原 (5,5) q-core、多 mixed／no-mixed／非相鄰
roots 保留；ε≥3、一般出口、來源實現及 K∞=K≤5 未證。

```text
cwd=/home/ray/developer/ai/math；先讀docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md及docs/c5_excess_two_mixed_core_four_spoke_binary.md。
接手b63a096；保留前輪工作樹，未commit/push。
固定933/941完整Σ、edge-minimal induced-C5 disk，ε≥2；相鄰唯一mixed，
四spoke(3,1)的mixed(1,1)+兩單接點unary已全排。
本輪推進一原binary unary：原U短支援排除、原leaf完整反像、同源支援／
同列完整schemas後保留933/941的116/256必要域，含root交換，整型未排。
雙禁色K迫原C精確對角pair，x-y是偶數原bridge path，含x=y零長度。
下一窄入口a-spokes012、b-spoke0、S_C012、S_U234；q01021下
C={(2,2),(3,3)}、K={(2,3),(3,2)}，保留原U完整二接點joint與跨列palettes。
24固定完整度數圖、720全圖joins、11520 pinned完整(y,u,v)纖維通過。
舊two_two byte-check只有cores.md來源hash漂移；新checker核對全部舊數學
payload與table相同，保留原artifact。未新增Lean theorem，ε≥3未證。
重播：PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
```
