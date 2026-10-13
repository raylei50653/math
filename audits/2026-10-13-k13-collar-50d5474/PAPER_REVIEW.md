# K13-COLLAR 紙面適用性覆核

固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`；檢查對象是
[PROOF](PROOF.md)。本檔由紙面子任務撰寫，是明列義務及推理的人工覆核，
不冒稱另有第二位作者完成獨立定理證明。完整程式獨立性見本包 REPORT。

| 義務 | 覆核結果 |
|---|---|
| 極小量詞 | 先在全部目錄外來源最小 k，再最大 E；反設與既有界共同給 k=13。 |
| 上游 degree | 原 B 完整≥4，全部原內點完整≥5；來源與上游全域最小性完全相同。 |
| h 上界 | Euler 重新推出 n5=6+h+Σ(d−6)，n5≤13 給 h≤7。 |
| h=3 使用範圍 | 只用既有 h=3⇒k≥14；未使用更長 C 無 chord 或 apex-H≥4。 |
| 原環帶 | 對每個具名合成，rotation 依序定義 y；面、附件、C 全部明定。 |
| chord 範圍 | 主有限域保留所有 chords；紙面排除先論證弦空側 ear，沒有假設它不存在。 |
| h=7 | 一個 I 點迫無弦，輪的所有 C 點 degree3，與 y≥4 矛盾。 |
| h=6 | 有弦 cell 樹兩個葉各為 hub degree≥5 的輪，迫至少六個 C-degree3 點。 |
| h=5 紙面子域 | 無弦時 h≤2|I|−2=4，故排除；有弦仍交有限分類。 |
| 小 cap 前提 | 紙面新排除不需 C4/C5 cap 加剪枝；保留上游必要性但不用於生成刪候選。 |
| sphere coning | 只在指定外面加 z；所有舊度數恰按一個明列公式改變。 |
| root 逆向 | 刪原 degree5 星，原 rotation 重建指定外 C5；所有鄰環 chord 保留。 |
| 內側第二路徑 | H 外 C 加 cone 得十四點 min4 sphere；每個 degree9–12 root 刪星恢復指定 C。 |
| 內側正式剪枝 | 只刪 I-degree<5 或超過五個 forced apices 的 roots；全部相容五點子集均重建原環帶。 |
| 內側與主域對齊 | 28 份內側 apex placements 都保存完整圖映射；兩域的 rooted 嵌入同構類集合相等。 |
| 外部生成範圍 | 使用三連通 min5 的完整類；未以五連通或僅插三度點取代。 |
| D5 | 同時搬運整圖／原 labels／全部染色；全部 degree5 roots 和十個順序覆蓋來源。 |
| 完整 Σ | 十個接受／拒絕列皆在同一完整 G 搜尋；最後直接對 K132。 |
| 結論邊界 | 有限證書全通過才採納 k≥14；不推一般 h≥4 或十四內點等式。 |

外部論文已直接讀取作者全文的定理敘述、Theorem 2 更正證明的來源鏈、
computer implementation 說明及十九點計數表。注意作者文本在 Theorem 3 後
的一段介紹對 (a)/(b) 有對調指代；本包只依定理本身與各段正式證明的內容，
不照該段指代把三環與四環類混淆。外部證明作依賴，未宣稱本輪重新證明。

紙面新 h=6 排除特別檢查的邊界情況：cell 樹可有空三角形中間節點，但
葉節點不能空；葉輪的附著 chord 端點可因其他 cells 得到更多度數，故只
計算端點以外至少三個點。兩個葉的這些非端點集合不交，五個 apices 的
計數矛盾有效。此證明不把兩葉的色列或 fibres 拼接成一份染色。

本覆核不代替實際編譯、枚舉、hash／embedding／四色重算、負控制、文件
檢查或 Lean build；這些實際執行結果及未執行項目由 REPORT／驗證紀錄承擔。

紙面子任務另以不匯入主 generator 的短程式直接解析 `spheres19.pc` 的
planar-code 鄰接 rotation 作算術校準：23 張 sphere、306 個 degree5 roots，
h=0,…,5 的 root 數依次為 5、24、98、134、41、4；沒有 h=6、7。
h=4 的 41 份中有 39 份 C 無弦、2 份一條弦；h=5 的 4 份均有兩條弦。
所有 root 均滿足 `|C|=5+h`。此校準與紙面排除相容，不充當生成完備性
或獨立四色證書；正式可重播版本以本包獨立 checker 為準。

後續覆核 `generation/inner_cover.py` 與其輸出，確認 degree3 的 C 點必為
apex 的必要性，以及列舉全部五點子集的充分覆蓋。十四點 min4 外部生成
使用的不是僅插三度點的族；其 octahedron 起點及 R4／R5／S 構造見作者
*Fast generation of planar graphs* §2。紙面來源自身的 cone／delete-root
互逆性給輸入域完備性，不由主程式成功匹配自己的輸出倒推。

`RESULTS.json` 的 306 份完整 masks 全為 1023，3,060 份接受 fibres、41,021
份 full lifts；獨立 normal／seed17 記錄同樣為 41,021，主—獨立逐份映射
核對已包含原 edges、degree、B、C、chords、faces 及每個 full lift。
