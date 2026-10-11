# N45-S-LONG-S-T2-Q2-RESTORE 獨立驗收

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

七份 schedules 的任意大小紙面排除通過；九項 claims 在指定完整 K1–K12 範圍採納。
coverage 須附112-cell更正 overlay，無紙面阻斷。採納只記在本新 review。

## 同源完整非空 fibres

固定原 U owner=s、U012/L234/pair S40、r-split(2,2)、s-split(1,1)、
t_s=2/spokes02、β=q2、X=G−原 rb4 且 X 自己 β-minimal。
complete-degree/slack 給全 assignment 存在性和禁 r 欄至多二色。S 在 β 的
attachment 色10，完整 (2 3) map 固定 r0/r1，讓唯一 actual s-contact 避3，
故 S(β;0,3)、S(β;1,3) 均非空。原 U 的已採納 β 避3 preimage 及 Xβ拒絕
迫 S 禁欄={2,3}、L 禁欄={0,1}。得到不同 r 的局部種子 L(β;2,3)、S(β;0,3)，
不把它們當作同一 β whole lift。

全頂點色雙射將兩種子帶到共同 q3／q4 frame 與共同 pins(0,3)。目標 U 的
actual query010 另由 strict slack 及 (2 3) 證完整避3 preimages 非空。
全部 actual L/S/U preimage sets 與原 Col^I 的 restriction/union 給精確
L_X(q3;0,3)、L_X(q4;0,3) 非空完整 fibres。每份 lift 的原 r=0 不等於
本列 b4 色1／2，故原 rb4 全部恢復；所有 original/shared contacts、空 fibres、
tuple preimages 和旁支保留，大小沒有上界。

選 q4 覆蓋933/0124、933/0234、933/1234、941/024、941/124；選 q3 覆蓋
933/0123、941/023。每份選定列都在原 Δ，與原 G 拒絕矛盾。
详證見 [q2-paper-review.md](q2-paper-review.md)。新目標 fibres 的存在性直接構造，
不使用 Q(X) 或舊 finite-terminal 供存在性；仍繼承已採納 SF-T2-ROLE 的 β U 角色。
其它未構造列的 QX metadata 另保舊信任邊界。

## 必要更正與獨立校準

原 coverage 漏標四份 T4 literals 01203/01213/01231/01232 的 U012 identity：
F_U(β)={1} 使其 s=1 的全部 X pins 空。7 schedules×4列×4 r pins 共112個
cells，原全標 source-specific，須改 empty；原 G filter/rejection flags 不動。
[q2-coverage-corrections.json](q2-coverage-corrections.json) 逐項綁原 SHA、JSON pointer、
原值與修正理由；[accepted-coverage.json](accepted-coverage.json) 保存採納副本。
此更正不影響兩份非空 fibres、七份 Δ 覆蓋或校準計數，原交付 bytes 不動。

普通／seed17原生只讀重播 exit0、stdout/stderr byte相同；兩個負控制均exit1，
manifest verifier exit0。另一份無 worker imports 的獨立腳本核720 S4 comparisons、
6 partitions、4 full ordered-pin transports（64 maps）、70列/1120pins/280diagonal，
以及112-cell遺漏；不把只檢位置與色 maps 的 worker checker 說成已驗必要空分類。
原始校準值與更正採納範圍詳見 [q2-custody-algebra-review.md](q2-custody-algebra-review.md)。

custody 通過90 payload/5,015,240 bytes、92 regular files、14 directories，
唯一排除是根 delivery.json 和 seal-receipt.json；frozen同名manifest照列payload。
12 BASE、11 sealed physical authorities及一份外部 PDF 全相符。原1037 records
對應1036 distinct files（同一 Gallai PDF 重複記兩次且同 hash），全live零漂移；
原樹、HEAD、tracked diff不變。失敗 manifest-generation 與 exit1 原生紀錄已保留。
原 delivery SHA：`79dc6912fbd13f863986d1d85e6f4b9490920711e023d8c2ab33feb8cd454605`。

## 剩餘域與停止點

整合已驗收 q0 ledger 僅用於計數，未作本證明前提：21→14 necessary schedules，
剩 t_s=1 的 βq3七份／βq4七份及28 spoke combinations；原 t_s=2 的14份
必要 schedules 已在完整指定契約內全排。見 [remaining-schedules.json](remaining-schedules.json)。

兩份缺 BASE observations findings 保留，dependent finite replay與舊19 controls
均未執行。target source executed=false、trigger_count=null、not triggered；
source realizability、新 Lean、一般 N45/N2/E closure 均未建立。
只新增本review，未修改共享文件、原交付或舊證書；未commit/push/PR。
機讀判定見 [acceptance.json](acceptance.json)，review由 [delivery.json](delivery.json) 封存。
