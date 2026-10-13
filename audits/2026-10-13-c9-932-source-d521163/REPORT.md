# T2｜C9-932-SOURCE：原 apex 低度排除

在 [固定來源契約](SOURCE_CONTRACT.md) 下，本輪證明

\[
\boxed{\Sigma(G)=932,\ h=4\quad\Longrightarrow\quad
d_H(a_i)\ge4,\quad d_G(a_i)\ge6\quad(i=0,\ldots,4).}
\]

這是對全部20份原具名殘留、任意有限內側大小的條件式來源定理。
100份「原配置＋原 apex 的 H-degree=3」假設全部有精確排除證書。
進一步由原小cap限制得到九條C9原邊的內側面第三點互異，故

\[
\boxed{\Sigma(G)=932,\ h=4\quad\Longrightarrow\quad
|V(H)\setminus C9|\ge9,\qquad k\ge18.}
\]

第二個結論中的 k 是原 B 內點數，包含C9九點。兩項結論均不使用四色定理，
也不借用C8的 apex 結論、274維介面或八項來源身份。

## 原圖身份與共同計數

研究 BASE 為 `d5211633ba80c2b10cb12eaa8189421e35a31cc3`；
[INPUTS](INPUTS.json) 凍結上游 frontier 完整包，並記錄逐檔SHA256。
G 先在全部目錄外 disk-C5 圖中最小化內點數，再最大化邊数。
固定同一原 B、五個 apex、四個私人點、原 annulus、原 rotation 和完整932。
不是在固定mask中另取最小來源。

20項按整圖D5分成三組：

| 原超額配置 | 具名份數 | 上游必要支援大小 | 低度 apex 排除數 |
| --- | ---: | ---: | ---: |
| 兩個不相鄰的2 | 5 | 376 | 25 |
| 連續正項1,2,1 | 5 | 352 | 25 |
| 連續正項2,1,1，含反射1,1,2 | 10 | 356 | 50 |

[身份表](SOURCE_CONTRACT.md)列出全部query、原C9順序與附件規則。
[獨立覆核](review/REVIEW.md)檢查200份整圖D5搬運：原B/A/Y名字、原邊、
有向面、rotation、820份內列、十份外列、全部 annulus full lifts及空fibres
一起搬運。全部100份假設仍逐份直接計算，不靠對稱猜測排除。

令 x_p 是同一H對固定literal C9列p的完整延伸數，p遍歷820個共同S4代表。
原annulus完整計數矩陣T由實際具名邊重新枚舉，原外框計數為 y=Tx。
932要求外列2、5、7、8、9為正，其餘為零；上游必要支援U外的x亦為零。
232份合法非交叉商圖正性仍作用在這份x上，點數為k−9+q≤k，
其可染性來自固定來源的相對大小界N≤k+5。

同一H也滿足C9非交叉等式向量的有號展開x=Ec。
本輪的低度矛盾已在下述較小的必要條件子系統中成立，無需解此線性展開、
移植C8矩陣或使用數值最佳化。詳細定義見[計數證明](counts/PAPER.md)。

## 新局部限制與精確排除

假設原apex a 有H-degree=3，記原C9鄰點u、v。原C9無弦及原三角化迫使
它唯一的其他鄰點t位於嚴格內側，原面恰含uat與avt，且tu、tv是原邊。
[原圖幾何證明](geometry/PROOF.md)逐項核對此局部以及刪點、補邊、
外側識別的平面性、無loop、接點映射及頂點預算；排除本身只需要原H與H−a。

固定H−a全部邊界色，且u、v同色c。其餘三色為i、j、l，令z_d計數t色為d
的完整H−a染色。逐份保留H−a的整份染色，只補回原a，得到

\[
x_i=z_j+z_l,\qquad x_j=z_i+z_l,\qquad x_l=z_i+z_j,
\qquad 2x_d\le x_i+x_j+x_l.
\]

此處三個x代表原C9三份完整列，不是另選的來源或邊際。
重新枚舉每個原C9位置得91份三項限制，完整保存重數。
如果一個三項式只有一個座標仍可非零且只出現一次，該座標也必為零。

將這個新零列規則與原C9三份互補色對的完整Kempe規則交替使用：
若一列某個split的每份非交叉component選项都有已為零的列，該列必為零。
真實完整染色必提供一份實際component partition，其所有獨立交換仍是
同一H的完整染色，所以每步刪除都保留所有真實支援。

[精確證書](counts/certificate.json.gz)保存全部100項的每一步支援、
D3三項見證及每份Kempe orbit的缺失列。全部100項的最後支援都是空集，
因此所有x=0，與任一必要接受外列的Tx>0矛盾；也與同一H的商圖正性矛盾。
這不是從浮點不可行狀態或未觸發來源控制推論排除。

## 原面推論與停止點

度數提升後，原C9每點H-degree至少四。若某嚴格內點t同時接原C9距離二
的兩點，短側原C4 cap必空，無弦迫其中間圈點H-degree三。
距離三則形成原C5 cap；空cap必是t-fan，非空cap只能是原W5，
兩者都迫短弧中間圈點H-degree三。故這兩種距離均不可能。

九條原C9邊的面第三點均在嚴格內側。任意兩條不同C9邊的端點中，
必有一對圓周距離二或三，故它們不能共用第三點。由此得到m≥9、k≥18。
完整任意大小證明及有限位置核對在[geometry](geometry/PROOF.md)。

本輪排除100份低度假設，**沒有排除20項在較高度數下的完整來源**。
20份上游支援仍只是必要上界；沒有提供或宣稱新來源圖、完整可行计數向量。
下一個同圖義務是把apex≥4、九個互異原面第三點、全部完整計數與
實際內側接線共同實現或排除；尤其距離四的原接點與同一內點的多接點限制
仍須保留，不能用分列自選的component資料代替。

繼承的932五度內點下界n5≥10不提高。一般932排除、h≥5、933／941、
K∞=K≤5及一般主命題均保持OPEN；沒有新增Lean形式化。
本輪不修改共享導覽、舊證書或其他工作者輸出，未commit／push。

## 獨立重播

```bash
python3 -B audits/2026-10-13-c9-932-source-d521163/verify.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c9-932-source-d521163/verify.py --check --negative
```

主checker使用Python標準庫重建820列、所有D3式、完整T及商圖mask。
獨立checker另從21,147份Bell partitions重建全部C9 Kempe options，
逐項檢查原表及新證書，並核對完整D5搬運。
正常、seed17、語義負控制及frozen-input drift结果見[VERIFICATION](VERIFICATION.json)。
