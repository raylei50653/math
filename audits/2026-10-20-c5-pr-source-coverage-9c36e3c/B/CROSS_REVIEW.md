# B 交叉審核：C 幾何、A 計數反例與主報告

2026-10-20，BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。
本審核只寫 B，不修改 A、C 或主報告。

## C：PASS，限所列來源合同

已讀 C/check_geometry.py、C/REPORT.md、frozen full-graph checker 的
disk/link 驗證與完整枚舉器，並只讀重播 C 證書。

- 逆 P 的判準需要**實際兩個三角內面**及第三鄰點是**目前框內點**，
  僅度三不夠。這些條件合起來確實給可移除的兩三角 collar；
  刪新增框點後，第三鄰點成為新框點，仍有五個相異框點。
  四邊形 cap 與框上第三鄰點負控制各針對一個必要條件。
- checker 的 inverse-P/I predicates 是在已驗證 oriented disk cellulation
  上使用；它不是任意未驗嵌入輸入的 topology oracle。
  六個有限真圖的驗證域足以承擔其宣稱的有限控制，沒有冒充整個一般圖域枚舉。
- 逆 I 的三角星刪除保同一目前框，restriction 逐份保留全圖染色，
  injectivity、surjectivity 與空 fibres 均有逐列檢查。
  五個剝除前後的頂點重標號有明示映射，沒有把獨立正規化的邊界混接。
- \(\mathcal G_{PRI}\) 的來源定理成立。I 點永遠是內點，
  P 只接目前框，不可能在後續把新邊接到 I 點；
  後續 I 可按反插入次序刪除，恢復先前的三角星。
  因此從最終來源按此順序 restriction 到刪 I 後的純 P/R 圖，
  是合法的完整 fibre 雙射；不是只憑支援相同猜雙射。
  只用逐步計數同步也能證較弱的同計數結論。
- `W5=FP` 的接線正確：原 fan 的首框點在 P 後成為五輪 hub。
  五面插點後框度五，排除純 P/R 生成；每個非種子的純 P/R 圖
  在最後 P 後必仍有一個度三框點。
- punctured icosahedron 的明列有向面、degree 與 `(2,...,2)` fibres
  都經 checker 重播。框度四、內度五排除任何第一步逆 P/I。
  它也不在 PRI 生成族：任何非種子的 PRI 字，最後非 R 步若為 P，
  留度三框點；若為 I，留度三內點。後續 R 不能改變度數。
  這不妨礙它由 C 代表**支援**，亦沒有證明其不具其他**計數**代表。

只讀命令：

```bash
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/C/check_geometry.py --check
```

exit 0，輸出 PASS：6 張初始真圖、60 個完整 canonical fibres、
18 個空 fibres、57 份完整染色、5 次 inverse-I fibre 雙射、
4 次 inverse-P roundtrip、4 個非法操作拒絕。

本次重播時 SHA256：

| 檔案 | SHA256 |
| --- | --- |
| C/check_geometry.py | `ba8b1e9b06dbe33851f3148f5f5256292b39b69681af0dd20bb1a3c9c6d0a145` |
| C/REPORT.md | `ac23398914e5a3d13390aa7532a7203ff5089e44ddbfd9d594ca3f6aa92a3044` |
| C/geometry_certificate.json | `d8a1e012c67a6e553b92ae7a49c2aa578459980922e543868b62239969539d09` |

## A 與 root 整數反解：PASS

A 的內部葉點例是一般 disk 域合法真圖，每個固定字面框色恰三份完整延伸。
「取最後 P」論證排除所有大小的 F/C 文法計數代表，而非只排除 C：
常向量 `(3,...,3)` 在 R 下不變；最後 P 輸出座標1、3、8之和必偶，
卻應等於9。無 P 的兩種種子及旋轉亦非該計數向量。
將這個一般域反例限制在允許葉點的合同內是正確的。

root 的 P 整數反解與 B 的 Boolean 四前像敘述沒有矛盾：
整數資料記錄了三個 pair sums，可唯一反解，支援只記錄其正值，
才會把 at-least-two 四種原三 bit 壓成同一像。

以下兩個只讀命令皆 exit 0：

```bash
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/A/check_contract.py --check
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/check_integer_inverse.py --check
```

A 輸出 `PASS: complete leaf fibres, last-P parity obstruction, saved catalogue identity`。
root 輸出 `determinant=-2, support_images=640, preimage_histogram={1:512,4:128}`。
此處沒有額外證明 bounded catalogue 完備性。

## 主報告 §3、固定 collar 與來源邊界：PASS

主報告的933／941「含 P 當且僅當終態入 K」正確限於十個指定有序 masks；
932 的六個 K 外態、P 自環與 `PRP^t` 負控制亦正確。
一般非空支援至多4個 P 的 pointwise bound 有 witness 與全邊成本不等式，
固定共同字串

```text
W = RRR(PPR)^4P(PRP)^4
```

則有28字母、17次 P，對所有非空 masks 終態均為1023。
這兩種量詞要分開；後者不聲稱17最少。
兩個字母保存聯集，十 singleton 軌跡已給全域證明，
補充 checker 又直接核對1023個非空 masks。

實圖推論保留了前提「原來源完整支援非空」，
P 增加內點並改目前框，所以外補完成不是原來源覆蓋，也不是 smaller-bad。
0 在所有字串下仍為0；不得由這個 collar 補出未證的非空性。

主報告 §5 的 ico 非生成族判定可用上面最後非 R 步的論證；
可剝 PRI 子類保完整 fibres，然後再取≤5代表的步驟僅保支援，
兩種保留量不得合併。已將一項文字建議傳給 root：
若主報告只採同步計數證明，無須否定 C 的合法反序刪 I restriction 構造。
