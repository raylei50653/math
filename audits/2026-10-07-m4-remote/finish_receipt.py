#!/usr/bin/env python3
"""Compile the completed M4-R delivery from preserved observations."""
import datetime
import hashlib
import json
from pathlib import Path

folder = Path(__file__).resolve().parent
FINAL = "1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf"
BASE = "2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090"
def saved(label):
    return json.loads((folder / "commands" / label / "stdout.log").read_bytes())

runs = []
for label, run_id, event in (("push-job-final",37592725527,"push"), ("pr-job-final",37592797376,"pull_request"), ("docs-job-final",37592841563,"workflow_dispatch")):
    run = saved(label)
    assert run["headSha"] == FINAL and run["status"] == "completed", (label,run)
    logs = json.loads((folder / "ci" / str(run_id) / "log-evidence.json").read_bytes())
    assert run["databaseId"] == run_id == logs["run_id"] and run["event"] == event
    assert len(logs["checkout_shas"]) == 1
    checkout = logs["checkout_shas"][0]
    if run["event"] != "pull_request":
        assert checkout == FINAL
    runs.append({**run,"actual_checkout_sha":checkout,"log_evidence":f"ci/{run_id}/log-evidence.json",
                 "original_logs_zip":f"ci/{run_id}/original-logs.zip"})
pr = saved("pr-final")
policy = saved("review-policy-final")["data"]["repository"]
rules = saved("rules-main-final")
assert pr["headRefOid"] == FINAL and pr["baseRefOid"] == BASE
assert policy["pullRequest"]["headRefOid"] == FINAL and policy["ref"]["target"]["oid"] == BASE
assert pr["autoMergeRequest"] is None and pr["state"] == "OPEN"
refs = (folder/"commands/final-local-refs/stdout.log").read_text().splitlines()
remote_lines = (folder/"commands/remote-final/stdout.log").read_text().splitlines()
remote = {line.split()[1]:line.split()[0] for line in remote_lines}
assert refs == [FINAL,FINAL,BASE]
assert remote["refs/heads/integrate-kprime-e3"] == FINAL and remote["refs/heads/main"] == BASE
threads = policy["pullRequest"]["reviewThreads"]
assert not threads["pageInfo"]["hasNextPage"]
unresolved = [row for row in threads["nodes"] if not row["isResolved"]]
integrity = json.loads((folder/"final-integrity.json").read_bytes())
assert integrity["status"] == "PASS"
status = (folder/"commands/final-status/stdout.log").read_text()
required = {"branch_protection_rule":policy["ref"]["branchProtectionRule"],"effective_rules":rules}
failed_ci = [f'{run["event"]} {run["databaseId"]}: {run["conclusion"]}' for run in runs if run["conclusion"] != "success"]
result = {"task":"M4-R","recorded_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "status":"Published; CI outcomes preserved; awaiting supervisor acceptance",
          "pr":pr,"review_threads_total":threads["totalCount"],"unresolved_threads":unresolved,
          "reviews":policy["pullRequest"]["reviews"],"required_checks_policy":required,
          "refs":{"local":refs[0],"tracking":refs[1],"remote_branch":remote["refs/heads/integrate-kprime-e3"],
                  "remote_main":remote["refs/heads/main"],"baseline_main":BASE,"main_advanced":False,"main_diff":"none"},
          "ci_runs":runs,"docs_failure_classification":"Archive targets retained but not restored by docs.yml before link validation",
          "delivery_manifest":"audits/2026-10-07-m4-local/DELIVERY.json",
          "accepted_final_receipt":"audits/2026-10-07-m4-supervisor/acceptance/final-receipt/FINAL_RECEIPT.json",
          "source_and_seal_integrity":integrity,"worktree_status":status,
          "new_commit":False,"force_push":False,"rebase":False,"merge":False,"auto_merge_enabled":False,
          "local_lean_build_rerun":False,"lean_axiom_process_rerun":False,"explicit_lc_evidence":"Same-hash M3 local explicit build",
          "failed_or_non_success_ci":failed_ci,
          "remaining":failed_ci+["Documentation workflow FAIL (two archived targets absent from plain checkout)",
                       "Supervisor acceptance pending; review state captured separately",
                       "Five strict provenance FAILs and historical evidence gaps preserved",
                       "U2-U4, E5 new proof, three-row generalization, epsilon>=3 and general theorem gaps preserved"]}
(folder/"FINAL_RECEIPT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
rows = []
for run in runs:
    jobs = "; ".join(job["name"]+"="+job["conclusion"] for job in run["jobs"])
    rows.append(f'| [{run["databaseId"]}]({run["url"]}) | {run["event"]} | `{run["headSha"]}` | `{run["actual_checkout_sha"]}` | {run["conclusion"]}; {jobs} |')
report = f'''# M4-R 遠端交付與 CI 回報

固定 final SHA 已正常 fast-forward push，並建立 [PR #3]({pr['url']})。
Lean push／PR 結果見下表；文件 dispatch **FAIL**，因此本回報不是全 CI PASS，也不是可合併宣告。
停止於待監督驗收；未 merge、未啟用 auto-merge、未 force push、未新增 commit、未 rebase／merge main。

| Git／PR 欄位 | 實際值 |
| --- | --- |
| Local HEAD | `{FINAL}` |
| Tracking origin/integrate-kprime-e3 | `{FINAL}` |
| Remote integrate-kprime-e3 | `{FINAL}` |
| PR head／branch | `{pr['headRefOid']}`／{pr['headRefName']} |
| PR base／branch | `{pr['baseRefOid']}`／{pr['baseRefName']} |
| 即時 remote main／本地驗收基準 | `{BASE}`；未前進，差異 0 |
| State／draft | {pr['state']}／{pr['isDraft']} |
| Mergeability／check state | {pr['mergeable']}／{pr['mergeStateStatus']} |
| Review | reviewDecision={pr['reviewDecision'] or 'none'}；reviews={policy['pullRequest']['reviews']['totalCount']} |
| 待解 threads | {len(unresolved)}；完整分页已核對 |
| Required checks | branchProtectionRule={policy['ref']['branchProtectionRule']}；effective branch rules={rules} |
| Auto-merge | null；未啟用 |

整分支相對 main：1,618 檔、+1,985,529／−70；PR 說明沿用監督 PR_BODY 並補全 K′、E3–E6、ES／ER／LC、D8／D9、C44 系列與 U1 範圍。
發布前遠端 branch 為 `1d026ee949d07a5b20bd60ec2f1e6d4329341cdf`，已核對是 final ancestor；本次正常前進 14 commits，沒有覆寫遠端新工作。

| Run URL | Event | API head SHA／關聯 PR head | 實際 checkout SHA（原 log 證據） | Run／各 job 結論 |
| --- | --- | --- | --- | --- |
{chr(10).join(rows)}

PR run 的 checkout 是 GitHub synthetic merge ref；其 SHA 與 PR head 分列，未混稱相同。
`ci/<run-id>/original-logs.zip` 保留 API 取得的原 ZIP bytes；`log-evidence.json` 保存逐檔 hashes、checkout command／SHA 行號與 build／failure 行。
`commands/*-job-final/stdout.log` 保存各 job／step 結論；`commands/*-run-original/stdout.log` 保存原 run metadata。
Lean workflow 執行 `lake exe cache get` 與 `lake build --no-ansi`，defaultTargets=Math。
顯式 LC build／558 公理仍沿用同 hash M3 原證據，沒有宣稱由預設 CI 重跑；本輪 Python reparse 與原 JSON 全等，不是 Lean 公理程序重跑。

文件 workflow `docs.yml` 僅 workflow_dispatch，本次實際 checkout 正是 final SHA，check job 在 Check local documentation exit1：

- `docs/c5_open_leaf_ledger.md:78` 指向缺少的 `audits/2026-10-04-task-d5/c4/scope_ledger.json`。
- `docs/history/2026-10-04-task-d2-integration-audit.md:39` 指向缺少的 `audits/2026-10-04-task-d2/integration_doc_changes.diff`。

兩份 ordinary paths 不在 Git tree，已提交的 `audits/ARCHIVE.json` catalog 指向已提交 gzip blobs；原／解壓／工作區／獨立還原副本 hashes 均核對相符。
workflow 只 checkout 後執行 `scripts/check_docs.py`，沒有 archive restore；因此分類為文件 workflow 未 materialize 已保存 archive，不是這兩份證據丟失。
本輪不修改候選／workflow，也不更新舊證書消除 FAIL。詳見 [失敗分類](docs-diagnosis/diagnosis.json)及原 ZIP。
同 final SHA 的本地文件／anchors/index PASS 與預設 DocGraph PASS 證據，位於既有
`audits/2026-10-07-m4-supervisor/acceptance/final-receipt/`、`audits/2026-10-07-m4-supervisor/acceptance/review.json`，
由先 restore archive、再 check 的 scratch-free checkout 取得；本地 PASS 不提升為本次文件 CI PASS。
原工作區 scratch 保留，其預設 DocGraph 62 duplicate-id FAIL 與 scratch-free PASS 的差別仍明列。

正式 manifest：`audits/2026-10-07-m4-local/DELIVERY.json`；572 entries＋seal＝573 檔，共 26,469,605 bytes。
既有驗收 final receipt：`audits/2026-10-07-m4-supervisor/acceptance/final-receipt/FINAL_RECEIPT.json`。
本輪前後核對 source／seal 無漂移，seal 118,904 bytes、SHA256 `0ee59a603a366808cc8fdfb52b32586403028fd72395a80785991584408d49fa`。
原三包 328 檔及其 manifests、109 份 Lean source/config/generated products 均無漂移；全 M3 snapshot 的 7,185 file hashes＋5 symlink targets 符合已驗收 final source snapshot。
歷史 M3→final 僅 STATUS／Kempe guide 兩份已授權文件 bytes 變更；三份既有工作區 mode 差異 bytes 相同，均在 source-integrity.json 明列。
數學來源、原 metadata／logs／certificates 未修改。新 source comparison、57 原 M3 commands／114 logs、558 公理 reparse 與 fresh seal checks 見 [integrity/source-integrity.json](integrity/source-integrity.json)及 [final-integrity.json](final-integrity.json)。

五项 strict FAIL 保留：C44 input／E4 reductions／E5 controls／E4C／E5 branches；原 29 命令仍 28 PASS／1 FAIL，另四項 strict FAIL。
Whitespace 原 86＋匯入 immutable log 85＝171；新 authored 0，整分支 diff --check exit2 仍保留。
完整原 M1 51 檔包與部分歷史 logs／tmp 證據仍不可用；追回 M1 REPORT／TSV 與 fresh Git reconstruction 不冒充缺失原執行 logs。
U2–U4、E5 新證明、三列推廣、ε≥3 及一般研究缺口保持原停止點，未新開證明輪次。

Tracked／staging 最終乾淨；原 scratch 與旁掛 supervisor 保留，新增本 M4-R 旁掛證據不提交。
最終 `git status --porcelain=v1`：

```text
{status.rstrip()}
```

操作命令、時間、exit 與原 stdout/stderr hashes 集中於 [commands.json](commands.json)，每次原輸出在 `commands/<label>/`。
網路初次 sandbox DNS 失敗，已授權的網路操作 retry 成功；未變更 remote 設定。
未成功 CI 結論：{'; '.join(failed_ci) or 'none'}。其餘未完成項為監督驗收；review 即時狀態見表，保留五項 strict FAIL、歷史缺失與上述研究界線。
Required checks 未設定不代表 CI 通過；技術 mergeability 與使用者實際 merge 授權分開。後續任何 merge 仍需使用者另行明確指示。
'''
(folder/"REPORT.md").write_text(report)
commands = [json.loads(p.read_bytes()) for p in sorted((folder/"commands").glob("*/command.json"))]
(folder/"commands.json").write_text(json.dumps(commands,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"receipt":str(folder/"FINAL_RECEIPT.json"),"report":str(folder/"REPORT.md"),"runs":len(runs),"commands":len(commands)},ensure_ascii=False))
