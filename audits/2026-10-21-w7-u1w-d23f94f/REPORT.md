# W7 原 u1w 四型：完整來源排除

2026-10-21；exclusive BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。

嚴格 only-R／W7 原來源若有實際原邊 **u1w**，則兩個原 target fibres
`Z44459=Z44466=0`，與原五邊路的同源 witness 正性矛盾。
原 profiles **96、97、100、101** 全排，並得 `X48647=X67765=0`。
完整任意大小紙證見 [PROOF.md](PROOF.md)，每一 literal tuple／完整
actual component contacts 見 [OPERATIONS.md](OPERATIONS.md)。

證明使用新增原弦零值之前的同一份 **307,197 欄**完整 family。
五個拓撲規則依序證 `44722、45945、65628、45034、44466` 為零，
對應全部 incident 欄數 **2、3、7、18、10**。每欄各有同一原 D 的
一份既有空 fibre 見證；合計四十個完整 component 作用，沒有跨來源拼接。
A44459 本身即在原 u1w 上同色。

B 的 03／12 首步亦已獨立重建：唯一欄 306993 的兩個要交換的 contacts
為 `{q,w}` 與 `{c,s,v}`，得到 44107。這裡的 v 不能漏掉；主證明使用
完整分支策略，沒有把 A 的證明經 v／w 頂點交換搬過來。

[BASE.json](BASE.json) 凍結八份輸入，逐份 bytes 與本輪 Git BASE 相等。
[check.py](check.py) 核對 frozen bytes／SHA，掃描完整原 family，重生
四十一欄的全部 component flips（四十個主證明欄，另加 B03 首步），
並核對原四型的全部原弦。生成的 [certificate.json](certificate.json)
採 exclusive-create，預設 replay 為唯讀。

normal、seed17、seed17 加 `-O` 均通過；三次輸出完全相同，
八份內部破損證書全部遭拒絕，見 [checks.json](checks.json)。
另將十八欄規則漏掉一欄的完整外部污染證書送回 checker，非零退出並
拒絕，見 [negative-control.json](negative-control.json)。frozen input drift 為零。

u3w agent 已唯讀交叉審查本項的完整 incidence、拓撲、原邊零值及
literal 整分量作用，未見問題。本項亦使用另一份 pairwise constant-XOR
partition 實作，獨立唯讀核對 u3w 的四態、二十九欄證書及完整 literal
作用，結果 PASS，見 [review-u3w.json](review-u3w.json)。

本項量詞為原 SOURCE_CONTRACT 下任意大小、固定原 u1w 的四型來源排除。
所有原私有點、rotation、附件、完整空／非空 fibres 及全部原 cap lifts
保持同一來源。一般 W7 的其他型、未加弦的必要計數錐、一般 J1／J2、
smaller bad 與主命題仍 OPEN；沒有 LP、新實圖枚舉或新 Lean。
