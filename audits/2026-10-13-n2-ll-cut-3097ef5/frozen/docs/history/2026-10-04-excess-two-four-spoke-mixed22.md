# 2026-10-04：任務 B，四-spoke mixed-(2,2) 無 unary 的原身份與窄化約

使用者要求與任務 A 分開，接續 disjoint-pairs 明列保留的原來源：
固定完整 Σ933／941、ε=2、相鄰唯一 mixed、兩側各兩 spokes、原 ab、
mixed incidence=(2,2)、沒有 unary。接手 HEAD=`0e38127`，
cwd=`/home/ray/developer/ai/math`；保留原未提交工作樹，本輪未 commit／push。

[B 報告](../c5_excess_two_mixed_core_four_spoke_mixed22.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py)、
[完整 joint helper](../../scripts/c5_excess_two_four_spoke_mixed22_joint_controls.py)、
[observations](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json)
是獨立證據層；沒有修改任務 A 的 theorem、checker 或數學內容。

## 交付與停止點

- 七份具名原 contacts 身份：D4、S00、S01、S10、S11、Pstraight、Pcross。
  同側不同；跨側共享逐份列明，完整 R_C 四座標、六角色 joint、實際
  附件、原頂點與完整 coloring witnesses 保留。
- G−C 的兩 roots degree 三，直接由每側≥2可用色證 Ω；它不是 q-core。
  原 q-core 的九種合法省略身份全部列明，mixed22不能省略。
- 任意大小窄引理：每條原 spoke 省略均 Ω。若拒絕，M 自己 minimal，
  原 M−另一root=C+降度root 有三個不同原 contacts，違反既有 two-spoke
  三接點排除；marked root 內度二，沒有借 A 的 leaf／unary 論證。
  因此原每個拒絕 q-core 就是 G (5,5)。
- 同色省略迫兩側 spoke pairs 皆為原框邊；47／75必要骨架各至25，
  equal pair 各五份由原 sealed triangle／三-hub 排除，保留20／20。
  共點 unequal 的 C 留在四框點長 face；disjoint 的短pair face及三點
  長face都保留，沒有直接套 unary short-support。
- 完整同列 root-pair 的拒絕 lists 給任意大小 tightness；原 actual
  附件子集與 face 逐份保存。Private leaf odd-cycle 的 missing-color
  signature 迫原 owner 身份一致。這是必要限制，沒有來源實現宣稱。

保存 W933-101／W941-139（原01／23，兩原 faces）與 W933-98／W941-135
（原01／04，四框點長 face）等全部具名必要見證。保留933原04／12的
長face共享contact附件{4}；不可一概宣稱原 C min degree≥2。
條件式 marked original K₅ 共14份，原 triangle=(a,x₀,x₁)、偶長兩臂，
只是在反設省略圖拒絕下提取；未補未用 arm 邊，不作完整 degree 圖。

固定控制是28張完整 degree 圖：七身份×short/long原C×root swap，
共1,680 independent full joins、26,880 pinned fibres、1,120 carrier
joins及1,120原spoke接回、840 root swaps、40,320全域S₄ witnesses、
6,720獨立S₄原R_C。Control20、Pstraight、q01012、rootcolors(2,3)
保存真實 marginal 假接受／完整四接點 fibre 空的反例。
控制圖不宣稱 disk、target Σ 或 criticality；short/long 不宣稱等價。

## 實際驗證與未重跑範圍

以下本輪均已執行：

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
python3 scripts/c5_two_spoke_three_contacts.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py record artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json
```

兩次 B checker byte-check、既有三接點80 minors／63 palette／512 parity
payload 重播均通過。新 B checker 亦唯讀重算既有three-hub payload相同，
來源 artifact bytes SHA256綁定，未覆寫原產物。25獨立原骨架共有
2,320 rotation assignments／60 disk rotations，原equal有四rotations、
共點unequal兩份、disjoint兩份；12,200共同D₅rootpair控制及122
原frame swaps通過。`lake build` 完成8,831 jobs，僅既有lint warnings；
沒有新增Lean theorem，本頁紙面topology未因此形式化。

新 observations 約26.6 MB，依既有大型artifact政策加入MANIFEST及
生成.gitignore；只記錄本層，不刷新舊artifacts。HANDOFF研究線未增減，
依DOCUMENTATION保持薄導覽不另加研究摘要；README增加B的獨立導航。
文件、DocGraph、manifest現況與diff檢查結果在本頁末尾記錄。

未重跑來源 catalogue、degree-6全分拆、其他mixed11／任務A全證書、
R系列、一般出口／Kempe閉包或Lean axiom audit；沿用其原報告依賴。
外部degree-list只核對Dvořák Lemma7／Theorem10的原前提，不把其原文
查證與新任意大小定理的Lean形式化混稱。

## 貼用摘要

> 任務B已獨立完成mixed22無unary的七contact身份及窄引理：四原spoke
> 省略各自Ω；每個原拒絕q-core必是原G (5,5)。保持完整原R_C四接點、
> 同框六角色joint與全witness。47／75骨架各縮至25相鄰pairs，equal
> 各排5，20／20原face必要見證保留。28完整degree圖、1,680joins／
> 26,880fibres及14條件式原K₅核對；不借unary crosscut、不宣稱來源實現
> 或ε≥3。B下一窄入口是01／23短face的原Gallai leaf，或933原04／12長
> face共享contact附件{4}的leaf bridge。先讀B報告，重播
> `python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check`。

目前停止點及任務A/B入口由 [Kempe 導覽](../c5_kempe_guide.md)維護。

## 文件與artifact檢查現況

`python3 tools/docgraph check` 通過：62 documents、213 relations、5 families，
0 errors／0 notes。`git diff --check` 通過。
`uv run --with-requirements requirements.txt python tools/artifacts.py status`
在本輪記錄後為 **ok=138**，新 B artifact digest／producer fingerprint 已登錄。

全倉 `python3 scripts/check_docs.py` 已執行，但並行工作途中未通過。
最後快照為514 Markdown files、5,298 local links、四個錯誤：
`mixed12` 報告及Kempe導覽所連的A歷史尚缺；
`c5_mixed_p3_common_endpoint.md` 所連歷史尚缺且當時未由STATUS直接索引。
這些文件在B執行期間由其他工作出現，保持原樣，不替A／P₃虛構歷史。
因此不報全倉文件檢查通過。

另以既有 `check_docs.links`／`anchors` 對B報告與B歷史逐連結核對，
**兩文件15個本地連結與章節錨點全通過，兩者STATUS直接索引皆存在**。
B完整交付及checkers均已完成；上述全倉錯誤由各並行工作的文件完成後處理。
