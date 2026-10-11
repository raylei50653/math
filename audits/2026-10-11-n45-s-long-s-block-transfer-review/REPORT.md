# N45-S-LONG-S-BLOCK-TRANSFER 獨立驗收

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

D 的七項 claims 通過指定範圍驗收：任意大小完整 assignment/fibre transfer 恆等式、
固定 C-interface 校準及歷史 necessary-domain ledger。無阻斷或需更正項；新增來源排除為0。

## 完整 assignment 恆等式

V-REC/K-REC 在 actual vertex/block incidence tree 展開全部原 vertices、原 bridge與
任意長 odd cycles，逐 vertex 核全部 literal attachments一次。child subtree只在具名
cutvertex 相交且同色；full assignment 的 restriction 與相容 union 互逆，故保全部
tuple preimages、空 ambient cells、diagonal、原 r 色、shared-contact單一座標與旁支。
recurrence 恆等式需 actual decomposition，無 degree4或 K11/K12 前提。

TF-X 的 full factorization 要另外供同一原 actual U與完整 X edges/spokes/contacts；
TF-RESTORE 只核同一原 r與 literal γ(b4) 的原 rb4 inequality。把 fragment升為來源
仍須全 K1–K12，特別是原 G Σ-critical 和 X 同β刪邊 witnesses。
完整逐claim核對見 [D-proof-review.md](D-proof-review.md)。

## 獨立原邊枚舉與 custody

另寫不 import worker 的 original-edge MRV DFS，完全不用 blocks作染色：四有效cases、
40列、1,344份 full assignments、2,560 ambient cells（1,966空）、640 ordered pins、
1,920 spoke-filtered pins及所有 restored preimages逐項與原certificate相等。
五份宣告全部保留；BRIDGE_BAD6 的原 l0完整degree5失敗亦精確保留，非target反例。
三份負控制的單一r色、空cell、原旁支座標刪除均由獨立完整重建核實。

checker與原 independent direct各自普通/seed17均exit0、stdout/stderr byte相同；
三負證書兩套validator共六次均exit1且命中指定原cell/vertex。native捕捉與第三套
獨立枚舉見 [checks.json](checks.json) 及 `logs/independent-original-edges.*`。

獨立custody核170 payload/24,839,641 bytes；唯一排除根 delivery.json。12 BASE與
11 sealed audit authorities對原live、本地與dispatch frozen、BASE blob精確相符。
1204份原protected files及加certificate後1205份全live零漂移，整原樹、HEAD與
tracked diff不變。詳細inventory/pins/findings見 `logs/independent-custody.stdout.log`。
原 delivery SHA：`ee7bd0093a4e244ee0d8c1af65f0ddedd95125861b5816c8dcbb7975aa43e0ed`。

## 採納界線

D 保留其輸入凍結時的24 schedules／38 spoke combinations／6080 symbolic pins；
這是歷史 necessary-domain，沒有使用同輪q0/q2/T1新排除作前提或重寫原ledger。
D本身的 same-source-Delta-restorable-r-fibre-nonemptiness 仍 OPEN；恆等式精確描述
所需完整介面，沒有證任何 Δ 可恢復 fibre 非空，沒有建立 actual U/G。

兩份缺 BASE observations findings 保留；dependent finite replay及舊19 controls未跑。
finite fragment controls為triggered and holds；whole-X/G、target source及非空孤立因子
finite controls為not triggered。BRIDGE_BAD6為degree4前提counterexample。
未建立 source realizability、新Lean或一般N45/N2/E closure；disk topology未驗。
只新增本review，未改原交付、共享文件或舊證書；未commit/push/PR。
機讀採納見 [acceptance.json](acceptance.json)，由 [delivery.json](delivery.json) 封存。
