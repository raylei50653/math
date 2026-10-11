# 本輪驗證、保留代次與重播

BASE／HEAD 均為 `4dd11f422c6fa49265a412085116b088786d0344`。初始工具讀取時工作樹乾淨；INPUTS記錄的是建立本目錄後的status，故含本目錄的untracked列。另一同日定理audit的新增輸出属于同時進行工作，本輪不修改、不清除、不納入來源採納。

本輪540個凍結輸入：530份BASE docs、6份額外BASE報告／程式、4份未採納的外部audit文獻／receipt bytes。全部SHA256與凍結bytes一致；凍結時及本輪收尾核對live输入drift為0。所有BASE輸入另對Git objects核回；外部觀測bytes明標provisional authority。

主端獨立重播固定literal checker：

| 查核 | 結果／verdict |
| --- | --- |
| 正常 `--check` | exit0；5張固定圖，每圖240 proper字面列，3,648全部full lifts；target來源 **not triggered** |
| `PYTHONHASHSEED=17`，另使用`--seed 17`改回溯頂點順序 | exit0；完整graph／relation／empty fibres／full lifts記錄完全相同 |
| corrupted certificate 刪一個空root fibre | exit1，`recomputed complete graph/lift/claim record differs`；負控制 **triggered and holds** |
| M自身β-minimality | 3份M、57條非框邊逐刪完整β witnesses，**triggered and holds** |
| 任意縮環保持full lifts的命題 | 72個字面列有保留點投影失敗，**counterexample**；完整root-pair relation差異0也不能保full lifts |
| βminimal＋連通＋單缺額推出bic的命題 | 具名割點s的toy為 **counterexample**；其非disk／非N45前提明列 |
| 原spoke恢復字面filter | 兩份G=M+rb2全部240列complete lifts逐一相等，**triggered and holds**；G原Σ-critical前提 **not triggered** |

原圖、完整colorings、全部16根pins含空fibres、actual support／contacts／ownership／bridge／combinatorial rotation、counterexample witness及原刪邊著色均在 [observations-v3.json](literal_controls/observations-v3.json)。rotation沒有冒稱disk embedding。主端命令與raw stdout／stderr／exit保存於 [ROOT-VALIDATION.json](ROOT-VALIDATION.json)。

初版C割點metadata沒有比較刪點前後分量數，已retired；初版原證書和生成log完整保留。v2修正此點，v3加入字面恢復filter；三份證書各exclusive-create，沒有覆寫既有代次。v3是當前控制重播入口，舊證書仍可查但不作當前C-cut判斷。子交付的 [validation receipt](literal_controls/validation-receipt.json) 與 [payload hashes](literal_controls/payload-hashes.json) 一併保留。

Git tracked diff與 `git diff --check` 均為空／exit0；未更新共享docs、腳本、舊證書、commit、push或發布。主報告／子報告local links已核對。封存 [SEAL.json](SEAL.json) 列此目錄全部regular payload（包含frozen、retired generations及negative controls），只排除SEAL自己；重播不写檔。

在repo根目錄运行：

```sh
python3 -B audits/2026-10-11-single-deficit-applicability-804e3b0b1b/verify_audit.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-single-deficit-applicability-804e3b0b1b/verify_audit.py --check --seed17
python3 -B audits/2026-10-11-single-deficit-applicability-804e3b0b1b/literal_controls/check_literal_controls.py --check --certificate audits/2026-10-11-single-deficit-applicability-804e3b0b1b/literal_controls/bad-certificate-empty-fibre-dropped.json
```

前兩條預期PASS，最後一條預期FAIL exit1。本輪沒有重播舊R／N45大型枚舉或terminal certificates、DocGraph全庫或Lean build；它們不會裁定新conditional paper。本輪A保持conditional、actual target source新增0、完整OPEN身份無條件新增排除0。
