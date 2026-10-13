# 具名來源 J/P 與 W／C 的 Lean 實例

2026-10-02。接續 [CommonRepair](lean_common_repair.md)、
[D₁₃ 密封替換](lean_sealed_four_port.md)及
[來源充分條件](c5_two_vertex_repair_sources.md)，完成正、反向兩個
`private_interiors` 核心的原圖延拓、具名投影與 repair 分類。
目前停止點見 [Lean 導覽](lean_guide.md)及[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

實作為 [NamedRepairCore.lean](../Math/NamedRepairCore.lean) 與
[NamedRepair.lean](../Math/NamedRepair.lean)，共用命名空間
`FiveBoundary.NamedRepair`；34 個公開 theorem 全列於
[公理審計](../Math/NamedRepairAudit.lean)，由 [Math.lean](../Math.lean) 匯入。

## 1. 原圖與同一份八點配置

固定具名次序，不取 S₄ 軌道商，也不獨立正規化來源或 scopes：

```text
U=(x,l,y,m,n,p,q,r)=(a0,a1,a2,a3,a4,b0,b2,b4)
rev=false: (s,t)=(x,y)；rev=true: (s,t)=(y,x)
內點 8,…,12 = A_inner5,…,A_inner9；13,14 = B_inner5,B_inner6
```

`coreEdges rev` 明列全部35條原邊，包含兩個原 C₅、原弦 q–r、
A 的完整五內點附件及 B 的完整兩內點附件。
`J rev` 定義為存在**同一份十五點原圖 proper coloring**，在八個具名點
逐一等於給定 row。`core_proper_iff` 把原邊表接到 `graphOfEdges`／`Proper`。

令 N 表示四個顏色至少一對相等。`a_rule` 將 A 私有路徑在 h7 分成
兩條短尾，對五個具名框色作有限 kernel 檢查，證完整私有延拓 iff
原 C₅ proper 且 N(x,l,y,m)、N(x,n,m,y)。`b_rule` 同樣檢查兩個
完整可用色 lists，證 B 延拓 iff 原框 proper、q≠r 且 (s≠r 或 p=q)。

`j_iff_rule` 明確構造／限制十五點染色，將兩個來源在同一 U 下合併：

```text
b ∈ J rev ↔ ARule(x,l,y,m,n) ∧ BRule(p,s,q,t,r)
```

此 iff 的充分方向實際填入全部七個私有內點；不是匯入 Python 的 J 表，
也不是只證必要條件。兩方向以同一個 `rev : Bool` theorem 涵蓋。

## 2. 指定框的 P 與全部七十個 scopes

`Accept rev S b` 是完整具名投影：存在 c∈J，在 S 的每個原點保持 b 的顏色。
本模組以兩個**明定**混合框的 scopes 定義 P：

```text
C₁={x,n,m,y,q}，C₂={s,l,t,r,p}
P={b | Accept C₁ b ∧ Accept C₂ b}
```

此處集合只作投影的 support；原框次序仍為 `(x,n,m,y,q)`、`(s,l,t,r,p)`。
不同框可有不同完整延拓；未將它們拼成 b 本身的共同延拓。
`j_subset_p` 給 J⊆P，`system` 直接使用既有 `projectionSystem`，
故每個 scope 的接受關係皆自動保留 J。

`Scope` 是所有四元素的 `Finset (Fin 8)`，`scope_count` 證其恰有70個；
沒有刪掉小排除類或空排除類。角色為

```text
A={x,l,y,m}，B={s,p,q,r}，T={x,y,p,q}
𝓔={S : Scope | {q,r}⊆S 且 S≠B}
```

`p_guard` 從兩個框各自的原圖延拓取回具名邊與色數限制；
`j_inside_p` 證 J=P∩N(x,l,y,m)∩(q≠r)∩(s≠r 或 p=q)。
`cover_ab`、`cover_ate` 再由投影保留的局部限制證兩類完整覆蓋。
對任意 E∈𝓔 的同一個證明只需 E 保留實際邊 q–r，不枚舉排除表。

## 3. 精確 witnesses 與分類

| 方向 | W_A | W_BT | W_BE |
| --- | --- | --- | --- |
| 正向 | `01232113` | `01201130` | `01012122` |
| 反向 | `01232112` | `01212132` | `01012122` |

每方向保留原來源證明的十一份八點補全。`lift_check` 遍歷明列清單，
核對每份補全滿足 JRule、每個應接受的四點 scope 有保持原色的補全，
以及兩個框各有補全；`j_iff_rule` 將它們全部接到原圖延拓。
被拒絕的 scopes 則由 `accept_a/b/t` 與原邊 q–r 直接反證。
`witness_rejectors` 因而證三個完整 rejector 集合恰為
`{A}`、`{B,T}`、`{B}∪𝓔`，相對於全部70個 scopes。

`witness_coverage` 將這些事實組成既有 `Roles.WitnessCoverage`，
後續分類使用 CommonRepair 的普通集合論定理：

| 定理 | 已證結論 |
| --- | --- |
| `repairs_iff` | 全部 repairs 恰為含 `{A,B}` 或某個 `{A,T,E}` 的集合 |
| `minimal_repairs_iff`、`minimal_repairs_mem` | 全部 inclusion-minimal repairs 恰為這些模板 |
| `fifteen_minimal_repairs` | 每個方向的完整極小 repair 清單恰有15份 |
| `unique_minimum_pair` | 條件份數至多二的 repair 唯一為 `{A,B}`；最少份數為二 |
| `forced_scope_iff` | A 是唯一出現在每份 repair 的 scope |
| `no_small_projection_repair` | 任意一族至多三點的具名投影，其任何合取都不能修復 P |
| `four_point_repair` | 兩份四點投影 `{A,B}` 確實修復 P |

最後兩條給此**無輔助變數、僅合取原 J 投影**模型的 `r*=4`。
下界保持 W_A：每個至多三點 scope 都包含於某個異於 A 的四點 scope，
因此仍接受 W_A，而 W_A∈P\J。下界容許任意索引族，不只已枚舉的四點集合。
最少份數二、十五份 inclusion-minimal repairs 與最小 arity 四是不同結論。

## 4. 驗證與信任界線

34 條 theorem 無 `sorry`、新增 `axiom` 或 `native_decide`。
有限 source lists、固定補全及小型 scope/cardinality 檢查使用
`decide`／`decide +kernel`，均由 Lean kernel reduction 驗證。
公理審計至多使用 `propext`、`Classical.choice`、`Quot.sound`，
不含 `sorryAx` 或 `Lean.ofReduceBool`。實際命令與結果見
[研究紀錄](history/2026-10-02-lean-named-repair.md)。

[只讀來源核對](../scripts/c5_lean_named_repair.py)將 Lean 邊表、六個
witness 字串、22份補全、具名點序及角色編號對照原 Python source／artifact；
它驗資料來源一致性，與 Lean kernel 證明分開。原 artifacts 不變。

本輪形式化只涵蓋兩個十五點核心及**上述明定兩框**的 P。
兩框可作 disk 外界、其餘候選框不可用、全部可用框恰為這兩框，
仍沿用紙面及 Python 拓撲證書，沒有 Lean topology theorem。
四個 P=J 圖的具體前提、任意大小的來源族、D₁₃ 替換在這些來源中的
具名附件與逐層圖結構，亦未由本模組形式化。
因此可稱為「兩核心指定框 repair 的端到端 Lean 證明」，
不能稱為「全部 disk 來源族的端到端 Lean 證明」。
一般出口、多步充分性及 `K∞=K≤5` 仍未證，未使用四色定理。

## 5. 重播與接手

```bash
python3 scripts/c5_lean_named_repair.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
lake build
lake env lean Math/NamedRepairAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

下一個可分離接口：將具名核心的 D₁₃ 附件接到 `cap_sealed_replacement`，
證替換圖在原 U 上的 J 與指定框 P 相同；框族的 disk 可用性仍獨立保留。
完整下一步以所屬導覽為準。本輪未重跑其他替換族、D₁₃ checker、
大枚舉或其他 Lean 模組的獨立 axiom audit，未更新工具鏈或重新生成 artifacts。
