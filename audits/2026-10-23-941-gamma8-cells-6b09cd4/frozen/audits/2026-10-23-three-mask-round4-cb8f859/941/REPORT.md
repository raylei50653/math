# 941第四輪：T的原02分枝與私有Q插入橋二分

2026-10-23；BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

**新增同一來源的分枝必要二分，未排03／02配對。** 在普通短型I、02型13／36，
取第三輪同一原01路的指定最後C橋點T∈Q。令J為原完整02／13分量樹，K為
完整U02分量；刪去K後，含B13(V,Y,q,c)的支記為J_B。

原框除U外是一條避K的連通路，故全部碰框分量均在J_B，其餘支皆rootless。
若T的原02分量M不在J_B，同一T→c尾路必重返K0，但已不回後繼C。沿同一
完整K的U→該返回點原02路，可指定最後C橋點

```text
u⁻0∈K∩C — Z2∈K∩Q — u⁺0∈K\C。
```

Z必私有。其全部原色0鄰點都在K、全部原色3鄰點都在同一完整Q；完整link
迫至少兩個原色0及兩個原色3鄰點，五度時恰`{0,0,1,3,3}`。唯一原色1鄰點
落在C／C外兩側都保留，無色1的偶數度至少六及其他高階亦保留。若M在J_B，
仍不能認M=L，也不排除Z存在。這是「不在B側便迫Z」的條件式，沒有聲稱
兩支皆已排，亦未說任取K2∩Q點都有標記鄰點。完整論證見[PROOF](PROOF.md)。

再需初始03型4及M不在J_B時，前輪X∈B13∩A與本輪T、Z共同成三個相異
F私有點，XT、XZ、TZ皆是原非邊。同一B13路的R仍在C；R與u⁻、s不同，
是否R=r或與r相鄰尚未知。此處Z的路鄰u⁻／u⁺均非原框literal v；
03型9不套X／R／三私點結論。

同一原01路最後K0出口之後的色1點b可證在完整B13，但其實際後繼12分量
E'不能自動當C。新增八點真三角化disk反控制保K的框接點恰{U}，卻有原K0
交換後落在C外，直接拒絕這個補連通推論。該圖不是完整941來源，來源控制
為`not triggered`；沒有來源disk搜尋或新增有限生存控制。

[certificate](certificate.json)承接第三輪四列的全部完整記錄，含原03兩型、
原01四型、同一全域inverse、全部七點lifts、完整原cap及1,186份空fibre的
上游bytes保管。[INPUTS](INPUTS.json)凍結23份數學authority，六份routing另存；
immutable drift與live routing drift分開。正常／seed17在獨立程序重建相同結果；
16項semantic反控制、外部破壞證書及缺欄證書均拒絕。完整link有限校準有
20份五度、72份六度標記，六度含12份無色1；只是link校準，非941來源。

```sh
python3 -B audits/2026-10-23-three-mask-round4-cb8f859/941/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-three-mask-round4-cb8f859/941/check.py --seed 17
python3 -B audits/2026-10-23-three-mask-round4-cb8f859/941/check.py --negative
```

結果見[VERIFICATION](VERIFICATION.json)。有限checker驗來源合同、原框與樹路、
完整原link及反推論控制；任意大小二分由紙證承擔。M不在J_B的完整來源尚未
觸發，沒有來源實現、配對排除、較小bad或Lean。兩target各八配對及一般
941／W7／J1／J2仍OPEN；V=w、型II、長路、profile1、K≥2、tip、rootless與
原X／T五度唯一色2兩側／至少六度均保留。

下一窄題是原B側M的共同rotation，或標記Z∈K2∩Q與同一B13路R的共同接合；
R不自動認r，M不自動認L。只寫本941目錄，前三輪與shared docs未改，
未commit／push。
