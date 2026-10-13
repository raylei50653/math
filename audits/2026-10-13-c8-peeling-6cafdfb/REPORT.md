# C8 反覆剝層的結構分類與染色轉移

2026-10-13。BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`。
權威入口為 [C8 剝層](../../docs/c5_c8_peeling.md)，接續
[原 m=9 報告](../2026-10-13-c8-followup-6cafdfb/REPORT.md)。
本輪交付任意大小的第一層三型與一般完整剝層定理，另完整排除 m=10 原來源。

## 前提、結論與證據層

固定原 globally vertex-minimal、then edge-maximal 目錄外 disk-C5 來源 G，
其同一有序 B、八項 h=3 原 collar、C8、H、I 及完整 933／941 色框。
C induced、H 三角化，d_H(C)≥4、d_H(I)≥5；原 C3／C4 cap 空，C5 cap
空或 W5。上游已證 I 點至多兩個 C 附件，雙接只能相鄰或正對，八個原面
第三點 t_i 全異。相鄰雙接唯一性使用另外明列的無 occupied C3 前提。

| 交付 | 精確量詞與狀態 | 權威證據 |
| --- | --- | --- |
| 原接點分類 | 任意有限 m；相鄰雙接恰為 t_i，正對點同一 pair、最多兩個。 | [structure/PROOF.md §§1–3](structure/PROOF.md#1-原前提與具名分類資料) |
| 內側外面分類 | RING／PINCH／BRIDGE 完備；simple cycle iff 無正對點；所有重複點及 bridge 具名。 | [結構證明 §§2–4](structure/PROOF.md#2-link-walkc-接點精確等於-q-外面點) |
| 完整染色轉移 | 同一 literal frame、完整 fibres／empties／full lifts，T1–T9 逐份雙射重建。 | [TRANSFER.md](TRANSFER.md) |
| 一般反覆剝層 | 任意有限內側大小；保存原三角面及 rotation，容許多 components、cuts、bridge、孤點。 | [TRANSFER.md §3](TRANSFER.md#3-任意大小的反覆剝層定理) |
| 同型 C8 遞迴 | 局部契約不足；七個具名障礙及原嵌入控制。固定寬度壓縮 OPEN。 | [結構證明 §6](structure/PROOF.md#6-任意大小剝層能保證甚麼以及不能照搬的具名障礙)、[獨立控制](independent/REVIEW.md) |
| m=10 完備分類 | 紙面只剩 CHORD-55／EDGE-35／EDGE-44，共 16 具名 H；有限計算不外推。 | [結構證明 §5](structure/PROOF.md#5-m10-的紙面完備分類)、[校準證明](calibration/PROOF.md) |
| m=10 原來源排除 | 16 H × 8 原 collar 全 Σ1023；接上游 m≤9 排除，h=3⇒k≥19。 | [complete certificate](calibration/certificate.json.gz)、[獨立覆核](independent/REVIEW.md) |

八個 h=3 任意大小來源仍 OPEN；沒有證得一般來源不存在或 K∞=K≤5。
一般 k≥16、h≥3、n5≥9 不變。本輪沒有新的外部定理或 Lean theorem。
小 cap 的既有目錄與外部定理依賴原樣沿用；不重播該論文的計算證明。

## 小型校準與完整 fibres

[校準 checker](calibration/check.py) 從紙面三型生成全部 16 具名位置，保存
原 vertices、所有 edges、定向 triangular faces 及固定 C/T 順序。它檢查
disk Euler、連通 vertex links、度數、附件與全部原 C3／C4／C5 cap 側。
八項 B–C collars 從 frozen 舊證書的 literal edges／faces 核對。

- C8 的 274 個共同 S4-orbit 代表，每 H 均保存全部 fibre：4,384 cells，
  1,500 個空 cells，7,408 份 full lifts。內 T 介面保留全部 6,564 literal
  proper 指派，包含 chord／中心造成的空 fibres。
- 接回 B 的 128 個具名圖，各保存同一十列：1,280 cells、75,936 full lifts，
  全部 Σ1023。每列直接整圖染色與逐層 full join 逐字一致。
- [獨立 checker](independent/check.py) 使用自己的搜尋次序，從 literal 圖邊
  重算全部保存 fibres；另構造具名 pinch／bridge 控制，核對一般層遞迴。

「target source not triggered」表示這些局部候選不是實際目錄外来源；排除
m=10 的依據是紙面完備分類加完整 Σ，不是零 target sightings。PINCH／BRIDGE
控制只證明幾何／轉移可触發，不賦予它們 933／941 全域最小來源身份。

## 重播、完整性與工作範圍

```bash
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --check
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --negative
```

[INPUTS.json](INPUTS.json) 凍結並雜湊本輪 authority inputs，包括未提交的原入口；
BASE 是 Git 基點，frozen SHA 才是實際讀取版本。舊證書未覆寫。
[MANIFEST.json](MANIFEST.json) 封存數學輸入、證明、程式與證書；logs／receipts
不在 immutable seal 內。checker 是 read-only，不重寫 RESULTS 或證書。
負控制實際通過同一 validator 拒絕缺失 lift、原邊、空 fibre 及接點一致性錯誤。
執行結果、文件檢查及 existing Lean build 見 [VERIFICATION.json](VERIFICATION.json)。

本輪不 commit／push。保留工作區全部既有變更，只新增本獨立包、剝層入口，
並依新 h=3 界更新直接 consumers 的當前路由；歷史 m=9 論證不覆寫。
README／HANDOFF 的主題清單沿用，HANDOFF 無新線或 tag 變動。
正式 docs 的 DocGraph 與全工作樹 DocGraph 分別記錄；全工作樹的歷史
duplicate-id 問題不由這個數學包處理。
