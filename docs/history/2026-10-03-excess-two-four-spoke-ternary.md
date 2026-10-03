# 2026-10-03：四-spoke 原 mixed-(1,2) 三接點身份整型排除

基準 `b63a0965434d68a28292994638b2c98e848585b8`，工作目錄
`/home/ray/developer/ai/math`。接手前序 singles／binary／star／hubs
的未提交工作樹，推進使用者指定的下一窄型。本輪未要求也未執行
commit／push，沒有來源圖新枚舉。

## 結果與證據

[新報告](../c5_excess_two_mixed_core_four_spoke_ternary.md)／
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_ternary.py)
完成四-spoke (3,1)、mixed-(1,2) 加一原單接點 unary 的來源排除，
含 root 交換。先固定原 a=6、b=5、a-spokes=012、b-spoke=2、q=01021。
刪 a0／a2 時保留同色原 spoke，M 仍拒絕；原 (4,4) 身份全排與
degree-4 飽和迫 M 自己是唯一 degree-5 minimal q-core。

M−b 是整份原 K=C+a 與原 U，原接點分拆 (3,1)，K contacts 是
(a,y₀,y₁)，不是 binary。原 C 仍保留三接點 (x,y₀,y₁)，允許
x=y₀／y₁；完整六點 joint 為 (b,a,x,y₀,y₁,u)。marked a 的 boundary
lists 迫 F_K={2,3}、F_U={1}，前序 single-spoke (3,1) active-triangle
定理的所有前提在同一 M 成立，給原 G 的 K₅ minor。

933／941 的 20／60 份具名必要框架全部至少有一份這種原同色省略。
200 個 queries 中 48 份先由 marked-leaf slack cover 矛盾排除，其餘
152 份對齊既有三接點 covers；整型剩 0／0。核對 80 個 root 交換、
2,000 次整體 D₅ query 搬運及 320 份保留原 a 為 arm 末端的 K₅ skeletons。
Skeletons 不聲稱完整 degree/list 或候選來源實現。

另有 50 張完整 degree 圖、1,500 次獨立完整六點 joint、1,500 次完整
K 三接點 relation、24,000 份固定原 (b,a) 的空／非空纖維及 300 次
同色 spoke 等式，全部核對。每份 C／U tuple 保留整份 coloring witness；
shared x 只有同一頂點顏色。存原 ternary marginals 假允許、完整 guarded
fiber 為空的反例；這些完整圖不聲稱 disk、Σ=933／941 或 Σ-critical。

任意大小由紙面身份傳遞及既有 active-triangle／Gallai 論證承擔。
本輪核對 Dvořák 講義 Lemma 7／Theorem 10 的 degree assignment、
tightness 與 block palettes 前提；沒有從 320／800 minors 或短圖外推。
共同 ε≥2 不變；ε≥3、一般出口、K∞=K≤5 未證，未新增 Lean theorem。

## 實際重播、hash 邊界與產物

新證書預設 seed 與 PYTHONHASHSEED=17 的逐 byte checks 通過；既有
(3,1) checker 與原 binary hub checker 重播通過：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_three_one.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

既有 (3,1) 的全部 saved payload 原樣重算相等：15 covers、356 tight
attachment rows、792 palette states、512 parity controls、800 minors、
800 reflections 及八個負控制；新 checker 每次重播亦核對完整 payload。

另實際嘗試原單 spoke 的歷史 byte-check：

```bash
PYTHONHASHSEED=17 PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f python3 scripts/c5_excess_two_mixed_core_single_spoke.py --check
```

**此項 byte-check 未通過**：只在原 root-deletions、mixed-omission、
mixed-core-spokes 三份 docs 的既有 input hashes 不同；這三份文件本輪未改。
隨即使用同一 networkx3.5 cache 做下面的唯讀數學 payload audit，通過，
確認 20／60 必要框架及整份數學內容不變：

```bash
PYTHONHASHSEED=17 PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f:scripts python3 - <<'PY'
import json
from pathlib import Path
from c5_excess_two_mixed_core_single_spoke import build
saved = json.loads(Path('artifacts/c5_excess_two_mixed_core_single_spoke/observations.json').read_text())
current = json.loads(json.dumps(build()))
old_inputs = saved.pop('input_sha256')
new_inputs = current.pop('input_sha256')
assert saved == current
drift = [p for p in new_inputs if old_inputs[p] != new_inputs[p]]
assert drift and all(p.startswith('docs/') for p in drift)
print('complete mathematical payload equal; document drift:', sorted(drift))
PY
```

新 observations 明存這三份 provenance 漂移及原 source digest。
更前序 two-two 的單一 c5_single_spoke_cores docs hash 漂移亦仍保存；
沒有覆寫任何舊 artifact，沒有將歷史 byte-check 寫成通過。
本輪未重播原 binary／star／singles、其他雙 root／唯一 degree-6、
R-series、weak-deletion、來源圖 catalogue 或 Lean axiom audit。

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；這不形式化新 topology。文件檢查通過 495 份 Markdown／
5,072 個本地連結；DocGraph 通過 62 documents／213 relations／5 families，
零 errors／notes。產物 status 為 `ok=130`，無 missing／changed／stale，
`git diff --check` 通過。HANDOFF 研究線與 tags 未變，依治理規則
維持薄索引；README、Kempe 導覽、STATUS、全線整合與相關前序後續已更新。

新 observations 為 **25,895,377 bytes**，SHA256
`a5b2720255048e94eae4a129fb395dff107e36e6b354aed072a3b355e230233e`。
依大型產物政策留本地，MANIFEST 記錄 digest 及 producer；舊產物保留。

## 停止點與貼用摘要

```text
cwd=/home/ray/developer/ai/math；先讀docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md及docs/c5_excess_two_mixed_core_four_spoke_ternary.md。
保留b63a096上的既有工作樹，本輪未commit/push。
完成四-spoke(3,1)、mixed-(1,2)+一原單接點unary及root交換的來源排除。
原a012/b2、q01021省略a0或a2；M自己是唯一degree5 minimal q-core。
M-b保留整份原K=C+a與U；K contacts=(a,y0,y1)，原C=(x,y0,y1)，共享x保留。
marked a迫完整K禁{2,3}、U禁{1}；既有(3,1) active-triangle原K5全部前提接上。
933/941原20/60具名框架全排；200queries、80 root交換、2000 D5、320 marked minors。
50完整degree圖、1500全圖六點joints、1500完整K relations、24000 pinned fibres、300等式。
重播：PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check。
既有three_one與binary_hubs byte-check通過；lake build通過8831jobs。
原single_spoke byte-check因三份既有docs hash漂移未過；完整數學payload唯讀重算相同。
更前序two_two單一docs hash漂移保留；所有舊artifact不覆寫。
下一窄型mixed-(1,3)無unary：原C+a四contacts(a,y0,y1,y2)，先核對三禁色及leaf slack。
該型本輪尚未證；其他四/較少spokes、(5,5)、多mixed、no-mixed、非相鄰等仍保留。
共同ε>=2不變；ε>=3、新Lean theorem、一般出口、來源實現及K∞=K≤5未證。
```
