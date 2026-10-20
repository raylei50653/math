# C 的獨立審查

## 右六邊面比較：PASS

審查對象：[../right_minimality.py](../right_minimality.py) 及
[../right-minimality.json](../right-minimality.json)。

紙面合法性：原 r 的完整 link 是 `(x,y,t,w,v,s)`，由原三角形皆面，
非連續 link 點之間沒有原弦。刪原 r 留下實際六邊面。九個非相鄰頂點對各自可在此面內
畫弧並識別；不存在 loop，且不識別兩個原框點，因 rim 中的原框點只有相鄰 x,y。
十四種互不交對角線三角化各自可在同一實際六邊面內畫出，沒有新增點。
原框字面值保持；兩左／右操作位置的被刪點及被識別類互異，故指定的組合可同時完成。

完成內點數：單右識別是 k−2，單右三角化是 k−1。
右操作與 Q1/Q2 合作分別為 k−6、k−5；與左 G_B 或左六邊面三角化合作分別為 k−4、k−3。
完整雙側三角化為 k−3。這些是完成圖的內點數，不能使用 D10 的 k−11 代替。

完整投影：原右 cap 刪 r 後，僅需 x≠s、y≠t，加上 E 的 cx,xy,ya
與 C10 的 sv,vw,wt；原 r 四條邊已隨 r 刪去。右識別加精確等色，右三角化加三條精確異色。
root 的 transfer 逐份枚舉 s,v,w,t 並保留全部 multiplicities，與這些條件一致。

[review_right.py](review_right.py) 以獨立 Catalan 遞迴重建十四種三角化，
直接枚舉固定字面 C10 著色及完整左 cap；不匯入舊 matrix 或 B/minimality。
它獨立核對所有23張右候選、196張雙側三角化在兩控制上的576份十列完整計數。
全部與 root 保存結果相等。這是必要比較與控制投影審核，並非任何控制的來源實現。

## B 幾何：PASS

審查對象：[../B/CHORDS.md](../B/CHORDS.md)、[../B/check.py](../B/check.py)
與 [../B/certificate.json](../B/certificate.json)。已回到原
[雙低 p,q 證明 §5](../../2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md)
核對 `p=q=5 ⇒ ell>=6` 的同一原圖身份與最小性前提。本輪 p=ell=5，
故 q 不能為五度；原內點下界五給 q>=6。這是原 G 度數，不能誤換成商圖度數。

D10 是原 G 內的實際有界 disk，其外側連通原外面；短框弧與內部 chord
圍出的有界子 disk 全在 D10，六個被刪點在其外側。故原 C3/C4/C5 定理
確實作用在該 pocket 的有界內部。嚴格中間框點的 D10 內角全屬 pocket，
任何 core 邊若離開 pocket 必跨 chord 或 C10，所以其所有 core 鄰點都算入填片度數。
此論證只對嚴格中間點，沒有錯用到 chord 的端點。

[review_geometry.py](review_geometry.py) 用另一份 Catalan 遞迴，獨立重建
35 個可能 chord 的每一條短弧、全部空三角化與 C5 的 W5 例外。
與 B 證書逐案比對填片、度數及 admissible 判定，全部一致：27 條由短圈／度數排除；
ac 由原 triangle abc 內至少有 p,q 排除，ns 由原圖非邊排除；
其餘僅 `Rv,Ls,Lv,Lw,qs,qt`。

Ls 的四圈 pocket 唯一填片加 qs，因此迫原 q=6,c=4。
Lv 的五圈 pocket 唯一填片是 s 扇心，必加 Ls,qs，因此迫原 q=6,c=4,s=6；
W5 會使中間 s 的 core 度數只有三，低於四，確須排除。
原 qs 若存在則其 triangle qcs 迫原 c=4；反向由原 c 四度完整 star 給 qs。
故額外 c>=5 分支只容 `Rv,Lw,qt`，其端點兩兩交錯，至多一條。

兩控制每條可能 chord 的等色 fibre 和由 C 獨立計算，與 B 全相等：

| 控制 | Rv | Ls | Lv | Lw | qs | qt |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Q2_source_positive | 188 | 60 | 340 | 156 | 343 | 159 |
| allK_source_positive | 1236 | 1380 | 1371 | 1331 | 1416 | 1354 |

因此任一控制若有真來源實現，其 D10 必 induced；此必要判定不排除控制，
也沒有構造真來源。接受 B 的任意大小來源必要定理，沒有接受 Q1/Q2 主目標已閉合的宣稱。

## A 任意大小四弦排除與共同計數：PASS

審查對象：[../A/PROOF.md](../A/PROOF.md)、[../A/model.py](../A/model.py)、
[../A/check.py](../A/check.py)、[../A/certificate.json](../A/certificate.json)
及 [../A/chord-closures.json](../A/chord-closures.json)。已逐字核對其完整來源範圍、
三角化、全色置換、逐輪支援消元和映回原 G 的計數鏈。

**任意大小分量引理。** F 的每個 proper 三角面必用三種顏色，故在固定兩個互補二色側中，
每面恰有兩條跨側邊。連其中點得到互不相交的 interface arcs 和閉圈，沒有分叉。
若框有 2m 次側轉換，就有 m 條 boundary-to-boundary arcs，切成 m+1 個接框區域；
閉圈只另隔出不接框區域。逐面縮回同側誘導圖，接框區域恰為接框分量。
因此實際分量分割 noncrossing、每塊同側、同側鄰接框點同塊，且 b=m+1。
內部私有分量可任意多，其交換只增加相同邊界結果的正重數。
這個論證無來源大小上界，也不把不同完整著色或色對的路徑拼接。

**完整 family 與每個全稱刪除理由。** C 的
[review_closure.py](review_closure.py) 不匯入 A 或舊 model。
它先將相鄰同側框點合成循環 side-runs，再分別枚舉兩側 run 集合的全部分割，
組合後檢查 noncrossing 及 b 規則，最後枚舉每份完整分量的所有交換並保存 H-row 重數。
這與 A 從全部 noncrossing partitions 篩選的算法不同；兩法所得10798個完整 counted columns
的 canonical SHA256 完全相等：
`3d17c932692bd15a22b45c6222d62a08f8af4ded132fd213f18441f9bd6f66ab`。
每份真實著色的分量分割都被包含，容許額外不可實現分割只會減弱排除。

原三拒絕的非負完整 cap 矩陣迫244個 core 格空。假定弦再迫該弦兩端同色格空。
每輪一個被刪 core 格 i 的證據是一份同 S4 軌道的 H-row r：任何包含 r 的容許 column
都會碰到**前一輪**已證空格。若 i 真非空，全色置換給 r 非空，實際完整分量交換
則給完全位於前一輪 live set 的 column，矛盾。這證的是每個實際 F 的空性，
沒有把一個可行模型選作真來源，也沒有以某個未被觸發的條件聲稱排除。

C 使用自己的直接字面 cap 矩陣（沒有使用 A 的 G 矩陣）重建全部四個分支。
每輪被刪的全部 core IDs、每格 uncovered H-row witnesses、最後 live set，均與 A 逐份相等：

| 假定弦 | initial | rounds removed | final live | 原 alpha 係數 |
| --- | ---: | --- | ---: | --- |
| qs | 1472 | 292,141,99,48,44,62,30 | 756 | 全零 |
| Rv | 1682 | 286,181,175,130,11 | 899 | 全零 |
| Lw | 1680 | 263,191,189,120,18 | 899 | 全零 |
| qt | 1693 | 258,147,87,34,52,64,32 | 1019 | 全零 |

[closure-review-v2.json](closure-review-v2.json) 保存 C 的完整獨立重建；
[closure-review.json](closure-review.json) 保留最初 qs 單分支重建的原 bytes。
四分支各自沒有任何 live core 格可接原固定字面 alpha；同一核心全部完整著色因此給
`N_alpha(G)=0`，矛盾於原941。接受任意大小的四條原非邊定理；由 qs iff c=4 得 c>=5；
再結合 B 六弦 envelope、Ls/Lv迫c4，接受**所有本輪真來源的 D10 induced**。
不使用 U319、指定正子 fibres 或 signed planar span 來排這四弦。

**兩個新計數恆等式。** [review_counts.py](review_counts.py) 另外核對全部2560份
joint fibres、2461份 cap lifts、四圖共40份固定字面 core 矩陣的每個係數。
用同一個獨立 side-run 方法重建 C8 的全部981 columns，SHA及兩輪刪6、2格至225格與 A 相等。
從完整 joint fibres 獨立重建 Aa/Ab 扇區與四個線性泛函。
91個 planar 等色 columns 上，C 對已證空行的 constraint row-span 做精確 Fraction 消去，
得到 rank47（維度44），四個泛函全部歸零。這與 A 構造 nullspace basis 的驗證方式不同。
因此接受 `a1+a2=2Aa`、`Ab=U1+V1+U2+V2`，並獨立重播舊 GB 兩等式。
接受至少一候選洩漏及成功候選若存在必唯一；沒有接受任何同一接受候選三個拒絕全空的宣稱。

**控制界線。** 兩份控制都違反每一條假定弦的零條件，不能實現有該弦的來源。
真來源不得有這些弦並不要求某個等色 fibre 反而非空，所以無附加弦的兩控制仍存活。
新定理排除任意大小的具名弦子分支；尚未排除 allK，主目標仍 OPEN。

重播：

```
python3 -B audits/2026-10-19-r6-941-quotients-13dc5ff/C/review_counts.py
python3 -B audits/2026-10-19-r6-941-quotients-13dc5ff/C/review_closure.py --additional-chords
PYTHONHASHSEED=17 python3 -B audits/2026-10-19-r6-941-quotients-13dc5ff/C/review_closure.py --additional-chords
```
