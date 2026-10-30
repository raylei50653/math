# R6-MARKED-SIX：目前進展整理與發布

2026-10-17；研究與提交父 BASE `6c420f3ca77d60952ed76f93dff7449c522715ca`。
使用者授權「整理目前進展 commit + push」。本次交付完整研究 audit、
三份直接導覽／索引更新及本發布紀錄。研究封存中的「沒有 commit 或 push」
保留當時交付語境；提交與遠端狀態以 Git 為準。

## 採納成果與仍開放的義務

同一原 no4ct 全域最少內點、次級最多邊的 C5 來源 G，原框
`(x,y,a,b,c)`、原 x,y,b 四度、r 六度，同一 U319、J、D及具名 e,f,g，
保留全部原扇區、接線、固定原支持、完整及空 fibres 與每個原接回。
權威入口是[整合報告](../../audits/2026-10-17-r6-marked-six-exclusion-6c420f3/REPORT.md)
與[完整紙證](../../audits/2026-10-17-r6-marked-six-exclusion-6c420f3/PROOF.md)。

| 項目 | 本輪結果 | 證據與界線 |
| --- | --- | --- |
| 完整 r6 同標記六圈／六割 | 所有同含 vw,pq 的簡單 J 圈長至少七；所有同含 e,f 的 cyclic D cut 至少七邊，無原 v5 前提 | 任意大小紙面來源定理；覆蓋全部配對、hub 與 disk 端點情形，未 Lean 化 |
| 舊 c4 殘支 | 改用原五圈 `(a,p,h,w,t)` 排除；新兩步引理再推至整個 r6 支 | 不沿用舊錯誤反射，也不更換原支持 |
| 十二點弱前提控制圖 | 38 個 PM、3 個聯合101；五個標記六圈中恰兩個為 cyclic 六割，因此違反新來源限制 | 完整固定圖證書；缺原來源接線，仍是 not triggered，並非來源反例 |
| 聯合交換 | 從110/101出發，e不可翻，f,g必同翻或同不翻；從111出發則恰翻一條 | 只保證聯合身份，沒有證出完整補圈奇數下降 |

**W110+W101>0、omega_e=0、完整319及任意大小奇數修復仍 OPEN。**
下一窄問題是保持非面七缺陷的五個原有序接點及完整外側，證實際下降，
或證修復受阻必迫同標記小 cyclic cut；後一連接尚未證明。
原 v/w 五度排除、一般 T/T0、r≥7 及 K∞=K≤5 不由此完成。
一般 K≤22、固定 r6 的 k≥25 與接回成本 k+5 均不變。
目前接續入口見 [Kempe 導覽](../archive/guides/c5_kempe_guide.md#3-停止點與保留缺口)。

## 保存身份與發布驗證

[初始盤點](2026-10-17-r6-marked-six-publication/initial-state.json)凍結81份 audit
檔案及三份研究交付時的routing快照。原83項 SHA256 清單、所有證明、證書、
正常與失敗紀錄均不改寫。檔案均低於大型 generated JSON 門檻，本次不新增archive。

STATUS另補本發布紀錄連結，故其live hash與研究交付時不同；這是已授權的
routing變動。發布後以[只讀custody checker](2026-10-17-r6-marked-six-publication/check_custody.py)
對83個seal項逐一核對，三份routing使用研究交付快照，其餘使用原audit bytes，
並重播root的22個BASE來源檢查。不能把預期的STATUS hash變動稱為證據損壞。

[發布檢查收據](2026-10-17-r6-marked-six-publication/checks.json)記錄實際命令、
exit code與log hash；研究時的三路獨立重建、交叉審核及所有負控制仍見
[原驗證紀錄](../../audits/2026-10-17-r6-marked-six-exclusion-6c420f3/VERIFICATION.md)。
本次root及A/B/C正常與seed17重播通過，C的七項污染及覆寫負控制重播亦通過。
`lake build`通過既有8832 jobs。系統Python首次工具測試因缺networkx失敗，
失敗log保留；使用`uv run --with-requirements requirements.txt`後94項測試全通過。
正式／有效範圍DocGraph與全樹結果分開記錄；全樹原有70個錯誤仍保留。
既有Lean build通過不表示本輪紙面定理已形式化；本次不重跑來源大型枚舉或九框計數。

從repository root只讀重播：

```sh
python3 -B docs/history/2026-10-17-r6-marked-six-publication/check_custody.py
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/A/check.py
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/B/check.py --check audits/2026-10-17-r6-marked-six-exclusion-6c420f3/B/certificate.json
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/C/check.py --check
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/C/run_checks.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
```

Updated：本發布紀錄、STATUS歷史索引；研究時三份導覽／索引更新一併交付。
Reviewed-unchanged：README、HANDOFF的研究線與tag，全部原封存證據及一般界。
Propagation stop：L2直接父入口，父題OPEN狀態未變。
