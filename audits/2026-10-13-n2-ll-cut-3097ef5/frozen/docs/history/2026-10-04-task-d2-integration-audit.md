# 2026-10-04：D₂文件整合與A／B新增成果稽核

接手HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`，
工作目錄`/home/ray/developer/ai/math`。原工作樹已有A／B／C與mixed11
五輪未提交成果；本次不commit／push。

依[原D清單](../../audits/2026-10-04-task-d/REVISION_CHECKLIST.md)
套用全部18項適用修訂，逐項驗收見[D₂修訂表](../../audits/2026-10-04-task-d2/REVISION_RESULTS.md)。
H1固定来源前提、mixed11完成／其他incidence保留、四／五／六角色
投影與joint界線、合法搬運rotation與canonical重新選取的差異分開。
歷史正文、舊輪次、原checkers／artifacts及原D稽核包不覆寫。
HANDOFF仍是薄索引；A／B停止點歸[Kempe guide](../c5_kempe_guide.md)，
C停止點歸[weak-deletion guide](../c5_weak_deletion_guide.md)。
整合期間新增A₂／B₂／C₂亦納入：A₂原01／12全排後保存20／24，
B₂只排W933-101／W941-139短face、同骨架長face與其他20／20骨架
保留，C₂只關閉geometry30／side20窄支，下一入口轉geometry34。

新增A／B身份、完整relations／joint、空fibres與每份serialized witness
以獨立audit處理；來源域、原附件、owner、共享contact及一份共同色框
保留。新增覆蓋數字、實際命令／結果與限制見[D₂ REPORT](../../audits/2026-10-04-task-d2/REPORT.md)。
這是固定域稽核，不把任意大小紙面topology或外部Gallai依賴算作新Lean定理。
C／C₂本次只同步入口及重播，不算進A／B新增身份／joint稽核覆蓋。
新增A／A₂、B／B₂四層獨立audit全部PASS：150完整degree固定圖、
11,160完整joints、178,560字面fibres（141,624空）；逐份stored witnesses
各層為144,830／81,559／45,178／9,598。四份新producer各default／17
的八次byte-check都PASS。這些是固定controls coverage，不是来源catalogue。

## 歷史hash失敗與D₂漂移

原D的44次check、40 PASS／4文件hash FAIL保留為原截點結果。
D₂再以指定環境跑兩份舊證書的兩種hashseed，並重新深比較兩份全部
producer payload：只去掉直接input_sha256映射後相同，舊byte-check
仍不改寫成PASS。初次singles兩份NetworkX環境失敗另留attempt1 logs。

D₂對原D 22份證書及新增A／B／C、A₂／B₂／C₂共28份、192個直接hash紀錄核對，
仍是原4個文件hash漂移、零非文件漂移；相對原D截點與D₂起始沒有
新增直接input hash漂移。11份既有README／docs文件的本輪新bytes／SHA256另存
[integrity_results](../../audits/2026-10-04-task-d2/integrity_results.json)
與[integration_doc_changes.diff](../../audits/2026-10-04-task-d2/integration_doc_changes.diff)。
此範圍不宣稱全倉所有證書hash皆目前有效。
新A₂／B₂producer收尾版本變化獨立保存SHA256與source diff；前後全部
payload除直接input hash map外相同，最終audit對齊v2。初次版本
一致性失敗保留，與原歷史四份文件hash失敗分开。全部1,039份起始
protected文件bytes保持；manifest只新增作者A₂／B₂條目，舊條目不變。

## 重播與停止點

```bash
python3 audits/2026-10-04-task-d2/a/audit_a.py --repo . --output /tmp/task-d2-a
python3 audits/2026-10-04-task-d2/a2/audit_a2.py --repo . --output /tmp/task-d2-a2
python3 audits/2026-10-04-task-d2/b/audit_b.py --repo . --output /tmp/task-d2-b
python3 audits/2026-10-04-task-d2/b2/audit_b2.py --repo . --output /tmp/task-d2-b2
python3 audits/2026-10-04-task-d/identity/audit_identity.py --repo . --output /tmp/task-d2-identity
python3 audits/2026-10-04-task-d2/run_validation.py --repo . --output /tmp/task-d2-checks --scope integration
git diff --check
```

全倉文件、DocGraph、artifact status、diff檢查及C／C₂ seed17重播通過；
lake build完成8,831 jobs（既有lint warnings），未新增Lean theorem。
最後實跑命令及logs見[D₂ REPORT](../../audits/2026-10-04-task-d2/REPORT.md)。
保留ε≥3、mixed12／mixed22整型、來源實現、一般出口與`K∞=K≤5`未證。
接續研究直接讀各guide的既有窄入口；D₂到文件一致與獨立有限稽核為止。
