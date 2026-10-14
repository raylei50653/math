# 無四色定理前提路線：C8 三支依賴接入

2026-10-13。BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`；輸入是當時工作樹，
包含既存未提交成果。本輪只寫新獨占 audit，未修改共享文件或舊證書。
直接及遞迴 frozen bytes 見 [INPUTS.json](INPUTS.json)，額外子包輸入另有各自 manifest。

**C8 已接入新 932／933／941 全域最小來源契約，不以四色定理為前提。**
全部 35×3 個 h=3 具名查詢排除 97 項、保留原八項必要條件殘留。
新增 932 分支的 `h≥4,n5≥10`；原八項 apex／內圈／剝層證明與完整 fibres
亦完成接入，得到此新契約下的 `h=3⇒k≥19`。

**無界三支及一般 `K∞=K≤5` 仍 OPEN。** 一般 `k≥16`、共同 `h≥3,n5≥9`
保持；h=3 的十九內點界不能套到 h≥4。本輪沒有新增 Lean theorem。

## 1. 精確契約與證據層

沿用 [前輪外圈報告](frozen/audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md)：
K 是固定 132 個完整 C5 關係及至多五內點 witnesses。在所有有限簡單 C5
disk 的目錄外來源中先最小化內點 k，再最大化邊數；原圖類允許 chords 與
不連通。不改成固定 mask 最小性，不加入 edge-critical、ε、N2 或 P 非空。

同一原圖、原有序 B 及所有列共同 D5 對齊後，完整 `Σ(G)∈{932,933,941}`。
已知 k≥16、G 二連通、B chordless、內面全三角、原內度≥5、框度≥4、
無分離三角形及二邊 crosscut，且有實際簡單內圈 C_(5+h)。
若 h=3，內側 H 含 G 的全部原內點，**H 總頂點數為 k**，嚴格內點數為 k−8。

本輪證據分為：相對最小性的紙面下降、原 cap／rotation／Euler 證明、
完整有限介面及精確計數證書、下游完備小核心的 full-fibre 重播。
實際目標來源仍 `not triggered`；必要向量未被當作來源圖。
已有 k≥16 的外部 Corollary 20、plantri 完備性與球面實作信任仍保留，
本輪未重跑它們，也不把有限 PASS 當作普遍拓撲的形式化。

## 2. 修復兩個舊四色定理入口

完整證明及逐命題大小表見 [geometry/PROOF.md](geometry/PROOF.md) 與
[DEPENDENCIES.md](geometry/DEPENDENCIES.md)。

**原內部小 cap。** 原 C4／C5 的環點本身已是原內點，故其嚴格內點 s
分別滿足 `s≤k−4<k`、`s≤k−5<k`。C4 因而可用前輪受限代表引理，C5
可用全域最小性；同一有序環及 literal 色值的完整關係替換給 s≤3／s≤5。
Euler 與 outerplane 邊界再給 C4 cap 空、C5 cap 空或 W5。這不主張任意
大小 C4 都有小代表，亦不主張替換前後染色數量相同。

由原 C3／C4／C5 caps 和五個 apex H-degree≥3、三個 y H-degree≥4，
逐一排除環距 2／3／4 的 C8 chord。因此三支的原 C8 全是 induced。

**相對平面圖可染性。** 前序無四色定理的下降引理 A 給：若有至多 N 點
不可四色平面圖，則存在完整 Σ=932、至多 N−6 內點的 C5 disk。
因此在此固定最小來源的 k 下，**每個至多 k+5 點的 loopless planar graph
皆可四色**；否則會得到小於 k 的目錄外來源。這只在此相對大小內成立。

原 H 中兩個非相鄰共面點識別後只有 k−1 點，故可染；拉回得到同一 H
使它們同色的完整染色。更一般地，C8 上有 q blocks 的 independent
noncrossing partition，外側樹收縮後有 `k−8+q≤k` 點，故全部 91 個
同色 fibre 的總計數正性均可接入。不同 blocks 仍允許同色。

| 圖或 cap | 精確大小 | 使用依據 |
| --- | --- | --- |
| 原內部 C4／C5 cap | s≤k−4／k−5 | 受限 C4／真正較小 C5 完整關係 |
| H | 總點 k、嚴格內點 k−8 | 相對平面圖可染性；不當成 C5 |
| H/(a1=a4) | 總點 k−1 | 若不可染，下降到至多 k−7 內點的 932 |
| q-block 商圖 | 總點 k−8+q≤k | 同一相對引理 |
| 原 G 加外側五輪中心 | 總點 k+6 | 只能下降到≤k，不能據此排除 932 |

c16-941／c32-941 的 (a1,a4) 原位置為 (3,7)／(1,5)。各有 74 個 proper
同色列，卻全部不在其 102 列必要上界中；相對商圖可染性給整項矛盾。
未採納舊報告不附大小的普遍 cofacial 可染性命題。

## 3. 完整 105 項查詢與八項殘留

[有限證書](finite/certificate.json) 重建全部原 collars、274 個 C8 色軌道、
完整 transfer 和 Kempe obligations；保留 95,900 個具名 annulus fibres，
其中 85,320 個空，合計 12,180 份完整 annulus lifts。內側任意 H 的 full
lifts 沒有被捏造；它們依同一內圈 literal 指派與 annulus 逐点接合。

| 目標 | transfer／Kempe 排除 | 共同計數排除 | 相對 quotient 排除 | 剩餘 |
| --- | ---: | ---: | ---: | ---: |
| 932 | 35 | 0 | 0 | 0 |
| 933 | 33 | 0 | 0 | 2 |
| 941 | 24 | 3 | 2 | 6 |
| 合計 | 92 | 3 | 2 | 8 |

932 的 30 個固定點為空；另外五個為 e 集中於單一框點的全部配置，
各有 100 個內列，但完整外列像為空，無法產生 932 的任何接受列。
所以 932 的 h=3 全排，連同前輪 h≤2 全排及 Euler，得到

\[
\boxed{\Sigma(G)=932\Longrightarrow h\ge4,\qquad
n_5=6+h+\sum_{v\in V(G)\setminus B,\ d(v)\ge7}(d(v)-6)\ge10.}
\]

舊 70 項重播逐項一致，三份共同計數排除及四份可逆 Kempe 迫零 fibres
全保留。計數的 equality 展開係數可帶符號；非負的是同一 H 的實際 x 與
實際 Kempe 軌道權重。没有依靠不同 splits 分別可行就推來源存在。

最終具名剩餘與必要支援大小為：

| 查詢 | e | 必要支援 |
| --- | --- | ---: |
| c15-933 | (0,1,2,0,0) | 134 |
| c18-933 | (0,2,1,0,0) | 134 |
| c04-941 | (0,0,1,0,2) | 193 |
| c07-941 | (0,0,2,0,1) | 193 |
| c15-941 | (0,1,2,0,0) | 171 |
| c18-941 | (0,2,1,0,0) | 175 |
| c20-941 | (1,0,0,0,2) | 171 |
| c30-941 | (2,0,0,0,1) | 175 |

它們是必要條件殘留，沒有任何一項被證來源可實現。
全部 105 項最終狀態與各原名字見 [RESULTS.json](RESULTS.json)。

## 4. 接回 apex、原內圈與剝層

[integrate.py](integrate.py) 核對新的八項完整計數／支援與 apex 所消費的
整份舊 RESULTS 完全相同，並逐一核對 m9 的 8 圖、m10 的 128 圖之原
collar 全部邊、C 名字與順序、e、目標及十列順序。此接入不只比對查詢名稱。

1. 40 個 degree-three apex 假設全排：38 項支援閉包、2 項精確有理 dual。
   紙面用同一 H−a 的完整計數 `x_i=z_j+z_l`，得全部 C8 點 H-degree≥4。
2. 新小 cap 定理接回原短弧限制，八個原面第三點全異，outerplane 耳點迫
   m≥9。m=9 唯一局部 H 接八個 collars 的完整 80 fibres／3,272 lifts
   全得 Σ1023，排除 m=9。
3. 第一層 RING／PINCH／BRIDGE 紙面分類接回；m=10 只有三族共 16 個
   具名 H。接八個 collars 的 128 圖、1,280 fibres／75,936 lifts 全得
   Σ1023；逐層轉移與直接全圖染色的完整 fibres 一致，故排除 m=10。

因此本輪在新三支契約下採納

\[
\boxed{h=3\Longrightarrow m\ge11\Longrightarrow k(G)\ge19.}
\]

任意有限原圖的完整 separator 剝層公式亦接入；PINCH 共享原點同色，
BRIDGE 保留原邊兩端異色，重複 walk 位置仍是同一點。它不保證固定八點
寬度或下一層仍有第一層的度數／接點限制，原七項障礙保留。

## 5. 驗證、停止點與後續入口

主重播為標準庫、只讀：

```bash
python3 -B audits/2026-10-13-c5-no4ct-c8-6cafdfb/verify.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c5-no4ct-c8-6cafdfb/verify.py --check --negative
```

[VERIFICATION.json](VERIFICATION.json) 記錄正常／seed17、負控制、上游重播、
輸入穩定性及交付檢查。[独立覆核](review/REVIEW.md) 從頭重建全部 105
固定點、完整 annulus fibres、95,900 transfer 係數與 91 個 quotient 界面；
不 import producer 或舊 checker。它亦獨立核對相對大小及下游紙面依賴。

前輪整包入口首次因 uv 想寫不可寫的預設 cache 而失敗，原錯誤留存。
後改以唯讀的既有 NetworkX 3.5 路徑重播受限 C4 checker，並用標準庫
重播前輪 collar，均通過；沒有將首次失敗記成 PASS。
本輪未重跑外部 cone 證書、K13–K15 球面生成或 Lean build。

下一窄入口可直接從同一原 C8 的 m≥11 接點／第一層三型開始，保留八份
完整關係與 actual faces；PINCH 首次可在 m=11 進入，不能只沿 RING
推論。h≥4 的一般來源仍需另外處理。本輪不以擴大有限圖搜尋代替無界證明。

Closure scope：新全域最小三支來源的 C8 分類、932 分支 h≥4/n5≥10、
原八項的 apex／剝層及 h=3⇒k≥19 依賴接入。
Updated：僅本隔離 audit。
Reviewed-unchanged：共享交接、STATUS、C8 apex／內圈／剝層入口已核對，
保留歷史文字，後續接手應從本報告取新契約下的採納狀態。
Remaining OPEN：無界三支、八項同圖實現矛盾、h≥4 來源、固定寬度剝層、
一般主命題及新論證 Lean 化。
Propagation stop：未 commit／push，未改寫舊證書或其他研究線。
