# C8 apex 度數縮減：四十份條件來源排除

2026-10-13。BASE `45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。
本輪只作本地研究、證明、程式與驗證；沒有 commit、push 或對外發布。
開始封裝時有同輪 W5 rank3 的並行產物；不宣稱工作樹乾淨。

**新結論：h=3 的每份最小來源，五個原 apex 的完整度數都至少六；因此
h=3 的來源至少有十四個原內點。** 此前上游只給一般十三內點下界。

C8-STRUCT 留下八份完整具名來源契約。本輪逐項排除「指定 apex 在 H
度數三」的全部 8×5=40 個子域，對任意大小來源成立。沒有把八份查詢中
任何一份整項排除；70 項仍為 62 排除、8 殘留，h≥3、全域 n5≥9 不變。

[紙面證明](PROOF.md) 引入一個局部完整延伸計數引理：若 apex a 在 H 中
只有三個鄰點，固定另七個 C8 點且 a 的兩個環鄰點同色，a 可取的三個色值
之完整延伸數必滿足三角不等式。此式固定同一圖、同一 t、同一 literal
外部染色，canonical 化保留重複索引的重數。

其中 38 份用新的迫零規則與既有完整可逆 Kempe 軌道支援閉包即矛盾；
另外 c04-941/a1、c07-941/a4 各有獨立精確有理分離證書，迫原接受列
`01232` 計數為零。這些結論使用來源必要上界，不把任何儲存正向量
當作實際完整關係。共同 equality 展開係數仍可有符號。

證書集中在 [certificate.json](certificate.json)、
[第一份精確 dual](dual-c04-a1.json)、[第二份精確 dual](dual-c07-a4.json)。
[check.py](check.py) 使用標準庫 Fraction 驗證所有 91 座標恆等式與軌道
非負性，並从原具名附件及全部 literal lifts 獨立重建 8×10×274 個
transfer 係數；不用 SciPy 的可行／不可行狀態作驗收。

來源、無內弦、計數空間及軌道定理均沿用 C8-STRUCT 的 frozen 文件與
已驗證證書。本輪七份依賴逐一從 exact BASE Git object 驗證；
[BASE.json](BASE.json) 保存 SHA256、大小、來源與 frozen 路徑。
舊 generated interface 的 Git-blob 核對失敗另存
[discovery_failure_01.txt](discovery_failure_01.txt)；新 checker 完全移除
該生成檔依賴，改從完整原邊重建 transfer。沒有修改任何上游證據。

[controls.json](controls.json) 分別記錄 W8 的 732 份 literal 校準
（triggered and holds）、把 degree3 弱化為 degree4 時的明列完整染色
反例（counterexample），與三項證書破壞控制。實際最小目標來源構造
為 not triggered；未用零構造樣本宣稱排除。

本輪沒有新增 Lean theorem。h≥4 的十三內點来源仍 OPEN，沒有證明
K≤13=K≤5 或 K∞=K≤5。新的精確停止點是：h=3 的同一 induced-C8 H 必有
五個 H 度數至少四的 apex、三個 H 度數至少四的 y，以及至少六個嚴格
內側五度點，仍須同時實現完整原 Σ、附件、原面與跨 splits 的共同交換。

重播與控制見 [VERIFICATION.md](VERIFICATION.md)。
