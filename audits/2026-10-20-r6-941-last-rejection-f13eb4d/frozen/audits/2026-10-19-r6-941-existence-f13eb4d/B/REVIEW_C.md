# B 對 C 的獨立交叉審查

審查對象為 [C/PROOF.md](../C/PROOF.md)、[compare.py](../C/compare.py)、
[acceptance.py](../C/acceptance.py)，逐檔SHA記於
[review-c-inputs.json](review-c-inputs.json)。結論：兩張具名新圖的合法性、
同來源固定字面計數、接受注入及條件支持排除均通過；沒有發現需修正的
數學缺口。此審查不把剩餘支持型當作實圖實現。

1. 原實際六角洞 `(a,b,q,L,R,n)` 的三條新增弧 aL、aR、bL 不交叉；
   對應四個三角片恰為 abL、bqL、aLR、aRn。所有弦的原非邊性由
   induced C10 及原 b 完整 star 給出。J2 保留整個原框、完成 k−2。
   在同一已畫好的洞內收縮 bL 得 J1；aL 變成 ab 平行 copy，可保留
   原框 ab。bq/Lq 的重邊只圍原新三角片，抑制不失私有點。只有一個
   原框點參與收縮，框五點仍互異，完成 k−3。
2. J1 的全部左條件確為 `b=L,a!=R`；J2 為 `a!=L,a!=R,b!=L`，另有
   共同 `b outside {a,c,q}`。我沒有重用C的C8→C10矩陣推導；另以
   全部2461個C10代表逐份枚舉 `(b,x,y,r)`，保持所有右cap附件，按
   `(4-d)!` 正規化，得到的兩份十列矩陣與C逐係數完全相等。
3. 接受零分支匹配正確：a1=0迫同一d_a完整著色 `R=3,L=1`，供J1；
   a2=0迫 `R=2,L=3`，供J2。該R、L結論先由固定xy=(2,3) lift
   取得，但R、L本在同一D_old中，所以另一xy lift也保留它們。
   兩份歸一化後的原q分別是0、1，故兩個像不交；q沒有被新商識別。
   由q逆置換、J1反拉b=L、恢復固定h色，即恢復全部D_old私人顏色。
   因此 `N_alpha(Ji)>=2*d_a>0` 的因子2有效；沒有再把v,w次序乘二。
4. 兩候選都沿原 `(x,y,a,b,c)` 計數。935、942、943的原bit4及bit6
   皆零、bit1及bit9皆正。因此 `a1=0` 下J1三個必要支持及 `a2=0`
   下J2恰943，確實將同一新候選收窄至只剩原01021拒絕列。
   完整全域最小性只用於合法較小J的支持落K132；沒有假設新J仍r6
   或具原來源度數，也沒有移用另一張候選的接受。

唯讀重播已通過：

```
python3 -B audits/2026-10-19-r6-941-existence-f13eb4d/C/acceptance.py
python3 -B audits/2026-10-19-r6-941-existence-f13eb4d/C/compare.py
python3 -B audits/2026-10-19-r6-941-existence-f13eb4d/B/review_c.py
```

compare 重建的未排除支持恰為C表列9個／6個，結合接受注入後是3個／1個。
[review-c.json](review-c.json)記獨立完整cap核對。這仍未證剩餘01021為零；
沒有把舊接受零控制被新最小性排除，提升成所有真來源接受零分支被排除。
