# N45-S-LONG-S-T2-Q0-RESTORE 獨立驗收

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

三份 schedules 933/0234、941/023、941/024 的任意大小紙面排除通過獨立驗收。
九項 claims 在指定完整 K1–K12 範圍採納，無阻斷 finding、無需修正文義。
採納只記在本新 review；原 worker 的 pending bytes 與所有共享文件保持原樣。

## 完整同源證明

範圍是原 U owner=s、U012/L234/pair S40、原 r-split(2,2)、s-split(1,1)、
t_s=2/spokes02、β=q0、X=G−原 rb4，且 X 本身是 β-minimal core。
原 S 及各件的大小、blocks、bridges、旁支不設上界。所有 K1–K12，包括原 G
的逐邊 Σ witnesses 與 X 的逐邊 β witnesses，均保留。

原 actual U 和 spokes 在 β/q1/q2 強制 s=3。直接 complete-degree/contact
list-slack 論證給每個 L/S 完整 forbidden r 欄至多兩色；β 拒絕迫兩欄各二色且
互補。原 S 的 N-diagonal 必要充分介面已對回 BASE E4 及 Phase B B-SD：
原外側連通並具全部所需 B-touch，故 S(β;3,3) 非空、3 不在 S 的禁色欄。
三份原 G 均接受 q1；L 的完整 (0 1) 雙射排除 S 禁色欄={0,1}，迫 β 下 S 禁 r=2。
S 的完整 (1 2) 雙射遂給 q2 的 r=1 fibre 空。雙射作用於每個原 vertex、全部
ordered/shared contacts、tuples 和每個 preimage；空 fibres 與 diagonal 同時保留。

沿用已採納 Q(X)={β}，q2 的完整 X lift 聯集非空。每份 lift 均有 r≠1=q2(b4)，
故全部恢復同一原 rb4；三份原 Q(G) 均拒 q2，逐份矛盾。非空池是
(r,s)=(0,3),(2,3),(3,3) 的聯集，沒有聲稱每個個別 fibre 非空，也未證個別
q3/q4 恢復。完整論證與充分前提核對見 [paper-review.md](paper-review.md)。

q2 存在性明列繼承 SF-QX、SF-T2-EXTEND 與 E2 paper/finite-terminal 信任鏈；
本輪沒有重新證明或重播該历史鏈。q1 存在性直接由原 K2 得到。額外查用的三份
BASE proof 文件已凍結於 `authority/`，含 Git blob/SHA/size pins。

## 獨立校準及 custody

普通與 seed17 原生只讀重播均 exit0，stdout/stderr 逐 byte 相同；兩個指定負控制
均 exit1 且在指定 certificate/coverage 階段拒絕。delivery verifier exit0。
另一份不 import worker 的算術核對涵蓋三欄案例、兩個唯一 s=3 固定的 support
permutations、32 ordered pin maps、三 schedules 的30列/480 pins，其中120
diagonal。這些是 abstract interface arithmetic，沒有 actual source assignments。
詳見 [algebra-review.md](algebra-review.md)、[checks.json](checks.json) 和 `logs/`。

獨立 inventory 核對通過76份 payload/1,665,969 bytes；整樹77個 regular files、
5個 directories，唯一 manifest exclusion 為 delivery.json。無 symlink、special
entry、重複/缺漏/額外 payload 或 hash mismatch。12份 BASE 與11份 sealed
physical audit 權威分列，3份 dispatch metadata pins 相符；60份原 recorded inputs/
舊證書 before/after/live 相等。root另加三份 BASE proof，63份 guarded authority
及整個原 target tree 均零漂移，HEAD/所有 tracked diff 不變。
原16份 metadata-initial/history 已保留，不能替代 final authority。
詳見 [custody-review.md](custody-review.md) 與 native independent-custody logs。

原 delivery SHA256：`920a7161ac5c758dea78c45b9360eb00f81bc6f91ea0c39b45e09723e026b349`。

## 剩餘域與證據界線

前次24份必要 schedules 中僅刪除此三份，剩21份：t_s=1 的14份，以及
t_s=2/β=q2 的7份（35份 schedule/spoke combinations）。前次 q1-restoration
已排另四份，合計排盡原 t_s=2/β=q0 的七份必要 schedules；這個分支只在完整
指定契約與已採纳 Q(X) trust 邊界內閉合。ledger 見
[remaining-schedules.json](remaining-schedules.json)。沒有使用同輪其它新成果。

兩個既有 observations 缺 BASE blob findings 由 git show 再確認，physical/
quarantine 均不補作權威；依賴該 bytes 的 finite replay 未執行，舊19 controls
未重跑。target source executed=false、trigger_count=null、not triggered。
未建立 source realizability、新 Lean 或一般 N45/N2/E closure。

本輪只新增專屬 review 目錄，未改共享文件、原交付或舊證書；未 commit/push/PR。
機讀採納及完整範圍見 [acceptance.json](acceptance.json)，本 review payload 由
[delivery.json](delivery.json) 封存。
