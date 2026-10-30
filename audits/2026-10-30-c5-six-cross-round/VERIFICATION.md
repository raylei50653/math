# 六附件跨輪研究：來源、重播與證據範圍

2026-10-30。權威報告為[無弦六附件跨輪限制](../../docs/c5_six_attachment_cross_round.md)。
本輪證明等號幾何與條件逃逸；沒有排除合法全封鎖真正四週期的六附件分支。

## 同一原圖的完整來源

- [上游 controls.json](../2026-10-30-c5-d2-separation/controls.json)保留兩源的原邊、
  有向原面、原輪轉、v／B、完整 O、全部字面 fibres、完整 Kempe actions、正規化與原交換。
- [上游 separation-certificate.json](../2026-10-30-c5-d2-separation/separation-certificate.json)
  保留全部差異分量原鄰點、原面索引、原附件、輪廓、面邊界、原環及雙面側。
- [cross-round-certificate.json](cross-round-certificate.json)以 SHA-256 與精確 JSON pointer
  綁定上游全部資料；另存兩組差異、兩側連通分量、原六環、每次交換前後的完整色態、
  全部六色對的兩側分量與全部接口附件、當下全 O 接合、連續二十交換、逐點 membership 詞、
  盤的完整 fibres、內部 Kempe actions 及合法完整逃逸路線。
- [review-certificate.json](review-certificate.json)記錄獨立重播及全部輸入／程式 SHA-256。
- [paper-review.md](paper-review.md)為獨立紙面核查；一般引理不由有限控制推定。

每源完整 O 著色均重新由原邊直接枚舉，並核等於全部共同 S₄ lifts。
每源 240 個 proper B 字逐列保留完整 fibre；其餘 784 字由原 B 邊判空。
本輪完整盤 fibre 是固定六環字後**直接枚舉全部盤原邊著色**，再附上全 O 延伸引用；
不以全圖可延伸性過濾盤解，空延伸列也必保留（這兩個控制實際為零空列）。

| 來源 | S34／S5／全封鎖 | 完整字面 O 態 | 六環盤 | 快照 | 六色對接合 | 保存的真交換 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| n17 原第0圖、v=2 | 是／是／否 | 1,296 | 1 | 16 | 96 | 13 |
| Errera | 是／否／否 | 2,400 | 2 | 24 | 288 | 20 |

n17 的 13 次是十次已完成兩輪、第三輪兩次成功指定交換及一次碰額外框點的合法測試交換。
最後一次仍是合法 Kempe 交換，但違反指定 H 步的單點框交集；第三輪 H 因此未定義。
不能把它計為完整三輪或四輪。保存的建構逃逸另從失敗前分支，沒有先執行失敗步。
六環均有完整開側等於 Q 的核查；其他原點完整留在接口或外側。
三盤合計 40 份當下色態、384 份接合，保留 102 個零接口接觸的側分量。
另逐項核 23 次同步差異更新：Errera 四組相隔兩輪比較各五步，n17 僅三步未閉前綴。
每次均保存完整當下分量 K、L、共同有效色點 J、差異出生／消失與重算分量，
核 `D_after = D_before △ ((K △ L) ∩ J)`；n17 末步不通過指定條件，沒有標成 D⁽¹⁾。
checker 另外核 216 種合法逐點代數指派的公式，不把它們稱為來源實現。

固定接口的盤 fibre 共 8 個不同環字、11 列完整盤解。
n17 的二點 Q 與 Errera 的 D⁽⁰⁾ 二點 Q 各有兩列填色，由單次內部交換互達。
Errera D⁽¹⁾ 的接口 `BCBDBA` 也有兩列填色，卻各為孤立的內部 Kempe 類，
沒有不碰接口的內部交換；多值 fibre 不能自動當成同一 Kempe 類的自由混合。
該來源的全圖兩端仍由四輪軌道相連，兩種連通概念分開記錄。

獨立 literal BFS 的各已存正規化初態最短逃逸長度為 n17 `[1,3,2]`、Errera `[3,2,3,2]`。
n17 失敗前的指定兩步後，當下 AD 分量 `{0,4}` 與 `{6,7,9,12,15,16}` 分開；
換 `{0,4}` 使 B 成 `DBDCB`。從 c₂ 起這是三次真交換的建構出口；最短出口另只需兩次。
所有保存的路線逐步重求完整分量，不插入重標或借用別態的路。

## 獨立方法與數學邊界

[checker](../../scripts/c5_six_cross_round_review.py)不匯入任何 producer。
它重跑[舊獨立 reviewer](../../scripts/c5_d2_separation_review.py)的原球面、完整 fibre、
全 actions、輪廓及原雙面側核查，再自行由原邊及完整色向量重播新增資料。
兩側接合以 union-find 獨立展開；盤 fibre 與完整 literal 逃逸 BFS 另行枚舉。
producer 使用舊 producer 的分量及原雙面側 helper，獨立 checker 不依賴這些 helper。

Errera 二十步逐點閉合只迫合成色置換固定各點初色；其中 10／16 點的合成置換非恆等。
n17 沒有四輪閉合或第二組完整差異證書，Errera 違 S5 且未全封鎖。
沒有在此生成新的抽象必要模型或分類來源；接口與色詞限制不聲稱充分。
本輪沒有重跑上游 12–24 點來源分類、使用 4CT oracle 或新增 Lean theorem。
六附件、七附件以上、P₄、週期六以上與原 Q5 的 OPEN 邊界見權威報告。

## 重播指令

```bash
python3 -B scripts/c5_six_cross_round.py --check
python3 -B scripts/c5_six_cross_round_review.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

producer 與獨立 checker 的 `--check` 均通過；`git diff --check` 通過。
本任務六份相關 Markdown 的 491 條本地連結／錨點及新報告 STATUS 直接索引通過。
正式 docs 的 DocGraph 通過：98 文件、386 關係、零 errors。

全域 `scripts/check_docs.py` 的本輪最後執行沒有通過：806 份 Markdown、10,758 條本地連結，
兩個錯誤位於工作樹其他正在新增的來源：
`docs/four_color_three_step_annotation_projection.md` 引用尚缺的
`audits/2026-10-30-three-step-annotation-projection-e1a90fe/checks.json`；
`docs/four_color_no_hub_three_branch_continuation.md` 當時未被 STATUS 直接索引。
本任務檔案沒有該檢查的錯誤；未修改其他研究線來消除這些結果。
全工作樹 DocGraph 也仍有 72 個歷史 frozen／scratch 重複 ID 錯誤，
例如 `c5.adjacent-degree5-interfaces`；正式 docs 通過不等於全域通過。
沒有執行 Lean build。詳細數學重播計數以重播 JSON 為準。

## 文件傳播

L0：更新附件分隔原報告中的六附件等號及七附件以上限制，新增跨輪權威報告與證據。
L1：Kempe guide 與 STATUS 增加直接來源入口。
L2：S5／週期四父報告連入新結果，父 P₄ 仍 OPEN；封鎖來源的量詞、偶週期及原 Q5 狀態不變。
HANDOFF 研究線未變，README 不擴散更新。上游 frozen JSON 均未修改。
