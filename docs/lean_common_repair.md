# 共同 repair 判準的 Lean 形式化

2026-10-02。接續[共同 repair lemma](c5_two_vertex_common_repair.md)，將抽象
W／C 充要判準及其分類推論補成普通 Lean 證明。實作為
[CommonRepair.lean](../Math/CommonRepair.lean)，由 [Math.lean](../Math.lean)
匯入；命名空間為 `FiveBoundary.CommonRepair`。
目前形式化停止點見 [Lean 導覽](lean_guide.md)，圖論來源線仍見
[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

## 1. 完整集合與前提

`System Ω Λ` 保存同一 row 空間中的 `target=J`、`base=P`、每個索引的
完整接受集合 `accept i=Kᵢ`，以及 `J⊆P` 和 **每個** `J⊆Kᵢ` 的證明。
定義與原報告一致：

```text
delta       = P \ J
result H    = {x ∈ P | ∀ i ∈ H, x ∈ Kᵢ}
Repairs H   ↔ result H = J
rejectors x = {i | x ∈ delta ∧ x ∉ Kᵢ}
Covers H    ↔ ∀ x ∈ delta, ∃ i ∈ H, i ∈ rejectors x
ExactWitness Q ↔ ∃ x ∈ delta, rejectors x = Q
```

`Covers` 是原完整排除集合覆蓋等式的逐元素形式；不是覆蓋數量。
`ExactWitness` 的等式相對於全部 `Λ`，包含角色以外的任意候選條件。
保真性是 `System` 的必要欄位，不以「覆蓋全部錯誤 rows」代替保留 J。

`Roles Λ` 保存互異的 A、B、T，非空集合 𝓔，以及 A、B、T 均不在 𝓔 的
證明。`WitnessCoverage` 恰為五條前提：

- `ExactWitness {A}`、`ExactWitness {B,T}`、`ExactWitness ({B}∪𝓔)`；
- `Covers {A,B}`，以及每個 `e∈𝓔` 的 `Covers {A,T,e}`。

Ω 與 Λ 都可無限。主充要判準、極小分類及極大失敗分類不需要有限性；
份數定理另外以有限的 `H : Finset Λ` 表示選用條件。

`projectionSystem J P hJP scope` 將具名完整配置 `U→C` 接到此模型：
條件 i 接受 x，恰指存在 `y∈J` 在 `scope i` 的每個具名點上與 x 相等。
保真性直接以 y=x 證明。各 scope 的延拓仍各自存在，沒有將它們拼成同一份
全域延拓，也沒有獨立正規化各 scope 的顏色。

## 2. 具名定理與結論

下表省略共通命名空間。`System.*` 屬集合模型，`Roles.*` 屬具名角色模型。
完整 27 個公開 theorem 均列入 [axiom audit](../Math/CommonRepairAudit.lean)。

| 定理 | 精確結論 |
| --- | --- |
| `System.repairs_iff_covers`、`System.repairs_mono` | repair iff 完整覆蓋；加入保真條件仍為 repair |
| `System.not_repairs_iff_residual`、`System.witness_hits` | 失敗 iff 有完整殘留 row；每份 repair 必命中每個 exact witness 的 rejector 集合 |
| `System.residual_compl_eq`、`System.exactWitness_of_compl` | 若向 Q 的補集加入每個缺項都修復，該補集的殘留恰是 rejectors=Q 的 rows；補集失敗即抽出 exact witness |
| `System.minimalRepair_iff_deletions` | inclusion-minimal iff repair 且刪任何單項都失敗；不需要 Λ 有限 |
| `mem_projection_result` | 原 J 的具名 scope 投影接回完整 result 語義，保留逐 scope 的存在量詞 |
| `Roles.repairs_iff_template` | 五條 W／C 推出：H 修復 iff 含 `{A,B}` 或含某個 `{A,T,e}`，e∈𝓔 |
| `Roles.witnessCoverage_of_classification`、`Roles.witnessCoverage_iff_classification` | 上述分類反推出五條 W／C；完整雙向等價，而非只證充分性 |
| `Roles.minimalRepair_iff` | 全部 inclusion-minimal repairs 恰為 `{A,B}` 及每個 `{A,T,e}` |
| `Roles.forced_iff` | 索引 i 屬於每份 repair iff i=A |
| `Roles.maximalFailure_iff` | 全部 inclusion-maximal 非 repairs 恰為 `{A}`、`{B,T}`、`{B}∪𝓔` 的補集 |
| `Roles.obstruction_residual_eq` | 三個極大失敗集合的完整殘留分別恰是對應 exact-rejector rows，涵蓋原報告式 (4) |
| `Roles.repair_card_ge_two`、`Roles.repair_card_le_two_iff` | 每份有限 repair 至少兩項；repair 且至多兩項 iff 正是 `{A,B}`，所以最少恰二且唯一 |
| `System.repairs_of_base_eq_target`、`System.minimalRepair_of_base_eq_target` | P=J 時每個 H 都修復，唯一極小 repair 為空集合；不使用非空角色或 witnesses |

必要方向先證三個補集都缺少模板，但任添一個缺項就含模板，再以
`exactWitness_of_compl` 抽取完整 witnesses。極小分類直接證各模板彼此
不包含；不依賴列舉候選子集合。最少份數與 inclusion-minimal 保持為
兩個不同的結論。

## 3. 證據層與停止點

本輪完成的是上述一般集合定理與具名投影介面。普通 Lean 證明沒有
`sorry`、新增 `axiom` 或 `native_decide`；27 條 theorem 的審計依賴
至多為 `propext`、`Classical.choice`、`Quot.sound`，不含 `sorryAx` 或
`Lean.ofReduceBool`。實際驗證命令及輸出摘要見[本輪紀錄](history/2026-10-02-lean-common-repair.md)。

既有六圖的 W／C 前提仍由原
[Python checker](../scripts/c5_two_vertex_common_repair.py) 與
[完整證書](../artifacts/c5_two_vertex_overlap/common_repair.json) 負責；本輪
重播通過，但沒有將六圖 J/P、七十個 scopes 或其 witnesses 匯入 Lean。
因此「兩非平凡圖各十五組修復」仍是一般 Lean 判準配合外部 Python
前提驗證，尚不是這兩張圖的端到端 Lean theorem。
舊 artifact 的 `new_lean_theorem=false` 描述原生成輪次，本輪保留其 bytes
及來源 hash；新形式化由本報告及 Lean 檔記錄。

來源 relation、來源替換、D₁₃ 四接點等價、disk rotations／可用框、
四點 arity 下界 `r*=4` 均未由本模組形式化。也未補一般後繼表、
多步摘要充分性、完整 Σ、一般共同出口或 `K∞=K≤5`。
原報告「僅由全部極小解分類反推全部 repairs」所用的有限極小元抽取，
本模組未另列 theorem；主 W／C 與**全部 repairs** 的 iff 已完整證成。

下一個可分離的形式化工作是：在 Lean 中定義具名來源 J/P，證成每條
W／C，再套 `witnessCoverage_iff_classification`；幾何框可用性仍須另證。

## 4. 重播

```bash
python3 scripts/c5_two_vertex_common_repair.py --check
lake build
lake env lean Math/CommonRepairAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪沒有重跑來源替換族或其他研究線的 checker，也沒有重新生成 artifacts。
