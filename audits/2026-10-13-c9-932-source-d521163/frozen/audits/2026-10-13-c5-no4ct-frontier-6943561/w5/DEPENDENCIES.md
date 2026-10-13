# 全內部 W5：新三支契約的依賴帳本

BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`。所有引用使用本包 frozen
bytes；不是沿用舊文件中尚保留的普遍 4CT 推導。數學論證見 [PROOF](PROOF.md)。

| 所需事實 | 新 no4ct 依據與精確限制 | 本輪作用 |
|---|---|---|
| 全域內點最小性、再最大邊數；K132 與 ≤5 witnesses | [目前交接 §§2–3](../frozen/docs/tasks/c5_no4ct_handoff.md)；對所有目錄外來源最小化，非固定 mask 最小性 | 替換後保持完整 Σ，即可比較內點數 |
| Σ∈D5·{932,933,941}，G 簡單、二連通、B induced、內面三角化；k≥16 | [度數／球面接入 §§1–5](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)與交接；不假定 singleton support 非空 | 三支共同来源，包括 932；無界來源並未排除 |
| 原內點完整 degree≥5、B degree≥4、無 occupied triangle | [度數接入 §§2–3](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)及[完整外圈契約](../frozen/audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md) | 小 patch 的 degree、原框接點與 induced rim |
| C4 完整有序關係有 ≤3 內點代表 | 同上度數接入 §2 的**受限** s<k 引理；本輪逐原 C4 證 i(C)≥1，故 s≤k−i(C)<k | 修復舊任意大小 C4 前提；推出原 C4 無內點 |
| proper C5 cap 有 ≤5 內點代表 | 每個 proper C5 亦有 i(C)≥1；s<k，由全域最小性使其完整 Σ∈K | 原 proper C5 cap 空或恰一 W5 中心 |
| 同框 cap 替換保持外 B 完整 Σ | 按每份 literal 介面指派的共同 full-lift 存在性接合；不使用 fibre 數量相等 | k′=k−s+s′，若 s 大於代表上界即嚴格下降 |
| 小 patch counting、五個雙接 apex、深層 identity | 本輪 [PROOF §§3–5](PROOF.md)，重新由 Euler、outerplane 邊界、原面與 rotation 證明 | n5(deep)=1+X+h1；三支皆有全內部 induced W5 |
| 舊 W5 母結果的來源與比較範圍 | [原結構證明 §§1–5](../frozen/audits/2026-10-12-c5-deep-five-wheel-01a12ffa/review/separator_proof.md)及[五輪母入口](../frozen/docs/c5_degree5_link_reductions.md) | 僅識別已知結構與本輪修復差異，不直接繼承舊 universal C4／4CT 前提 |

本輪新論證不消費 4CT、普遍 exterior screen、任意大小 C4 定理、C7 普遍
可染性、私人圈秩證書、N2／ε／Gallai 契約或 annulus 小代表構造。
保留的上游信任是 no4ct 有界結果中已明列的 K132 witnesses、外部有限計算
定理與 plantri 完備性／實作；本輪沒有重跑它們。W5 接入本身是條件性
紙面證明，不是 Lean 完整形式化，也沒有構造真正目錄外來源。

採納範圍僅為本輪原 C4／proper C5 cap 結構、(6) 的精確深層五度點計數及
全內部 induced W5 存在性。ρ≥5、一般四接點壓縮、h≥4 無界來源排除、
無界三支與 K∞=K≤5 均未由本輪宣稱完成。
