# 2026-10-04：B₂，mixed-(2,2) 原短 face 的 Gallai leaf／原 K₅

使用者要求接續 B 報告 §7，只固定 W933-101／W941-139、原短 face
{1,2}，利用四原 spoke 省略全收及原 G 自己是 (5,5) q-core，研究
完整 C 的 Gallai leaf、leaf-owner tightness 及實際外部路徑；完成窄
引理或保存具名殘留即停。接手 HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`，
cwd=`/home/ray/developer/ai/math`；原工作樹已有多輪未提交成果，全數保留。
本輪未 commit／push。

[B₂ 報告](../c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py)、
[helper](../../scripts/c5_excess_two_four_spoke_mixed22_short_face_controls.py)、
[observations](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face/observations.json)
構成本層獨立證據；B 的原 checker／observations 不覆寫，既有任務 A、
P₃ 及獨立稽核成果原樣保留。

## 任意大小窄結論及精確停止點

**兩個具名短 face 均全來源排除，七身份零短-face 殘留。**
完整 R_C(x₀,x₁,y₀,y₁)、六角色 joint、shared-role 原頂點、actual
附件／supports、ownership、原 C／bridges／旁支、環序及 witnesses 保持。

全部拒絕列的原 actual 附件交集迫 min deg_C≥2；同一 leaf private
vertices 有同一 owner。Private 點內度二、完整 degree 四迫四種原
外鄰 pair 為 {1,2}、{a,1}、{b,2}、{a,b}，它們都是原外部四環的邊。
相鄰 private 點 u,w 加其原 hubs 成 K₄，C−{u,w} 沿實際外部路徑
成第五袋。Shared leaf 消耗全部四個 contacts，另一 leaf 的 nonowner
private 點實際接 {1,2}，故第五袋連通。各型得到原 K₅ minor。

另外補強 K₄-block 的原 tethers 證明：有限 Gallai bridge-side 的末端
private 點內度≤3，完整 degree 四迫它有實際外部邊。四側互斥，
與原連通 B+a+b 提供第五袋；不需假設每個 pinned root pair 逐邊 minimal。
外部 degree-list 的 Lemma 7／Corollary 8／Theorem 10 已 live 核對
[Dvořák 原 PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) 的條件。
單列 q01021 的 tightness 不足；報告明列跨完整拒絕列的交集用途。

本輪僅排兩份具名短 face，同一 W 的長 face {0,4,3} 及其他 faces
保留，原20／20必要骨架不因一個 face 排除而刪整筆。
未證 mixed22 整型、ε≥3、來源實現、一般出口或 K∞=K≤5，未新增
Lean theorem。下一窄入口為同一原骨架長 face 的完整 C／共享 contact
實際框附件與 leaf bridge；目前排程由 [Kempe 導覽](../c5_kempe_guide.md)維護。

## 固定證書的實際覆蓋

- 七種 contacts × root swap＝14張手列完整 degree 圖，所有 C 點原
  degree 四、兩 roots 各五，原支援 envelope={1,2}。
- 十列 boundary 的完整原 R_C、G、四個 G−e、G−C：840 independent
  whole-graph joins、13,440 pinned fibres（含空）、560 原 spoke 接回；
  420 root swap 核對、3,360 獨立 global S₄ 原 R_C、183,312 transported
  完整 joint witness 核對。
- 七份完整 degree 的條件式原 leaf K₅：nonowner leaf 長3／5／7、
  a-only／b-only leaf chains、Pstraight／Pcross shared leaf；70條原
  branch-bag 鄰接邊、10份逐原邊核對的長外路徑，原 block ledger 及
  C 減 private 部分的連通性保存。
- 兩份條件式 K₄ 四 tethers，原長度分別 (1,1,1,1)／(2,3,4,5)，
  20條原 K₅ 鄰接邊；這兩份未補未用 degree 邊，與完整 degree 控制
  分開標示。全部 minors 都使用原圖邊，不添 apex。

上述固定圖不宣稱 disk、目標 Σ、criticality 或來源實現；任意大小
覆蓋由紙面引理承擔，沒有重啟來源 graph catalogue。

## 重播及實際驗證

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

本輪既有 B checker 已重播通過，原 artifact bytes 保持；`lake build`
完成8,831 jobs，僅既有 lint warnings。B₂ 自己的 observations 另生成後
以 default／seed17 重算逐 byte 比對；文件、DocGraph、manifest 與
diff 實際結果在本頁末尾記錄，不預報通過。

未重跑來源 catalogue、其他 incidence、任務 A／P₃、R 系列、一般
出口／Kempe 閉包或 Lean axiom audit；沿用各原報告的證據邊界。
依 DOCUMENTATION 維持 HANDOFF 的薄導覽角色，研究線／tag 未變，
故不把新成果或重播命令塞入 HANDOFF；README、B 後續狀態、Kempe
停止點與 STATUS 直接索引已接入本層。

## 貼用摘要

> B₂已完成固定W933-101／W941-139、原01／23短face{1,2}的任意大小
> 原K₅排除，七種contact身份零短-face殘留。完整原C／四接點R_C、
> 六角色joint、actual附件與空fibres保持。Gallai leaf的private owner
> 同一，四種owner各用原外鄰K₄及實際外部路徑接成第五袋；shared
> 型由另一nonowner leaf的實際{1,2}附件接通。14完整degree圖、840
> joins／13,440fibres及7份原leaf K₅重播；紙面＋Python，未Lean化。
> 同一骨架原長face{0,4,3}、其他faces、mixed22整型及ε≥3仍保留。
> 先讀B₂報告，重播 `python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check`。

## 最終檢查紀錄

B₂ default／`PYTHONHASHSEED=17` 兩次逐 byte `--check` 均通過；
既有 B `--check` 通過，原 B artifact SHA256 為
`f7168b09b9a19957e0c3be50cbd9382cc4fa650619a563c5819962c4a3c254de`。
本層 observations 為 **7,382,053 bytes**，以既有大型 artifact 政策
僅記錄新路徑至 MANIFEST／生成 .gitignore，未刷新其他 artifacts。
記錄後 `tools/artifacts.py status` 為 **ok=140**。

`lake build` 通過（8,831 jobs，僅既有 lint warnings）；
DocGraph 通過：62 documents、213 relations、5 families，0 errors／0 notes。
兩份 B₂ 文件的12個本地連結／章節錨點與 STATUS 直接索引均通過。
全倉 docs 檢查最終通過：**523 Markdown files、5,414 local links**；
`git diff --check` 通過。

較早並行工作快照的 docs 檢查曾有三個缺失連結，均指向任務 A₂
當時尚未寫出的歷史檔；該檔由原工作補齊後，全倉重跑通過。
本輪沒有代寫任務 A 的歷史或改其證明內容。
