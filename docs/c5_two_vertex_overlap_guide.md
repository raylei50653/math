# C₅ class 兩點重疊研究導覽

更新：2026-09-30。研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見
[STATUS](STATUS.md)，共通規則見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

任選兩個 C₅ class，各選兩個邊界頂點，以明確雙射識別；研究重疊造成的
完整染色狀態。拓撲線判斷實際接法、側別及可施工位置；狀態線依同一
接合圖更新 relation。Class 固定具名邊界，不省略接點對應。

使用者已澄清這是**兩個 class 的兩點重疊**。不改成單一 C₅ 加邊、
整框五點接合或 C₅→C₆→C₅ 路徑黏合；不從一般大枚舉重新開始。

## 2. 項目現況

| 項目 | 現況與證據 | 入口 |
| --- | --- | --- |
| 可用 class | 既有 132 類完整 Σ／24 個 D₅ 軌道；87 類另有豐富查詢，為子集 | [資料與規格](c5_two_vertex_overlap.md) §2 |
| 兩點接口 | 1,320 份投影已保存並重播；695 強迫異色、625 自由、0 強迫同色 | [artifact](../artifacts/c5_two_vertex_overlap/pair_interfaces.json)、[checker](../scripts/c5_two_vertex_overlap.py) |
| 一次染色相容 | 在精確兩點共享、私有內部互斥、S₄ 換色不變的前提下，兩點型別交集非空 iff 可染；目前目錄全部容許異色 | [紙面推導](c5_two_vertex_overlap.md) §3–4；未新增 Lean theorem |
| 八點共同後繼 | 具名 evaluator、六份完整 relation／雙側回投影及同圖核對已完成；主例 140 軌道，完整後繼表未完成 | [八點接合](c5_two_vertex_join.md)、[artifact](../artifacts/c5_two_vertex_overlap/eight_point_joins.json) |
| 主例拓撲 | 同一八點十邊圖的 36 組環序與 24 份外面配置全核對；兩原框各自可作整圖外界，四種 disk 區域關係均有見證；未 Lean 化 | [主例拓撲稽核](c5_two_vertex_join_topology.md)、[artifact](../artifacts/c5_two_vertex_overlap/reference_topology.json) |
| 私有內點原框 | 指定十五點三十五邊圖平面，兩來源各在自己的 disk 內且內部互斥；兩組原路徑排除 A、B 作整圖外界，完整 J 仍 60 軌道；未 Lean 化 | [私有內點拓撲](c5_two_vertex_private_topology.md)、[artifact](../artifacts/c5_two_vertex_overlap/private_topology.json) |
| 反向私有內點原框 | 反向指定圖亦平面、來源 disk 可內部互斥、兩原框皆被交錯原路徑阻斷；完整 J 與正向各有 16 個獨有 patterns；保存一個混合 C₅ 外面，未 Lean 化 | [反向拓撲](c5_two_vertex_private_reverse_topology.md)、[artifact](../artifacts/c5_two_vertex_overlap/private_reverse_topology.json) |
| 反向混合外框 relation | `(a0,a4,a3,a2,b2)` 的完整 R255／8 軌道／192 賦色及全部原 J 纖維已核對；等於既有單內點 disk 代表，替換須密封其餘點，未 Lean 化 | [混合框報告](c5_two_vertex_mixed_frame.md)、[artifact](../artifacts/c5_two_vertex_overlap/mixed_frame_relation.json) |
| 反向第二混合外框 relation | `(a0,b4,b0,a2,a1)` 的完整 R1022／9 軌道／216 賦色及原 J 纖維全核對；等於既有雙內點 disk 代表，與 R255 非 D₅ 等價；替換須密封其餘點，未 Lean 化 | [第二混合框](c5_two_vertex_second_mixed_frame.md)、[artifact](../artifacts/c5_two_vertex_overlap/second_mixed_frame_relation.json) |
| 兩混合框共同拉回 | 完整拉回為 114 軌道，較原 J 多 54；補回 b2–b4 仍多 16，加入兩條四點條件恰還原 J；完整差集、分別延拓及原邊拒絕全保存，未 Lean 化 | [拉回與修復](c5_two_vertex_mixed_pullback.md)、[artifact](../artifacts/c5_two_vertex_overlap/mixed_frame_pullback.json) |
| 全部三點投影與四點下界 | 56 份三點投影各等於誘導原邊關係；加到兩框後仍多 16 軌道／384 賦色，保存 896 份三點延拓；原 U 無輔助變數的局部合取修復所需最大 arity 恰為四，未 Lean 化 | [三點投影報告](c5_two_vertex_ternary_projections.md)、[artifact](../artifacts/c5_two_vertex_overlap/ternary_projections.json) |
| 四點投影最少個數與全部最小組合 | 70 scopes／八種排除集合及 2,415 配對全核對；最少兩份，唯一組合為 `(a0,a1,a2,a3)` 與 `(a2,b0,b2,b4)`；三份唯一性見證／192 份原圖延拓保存，未 Lean 化 | [最小修復報告](c5_two_vertex_quaternary_repairs.md)、[artifact](../artifacts/c5_two_vertex_overlap/quaternary_repairs.json) |
| 一般拓撲與多步 | 其餘代表、指定接合政策及未來接觸範圍須另查；尚無一般充分摘要 | [拓撲界線](c5_two_vertex_overlap.md) §5 |

## 3. 精確停止點與下一個窄問題

目前最前沿是[四點投影最小修復](c5_two_vertex_quaternary_repairs.md)，
固定 R127 `(0,2)` 接 R167 `(3,1)` 的原十五點三十五邊圖，
識別 a0=b3、a2=b1，保留全部原邊、七個私有內點及共同色框：

```text
U   = (a0,a1,a2,a3,a4,b0,b2,b4)
C₁  = (a0,a4,a3,a2,b2), relation R255
C₂  = (a0,b4,b0,a2,a1), relation R1022
S_A = (a0,a1,a2,a3)
S_B = (a2,b0,b2,b4)
```

J 是原圖在 U 上的完整可延拓關係，P 是 C₁、C₂ 兩份完整關係的
共同拉回。不得把各框的分別延拓拼成同一份原圖延拓。

| 同一 U 上的關係 | 全域 S₄ 軌道 | 具名賦色 | 與 J 的差集 |
| --- | ---: | ---: | --- |
| 原 J | 60 | 1,440 | 空 |
| 兩框拉回 P | 114 | 2,736 | 54 軌道／1,296 賦色 |
| P 加全部 56 份三點投影 | 76 | 1,824 | 16 軌道／384 賦色；恰等於只補回 b2–b4 |
| P 加 S_A、S_B 的完整四點投影 | 60 | 1,440 | 空；已核對完整關係相等 |

在原 U、無輔助變數的局部條件合取模型中，新增條件的最小最大
arity 恰為四。以 **P 單獨為基底**，70 份完整四點投影的全部
2,415 個無序配對中，只有 `{S_A,S_B}` 精確修復；最少恰為兩份。
S_A 在任何四點投影修復中都不可省，S_B 只在最少兩份時被迫。
三份唯一性見證、全部差集、具名投影及原圖延拓均在證書中保存。
上述結論是固定圖的 Python 證書與紙面推論，未 Lean 化。

**下一個窄問題：同一 P 上全部 inclusion-minimal 四點修復。**
沿用八種排除集合及完整 54 軌道差集，分類個數較大、但刪掉任一份
即失效的組合，尤其不含 S_B 的替代修復。仍保留具名 scopes 與
共同色框，不遍歷新來源圖或環序；不改變最少兩份且組合唯一的結論。

拓撲證據的適用範圍仍須分開：主例已完成全部環序／外面分類；
正反向私有內點例各保存平面及來源 disk 內部互斥見證，並排除
兩原框作整圖外界。它們未分類全部嵌入。兩混合框只核對反向例
指定 rotation 的兩個五邊形面，五點 relation 替換只適用於未來
僅接觸該新框、其餘十點已密封的染色情境。

其餘三份控制拓撲、一般 class-pair 後繼表、區域重疊政策及
未來接觸／多步摘要充分性保留；一般重疊政策尚未指定。
R255／R1022 不證一般接合後的五點 relation 都屬於 132 類。
任意大小目錄完備性、拓撲摘要充分性、無假路徑的多步同餘、
生成圖類涵蓋與五內點代表命題全部保留；`K∞=K≤5` 未證。

## 4. 閱讀與重播入口

先讀[資料與規格](c5_two_vertex_overlap.md)、[八點接合報告](c5_two_vertex_join.md)、
[主例拓撲稽核](c5_two_vertex_join_topology.md)與
[私有內點拓撲](c5_two_vertex_private_topology.md)，再讀
[反向拓撲](c5_two_vertex_private_reverse_topology.md)與
[第一混合框](c5_two_vertex_mixed_frame.md)、
[第二混合框](c5_two_vertex_second_mixed_frame.md)、
[兩框共同拉回](c5_two_vertex_mixed_pullback.md)與
[全部三點投影](c5_two_vertex_ternary_projections.md)、
[四點最小修復](c5_two_vertex_quaternary_repairs.md)；最新驗證見
[發布整理與驗證紀錄](history/2026-09-30-c5-two-vertex-publish.md)。再視需要讀
[state language](state_language.md)、[local closure](local_closure.md)、
[cell enumerator](c5_cell_enumerator.md)及[既有 state 導覽](c5_state_guide.md)。

三點與四點證書超過 1 MB，依 [README 大型 artifacts 規則](../README.md#python-產生器與大型-artifacts)
只在 Git 保存生成器及 [manifest](../artifacts/MANIFEST.json)。新 clone 若尚未
重建，先依序執行下列兩個生成器；其餘本線證書直接隨 Git 保存。

```bash
python3 scripts/c5_two_vertex_ternary_projections.py
python3 scripts/c5_two_vertex_quaternary_repairs.py
python3 tools/artifacts.py status
```

以下為只讀重播；`--check` 會重算並逐 byte 比對既存證書：

```bash
git status --short --branch
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_join_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_join_topology.py --check
python3 scripts/c5_two_vertex_private_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_topology.py --check
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_second_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_second_mixed_frame.py --check
python3 scripts/c5_two_vertex_mixed_pullback.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_pullback.py --check
python3 scripts/c5_two_vertex_ternary_projections.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_ternary_projections.py --check
python3 scripts/c5_two_vertex_quaternary_repairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_quaternary_repairs.py --check
```

點對重播只依現有來源 JSON；八點重播另驗四份來源代表與六份接合圖的
完整染色。主例拓撲 checker 遍歷該圖環序／外面；正反向私有內點 checker
各核對一份平面見證、兩份對所有嵌入有效的原框阻斷及完整染色；
反向 checker 另直接重播正反向原圖的完整 J 差集。兩個混合框 checker
各驗完整纖維、原圖十內點延拓及單／雙內點代表；第二框另驗 D₅
位置作用與三項 verifier 擾動。拉回 checker 重建原 J、完整拉回與差集，
核對全部拒絕證明、分別延拓、八份條件子集合及五項 verifier 擾動。
三點 checker 重建同一 J，核對全部 56 份投影、16 份殘留軌道的
896 份三點延拓及其 21,504 份具名換色、兩份四點修復與六項 verifier 擾動。
四點 checker 重建同一 J，核對 70 份完整投影、全部 2,415 配對剩餘集合、
三份唯一性見證的 192 份延拓／4,608 份具名換色及九項 verifier 擾動。
本輪實際重播範圍見紀錄。
其餘三例的 embedding 與來源大枚舉未重驗。
不得以 1,320 份點對表取代完整 Σ；不得把 `geometry=unknown` 當 disk transition。
