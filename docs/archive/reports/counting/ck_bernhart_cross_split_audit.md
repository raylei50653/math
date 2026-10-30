# Bernhart B₈ 證書的跨 split 語意稽核

2026-10-29，接續 [Bernhart 基準](ck_bernhart_benchmark.md)、
[標準計數錐](../four-color/four_color_counts_surgery_verification.md)與
[去奇偶／共同切口](../c5/connections/c5_parity_shared_cut_continuation.md)。不修改既有具名圖與雜湊證書。

同日後續：[retained 共同原邊交會奇偶](ck_bernhart_retained_intersection.md)為兩條射線補具名
局部真來源與完整切口，證 rotation 必要式；未排除任一射線的全部正比例來源，76 列不變。
其[共同端點續進](ck_bernhart_endpoint_ray_continuation.md)完成 RIP 邊界修正，並將 r₂
候選來源合法封口成帶標記邊的六葉來源；射線排除仍 OPEN。

## 實驗前登記

本輪只使用已保存 6–6 Bernhart 的 76 列計數向量、88 個正 signed signatures，
核對其 word／split incidence，以及能由這些觀測推出的額外限制。
不假定 `y_S` 是同一圖的全部 `PM_I` 計數，不為沒有原邊身份的模型虛構共同切口。

1. 獨立重算完整 incidence 方程，保存具名座標／signature／word 對照。
2. 尋找精確同觀測、不同跨 split 配對的 extension 控制；若觀測不能決定 shared-cut 或
   去奇偶六項式，給出明確投影缺口，不任意將一種 extension 的失敗歸因於觀測本身。
3. 審計「非平面極射線」一詞：嘗試給精確非比例分解，並明列計數向量、完整 LP lift、
   實際來源與最小反例外側的不同量詞。
4. 只有額外條件的 soundness 已證、且所有合法 extension 都被排除，才准刪除邊界座標。
   本輪不擴大未知原圖搜尋，也不以經典 C 可約性直接認定抽象 B₈ 向量不可平面實現。

此段先於本輪實算建立；結果與 OPEN 邊界隨證書完成後補入。

**追加登記（仍在相關實算前）：** 使用固定 C₈ wheel，在一份內三角面 stack 一個三度點，
對偶為局部 `Y→Δ`。兩圖各自完整列舉 Tait 與全部偶刪葉 PM 族，核對 boundary `n`、
signed-signature `y` 是否完全相等，而普通 PM 計數 `Z_I` 是否改變。
舊 PM 的唯一延伸使補圖路／環長加二；額外 PM 可包含三條外接邊，其補圖有新三角奇環。
若出現此差異，作為真 plane 來源的非函數性控制；不宣稱該控制具有 Bernhart 的阻擋支援。

## 1. 裁決：76 列仍保留，但「極射線」稱呼可以確定更正

本輪沒有排除新的 Bernhart 座標。得到三個可重跑的精確結論：

- 已存的 76 列 `n` **不是極射線**，可分成兩個不成比例的 41 列整數計數向量。
- 兩個分量各自是完整 `(y,n)` lift cone 的極射線；其 `n` 投影是否極端尚未證明。
- 真正平面 C₈ 的兩張固定圖，具有**完全相同的全部 n 與 y**，普通 PM 表卻不同。
  因此不能將當前 `y` 當作 `Z_I`，或認為已決定普通 PM 支援。

「非平面」也不能從 Bernhart 的古典 C 可約性免費推出：
前輪還原使用假想**頂點最小反例**的最小性，迫其外側有一份指定替換框列。
任意可染平面外側沒有這項較小商圖可染保證。要判定當前抽象向量沒有任何平面來源，
仍需獨立證明；本輪沒有這份非實現性證書。

## 2. y、普通 PM 與隱藏奇環的精確關係

固定一張實際 near-cubic disk `Q`、八個有序葉及三種邊色。令 `PM_I` 為
刪除葉集 `I` 的全部完美匹配，`Z_I=|PM_I|`。固定第三色的匹配 `M` 後，
`Q−M` 為以 I 中葉為端點的完整路徑及若干閉環。
若某個閉環為奇長，M 不產生任何 Tait 染色；若全部閉環偶長，
各閉環獨立有兩種交替填色，完整路徑則由指定端邊字唯一決定填色。
令 `S(M)` 記每條路的端點與長度奇偶，`c(M)` 為補圖閉環數；有

\[
y_S=\sum_{\substack{M\in PM_{\operatorname{cover}(S)}\\
  S(M)=S,\ \text{全部閉環偶長}}}2^{c(M)}.\tag{1}
\]

此式是同一原圖的完整匹配計數。不同 S 的匹配族互斥，因此對**實際整數 counts**，

\[
Z_I\ \ge\ \sum_{\operatorname{cover}(S)=I}\operatorname{popcount}(y_S).\tag{2}
\]

證明：每個 `y_S` 為二的非負整次冪之和，項數至少其二進位 1 的數目；
兩個相同次冪相加會進位，不能增加 popcount。不同 S 再相加即得 (2)。
特別地 `y_S>0` 迫相應普通 PM 族非空；`y_S=0` 不迫其空，
而 `y_S=2` 也可能只來自一個有一個偶閉環的匹配，不能據此聲稱 `Z_I≥2`。
`n_w=0` 只是否定該字的完整 Tait 延伸，不否定所有普通 PM。

本輪固定 lift 有 88 個正 y、總權重 92（84 個 1、四個 2），涉及 67 個 covered sets。
式 (2) 是條件於「這些 y 確為同一實際來源的 counts」的必要界；
它沒有為當前抽象證書提供原圖、被忽略的奇補匹配或共同切口。
即使選定比例縮放，普通 PM 的隱藏部分仍未被決定。

## 3. 精確非極端分解及兩個較小子靶

76 個正 n 的總質量為 88（64 個 1、12 個 2）。保留完整 4,923 條標準 B₈ 方程，
限制至既存正座標的 88 個 y 與 76 個 n，得到 164 欄、227 種非零行。
有理數 Gaussian elimination 得 rank 162、kernel 維度二。
兩個非負整數基向量的和**逐座標等於**原 lift，各自滿足全部 4,923 式：

| 分量 | 正 n 座標 | n 總質量 | 正 y 座標 | 正欄數／rank |
| --- | ---: | ---: | ---: | ---: |
| 第一個 | 41 | 44 | 46 | 87／86 |
| 第二個 | 41 | 44 | 46 | 87／86 |

兩份 n 在具名座標 0、1 已不成比例，故原 n 不是投影 B₈ cone 的極射線。
各分量的正座標矩陣 kernel 維度一，故在完整非負 lift cone 中為極射線：
任何非負分解都不可能在原零座標產生正質量，其分量只能留在此一維 kernel。
投影 n 可以有其他 y lift，因此上述 rank 不自動證 n 極端。
這兩個 41 列向量可作較小子靶；本輪沒有將其宣布為非平面，也沒有排空它們。

## 4. 先加「同字三 split 聯合分布」仍無增益

已存 n 對應 453 個正八端口 words、總質量 522；三 splits 合計有 1,566 單位 incidence。
完整逐 word 資料保存每個 split 的全部正 signature 權重。
若只增加形式聯合變數 `q_w(S₁,S₂,S₃)≥0`，要求三個 marginals 等於各自的 y，
每個 word 的三份邊際總質量都同為 `n_w`，故永遠可配成共同 tokens；
一般實權重也可用 `q=y₁y₂y₃/n_w²`。因此這層 transport projection 恰回到原等式。

具名例為 `w=11111111`、`n_w=2`。signature 編號沿用原完整 1,961 份次序：

```text
S1849 = 05 / 12 / 34 / 67，全部 sign −1
S1913 = 07 / 14 / 23 / 56，全部 sign −1
S0    = 空配對

聯合 A： (1849,1849,0)、(1913,1913,0)，各質量1
聯合 B： (1849,1913,0)、(1913,1849,0)，各質量1
```

A、B 的每個 split 邊際完全相同，跨 split 相關性不同。
這兩份都是**代數 extension**，不聲稱有原圖或真實交換動作。
它們明確指出觀測沒有保存共同染色中哪幾份 signatures 同時出現；
即使將此相關性補上，[既有同 disk 反例](../four-color/four_color_counts_surgery_continuation.md#3-連全部具名分量分割也不能自我更新)
仍表明它不足以自我更新切口歷史。該舊反例本輪僅沿用權威報告，未重跑。

## 5. 普通 PM 六項式的投影缺口：代數與真圖兩層控制

### 5.1 同 y 的正、負代數 extension

對當前 y，先給每個 S 恰 `y_S` 個「零閉環 good matching」形式原子，
令 `g_I=Σ_cover(S)=I y_S`；本輪 `max g_I=3`。
取全部 128 個偶數刪葉集合的普通 PM counts 都為 `Z_I=3`，
並給每族 `3−g_I` 個隱藏 odd 原子。這不改 y，且全滿足式 (2)。
全部改成 `Z_I=4` 並補相應 odd slack，也成立。

對任意偶數共同刪除基集 B 及與其不交、依環序四葉 a,b,c,d，
完整核對 560 份 [P1b 六項式](../c5/connections/c5_parity_shared_cut_continuation.md#2-p1交錯路的完整證明與精確計數式)：

\[
Z_BZ_{Babcd}+Z_{Bac}Z_{Bbd}=Z_{Bab}Z_{Bcd}+Z_{Bad}Z_{Bbc}.\tag{3}
\]

兩份 extension 全部通過，因兩側都是 `2L²`。若只將 `Z_∅` 從 3 改成 4，
同一 y 與非負 hidden slack 仍保留，但 70 式失敗，首式為 `21≠18`。
所以由同一 y 任選一次失敗的 PM extension，不能推出 y 自身違反 (3)。
反過來，通過這些方程也不證實際圖存在；此處只否定「當前 y、普通 PM 下界加 (3) 已迫矛盾」這一推論。

### 5.2 真 plane C₈ 控制：n、y 全同而 Z₁₇ 改變

固定原環 C₈ 與中心 hub，取 wheel；在面 `(r₀,r₁,hub)` 插入一個三度點並連該面的三點。
兩圖均保存全部原邊、整數嵌入及有向面，精確幾何 checker 通過。
每份舊四色染色在新三度點恰有唯一可用色，因此全部有序 boundary n 相同。
對偶中這是把一個 cubic vertex 展成三角形。

舊 PM 在該頂點恰用一條外接邊；延伸時在新三角中補一條匹配邊，方式唯一。
補圖一段原路被長三的路替換，長度加二，閉環個數與奇偶、各完整路的 signature 均不變。
新 PM 還可以取三條外接邊，此時補圖含新內三角奇環，故不貢獻 y 或 n。

| 真 disk 控制 | 正 n 列／正 y | 普通 PM 總數 | 偶補 PM 總數 |
| --- | ---: | ---: | ---: |
| C₈ wheel | 43／47 | 47 | 47 |
| 一面 stack 後 | 43／47 | 55 | 47 |

兩份完整 n、y **逐項相等**；八個 PM 族增加一份。
其中 `I={1,7}` 在舊圖為空，在新圖有唯一匹配，其補圖含新三角奇環。
兩圖各自全部 128 族 PM 及全部 560 式均完整核對；另從原 primal 邊獨立枚舉染色核 n。
這證明在真 plane C₈ 圖類上也不存在由 `(n,y)` 唯一重建普通 PM 表的函數。
它不證 y 無法支持任何 PM 必要條件，也不是 Bernhart 阻擋支援的來源實現。

## 6. shared-cut 接口與精確停止點

shared-cut 必須輸入同一完整 Tait 染色、具名原邊路徑的先後順序、各第三色原邊的共同 port 身份，
以及兩份刪路後的完整外部接線。n、y 及本頁形式 q 均不提供這些資料。
一份失敗的任選 cut extension 只能否定該 extension；要刪除一個邊界座標，
必須證所有同源合法 extension 均失敗，並保留其他座標與其共同計數關係。
即使排除一份 primal 向量，也不能直接刪整個 B₈ 面中的座標。

本輪新增的是式 (1)–(2)、精確非極端分解及兩層投影缺口證書。
76 列與兩個 41 列子靶仍保留。能從同一未知原圖推出何種必要 mixed 接線、
如何保證跨 split extension 的共同來源、任何新座標排除／可約性與 4CT 均 OPEN。
沒有新增 Lean、未知圖搜尋或新 LP 必要條件；經典 `LOCK-NO-GAIN` 的量詞未改。

## 證據、重播與治理

紙面證據為式 (1)–(2)、transport 投影、非負零座標的 lift 極端性準則與 Y→Δ 證明。
Python 固定域證據保存完整 incidence、兩個整數分量、453 份 word marginals、
兩份形式 PM 表及兩張實際 plane 圖的全部 PM、n、y。
[完整證書與來源 SHA256](../../../../audits/2026-10-29-bernhart-cross-split-e1a90fe/verification.json)、
[程式](../../../../scripts/ck_bernhart_cross_split_audit.py)、
[重播收據](../../../../audits/2026-10-29-bernhart-cross-split-e1a90fe/RECEIPT.json)。

```bash
python3 scripts/ck_bernhart_cross_split_audit.py --check audits/2026-10-29-bernhart-cross-split-e1a90fe/verification.json
```

只讀既有 Bernhart 證書，先對其前輪收據核 hash，沒有改寫舊證據或主求解器。
L0 新增本頁與獨立腳本；L1 導覽／STATUS 由整合者連入；既有 C 正控制、B₈ 最大支援及
單 split 無增益裁決保持原狀，不上推父命題收尾。未 commit／push。
