# ε=2：t=1、(2,1,1,1) 的兩原 unary 省略排除

**後續（2026-10-03）**：[t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)
已將本型提升為整型來源排除；下文保留當輪省略核心結論及原證書。

**後續（2026-10-03）**：[t=1、(2,2,1) 原 binary 省略](c5_excess_two_single_spoke_binary.md)
已完成下一窄題；同一三 root 色存活論證以完整 binary relation 接合，
該型亦無全 degree-4 真子核心。下文保留本輪結果。

2026-10-03，基準 `bbd900a`，接續
[四原 unary 排除](c5_excess_two_four_unary.md)。目前接手入口見
[Kempe 導覽](c5_kempe_guide.md)，當輪驗證見
[研究紀錄](history/2026-10-03-excess-two-single-spoke-two-unary.md)。

**結論：933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、
唯一 degree-6 root、t=1、原接點分拆 (2,1,1,1) 下，省略任意兩份
原 unary 後必接受全部十列。**

148 個保留原接點的必要核心位置、1,480 次候選比較全部排除：兩份
unary 各至多封鎖一色，不能封鎖核心留下的三種 root 色。不需新增
支援幾何、D 守恆或跨列省略配對。再套既有結構分類，該型其餘容量二
省略亦全收，故**沒有全 degree-4 的 minimal rejected-row core**。
這不排除整份來源；共同下界仍 ε≥2，其餘 ε=2、兩個 degree-5 roots、
一般出口及 K∞=K≤5 保留。證據是任意大小紙面化約＋Python 固定域
證書，未新增 Lean theorem。

## 1. 原來源、具名省略與完整六接點

G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框；完整 Σ
為 933、941 或整圖 D₅ 像，接受全部 T4。每條非框邊 e 都滿足
Σ(G−e)⊋Σ(G)。有效內部 H 連通，r 完整 degree 六，其餘內點完整
degree 四。r 唯一原 spoke 是 rb_s；H−r 的四份原分量是 binary A
及 unary U、V、W，原接點分別為有序 (x,y)、u、v、w。
固定全部原附件、ownership、root 邊、環序及同一嵌入。

反設 K=G−U−V 拒絕 q。K 有效內部連通且全部完整 degree 四，並
繼承 disk 與 T4。minimal q-core 的 degree-4 飽和沿內部傳播，迫
core 等於整張 K。[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)給
Σ(K)=Ω∖{q}。r 在 K 有三個內鄰點 x,y,w；原 A 的 x–y 路徑使
r 位於 cycle 上，分類迫其為原 triangle rxy，rw 是原 bridge。

對整張來源共同作 D₅／S4 搬運，使 q=q₄=01012（十列索引 0）。
其後所有分量及列保留同一字面色框。對每個 proper boundary coloring b，
記 K 的完整有序關係為 T(b;r,x,y,w)，原 U、V 的 endpoint domains
為 S_U(b)、S_V(b)。兩者都非空：刪去 r 後接點具有 list slack，
以接點為生成樹根逆序貪婪即可，見
[unary slack 引理](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)。
完整接合恰為

\[
\mathcal R_G(b;r,x,y,w,u,v)=
\{(a,c,d,e,f,g):(a,c,d,e)\in T(b),\ f\in S_U(b),\ g\in S_V(b),
\ a\ne f,\ a\ne g\}. \tag{1}
\]

T 保留同一原 A 的完整有序雙接點 relation 及原 W，沒有拆成
marginals。各 tuple 由同一 b 下三份完整原染色拼接，再檢查 ru、rv。

## 2. 任意大小涵蓋與三色存活

[原接點保持報告 §2–3](c5_941_two_spoke.md#2-保留-r-的原核心分類)
已涵蓋全部上述 K：18 個單 triangle／path-tail bases 有 20 個原
degree-three triangle 位置，64 個直接 bridge 雙 triangle bases 有
128 個位置，合計 **82 bases／148 marks**。

任意長原 tail 的 transfer 保持每個 proper b 的 T、R_A(x,y) 及
S_W(w)；r、x、y、w、原 spoke 及末端實際附件保持。U、V 及它們
的所有附件完全不縮減。使用前報原核心，沒有使用其「接回新 spoke」
的圖，也沒有新增來源圖枚舉。無界涵蓋沿用全 degree-4／degree-list
與原 tail 論證，並非由 148 個有限模型自行推出。

令 C(b)={a:存在 (a,c,d,e)∈T(b)}，並令 F_Z=S_Z 若 |S_Z|=1，否則
F_Z=∅。由式 (1)，原完整 root 投影恰為

\[
C(b)\setminus(F_U(b)\cup F_V(b)). \tag{2}
\]

因兩個 F 各至多一色，**|C(b)|≥3 時 G 必接受 b**。亦可直接構造：
任選原 U、V 完整染色，其 endpoint 色至多占兩色；從 C(b) 選另一色，
取相應完整 K tuple 與染色，即得原 G 延拓。這保留完整 tuple 及原
染色的存在性，色集合只用於此一固定 root 接合判定。

## 3. 固定域排除與原染色見證

兩候選的整圖 D₅ 像為

\[
933:\{933,934,940,948,996\},\qquad
941:\{941,949,950,998,1004\}.
\]

逐一比較 148 個 marks 與十個目標像。若目標接受 q₄，K 已拒絕該列，
故排除；其餘每份比較均找到目標要求拒絕、但 |C(b)|≥3 的列，與 §2
矛盾。不需預先假設其他省略子圖全收，也不需把不同省略 pair 的見證
列配對。三種具名省略 pair 都涵蓋：任取被省略的兩份，將保留的一份
命名 W 即得以上證明；不是聲稱原 U、V、W 有圖自同構或可獨立換色。

| 排除原因 | 933 五像 | 941 五像 |
| --- | ---: | ---: |
| K 拒絕目標要求接受的 q₄ | 148 | 296 |
| 指定拒絕列有至少三個 root 色 | 592 | 444 |
| 合計 | 740 | 740 |
| 剩餘 | 0 | 0 |

[Checker](../scripts/c5_excess_two_single_spoke_two_unary.py)及
[artifact](../artifacts/c5_excess_two_single_spoke_two_unary/observations.json)
保存全部比較、原 mark／base／root／spoke 索引、指定列、root 色及各色
對應的原核心完整 tuple／染色 witness 索引，並雜湊固定輸入。
Checker 重驗 82 bases 的原邊、degree、apex rotation、q₄-criticality，
148 marks 的原分量、具名接點、實際支援及全部 1,480 列的完整 relations
和染色 witnesses。原來源資料見
[原核心 artifact](../artifacts/c5_941_two_spoke/observations.json)。

另對 137 份不同的字面 T 保存完整六接點算子及全部原 (mark,row)
索引。每份算子限制到全部 15×15 對非空 unary domains，再用獨立
Cartesian-product 定義核對 tuples 及式 (2)，共 **30,825 次控制**。
「全部 domain pairs 都接受」亦逐一核對恰等價於 |C|≥3。
共用算子只去除代數檢查的重複，未合併原來源身份；抽象 domains 沒有
聲稱可由 degree-4 圖或 disk 同時實現。

故對任意兩份不同原 unary Z₁、Z₂，

\[
\boxed{\Sigma(G-Z_1-Z_2)=\Omega.}
\]

## 4. 直接推論：同型無全 degree-4 真子核心

其餘容量二省略可直接由同一全 degree-4 結構分類處理，不新增計算：

- 省略唯一 spoke 及任一原 unary：root 在省略圖的內部 degree 為四。
  若拒絕，飽和傳播迫該圖自身為全 degree-4 核心，但分類中所有內部
  degree 至多三，矛盾。
- 省略整份 binary A：root 有三條分屬原 U、V、W 的 bridges。
  若拒絕，分類要求內部 degree-three root 在 triangle 上，與三條
  incident 邊全是 bridges 矛盾。這不假設 U、V、W 本身無 cycle。

若 G 有全 degree-4 minimal rejected-row core，它必含 r：其餘內點
原 degree 已為四，任何被保留內點都要保留全部 incident 邊，沿原
連通分量傳播必碰到 r。也因此任何保留的原分量都完整保留，root 從
六降四只能省略 A，或在 spoke、U、V、W 四個 unit 中省略一對。
三份 unary-pair 由 §3 全收，三份 spoke＋unary 及一份 binary 由本節
排除拒絕，七個具名身份全部涵蓋。

此推論排除的是全 degree-4 真子核心；含 degree-5／degree-6 的核心
仍可能存在，不能據此排除整份 (2,1,1,1) 來源或提高 ε≥2。

## 5. 重播與停止點

```bash
python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
python3 scripts/c5_941_two_spoke.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

超過 1 MB 的新 artifact 按大型產物政策登錄 MANIFEST、producer 及
原核心輸入依賴。本輪重播原接點 transfer 的固定控制及原核心 checker，
未重跑全 degree-4 分類／外部 degree-list 的全部歷史拓撲證據。
未新增 Lean theorem；`lake build` 只驗證既有 Lean 專案。

本輪停止於兩原 unary 省略排除及上述直接推論。目前下一窄題見導覽；
其餘 ε=2、兩個 degree-5 roots（含 mixed）、一般來源與出口均保留。
