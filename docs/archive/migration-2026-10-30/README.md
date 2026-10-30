# 2026-10-30 文件重構與原始資料保存

本次把文件改為依工作查找，將目前採納結論集中於
[CONCLUSIONS](../../research/CONCLUSIONS.md)，接續工作由[研究契約](../../research/4ct_guide.md#精確消元主線的研究契約)維護。
完成的完整研究報告退出活躍工作區，保留原論證供按需查證；封存不表示命題失效或父題已完成。
舊停止點的更正及後續涵蓋見[封存導覽](../archive_guide.md)。

## 保存內容與身份

搬移基線為 `870eab2746e82a37d18d6a1b1af73ebf33dd8295`。
快照另包含當時工作樹尚未提交的文件內容；它是實際搬移前的 Markdown 保存，不冒充該 commit 的純 Git tree。
入口在本輪先作了功能導向調整，快照擷取後又依使用者採納補上活躍結論及短生命週期規則。

- [original-markdown.tar.gz](original-markdown.tar.gz)：819 份搬移前 Markdown 的原始 bytes 與 repo-relative 路徑，涵蓋 README、當時全部 docs、paper 及 artifacts Markdown。
- [paths.tsv](paths.tsv)：每份原檔的 SHA256、重構後位置與角色。STATUS 的原完整內容保存於封存目錄，根 STATUS 另作工作入口。
- [SHA256SUMS](SHA256SUMS)：上述快照與對照表的容器雜湊。
- [verify.py](verify.py)：只讀核對容器、清單及全部原始 member；不解壓、不重建研究產物。

450 份根層文件搬入功能目錄或封存，根層保留四個入口。完整研究報告正文未縮寫；
相對連結已重定位，四份 mixed P₃ 前序報告及舊 synthesis 另加後續提示，文件治理與活躍入口依新規則調整。
49 份 artifacts Markdown 僅修正連結，其原始 bytes 同樣在快照內。
既有研究程式、JSON／二進位證書、凍結 publication、匯入原稿及原始 audit blobs 不隨文件搬移改寫。

```bash
python3 docs/archive/migration-2026-10-30/verify.py
```

這份對照表記錄本次遷移，不是新的研究狀態總帳，也不要求每輪再製作全庫快照。
後續完整研究檔採同輪核對、整合結論後封存；原資料身份沿各報告及既有 audit 機制保存。

## 原路徑、雜湊與歷史重播

當前文件中的可點連結採新位置；舊報告的程式碼區塊、命令與來源清單保留當輪路徑。
部分歷史程式會把 `docs/舊檔.md` 的 bytes 納入輸出身份，或使用 `git show <commit>:<path>`。
本次沒有修改這些研究程式或重新接受一批新證書；搬移後不能假定它們在目前 checkout 直接執行仍有同一輸出。
當前求解工具的操作入口見[工具導覽](../../tools/four_color_guide.md)。

若要重建**此次搬移前的工作樹文件環境**，可從目前專案根目錄建立獨立 checkout：

```bash
snapshot="$PWD/docs/archive/migration-2026-10-30/original-markdown.tar.gz"
replay_dir="$(mktemp -d /tmp/math-docs-replay.XXXXXX)"
git worktree add --detach "$replay_dir" 870eab2746e82a37d18d6a1b1af73ebf33dd8295
tar -xzf "$snapshot" -C "$replay_dir"
```

這些指令只把保存的 Markdown 放回獨立 checkout，不執行研究搜尋或產物生成。
若需凍結稽核資料，再從該 checkout 依[原有還原說明](../../../audits/README.md)還原 artifacts。
用完可自行移除這個獨立 worktree；不在目前研究 checkout 解壓覆寫文件。

若原報告釘選的是更早 Git 基線，應使用**該報告指定的 commit 與 frozen 輸入**，
而非把本次 10/30 快照覆蓋到更早版本。此次快照只能還原搬移前文件，不修補既有來源漂移或歷史 FAIL。
完整關係、空 fibres、原 witness、失敗收據及原 hash 仍以各具名證據為準。

## 驗證界線

本次核對文件可達性、錨點、目錄覆蓋、活躍入口結構、stable IDs 與快照完整性；
另對 artifacts Markdown 的連結修改核對原始及修改後 bytes。
沒有因整理文件重跑研究枚舉、重新生成證書或執行 Lean build。
正式 docs 與全工作樹 DocGraph 分別記錄；歷史重複 ID 不因封存而刪除。
這些檢查不提升任何數學結論，也不宣稱全部歷史程式已在當前 checkout 重播。
