# ε=2 唯一 mixed：原 spoke＋unary 省略全收

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[兩側原 unary 省略](c5_excess_two_mixed_core_two_unary.md)
已由雙固定支援 transport 及 3,180 份同源雙收縮星 subdivisions 全排。
因此 (4,4) 保留 mixed 的全部原省略身份已封閉；若有 (4,4) core，
必恰只省略唯一原 mixed，其 incidence 向量為 (1,1)。下文保留本輪
spoke＋unary 結論與原停止點。再後續[省略原 mixed](c5_excess_two_mixed_omission.md)
亦全排，因此相鄰唯一 mixed 的 (4,4) 核心全部封閉。
共同 ε≥2 不變，目前入口見 [Kempe 導覽](c5_kempe_guide.md)。

2026-10-03，接手基準 `722bfa6`，保留既有未提交成果。接續
[原省略身份與雙 spoke 排除](c5_excess_two_mixed_core_spokes.md)，完成其
spoke＋原 unary 停止點；目前入口由 [Kempe 導覽](c5_kempe_guide.md)
維護，實際驗證見 [研究紀錄](history/2026-10-03-excess-two-mixed-core-spoke-unary.md)。

**結論：固定完整 Σ=933／941 的 ε=2 相鄰雙 degree-5、唯一原 mixed
disk 來源，省略一側原 spoke e 及另一側原單接點 unary V，必全收 Ω。**
含 root 交換型。結合前輪，保留 mixed 的 degree-(4,4) rejected-row
core 若存在，其兩個原省略因子必須都是單接點 unary。

證據為任意大小紙面接合／minor 化約及 Python 固定必要域證書。
**共同下界仍 ε≥2；未證 ε≥3，未新增 Lean theorem。**

## 1. 同一原來源與要排除的省略

完整沿用前輪來源前提：G 有限簡單，B=(b₀,…,b₄) 是指定有序
induced-C₅ disk 外框，完整 Σ 為 933、941 或其整圖 D₅ 像，且每條
非框邊刪除都嚴格擴大 Σ。有效 H 非空連通，恰兩個完整 degree-5
roots z,w，其餘有效內點完整 degree 四；原 zw 存在，H−{z,w}
恰一份原 mixed C，其餘為原 unary。保留原 contacts、全部附件、
ownership、原嵌入環序及同一字面色框。

令 e=zb 是原 z-spoke，V 是原 w-unary，其唯一 w-contact 是 v。
省略 V 表示去掉整份 V 及其全部 incident 邊；不是只刪 wv。
記 M=G−e−V。它繼承 T4、disk，原 mixed 與 zw 仍在，故有效
內部仍連通；所有有效內點在 M 自己的完整 degree 都為四。

若 M 未全收，它必拒絕 singleton 列 q。Degree-4 飽和沿其連通
內部傳播，使任何 minimal q-core 等於整張 M。因此 M 自己是
全 degree-4 minimal q-obstruction。此處沒有把原 G 當成 q-core。

由 [前輪原形限制](c5_excess_two_mixed_core_spokes.md#3-44-且保留-mixed原形比-contact-數更受限)，
原 C 的兩側 contacts 必同為 {x}，z,w,x 是原 triangle。
全部保留分量仍是原分量。對整張 G 作一次 D₅／S₄ 搬運，令
q=q₄=01012；V 的支援、e、兩 roots 及所有列同步搬動。

## 2. 原 V 非空的完整 relation 與精確接合

對任意 proper boundary coloring β，定義原 endpoint relation

\[
S_V(\beta)=\{f(v):f\text{ 是原 }V\text{ 的完整延拓染色}\}.
\]

在 v 的原 root 邊 wv 去掉後，可用 list 至少有 deg_V(v)+1 色；
其餘點至少有 deg_V 色。以 v 為根的 spanning-tree 逆序貪婪染色給
S_V(β)≠∅；沿用 [原 unary slack 證明](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)。
V 的大小、blocks、路徑及全部實際附件不受新限制。

令 P 包含原 roots 及 M 的所有原分量 contacts，共鄰 x 只列一次。
\(\mathcal T_\beta\) 是 M 接回原 e 後的完整 P-tuple relation。
原圖的完整接合恰為

\[
\mathcal R_G(\beta;P,v)=
\{(t,d):t\in\mathcal T_\beta,\ d\in S_V(\beta),\ t_w\ne d\}.\tag{1}
\]

每個 t 有同一份 M+e 全染色，d 有原 V 全染色；兩部分只共用
固定的 B，再檢查原 wv 即能拼接。沒有獨立換色或把 mixed contacts
的 marginals 相乘。只有在完整 tuple 已算出後，才取

\[
A_\beta=\{t_w:t\in\mathcal T_\beta\},\qquad
F_V(\beta)=\begin{cases}\{d\},&S_V(\beta)=\{d\},\\
\varnothing,&|S_V(\beta)|\ge2.
\end{cases}
\]

由式 (1)，β 接受 iff A_β∖F_V(β)≠∅。特別是 |A_β|≥2 時，
不論同一原 V 的非空 relation 為何，G 都接受 β。

Checker 保存 \(\{(t,d):t\in\mathcal T_\beta,d\in U,t_w\ne d\}\)
這份完整接合算子。最後一欄限制到真實 S_V 才是式 (1)；自由 endpoint
座標不冒充 degree-4 原 V 或它的內部 coloring witness。

## 3. 原 V 的固定實際支援限制跨列選色

令 S=N_B(V)⊆B，是同一原 V 的實際支援。若色置換 π 滿足
p(b)=π(q(b)) 對所有 b∈S 成立，將 V 的整份染色一起換色便給

\[
S_V(p)=\pi S_V(q),\qquad F_V(p)=\pi F_V(q).\tag{2}
\]

因此 V 的空／singleton 禁色是 **S 上局部 equality shape** 的函數。
固定該 shape 的一列代表後，候選 singleton 色必被固定支援色的
stabilizer 固定。S 上看到至多兩色時，它只能是已看到的色；看到
三或四色時，至多可選任一 literal 色；空禁色始終是代數選項。

Checker 窮盡全部 32 份具名 S，對每份 S 保存 local shapes、全部
色置換數、逐列 transport 和合法 singleton 選項。对每個候選 mask，
式 (1) 的接受／拒絕要求都限制同一 shape 變數；將各列允許選項取交。
交集空便有明示衝突列；非空只表示必要代數相容，沒有 V 實現宣稱。
不枚舉任意十列自由選色，也不需要新的 D 身份或 Gallai 假設。

## 4. 同一原 V 的連通收縮必為 disk minor

固定一份相容 S。只為拓撲反證，把 **原連通 V 全部收縮成一點 a**，
保留原 wa 及 a 到 S 的所有框邊，去掉 loops／重邊。這是 G 的
boundary 不識別 minor；不宣稱收縮保持 S_V、完整 Σ 或 degree。

對 M 的原 triangle 外掛路徑枝，使用前輪相同的原 run 化約：
單 run 保留一個非葉點，兩-run 保留 X,Y,Y,leaf；其餘原區段沿
路徑收縮，重複附件合併。它同時是 boundary 固定 minor，並保持
原 triangle／roots 的完整聯合染色 relation。原 z,w 不在被縮枝內，
這些 branch sets 與原 V、B 互不相交。

故兩個步驟可在同一原 G 同時進行。原 spoke e 保留，所得必要圖是

\[
J=M^*+e+wa+\{ab:b\in S\}.\tag{3}
\]

在 disk 外侧加一個只連向五框點的 apex h。真正的 disk 來源必使
J+h 平面；只要它有明示 K₅／K₃,₃ subdivision，就排除原 G。
這些 subdivision 路徑是在指定收縮 minor 的實際邊集上驗證；回到
任意大小原圖由互斥連通 branch sets 及 minor 傳遞負責。

沿用 [前輪 126 份必要正常形](c5_excess_two_mixed_core_spokes.md#4-雙-spoke-省略的任意大小覆蓋)：
十八份帶枝單 triangle、八份兩-run、36 份裸 triangle 的 T4 全收
必要支援，以及 64 份直接-bridge 雙 triangle。全部原 triangle 邊
都可標 roots，合計 570 份具名原 root 邊。裸 triangle 必要域未先
篩 disk；非 disk 放寬只會增加需要排除的案例，不是來源實現。

## 5. 完整固定必要域與排除結果

兩個 root 方向及所有不存在於 M 的另一條 spoke，共 3,732 份
spoke＋原 unary 接合。對 933／941 各五個整圖 D₅ 像直接比較：

| 目標 | 比較數 | 目標接受列已空 | 兩色存活迫接受 | 留待固定原支援 |
| --- | ---: | ---: | ---: | ---: |
| 933 | 18,660 | 5,880 | 11,552 | 1,228 |
| 941 | 18,660 | 9,382 | 7,722 | 1,556 |

2,784 個殘留各檢查同一 V 的全部 32 份支援，共 89,088 次：

| 原支援判定 | 次數 | 剩餘 |
| --- | ---: | ---: |
| 同支援 S₄ transport 的 shape 選項交集空 | 83,644 | 0 |
| S₄ 相容，但同源收縮星 minor 非 disk | 5,444 | 0 |

後者去掉重複候選 mask 的相同原圖／支援查詢，恰 2,640 份具名
minor；逐份保存明示 subdivision，**2,637 份 K₃,₃、3 份 K₅**。
Verifier 獨立檢查每條 path 的原 minor 邊、簡單性、內部互不相交、
branch 頂點及全部九／十份鄰接，不只保存 planarity boolean。

因此反設 M 未全收不可能，得到在 §1 全部來源前提下

\[
\boxed{\Sigma(G-e_z-V_w)=\Omega,\quad
       \Sigma(G-e_w-V_z)=\Omega.}\tag{4}
\]

式 (4) 的 V 是另一 root 的原單接點 unary；不適用於同側省略、
多接點 unary、非相鄰 roots 或一般來源。結合前輪雙 spoke 排除，
保留 mixed 的 (4,4) q-core 若存在，只能省略兩份原單接點 unary。

## 6. 證書、原長圖控制與停止點

[Checker](../scripts/c5_excess_two_mixed_core_spoke_unary.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_spoke_unary/observations.json)
重建全部必要核心，從實際邊重算 q₄-critical witnesses、分量、具名
contacts、全部附件及共同 root/contact tuples。不讀舊 Σ flags 作判定。
5,700 次 core 列關係、37,320 次 spoke 過濾與獨立完整圖回溯比較，
559,800 次十五份非空 endpoint relation 的完整算子接合全通過。

26 張固定原長圖保存所有原 contacts／attachments／support、run
收縮 branch sets 及各自完整 joint tuples；780 次 root-pair 關係、
5,240 次 spoke 接回後的原 unary-owner 色集相等。跨縮減只宣稱
原 triangle／root relation 保持，長短圖的其他 contact 座標各自保存。

另保存 32 張接上實際 singleton／edge／path／triangle unary 的完整
原圖，320 次十列接合與全圖回溯相等，原 V 全邊、原附件與全部
tuple coloring witnesses 明列。它們只是有限染色控制，不聲稱 disk
或 Σ-minimal。負控制保存一份逐列自由禁色能匹配目標的算子案例；
固定同一原支援及 disk minor 才排除它，不能把該自由 schedule 當來源。

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
python3 scripts/c5_excess_two_mixed_core_spokes.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

實際執行及未重跑範圍見 [本輪紀錄](history/2026-10-03-excess-two-mixed-core-spoke-unary.md)。
大型產物由 MANIFEST 登錄、generated ignore 及 producer 依賴維護。
全 degree-4 任意大小分類仍沿用既有 degree-list／Gallai、紙面及
有限 topology 完備性；新接合、固定支援 transport 及 minor 傳遞
是紙面證明，Python 證固定必要域。`lake build` 不形式化本頁。

**停止點：** 保留 mixed 的 (4,4) core 已排除所有包含原 spoke 的
雙省略身份。下一窄題是同一原共鄰 triangle z,w,x，各側省略一份
原單接點 unary U、V；保留兩份原完整 endpoint relations、兩份
固定實際支援及同一 root-pair joint relation，再檢查精確雙接合。
不能只看兩側 root marginals，也不能各自選不同的原支援色框。

省略唯一 mixed、(5,4)/(4,5)、G 自己為 (5,5) q-core，以及多 mixed、
no-mixed、非相鄰 roots／unary 側例外均保留。未證全部 ε=2 排除、
ε≥3、一般出口、來源實現或 `K∞=K≤5`。
