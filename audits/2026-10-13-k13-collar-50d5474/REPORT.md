# K13-COLLAR：十三內點完整外圈排除

2026-10-13。**證成 `K_{≤13}=K_{≤5}=K132`**，一般目錄外來源至少十四內點。
這是既有全域最小來源化約、新紙面結構排除、已發表完備生成定理與本輪完整有限證書的結合。
沒有剩餘十三內點 h=4–7 子域；一般 `K≤14=K≤5`、`K∞=K≤5` 仍 **OPEN**。
共同 h≥3、n₅≥9 不提高；沒有新增 Lean theorem。

固定 BASE：`50d5474f2446403f3b3001d5943571184c8c9936`。
隔離 worktree：`/home/ray/developer/ai/math-k13-collar-50d5474`。
[START.json](START.json) 保存原工作樹 HEAD 與 Cell 翻邊等未提交修改；
[INPUTS.json](INPUTS.json) 保存 BASE 正式輸入與目錄／程式 hashes，原 bytes 在 `frozen/`。
只本地研究、程式、文件與驗證，沒有 commit、push、PR、Issue 或留言。
正式入口為 [十三內點界](../../docs/c5_k13_collar.md)，研究停止點見
[Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)。

## 1. 全域來源與四分支

[PROOF.md](PROOF.md) §1–3 逐項核對指定正式來源的實際前提。
從全部目錄外來源先最小化 k，再最大化邊數；假設存在 k≤13，既有十二內點界迫 k=13。
沿同一全域來源得到簡單、二連通、原有序 chordless C₅、內面全三角化、
原框完整 degree≥4、原內點完整 degree≥5，完整 Σ 可共同 D₅ 搬到 933／941。
沒有固定 mask／固定 h 極小化，亦沒有 N2、ε、Gallai 或 edge-critical 前提。

從 Euler／握手式重新推得

```
|V(G)|=18, |E(G)|=46,
n₅=6+h+Σ_{原內點 d≥7}(d−6),
h≤7, |C|=5+h, |I|=8−h, |V(H)|=13, |E(H)|=31−h.
```

既有 h≤2 排除與 C₈ 的 h=3⇒k≥14，恰留下 h=4–7。
五個 apex 各有兩個原 B 附件，所有 y 各有一個附件；原 rotation 決定每條 y 鏈。
只使用 apex H-degree≥3、y H-degree≥4、I degree≥5。
全部可能的 C chords 均保留，未移植 C₈ 的更強結論。

## 2. 完整覆蓋表及排除結果

| h | C／I | 具名 e 數／D₅ orbit | 內側 cone 原始 roots | 通過兩項必要度數篩選 | 全部 apex 選位核心 | 主路徑 roots／弦數 | 完成方式 |
|---:|---|---:|---:|---:|---:|---|---|
| 4 | C₉／4 | 70／10 | 629 | 19 | 27 | 41：39 無弦、2 一弦 | 全部完整 Σ=1023∈K |
| 5 | C₁₀／3 | 126／16 | 214 | 1 | 1 | 4：全有兩弦 | 全部完整 Σ=1023∈K；無弦另由紙面排除 |
| 6 | C₁₁／2 | 210／26 | 41 | 0 | 0 | 0 | 全部分支紙面排除，完備分類吻合 |
| 7 | C₁₂／1 | 330／38 | 2 | 0 | 0 | 0 | 全部分支紙面排除，完備分類吻合 |

根點／核心數保留生成中的同構重複，不能相加作未標號圖數。
45 個主路徑 h4／h5 roots 與 28 個內側 apex 核心恰覆蓋同一組 **26 個帶根嵌入類**。
僅篩選 I degree≥5 的中間數是 24、24、12、2；表中 19、1、0、0 已再施加
「H-degree3 的 C 點必為 apex，至多五個」這一必要條件。

全部 **736** 份具名非負超額 e、每份到 D₅ 代表的映射、所有核心／整圖 frame 對應
及空配置保存在 [named_configurations.json](generation/named_configurations.json)。
h4 有55份、h5有10份配置在完整度數相容域中非空；其餘都是已完整分類的空域。
非空不代表目錄外來源：這些實際有限圖的 Σ 全在 K。

紙面 [PROOF §4](PROOF.md#4-可獨立紙面排除的最小內側域) 說明：
任一 C chord 的兩側都必含 I，否則多邊形 ear 迫 C-degree2。
h7 因此無弦，只能是單輪；h6 有弦時兩個葉區域各為輪，合計至少六個
C-degree3 點，超過五個 apices。另有無弦式 h≤2|I|−2 排 h5 無弦域。
這些純結構證明固定同一原 H，不作保關係改圖，也不作生成剪枝。

## 3. 完備性由哪些證明與獨立路徑承擔

主完備性證明是 [PROOF §5–6](PROOF.md#5-十九點最小度五球面三角化的覆蓋定理) 與
[生成完備性](generation/COMPLETENESS.md)：

1. 在 G 的**原指定外面**加 z 連到五個 B 點，得到十九點最小度五簡單球面三角剖分。
   完整生成全部球面嵌入、取每一個五度 root、保留全部十個原 B frames，覆蓋每份原 G。
   不按 mask、collar、cap 或 chord 刪掉任何主路徑 root。
2. 固定 BASE 的 plantri **5.8** 以 `-m5 19` 產生23份球面嵌入、306份根點刪除圖。
   外部數學完備性依據 Brinkmann–McKay 的 min5 構造定理，包含分離三／四環的類；
   沒有把 `-c5` 當來源前提。實際重播 C 程式，非僅引用表中23。
3. 以不同的 min4 生成遞迴完整處理十九點 **11,284,042** 份球面嵌入，只在輸出時
   篩完整 min degree≥5；所得23份與主路徑的完整嵌入 key 集合相同。
4. 直接內側路徑在 C 的指定外面加 cone，完整枚舉十四點 min4 的 **2,472** 份嵌入，
   取 degree9–12 cone roots、施加上述兩個必要條件、選全部五 apex 子集並補回原環帶。
   這獨立涵蓋全部 C₉–C₁₂、全部 chords／內邊／attachments／embedding。
5. 獨立程式重新枚舉所有 cone roots／apex 子集，以 NetworkX VF2 加**整份 rotation**
   同構核對主路徑，完整檢查736份配置，不只讀產生器自報的覆蓋數。
   見 [inner_coverage.json](independent/inner_coverage.json)。
6. 另以與 plantri 無關的全部帶標號邊集枚舉 n=4–7 的 3n−6 邊平面圖，
   共54,730個邊集，得到1、1、2、5個類，與生成器一致；見
   [small_exhaustive.json](independent/small_exhaustive.json)。此小域校準不替代全域生成定理。

min4／min5 分別從 octahedron／icosahedron 的已證構造出發；仍共享 plantri
資料結構／canonical machinery，不能稱兩套完全獨立的 C 實作。
生成定理、C 實作和編譯器是明列信任邊界，並未形式化驗證全部指令。
外部 PDF、版本、hashes 在 [external_inputs.json](generation/external_inputs.json)；
編譯器為 GCC 16.2.1，Python 3.14.7，NetworkX 3.5 只用於獨立小域／同構核對。
既有 K132／普遍 screen／4CT／K≤12 依賴保留；未重播 Dvořák–Lidický 的
外部計算證書，更未將其「少於30」擴到恰30。這裡的19點球面 cone 不是其30點對偶。

## 4. 完整 fibres、原圖結構與負控制

[check.py](check.py) 直接解析 planar_code，對每份圖保存：原邊、原 B／C、
原 rotation、有向面、原嚴格內點、完整 degree、所有附件及 canonical-to-original map。
`cores/sphere-00.json.gz` 至 `sphere-22.json.gz` 是完整23包資料，沒有截斷样本。
外面由 dart traversal 驗證；不只檢查抽象 planarity。H 的 labels 為主圖5–17；
`H_rotation`／`H_faces` 用0–12，透過加5還原，其他 C／I／H_edges 用主圖 labels。

每個原 B 固定十列，主 checker 以固定頂點順序完整回溯；
[independent/check.py](independent/check.py) 另以 domain propagation／MRV 重算全部 lifts。
[compare_main.py](independent/compare_main.py) 把所有 literal 染色搬回同一原圖逐份比較，
也核對3,060份整圖 D₅ frames、度數、外面、chords及附件。
28份另一途徑核心透過已獨立核對的完整頂點同構，逐點拉回對應主圖全部lifts；
不另更名一個piece，無需重複存同構的染色資料。

結果：**306份根图、3,060列全接受、41,021份完整 lifts，全部 mask=1023**。
主域沒有拒絕列，不虛構空 fibres；[calibration.json](calibration.json) 的 C₅ chord
及五輪控制實際包含8份拒絕列，保存空列表並完整重算；
[calibration_review.json](independent/calibration_review.json)另核對300次整圖D₅逐lift比較。
按固定邊界列枚舉的唯一搜尋前綴證明既無漏 lift，也無重複；不用局部非空關係接合。
所有目錄外最小來源是 `not triggered`，有限核心符合自己的結構條件並已完整計算。
零 target 不被獨立當成定理；矛盾來自上述全覆蓋加 Σ∈K。

[compare_main.json](independent/compare_main.json) 及 [review.json](independent/review.json)
保存至少以下負控制，均 `triggered and holds`（破損資料被拒）：
漏 C chord、錯指定外面、錯原 B 標號、degree 誤算、漏一份接受 lift、錯完整 mask。
另拒絕漏一個 degree5 root。控制使用損壞的記憶體副本，不覆寫正常證書。

## 5. 實際重播與工作邊界

全部命令及退出碼由 [VERIFICATION.json](VERIFICATION.json) 與 `logs/` 保存。
normal／seed17 的十二份生成數學產物逐 byte 相同；主 checker、獨立全部 lifts、
結構、主證書比較與內側覆蓋皆一致。生成重播需新目錄，拒絕覆寫歷史產物：

```bash
python3 -B audits/2026-10-13-k13-collar-50d5474/generation/replay.py --output /tmp/k13-generation-new --seed 0
python3 -B audits/2026-10-13-k13-collar-50d5474/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k13-collar-50d5474/check.py --check
python3 -B audits/2026-10-13-k13-collar-50d5474/independent/check.py --check
python3 -B audits/2026-10-13-k13-collar-50d5474/independent/review.py --check
python3 -B audits/2026-10-13-k13-collar-50d5474/independent/compare_main.py --check
uv run --with networkx==3.5 python -B audits/2026-10-13-k13-collar-50d5474/independent/inner_coverage.py --check
```

大型原始 JSON、保有原始 whitespace 的 frozen vendor與原始log沿用 `tools/audit_archive.py append --paths`，保留原 bytes 並按 hash
去重 gzip；新 checkout 先依 [還原規則](../README.md) 還原。舊 ARCHIVE records、
舊證書／manifest／frozen bytes 均保持。新封存驗證及儲存檢查另記實際結果。
第一次主 checker 對 successor dart 方向預期錯誤，尚未寫核心即停止；修正為
原 rotation 的**全域反向外面**，原失敗 [main-write.log](logs/main-write.log) 保留。
生成 plug-in 編譯引號與獨立 comparator 的 y 分組介面初次失敗亦保留，不隱藏歷史。
初次文件檢查有22項未還原封存連結；按BASE封存hash還原後通過全部8,172連結。
還原 helper 首次誤用kind名稱 `file` 而非既有 `regular`，停止且保留log；修正後完成。

`lake build` 在獨立複製的 `.lake` 中成功（8,831 jobs），只作既有 Lean 回歸。
正式 docs DocGraph、全域 DocGraph、文件連結、相關工具 tests、儲存規則和
`git diff --check` 分開報告；工具56 tests與DocGraph18 tests皆通過。
全域既有62項 duplicate-ID 不修復、不宣稱通過。
未執行：新 Lean 形式化、外部 Dvořák–Lidický 計算證書重播、其他研究線大枚舉、
commit／push／遠端發布。沒有因本輪成功提高 h 或採納十四內點等式。

## 6. 採納與精確殘留

四項驗收均完成：全域最小來源正確；h4–7窮盡；各分支紙面或有限分類完備；
所有正式核心的原 embedding／完整關係有獨立核對。故 `K≤13=K≤5` 可採納，
**十三內點來源殘留為空**。一般十四內點以上、h3 的八份任意大小必要上界、
一般縮減／跨邊同步、K∞以及新 Lean 形式化都仍未解，沒有把它們併入結論。

Closure scope / Canonical Source + Evidence：十三內點全部 disk-C₅ 關係，正式入口及本包證據。
Updated：cofacial／degree／collar／C8 四份直接來源加後續導向；Kempe 導覽及 STATUS 更新目前界。
Reviewed-unchanged：State／common-language／synthesis 不以十三內點為當前未解界；
HANDOFF／README 的研究線與入口角色不變，其他歷史快照保留。
Propagation stop：父命題 K∞仍OPEN，沒有進一步改動無關分支或全域 DocGraph 歷史。

驗證期間原共享checkout已由其他session前進至 `5211a92178dffd9d7cd3f883a19d8a3f03932d07`；本輪worktree仍固定BASE，沒有把新結果當前提。

[SEAL.json](SEAL.json)保存本包與相關正式文件的最終hash；以 `python3 -B audits/2026-10-13-k13-collar-50d5474/verify_bundle.py --check` 只讀核對。
