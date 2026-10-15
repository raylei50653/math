# 第二輪：奇環交換下降的精確機制與平面反控制

2026-10-15；BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
只寫本獨占 audit；未 commit／push。

**新紙面成果是固定分離方向 PM 交換空間連通、任意單環交換的完整路徑
奇偶公式，以及一次切每個舊補環時的嚴格奇環下降公式。** 新36點平面
控制否決固定方向逐步降低 `(奇環數,奇環總長)`：全部12個第一步都從
`(2,10)`升至`(2,36)`，再一步才可偶補。**容許反轉分離方向時已有
11個直接偶補下降，因此本控制沒有否決原 XOR 分離下降義務。**

完整論證見 [PROOF.md](PROOF.md)，逐字可重播證據見
[certificate.json](certificate.json) 和 [check_controls.py](check_controls.py)。

| 已完成項目 | 精確域／結論 |
| --- | --- |
| 同方向交換連通 | 任意圖的普通 PM；對稱差逐環翻轉避開 e,f |
| 完整奇偶手術 | cubic 同一匹配；切開全部接觸補環，保存每段路徑及奇偶 |
| 嚴格下降充分條件 | 每舊補環恰切一次、碰至少兩奇環，奇環數下降至少2 |
| 36點平面控制 | 對偶四連通、所有度至少5、指定原邊互不相交；固定方向 μ 局部停點 |
| 20點對偶控制 | 六個奇環數非零的匹配皆無上述一次切環交換，但可用重訪舊環的交換下降 |
| 46點較弱控制 | 保 XOR 單環也可遇 μ 停點；有非平凡3割且指定原邊不互異 |

36點圖有365份完整 PM、60份固定方向狀態及390條完整單環交換，
含20份偶補。起點83的全部12個鄰居均保存；完整最短路徑
`83→3→0` 的三份 PM、補環及逐邊身份一併保存。
原具名取 `z=9,x=3,y=10,b=8` 時，by 是邊，這違反原 T 來源非邊；
因此來源排除 `not triggered`。其平面性、度數、全部≤3割與四個原端點
則由邊表、coherent face/rotation、對偶重建直接核對。

三控制共1361份完整 PM；獨立頂點子集 DP 再核完整計數。
允許狀態的全部9289條交換都核路徑奇偶公式，不只核選中的成功路徑。
資料沒有假定 edge-Kempe 連通，也沒有把跨匹配 witnesses 拼成單份染色。

凍結原來源與前輪輸入見 [INPUTS.json](INPUTS.json)：BASE tracked 原件
與第一輪尚未 commit 的交付分開記錄，逐檔 SHA256、重播 drift=0。
具名圖見 [graphs.json](graphs.json)，也由 hash 固定。生成探測只使用
三個既有具名控制與一個明確四邊拼接，沒有跑來源全集或提高枚舉界。
`probe_*.py` 和 `probe-*.json` 保留產生路徑；重播正式證書僅需標準庫。

```sh
python3 -B audits/2026-10-15-oddness-descent-6ddea32/check_controls.py --check audits/2026-10-15-oddness-descent-6ddea32/certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-oddness-descent-6ddea32/check_controls.py --check audits/2026-10-15-oddness-descent-6ddea32/certificate.json
```

正常、seed17、漏一個允許鄰居與錯路徑奇偶的負控制，詳見
[VERIFICATION.json](VERIFICATION.json)。`--write` exclusive-create，
`--check` 完整重建證書、拒絕缺漏與多餘欄位；無弱化 source 介面。

Closure scope：交換連通及局部手術／充分下降定理；明確候選規則的反控制。
Remaining OPEN：完整合法來源的保 XOR 下降或平台離開定理、ω=0、
完整319來源排除及一般主命題。無新 Lean theorem，無新來源實現，
沒有改原文獻、外部定理、權威 docs 或既有界。
