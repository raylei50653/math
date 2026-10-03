# 2026-10-03：ε=2 唯一 mixed 的單 spoke 原附件化約

接手基準 `722bfa6`。沿使用者交接的下一步，推進 (5,4)/(4,5)
原 spoke 省略子型。先讀 HANDOFF、STATUS、Kempe 導覽、原 mixed
省略報告、即時 Git 與相關記憶，使用 math-research-handoff-publish。
保留前序未提交 bundle；未用 Graphify／sub-agents，未 commit／push。
成果見 [專題報告](../c5_excess_two_mixed_core_single_spoke.md)，目前停止點
由 [Kempe 導覽](../c5_kempe_guide.md)維護。

## 新結論與界線

固定完整 Σ=933／941、Σ edge-minimal、induced-C₅ disk、ε=2、
相鄰雙 degree-5 roots、恰一份原 mixed。原 spoke e 的省略圖若
拒絕 q，原 (4,4) 核心排除迫它自己就是唯一 degree-5 minimal core。
每份省略圖的拒絕 singleton 位置形成原 C₅ 的獨立集，完整 child
masks 含全收時只有 8／6 份必要選項。

同色原 spokes 在同一列刪掉一條不變更染色集合，因此對每份具名
e 保存保留的同色 spoke 及其迫出的拒絕列；相鄰兩列矛盾。原三-spoke
附件只餘 933 的兩組、941 的六組。保留原框、zw 與所有原 spokes
的 666 份必要 skeleton 有 58 明示非 disk subdivisions；雙側各三
spokes 的十四份平面骨架中，八份拒絕 T4、六份違反原 Σ(G−C)=Ω。

五-spoke 側型只有三＋二。兩側的原 mixed incidence 只能是 (1,2)
或 (1,1) 加二-spoke 側的原單接點 unary。同色省略迫 unique-degree-5
two-spoke minimal core，前型被既有三接點來源定理排除。後型沿用
(2,1) 必要位置及相鄰 split-support 的完整附件定理：112 個具名
原支援對中，80 個違反 singleton 位置、24 個有同源實際附件衝突。
933 的 24 份全部排除；941 的 88 份只餘八份有序原附件。

所以 **933 原總 spokes≤4，941≤5**。941 的五-spoke 型只餘
(012,03)、(014,13)、(034,13)、(123,03) 與 root 交換，並必有
原 mixed incidence-(1,1) 加二-spoke 側的原 unary。這些只是必要
附件，未證可實現、完整 Σ 或其原 spoke 省略必全收。
**共同 ε≥2 不變，ε≥3 仍未證；紙面＋Python，未新增 Lean theorem。**

## 完整原圖控制與 artifact

[Checker](../../scripts/c5_excess_two_mixed_core_single_spoke.py)／
[artifact](../../artifacts/c5_excess_two_mixed_core_single_spoke/observations.json)
保存全部位置與 child masks、共同 D₅ 映射、實際骨架邊、rotation、
明示 subdivision paths、原雙三-spoke G−C 全部十列 relations、
三／二-spoke 原 incidence 身份及每份同源附件衝突。跨圖必要
骨架沒有被當作可獨立拼接的原分量。

固定控制沿用既有八點 943 原圖，標記相鄰 degree-4 原點並接回
六條具名 spokes；60 次 joint-tuple 過濾與獨立全圖回溯相同，
960 次 pinned root-pair 查詢含空纖維，完整 coloring witnesses、
原 singleton mixed 及全部實際附件／ownership 明列。原 943
core 對兩拒絕列均非 q-minimal，保存仍拒絕的刪邊身份；沒有拿
控制圖反駁唯一 degree-5 定理，亦沒有來源 disk／minimality 宣稱。

新 artifact **1,720,841 bytes**，由 MANIFEST／generated ignore
登錄；共 124 份大型產物／119 producers。保留前序研究產物，
新報告、README、導覽、STATUS 及前序後續標記連動更新。HANDOFF
的研究線與 tags 未變，依薄索引規則保持原內容。

## 實際驗證及未重跑範圍

新 checker 的預設 hashseed 與 17 逐 byte 重播均通過：

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
```

直接採用的三接點來源與 split-support 層重播均通過：

```bash
uv run --with networkx==3.5 python scripts/c5_two_spoke_three_contacts.py --check
uv run --with networkx==3.5 python scripts/c5_two_spoke_split_support.py --check
lake build
```

三接點控制為 80 K₅ 證書、63 local states、512 parity tests。
Split-support 重驗 64 A forms／15,360 完整列、252 D exceptional forms
及四份既有來源控制。lake build 通過（8,831 jobs，僅既有 linter warnings）。
Lean build 沒有形式化本輪紙面飽和、附件限制或 spoke 接回。

文件、DocGraph、artifact 與 whitespace 收尾命令：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

上述收尾檢查均通過：482 Markdown／4,989 local links，anchors／
直接索引／HANDOFF 無錯；DocGraph 62 documents／213 relations／
5 families，0 errors／notes；artifact status 為 ok=124，無
missing／changed／stale；git diff --check 無輸出且 exit 0。

未重跑：前序原 mixed 省略／双 unary／spoke＋unary 全份 checker、
全 degree-4 topology 合成、adjacent／middle／reflection 的舊全批、
唯一 degree-6 全分拆、root／zw 刪除全批、一般來源 catalogue、
其他出口及 Lean axiom audit。紙面依賴逐份閱讀並保存 hashes；新
Python 不重證外部 Gallai／degree-list 定理或這些一般來源 lemma。

## 跨對話接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留前序未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、Kempe導覽及git status，
再讀docs/c5_excess_two_mixed_core_single_spoke.md與本輪history。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk、ε=2雙degree5，
相鄰且唯一mixed的(4,4)拒絕核心已全排。原spoke省略圖若拒絕，
自己就是唯一degree5 minimal core，拒絕位置無相鄰，必要child masks共8/6。
同色原spokes限制三-spoke附件為2/6組；666骨架、58明示subdivisions，
雙三-spoke餘下8個T4衝突+6個原mixed省略衝突，原總spokes≤5。
五-spoke原mixed(1,2)全部被three-contact來源定理排除；(1,1)+unary
112個支援對中80位置矛盾、24同源split-support附件矛盾。
故933總spokes≤4；941≤5且五-spoke只餘(012,03)、(014,13)、
(034,13)、(123,03)及root交換，原mixed(1,1)+二-spoke側原單unary。
下一窄入口固定上述四組，保留(b,a,y,u)完整joint relation、原C與U、
所有實際附件及leaf a色纖維，於同一原色框接回a的原spoke。
單spoke省略尚未全排；較少spokes、原unary省略、(5,5)原core保留。
共同ε≥2不變，ε≥3未證；紙面+Python，無新Lean theorem或一般出口。
重播：uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
```
