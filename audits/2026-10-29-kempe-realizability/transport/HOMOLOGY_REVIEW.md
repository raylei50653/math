# 五步回返的短週期同調證書：獨立稽核

2026-10-29。獨立檢視 [c5_blocked_history_homology.py](../../../scripts/c5_blocked_history_homology.py)
與 [history-cocycles.json](../history-cocycles.json)，並實際執行 `--check`。
本稽核不修改產生器或證書，也不以矩陣秩輸出代替直接核對 cocycle。

## 核對的命題

令 O 為外框同一有序 C5、全部內面為三角形的 plane disk。
令 K 為完全封鎖五度星延拓的非空完整 Kempe 分量。
沿 [五步傳輸證明](PROOF.md) 定義 X_b 與完整回返雙射 H。
若存在 c∈X_b 滿足 H^k(c)=c，則五個 boundary histories 構成的邊鏈
必在相容歷史複形內界出一個 mod-2 三角形鏈。
給定證書對 k=1、2、3 分別提供一個在每個三角形上總和為 0、
在此 boundary 邊鏈上總和為 1 的 cocycle，因此這三種週期全部不可能。

## 逐項核對

1. **完整中間正規化。** 每輪依 AD、BD、BC、AC、AD 五個色對交換實際完整 component，
   其後對**所有原頂點**施行同一 σ⁻¹。產生器在下一輪之前確實為每個頂點附上正規化後的色。
   因為它是共同雙射，正規化前後的每條原邊都保持 proper；
   這項操作不能只施行在框上。第 k 輪末只要驗 σ⁻¹(末色)=初色即可，
   不必額外保存末次正規化欄：對全部頂點的完整 H^k 回返條件恰是這個等式。

2. **窮盡方向正確。** `histories(k)` 允許每個原頂點在其顏色屬於當步色對時獨立選擇換或不換。
   它忽略 component 連通與原邊身份，是對真實頂點歷史的必要鬆弛。
   這個放寬只可能增添相容頂點／邊／三角形，仍可用其上 cocycle 排除真實來源。

3. **相容圖與非退化三角形。** 兩歷史相容當且僅當每個保存時刻皆異色。
   O 的每條原邊必投影到相容圖的一條邊。
   O 每個三角面的三個端點在初始完整著色中兩兩異色，故它們的完整歷史也兩兩不同；
   所以面不會退化為一條邊或一個點，恰投影到 checker 列舉的一個三角形。
   不需假設歷史映射在全部原頂點上單射。

4. **逐面鏈的推出。** 在 F2 上相加 O 的全部內三角面。
   每條非框原邊有兩個 incident 內面，故其係數為 0；每條框邊只有一個，故其係數為 1。
   在歷史映射下逐原面、逐原邊線性推出這個等式，即得到相容三角形鏈的邊界恰為五條框歷史邊。
   即使不同原面或原邊投影到同一目標單形，它們仍按 F2 係數相加，邊界算子依舊可交換。
   因此 separating triangles、重複的歷史類或投影碰撞不形成缺口。

5. **框鏈精確一致。** 每輪的 X_b 起終框色固定，故五個框頂點的歷史是同一份六色時序重複 k 次。
   `BOUNDARY` 五列的串接與產生器每輪插入正規化的格式一致。
   五個 boundary history vertices 相異，五條 cycle edges 也相異。
   證書所驗的 boundary 邊鏈恰是第 4 項推出的鏈，沒有改換環序或獨立來源。

6. **直接 cocycle 矛盾。** `--check` 重新列舉歷史、相容邊與所有三角形，
   不信任產生時的消元過程。它直接核對每個目標三角形三邊的標記和皆為 0，
   框五邊標記和卻為 1。對第 4 項三角形鏈求值必為 0，對其同一邊界求值卻為 1，矛盾。
   `triangle_rank` 是生成統計，不是上述直接證書所需的前提。

## 結論與排除力的範圍

H 是有限非空 X_b 上的置換；其每個 orbit 長度至少 4，故 |X_b|≥4。
由五個完整可逆傳輸，五型每個固定字面框色的延伸數皆為相同 m，因此 m≥4。
這項結論控制完整回返作用，強於只證五型全支援或五型等量。

具名必要資料候選 THIN-932(m)，m=1、2、3，指定五個四色情形的每份字面框色 fibre
皆恰有 m 份、三色情形皆空。其 support 932 仍通過 D；
既有 t 計數資料的正整數倍亦通過齊次 classwise／B5 必要等式。
本證書排除這三份薄 fibre 候選在三角化 disk 中的同一來源實現。
其中 m=1 的全部120態抽象交換模型已在獨立 [return-certificate.json](return-certificate.json)
完整列出；m=2、3 在此只指必要資料候選，不另外宣稱已構造具備全部真實 component 性質的 connected cover。

**限制：** support 932 完全未被新條件排除。m≥4、H 的較長週期、任意封鎖分量不存在，
以及允許局部結構族的全量詞命題仍 OPEN。這不是任意大小 Kempe 逃逸的證明。

## 實際重播

```text
python3 scripts/c5_blocked_history_homology.py --check
PASS:
k=1: histories=6, edges=5, triangles=0, boundary cocycle=1
k=2: histories=46, edges=195, triangles=200, boundary cocycle=1
k=3: histories=309, edges=3611, triangles=5324, boundary cocycle=1
```

證據層：短週期到逐面鏈的推出為上述紙面論證；cocycle 是精確 F2 Python 證書；
沒有新增 Lean，也沒有使用四色定理。
