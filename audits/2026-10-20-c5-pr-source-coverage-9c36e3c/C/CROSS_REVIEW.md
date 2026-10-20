# C 對 A／B 與整合稿的獨立交叉審核

2026-10-20；BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。
只讀 A／B 證據；本檔只寫 C 目錄。下列是紙面命題與實際 checker 的分層審核，
沒有把重播 PASS 視為一般 disk 來源覆蓋。

## A：量詞、有限目錄與 count 反例

已讀 [A/REVIEW.md](../A/REVIEW.md) 及
[check_contract.py](../A/check_contract.py)，並執行：

```text
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/A/check_contract.py --check
exit 0
PASS: complete leaf fibres, last-P parity obstruction, saved catalogue identity
```

1. 三探測 RR／PRR／RRR 的逆公式直接讀取十個座標。故相等的全部後綴四列
   支援必給相等完整十列支援；反向由每步確定性支援轉移歸納。來源域不必
   先限制在 K132，空支援也沒有被省略。代表 H 必須在全體後綴量詞之前
   選定，報告保留了這個順序。
2. `K∞=K132` 的等價敘述成立。它與 `K∞=K≤5` 的連接需要既有 bounded
   catalogue authority，單憑 saved keys 相同不能證重枚舉完備性。
   A 已明示此限制；checker 也只主張 keys 同一性。
3. C5 內接單一葉點是共同一般 disk 域的合法真圖，十列各有三份 full lifts。
   此圖不滿足 C 的 simple-face cellulation checker 前提，這不影響其在
   共同一般域內的有效性。
4. 最後一次 P 的三座標和必為偶數；常向量全三在 R 下不變，故任何結尾
   旋轉都無法逃過奇偶矛盾。無 P 的兩種種子及旋轉另已排除。
   這是對**任何長度、任何大小**文法 count 代表的反證，不是有界實驗。
5. Fibre 雙射必保 cardinality，故 count 不可能性確實也否定完整 fibre
   代表。它不否定 P/R 操作本身的完整 fibre 公式，也沒有跨到 r6、
   critical 或內面全三角來源的 count 覆蓋；A 的邊界正確。

結論：PASS，未見需修正的量詞或來源提升。

## B：任意字串、第一個 P 與共同 collar

已讀 [B/REPORT.md](../B/REPORT.md)、轉移及共同 collar checker，執行：

```text
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_transition_obstruction.py --check
exit 0
K=132, P_image=640, P_preimage_K=256, R_preimage_K=132,
P_outside_entering_K=124, nonzero_basin_K=1023

python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_universal_collar.py --check
exit 0
all_nonempty_masks_to_1023=true, push_count=17,
PR_power_synchronizes=false
```

1. 933／941 的兩個有序 R 軌道都在 K 外，十個 P 像都在 K。對任意有限
   字串按第一個 P 分成 `R^a P v`，就得到精確 iff；無 P 時沿 R 軌道，
   有 P 時先進 K，再由封閉性留在 K。因此任意字串的結論有紙面歸納，
   並非以測到某個長度替代全稱量詞。
2. 932 的第一個 P 到63，之後五態 R 圈的兩個位置有 P 自環。
   以後綴 R 累計數 mod5 作指標的判準正確；首次進 K 前，自環 P 不改
   residue，其餘三個位置 P 直接進 K。`PRP^t` 永留459 確實排除
   「只要 P 次數夠多就一定進 K」。
3. 形式 mask 與未知實圖來源保持分離。`941∉K` 而 `P(941)∈K` 是有限
   支援反向推理的反控制，沒有假稱已建出一張 941 disk。
4. 非零各態到 K 的最小 P 次數上界4，由實際路徑加全邊 Bellman
   不等式給雙向證據。它是 `∀m≠0 ∃w`，不是所有 w 都成功。
5. `W=RRR(PPR)^4P(PRP)^4` 的十個 singleton 像都為1023，P/R 保聯集，
   遂得 `∀m≠0 T_W(m)=1023`。checker 再直接核對全部1023非零 masks。
   零仍到零；此結果不使用四色定理產生非空性，也不聲稱 W 最短。
   實圖解釋增加17內點且換框，不能當作原來源更小化或原框覆蓋。
6. `(PR)^n` 的軌跡自 n=10 出現週期4，並逐個保存週期內非同步分量。
   確定性轉移保證這個明確週期無法在更後面突然同步；有限週期控制充分。

結論：PASS，任意字串、存在後綴與共同後綴三種量詞分開且均有對應證據。

## 整合稿 §5 的幾何及來源合同

已審 [主報告](../REPORT.md) §5。逆 P 的第三鄰點須內部、面須為實際空
三角面，兩條件都必要。移去的 collar 沒有其他附件後，剩餘部分可為
一般 embedded disk 圖，不須全部位於 C 的有限 cellulation checker 域。
有限證書本身則只驗證較強 cellulation 域的六張控制；應如 C 報告所述分層。

若重建字含 I，其 I 點出生即為內點，P/R 永不把內點帶回外框。
因此 P 從不接到 I 點；按插入逆序撤掉所有 I 點會逐一恢復三角星。
這使「省略 I 後同十列計數」有一個更強、合法的證明：
所得確是最終同框 P/R 骨架，完整染色的 restriction 與唯一補第四色互逆。
同步 count-vector 歸納也成立，但不必否定這個直接完整 restriction 構造。

正二十面體 puncture 沒有逆 P/I，亦不在 P/R/I 生成族中：
任何非種子生成字的最後非 R 字母都必留下可撤銷的 P 或 I。
然而此圖支援為1023，C 是支援代表。故可剝來源定理僅給充分子類，
「剝不動」不能推無文法支援代表。整合稿保持此界線，PASS。
