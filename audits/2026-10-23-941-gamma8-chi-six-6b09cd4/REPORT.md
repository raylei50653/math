# 941 Γ8 空 M2：六外點整支排除，七點尚需新 rootless／K 資源

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
本 exclusive 目錄接續[第二輪](../2026-10-23-941-types-wrong-side-round2-6b09cd4/REPORT.md)
指定的空 M2／新 χ 六外點義務，保同一原圖、rotation、字面框、完整
原分量、原附件、全部空 fibres 及 full lifts；15份直接 authority 與3份
routing snapshot 見 [INPUTS](INPUTS.json)，數學 authority 零漂移。

**空 M2、Γ8 內恰二點的 T 六度支不可能只有六個外側私有點；因此空支
至少七外點。合前輪非空 M2 界，全11必要型共同至少七外點。**
這是具名條件來源排除，11整型仍 OPEN，全域 k≥23 不變。

[紙證](PROOF.md)先把 χ 的完整原分量身份接回原接觸圖：χ2 的 L02
碰框，χ3 的 B13 碰框，均不在原 J−K 中含 M 的 rootless 支 R。
故兩支 χ 都對 R 的全部原點無邊。六外點反設下
`X={a3,y1,b3,p_d2,p_x2,χ}`；χ 對完整 N13 無邊，使 a,b,y,r,sΓ
的完整原星包絡與舊五外點情形完全相同。O 用原度數缺口排除；L／R
重現同一七內點、30邊、18面 K6 cap。χ 及其全部原附件均在此 cap 外側。

於是引用[已證四候選縮減](../2026-10-23-941-types-wrong-side-round2-6b09cd4/PROOF.md)：
同一原 G 的一份真正01232接受 witness 只選一次 H；同一 H 的三拒絕列
全部沿同一外側／商映射回填原七點，恰嚴降7／9個原內點。χ 不被刪除，
沒有新完成成本或未知接線，與全域最小性矛盾。

另得較尖的剩餘合同：T 六度時，原外側至少六點必在
`Z=X∩(V(R)∪V(K))`。任何 Z 外點都對 N 無邊；若只有原五點
`{a,y,b,p_d,p_x}` 在 Z，不論還有多少外部 spectator，仍出現同一可縮 cap。
χ 不在 Z。因此空 M2 的七外點等號必另有
`ω∈V(R)∪V(K)`，不能以第二個 L／B 外點補足；ω 原星與外側接合仍 OPEN。

[producer](produce.py)以紙面列表及凍結全 fibres exclusive-create 新
[certificate](certificate.json)。[獨立 checker](check.py)從實際原邊重建
11型×兩種 χ 色×兩種 U 身份的44份原星小接口，完整窮盡 y,a,b 原
cyclic links（候選池包含 χ，並由完整分量限制排除）；16份 L／R 原星列
全迫同兩張 cap，O 及 d=U 無共同星。另由實際18面核共同方向／完整
內點 rotation；直接 backtracking 核全部62個正規化 proper 六框 fibres、
104份原完整 lifts 與24空 fibre。四份實際候選圖／商映射的全16,384
個字面 relation bits 另行重建，各自單向回填且聯集恰原 R19。

```sh
python3 -B audits/2026-10-23-941-gamma8-chi-six-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-chi-six-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-chi-six-6b09cd4/check.py --negative
```

[VERIFICATION](VERIFICATION.json)記 normal／seed17 結果一致、10個語義
反控制及2份外部破壞／malformed 證書全拒絕、15份原 authority 最終零漂移。
有限域為 `triggered and holds`；具名實際完整來源為 `not triggered`。
一般原圖的 anticompleteness、包絡完備、密封嵌入及最小性反證由紙證承擔，
沒有從控制 PASS 直接推出來源排除。

下一窄義務是空 M2 七外點中同一 `ω∈V(R)∪V(K)` 的完整原星及與 χ
的共同外側接合。同輪[另一線的34候選縮減](../2026-10-23-941-types-wrong-side-round3-6b09cd4/PROOF.md)
已另排非空 M2 七外點，該支現至少八外點；本目錄 checker 的空支範圍不變。
非空 M2 至少八外點、全部11整型、更多 Γ 內點、較長 Γ、
一般 wrong-side、初始八配對、941／W7／J1／J2、一般較小 bad、Lean 與
matching 仍 OPEN。沒有新增 LP 或 Lean；本子線未 commit／push。
