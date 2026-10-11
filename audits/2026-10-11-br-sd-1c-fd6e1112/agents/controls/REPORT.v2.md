# BR-SD-1c：四份最小原邊／list 控制

BASE `fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69`。本子工作只新建本專屬目錄，沒有修改舊 BR-SD-1a／1b、共享 canonical source，沒有 commit／push。

## 結果與證據邊界

只核 **4 份固定具名圖與 list assignment**，沒有枚舉 list 域、來源域或新增大規模搜尋。每份 C 均為10點／12邊；全部原 G／M／C 點與邊、blocks、cutpoints、實際 synthetic 附件、逐點原 lists、四個 s-query 的完整 C tuples、所有 contact fibres（含空 fibres）以及完整 M／G lifts 都保留。

- 原邊重建、degree、unused-D、完整 fibres／lifts 校準：`triggered and holds`。
- private-witness 保留正常控制：`triggered and holds`。
- support-preserved、witness 被旁支佔用正常控制：`triggered and holds`。
- 無 pair-support 時「割點 list 含 D ⇒ 本環 palette 含 D」：`counterexample`。
- 實際 N45 disk／Σ-critical／minimality／ownership／rotation 來源：`not triggered`。實際 target source 數0，不能由此零觸發證成來源排除。

四份 synthetic M 都只供逐原邊語義校準；即使負控制 M 確實拒絕 β，也沒有 disk embedding 或完整來源合同。任意大小 scoped exclusion 由父 audit 的紙面證明與獨立審查負責，不能由這四份圖代替。

## 同一具名骨架與 literal 色框

三個 cycle blocks 為 `J1=(r,a,x)`、`J2=(r,u,w)`、`J3=(v,z,t)`；唯一原環間 bridge 為 `uv`。
原 s-contacts 有序為 `p=a, q=q`，p 外臂零長，q 外臂為原 edge `tq`。
唯一新增旁支為 `hy`，h 在各 fixture 為 a、x、w。沒有更換 contacts 或原邊。

有序 induced C5 是 `B0..B4`，同一 proper β 為 `(A,B,A,B,C)`，D 是未用的第四色。
M 的原 s-spokes 為 `sB0,sB1,sB4`，因此完整 M-beta lifts 只能取 s=D。
原 G 額外原 spoke `rB2`；省略同一原 edge 得 X=M。每份圖均直接核 r/s 在 G 完整 degree5、M 中 r degree4／s degree5，其餘 C 原點完整 degree4。

證書使用 literal color indices `A=0,B=1,C=2,D=3`。圖形、所有完整 lists 和每份 tuple 都在相同 vertex_order 與同一色框下保存，沒有 marginals 或獨立正規化。

| 固定 fixture | J1/J2 private witnesses 數 | S 原 support | 四 C-query fibre 數 s=A/B/C/D | 完整 M-beta lifts | 完整 G-beta lifts |
| --- | --- | --- | --- | --- | --- |
| two-private-witnesses-J1-branch-at-a | 1 / 1 | B0,B1 真框邊 | 56 / 80 / 40 / 54 | 54 | 42 |
| support-preserved-J1-triangle-branch-at-x | 0 / 1 | B0,B1 真框邊 | 52 / 52 / 32 / 12 | 12 | 12 |
| J2-triangle-private-witness-consumed | 1 / 0 | B0,B1,B4；不為 pair | 72 / 68 / 59 / 48 | 48 | 36 |
| negative-J1-D-routed-into-pendant-bridge | 0 / 1 | B0,B1,B4；不為 pair | 22 / 30 / 34 / 0 | 0 | 0 |

前兩份保 local true-edge pair support，但 M 接受 β，故均沒有進入目標拒絕來源。
J2 單 bridge 旁支的 leaf y 非 s-contact，`d_C(y)=1`；完整 degree4 必需3個不同 B 鄰點，所以這個最小形狀本身不能保 S 的兩點支援。此局部 degree 排除不代表所有較大 J2 原旁支都被這份有限控制排除。

四 C-query 固定 β 的 C–B 原邊及選定 s 色的 s–C 原邊，**暫不施加 s–B spokes**。
完整 M lifts 再逐原 s–B 邊篩選並沿全部原邊核查；完整 G lifts 另加回原 rB2。
所有4×16份 ordered contact-colour fibres 均留在各 fixture，不只保存數量或端點投影。

## 兩份來源條件控制

旁支接 a 時，具名 x/w 仍非 C-cutpoints、非 s-contact，且只屬 J1/J2，各自 L^D 含 D。
假想 bad degree-list 的 J1/J2 palettes 均被這兩點迫含 D，與共用 r 的互斥條件矛盾；實際固定圖的全部54份完整 M-beta lifts 另由直接原邊回溯核得。

旁支接 x 時，J1 triangle 已沒有 private witness。保 S 真 pair 的控制沿原 M 邊給
`L^D(z)={C,D}`、`L^D(q)={C}`；z 只屬 J3，q 只屬末端 bridge tq。
假想 bad certificate 必給 `P_J3={C,D}`、`P_tq={C}`，在原 t 相交，違反互斥。
這校準父 proof 的 pair-supported J3／末端外臂機制；实际12份完整 M-beta lifts 保留。
此固定臂長1控制不是任意臂長紙面證明，沒有抽樣 parity 或暗示普遍來源枚舉。

J2 witness 被 w-y 佔用的第三份 toy，也保存合法必要 routing：J1 private x 迫其 palette 含 D，
r 處迫 J2 不含 D；非contact u 的全部 incident blocks 只有 J2／uv，因此 uv 含 D；
J3 private z 迫 J3 含 D，uv 與 J3 在 v 矛盾。這是從具名 incident blocks 核對的必要推論，未把 cutpoint 的 D 發到全部 incident palettes。

## 明確反例：未保 pair-support 的錯誤 D 傳遞

同一 `J1=(r,a,x)`、旁支 xy、p=a、q 正臂 tq，給 palettes

`J1={A,B}; J2={C,D}; xy={D}; uv={A}; J3={B,D}; tq={A}`。

所有相交 blocks 的 palettes 兩兩互斥；逐點 lists 恰為 incident palettes 的完整聯集，list 大小恰 d_C。

| 原點 | 完整 L^D | 原 synthetic B 附件 |
| --- | --- | --- |
| r | A,B,C,D | 無 |
| a | A,B | B4；另有原 s-contact |
| x | A,B,D | B4 |
| u | A,C,D | B1 |
| w | C,D | B0,B1 |
| v | A,B,D | B4 |
| z | B,D | B0,B4 |
| t | A,B,D | B4 |
| q | A | B1,B4；另有原 s-contact |
| y | D | B0,B1,B4 |

非contacts 的全部 lists 含 D，而 a/q 均不含 D。原 cut vertex x 的 D 完全分到 xy，J1 palette 不含 D。
完整 D-C fibre、完整 M-beta fibre 和完整 G-beta fibre 都為空；四個 C-query 的所有 fibres 仍完整留存。
這證成 unsupported cutpoint-to-cycle D propagation 的 `counterexample`，不是來源排除命題的反例。

其原 S 的附件使用 B0/B1/B4 三個框點，違反 actual true-edge pair support。
父 `PROOF.md` §7 的 palettes 與此負控制逐項相同，只需具名對照 `a1 ↔ a`；其餘點／邊／色名相同。
沒有將 synthetic 附件、拒絕 list 或抽象 block palettes 升為 actual disk 可實現性。

## 可重播產物与驗證

`checker.py` 不 import 舊 solver、證書或 repository 程式；以 Tarjan 從原 C 邊重建全部 blocks，逐點刪除從原邊重建全部 cutpoint witnesses。
完整 tuples 由直接原 C 邊回溯得到，全部原 M 邊另逐條驗證。
`--check` 先直接檢查給定完整 tuples，再完全重新計算證書，要求 canonical bytes 相同。
所有寫入用 exclusive-create；未覆寫或刪去任何產物。

`independent_edges.py` 是第二份固定 alphabetical 順序回溯。
它只從證書的原 M 點／邊重建 C、neighbors、attachments、s-contacts、degree 與 lists，
逐一核所有 C-query 完整 tuples、ordered contact relations／fibres、完整 M／G lifts，以及 S 真 pair support。
它不 import `checker.py`，不用第一份 solver 的 lists 或 block 求解。

从工作目錄 `/home/ray/developer/ai/math` 重播：

```sh
python3 audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.seed17.json
python3 audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/independent_edges.py --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
python3 audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.corrupted.json
```

前三條 exit0；最後一條預期 exit1。正常與 seed17 generation／checks 的 commands、環境、stdout／stderr／exit codes 见 `replay-log.json`；第二份 checker 的正常／seed17 replay 見 `independent-replay-log.json`。

正常與 seed17 證書各87402 bytes，完全 byte-equal；SHA256
`0b2193d4d13f715272f78f3df2431aca915efd2dd77f60ef52de3549d230906a`。
Corrupted 證書將第一份 fixture 第一個 s-query 的第一份完整 tuple 首色由1改為非法色9，保持 JSON 可解析；checker 拒絕，exit1，stderr為 `illegal complete coloring tuple`。損壞證書與所有負 logs 保留。

`first-full-witnesses.json` 另保存每份正常控制的第一份完整 M assignment 及全部原 M 邊的兩端色 witnesses。
`HASHES.json` 保存本目錄其餘交付檔的 bytes／SHA256（manifest 不自雜湊）。
父紙面結論、独立審查、canonical 採納、actual source、Lean 與完整 N45 身份 closure 均是不同證據層；本有限控制沒有替代或放大任何一層。

代次說明：本 REPORT.v2.md 只更正負控制原色1的文字；原 REPORT.md 保留，其中誤寫0。實際 certificate／corruption-mutation／replay logs 始終為1→9，沒有改動或重建任何證書。
