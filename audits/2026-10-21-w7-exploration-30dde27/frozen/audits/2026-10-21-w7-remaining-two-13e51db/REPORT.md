# W7 剩餘兩型：完整第二層界面與排除嘗試

2026-10-21；exclusive BASE `13e51db3ec3d8d7ec7eeef60167afdc19ad956c4`。
[BASE.json](BASE.json) 凍結十二份原輸入的 bytes／SHA256；原來源、字面色框、
rotation、全部附件、空 fibres 與完整 cap lifts 均沿用原契約。

**本輪尚未排除 profile 0、profile 1；原40型仍是排38、餘2。**
新完成的是兩型原第二層的無弦圈定理、完整八內點接合界面，以及三條
具體排除路線的精確審核。沒有把必要支持或失敗的替換控制提升為來源結論。

## 1. 新原圖結構：第二層恰為 induced 圈

[原圖紙證與有限拓撲校準](../2026-10-21-w7-profile0-13e51db/REPORT.md)
令 `C=(n,h,L,u1,u2,u3,u4)`，原 `int(C)={R}`，證明

\[
W=N_G(V(C))\setminus(V(C)\cup\{R\}),\qquad G[W]=S,
\]

其中 S 是原 induced 簡單圈，且 `int_G(S)=V(C)∪{R}` 恰八點。
所有原額外 link 鄰點均只接一個 C 點，各完整 link 列表互不重疊。
原 C3／C4／C5 pocket 定理排除 S 的全部額外弦；不是將未知區域補成面。

| 固定原型 | 原完整第二層 S | 必要長度 |
| --- | --- | --- |
| 0：無弦、n≥6 | `(p,a,rev(H_n),z1,H1,z2,H2,z3,H3,z4,H4,z5,H_L,q)` | `8+K≥9` |
| 1：僅au4、n=5 | `(p,a=z1,H1,z2,H2,z3,H3,z4,H4,z5,H_L,q)` | `7+K≥8` |

K 是相應全部 H 列表長度之和。既有 03 分量分離迫 K≥1，且其中某個
反色12鄰點 y 必在**同一完整 `K12(P)`**，不能單獨交換 y。
這改進了前輪只把外側 link 接成可能重訪步道的描述。

S 是真正的完整接合界面：所有更外側原附件留在同一 E，八內點的全部
向外鄰接都經 S。可用七份由同一 S 字面色列決定的完整色列表，精確表示
原八內點 patch 的全部延伸與空 fibre。仍未取得合法的較小替換。

## 2. profile 1 的完整 n-star 沒有再縮支持

原 `N_G(n)=(a,p,h,R,u4)`，故同一 D 中 `N_D(n)={a,u4}`，且原 au4 有邊。
若 n 的 palette 不含 a、u4，n 的實際完整分量就是單點。又固定 D−n 的
全部著色後，可將 n 改成任一未被 a、u4 使用的色；這是完整 fibre 雙射。

[check_n_star.py](check_n_star.py)從原全部307,197欄復算此必要分量限制，
再做完整 incident 零傳播，與只加原 au4 的閉包逐項相同：

```
38,647 states／133,271 columns；兩target 44459、44466 仍存活。
直接 n 改色分別給 44459 ↔ 66233、44466 ↔ 66242。
```

全部合法 n 改色均留在同一必要支持中。
[證書](n-star.json)保存完整集合的 SHA256、每輪量及具名改色對；
[證明與程式範圍](N_STAR.md)區分完整原分量與欄中的框接觸。
**這不證共同計數錐可行，更不證實際來源存在。**

## 3. 已測的較小替換未給來源排除

[profile1 原555 patch](../2026-10-21-w7-profile1-13e51db/REPORT.md)
有完整界面 `(a,b,q,L,R,u4)`、原內點 `{p,h,n}`。
31份 proper normalized界面色列中，14非空、17空，全部 lifts 保留。
任何同一界面、至多兩內點的完整關係相等替換都有直接兩色障礙；
允許弦後的全部602個較小三角化 patch 亦無一具有原關係的子集。
這只關閉此具名通用局部替換路線；原 E 限制下的有條件替換仍未判定。

[原cap刪點候選審核](../2026-10-21-w7-replacement-13e51db/PROOF.md)
另檢驗刪 p、h、R 後，對完整暴露 link polygon 的全部52種三角化。
在兩型各自的完整必要支持上，每個候選都仍有可產生拒絕列的輸入格。
profile0 每候選328–1,676格，profile1 每候選160–1,226格。
這些格未被實際來源觸發，不能稱為原來源反例，也不能據此排除所有縮減。
該報告另給 W7 單獨刪 hub 的通用子集替換不可能的紙證。

## 4. 精確停止點與驗證

兩型的較高度數原來源仍未矛盾。接續可使用上列**同一原 S 的七列表完整
關係**，尋找保留所需接受列且不引入拒絕列的合法較小 patch，或對原 E
的完整 fibres 證更強限制；不能以獨立接點、各自可行分量或不同來源拼接。

本輪不再擴大實圖枚舉，未跑大型 LP，沒有新 Lean。
normal／seed17 optimized 的 n-star 重播逐字一致，三項內部負控制及外部
冒稱排除的污染證書均拒絕，見 [n-star-verification.json](n-star-verification.json)。
各子審核的原 bytes、完整有限核對及負控制由其報告索引；
本輪整合核對見 [verification.json](verification.json)。

```bash
uv run --with-requirements requirements.txt python -B audits/2026-10-21-w7-remaining-two-13e51db/check_n_star.py
PYTHONHASHSEED=17 uv run --with-requirements requirements.txt python -B -O audits/2026-10-21-w7-remaining-two-13e51db/check_n_star.py
```

Closure scope：原第二層全部弦排除、完整八內點界面；具名通用局部替換障礙。
Updated：本報告與新證據、Kempe導覽及STATUS直接索引。
Reviewed-unchanged：前輪38型排除、父W7兩型清單、一般J1兩項／J2六項；
HANDOFF研究線及README入口未變。
Remaining OPEN：profiles0／1來源排除、原必要計數錐、來源實現、一般W7／
C7多內點／J1／J2、嚴格較小bad及主命題。
Propagation stop：L1；兩個原型均未closure，不改寫前輪凍結結論。
本輪未commit或push。
