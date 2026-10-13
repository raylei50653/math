# C₈ 外圈完整 transfer 與同圖共同計數

2026-10-13。BASE／開始 HEAD 均為
`3097ef5be241b7777451a5ef8a663f3987d6b866`，分支 `main`，開始工作樹乾淨。
本包只含本地研究與驗證，沒有 commit、push、PR、issue 或留言。
來源及逐檔 SHA256 見 [BASE.json](BASE.json)；原證書、frozen inputs、manifest
及歷史失敗紀錄均保留。本輪使用的正式來源在 BASE 均可直接讀取，毋須封存還原。

## 1. 最強結論與採納邊界

在完整最小目錄外來源契約下，h=3 的 **35 份具名外圈、70 項查詢全部覆蓋**。
完整 transfer 與必要 Kempe 閉包排除 57 項，共同計數恆等式再排除 3 項。
其餘 **10 項為必要條件殘留**：有精確共同計數向量，正計數支援本身也通過
全部本包 Kempe 必要閉包。它們不是實際圖、反例或關係實現。

| 完整 Σ | 查詢 | transfer＋Kempe 排除 | 新共同計數排除 | 必要條件殘留 |
|---|---:|---:|---:|---:|
| 933 | 35 | 33 | 0 | 2 |
| 941 | 35 | 24 | 3 | 8 |
| 合計 | 70 | 57 | 3 | 10 |

所有排除均對任意大小合法內側圖成立；有限圖控制只校準實作。
**不能採納 h≥4 或 n₅≥10**；共同下界仍為 h≥3、n₅≥9。
本輪沒有證明 K≤13=K≤5，也沒有證明 K∞=K≤5。
全部逐項狀態、殘留分配及最終支援大小見 [QUERIES.md](QUERIES.md)。

## 2. 精確来源與外圈完備性

G 是所有完整關係不屬於 K132 的有限簡單 disk-C₅ 圖中，先最小化內點數 k、
再最大化邊數的來源。原有序外框 B=(b0,b1,b2,b3,b4) 無 chord；G 二連通，
所有內面三角化；整張圖經同一 D₅ 搬運後完整 Σ=933 或 941。
原框點完整度數至少四，原內點完整度數至少五。沿用既有二邊 crosscut 與
分離三角形排除，原邊界鄰點形成實際簡單內圈。沒有加入 N2、edge-critical、
ε=2、兩個 degree-5 roots、其餘 degree-4 或 Gallai 假設。

令 e_i=deg_G(b_i)−4（即任務中的 a_i；此處 a_i 留作原框邊 apex），Σe_i=3。
五個 apex 及每個 b_i rotation 中的 e_i 個私人鄰點決定整份環帶。
35=C(7,4)=5+20+10；每份查兩個目標，不作對稱縮減。
內圈頂點依原 rotation 具名；全部其餘 chords／頂點／邊留在同一 H。
分配決定全部外圈附件的證明、原 labels 及 35 份清單見
[COVERAGE.md](COVERAGE.md)，不是只把弱分拆數目當成圖形分類。

## 3. 完整 literal transfer 與 Kempe 必要上界

[interface.json](interface.json) 保存全部 274 個 C₈ proper S₄ 軌道、6564 份
literal 指派、每份指派的軌道歸屬、全部十個外列，以及每份環帶的原邊／附件。
二色、三色、四色軌道數分別是 1、42、231；軌道大小分別是 12、24、24。
這些值由完整指派及 restricted-growth partitions 獨立枚舉，另以
P(C₈,q)=(q−1)⁸+(q−1) 和 onto-color inclusion–exclusion 核對。

固定同一 literal 色框 0,1,2,3，令

\[
T_{r,p}=|\{s\in\operatorname{Orb}(p):\text{s 與固定原外列 r 在全部外圈原邊相容}\}|.
\]

若 x_p 為同一 H 在固定具名內列 p 下的延伸數，則完整原外列計數
y_r=Σ_p T_(r,p)x_p。係數直接枚舉 literal 接合，不拼接分別正規化的代表。
逆向固定 p 的 literal B lifts 也全部保存，並逐格驗證
24 T_(r,p)=|Orb(p)| L_(p,r)。因此二色列使用 L/2，而非一律 L。

由所有會產生拒絕外列的內列開始排除，對每份內列及三組互補色對，枚舉
實際二色連通分量在環上可能形成的 noncrossing partitions 與全部交換軌道。
若某色對已無一份完整交換軌道包含於候選集合，就刪除此列。
初始集合、每輪同步刪除及失敗色對、固定點、完整外列 preimages 均保留。
同一實際 H 的完整關係始終留在集合中，證明見 COVERAGE §6。
固定點只是一份必要上界。

## 4. 普遍共同計數與精確排除

對任意有限平面 disk H，逐邊 inclusion–exclusion 給

\[
x_p=\sum_{F\subseteq E(H)}(-1)^{|F|}4^{k_0(F)}E_{\pi(F)}(p).
\]

分量邊界分割 π(F) 必 noncrossing。因此同一 x 落在全部 1430 個 equality
vectors 的共同線性空間。proper C₈ 上只有 91 個非零欄，精確秩也是 91；
其餘 1339 欄為零。只要求實際計數 x≥0；**不要求展開係數非負**。
完整 partitions、非零矩陣與所有精確恆等式保存在
[最終計數證書](counts/certificate.v2.json)，零欄由 active indices 的補集指定。
另提供顯式的 [274×1430 完整矩陣](equality_matrix.json)，與壓縮表示逐格核對。
checker 逐項在全部 1430 個 partitions 上驗證每個恆等式。

新排除的三份分配都是 Σ=941：
`(0,0,1,1,1)`、`(0,1,1,0,1)`、`(1,0,1,0,1)`。
每份證書給出正係數左式等於必要零列的有號線性組合；非負性迫左側全部
計數為零，涵蓋接受外列 `01232` 的**全部**必要 preimages，故矛盾。
例如第一份迫

\[
x_{28}+4x_{123}+x_{207}+2x_{225}=0,
\]

而 `01232` 的全部上界內 preimages 恰為 `[28,207,225]`。
右側 46 個有號零列係數與其具名色列完整保存在證書，無浮點驗收步驟。
其餘兩份的全部 preimages 分別為
`[18,59,87,131,205,250,269,272]` 與
`[18,21,59,60,176,270,271,272]`。
詳細證明與算法見 [COUNT_PROOF.md](counts/COUNT_PROOF.md)。

## 5. 精確殘留與缺少的結構

對十份殘留再交替套用共同計數迫零和 Kempe 刪除，保存每一步理由。
最終每份保存全部 274 個具名 x 座標、共同 equality 展開係數、十個原外列計數，
以及正計數支援的 Kempe 檢查。接受外列全正、拒絕外列全零。
初次解 [certificate.json](counts/certificate.json) 是較弱放鬆的歷史診斷，
其中若干解的自身 support 不閉合；它沒有被改写或冒充最終殘留。

有理數可乘共同正分母化為非負整數，保持全部齊次等式、零列及正性，故
單靠「真實計數必為整數」不能排除這些向量。它們證明本包列出的 transfer、
Kempe 必要閉包及共同線性計數條件仍不足以排除全部 h=3。

未編碼的來源結構包括：原近三角化的面／邊相容性；apex 的 H 度數至少三、
私人鄰點的 H 度數至少四、H 私有內點的度數至少五；分離三角形排除及全域
最小性。更根本地，分割係數須由**同一張 H 的邊子集展開**共同實現，不能
任選線性空間中的係數。Kempe 規則也只檢查每列每色對有可用分量分割，
未構造不同完整染色之間的共同連通分量、交換雙射與原面配置。
本輪沒有證明上述哪一條足以排除殘留；下一個缺口是從這些同圖結構導出
能否定所列殘留的新增必要條件，不能把放鬆可行向量稱作來源。

## 6. 證據、驗證與未執行項目

主要重播（僅標準庫，無 LP solver）：

```bash
python3 audits/2026-10-13-c8-joint-count-3097ef5/interface.py --check
python3 audits/2026-10-13-c8-joint-count-3097ef5/controls/checker.py --check
python3 audits/2026-10-13-c8-joint-count-3097ef5/counts/checker.py --check
python3 audits/2026-10-13-c8-joint-count-3097ef5/verify.py --check
```

SciPy 僅發現候選；所有排除與可行向量由 int／Fraction checker 精確驗收。
独立介面 checker 不匯入 producer，從全體 NC partitions 重建 Kempe 表；
有限實際圖為空 C₈、fan triangulation、wheel、two-center disk。
4×35×10=1400 份全圖 literal 計數與 transfer 一致，全部內列完整計數亦保留。
wheel 的實際計數通過共同恆等式，Boolean support 向量則不通過。
完整正常／seed17、破壞係數／preimage／標號／軌道權重、C₇ 回歸及輸入 hash
紀錄見 [verification.json](verification.json)；獨立證明審查見
[COUNT_REVIEW.md](COUNT_REVIEW.md)。修改清單與產物 hash 見
[MANIFEST.json](MANIFEST.json)。

`lake build` 為既有專案回歸，未新增 Lean theorem，沒有把本輪紙面定理
或 Python 證書稱為 Lean 形式化。沒有擴大來源圖搜尋、重播外部論文計算、
假設未知 count-cone 猜想或修復全域 DocGraph 的歷史 duplicate IDs。
文件核對及正式／全域 DocGraph 分開記於 [documentation_checks.json](documentation_checks.json)。
本次實際結果：C₇ 回歸、所有精確 checker、normal／seed17 產物一致性、所列
負控制及 `lake build` 均通過；文件連結、正式 docs DocGraph 與 `git diff --check`
通過。全域 DocGraph 失敗仍恰為 62 項歷史 duplicate-ID，沒有其他種類錯誤。

只更新外圈權威入口、Kempe 導覽與 STATUS 對應條目；README／HANDOFF 的
研究線路由與進行中狀態沒有變，維持原樣。原下界消費文件仍正確，無須提高
任何數字。其他 session 的 N2／W5 工作另有隔離目錄，沒有覆寫。
目前停止點仍由 [Kempe 導覽](../../docs/c5_kempe_guide.md) 維護。
