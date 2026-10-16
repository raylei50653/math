# R6-DOUBLE-W5-101 發布紀錄

2026-10-16。使用者明確授權 `commit + push`。
研究及提交父 BASE：`0b639cf5ffd57e8e394add4e0b56cd60cc2ce38c`。
本次僅提交 [雙 W5 audit](../../audits/2026-10-16-r6-double-w5-101-0b639cf/REPORT.md)、
四份相關文件入口及本發布紀錄。提交 SHA 可由本檔的 `git log -1` 查得；
遠端發布狀態以 HEAD、origin/main 與 remote main 的即時比對為準。

## 採納與保留界線

在完整原 no4ct 全域最小、次級最大邊數 C5 來源，原 x,y,b 四度、r 六度，
及具名 `J=U/(s=t)`、D、e,f,g 契約下，任意大小排除 101 雙完整 W5
最大 Tutte 障礙。獨立審查重建前輪五割證明及本輪完整第二鄰域矛盾。

101 普通匹配失敗僅剩非輪七割；110、偶補正值、完整319、一般無界主命題
仍 OPEN。既有一般 K≤22、固定 r6 的 k≥25 與來源接回成本 k+5 不變。
紙面證明、有限校準及 Lean 工程驗證分開，未新增 Lean theorem。

## 封存與提交前驗證

本 audit 共 98 檔、1,117,554 bytes，含 MANIFEST 及其 97 個封存成員。
本次獨立核對全部 SHA256、檔案名單及舊三輪 424 檔，均無漂移。
沒有 cache、symlink 或超過 1 MB 的單檔，無需新增大型產物例外。
原 REPORT／VERIFICATION 的「未 commit、未 push」保留研究交付時語境。

提交前重新執行原 bundle、sector matching fibre、radius-two 校準及 seed-17
入口，正式文件與 scoped DocGraph 亦通過。完整 normal／seed-17、負控制、
既有依賴與 Lean build 收據保留在原 audit；Lean 內容未變，本發布未重跑 build。
全樹 DocGraph 的70個歷史重複ID維持原記錄，不改寫 frozen 證據取得 PASS。
staged artifact policy 與 whitespace 檢查在提交前執行。

## 提交後重播

原 `check_bundle.py` 明確鎖定研究 HEAD=BASE 及未加入 index 時的 routing diff。
提交後直接執行會被其歷史 HEAD guard 拒絕；不修改封存 checker 或 MANIFEST。
兩個數學校準 checker 仍可按原命令直接重播。發布版本的封存／來源核對可用：

```sh
python3 -B - <<'PY'
import hashlib, json, pathlib, subprocess
root = pathlib.Path.cwd()
audit = root / 'audits/2026-10-16-r6-double-w5-101-0b639cf'
base = json.loads((audit / 'BASE.json').read_text())
manifest = json.loads((audit / 'MANIFEST.json').read_text())
subprocess.run(['git', 'merge-base', '--is-ancestor', base['base'], 'HEAD'], check=True)
expected = {r['path'] for r in manifest['files']} | {'MANIFEST.json'}
actual = {str(p.relative_to(audit)) for p in audit.rglob('*')
          if p.is_file() and '__pycache__' not in p.parts}
assert actual == expected, 'audit membership drift'
rows = [(audit / r['path'], r['sha256']) for r in manifest['files']]
rows += [(root / r['path'], r['sha256']) for r in base['prior_audits']]
for path, expected_sha in rows:
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_sha, str(path)
print('PASS: 97 sealed members and 424 prior audit files; BASE ancestry retained')
PY
```

未重跑外部枚舉或擴大來源圖類。README／HANDOFF 的研究線與操作入口不變；
文件傳播止於 Kempe 導覽、STATUS、C4 直接父題與 State 活躍入口。
