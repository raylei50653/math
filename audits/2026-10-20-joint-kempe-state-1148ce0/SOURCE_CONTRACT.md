# 同染色聯合 Kempe 狀態：本輪契約

日期：2026-10-20。BASE 為 `1148ce026aaf764e6e2766aebc096eebe193ed13`；
原 Git 狀態及輸入雜湊見 [BASE.json](BASE.json)、[INPUTS.json](INPUTS.json)。
本輪只讀既有來源；未提交的 `2026-10-20-r6-941-j1-c11-1148ce0`
屬既有工作，不作本輪證據，也不修改。

## 1. 第一個候選摘要

固定同一有限簡單圖 G、有序具名接點 B，及同一份 proper 四色染色 c。
色名為字面 `0,1,2,3`。對每個 unordered pair ab，先在全圖 G 上求
所有 maximal ab components，再取它們與 B 的非空交集，得到分割
`pi_ab(c)`。候選為

```
S_B(c) = (c|B, pi_01(c), pi_02(c), pi_03(c),
               pi_12(c), pi_13(c), pi_23(c)).
```

六份分割必須來自同一個 c。此摘要刻意不保存不接 B 的 components、
接框分量的私有頂點身份、刪除後的分裂與跨分量實際附件。
不同圖不合併作同圖充分性反例；圖身份、全部邊與嵌入另行保存。

固定 action label `(a,b,r)`，其中 `r in B`。
當 `c(r) in {a,b}` 時，交換全圖中含 r 的完整 maximal ab component。
否則 action 不合法。先比較相同 literal source frame 下的結果；
若計算另外使用全域換色商，必須明確保存作用於整份染色的共同置換，
並分開記錄 literal 反例。

本輪問：

```
S_B(c)=S_B(d)  =>  S_B(swap_ab,r(c))=S_B(swap_ab,r(d)) ?
```

更強的多步充分性要求所有 action 的合法性及後繼可由摘要更新。
單步反例足以否定這個候選；有限域無反例不證明一般充分。
根在 B 的操作未涵蓋所有不接框分量交換。

## 2. 真圖控制域

使用凍結的 132 份 C5 catalogue witnesses，讀取全部原邊並補上原 C5
框邊；每個固定 canonical 字面框色保存完整延拓集合，包括空 fibre。
這是既有代表的重播，不重新枚舉所有 disk 或所有同支持圖。
必要時使用凍結的 survivor-811 具名 disk 及其完整染色；實際測試
範圍、嵌入核對和 action 範圍由本輪報告精確記錄。

這些控制不被指定為完整 r6／941 來源。其來源前提未觸發時，
狀態一律為 `not triggered`，不能解讀為 941 來源不存在。

## 3. J1 的條件式接口

承接凍結的 [來源契約](frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/SOURCE_CONTRACT.md)
及其上游全部最小性、完整支持941、原 stars、附件、rotation、
私有點、非邊及 pocket 前提。共同核心是
`F=G−{b,p,h,x,y,r}`，有序 induced rim
`(a,n,R,L,q,c,s,v,w,t)`。

只在 `a1=N01232(Q1)=0` 的 J1 分支使用
`J1=(G−{p,h})/(b=L)+aR`；不混用 J2 的染色或前提。
兩個剩餘核心 fibres 的 rim literal 是

```
(0,1,3,2,3,1,2,0,1,2)
(0,1,3,2,3,1,2,1,0,2).
```

每個 fibre 保留所有私有點的完整染色；沒有見證的 fibre 仍顯式為空。
必要分割表只給每份真正來源染色必須滿足的條件，不提供共同平面
實現，也不允許把不同色對各自可行的分割拼成一份染色。
所有新條件若要排除 J1，須對同一原來源與全部完整 fibres 證明，
並保留原候選的接受與另外兩列拒絕。這些義務本輪保持 OPEN。

## 4. 證據層

新有限反例／分類以完整圖染色及實際 maximal component 核對。
既有 residual-components 加 stars 的精確更新定理可沿用；
本輪不把該定理重新宣稱為新成果。
紙面候選、有限重播、完整來源觸發、一般充分性和 Lean 分開報告。
不使用四色定理作 oracle；不 commit 或 push。
