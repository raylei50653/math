# 剩餘0／1型的原外側私有面點：結構接續入口

2026-10-21；BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。

[來源紙證](PROOF.md)保留原完整嵌入、度數、附件、所有同源fibres及cap lifts，
得到兩型的新必要結構；**沒有排除這兩型**。

- profile0的五個原外側第三面點z1,…,z5都是不同D私有點；profile1只有四個，
  因唯一原弦au4迫完整n五度及原三角面a−n−u4，故 **z1=a**。
- 每個zi的C7接觸恰為其原路邊兩端，兩target中皆色03。相鄰zi有原邊，
  恰當它們的共同原ui五度；原完整外側link的額外鄰點始終保留。
- 兩target的完整原03分量分別有contacts `{a}`與`{q,v}`／`{q,w}`。
  未假定zi互鄰或全在同一個分量。
- 把完整原外側links接成a–q步道後，a/q的03分離迫至少一個額外私有鄰點
  為其中心的**相反12色**。profile1某ui或L度≥6；profile0則n≥7或某ui／L≥6。

[證書](certificate.json)與[checker](check.py)凍結八份原輸入，獨立核對兩型的
rim第三點候選、完整n star、原target03全部incidence及完整component flips，
並核對小型局部link色表。normal、seed17、`-O`結果相同；六內部負控及外部
五私有誤稱污染證書均拒絕。局部色表不觸發完整941來源，不作來源實現。

另已證完整支援接合引理：相同完整有序界面S、同一外側E及`R_S(H)=R_S(H')`
（含空列）迫原外框完整Σ相等。因此合法且嚴格較小的具體替代保Σ941即可
違反全域最小性；不要求著色計數相等。若要繼續沿用原同源計數模型，才需
另證相應full-fibre傳輸及全部cap lifts。

目前缺的是實際H'、該來源的R相等、合法性及嚴格下降；尚無這個具體替代。
profile0/1、一般W7、J1/J2、strict smaller bad及主命題仍OPEN。
沒有大型LP、廣泛實圖枚舉或新Lean。
