# W7：原接觸定理、兩個 target 的分量化約與任意 k 模板秩

2026-10-21；Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。
工作前 tracked tree 乾淨；[BASE.json](BASE.json) 凍結本輪來源 bytes／SHA256。
數學來源仍為 `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02` 的嚴格 only-R／W7
契約；沒有重新枚舉原圖、沒有求解或延長大型 LP，沒有 Lean 修改。

**本輪新增結構性結果；嚴格 W7 及既有必要計數錐仍 OPEN。**
原112份共同必要接觸縮為69份，實際正 witness 再限於40份；另證任意
`k>=1` 的未裁切局部模板秩公式。這些結果都沒有證出 target fibre 為零。

## 1. 固定來源、量詞及證據層

完整承接[五邊路來源契約](../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
及[共同必要計數模型](../2026-10-20-w7-count-cone-d5b8a86/MODEL.md)：
任意大小原 plane C5 disk G、原框 `(x,y,a,b,c)`、支持941、全域最小內點數
再最大邊數、全部原 stars／旋轉／私有點及附件、原短圈定理。固定原 Q1
接受零的 J1 type III 實際12五邊路，且它圍出的 induced C7 內部恰只有 R。
只有在這個額外 only-R 前提下，才是完整七度 W7。

同一原核心

```
F13=G-{b,p,h,R,x,y,r},
rim=(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)
```

供應全部完整 Z、空 fibres、私有分量重數及所有完整 cap lifts。
一張原圖只有一份固定完整接觸 profile；沒有跨型或跨 palette 拼湊來源。
全來源計數與選路後的歷史殘餘仍分開，沒有把後者當作完整 Kempe orbit。

原圖幾何及任意 k 模板秩由紙面證明承擔；有限 checker 核對指定原接觸表、
全部原欄及已凍結六模板，不把有限核對升格為 Lean 形式化。

## 2. 原 W7 外點接觸定理：112 → 69 → 40

[幾何紙證與完整證書](geometry/PROOF.md)證明：

1. 閉 W7 外的同一原點至多接兩個原 C7 框點，且必相鄰。否則它與原 R
   圍出 C4，兩條開框弧各含原點，違反原 C4 空內部。
2. 三種原 C5 分別迫 u3、u2 或 v 為**完整五度中心**；缺必要 spoke 或另有
   原鄰點時不可能。完整合法 W5 例外仍保留。
3. W7 七條框邊的外側第三面點皆不同。其中兩個已是 p、q，另外五個對應
   五邊路；C13 無弦時，這五點均是同一 F13 的不同原私有內點。

把前兩條施於原112份完整共同接觸，只刪已有不可能原圈的型：

| 範圍 | 原必要型 | 本輪剩餘 |
| --- | ---: | ---: |
| 全部共同接觸 | 112 | 69 |
| `d(n)=5`／`a-u4` 有原邊 | 44 | 30 |
| `d(n)>=6`／九框 induced | 68 | 39 |
| target44459 proper | 38 | 28 |
| target44466 proper | 29 | 24 |
| 至少一個 target proper | 54 | 40 |

43份幾何排除是28份非空原 C4，再加15份缺失完整 W5 中心 spoke；交疊理由
沒有重複計數。最後40型的 n=5／n>=6 分別為18／22。原正 witness 必為兩個
target 之一，故40型是本契約內真來源的必要覆蓋；不聲稱任何型已實現。

無弦原profile0仍保留。五個外側原私有點說明此型不能縮成一張空外側的小圖；
要排除它，仍需要941共同色義務或最小性的新增作用。

## 3. target 交換、完整 orbit 與固定原附件

[完整分量紙證](review/PROOF.md)從原307,197欄中只取兩個 target 的01|23
half-rows：各有10欄，五個共同、各五個專屬。全部15欄逐份恢復完整 boundary
components，並重生16個 normalized rows，沒有以 pair marginals 代替。

令 K 為同一完整著色的實際01分量 K(v,w)。若 K 的原 rim 接觸恰為 `{v,w}`，
交換整個 K 給兩個 target 的 separated strata 完整雙射，包含所有原私有點。
joined stratum 中，K 另接 a,n,c，且可能包含 u3／u1；此時沒有全域 target
相等式，也不假設原圖交換 v,w 的自同構。

令 U 為五個共同欄的 X 之和，V_A、V_B 為各自五個專屬欄之和，則

```
2Z44459=U+V_A，2Z44466=U+V_B。
```

如果日後證 `Z44459=0`，則第二個 target 只剩五個 joined 欄：

```
2Z44466=X43380+X43381+X48647+X66602+X67765。
```

這是條件化約，沒有把其前提當成本輪成果。固定原附件對這15欄的完整
接合結果見[逐型原弦／完整 orbit 分類](review/PROFILE_ORBITS.md)：69型逐一核對
每個完整欄的全部16個 rows，40型數量不再減少，但分成

| 固定原附件 | 型數 | 兩個target的全部剩餘欄 |
| --- | ---: | --- |
| 有原邊 u3v | 8 | A 的 `66582,67755` |
| 有原邊 u1v | 8 | A 的 `48617,67755` |
| 有原邊 u3w | 8 | B 的 `66602,67765` |
| 有原邊 u1w | 4 | B 的 `48647,67765` |
| 其餘target可用型 | 12 | 全部15欄 |

前28型的另一target及 separated stratum 必空，故各自是同一原來源上的
兩欄問題。四個附件類別互斥；外點接觸引理排除同一外點同接u1、u3，
字面target色又排除v、w兩側同時觸發。沒有把不同profile的X各自拼合。

## 4. 103正價欄的精確結構與補償缺口

[完整整數分解](compensation/REPORT.md)把既有13項 potential 按原 literal
palette word 分成七塊，對全部307,197欄逐項定價，得到

```
Z44459=Z44480<=Z44541<=Z784+Z37416+Z46468+Z66394。
```

103個正價欄恰為 `42+42+14+5` 四個完整 marked-phase stars；每個 star 的
所有未裁切 universal partition 選擇都仍存活。所有正價與負價分別位於不同
palette words，因此保持同一 palette 的 component flips 不能直接把正價
orbit 配到負價 orbit。

提議的加權補償不等式，在既有精確恆等式下等價於 `Z44459=0`。它仍須一條
新的原來源機制。另有直接弦迫零的限制：任何對44459 proper的可選原弦集，
也對輔助state66394 proper；故僅靠直接等色弦測試無法把上述四個輔助state
全殺掉。這不排除進一步 orbit closure、拓撲或最小性，也不證必要錐可行。

## 5. 任意 k 的模板秩與完整 Walsh support

[自足紙證](template/REPORT.md)證明：對任意 `k>=1`，取2k個交替 palette
contacts、兩個固定 anchors，並取所有非交叉同 palette `k+1`-block partitions
及其全部 block-flip cosets 所成的 universal local matrix B_k，則

```
rank_Q B_k=binom(2k-1,k-1)。
```

頻率補兩個 anchor bits，使每個 palette 的選點數為偶後，恰當選點 E/O 字
能用 `EE->empty, OO->empty` 約成空，它才在完整 Walsh support 中。
證明經過非交叉同 palette matching、互補區域的partition completion，以及
無窮路徑的 Pascal 回返計數。[獨立紙證審查](review/all-k-review.md)核對了
completion 的非空區域、anchor 雙射與遞推邊界。

標準函式庫 checker 重建六模板全部5,033欄，逐頻率比對原 Fourier support，
得1、3、10、35、126、462，並拒絕三個對照。任意 k 結論由紙證承擔；
有限相容性檢查沒有被當作歸納證明。

這是 **signed rational span** 定理，不能保證 X 非負、全域共享 Z 相容或
十個正量同時成立。它不提供新的 primal／dual 證書。

## 6. 驗證、停止點與下一個義務

每個子目錄的 checker 預設只讀。normal／seed17、完整重建與負控制結果，
以及文件檢查與 frozen-input drift，集中見 [verification.json](verification.json)。
本輪五組checker共10次正常／seed17重播均通過；正式docs檢查與docs範圍
DocGraph通過。全樹DocGraph仍因既有frozen／scratch重複ID而失敗（72項），
沒有把正式docs通過寫成全樹通過，亦未刪除歷史證據。
重播入口：

```
python3 -B audits/2026-10-21-w7-structural-30f2d19/geometry/check.py --controls
python3 -B audits/2026-10-21-w7-structural-30f2d19/review/target_exchange.py
python3 -B audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.py
python3 -B audits/2026-10-21-w7-structural-30f2d19/compensation/check.py
python3 -B audits/2026-10-21-w7-structural-30f2d19/template/check.py
```

本輪研究重心已移至原來源結構。下一步須在同一固定原附件與完整 components
下證新增的跨 palette 作用／最小性引理；先對無弦profile0與五個不同原外側
私有點，或已強迫 joined 的小類別動手，保原點身份、全部 lifts 與嚴格下降。
目前接續入口由 [Kempe導覽](../../docs/c5_kempe_guide.md)維護。

仍OPEN：嚴格W7來源排除、既有必要錐可行性、原來源實現、一般C7多內點、
type I／更長路、一般J1／J2、嚴格較小bad及主命題。沒有新Lean；沒有宣稱
既有線性必要條件不足。未commit或push。

L1核對更新Kempe導覽及STATUS。既有五邊路來源與計數封存只讀；State導覽、
HANDOFF及README不受子型排除或研究線變動影響，reviewed-unchanged。
Propagation stop：L1；本輪沒有W7 closure可上推父題。
