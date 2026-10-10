# N45-S 監督預審與增量交叉驗收

2026-10-09；BASE／實際 HEAD：
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**裁決：交付、六項 claim 的紙面預審與固定有限控制通過；正式交叉驗收仍待獨立增量回報。**
已凍結 [S 原報告](../2026-10-09-n45-s/REPORT.md)，逐條核對 BASE 依賴，
並用獨立完整圖枚舉與已驗收的 J 證書交叉核對。沒有發現需退回 S 的數學缺口。
依 [第一批驗收安排](../../docs/history/2026-10-09-n2-45-54-parallel-tasks.md#5-結果返回後的監督與第二批)，
準備 [N45-SU-A／N45-SU-J 增量任務](cross-audit-tasks.md)，兩份可併行；
使用者隨後回傳A／U，已合併兩份proof的增量，見[批次裁決](../2026-10-09-n45-batch-supervision/REPORT.md)。
本輪沒有代替 N45-A 宣稱它已審 S，也沒有把 N45-J 首輪工具驗收算作新 paper 的獨立驗收。

## 1. 凍結交付與來源

| 輸入 | 本輪獨立確認 |
| --- | --- |
| S REPORT SHA256 | `51ea0e8406998e0a2f8dda8edf785e3a67cbeee412cc8a5d3272430bd0138fa1` |
| S checker SHA256 | `94b3fb13e8268080e80a441f595fd3fcab449ea2c2937b2bf92c1725e5977dae` |
| S certificate SHA256 | `9acb2a6b40de32aeca60ecf9a5b33065c9cba60ad47f5243c1eccadf31f59a02` |
| S inputs SHA256 | `09aeaaa919c299c5a8c3ed44ef250e6e90a96ab1040e3fd8bea6fbc57b1e63de` |
| S delivery SHA256 | 見本輪 [inputs.json](inputs.json)，另凍結未自雜湊的 delivery.json 本身 |
| S 輸入 | 69 份逐項與 `git show BASE:path`、獨立 BASE checkout bytes 相等 |
| S 輸出 | delivery.json 的 21 項 hashes／bytes、精確 inventory 全部相符；連 manifest 共 22 檔 |
| J 輸入 | 89 項 MANIFEST hashes 核對；讀取已通過 [J 監督驗收](../2026-10-09-n45-j-supervision/REPORT.md) 的證書 |
| J certificate SHA256 | `ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4` |
| 外部來源 | [Dvořák 講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，2018-03-24，Lemma 7／Theorem 10；重新讀取原始 PDF，bytes 與 S frozen copy 相同，見 [來源核對](gallai_primary.sha256.json) |

S／J 全檔 bytes＋mtime 前後均零漂移；S 的 detached BASE checkout 維持 clean。
S預審階段尚未讀N45-A／N45-U；其後使用者回報兩份，核對與裁決另列批次報告。
所有執行者原目錄均未修改。

## 2. 紙面逐項預審

全部判定均在 S REPORT §1 的**同一原 G**：固定完整 Σ933／941 或整圖 D5 像、
Σ-critical、disk induced C5、ε2、非相鄰雙 degree5、恰兩 mixed，
指定原 spoke e，且 X=G−e 自己是所選拒絕列 β 的 inclusion-minimal core。
root 交換搬運整圖；不改 contacts、actual support、ownership、bridges 或共同字面色框。

| CLAIM | 預審判定與必要界線 |
| --- | --- |
| N45-S-01 | 通過。X 繼承 disk／T4，ε1；任意 derivative 要先保同 Σ minimalize，不能先假定 Σ-critical。刪除公式使用 X 的有效內點 degree≥4。X=M 時 β-critical 才推出 Σ-critical。E2 的空／單點／相鄰二點 Q，加上 Q(X)⊆Q(G)，給表列必要 masks；933 的 q2 已保留。新接受列的每份 full lift 必使已刪 spoke 兩端同色。 |
| N45-S-02 | 通過。unary／mixed 的原 degree4 連通 lists 有未固定 r-contact 的 strict slack，故完整局部 relation 非空、禁色界成立。s 的 side incidence 5−m_s 保 E_s≥m_s−1>0；X 的 χ0、degree4 使 B-C2 五項非負費用全零，對每個 b∈E_s 得兩欄飽和、不交、完整覆蓋 E，並且沒有 E 外禁色。 |
| N45-S-03 | 通過。c∉E 時，X 的 side factors 無重疊，c 已被恰一份原因子禁止；加回 spoke 增 O 一。c∈E 時 side overlap 不增，mixed 欄聯集仍為 E，但可用色失 c，增 λ 一。blocker 為整 unary 時不可套重色 spoke 的 E4-D；mixed owner 可隨 b 改變。 |
| N45-S-04 | 通過。實際支援 singleton {h} 的局部 relation 只見 c=β(h)，可用固定 c 的共同 S3 置換。全 B-touch 的原 G 與 one-sided 保 N-diagonal 四個 diagonal；其餘恰三軌道，行／欄接點界排除 k_r+k_s≤3 的任何 forbidden orbit。這只排低 incidence singleton，沒有排 (2,2)、(1,3) 或一般 short。 |
| N45-S-05 | 通過。兩 short 先由 diagonal 接回迫 E∩E_s=∅，進而 m_r+m_s≤5；每份 mixed 總 incidence≤3，非空支援加 S-04 排 singleton，故各為真框邊 pair，原盾弧各長1。兩原 unary 的各自 critical-contact witness、避自身外路與 one-sidedness 可用 B-S0，原費用 1+1+2+2>5；含 long 的兩 unary 子型另由 2+2+2>5 排除。 |
| N45-S-06 | 通過。u0 由原兩 short 的未用色 diagonal 排除，u2 由 S-05 排除。無 unary 側若 m_t2，三 original spokes 的 star 與 H−t 連通、全 B-touch 迫唯一含兩個非-spoke 框點的長3弧；三份原盾弧全在此弧內，却需 1+1+2=4。故 m_t≥3，和 m_a≥2、總和≤5 得 (m_a,m_t)=(2,3)；LOW／HIGH 的 side incidence／E 域計數相符。 |

以上沿用 BASE 的 E2 任意大小化約與有限末端證書、N-diagonal 的 hub／Gallai 論證、
B-S0 的拓撲互斥及拒絕見證、B-C2 的完整逐欄計數；沒有重跑其全部分類。
外部 Lemma 7 的 strict slack 步驟已重新對原文核對；未新增 Lean theorem。
獨立增量 A 必須核這些依賴如何用於新 claim，不能只返回「BASE 引理成立」。

### 2.1 S-06 原 star 面論證的展開

若 t 無 unary 且 m_t=2，t 恰有三個不同的原 spoke 端點 A。
原 H−t 是由另一 root、P、Q、唯一 unary 連成的一份，全部非框部分避开 B+t-star，
因此在 star 的同一個 disk 面。B∖A 的兩點都須由 H−t 碰到，
故同一個 A 間的 open 框弧含這兩點；另兩弧各長1，所在框弧長3。

對每份 C∈{P,Q,U}，K_C 只保 B、C 與它的框附件，C 的非框部分在上述長弧面內。
另兩個小面內沒有 K_C 的非框部分；它們可經未列入 K_C 的 t-star 鄰域連到 t。
所以兩個小面都在含 H−C 的 F_C 中，它們各自的框邊仍在 ∂F_C 上。
於是 σ_G(C) 不含那兩邊，三份盾弧都包含於同一長3弧。
再用原盾弧邊互斥與 S-05 的 1、1、2 下界得矛盾。
此論證完全在原 G；不假定 X 全 B-touch，也不搬用 U4 的 retained44／O11 下界。

## 3. 獨立有限核對

[review.py](review.py) 不 import S、J 或專案 checker。
採固定頂點順序與 forward checking，枚舉指定圖的所有完整染色，取精確 root-pair 集；
既核接受又核空 fibres，並逐份核 S full lift 的所有原邊與字面 pins。
對 singleton 表則由實際固定 c 的置換重建軌道，另核完整抽象容量。

| 範圍 | 結果 |
| --- | --- |
| S 普通／seed17 `--check` | 新 logs 均 exit0；S bytes／mtime 不變 |
| S exclusive-create guard | 預期 exit1／FileExistsError，原證書不變 |
| singleton 288 項 | 92 項滿足接點界；其中低 incidence 的12項均為通用 relation；196項未觸發接點界 |
| 3 個抽象完整16-pair模型 | 共4個可核容量欄，等式與 blocker 二分相符；缺 graph／full lifts／target Σ／criticality／minimality，不是來源正控制 |
| 12 個 incidence scalar／2份 Q-mask 表 | 獨立必要算術相符；不承擔 disk 實現 |
| 19 份原 N2 圖 ×10列 | 190 份完整 root-pair 集與 J 相等，S 接受性、原 contacts／ownership／support／rotation 相符 |
| 47份原 spoke ×原拒絕列 | 全部接受；完整 root-pair 集與 J 相等，full lift 在原删邊位置同色 |
| 合計 | 237個圖／列查詢，3792個 root-pair cells，218份 S full lifts 逐邊合法 |
| 精確 N45-S 來源前提 | 0觸發；19圖不具完整 canonical 933／941，47份 derivative 未拒絕所查 β |

正常與 seed17 的獨立 review output 見 [independent_review.json](independent_review.json)、
[independent_review_seed17.json](independent_review_seed17.json)；新 S 重播及 guard 見
[replay_records.json](replay_records.json)。命令、exit、文件檢查見 [checks.json](checks.json)。
沒有把有限控制接受性當成 S-01–06 任意大小 paper 的證明。

```bash
python3 -B audits/2026-10-09-n45-s-supervision/review.py --output /tmp/n45-s-review-fresh.json
```

輸出必須尚不存在；以上只讀輸入，生成使用 exclusive-create。

## 4. 文件失敗、管理狀態與停止點

保留 S 原交付的兩項文件失敗，不修寫原 logs：

- fresh BASE 的 docs check 缺兩份未入 Git 的歷史 audit 目標；本輪同 checkout 重播仍 exit1。
- 全工作樹 DocGraph 遇 scratch／並行來源 docs 副本 duplicate IDs；本輪實際結果另記 checks。

S預審階段正式 `docs/**/*.md` DocGraph exit0（62 documents、213 relations、5 families），
共享工作樹 docs check exit0（587 Markdown、7012 links），tracked whitespace exit0。
fresh BASE docs check exit1（2 errors、586 Markdown、6982 links），全工作樹 DocGraph
exit1（62 duplicate-ID errors）；與兩份保存失敗分列，不宣稱全域 PASS。
這兩項是交付治理限制，不是已發現的 S paper 反例。

管理狀態：S／U待增量交叉驗收；J首輪工具／固定控制、A首輪依賴已驗收，詳見批次裁決。
已核出的 S 紙面窄排除是**指定 spoke-omission 45／54 身份下 u2 不可能**，
其正式採納等獨立 A 增量；零 slack 與 2／3 身份是必要化約，不是其餘來源排除。
本輪未啟動執行者或對外發布；下一個研究批次待第一批裁決後再選。

仍 OPEN：S-SHORT-U-LOW、S-SHORT-U-HIGH、一 long 的零／一 unary、兩 long 零 unary，
以及整 unary 省略、原55、無45／54 core來源與一般 N2。
LOW 的 n_U1 是目前候選最小義務，尚未另派，須同原圖驗全部列、完整 relations／lifts 與 criticality。

文件責任核對：只改派工狀態、Kempe 導覽相關入口、STATUS 直接索引。
L0 預審與證據完成；L1 已更新；尚未正式採納子型 closure，不改 BASE E4 的權威正文或 Phase B。
父 N2／猜想 E 仍 OPEN、上層入口語義不變，本輪停止於 L1。
未 commit／push；不改 S／J／A／U 輸出及既有 artifact。
