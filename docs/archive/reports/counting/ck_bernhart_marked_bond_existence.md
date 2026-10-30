# Bernhart 目標六葉：含標記二邊 bond 與來源非空性

2026-10-30 同日後續：[通用標記與唯一 lift](ck_bernhart_universal_marking.md)
證任一無標記 `n=μh` 來源自動有完整 y=μk，並可用固定構件乘 12 取得沒有含標記二邊 bond 的目標來源。
因此本題等價於無標記 h 來源類空；r₂ 的 free-edge 分支也取得到標記目標的正向化約。
下文保留前輪 diamond 結果及當時的驗收邊界；末節 free 分支義務由此後續補進。

2026-10-30，接續[標記六葉的條件式分離](ck_bernhart_marked_separation.md#3-指定-lift-對含-f-二邊割的實際限制)。
本頁負責「是否必有含 f 的二邊 bond」；既有完整二端分離契約仍由原報告負責。

**驗收尚未完成：未證目標來源為空，也未給出符合目標完整 lift 的實際反例。**
本輪證出一項適用全部大小與尺度的條件構造：任一目標來源都可經 diamond 二端插入，
變成完整 lift 乘二、仍有外面全染色雙閉圈標記、卻沒有含新標記二邊割的另一目標來源。
因此，本題的全稱 bond 存在命題其實**等價於目標來源類為空**。
這項等價尚未裁決哪一側成立，不能把條件構造當成完整目標反例。

## 1. 完整量詞與結論

令 T 為所有下列帶標記物件 `(Q, rotation, B, f)` 的類：Q 是有限連通 plane near-cubic
六葉網路，六葉以固定正序 B 位於同一指定外面，容許平行具名原邊；f 是該外面的原邊。
全部完整 Tait 染色的計數，包括零座標，滿足

\[
(y_Q,n_Q)=\mu(k,h),\qquad \mu\in6\mathbb Z_{>0},
\]

其中 k、h 是[固定 r₂ 的六葉降階](ck_bernhart_endpoint_ray_continuation.md#2-選定-r₂完整支援的全稱限制)。
每份完整染色中，含 f 色的兩個雙色系統，其含 f 分量都必須是完整閉圈。
兩條平行邊形成的二圈也計入。此處無頂點最小性或尺度最小性假設。

記 P 為「每個 T 中物件都有實際 bond `δ(U)={f,g}`」。本輪紙證給出

\[
\boxed{P\quad\Longleftrightarrow\quad T=\varnothing.}
\]

更具體地，若存在尺度 μ、v 個 cubic 頂點的 T 中物件，則存在尺度 2μ、v+4 個
cubic 頂點的 T 中物件，對其標記 m，**每個含 m 的實際邊割大小至少三**。
輸出物件的具名原邊、rotation、六葉次序和標記一次固定；所有染色使用同一輸出物件。

## 2. 同一個 diamond 的全部 extensions

取任一假定的 T 中來源，記 f=pq。正計數保證有完整染色；f 在閉圈上，故非 bridge，
Q−f 連通，且 p、q 為互異 cubic 頂點。

刪去 f，添四個新 cubic 頂點 a,b,c,d 及七條各有身份的邊

\[
pa,\quad bq,\quad ac,\quad ad,\quad bc,\quad bd,\quad cd.
\]

指定輸出標記 **m=ac**。以 a,b 為端點，內部是 `K₄−ab`，外四環為 a–c–b–d–a，
cd 為內對角線。

對此四頂點區域的 Klein-four flow 求和，兩條 stems pa、bq 必同色。固定共同色 x，
另兩色記 y,z，全部局部 extensions 恰為

\[
cd=x,\qquad ac=bd=y,\qquad ad=bc=z,
\]

以及互換 y,z 的另一份。證明可直接在 a 選另兩色的次序：cd 在 c、d 處須分別
異於 ac=y、ad=z，故 cd=x，再逐點唯一傳播。
這包含三種 x 的全部六份 extensions，沒有額外局部染色。

把原 f 的細 ribbon 中段換成此 diamond，a、b 分別朝 p、q。
選 a–c–b 為原 f 的外面一側，a–d–b 為另一側，cd 在四環內。
原頂點上 pa、bq 分別佔 f 原 dart 的位置，其餘原 rotation 不變；新點的 rotation
由這個局部嵌入固定。此局部替換保球面嵌入、連通性、六葉正序及同一外面，
且 m=ac 位於該外面。它適用於原 f 已有平行邊的情況，所有邊身份分別保留。

## 3. 完整 fibres、三個 signatures 及雙閉圈

對每份原完整染色 ψ，以 x=ψ(f) 分別回填上一節的兩份完整 extension，
其餘原邊色逐邊保留。反向把兩條同色 stems 換回 f，得到唯一 ψ。因此有逐份雙射

\[
F_{Q^\diamond}(u)\ \cong\ F_Q(u)\times\{0,1\}
\]

對全部 729 個 literal 六葉字 u 成立，包括空 fibres。這個二值記錄完整局部 extension，
沒有拼接不同原染色的端點邊際。

固定一份染色及任一雙色系統。若系統含 x，原 f 的單邊段分別換成

\[
p-a-c-d-b-q\quad\text{或}\quad p-a-d-c-b-q,
\]

都是五邊段，長度差四。其他 boundary 路保留，所有端點配對與路長奇偶不變。
若系統不含 x，diamond 中僅新增內四圈 a–c–b–d–a，不改任何 boundary 路。
故同一份染色的**三個完整 signed signatures 同時保留**，由完整 fibres 推得

\[
n_{Q^\diamond}=2n_Q,\qquad y_{Q^\diamond}=2y_Q.
\]

包括所有零座標，輸出正是 `2μ(k,h)`，而 `2μ∈6ℤ₊`。
這裡 y 使用原報告的完整染色／signature 計數語義，不使用普通未加權 PM 計數。

在上述局部 extension 中，m 色為 y。其 yz 分量就是內四圈；其 xy 分量則是
原含 f 的完整 xy 閉圈，將 f 換成五邊段後所得的完整閉圈。
互換 y,z 的另一份 extension 同理。故**每份輸出完整染色**的標記兩相關系統均為閉圈。

## 4. 含 m 的實際邊割至少三

由 Q−f 連通，選其中任一條 p–q 簡單原路 γ。輸出中 a、c 之間有三條邊互不重疊的路：

\[
ac,\qquad a-d-c,\qquad a-p\;\gamma\;q-b-c.
\]

任何實際邊割 δ(U) 若含 m=ac，便將 a、c 放在相反兩側，因此必各跨上述三條路至少一次。
三路邊集互不相交，故 `|δ(U)|≥3`。這已排除含 m 的二邊 bond，且未限制其他位置的割。

要區分「實際割」與「刪兩邊後不連通」：若另一邊 g 是遠處 bridge，
刪 m、g 仍會使整圖不連通，但不是實際割 `{m,g}`。三路論證保證刪 m、g 後，
m 的兩端 a、c 仍在同一分量；這才是本題需要的判據。

現在若 P 成立而 T 有任一物件，對其作上述替換，便得到另一 T 中物件，
其標記不在任何二邊 bond，與 P 矛盾。故 P 蘊含 T 空；反向由空類的全稱命題成立。
此證明使用了全部允許尺度對乘二封閉；不能用來裁決僅固定單一尺度或頂點最小的另一命題。

## 5. 有限重播及證據界線

第 1–4 節是一般紙面論證，不用四色定理、圖庫 oracle、有限大小枚舉或資源 limit。
Python 只核對局部六份 extensions 與一份具名非目標控制的完整替換。

- [checker](../../../../scripts/ck_bernhart_marked_bond_obstruction.py)
- [完整證書](../../../../audits/2026-10-30-bernhart-marked-bond-obstruction/verification.json)

```bash
python3 scripts/ck_bernhart_marked_bond_obstruction.py --check audits/2026-10-30-bernhart-marked-bond-obstruction/verification.json
```

控制以原 MC40 的具名原圖與 rotation 作輸入。它的完整 lift 不符合目標；乘二後也不符合。
本控制只核對一般構造，**沒有用 MC40 充當目標反例**。完整數字、檢查結果及檔案雜湊
見[收據](../../../../audits/2026-10-30-bernhart-marked-bond-obstruction/RECEIPT.json)。未新增 Lean。
大型證書依[既有封存規則](../../../../audits/README.md#新-checkout-的還原)保存原 bytes；新 checkout
先執行 `python3 tools/audit_archive.py restore --artifacts`，再執行上述 checker。

本輪 checker、正式 docs DocGraph 及 `git diff --check` 通過；封存與原證書逐 byte 相同。
全域文件連結檢查另有三項其他並行文件的缺失連結／索引錯誤，詳見收據及 docs.log；
全工作樹 DocGraph 仍有歷史快照的 72 項 duplicate-id。未把這兩項失敗報成通過。

## 6. 分開裁決與停止點

| 義務 | 本輪裁決 |
| --- | --- |
| diamond 的完整計數、平面、外面標記與無二邊割條件構造 | 一般紙證完成；適用全部輸入大小與 μ，輸出尺度 2μ |
| 任一目標來源必有含 f 的二邊 bond | **OPEN**；與目標來源類空等價 |
| 符合全部目標條件的完整反例 | **未提供**；仍缺任一實際目標來源作構造起點 |
| 既有「割若存在則有無葉側、可安全保標記分離」 | 保留原條件定理 |
| 一般無標記二端區域是否必存在 | **OPEN**；本構造本身有無葉二端插入區域 |
| r₂ 的全部實際來源排除 | **OPEN** |
| 原 76 列新增必零座標 | **0** |

本頁未將切 f 後的等色 sector 升格為完整八葉來源，未證異色新 fibres 空。
即使本標記目標類日後證空，r₂ 的 free-edge 分支及六葉無標記來源仍須另按原契約處理。
本輪沒有取得正的目標子類 bond 存在定理；新增結果是上述一般條件構造與等價命題。

文件閉包：前輪分離來源、4CT 導覽、任務二直接父報告及 STATUS 連入本頁；
一般來源排除未收尾，HANDOFF 的研究線標記不變。未 commit／push。
