# 2026-10-03：ε=2 四-spoke 原 unary 短 face 與非 critical 接線

使用者要求「繼續推進 ε ≥ 3」。接手 `0e38127`，工作樹乾淨，
cwd=`/home/ray/developer/ai/math`。本輪依 Kempe 導覽處理原
01／02、source indices=97／133、root 交換=111／153；
沒有重開來源圖 catalogue，未 commit／push。

## 結果與原身份

[新報告](../c5_excess_two_mixed_core_four_spoke_short_face.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_short_face.py)、
[joint helper](../../scripts/c5_excess_two_four_spoke_short_face_joint_controls.py)、
[證書](../../artifacts/c5_excess_two_mixed_core_four_spoke_short_face/observations.json)
保存下列窄進展。

固定完整 Σ=933／941 或整圖 D₅ 像、Σ edge-minimal、指定有序
induced-C₅ disk、有效 H 連通、ε=2，限定相鄰雙 degree-5 roots，
其餘有效內點完整 degree 四、唯一 mixed incidence-(1,1)，各側
一原 unary 與兩原 spokes。原 C／U／V、actual attachments／supports、
有序 contacts、ownership、所有原邊、嵌入環序及字面色框保持。

原 crosscuts 證明 01／02 的 a-side U 只能位於包絡 01、0 或 12
的同一固定 face。原外路徑 a–b–2 或原 spoke a–0 滿足既有
短支援引理，逐列 F_U=∅。因此只替換整份原 U 的 coloring，
保留 roots 與完整 C／V witnesses，即可接回原 au；
Σ(G−au)=Σ(G) 與 criticality 矛盾。五角色投影相等，不宣稱
六角色 joint 相等；無須先證 mixed relation 的所有 pair 可延拓。

| 同一候選必要域 | 933 | 941 |
| --- | ---: | ---: |
| 原 unequal-pair frames | 40 | 66 |
| 本輪短 face 任意大小來源排除 | **8** | **16** |
| 剩餘共用一框點 | 18 | 32 |
| 剩餘不相交 | 14 | 18 |
| 剩餘 unequal 合計 | **32** | **50** |

74 共用一點骨架各檢查 96 rotations，共 7,104 assignments／
148 份原 C₅ 為外框的 disk rotations；逐份保存原 edges、root
order、spokes、兩份 rotations、所有 incident-face 包絡與原 L。
24 原 root 交換、7,200 整圖 D₅／列／L 搬運皆核對。沿用短支援
的 local／three-hub 完整数學 payload 唯讀重算相同。

24 張完整 degree 控制圖保存 C 共鄰 singleton、不同接點 edge／
triangle、四份 U／V 形狀配對及 root 交換。九種原圖變體的
2,160 完整 joints、34,560 pinned root-pair fibres（含空）、
1,680 原邊接回及 1,080 root 交換與獨立全圖回溯相同。
108 份 |R_U|≥2 列核對五角色投影相等，3,736 原 U 替換 witnesses
逐完整原邊驗證，原 U 外所有頂點保持。58 singleton 投影失敗
列、au／spoke 接回阻塞、C marginal collision 與短支援 U 的
具體原 K₅ 負控制皆保存。這些控制圖不聲稱 disk、候選 Σ 或
Σ-critical；任意大小來源排除由紙面證明承擔，Python 只核對固定域。

## 實際驗證與產物

新 checker 的預設 hashseed 及 17 的逐 byte replay 均通過；
直接依賴的短支援與共用 pair checker 的 hashseed=17 replay 均通過。
degree-list 外部講義重新取得，核對 Lemma 7 的 slack／tightness
及 Theorem 10 的 degree-assignment／blockwise-uniform 前提。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings，沒有新 Lean theorem。新 observations 為
**33,200,245 bytes**，SHA256
`ac9bfe98fdb11894584b7ef71bc4f38ac146c14ad0363869b579faa38adf8630`；
依既有政策本地保留，MANIFEST／.gitignore 登錄 producer、依賴
與 fingerprints。所有前序 artifacts 原樣保留，文件更新不要求
覆寫既有數學證書；歷史 byte-check／文件 hash 漂移沿用前序紀錄。

README、STATUS、Kempe 導覽、全線整合頁及共用 pair 後續說明
同步。HANDOFF 研究線與 tags 未變，依治理維持薄索引。文件檢查
通過 502 份 Markdown／5,148 個本地連結，anchors、index、handoff
均通過。DocGraph 通過 62 documents／213 relations／5 families，
零 errors／notes；產物 status 為 ok=133，無 missing／changed／stale；
git diff --check 通過。獨立紙面審查未發現實質問題。這些檢查不
形式化本輪 topology，也不建立來源實現。

未重跑 degree-6 全分拆、單 spoke 舊 byte-check、singles 漂移
audit、R 系列、weak-deletion／Kempe closure、全倉來源 catalogue
或 Lean axiom audit，不宣稱全倉研究重新驗證。

## 停止點與貼用摘要

**共同下界仍是 ε≥2；ε≥3 未證。** 本輪完成選定 01／02 及
同機制 8／16 份來源排除，整個 (2,2)、mixed-(1,1) 加各側一 unary
仍有 32／50 份。下一窄入口原 01／04，indices=98／135，
root 交換=126／195；兩側都仍有長 face，不能套所有 incident
faces 都短的前提。其他 incidence、較少 spokes、單省略、原
(5,5) q-core、多 mixed／no-mixed／非相鄰 roots 及 unary 側例外
保留。一般出口、來源實現及 K∞=K≤5 未證；目前排程見
[Kempe 導覽](../c5_kempe_guide.md)。

```text
cwd=/home/ray/developer/ai/math；先讀HANDOFF/STATUS/Kempe導覽，再查即時Git。
基準0e38127；本輪沒有commit/push。
固定完整Σ=933/941、edge-minimal induced-C5 disk；共同ε≥2不變。
四spoke(2,2)、mixed(1,1)+各側一unary：原01/02及交換97/111、133/153全排。
原a-side unary的faces包絡01、0、12；原a-b-2/a-0路徑接短支援迫au非critical。
保留原C/U/V與完整六角色joint；五角色投影相等，不稱六joint相等。
同機制排8/16；unequal從40/66到32/50，共一點18/32、不相交14/18。
新checker：python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check。
74原骨架7104rotations，24全degree圖2160joints/34560fibres、3736原U替換witnesses。
新checker兩hashseed、短支援、共用pair及lake build通過。
下一原spokes01/04，indices98/135、交換126/195；保留同一長face的actual supports/共同lifts。
其他incidence/較少spokes/單省略/(5,5)/多mixed/no-mixed/非相鄰保留。
紙面+Python；ε≥3、一般出口、來源實現、新Lean theorem及K∞=K≤5未證。
```
