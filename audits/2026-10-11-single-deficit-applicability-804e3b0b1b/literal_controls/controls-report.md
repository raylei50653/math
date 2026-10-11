# 單缺額適用性：三個固定 literal controls

這份交付只校準前提與同源資料的保存。**新增 actual N45 來源與身份排除皆為 0。**
LIT-SD-A 尚無本輪凍結、已通過的 A 結論，故其推論仍 conditional；以下 Python 不能代替 A。

權威 BASE 為 `4dd11f422c6fa49265a412085116b088786d0344`。指定六份文件及三份補充文件的
凍結 SHA-256 見 [inputs.json](inputs.json)。本子目錄的 checker 只使用 Python 標準庫，
不匯入既有研究 checker、不讀寫既有證書、不搜尋圖族。

## 判讀及證据分層

| 控制 | 有限 verdict | 實际內容 | N45 target |
| --- | --- | --- | --- |
| `ARTICULATION_M` | counterexample | β-minimal、連通、恰一個 degree5，H 的具名割點為 s；因此這三項本身不推出二連通 | not triggered：r–s 相鄰、Σ=56，並有原圖 K5 minor，非 disk |
| `TRIANGLE_M`、`LONG_M` | triggered and holds | 各自 β-minimal；r=4、s=5、其餘=4；H 二連通、d_H(s)=2、C=H−s 是 Gallai tree，r/a 是 C 的具名割點 | not triggered：不是完整Σ933／941原來源 |
| 兩圖的共同 (r,s) relation | triggered and holds | 全240 proper literal rows、全部16根pins（含空fibres）逐列相同 | 不證 actual 來源，不證 graph replacement |
| 保留頂點縮 C5 成 triangle 的 full lift 投影 | counterexample | 同一字面色框與共同根關係仍相同，但72列投影失敗，且存在無來源 preimage 的目標 assignments | 不可把內部 Gallai 結構／根關係升為完整 lifts 保存 |
| `G_test=M_test+rb2` 的 literal spoke filter | triggered and holds | 每列 G 全 lifts 恰為 X=M 全 lifts 中 r≠b2 的所有原 assignments；附每列完整索引 | not triggered：Σ(G)=Σ(M)=266，原 rb2 非 Σ-critical |
| 腐證書省略一個空根fibre | triggered and holds | replay 回 exit 1；未把省略欄位當成空集合或默許 | 校準完整性，不裁決任意大小定理 |
| 單缺額 A 定理 | not triggered | 沒有已採納 A 證明可由本 checker 認證 | 保持 conditional |

`ARTICULATION_M` **不是「全部 N45 前提仍不二連通」的反例**。它精確反駁只從
β-minimality、連通性及完整 degree profile 推得二連通的捷徑。其 disk 缺失前提明確保留。

## 原邊、M 自身 degrees 與具名割點

全圖均有同一有序 induced 外框 `(b0,b1,b2,b3,b4)` 及 literal 四色 `(0,1,2,3)`。
共同 β=`(0,1,0,1,2)`、未用色 D=3。完整 vertices／edges、每點實際 boundary 鄰居、
ordered contacts、actual supports、ownership、原 bridges 與 combinatorial rotation 在證書內，
rotation 只代表明列的 cyclic neighbor order；未宣稱它是 disk embedding。

| 图 | G_test／X_test／M_test | M 自身完整 degrees | H 與 C 的證據 |
| --- | --- | --- | --- |
| Articulation | 獨立 T=M_test；不指定 N45 原 G 或 derivative | s=5；r,p,u,v=4 | H 為 triangles s–r–p–s 及 s–u–v–s；刪 s 變 {r,p}、{u,v}；d_H(s)=4 |
| Triangle | G_test=M_test+rb2；X_test=G_test−rb2=M_test | s=5；p,r,a,c,q=4 | H 無割點；C 為 p–r、triangle r–a–c–r、a–q；C 割點 r,a；原 ordered s contacts=(p,q) |
| Long | G_test=M_test+rb2；X_test=G_test−rb2=M_test | s=5；p,r,a,c,q,x,y=4 | H 無割點；C 為 p–r、C5 r–x–a–y–c–r、a–q；C 割點 r,a；原 ordered s contacts=(p,q) |

Triangle／Long 的 G_test 自身 r,s=5 且非相鄰；其餘內點=4。但只補 rb2 沒有新增接受列，
故 G_test 的 rb2 不滿足原 Σ-criticality，不能冒充已知 N45 actual source。
M_test 的 β-minimality 則逐項由全部 retained 非框邊刪除後的完整 β coloring 確認；
三份 M 共57份逐邊完整見證。M 的 β-criticality 蘊含它自己 Σ-critical，
不能逆向把此結論搬到 G_test。

Articulation 的非 disk 證據是原圖中的五個互斥連通 bags：
`{s}`、`{r}`、`{p}`、`{b4}`、`{b0,b1,b2,b3,u}`。
每對 bags 均有原鄰接；checker 逐一驗証，得到 K5 minor。
這個 non-disk controls 保留，沒有從樣本移除以造成「全部都二連通」的假象。

## 完整 lift 保存失敗的 literal 見證

在 `LONG_M` 的同一原色框，boundary row 是 `(0,1,0,2,1)`。
完整 proper coloring 為

```
b0=0 b1=1 b2=0 b3=2 b4=1
s=2 p=3 r=0 a=2 c=2 q=3 x=3 y=3
```

來源 C 的 r–x–a–y–c–r 全部原邊 proper。保留 r,a,c 縮到 `TRIANGLE_M` 時新增 a–c 邊，
但同一完整 lift 在 a,c 都用2，所以不能延續成目標 proper lift。
同列的一個目標 coloring 改 c=3 能 proper，卻沒有相應來源 preimage。
完整 witness 見 [projection-witness.json](projection-witness.json)；全部72列失敗及全部
來源／目標完整 lifts 保存於 [observations-v3.json](observations-v3.json)。

這個控制更精確地顯示：**即使完整 (r,s) relation 逐列保持，原完整 assignments 仍不保持**。
本輪没有要求任何獨立 pieces 色正規化，也没有使用 marginals 判定延拓。

## 既有精確反例壓力

- 凍結 `docs/c5_degree5_shared_cycle_roots.md` §3：來源 C5 lists
  `[15,10,3,10,3]` 的 root 集為15，保留 r 與兩接點的 triangle `[15,10,10]` 為5；
  配另一環後交集3變1，雖四列可延拓布林值不變。此既有 list control 不等於 actual N45 source。
- 凍結 `docs/c5_degree5_long_triangle_roots.md` §5：C5 lists
  `[{C},AB,{C},AB,AB]` 可著色，兩個 pinned 接點縮成相鄰 triangle 點後不可著色；
  任意二點 pinning 不由四列 root 介面等價推出。
- 凍結 `docs/c5_degree5_interfaces.md` §§1–4：固定同一根色後才接合原分量；
  完整 R_C 可作 natural join，F_C 是一種根接合的投影，不是 R_C 可逆表示。

以上文件是反例壓力，沒有在本輪重播既有大型有限控制，也沒有重開已採納的限定排除。

## 最小橋接的驗收界線

本控制支持把後續義務限於 **actual M 的具名 block 鏈與既有 R 分支的前提映射**：
先逐項核 M 自己的 degree profile、H 二連通及 d_H(s)=2，再在同一原圖辨識 C=H−s 的
兩個原 s contacts、橋邊、blocks、actual attachments／ownership／rotation。
這是結構辨識義務；不能預加「縮圖保持完整 Σ／root fibres／full lifts」。
若後續需要圖替換，必須另給同源全 relations、完整空fibres與preimages／full lifts證據，
或使用只承擔拓撲目的的原 branch sets 明確避開染色替換主張。

成功停止點：一份 actual-source 條件下、同圖同色框的既有 R 前提映射，精確列出仍未覆蓋身份。
失敗停止點：具名割點、缺少 M= X、度數改變、缺少 actual attachments 或完整接合前提，均維持
conditional／unknown；本轮 toy 零來源觸發不是來源排除。

## 重播、負控制及 retained generations

在 repo 根目錄运行：

```bash
python3 audits/2026-10-11-single-deficit-applicability-804e3b0b1b/literal_controls/check_literal_controls.py --check
python3 audits/2026-10-11-single-deficit-applicability-804e3b0b1b/literal_controls/check_literal_controls.py --check --seed 17
python3 audits/2026-10-11-single-deficit-applicability-804e3b0b1b/literal_controls/check_literal_controls.py --check --certificate audits/2026-10-11-single-deficit-applicability-804e3b0b1b/literal_controls/bad-certificate-empty-fibre-dropped.json
```

前兩項 PASS，各重算5張圖×240列、全部3648 full lifts，normal／seed17 完全相同；
第三項预期 FAIL exit1。Python版本、負控制省略的字面欄位及重播结果見
[validation-receipt.json](validation-receipt.json)。

初版 `observations.json` 錯把「原本已不連通 C 的刪點後仍>1分量」當割點，
因此初版 C-cut metadata retired；其圖、full lifts 與 H 的具名割點結論未變。
原初版與 `generate.log` 完整保留。v2改按分量數的實際增量判定，保存自己的
`check_literal_controls-v2.py`／`observations-v2.json`；v3另增完整 rb2 filter 的校準。
沒有覆寫任何已生成證書。交付 payload hashes 見 [payload-hashes.json](payload-hashes.json)。
