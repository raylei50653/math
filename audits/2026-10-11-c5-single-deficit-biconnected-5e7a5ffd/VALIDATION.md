# 本 audit 的實際驗證

BASE：`4dd11f422c6fa49265a412085116b088786d0344`。
主 audit 已獨立讀取两份 checker，核對生成資料與所聲稱的控制範圍，再以現有唯讀
`.venv/bin/python -B` 重播。Python `3.14.7`，NetworkX `3.5`；沒有安裝依賴或寫入環境 cache。

| 實際檢查 | exit code | 控制狀態 | 保存紀錄 |
| --- | ---: | --- | --- |
| 六個前提控制正常逐 byte 重播 | 0 | triggered and holds | [premise-normal.json](validation/premise-normal.json) |
| 前提控制 PYTHONHASHSEED=17 逐 byte 重播 | 0 | triggered and holds | [premise-seed17.json](validation/premise-seed17.json) |
| 損壞 interior-degree 證書被 --check 拒絕 | 1，預期 1 | triggered and holds | [premise-corrupt-rejected.json](validation/premise-corrupt-rejected.json) |
| 758 minor controls 正常順序 seed=0 | 0 | triggered and holds | [minor-normal.json](validation/minor-normal.json) |
| 758 minor controls seed=17，PYTHONHASHSEED=17 | 0 | triggered and holds | [minor-seed17.json](validation/minor-seed17.json) |

前提控制的六個 named inputs 共 960 個完整 `4^|H|` interior assignments，
包括全部成功／失敗 assignments、每個失敗的衝突邊、原列表、完整 attachments／degrees、
rotation、全部 faces 與原 C5 外面。第二個 list-restricted 搜索使用 seed 17 的不同變數次序，counts 一致。
三個撤前提反例、附件中間推論反例及 G／M bookkeeping 按各自的 claim 記錄；
原定理只有基準 triangle 控制觸發，其他五個均 not triggered。

minor 證書是 27 個左 seed stretches、729 個中 seed stretches，加 spindle 與 complete K4。
重播核對每組連通樹、互斥 bags、六個 K4／十個 K5 original-edge witnesses、原 H／B 分割、
完整 degrees 與 H 二連通。證書 byte hash 與 manifest 相符。
三個 in-memory 損壞控制（非原邊 witness、重疊 bags、degree metadata 改寫）均被拒絕。
這批 minor claim 是 triggered and holds；每個合成 M 已含 K5，原 disk theorem domain 都 not triggered。
沒有對這些 nonplanar 合成圖主張 β 拒絕或 disk 實現。

可從工作目錄 `/home/ray/developer/ai/math` 重播：

```bash
.venv/bin/python -B audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/premise_controls/replay.py --check
PYTHONHASHSEED=17 .venv/bin/python -B audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/premise_controls/replay.py --check
.venv/bin/python -B audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/existing_results_overlap/minor_controls.py --check --seed 0
PYTHONHASHSEED=17 .venv/bin/python -B audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/existing_results_overlap/minor_controls.py --check --seed 17
```

損壞證書負控制命令如下，**預期失敗 exit 1**，不可當成原證書失敗：

```bash
.venv/bin/python -B audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/premise_controls/replay.py --check --output audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/premise_controls/corrupted-degree-certificate-v1.json
```

两份 checker 的生成模式均 exclusive create，既有 certificate 不覆寫。
前提子工作較早自身生成的 `certificates.json` 保留為 pre-final snapshot；
最終重播對象為 `certificates-final-v1.json`，其 SHA-256 為
`ff27e4f930e9fd137c0d5c891603751cb5be6e46b2a07a5cd1177e90a719144a`。
minor certificate 的 SHA-256 為
`6d2286f6f83c753163aba22add705e09c1cb1e3a9b3b72551d4b6f48209e5c69`。

正式 PDF 的 2、3、4、11、12 頁已由主 audit 與獨立子工作視讀。
Figure 1 另作 450 dpi 與 SVG stroke 核對；沒有僅依賴 PDF 文字抽取。
獨立文獻子工作最後再核對主 REPORT：定理、全部 minor bags、完整 degrees、
前提表及 960／758 控制數均相符。其唯一來源措辭修正已套用：
把 `≥3` 顯成 `>3` 的是網頁工具抽取，本地保存的 pdftotext 本來正確。
初次嘗試 PyMuPDF renderer 因未安裝 fitz 而未產生圖檔，改用現有 pdftoppm／pdftocairo，
沒有為此安裝套件，且不影響正式 PDF bytes。

`initial-receipt.json` 的 tracked inputs 在目錄建立後即保存；
其中 `initial_git_status` 是建立四份凍結文件後的狀態，故已列本 audit 為 untracked。
建立目錄**前**第一次 Git 檢查為空，且 HEAD 精確等於 BASE；兩個時點沒有混為一談。
最終對全部起始 tracked bytes、十一份 BASE documents 與 PDF 的核對記錄在
[seal.json](seal.json)。同時記錄其他工作新增的 outside untracked 目錄，
不把權威 bytes 零漂移說成整個工作樹未變；沒有讀取或修改該其他目錄。

產物與權威 bytes 可唯讀再核對：

```bash
python3 -B audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/verify_seal.py --check
```

未重跑 DocGraph、lake build、舊證書或來源枚舉；本次沒有 Lean 證明修改。
紙面任意大小論證與以上有限重播的信任邊界見 [REPORT.md](REPORT.md)。
