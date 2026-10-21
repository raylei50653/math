# W7 其餘原接線：十二型排十型，保留兩個完整來源缺口

2026-10-21；凍結 BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。
只寫本目錄，不修改舊證據與共享文件，沒有 commit／push。

在同一任意大小嚴格 only-R/W7 原來源與完整 D fibres 上，新增四條
原非邊結論：`u4v,u3s,u2v,u2w`。完整紙證見 [PROOF](PROOF.md)。
十二個原 full15 profiles 中，排除
`3,5,6,8,40,41,60,61,64,65`，留下必要型 `0,1`。

前三條原邊由完整實際分量 involutions 給長一或二的支配鏈；u2w 的 B
亦有兩步鏈，A 則由 89 節點的精確零 DAG 在深度三閉合。
[certificate.json](certificate.json) 保存所有字面 tuples、完整 incident
columns、逐欄已零 fibre、173 欄的全部 half-rows 與完整 component contacts。
[check.py](check.py) 從原 307,197 欄重掃全部 incidence，獨立重生所用各欄
的完整 flips，核對每一步和原邊同色終點。
[transport.json](transport.json) 另保存六個短鏈作用的原 palette、具名 root
與全部 incident columns；checker 逐型核對完整實際分量聯集的字面終點。

[closure.json.gz](closure.json.gz) 保存十二個固定原 profile 各自的全部零
步驟、欄零見證、完整 surviving states 與 columns。只讀 checker 另重新
算全十二型，要求與封存逐項相等。normal、seed17、seed17 加 `-O` 的完整
重播及六項破損負控制均通過，輸出見同目錄三份 `.log`。

兩個殘餘的完整原接觸均為 `S(u1)=RL,S(u2)=R,S(u3)=R,S(u4)=nR`，
1 型另有原 au4，等價原 n 五度；0 型 au4 不存在。必要閉包各有
`61,308/307,197` 與 `38,647/133,271` 個 states／columns，兩 target 皆保留。
0 型的五條路邊外側各有不同原私有第三面點；1 型由 au4 固定 n-u4
外側第三點為 a，其餘四條路邊仍各有不同原私有第三面點。

這些必要支援**沒有證成共同計數可行或同一原圖實現**。它們表明現有
完整零傳播對兩型尚無出口；來源縮減仍須保留這些私有點、原 rotation、
完整空 fibres 與全部 cap lifts。精確殘餘見 [RESIDUAL](RESIDUAL.json)。
一般 W7／J1／J2、較小 bad、主命題仍 OPEN；沒有 LP、新來源枚舉或新 Lean。
