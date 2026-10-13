# ε=2：t=1、(2,2,1) 的原 binary 省略排除

**後續（2026-10-03）**：[t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)
已將本型提升為整型來源排除；下文保留當輪省略核心結論及原證書。

2026-10-03，基準 `bbd900a`，接續
[t=1 兩原 unary 省略](c5_excess_two_single_spoke_two_unary.md)。目前入口見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見
[研究紀錄](history/2026-10-03-excess-two-single-spoke-binary.md)。

**結論：933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、
唯一 degree-6 root、t=1、原接點分拆 (2,2,1) 下，省略任一整份
原 binary 後必接受全部十列。** 結合 spoke＋unary 的結構排除，該型
沒有全 degree-4 真子核心。未排除整型來源，未提高共同 ε≥2。
證據是任意大小紙面化約與 Python 固定域證書，未新增 Lean theorem。

## 1. 原來源與省略核心

G 有限簡單，指定有序 induced-C₅ 外框 B=(b₀,…,b₄) 是 disk 邊界；
完整 Σ 為 933、941 或其整圖 D₅ 像，接受全部 T4。每條非框邊 e
滿足 Σ(G−e)⊋Σ(G)。有效內部 H 連通，唯一 root r 完整 degree 六，
其餘內點完整 degree 四。唯一 spoke 為 rb_s；H−r 的原分量為
binary A、C 及 unary W，有序原接點分別為 (x,y)、(u,v) 及 w。
保留原附件、ownership、環序、嵌入與全部原邊。

反設 K=G−C 拒絕 q。K 有效內部連通、全部完整 degree 四且接受
T4。minimal q-core 的 degree-4 飽和沿內部傳播，迫 core 等於 K。
[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
給 Σ(K)=Ω∖{q}。A 內原 x–y 路徑使 r 位於 cycle 上，分類迫其為
原 triangle rxy，而 rw 是原 bridge。

共同搬運整張來源的 D₅／S4，把 q 對齊 q₄=01012（十列索引 0）。
K 恰屬[原接點保持分類](c5_941_two_spoke.md#2-保留-r-的原核心分類)
的 82 bases／148 marks：20 個單 triangle／path-tail 位置及
128 個直接 bridge 雙 triangle 位置。任意長 tail 的化約保持全部
proper b 的完整 T(b;r,x,y,w)、原 A 的有序雙接點 relation、原 W
的 endpoint relation、原 spoke 及實際末端附件。C 全部保持原狀。
這是既有任意大小涵蓋的使用，不是重新枚舉來源圖，也未使用原資料
中接回新 spoke 的圖。

## 2. 完整六接點接合與三色存活

固定同一字面 boundary coloring b。記原 C 完整有序雙接點 relation
為 R_C(b;u,v)。R_C 非空：刪 r 後每個接點有 list slack，以其中
一接點為生成樹根，逆序貪婪染色其餘點，最後染根即可。每個非根點
染色時仍有未染的父點，根的 list 比內部 degree 至少大一。此論證
允許任意大小、任意內部結構；不要求 C 是邊或樹。

原來源的精確完整關係為

\[
J(T,R_C)=\{(a,c,d,e,f,g):(a,c,d,e)\in T(b),\ (f,g)\in R_C(b),
\ a\ne f,\ a\ne g\}. \tag{1}
\]

每個 tuple 由同一 b 下的完整 K 染色和完整原 C 染色拼接，檢查
ru、rv 即得。兩個有序 binary relations 都未被 marginals 取代。
令 P(b) 為 T 的 root 投影，F_C(b)=∩_{(f,g)∈R_C(b)}{f,g}，則

\[
\operatorname{proj}_r J=P(b)\setminus F_C(b),\qquad |F_C(b)|\le2. \tag{2}
\]

因此 |P(b)|≥3 時必可延拓。構造上，任取原 C 一份完整染色，其
兩接點最多使用兩色；選 P 中另一色及其完整 K 染色即可。這只用於
指定 root 接合，不宣稱 root 投影是一般可迭代 state。

任意 binary relation 的完整控制可用恆等式

\[
J(T,R)=\bigcup_{p\in R}J(T,\{p\}). \tag{3}
\]

式 (3) 是逐 tuple 的集合等式。故檢驗全部 16 個 singleton 有序
色對，配合非空性，即涵蓋任意非空 R；包含相同色的有序對，並未
預設 uv 為原邊。有限控制另測全部 120 個二元素 relations 的式
(1)–(3)，其中也含不可拆成兩個 domains 乘積的 relations。

## 3. 固定域證書與排除

對 148 個原 marks，比較 933 的五個 D₅ 像
{933,934,940,948,996} 與 941 的五像 {941,949,950,998,1004}。
若目標接受 q₄，與 K 已拒絕矛盾；其餘每份比較均有目標要求拒絕
但 |P|≥3 的列，與 §2 矛盾。

| 排除原因 | 933 五像 | 941 五像 |
| --- | ---: | ---: |
| 核心拒絕目標須接受的 q₄ | 148 | 296 |
| 三個 root 色不能被原 binary 封鎖 | 592 | 444 |
| 合計 | 740 | 740 |
| 剩餘 | 0 | 0 |

[Checker](../scripts/c5_excess_two_single_spoke_binary.py)與
[artifact](../artifacts/c5_excess_two_single_spoke_binary/observations.json)
重新由原邊核對 82 bases 的 degree、apex rotation、q₄-criticality，
148 marks 的具名接點、原分量、實際支援、1,480 份完整 relations
及其全染色 witnesses。資料沿用
[原核心 artifact](../artifacts/c5_941_two_spoke/observations.json)。

對 1,036 個三色排除比較的全部 16 個有序 binary 色對，各保存一個
相容原核心 tuple／完整染色 witness 索引，共 **16,576 個 lifts**。
原 C 的實際 tuple 用其自身完整染色見證，並未以兩個自由新點代替 C。
137 份不同字面 T 的算子控制共有 **2,192 次 singleton relation**
及 **16,440 次二元素 relation** 完整六接點核對；每份算子保留所有
原 (mark,row) 索引。沒有枚舉全部 65,535 個非空 R；一般涵蓋由式
(3) 給出。抽象 relations 也不宣稱有同一 disk 來源。

任選被省略的原 binary 命名 C，另一份命名 A，上述證明均成立。
這不假設 A、C 可由圖自同構互換，也不允許各自重命名色。故

\[
\boxed{\Sigma(G-A)=\Sigma(G-C)=\Omega.}
\]

## 4. 同型無全 degree-4 真子核心

省略 spoke 及 W 時，root 內部 degree 四。若此省略圖拒絕，飽和
傳播迫它自身為全 degree-4 核心，但分類中的內部 degree 至多三，
矛盾。因此這個省略身份亦全收。

任何全 degree-4 minimal rejected-row core 必含 r：其他內點原
degree 四，保留它即須保留全部 incident 邊，沿原分量傳播必碰到
r。每份被保留的原分量遂完整保留。把 r 從六降四只能省略 A、
省略 C，或省略 spoke＋W；三個具名容量二身份全部涵蓋。

故該型沒有全 degree-4 真子核心；含 degree-5／degree-6 的核心
仍保留，不能據此排除整份來源。其餘分拆、兩個 degree-5 roots、
一般出口與 K∞=K≤5 均未由本輪解決。

## 5. 重播與停止點

```bash
python3 scripts/c5_excess_two_single_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_single_spoke_binary.py --check
python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
python3 scripts/c5_941_two_spoke.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 artifact 依大型產物政策登錄 MANIFEST、producer 與原核心依賴。
本輪重播原接點 transfer 固定控制與上一輪核心檢查，未重跑全
degree-4 分類／外部 degree-list 的全部歷史拓撲證據。`lake build`
只核對既有 Lean 專案，不形式化新增紙面接合或無界化約。

停止於原 binary 省略排除及同型無全 degree-4 真子核心。下一窄題
由導覽維護；本輪未作 commit／push。
