# 2026-10-04：B₄，933 原 04／12 的 shared-{4} 原 cut parity

使用者指定接續 B／B₃ 與 Kempe §3，先從原 artifact 確定 933、spokes
04／12 的精確 frame、長 face 及 shared-contact 身份，僅完成實際框附件
{4} 這支；保持完整 C、四接點 relation、root-pair fibres、shared bridges
及原 (5,5) q-core。接手 cwd=`/home/ray/developer/ai/math`，
HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`；原工作樹多輪未提交
成果全部保持。本輪未 commit／push。

[B₄報告](../c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py)、
[helper](../../scripts/c5_excess_two_four_spoke_mixed22_shared4_controls.py)、
[observations](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4/observations.json)
構成獨立本層證據。原 B／B₃ producers、artifacts、七身份、具名必要表
與稽核歷史不改寫；B／B₃頁首加後續範圍，README、Kempe、STATUS 與
synthesis 接入新報告。HANDOFF 研究線／tags未改，依 DOCUMENTATION
保持薄導覽；沒有向它加入新輪次或 checker 命令。

## 任意大小窄結論與證據層

精確入口是 **W933-129**，原a=5、b=6、spokes04／12，長圈
2–b–a–4–3–2、envelope={2,3,4}，原兩份disk rotations均保存。
指定shared v接{4}時原deg_C=1，四拒絕rows的11合法pairs均tight
singleton；不能套用B₃的shared-leaf strict slack或min-degree二分類。
刪v、固定原leaf色後，原neighbor t的13附件候選跨143row/pair檢查，
以strict slack排5份，8份保留到下一原圖論證，沒有憑必要表刪來源。

K=C−v非空連通，原完整degree四與原cut給
`4|K|=2|E(K)|+3+n_B`：三條固定外接恰為ax*、by*、vt，n_B是全部
實際K–B邊。故n_B奇數且至少一；雙shared的x*=y*仍是兩條不同
root邊。五袋{a},{b},{v},原B,整份K連通互斥，十對鄰接均有原邊，
直接給原K₅ minor。六shared身份／八指定選擇此附件支全排，零殘留。
涵蓋C僅兩點、任意原bridges與旁支，不依賴Gallai分類或固定pair minimality。
原長face插入av、bv、4v的108rotation controls另交叉核對K被封abv，
若保持disk則n_B=0，與完整degree parity矛盾；主K₅證明不需這條化約。

外部[Dvořák Lemma 7](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
僅供connected-slack說明，原PDF已live核對；主要來源排除是原degree
與connected bags的紙面證明。Python檢查固定完整圖的relations、原
路徑與minor，沒有列舉來源catalogue。未新增Lean theorem，沒有把
`lake build`稱為本頁拓撲形式化。

完整原C、actual附件、四接點relation、全部空／非空fibres與原bridge
保持，minor不作其不變量；只登記W933-129指定shared-{4}附件支排除。
D4、shared空附件、其餘contact附件／短face、其他骨架與mixed22整型
均保留；ε≥3、來源實現、一般出口與K∞=K≤5未證。在此窄支停止。

## 固定控制覆蓋

- 40份完整degree原圖、6shared身份、8指定shared選擇；包括8份最小
  雙shared兩點C edge、短／較長原cycle接shared leaf bridge與root swaps。
- 每圖的v原C-degree一，原vt刪除後C斷開；完整K的三固定外接與
  奇數實際框附件逐份核對。40原K₅、400原鄰接，保存B路徑
  4–3–2–1–0及K從t到剩餘contacts／實際框附件的原路徑。
- 2,400直接整圖joins、38,400獨立pinned fibres，含29,768空纖維；
  保存5,336個完整R_C tuples、25,416個完整joint tuples與整份witnesses。
- 1,600原spoke接回、1,200literal root-swap variant controls，9,600
  獨立重算globalS₄ R_C及57,600 variant witness控制組，每組核對所有
  完整joint witnesses。Root swaps只屬控制，不新增其他frame排除。

這些圖都是非平面原K₅正控制，不宣稱disk、Σ=933、Σ-critical或來源
實現；短／長C是不同原圖，沒有relation等價宣稱。

## 重播與驗證範圍

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

未重跑任務A／P₃、其他incidence、D–D₄整合稽核、R系列、一般出口／
Kempe閉包或Lean axiom audit；沿用各原報告的證據邊界。
舊稽核截點與停止點保持當輪語境，沒有覆寫成B₄結論。
實際檢查結果記在下節。

## 貼用摘要

> B₄完成W933-129、原933 04／12長face{2,3,4}的指定shared-{4}窄支。
> 真正shared leaf在全部11原pairs均tight；bridge鄰點13候選跨143pairs
> 以slack排5留8。整份K=C−v的原cut parity迫奇數框附件，五原bags
> {a},{b},{v},原B,整份K給原K₅，六shared身份／八指定選擇此支零殘留。
> 40完整degree圖、2,400joins／38,400fibres、40原K₅與actual paths保持。
> 完整C／四接點relation／空fibres／bridges及(5,5)q-core不作minor不變量。
> 同份骨架其他附件／身份、其他骨架與mixed22整型保留；ε≥3未證。
> 紙面＋Python、未Lean化、未commit／push；在此窄支停止。
> 重播 `python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py --check`。

## 最終檢查紀錄

B₄ default／`PYTHONHASHSEED=17` 兩次逐byte `--check` 通過；
原B／B₃ `--check` 通過。兩份舊artifact bytes保持，SHA256分別為
`f7168b09b9a19957e0c3be50cbd9382cc4fa650619a563c5819962c4a3c254de`、
`513c582f1067306ae67d8ef1fab46ba6c6fe5889923c95923688ba4a2aaaebd7`。
新B₄ observations為 **35,337,366 bytes**，SHA256
`75031e3eee07a05a65aaba31c7a6d659ac4c2620340809dd8dbf2ae1227d58c0`。
大型artifact只針對新B₄路徑`record`，登記MANIFEST並生成.gitignore；
record前的144個file entries、139個fingerprints及139個producer entries
全部原樣，只新增本B₄的一份file／fingerprint／producer。
記錄後artifact status通過：**ok=145**。

`lake build`通過（8,831 jobs，僅既有lint warnings）；DocGraph通過：
62 documents、213 relations、5 families，0 errors／0 notes。
兩份新scripts的py_compile及`git diff --check`通過。
全倉文件檢查初次有四個缺失連結，均指另一研究尚未生成的
P₃雙框點兩unary歷史文件；該文件隨原工作補齊後，重跑通過：
**536 Markdown files、5,565 local links**，anchors／STATUS index／
薄HANDOFF全部通過。本輪沒有代寫其他分支結論。

獨立read-only稽核未匯入本層checker／helper solver，從原edges自行
BFS及完整MRV枚舉，重算400份R_C與2,400份variant joints，全部一致。
40圖的原degree、指定v實際附件／leaf／bridge、完整K cut及parity、
40原K₅／400原鄰接／752保存actual paths全數通過。
所有38,400 pinned fibres完整，29,768空fibres；5,336R_C tuples、
25,416joint tuples及重複pinned witnesses共56,168份合法性核對通過。
另獨立重列所有actual附件，重現13候選／143crosslists的排5留8；
11份leaf singleton、108rotation insertions／兩份extensions、原frame
完整相等及六份SHA256 input bindings均通過。
