# W7單障礙、完整原E與L混色路整理發布

2026-10-21；發布前 Git BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
依使用者「commit + push」要求，連貫發布四包未提交證據：
[多分支與特殊規則](../../audits/2026-10-21-w7-exploration-30dde27/REPORT.md)、
[單障礙原幾何](../../audits/2026-10-21-w7-single-barrier-30dde27/REPORT.md)、
[同一E完整混色作用](../../audits/2026-10-21-w7-k1-mixed-30dde27/REPORT.md)、
[L三邊短型與至少五邊長路](../../audits/2026-10-21-w7-L-path-30dde27/REPORT.md)。
來源量詞、原rotation／完整stars、同一E、字面框、空fibres與全部cap lifts不變。

profile0的K=1先排n／u4／u2，再排u3／u1，只餘L。L完整01分量contacts
僅四個必要型；三邊路的普通六度／雙五度在01／02／03仍各留4／4／2及
4／4／3必要型，不能拼成共同原來源。本輪只再排雙五度II／target44466／
U=原w子支：原02路w–K–z4與父兩個完整02欄的分離直接矛盾。

恰五邊最短01路的原z5接線只剩七型：三型迫z5七度加原K五度，一型迫
z5八度，另三型保留任意內點數的induced C6／C7。任意奇長ell若全為
gap1／3、其中r個gap3，精確d_G(z5)=ell+3−r；gap≥4的多內點cell未解。
新cell位於原E內，舊R在其外，不能套用only-R前提。L四型、兩短整型、
profile1、K≥2、一般W7／J1／J2、來源實現及合法較小bad均仍OPEN。
原40 profiles仍排38型、餘0／1，沒有新Lean或完整計數錐結論。

317份原證據共138,163,658 bytes，包含失敗初證、後續版本與全部負控制，
逐份SHA見[發布前清單](../../audits/2026-10-21-w7-L-publish-30dde27/evidence-before.json)。
三份大型JSON保存21,816,344原bytes，追加三個gzip blobs共720,740 bytes；
舊6,145個file records及3,120個blob records逐項不變，其餘檔案直接Git保存。
原報告與receipt的「未commit／push」保留當時語境，本紀錄另記這次發布。

一個本機mixed整合重播因多出ignored bytecode而不匹配舊artifact清單；
原46份artifact都未漂移。在無bytecode、原routing的臨時overlay已通過。
另有single舊receipt列到衍生bytecode，保留該歷史receipt但不發布快取。
完整成功／失敗與新驗證分開記入[發布報告](../../audits/2026-10-21-w7-L-publish-30dde27/REPORT.md)。

現行STATUS／guide的授權更新不回寫原checker或BASE。先還原封存，再用
publication verifier核原證據與舊routing；current docs由文件checker獨立核對：

```sh
python3 tools/audit_archive.py restore --artifacts
python3 -B audits/2026-10-21-w7-L-publish-30dde27/verify.py
python3 -B audits/2026-10-21-w7-L-publish-30dde27/verify.py --replay root --replay mixed --log-dir /tmp/w7-L-published-replay
```

Closure scope：profile0的K=1五個位置，以及L型II／B／U=w具名子支；不提升
成整個profile或L排除。Canonical Source：上述四包原報告及完整原證書。
Updated：Kempe導覽、STATUS直接索引、README最新發布入口、封存入口及本紀錄。
Reviewed-unchanged：HANDOFF活躍研究線、原frozen證據、State導覽、一般J1／J2。
Remaining OPEN：L四型共同來源、兩短型／pinched aliases、長路多內點cell、
profile1與K≥2、完整計數錐、較小bad及主命題。
Propagation stop：L2；父W7仍OPEN，未觸發更高層結論變動。
目前接續入口由[Kempe導覽](../archive/guides/c5_kempe_guide.md)維護；即時發布狀態以Git為準。
