# W7 恰一障礙續進：K=1十一支排三支，及任意K條件排除

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
[BASE.json](BASE.json)凍結15份輸入，正式數學 authority 對回 Git BASE；
上輪尚未提交的[結構探索](../2026-10-21-w7-exploration-30dde27/REPORT.md)
另記精確 bytes／SHA，不冒稱已在該 commit。

**沿恰一反色障礙追到新的來源條件排除：K=1的十一個具名位置中，
profile0的 n、u4、u2 三支排除，尚餘八支。** 這是同一原外側 E 的
六點共同重著色與完整 cap 紙證；不是有限局部可行性或數值 LP 結論。
任意 K 另有一組明確條件排除。原40個 profiles 仍是排38、餘0／1兩型。

## 1. 本輪精確縮小的分支

沿原來源契約固定 P=(n,u4,u3,u2,u1,L)、P色121212、a=0、q=3，
原 A 是完整第二層 S 上避 p 的 a–q 弧。b=1表示 A 上恰一個12點 Y；
K是全部 H 點總數，不能把 b=1 當作 K=1。

| K=1原分支 | 本輪排除的Y中心 | 尚未排除的Y中心 |
|---|---|---|
| profile0，原n至少六度 | n、u4、u2 | u3、u1、L |
| profile1，原n恰五度、z1=a | 無 | u4、u3、u2、u1、L |

K=1時唯一H點必為Y，所以上表確是具名原度數／位置分支的來源排除。
它不排 K≥2 的整體結構，更不排 profile0／1整型；不能將三個細子案加到
原38個已排profile的計數上。

## 2. 排除的核心：保持同一E，重新著色六個原路點

[完整短證](SHORT_PROOF.md)先證：原 D 確分成 P–A 的原三角 strip 和
同一實際外側 disk E，P全部外接觸恰在 A。固定一份實際完整 E 著色，
六個 P 點的共同 proper 延伸便與同一 D 的完整 fibre 逐份對應。
全部私有點、原邊、rotation及附件保留；沒有各點各自挑外側見證。

恰一障礙時，多數P點只允許12。唯一可能多一個03色的中心T，須滿足

```text
H_T={Y}恰一點，且Y在A上的左右鄰點同色β。
```

此時T可另用另一03色 γ=3−β。profile1 的 n 另有合法的3色選擇，
完整原耳 a–n–u4 始終保留。這把任意長列表壓成一個精確短signature。

例如profile0的Y在H_n時，改原六點為

```text
(n,u4,u3,u2,u1,L)=(3,1,2,1,2,1)，
(b,p,h,R)=(2,1,2,0)，(x,y,r)=(0,1,3)。
```

這些色與同一E逐條原邊相容，拼成原G的完整著色，原外框
`(x,y,a,b,c)=(0,1,0,2,1)`，撞上既有 `N01021(G)=0`。
其餘排除也各有具體完整構造，不需要 Q1／J1 零列或較小 bad。
原 target 本身不必能接回G；用的是改色後的完整D與cap。

## 3. 任意K的新增條件排除

下表皆假設 b=1、H_T恰為{Y}、左右03同β。

| 原型 | Y的中心T及相位 | 本輪結論 |
|---|---|---|
| 0 | n、β=0 | 排除 |
| 0 | u4／u3／u2／u1、β=3 | 排除 |
| 1 | u3／u2／u1、β=0或3 | 排除 |

其他signature未由這個構造排除。左右同色的必要奇偶是0型K奇、1型K偶；
其他H列表可任意長，並未被刪短。
[外側界面與全部signature](exterior/REPORT.md)記錄任意K完整列表公式，
並保58個原相位signature／target cases、232個四相位cases的全部P延伸與cap。
單翻完整 K03(a)／K03(q) 後沒有再排 K=1 的其餘八支。

## 4. 留下分支還須滿足的原來源結構

[原橋、鄰色與混色傳輸紙證](reduction/REPORT.md)給出任意K、b=1的必要引理：

- 完整12圖中，整條P經唯一原橋 T–Y 接向外側。原P到舊rim點t的12路
  都必經Y，並且Y在S外另有原12鄰點；它不是可忽略的私有死枝。
- Y的完整原鄰域必見其餘三色。若缺一個03色，單點重色Y便使A全03，
  原literal rim不變，違反全部同rim fibre 的a/q分離。
- 若Y的某個混色完整分量不碰rim，交換它必把障礙傳給其他H點，而且新
  障礙的原中心色與T相同。K=1沒有其他H點，因此Y的兩個混色完整分量
  都必碰rim；同中心色的全部H點只有Y時亦然。

這些義務保留同一份完整著色。不能把兩條混色路獨立挑選，再當作同一
來源的共同見證。原Y五度仍有必要色型存活，沒有取得通用W5替換。

[完整分量作用審核](transport/PROOF.md)另給精確反控制：翻K03(q)到達的
目的整fibre容許a/q合併欄，但真實作用的像仍保原分量不同。因此不可將
像補滿成目的整fibre後繼續推理。雙翻後框色回原樣，boundary-free私有03
分量仍可改相位，也不能冒稱整份原著色已還原。

這一路對K≤5的3,030個唯一障礙位置、兩target共6,060份局部色列做78,780
個必要連通gate，全部非空。這個陰性結果沒有提供共同外側E實現，也不
否定上面同一E重著色已證的條件排除。

## 5. 獨立驗證與精確停止點

[independent_caps.py](independent_caps.py)不讀worker checker：由原完整stars
直接枚舉左右cap，再與凍結的原G／Q1／J1三矩陣逐格比對。
58個原signature／target cases的完整P延伸均一致，其中22個case有禁止cap；
另核K=1十一位置、兩target、四個完整03作用，共88個cases。
短證另經兩位獨立reviewer逐原邊與同一E量詞核對。

```sh
python3 -B audits/2026-10-21-w7-single-barrier-30dde27/independent_caps.py
python3 -B audits/2026-10-21-w7-single-barrier-30dde27/exterior/check.py
python3 -B audits/2026-10-21-w7-single-barrier-30dde27/reduction/check.py
python3 -B audits/2026-10-21-w7-single-barrier-30dde27/transport/check.py
```

各checker均有normal／seed17重播、完整fibre／作用的負控制與輸入SHA核對；
整合receipt見[verification.json](verification.json)。本輪沒有跑大型LP，
沒有重新枚舉任意大來源圖，沒有外部新定理、matching或新Lean。

本輪完成：上述任意K的條件分支排除；K=1十一支排三；原橋與混色傳輸義務。
剩餘：profile0的K=1三支、profile1的K=1五支，其他K及多障礙，原共同計數錐、
一般W7／J1／J2、來源實現、合法較小bad及主命題仍OPEN。
下一個窄入口是0型剩餘 u3／u1／L：追Y缺側03色對的完整混色路如何經原E
接到rim，保同一E的全部palette與cap共同相容，不能只靠單palette非空gate。

Closure scope：具名恰一障礙條件子分支，非整個profile。
Updated：僅本exclusive審核的新紙證與證據；未改上輪探索或舊證書。
Reviewed-unchanged：已核父40型清單及Kempe導覽／STATUS的兩型OPEN停止點；
一般J1兩項／J2六項不變。共同路由未發布本輪窄結果，不覆寫舊快照。
Propagation stop：L2核對父分支，父型未closure；無L3語義變更。
未commit／push；目前Git狀態以即時工作樹為準。
