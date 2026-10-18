# 原 r 六度：C5 七接點轉移與相鄰五度 apex 排除

本文件只採用凍結的 [SOURCE_GEOMETRY](../frozen/audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)、
[JOINT_FIBRES](../frozen/audits/2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md)
及相對最小來源契約。本節給一個新的條件式排除：

\[
d_G(x)=d_G(y)=d_G(b)=4,\quad d_G(r)=6
\quad\Longrightarrow\quad d_G(s),d_G(t)\ge6.
\]

它沒有排除整個 r 六度分支。一般的七接點剩餘問題仍 OPEN。

## 1. 合法的 C4 到 C5 轉移

G 是所有目錄外合法 C5 disk 中內點 k 最小、再邊數最大的固定來源；
原框為 `(x,y,a,b,c)`。沿凍結建構識別 a,c 為 z，再刪除 x,y,b，得到
外框 `(z,s,r,t)`、總點數 `k+1` 的 R。原 xy、ya、ab、bc、cx 的 apex
依次是 r,t,p,q,s。

本節假定 `d_G(r)=6`，所以 R 中 r 恰四度，鄰序可記為

`N_G(r)=(x,y,t,w,v,s)`，`N_R(r)=(t,w,v,s)`。

原 r 不接 p,q，故 v,w 都不是 p,q；它們也不等於 z,s,t。刪 r 得

`U=R-r`，外框 `C=(z,s,v,w,t)`。

這是同一嵌入中的三角化 C5 disk，總點數 k、內點數 `k−5<k`。
五條可能的框 chord 都不存在：zv、zw 由凍結等式
`N_R(z)∩N_R(r)={s,t}` 排除；st 已排除；sw、vt 若存在，會分別使
三角形 rsw、rvt 成為 T0 的非面三角形，與 T0 四連通矛盾。
所以 U 的外框是 induced C5。p,q 仍是互異內点，原三角面 zpq 保留。

七接點為 `(z,s,v,w,t,p,q)`。恢復 r 時只加 `rs,rv,rw,rt`；
必須對**同一份完整 U 染色的每一個合法 r 顏色**檢查原 R 的共同条件。
這不是分別選一份可接回的染色。

## 2. 完整局部全 lift 表與 K132 接入

凍結 JOINT_FIBRES 的原 R 必要表為：ABAB 的 pq palette 恰 CD；
ABAC 空；ABCB 的 palette 是 CD 或 BD；ABCD 的 palette 恰 BD。
把 r 的所有合法顏色取交集，得到下表。空 r 欄表示四個鄰色全用齊，
因而該份 U 染色不接回 R；這些列仍須保留在 U 的完整關係內。

| C=(z,s,v,w,t) | r 全部合法色 | 同份 U 染色可有的有序 pq |
| --- | --- | --- |
| ABABC | D | BC, CB |
| ABACB | D | BC, CB, CD, DC |
| ABACD | 無 | BC, BD, CB, CD, DB, DC |
| ABCAB | D | BC, CB, CD, DC |
| ABCAC | D | BC, CB |
| ABCAD | 無 | BC, BD, CB, CD, DB, DC |
| ABCBC | A,D | 無 |
| ABCBD | A | 無 |
| ABCDB | A | CD, DC |
| ABCDC | A | 無 |

bit 順序就是表中十列，自 0 起算。因此 U 的完整外框關係包含於 mask319。
由 `k−5<k`，其關係必屬凍結的 K132；全部 132 個 mask 逐一查核後，
得到精確候選清單

\[
\boxed{\Sigma(U)\in\{271,314,319\}.}
\]

這是完整**外框**關係的三選一，不是七接點代表定理。不能用普通五點
小代表代换 U 並聲稱保留內部 p,q 的逐列 palette、完整 fibres 或計數。

七接點必要 Kempe 控制只用真正 Jordan 邊界 C，列出每份完整染色在
三種互補色對分割下可能的端點 component partition，再保留其全部子集
交換後仍在同一關係內者。結果如下：

| 另有原邊 | 能保留完整外框支持的候選 |
| --- | --- |
| 無 | 271,314,319 |
| tp | 271,319 |
| sq | 314,319 |
| tp 與 sq | 無；這個幾何子域本來也已排除 |
| tp 與 pw | 無 |
| sq 與 qv | 無 |

這份 finite control 的 surviving states 不是來源實現，不保存完整染色
多重度；它只驗證明列条件下的必要推論。其後兩列可由下面更強的紙面
定理統一涵蓋。

## 3. 原幾何補充：跨側邊與低度情況

假若 pv 存在，原五環 `(r,y,a,p,v)` 在 r 的兩個 sector 分別含 t,w
與 x,s；兩側都至少兩點，違反原球面 S 的 S6 五環條件。故 pv 不存在。
對稱五環 `(r,x,c,q,w)` 排除 qw。

假若 pw 存在，原五環 `(r,y,a,p,w)` 的兩側分別含 t 與 x,s,v。
S6 迫第一側恰有 t；原內點至少五度，故 t 接該五環的全部五點，且

`N_G(t)={r,y,a,p,w}`。

因此 `d_G(t)=5` 且 tp 存在，後者等價於 `d_G(a)=4`。反向若
`d_G(a)=4,d_G(t)=5`，由 t 的原面鄰序可得 pw。對稱地

`pw 存在 ⇔ d_G(a)=4 且 d_G(t)=5`；

`qv 存在 ⇔ d_G(c)=4 且 d_G(s)=5`。

本節尚未靠這些等價式排除單獨 t 五度；下一節不需要 a 四度。

## 4. 新排除：原 t 五度不可能

反設 `d_G(t)=5`。t 在原轉移中失去 y、r，a 政名 z，沒有其他 degree
損失，故 `d_U(t)=3`。令它的三個 U 鄰點為 `(z,h,w)`，面為 zth、thw。
h 是 U 內點，且不同於 z,s,v,w；它不能是 q，因原 tq 不存在。
它可能恰是 p，必須分開保留這個 literal identification。

刪 t 後得到

`V=U-t`，外框 `(z,s,v,w,h)`，總點數 `k−1`、內點數 `k−6<k`。

V 是合法 C5 disk，不需要外框 induced 才能用最小性。重新插 t 只接
z,w,h；再插 r 只接 s,v,w,t。下表對每份完整 V 染色取**全部 t lifts，
以及每個 t lift 下的全部 r lifts**。沒有任選接回顏色。

### 4.1 h 不等於 p：兩步 Kempe 排除

此時 p,q 都仍在 V 內，七接點順序為 `(z,s,v,w,h,p,q)`，面 zpq 保留。
完整必要表如下：

| V 外框 | 有序 pq |
| --- | --- |
| ABABC | BD, DB |
| ABACB | BC, BD, CB, CD, DB, DC |
| ABACD | BC, CB, CD, DC |
| ABCAB | BC, CB |
| ABCAC | BC, CB, CD, DC |
| ABCAD | BC, CB |
| ABCBC | 無 |
| ABCBD | 無 |
| ABCDB | 無 |
| ABCDC | CD, DC |

外框上界是 mask575。普通 K132 查表給候選 564、567、572、575；
**四者全含最後一列 ABCDC**。下面用同一張 V、同一份完整染色的實際
Kempe components 排除該列。

**第一步：排除 ABCAC 且 pq palette CD。**
固定 `(z,s,v,w,h)=(A,B,C,A,C)`。如果 z,w 分屬不同 AB components，
交換包含 w 的那個 component；因 zs 是 AB 邊，s 留在 z 那一側。
新外框變成禁止的 ABCBC。因此原圖必有 z 到 w 的 AB 路。

邊界上 z,v,w,h 的順序交錯，故 v,h 不能由 CD 路相連。交換包含 h
的 CD component，使外框變成 ABCAD。原 pq 是一條 CD 邊，所以它的
兩端要麼一起交換，要麼一起不交換，palette 始終是 CD。可是表中
ABCAD 只允許 BC，矛盾。

**第二步：排除 ABCDC。**
固定 `(z,s,v,w,h)=(A,B,C,D,C)`，由表知 pq palette 恰 CD。
如果 v,h 分屬不同 BC components，交换包含 h 的 component；因 sv
是 BC 邊，s,v 保持不變，新外框就是禁止的 ABCDB。因此 s,v,h 都在
同一個 BC component。

邊界 z,s,w,h 順序交錯，故 z,w 分屬不同 AD components。pq 的 D
端點與 z 由原邊直接相連，所以该端點在 z 的 AD component；另一個
pq 端點為 C。交換 w 的 AD component 完全不動 pq，卻將外框變成
第一步已排除的 ABCAC、pq palette CD，矛盾。

排除 ABCDC 後，V 的完整外框關係包含於 mask63；K132 沒有任何關係
包含於 mask63，與 `k−6<k` 的最小性矛盾。兩步都作用於實際完整
染色，因此不需要抽象端點 partition 的充分性，也沒有將不同染色
的連通資訊拼成同一份見證。

### 4.2 h 恰是 p：六個互異接點的單独處理

V 的外框是 `(z,s,v,w,p)`，q 是內點；不能再創造另一個內部 p。
原三角面 zpq 保留，pq、qz 為內邊。完整全 lift 表為：

| V 外框 | q 可有色 |
| --- | --- |
| ABABC | 無 |
| ABACB | C,D |
| ABACD | C |
| ABCAB | C |
| ABCAC | B,D |
| ABCAD | 無 |
| ABCBC | 無 |
| ABCBD | 無 |
| ABCDB | 無 |
| ABCDC | D |

外框上界是 mask542，而 K132 沒有任何關係包含於 542。由最小性
立即矛盾；此子支不需要額外 Kempe 控制。

兩種 h 身份已盡。因此原 t 五度不可能。反射原圖的命名
`s↔t,v↔w,p↔q,a↔c,x↔y` 給原 s 五度也不可能。配合原內點至少五度，
得到本節所述 `d_G(s),d_G(t)≥6`。

由 §3，還可得 r 六度分支中的四條原邊全部不存在：

`pv,pw,qv,qw ∉ E(G)`。

## 5. 大小與接回成本

| 狀態 | 總點數 | 接回原 G 的新增點數 | 完成後 |
| --- | ---: | ---: | ---: |
| R | k+1 | 4 | k+5 |
| U=R−r | k | 5 | k+5 |
| V=R−r−t | k−1 | 6 | k+5 |

新增點數包含 z 分裂成 a,c 的淨增一點。因此這不是保壞性的嚴格下降。
新排除的理由是更小合法 V 在 K132 的完整關係與逐份接回条件不相容，
不是「輔助圖少一點就已得到更小壞來源」。

## 6. 重播、有限域與停止點

凍結 [cells.json](cells.json) 是既有 `artifacts/c5_cells/cells.json` 的完整
副本；SHA256 與兩個 checker 綁定。本輪重查其 132 個 mask 的有限
membership screen，沒有重新跑 K132 的來源枚舉或改變原 catalogue 信任界。

```sh
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_transfer.py --check
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_t5.py --check
```

[transfer.json](transfer.json) 包括第一個全 lift 表、全部 18 個指定邊／
mask 組合的必要 Kempe fixed point 與所有 surviving partition 選項。
[t5.json](t5.json) 包括兩張第二層全 lift 表、獨立直接兩點 cap 枚舉、
每個移除輪次與所有 surviving 選項。七點表的 16,384 個標記指派、六點
alias 表的 4,096 個標記指派全部逐份比對；空 fibre 與沒有 r lift 的
情況均保留。相同 scripts 用 `PYTHONHASHSEED=17` 重播；蓄意改壞的
certificate 必須報錯，其完整 stdout/stderr 和 exit code 留在 logs。

初次尚未加入 tp+pw／sq+qv 的控制保留為
[check_transfer_initial.py](check_transfer_initial.py)、
[transfer-initial.json](transfer-initial.json)。它們是較弱歷史控制，
不取代目前證書。原 s 在 R' 四度的探索因上游 r 五度分支已被本輪
另一份證明排除，沒有作為活躍殘題接入本文件。

目前活躍結果為：r 六度時相鄰 apex s,t 至少六度；U 的普通完整支持
只剩 271／314／319，仍須保留七接點共同關係及完整 fibres。一般 r 六度、
r 至少七度、返回單射、保壞性的完成成本下降及無界主命題仍 OPEN。
本輪沒有新來源實現、外部枚舉或 Lean theorem。
