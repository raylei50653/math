# 一 long canonical 整合稿的獨立核對

2026-10-13。審閱對象：`docs/c5_excess_two_n2_one_long_closure.md` 全文。
結論：**採納定理 OL 的完整 `(1,0)` 來源排除**。主證明無數學或量詞阻塞。
一項範圍表述需修正：OL-F 的貪婪引理本身不依賴另一份 mixed 是 short；
兩 long 分支仍 OPEN 的原因是缺少短分量的全色 diagonal 入口 OL-C，不能
把 OL-F 自身說成僅能用於 short。父作者已告知會作此更正。

## 核對結果

1. **完整契約。** 原 complete Sigma933／941、T4、criticality、原55 degrees、
   nonadjacent roots、兩 mixed、u=0、one-sided/full B-touch 保留。本文明確
   沿用已採納來源定理取得 cactus、leaf private contacts、spoke cap、附件
   單射；沒有聲稱任意三列拒絕圖都滿足這些性質。
2. **OL-C。** 同一原 contact 的 owner／框鄰碰色產生一個 strict-list 點，
   原 L spanning tree 給全部 L lift；S 同一列、同一 pins 的 N-diagonal
   給完整 joint。聯集 W 僅尋找實際碰色點，未取代 attachments 或 fibres。
3. **具名閉包。** signatures `000,111,220,102,221` 正確。新增2恰需原0、4；
   新增4恰需原1、2。公式不作迭代，兩個新增不能同時出現在 `cl(T)-T`。
   該公式對全部32份 T 成立，不把高接點 L 壓縮為 Eq/Diff。
4. **單 block 排除。** 無 shared 且 incidence 至少四排 singleton／bridge。
   單 cycle 的同列 palette 在一個 contact 排除 D，迫所有點 contacts；
   三列同 palette 指每一列中所有私有 lists 相同，並非三列 palette 色集
   彼此相同。由此各框附件 signatures 相同，actual support singleton，違 long。
5. **末端 cycle 的加強 minor。** 整合稿從 `N_B(R)` 取 a，其中
   `R={r,s} union S`；S 支援非空保 a 存在，故比本人草稿只取 spoke 更強。
   若 a=h，五 bags 全連通且十對鄰接；剩餘 root-contact 由 k_L>=4 保證。
   若 a!=h，long 给 b!=a,h。原 a-h 弧 P 不經 b，補弧 Q 經 b；移去 h
   及 Q 中 a 後，兩個框頂點集互斥。第四袋由原 R-a 邊接通，第五袋由
   原 L'-b 邊接通；Q 在 a 的首邊提供第四、第五袋相鄰。這條邊確實存在，
   因 b 位於 Q 內部。p,q 各由原 root、h-附件、剩餘cycle邊接另三袋。
   任意奇 cycle 均有相鄰私有 p,q，刪兩點保剩餘 L 連通；沒有 triangle 假设。
6. **末端 bridge minor。** p 的 H 內度二及框附件邊由無 shared／完整degree4
   得到。若附件兩端都在 T，R-a、R-b 為實際 spokes，long 保剩餘 L 有 ab 外
   框附件，故 F 連通；十對相鄰完整。原 K5 只作平面矛盾，不移植 Sigma。
7. **中間分類。** 多 block 的 block-cut tree 至少兩 leaves；所有leaf bridges
   各用一條 incident exceptional h 的不同框邊，故恰兩份。閉包新增條件
   加兩鄰點迫 T=B-h。每 root 最多兩相鄰 spokes，使 t=4，兩 spoke edges
   為原 B-h path 的唯一 perfect matching。degree 等式逐側迫 L為2+2、
   S為1+1 incidences，沒有忽略 shared S 的可能。
8. **OL-F。** 固定 r=a 後，原 S+s 連通；S點 list size 至少其原內度，s 有
   strict slack。s 的 L 邊已隨刪 L 移去，不能再把其 L contacts 的色列為
   已染外鄰。整合稿正確只禁原spokes，rs亦不存在。貪婪構造的是真實完整
   外部 lift，沒有以 s marginal 取代外部 tuple。
9. **最後同列矛盾。** 兩側 L incidence 都二，OL-F 兩側適用；01、23、34
   都是自身的三列閉包。每個leaf附件邊不包含於任一owner spoke邊，所以
   存在同一拒絕 q_i 及合法owner色 a，先取完整外側，再原contact碰色補 L。
   最終 tuple 保原框及另一root真實pin，全原邊均滿足。沒有跨列拼接。
10. **證據界線。** 主證明不使用有限大小下界、來源枚舉或內部圖形窮盡。
    四／五點分割、全部十列pins與完整tuple校準是另一證據層；本審閱不替代
    checker 的實際重播。兩long、父N2、E-ARC2及契約外域保持OPEN。

## 表述建議

§3 的「三列 palette 相同」可改成「每一指定列中，全部私有點有同一個 cycle
palette」以避誤讀成不同列 palette 色集相等；主證明按後者正確解讀。
§7 最後一句應指出 **OL-C／永久 diagonal 入口依賴 short 的全色 diagonal**，
而 OL-F 自身可對任何另一份 mixed 使用，只要所有列出的 degree／incidence
及無 U 前提仍成立。

沒有修改共享 docs 或任何舊證據。主 theorem 可在上述精確來源內採納。
