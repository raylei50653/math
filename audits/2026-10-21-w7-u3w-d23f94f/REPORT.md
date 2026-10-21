# 原 u3w 的八型：完整來源已排除

2026-10-21；exclusive BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。

原 941/J1 strict only-R/W7 契約下，任意大小來源若含原邊 **u3w**，
則 `Z44459=Z44466=0`，矛盾於原 witness 的 `Z44459+Z44466>0`。
原 `X66602=X67765=0`；profiles **16,17,46,47,62,63,66,67** 全部排除。
各 profile 的全部原弦保存在 [certificate.json](certificate.json)，不以一條邊取代完整來源。

[紙面證明](PROOF.md)先整理原 B44466 的字面作用，再建立四態分支證明：

1. `Z49643=Z60707=0`：各自一份完整 half-family 的七欄全部經實際完整分量作用撞原 u3w。
2. `Z49955=0`：完整五欄全部送至上述兩個空 fibres。
3. `Z44466=0`：完整十欄中的八欄直接撞原邊；66602、67765 都送至49955。

證明共四個 derived states、29個完整 incident columns。每欄均保留全部 rows、
完整 boundary components、實際 whole-component 作用和字面輸出；
所有原 private points、空 fibres、原 caps 的全部 lifts 均保留於同一原核心量詞。
未使用圖對稱、v/w頂點互換、u3v/u1v新增零值或先前 closure transcript。

原 B 的03|12唯一欄是306993，其12-component的contacts是`{c,s,v}`。
所以把A證明的v/w對換會漏掉v，不能得到合法完整分量作用。
本證重新讀取未加弦的原307,197欄family，而不採這個錯誤捷徑。

[checker](check.py)在normal、seed17、seed17加`-O`三次唯讀重播完全一致；
七種內部破損證明均拒絕，外部漏欄污染證書以exit1拒絕，結果見[runs](runs/normal.log)。
[BASE custody](runs/base-custody.json)另確認HEAD等於凍結BASE，五份authority輸入
均與Git BASE原bytes相同，drift=0。

本項只排含原u3w的八型；一般W7、未加弦的原必要計數錐、一般J1/J2、
strict smaller bad、主命題及Lean仍OPEN。沒有大型LP、新實圖枚舉或新Lean。
未生成實際來源控制圖；本項為完整契約的條件排除定理。
