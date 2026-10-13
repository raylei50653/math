# No-mixed 無禁色增長：短側弧與共同 singleton 排除

後續（2026-09-29）：[增長完備性與共同分離](c5_no_mixed_growth_completion.md)
已從三個共同側弧位置直接指定排除配方，免查必要支援表地排除影響 R
的增長；結合無增長定理完成指定 p₁、p₂ 的存在性分離。下文未解描述
保留當輪語境；逐染色建構式 repair、完整 Σ 與一般出口仍未證。

2026-09-29，Git 基準 `3174f08`，接續工作樹中的
[統一局部篩選](c5_no_mixed_local_screen.md)。**在既有 no-mixed 前提下，
若每份原分量的 target 禁色大小都不增加，則指定 p₁、p₂ 必有異色 root
pair。** 以下用共同側弧與顏色置換給出免查必要支援表的紙面證明。

這關閉「無增長時不能留下同 singleton」的缺口；不是新增 target 接受，
也未證有增長時的共同局部規則必定成功。新
[checker](../scripts/c5_no_mixed_no_growth.py)／
[證書](../artifacts/c5_no_mixed_no_growth/observations.json) 重播原 7,848 個
無增長 joins，作為證明步驟的控制，不作紙面全稱的依據。
目前停止點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)，
實際驗證見 [當輪紀錄](history/2026-09-29-no-mixed-no-growth.md)。

## 1. 前提與沿用的結構

完整沿用[跨度報告 §1–2](c5_no_mixed_span_budget.md#1-適用前提與精確語義)：
M 有限簡單，B=(b0,…,b4) 為 induced C5 disk 外框，H=M−B 非空連通；
q=01012 拒絕，刪任一非框邊後接受 q。恰有相鄰 z,w 完整 degree=5，
其餘內點完整 degree=4；H−{z,w} 每份原分量 C 恰接一個 root。
U={0,1,2,3}，p₁=01021、p₂=01212。不需 T4，不限制原分量大小。

保留同一原 C、具名 contacts、bridges、旁支、actual support S_C、
spokes、zw、共同環序及字面色框。T_C(β) 為非空的完整有序接點關係，
F_C(β)=⋂_{τ∈T_C(β)}set(τ)，且

\[
E_r(\beta)=U\setminus\left(\beta(N_B(r))\cup\bigcup_{C\sim r}F_C(\beta)\right).
\]

延拓恰當 (E_z×E_w)∖Δ 非空。以下僅使用已證的三組 source 結構：

1. E_z(q)=E_w(q)={c}，沒有 source 重疊，各側
   t_r+Σ|F_C(q)|=3。這是 source minimality 與跨度排除的結論，
   **不預設 target 也滿足等號或 minimality**。
2. 同一份同序 lift 中，所有原分量 hull 有正整數跨度，與各 spoke
   作為具名單位依序排列，相鄰可共端點。兩側區段 I_z、I_w 包含
   各自全部支援及 spokes，框邊內部不交，2≤ℓ_r 且 ℓ_z+ℓ_w≤5。
3. 側跨度下界 A/B/C/D/E 為 2/2/3/4/3。因此長度二的側只能是 A
   或 B：分別為兩 spoke 加一份 singleton 禁色的 binary C，或一
   spoke 加兩份 singleton 禁色原分量。這只用側結構與下界，
   不用七類必要支援表、原 target 接受 flags 或個別原分量大小。

這些結構沿用原 annulus 次序、外部路徑及飽和分量的紙面引理；其前層
degree-list／Gallai 依賴仍是外部定理。本輪不另證或形式化那些前提。

## 2. 容量等號與支援穩定子

假設對每份 C 都有 |F_C(p)|≤|F_C(q)|。則每側禁色聯集的大小至多
t_r+Σ|F_C(p)|≤3，所以 E_z(p)、E_w(p) 均非空。

若某側 |E_r(p)|=1，上述兩個不等式都必取等號。於是該側所有 F 都
保持 source 大小，spokes 顏色互異，且各 F 與每個 spoke 的單色禁色
兩兩不交。這是**以 target singleton 為條件推得**的等號。

任何逐色固定 β(S_C) 的置換 π 都將同一原 C 的完整染色雙射到自身，
故 πT_C(β)=T_C(β)，從而 πF_C(β)=F_C(β)。同理，若 π 固定 r 側
全部實際 boundary 附件的顏色及 spokes，則 πE_r(β)=E_r(β)。
這使用完整關係，不使用接點邊際，也沒有改動另一份原分量或外框。

兩個直接推論：

- 若支援只見至多兩色，singleton F 的唯一顏色必在已見色中：未見
  色至少兩個，交換它與另一未見色會破壞 singleton 不變性。
- 若 r 側完全看不到兩色 a,b，則 E_r 在 (a b) 下不變，故不能恰為
  {a} 或 {b}。這不要求 E_r 非空，也不要求 F 為 singleton。

## 3. 短側引理：只能剩中間色或第四色

固定上述共同 lift 中長度二的側 r，其三個連續框點記為 x,y,z，y
在中間。取任一使用恰三色的 proper boundary coloring β，第四個
未用色記作 δ。假設該側各 F_C(β) 的大小至多一，且 |E_r(β)|=1。
則

\[
\boxed{\beta(x),\beta(y),\beta(z)\text{ 兩兩不同},\qquad
E_r(\beta)\in\{\{\delta\},\{\beta(y)\}\}.}\tag{1}
\]

**證明。** 若三個框點只見兩色，每份支援也只見至多兩色；依 §2，
每個非空 singleton F 只能禁已見色。Spokes 同樣只禁這兩色，故聯集
至多兩色，E_r 至少二色，矛盾。因此短弧呈三色。

若沒有分量禁 δ，全部禁色皆在這三個框色中；E_r singleton 迫三色
全被禁，所以 E_r={δ}。

若某 C 禁 δ，支援穩定子迫 S_C 見到另外三色，故 S_C={x,y,z}，
它的 hull 占滿短弧。每份其它原分量需正跨度，因而不可能存在；
該側只能為 A，有兩條不同 spokes。**共同單位次序禁止任何 spoke
落在 C 的 hull 內部 y**，所以這兩條 spokes 只能落在 x,z。它們禁
β(x)、β(z)，C 禁 δ，恰剩 β(y)。證畢。

不能把結論強化成 E_r={δ}：A 側可由完整支援的 C 禁 δ、兩端 spokes
禁端點色，留下中間色。AC80 的 z 側就是必要資料中的控制：短弧
(b4,b0,b1)，q 色為 (2,0,1)，Cz 禁 3，spokes 在 b4,b1，剩 0。
這仍不是 AC80 的來源實現證書。

共同次序也不可省：抽象地令短弧色為 012、C 支援三點且禁 3，將
spokes 放在位置 0、1，會剩端點色 2，違反 (1)。此配置讓 spoke
穿入原分量 hull，沒有符合前提的共同同序 lift；新 checker 保留此
負控制，不將它當 disk 反例。

## 4. 三色 C5 的唯一單現點與無增長定理

任一 proper 三色 C5 的色類大小為 2,2,1，記唯一單現色所在框點為
s(β)。一段長度二的框弧呈三色，**恰當它包含 s(β)**：移除單現點後
的四點路徑以另外兩色交替；包含單現點時，其餘兩點異色。

取任一短側 r（由 2≤ℓ_z,ℓ_w、ℓ_z+ℓ_w≤5 保證存在），中間框點為 y。
它的 source 禁色都為 singleton，因此 (1) 適用於 E_r(q)。短弧必呈
三色，且 E_r(q) 是 {3} 或 {q(y)}。

**Source 單現點不能在短弧中間。** 若 y=s(q)，另一側的全部 actual
supports 與 spokes 都不含 y：在同一 lift 中 y 是短側區段的內點，
另一側的正長度區段若含 y，必與短側共用框邊。於是另一側看不到
q(y) 與 3，其 E 在交換這兩色下不變；不可能等於 E_r(q) 的任何一個
選項。這與 source E_z(q)=E_w(q) 矛盾。

故 s(q) 是短弧的一個端點。現在固定 p∈{p₁,p₂}，並假設所有 F 都
不增長。q 的單現點為 b4；p₁ 的為 b3、p₂ 的為 b0，皆與 b4 相鄰。
兩側 E(p) 已由容量保證非空。

- 若短弧在 p 下不是三色，(1) 的逆否命題給 |E_r(p)|≥2；與另一側
  任一可用色即可挑出異色 pair。
- 若短弧在 p 下呈三色，它同時包含 s(q)、s(p)。這兩點相鄰、互異，
  而三點弧的兩端在 C5 中不相鄰，所以其中一點必為中點。s(q) 已
  排除在中間，故 **s(p)=y**。若 |E_r(p)|≥2 仍直接延拓；否則 (1)
  給 E_r(p)={3} 或 {p(y)}。另一側看不到 p(y)、3，E_{r′}(p) 對交換
  兩色不變，不能是相同 singleton。非空的兩個 E 因此仍有異色 pair。

這就證明

\[
\boxed{\bigl(\forall C,\ |F_C(p)|\le|F_C(q)|\bigr)
\Longrightarrow (E_z(p)\times E_w(p))\setminus\Delta\ne\varnothing.}\tag{2}
\]

證明不用目標分量的完整搬運是否可行，也不固定一份 source 染色來
repair；只用原完整關係的置換不變性與共同幾何。換色在此用來證明
集合不變性，並非直接對整張圖執行 Kempe 交換。

只要另一 proper 三色 target 的單現點與 s(q) 相鄰，同一論證成立；
不能刪去「相鄰、互異」前提，例如 p=q 本來就拒絕且完全沒有增長。
本報告仍只將 (2) 接回指定 p₁、p₂。

## 5. 有限控制與舊 joins 重播

新 checker 僅用 Python 標準函式庫，不匯入原 target 幾何排除引擎，
不讀取舊 acceptance／classification 作判定。證書綁定 root-transport
與其十份原輸入 SHA；完整 schemas、具名 contacts、支援與原圖身份
沿原 record pointer/hash 保留。沒有新來源圖或支援枚舉。

| 檢查層 | 範圍與結果 |
| --- | --- |
| 短側代數控制 | 1,872 份合法短側配置／禁色賦值，其中 216 份 singleton 均滿足 (1) |
| 三色框控制 | 120 個 proper 三色 C5；600 份三點弧控制；5,760 對相鄰單現點的兩列、11,520 份共同三色弧皆有單現中點 |
| 同源共同 lifts | 2,082 份原 placements 重新建立側區段；2,264 個短側的 q 單現點均在端點 |
| 全候選域 | 重建原 4,164 查詢／11,096 joins，與原具名 F tuple 域相等 |
| 無增長接合 | 7,848 joins 逐步檢查容量、短側引理及對側交換不變性，全有異色 pair |
| 查詢級共同理由 | 固定選一個短側；2,082 查詢為 target 短弧非三色，2,082 為 target 單現中點的交換不變性 |

7,848 joins 按原家族為 AA1500、AB2140、AC464、AE288、BB2880、BC288、
BE288。每筆保存原 join index、實際 E 與異色 root pair；家族名只用
來記錄覆蓋，target 理由不按家族分支。原短側的 A/B 結構仍是引理
的明示前提，並非宣稱完全不使用 source 結構化約。

原 32 個無害增長 joins 不在 (2) 的假設內，仍由局部篩選報告的
pair∩R_r=∅ 充分條件處理。原 434 個失敗 joins 的排除機制也未改寫。
本輪不新增 source 排除或 target 接受；source 短弧端點性是共同結構
的紙面推論，不另計一批已排除 records。

## 6. 重播與精確界線

```bash
python3 scripts/c5_no_mixed_no_growth.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_no_growth.py --check
python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無 `--check` 只生成本層 artifact，舊輸入前後 hash 不變。完整驗證及
未重跑範圍見[研究紀錄](history/2026-09-29-no-mixed-no-growth.md)。

(2) 是沿用任意大小 source 結構引理的紙面證明；Python 只是固定域
控制及必要表回歸。未新增 Lean theorem／`native_decide`，`lake build`
不表示紙面幾何已形式化。未證必要支援可實現、完整 Σ、一般共同出口
或 K∞=K≤5；外部 Gallai 文獻本輪未重讀。

剩下的共同證明缺口集中在**有增長且影響 root 可用色時，何以必符合
既有守恆／非守恆局部排除條件**。原局部規則的全表成功仍依證書，
不能從本輪無增長定理推出它的免表完備性；AA54 全路徑交換與 AB22
非守恆原端點仍須保留。下一入口由研究線導覽維護。
