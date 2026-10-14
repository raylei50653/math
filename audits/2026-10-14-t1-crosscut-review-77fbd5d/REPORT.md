# T1 一般正對切口：來源覆蓋與完整證書採納審查

2026-10-14。凍結 BASE：`77fbd5da7ba273f0af7c75175dc08376d2282f46`。

**審查結論：PASS，可在原 no4ct 全域最小來源契約下採納**

\[
\boxed{h=3\Longrightarrow p=0.}
\]

來源覆蓋、literal 完整接合、共同支援直積及有限矩形排除均已核對。
這關閉該契約下的全部 PINCH／BRIDGE，不限制單接點數或兩片內點數。
第一剝層只剩 RING；**RING、h≥4、一般 `K∞=K≤5` 仍 OPEN**。
既有一般 k≥16 與 h=3⇒k≥19 不因本次審查提高。

本次交付是獨立 worktree 內的完整採納審查；未更新 main 的研究入口，
未 commit／push。證據是 agent 輔助的紙面審查、Python 完整有限證書及
另一份重建，沒有新增 Lean theorem，也不稱為第三方人類數學審查。
機器驗收摘要見 [VERIFICATION.json](VERIFICATION.json)。

## 1. 來源與精確適用契約

在所有有限簡單 C5 disk 的目錄外來源中，先全域最小化原內點數 k，
再最大化邊數；不改為固定 933／941 分別最小化。原完整 B 關係在一次
共同 D5 對齊後屬於 932／933／941。沿用 BASE 已採納的 no4ct C8
依賴：h=3 時 932 已排除，只剩原八份具名 collar／target，原 C8 是
實際 induced 內圈，p 是其嚴格內點中正對雙接點的數量。

本次使用八份原完整 target，沒有把必要支援 U 的大小當作 target。
原八份契約含六個不同幾何 annuli；c15、c18 分別對兩個 target 核對，
因此 8×4=32 個必要單切口查詢的計数保持不變。

- [輸入與 SHA256](INPUTS.json) 保存 14 份直接 BASE 來源的 Git blob、
  SHA256，以及原附件與候選 zip 身份；附件和 zip 中的 notes 逐 byte 相同。
- 原 zip SHA256：`06c570b699817883ae6d444b33198a02693422c573bc8a7254e04c3aea457e4b`。
  原包 [MANIFEST](candidate-original/t1_broad_probe/MANIFEST.json) 的 41 份
  檔案均核對通過；原包展開內容沒有被 producer 覆寫。
- 原 T1 的 `authority.py --check --negative` 已重跑：20 份上游凍結檔、
  八份原身份及三項負控制通過，見 [log](logs/upstream-authority.json)。
  未宣稱重新證明或重跑全部更上游外部枚舉、no4ct 來源定理或 Lean。

## 2. 任意來源的覆蓋已完成

完整論證見 [SOURCE_COVERAGE.md](review/SOURCE_COVERAGE.md)。
對任意原正對點 x，原 crosscut `c_i–x–c_(i+4)` 把 C8 disk 分為兩個
閉 disk，原有序邊界正是筆記中的 D+、D−。兩片的頂點交集恰為
`{x,c_i,c_(i+4)}`，邊交集恰為兩條原 spokes。

P 精確保留原 B–C8 annulus 與該 crosscut。所有其餘原點、原邊及原
rotation sectors 留在實際所在的一片，沒有跨越兩個開 disk 的原邊。
故 `G=P∪L+∪L−`，`P∩L±=D±`。這是對任意有限原圖的分解，未作
來源大小截斷。BRIDGE 時另一端及原橋整體留在某一 L 中；因此程式
歷史標籤 `PINCH` 所指的 32 份单 x 核心，實際涵蓋全部 p>0 來源。

producer 與 verifier 的 shell 建構均符合此來源映射；逐份具名記錄的
邊、頂點及介面也已核對。單 x 外側為 14 點、28 邊；額外 BRIDGE
外側為 15 點、31 邊。小圖正控制只檢驗實作，不承擔任意來源覆蓋。

## 3. 完整支援論證與有限矛盾

完整審查見 [SUPPORT_LOGIC.md](review/SUPPORT_LOGIC.md)。固定原 B row β，
每份完整 P 染色 f 給出同一 literal 色框中的 γ±，有完整 fibres 雙射

\[
F_G(\beta)\cong\bigsqcup_{f\in F_P(\beta)}
F_{L_+}(f|_{D_+})\times F_{L_-}(f|_{D_-}).
\]

選定 f 及兩份 full lifts 後，其原點聯集唯一；不存在「每個支援軌道
只有一份完整著色」的假設。所有空 fibres 保留。各片完整關係的 S4
等變性才給支援式 `Σ_B(G)=⋃_{q∈R+,r∈R−}M_P(q,r)`；兩個軌道索引
始終從同一份 literal P 染色讀出，沒有拆開共享 x。

若完整 target 為 τ，必有同一份 `R+×R−⊆Eτ`。零輸出 pair 仍屬安全
pair。任一真實支援直積包含於某個完整枚舉的極大安全矩形 A×B；
枚舉包括空索引族交集及空側的正確語義。

實際平面 disk 染色在任一互補色對 split 上的連通分量，必給出所列
非交叉分割；所有獨立分量交換仍是同一 disk 的染色。因此 Kempe
刪除保留任何真實支援：`R+⊆κ(A)`、`R−⊆κ(B)`，不使用普遍四色
可染性，不把抽象支援當成可實現來源。

有限核對證明每個矩形經收縮的外框聯集都不含原 bit 9，即 `01232`。
933、941 都包含此列，所以每個矩形均矛盾。結合 §2 的任意來源覆蓋，
得到本契約下的 h=3⇒p=0；不是由零命中來源搜尋推論不存在。

## 4. 本次實際重播及獨立重建

| 核對域 | 具名 cases | 完整安全矩形 | 完整 P literal lifts |
| --- | ---: | ---: | ---: |
| 單 x 雙 C6，主結論必要範圍 | 32 | 512,568 | 25,348 |
| 額外雙正對點及橋外側 | 32 | 188,452 | 33,808 |
| 原包合計 | 64 | 701,020 | 59,156 |

lift 計數按八份 query 身份累計，含相同 collar 的重複核對。
這些是**外側 P** 的完整著色，不是未知整個來源 G 的著色數。
所有收縮後輸出 mask 恰落在 `0,165,424,429`，均缺 `01232`。

- 原 producer、獨立 verifier、七種 disk 正控制、八項破損證書負控制，
  都在兩個新目錄正常／seed-17 重播。8 份主結果、8 份獨立結果、
  8 份 full-lift gzip 及 controls，共 25 份檔案，各與原包逐 byte 相同。
  見 [normal](replay-normal/REPLAY.json)、[seed17](replay-seed17/REPLAY.json)。
- 第三份 [重建程式](finite/reconstruct.py) 在查看候選輸出之前，從
  BASE 與筆記獨立寫出，不 import 候選算法。完整 32 項的 30,752 個
  矩陣 entries（包括零）、512,568 筆六欄矩形及 25,348 份 literal lifts
  全部逐項一致；見 [比對](finite/candidate_comparison.json)及
  [完整新證書](finite/certificate.json.gz)。其正常／seed-17 亦逐 byte 一致。
- 新的 [Kempe 控制](review/kempe_controls.py) 與原兩套程式、新重建的
  31 rows／93 組交換規則完全一致，七份實際 disk 支援均未被誤刪。
- [完整接合控制](review/join_controls.py) 用上游原面表建外側，加入
  實際小 disk，將 fibre product 與整圖直接著色逐份比較：8 圖、80
  個固定 B fibres、1,709 份 lifts、4,671 個空 product cells 全部一致。
  這些圖不是 no4ct 最小來源，沒有把它們當成 target 實現。

## 5. 審查修補與交付界線

原 verifier 的單筆檢驗使用 record 自帶 kind／pair，未另外把它們綁定
到所要求的檔名槽位。這不影響已收到且逐筆核對正確的原資料，但單用
原 verifier 不能防止以重複槽位冒充全部來源覆蓋。本次
[replay_candidate.py](replay_candidate.py) 增加固定來源身份與完整檔名
槽位檢查；錯誤 kind、錯誤 pair、重複 query、遺漏 query 四項負控制
均被拒絕。原候選程式與證書原封保留。

筆記另有兩項措辭澄清：所有 B–C 邊已在 P，L± 保留其側的 C–內部邊；
「唯一黏合」指已選定完整 lifts 後的聯集唯一。支援不保存 fibre 數量。
審查稿中的 C6 色軌道計數式已校正為
`1×12+10×24+20×24=732`；固定四色色盤使用 `4!/(4−k)!`。

初次總驗收 wrapper 曾因 Python tuple 與 JSON list 的比較失敗；已改
為一致 JSON 表示，保留 [初次失敗 log](logs/verification-create.log)及
[修正後 log](logs/verification-create-v2.log)。沒有刪改原證書以取得 PASS。

本次 SOURCE-COVER 與有限判準均完成，沒有剩餘的 T1 正對點採納數學
義務。main 入口整合／發布是後續交付動作；一般 RING、h≥4 及主命題
的研究義務仍保留。未重播過渡單固定 W5 探索或 pair-prune 弱放寬，
它們保留在原包中，亦不是本定理的證明依賴。

## 6. 重播

從此 audit 目錄執行；新生成目錄須不存在，避免覆寫歷史證書：

```sh
python3 -B verify_review.py
python3 -B replay_candidate.py check
python3 -B replay_candidate.py normal --output-dir /tmp/t1-review-normal-new
python3 -B replay_candidate.py seed17 --output-dir /tmp/t1-review-seed17-new
python3 -B finite/reconstruct.py --output-dir /tmp/t1-review-independent-new
python3 -B review/kempe_controls.py
python3 -B review/join_controls.py
```

`verify_review.py` 是已存成果的只讀身份／一致性檢驗；完整數學重算由
接續三條 producer／verifier／獨立重建命令執行。原包與凍結輸入漂移為零。
