# 同來源 LL-CUT：有限必要介面與可讀容量 cuts

凍結 BASE：`3097ef5be241b7777451a5ef8a663f3987d6b866`。
本目錄只用 `../frozen` 的上游輸入。完整來源契約、上游前提與拓撲證明分別見
[BASE](../BASE.json)、[本輪紙面證明](../paper/TOPOLOGY.md)及根報告。

**結論：基本 S 的資料投影仍有 19,229 份三列共同可行 profiles；它們不是來源圖，
也不是 LL-CUT 反例。** 加強版的原拓撲／diagonal 證明須另讀紙面報告；不能把其中新增的
接受格偷偷加到本目錄的 S。這裡所有矩陣只用原題的 contact-boundary slack 與 shared slack。

## 1. 原來源到有限必要域的覆蓋

本段不是「只拒三列」的替代來源契約。完整 Σ、T4、所有非框邊 critical、原 degree、
平面 disk、有效 H、full B-touch、one-sided、原 blocks 等前提仍留在原來源帳本。
投影只抽取可被基本 cuts 使用的必要資料。

1. 由已採納盾弧引理及 full B-touch，兩份原 long 的 actual support 就是兩段原盾弧
   的全部頂點；弧邊互斥，長度為 2+2 或 2+3。保留原 B 的五個字面位置。
2. spokes 避開兩盾弧內點，同一 root 的兩 spokes 必接一條原框邊。
   整體交換 r,s 使 t 為 (2,0)、(1,1)、(2,1)；整體交換 P,Q 使長度較短者為 P，
   等長時按原盾弧邊的字面序排序。這兩個交換各只做一次，三列使用同一交換。
   **沒有旋轉 B、沒有重標顏色、沒有逐列或逐 piece 正規化。**
   剩下 85 個字面 geometry：33/t20 有 5；33/t11 有 45；33/t21 有 15；34/t11 有 20。
3. 對同一 source，原 root incidences 分別分成兩個正整數，總和 5−t_r、5−t_s。
   shared contact 對兩側各算一條原邊；沒有把兩條邊折成一次。
4. 每個原 contact 記作一個獨立 slot，記全部 owner 集合 r、s 或 rs、其**全部**原 B
   附件 A，並記 `degree_in_C=4−|owners|−|A|`。long 不是 singleton，故此度至少 1。
   所有 A 至多兩點，兩點時必相鄰（凍結 `c5_excess_two_arc_spoke_closure.md` §6，
   完整 Σ-critical 來源的共同框附件推論）。
5. 每份 long 至少有兩個可作私有 leaf contact 的不同 contact，即其原 C 度≤2：
   多 block 取兩個不同 leaf blocks 的私有 contacts；單 bridge 的兩端因完整 degree4
   與至多兩個 B 鄰點都必有 owner；單奇環由至多一個普通私有點及長度至少三得到。
   no-shared 時，這兩個 contacts 都有非空 B 附件。這裡只保留必要的「可作」條件，
   **不指定或虛構實際 leaf block**。
6. |A|=2 的 contact 有原 H 度2。採納的原框邊附件單射
   (`c5_excess_two_arc_size_bound.md` §3 引理2) 使這種 A 在全部 P,Q contacts 中不得重複。
   每份 contact fibre 按已用原框邊的 bit mask 分組，P,Q 只取 masks 互斥的組合。
7. 由同一 contact 資料取兩側 W、shared 身份和三列 q signatures。
   若三列基本 cuts 都未觸發，下面 §2 的 Z-screen 必成立。
   因此所有合格原來源的基本 LL-CUT 失敗者都映到 `profiles.json` 的一份紀錄，
   再映到 `contact_members.json` 指定的兩份完整 contact-interface 成員。

### 投影不等於改圖

原 source ledger 必保留原頂點與全部原邊、原 root 上的 contact incidence 次序、每個
contact slot 到原頂點的雙射、每個 shared slot 的兩條原 root 邊、原局部 rotation、
原 bridges／cycles／旁支、普通點的全部附件、支援弧所屬的原面、自由孤立座標因子。
contact slots 的排序只是有限檔案的序列化；同 type 的不同原 contacts 仍各有一個 slot。
逆雙射按 source ledger 還原原 names/order，不能由另一份 source 的 ledger 代入。

有限投影**沒有忘掉後再自行恢復**這些資料；它不判定它們是否存在。特別是 ordinary
vertices 的附件、contact 在何 leaf block、cycle adjacency 和原 minor bags 並未被此
必要域枚舉。接回及原 minor 必須回到 ledger；原 complete Σ／criticality 也未被有限
projection checker 所證。保留 support 字段不代表 contact 附件已實現整個 support。

## 2. 紙面 basic cuts 與 Z-screen

設 n=4−t_r、m=4−t_s、a=k_P^r、b=k_P^s。
不看任何固定格，總容量已迫

`n(b−1) ≤ ma`，以及 `m(a−1) ≤ nb`。

因此下列接線子域已由基本 LL-CUT 排除，與 long 大小、實际 W 皆無關：

| t | 不可行的 `(a,b)` |
| --- | --- |
| (2,0) | (1,4)、(2,1) |
| (1,1) | (1,3)、(3,1) |
| (2,1) | (1,3)、(2,1) |

若 `k_C^other≥2` 且某個 `h∈W_C^v` 在指定列的色屬於 E_v，C 接受該整行／欄。
C=P 時全部 M=0，與下界 `k_P^other−1≥1` 矛盾；C=Q 時全部 M=1，
但格數 `k_P^other+k_Q^other−1>k_P^other`，與上界矛盾。故三列皆可行迫

`k_C^other≥2 ⇒ W_C^v⊆Z(T_v)`，
`Z(T)={h: q_i(h)∈q_i(T) 對 i=0,1,3 全成立}`。

字面 signatures 是 `000,111,220,102,221`。Z(∅)=∅，Z({h})={h}；
相鄰 pairs 除 Z(12)=124、Z(40)=024 外都不擴大。這是同一原附件在三列的交集。
Z-screen 外的每份原介面都有上述具名 row/column cut，**沒有被未解釋地刪掉**。

### 固定格後只有四種證書

每個安全格的來源由實際 `(contact owner, B attachment h, q_i(h))` 或 shared 身份給出。
P 安全格固定 0；Q 安全格固定 1；重疊直接接回。沒有重疊時，記 F 是自由格集、
f_r/f_c 是各行／欄已固定的 1 數，並設

`l_r=max(0,b−1−f_r), u_r=b−f_r`；
`l_c=max(0,a−1−f_c), u_c=a−f_c`。

若任何 u<0，即固定 1 超過上界。否則對任意原色行集合 R、欄集合 C，必要不等式是

`Σ_(r∈R) l_r ≤ Σ_(c∈C) u_c + |F∩(R×(columns\C))|`；
`Σ_(c∈C) l_c ≤ Σ_(r∈R) u_r + |F∩((rows\R)×C)|`。

這兩式直接計數需要放置的 1；不引用 solver UNSAT。此域每列最多九格，凍結
`matrix.py` 的逐格分配亦保存 exact count 和第一份可行矩陣供獨立比對。
604 個 certificate shapes 分成：363 overlap、21 forced-upper、111 row-lower、109 column-lower。
這是四個紙面公式的有限帶參數例子，不是 604 條獨立定理。

具體可讀例子 `cut43131701a509`：P 支援012，Q支援234，T_r=04、T_s=0；
k_P=(2,1)、k_Q=(1,3)，Q shared 且 W_Q^s 含3。在 q0，root pin 行 x=3 中，
格 (3,1) 因 Q 的 s–contact–b3 碰色固定1，格 (3,3) 因 Q shared 固定1。
故 `Σ_y M(3,y)≥2>1=k_P^s`。所有固定格來源、literal root colors 與原 bounds 均在證书中。

純容量例 `cut1ef21c2ae186` 在 2×3 格、k_P=(1,3) 時，兩行各至少2個1，
三欄各至多1個1，得 **4≤3** 矛盾。無需任何固定格或額外接受資訊。

## 3. 有限結果與精確殘留

| actual support 大小／t | Z-screen profiles | 基本 cut | contact 介面不相容 | 三列共同可行 |
| --- | ---: | ---: | ---: | ---: |
| 33／(2,0) | 17,056 | 13,234 | 2,748 | 1,074 |
| 33／(1,1) | 132,165 | 108,018 | 18,584 | 5,563 |
| 33／(2,1) | 77,962 | 56,918 | 15,132 | 5,912 |
| 34／(1,1) | 194,740 | 151,720 | 36,340 | 6,680 |
| 合計 | 421,923 | 329,890 | 72,804 | **19,229** |

原 local contact 介面不相容是 §1 原 degree／leaf 必要條件／原附件單射的排除；
它不是 capacity cut，也不是完整 source realization 檢查。

19,229 份紀錄展開為 **64,408** 份必要 contact-interface pairs；1,378 個 piece
catalogues 的 **3,764** 個成員逐份完整列於 `contact_members.json`。每個 member 的
所有 slots、owners、附件、C 內度都列出；空 catalogue 在 contact-incompatible 階段保留於
可重算排除 stream。此處的 contact fibre 與原著色 full fibre 是不同層次，不能混稱。

每一保留 profile 都有同一 geometry、同一 contacts 的三列 references，指向 2,455 個
不重複 literal row certificates。證书的 `assignment` 是 M 的可行分配，**不是原染色**。
`cut_catalog` 保存每個 rejected shape 的 exact example；完整 329,890 個排除 tuples 可由
`candidate_profiles()` 順序重算，stream hash 位於 `cut_profile_digest`。未用不同列 profile
拼出一份三列來源。hash 是重播核對，覆蓋理由仍是 §1–§2 的紙面論證。

例如 `p00000` 保留支援012／2340、T_r=T_s={0}，P 的 k=(1,1)、
W_P^r=W_P^s={0}、無 shared；Q 的 k=(3,3)、W_Q^r=W_Q^s=∅、有 shared。
三列 E_r=E_s={1,2,3}，P 基本 S 為空，Q 基本 S 為 diagonal，每列 M 都可取3階單位矩陣。
這個 contact-interface 例子**不供應**原 cycles、普通附件、平面性、complete Σ或criticality，
因此只證本次必要 projection 未排空。它沒有反駁基本 LL-CUT。

## 4. 尚未由 basic projection 使用的完整條件

- 實際 cycle／bridge 鄰接及 contacts 所在 block，尤其相鄰私有 contacts 的原 K5／K3,3 bags。
- 跨兩 pieces 的原 rotation、原面與所有 ordinary attachments；full B-touch 目前只用於支援等於盾弧。
- 完整 Σ=933／941、T4 與 criticality 除已採納結構推論外的額外限制；絕不將三列拒絕冒充完整 Σ。
- 原 rejection 的完整 degree-list palettes／full diagonal lifts；本目錄的 S 沒有加入它們。
- 原圖完整纖維、空染色 fibres、同列同 pins 全 lifts、自由孤立座標乘積；由來源控制另行處理。

窄且可反駁的下一個 basic 子問題可固定 `p00000` 的字面 W／incidence／shared 資料，
要求把所有必要 contact slots 實現成保留完整 source ledger 的兩份原 long，並證明某個
**基本**原附件 cut 必觸發，或給出合格完整來源。若引用新增 diagonal lemma 排除來源，
必明記這回答的是 +diag 路線；不宣稱那個單位矩陣在原 basic 規則下不可行。

## 5. 證据、驗證與保留紀錄

- `domain.py`：必要介面生成、相同 frame 三列投影、凍結矩陣工具、完整 contact-fibre iterator。
- `profiles.json`：唯一現行 profile certificate，SHA256
  `e0ff3a1aa5b1f133d91c3ad665e256c3d3bd727fc57488d6c324acbbb8456eef`。
- `independent_contacts.py`：完全不 import 生成器，以 owner 分組的 attachment multiset 獨立枚舉。
- `contact_members.json`：完整成員清單，SHA256
  `89da171ab5d2bb0708467b5f6b634da01d6fc40c65dab913a601deaf7a2d5b4a`。
- 根目錄獨立 checker 重建每份 profile 的 S、bounds、三列 matrices 及 exact cuts。

`profiles.pre-copy-isolation.json` 保留第一版生成紀錄：piece option 的 dict 被重用，
contact-fibre annotation 曾進入較後 cut 的序列化。已用每份 candidate 的獨立 dict 修復，
数学欄位、矩陣結果與全部計數不變；舊檔不是現行證書，未覆寫。
獨立 contact checker 初跑曾因 example slot 排序採字典序而與 generator 的
`(owner,|A|,A)` 次序不同而失敗；統一明示序列化後通過，成員數從未有差異。

重播命令：

```bash
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/profiles/domain.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/profiles/domain.py --check
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/profiles/independent_contacts.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/profiles/independent_contacts.py --check
```

實際執行狀態見 `verification.json`。本目錄沒有新增 Lean theorem，沒有來源圖枚舉；
局部必要介面／矩陣控制可 triggered and holds，合格完整來源控制仍 not triggered。
