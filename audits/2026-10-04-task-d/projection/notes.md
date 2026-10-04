# 任務 D 獨立子稽核：投影、完整 joint、原 witness 與沿用範圍

稽核來源：`/tmp/math-task-d-audit-_l2g06k7/snapshot` 的固定唯讀副本。原工作樹、共用文件與歷史 artifacts 均未修改。本子稽核新增的程式、結果與紀錄只位於 `projection/`。

## 結論

最新五輪及前置 equal-pair 的關係宣稱，在現行報告、helper、artifact 與現行 synthesis／Kempe 導覽間一致。沒有發現把四／五角色投影相等提升成完整六角色相等的實作或文件錯誤；完整圖 controls 中有可獨立重現的反例，證明這個區分不可省略。

本子稽核不為任意大小 Gallai／Jordan／短支援定理新增形式化證明，不核定固定 graphs 的 disk／候選完整 Σ／Σ-criticality 實現。有限證據與紙面一般步驟在報告中已分開。

## 實際執行

命令：

```bash
python3 /tmp/math-task-d-audit-_l2g06k7/projection/audit_projection.py \
  --repo /tmp/math-task-d-audit-_l2g06k7/snapshot \
  --output /tmp/math-task-d-audit-_l2g06k7/projection
```

最終執行 exit 0。完整輸出為 `projection/run.log`、`projection/results.json`。程式不匯入任何 repo 的枚舉器、joint helper 或 witness validator；由新寫的 MRV 回溯，獨立列舉每個原分量與每個圖變體的完整 contact relation，與 serialized artifacts 比對。第一輪測試中的稽核程式 schema 鍵名錯誤已修正，沒有改動被稽核程式或 artifacts。

| 固定 controls | 完整 degree 圖 | 獨立全圖 joint | 全部 pinned fibres | 其中空 fibres | 原 full coloring witnesses | 原邊 literal filter 接回 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| equal_pair | 36 | 2,520 | 40,320 | 33,110 | 43,150 | 1,800 |
| short_face | 24 | 2,160 | 34,560 | 27,614 | 42,494 | 1,680 |
| long_face | 18 | 1,620 | 25,920 | 22,336 | 12,040 | 1,260 |
| crosscut | 18 | 720 | 11,520 | 10,368 | 10,488 | 360 |
| short_arc | 12 | 1,320 | 21,120 | 18,524 | 8,860 | 1,080 |
| 合計 | 108 | 8,340 | 133,440 | 111,952 | 117,032 | 6,180 |

另有 3,240 原分量 relation 獨立枚舉、9,440 分量 coloring witness 逐邊驗證，以及 4,170 次實際全圖 root relabel 的 edges／ports／完整 joint／完整 fibres 核對。每個變體都明存 16 個字面 root-color pairs；空 fibres 不被省略。38 張共鄰控制圖的 x=y 均保持同一原頂點，六角色仍含兩個相等命名欄位，不創建第二個 contact 頂點。

表中的「原邊 literal filter 接回」是先將省略圖完整 tuples 篩選為满足被省略的那條原邊，再與原圖完整 joint 相等；不是省略圖與原圖原先的六角色 joint 相等。完整 stored relations 也表示各自的完整關係已保存、而非兩個圖的關係彼此相等。

原分量的 vertices、internal edges、actual attachments、contacts、owners 與 root contact edges 重建後，逐張等於原圖 edges；a,b degree 5，其他有效內點 degree 4。Component coloring、全圖 coloring 與原 boundary 色框相同，未逐分量重新正規化。

## 四／五／六角色合約

| 階段 | 精確保留範圍 | 獨立檢查結果 | 證據邊界 |
| --- | --- | --- | --- |
| equal_pair | π(a,b,u,v) J_G = J_(G−C)；原 C witness 接回 | 固定 degree 圖的六角色／G−C 四角色完整 relation 及 literal 恢復通過 | 任意大小等式依賴 paper sealed triangle 與三-hub 前提；helper 明說不測式(6)的一般幾何結論 |
| short_face | 忘 U 的 contact；保留 a,b,x,y,v 五角色 | 108 個有至少兩個 U contact colors 的列均投影相等；3,736 份 U 替換，U 外逐點不變；58 列 singleton 投影失敗保留 | 不能從任意 degree 圖推定短支援避色或 planarity |
| long_face | 忘 U 或 V 的 contact，保留其餘五角色 | U／V 的 66／90 個多色列投影相等；680／1,012 份替換，分量外逐點不變；72／52 列 singleton 投影失敗保留 | 幾何先在 β 前固定短的原 W；不逐列換 owner 或支援 |
| crosscut | 忘原 C contacts；保留 a,b,u,v 四角色 | 540 個等式與 7,752 份原 C 替換通過；C 外逐點不變 | G−ax／G−by 的 180 列各全部四角色相等，六角色各全部不相等 |
| short_arc | q=01021 的指定完整六角色 tuple 與原全圖 witness | 12 份完整 q coloring 通過；完整抽象 schema 證據如下 | 不主張所有異色 root pairs 可延拓，也不主張刪邊六角色相等 |
| disjoint_pairs | 同一短 unary 的五角色投影；原 C 與另一 unary witness 保持 | 沿用 long_face conditional operator；沒有新增本輪 disjoint-spoke degree 圖 | 算子前提是同一原 unary relation 至少兩色；前提由本輪紙面 geometry＋短支援取得 |

具體反例：crosscut control 0、row 0 (`01012`) 的 G−ax tuple `(3,2,3,0,2,3)`，違反原 a≠x，所以不在原六角色 joint；保留 `(a,b,u,v)` 的投影仍能接回原 C。short_face control 0、row 1 (`01021`) 的 G−au tuple `(2,1,3,3,2,2)`，違反原 a≠u；五角色投影仍相等。均由獨立全圖枚舉確認。

short-arc 抽象 schema 另從全部 65,535 份非空 subsets of 16 ordered tuples 獨立枚舉，而非沿用原 10-orbit 生成法：恰 963 份同時 1↔3 stable、F_C=∅ 的完整 relations，其中恰 5 份只有 diagonal tuples；每份 A=2,D=1／3 的完整 guarded fibres 相符，全部 101,115 選定六角色 tuple 都符合相同 C relation、原 U／V palettes 及所有原 guards。這個數目是 963×7×15 個選定 tuple witnesses；沒有證成 963 份 relations 均可由來源圖實現。

## 可回查證據

- `docs/c5_excess_two_mixed_core_four_spoke_equal_pair.md:152-160` 明列四角色式(6)；`:196-201` 明說固定 graphs 不核對該任意大小結論。
- `docs/c5_excess_two_mixed_core_four_spoke_short_face.md:124-132` 明列五角色及否定六角色等式；helper `scripts/c5_excess_two_four_spoke_short_face_joint_controls.py:150-205` 以同一完整 U relation 替換、驗證 outside 不變並保存 singleton 負控制。
- `docs/c5_excess_two_mixed_core_four_spoke_long_face.md:126-142` 與 helper `scripts/c5_excess_two_four_spoke_long_face_joint_controls.py:97-138` 精確忘一個 unary role。
- `docs/c5_excess_two_mixed_core_four_spoke_crosscut.md:149-167` 與 helper `scripts/c5_excess_two_four_spoke_crosscut_joint_controls.py:89-122` 明列四角色、完整 C 替換、六角色可異。
- `docs/c5_excess_two_mixed_core_four_spoke_short_arc.md:123-126,162-173` 區分指定 q 出口、抽象 tuple witnesses 與整圖 witnesses；helper `scripts/c5_excess_two_four_spoke_short_arc_joint_controls.py:110-151` 保存所有 root-pair guards 及局部負控制。
- `docs/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md:91-105,125-127`；checker `scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py:271-274,321-336` 明說完整重算原 01／04 helper payload，沿用 conditional operator，且否定新 disjoint graphs 主張。
- 現行 `docs/c5_kempe_guide.md:61-63`、`docs/c5_research_synthesis.md:40-46` 的四／六／五角色界線相符，並保留 arbitrary-size paper／fixed Python 邊界。

## 建議修訂清單（本子稽核不套用）

1. 非必要的措辭澄清：`docs/c5_excess_two_mixed_core_four_spoke_equal_pair.md:152` 的「完整 relation 等式」可改成「忘記 C contacts 後的四角色完整 relation 等式」。現有公式正確，這只降低讀者把「完整」理解為六角色等式的機會。
2. 非必要的導覽澄清：`docs/c5_research_synthesis.md:24,27` 的「原 witness 保持」可明寫「被替換的 unary 外（含完整 C 與另一 unary）的原 witness 逐點保持；僅五角色投影相等」。主報告已有精確表述，現有摘要不構成錯誤。
3. 保存本輪獨立反例／統計入口，以後若新增「full joint equality」宣稱，應核對這些 literal tuples，而非只檢查 Σ 或 root marginals。

歷史 hash 漂移、按各報告執行的 `--check` 與 synthesis 的 stale ε=1 段落由主稽核整合。不能為讓 byte-check 通過覆寫歷史 artifacts；本子稽核沒有作這種覆寫。
