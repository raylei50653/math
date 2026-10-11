# BR-SD-1e：固定具名 private-witness 與 degree 控制

BASE `337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f`。本子工作只建立本專屬目錄，舊 BR-SD-1a／1c 原封存與 canonical source 唯讀；沒有 commit、push、發布或廣泛枚舉。

## 證據與界線

只核四份固定12點／15邊 C 與兩份小負控制，沒有搜尋環長、臂長、旁支大小、list 域或來源域。四份 synthetic M 保留各自的完整圖邊、附件、同一 β、全部 D-query lists、完整 C tuples、16個有序 p/q fibres（含空 fibres）、完整 M／G lifts、blocks、cutpoints 與刪點分量。這些資料全在 `certificate.normal.json`，seed17 證書與之 byte-equal。

- 三份允許接點的 private-witness／原邊 degree-list 校準：`triggered and holds`。
- q=a3=v 的滿度接點排除：`triggered and holds`。
- 禁止接入 J1 triangle 唯一 witness 時，泛化 preservation 聲稱：`counterexample`。
- 「cutpoint list 含 D ⇒ 每個 incident cycle palette 含 D」：`counterexample`。
- actual N45 disk／Σ-critical／β-minimal 拒絕來源：`not triggered`，實際 target source 數0。

四份 synthetic M **全部接受** β。它們都沒有 disk embedding、rotation、完整 Σ／ε、逐非框邊 critical witnesses、原來源 ownership provenance 或 β-minimality；它們不是本輪來源域的反例。任意大小排除只能由父 paper proof 與獨立紙面審查負責，不能由這些固定 tuples 或零 source 觸發承擔。

這些 fixtures 是每份完整候選 M 的獨立 local degree 校準；不聲稱從一張完整 BR-SD-1a 原圖加上 W 的實際手術。各自全部 attachments 一開始即固定，沒有提供／刪除某张 before-W 原 M 的附件以容納 W，也不聲稱 before-W 圖的 degree 已為4。

## 固定骨架、literal 色框與全部附件

三個 triangle blocks 為 `J1=(r,a1,w1)`、`J2=(r,u,w2)`、`J3=(v,a3,w3)`；bridge 為 `uv`；p=a1，p 臂零長；q 臂為 `a3-t-q`，長2。唯一 W 的 off-skeleton 頂點為 y/z，邊 yz 保它們連通，接點 h 的 incident edges 為 hy/hz；因此 W 的第一 block 是 triangle `(h,y,z)`，W 只接到同一 h。

有序 induced C5 為 `(B0,B1,B2,B3,B4)`，β=`(A,B,A,B,C)`，同一未用色 D，certificate 的 literal indices 為 A=0／B=1／C=2／D=3。M 的 s-contacts 按序為 `(a1,q)`，s-boundary spokes 恰為 B0/B1/B4，因此所有完整 M-beta lifts 的 s 色必為 D。G 加回同一 original omitted edge e=`rB2`，原 G 的 r/s 完整 degree5，M 的 r 完整 degree4、s 完整 degree5，其餘 C 點完整 degree4。

所有附件逐點固定如下：a1 接 B4；其他 C 點以 `k=4-d_C-1[contact]` 決定本份 fixture 的附件數，k=0/1/2 時分別為 `[]/[B0]/[B0,B1]`。這是 fixtures 的 explicit construction，不是把未知原來源的附件任意改寫。每份保留其全部 M／G 原邊與 attachments，S 的 synthetic actual support 恰為真框邊端點 `{B0,B1}`。四份 L support 都為 `{B0,B1,B4}`，不宣稱已核 long-L 原身份。

| 固定 fixture | h | w1／w2 private-witness | D-C tuples／M lifts | G lifts | 結果 |
| --- | --- | --- | --- | --- | --- |
| W-triangle-at-J3-ordinary-w3 | w3 | 保留／保留 | 112 | 56 | triggered and holds |
| W-triangle-at-q-endpoint | q | 保留／保留 | 256 | 128 | triggered and holds |
| W-triangle-at-q-arm-interior-t | t | 保留／保留 | 112 | 56 | triggered and holds |
| forbidden-W-at-J1-unique-triangle-witness-w1 | w1 | 失去／保留 | 16 | 16 | counterexample to unrestricted preservation |

前三份均逐項核 w1/w2 非割點、非 s-contact、只 incident 自己的 J1/J2、C-degree2、D 在 list、全部 B 附件不禁 D，涵蓋兩環都為 triangle 的最小見證情形。

W 接 q 時 q 的 C-degree 已由骨架1升為3，完整 `d_M(q)=3+0+1=4`，q 不是末端。W 接 t 時 t 的 C-degree 由2升為4，完整 `d_M(t)=4+0+0=4`，t 有額外兩條 C 邊。這兩份明確不滿足 BR-SD-1c terminal lemma 的末端／無額外臂邊前提，但 J1/J2 private witnesses 仍有效。

禁止控制接在 w1 時，w1 的 incident blocks 變為 J1／Wcycle、成為 C-cutpoint，C-degree4；J1 triangle 排除 r/a1 後只剩 w1，因此 private-witness selection 首次失效。這份 shape 明確違反本輪「W 唯一接 J3／q-arm」前提；不能用它反駁本輪排除。

此處 D-query 固定 β、s=D，只核 C–B／s–C／C–C 完整約束；完整 M lifts 另逐邊核 s–B／B–B，完整 G lifts 再核 rB2。沒有生成三個非 D 的 C-query，也沒有宣稱全部 β 的原來源 relations。由已固定的三條異色 s-spokes，保存的 D-query 已涵蓋這些 fixed β 的**全部完整 M／G lifts**。

## 兩份結構／palette 負控制

`saturated-q-equals-a3-equals-v` 只保存原骨架及 named equality：q 同時是 J3 錨點與 bridge 端 v，q 臂零長。原 C-degree3，加原 sq 邊即完整 degree4，B 附件數必0；任何非空 W 使 m≥1，因而 `d_M(q)≥3+1+1=5`。不刪原邊或附件以恢復 degree4。此結構排除 `triggered and holds`；未造 lists、boundary assignment 或 actual source。

`cutpoint-D-is-only-in-pendant-bridge` 是4點 abstract degree-list fixture：triangle `(x,a,b)` 與 bridge xy，palettes 為 triangle `{A,B}`、bridge `{D}`。lists 是所有 incident palettes 的完整聯集：a/b=`{A,B}`、x=`{A,B,D}`、y=`{D}`，每個 list 大小恰 C-degree，相交 palettes 互斥，完整 coloring tuple fibre 為空。x 是割點且 D 在其 list，D 完全屬 bridge palette、沒有進 triangle palette。

這精確反駁 unrestricted cutpoint-to-cycle D inference；未配置 synthetic B／s，也未聲稱本輪原來源合同。它不是 BR-SD-1e 的 actual source，僅校準 parent proof 不可使用的推論。

## 驗證方式與重播

`checker.py` 不 import 舊 solver、證書或 repository 程式，從完整 C 原邊用 Tarjan 重建 blocks、逐點刪除重建 cutpoints，計算所有 D-query 完整 tuples。`--check` 先核給定 tuples 的色值、list 與原邊，再完全重建固定證書並逐 canonical bytes 比較。

`independent_edges.py` 不 import producer；从 complete M 原邊重建 C、boundary attachments、s-contacts、lists、degree、ownership/supports，以 alphabetical DFS 重算全部 D-query tuples。它獨立驗證全部 M／G lifts與有序 contact fibres；blocks 由 complete edge partition、每個 triangle／bridge 的原邊形狀、刪點 cutpoint 及 block-cut incidence tree 核實。

所有 certificate／log 寫入均 exclusive-create。兩份證書各479425 bytes，SHA256=`b88736dabca36919202050fb85c61582749248a87db7368c9d2a20671b1660b9`。`generation-replay.json` 保存正常／seed17 generation 與 checks；`read-only-replay.json` 保存正常／seed17、corrupted／malformed 的雙 checker 命令、環境、stdout／stderr 與 exit codes。沒有失敗 generation；負控制和損壞證書全部保留。

從 `/home/ray/developer/ai/math` 重播：

```sh
python3 audits/2026-10-11-br-sd-1e-337d018b/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 audits/2026-10-11-br-sd-1e-337d018b/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.seed17.json
python3 audits/2026-10-11-br-sd-1e-337d018b/agents/controls/independent_edges.py --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 audits/2026-10-11-br-sd-1e-337d018b/agents/controls/independent_edges.py --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.seed17.json
python3 audits/2026-10-11-br-sd-1e-337d018b/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.corrupted.json
python3 audits/2026-10-11-br-sd-1e-337d018b/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.malformed.json
```

前四條 exit0；最後兩條預期 exit1。Corrupted 控制將第一份 fixture 第一完整 C tuple 的 a1 色由0改為非法9，JSON 仍可解析；primary 拒絕為 `illegal complete coloring tuple`，independent 也拒絕。Malformed 控制截斷 JSON；兩 checker 都拒絕為 JSONDecodeError。正常與 seed17 的 replay 不修改 certificate。

下一個最小 OPEN 義務在父 audit：owner 對新 candidate paper result 作 canonical 採納決定。任何 J1/J2 接入、多接點 cross edge 或其他來源域的推廣均須獨立證明；本控制沒有承擔任意大小量詞、actual source 存在或完整 N45 closure。
