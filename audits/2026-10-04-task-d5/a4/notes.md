# D₅ 的 A₄ 獨立稽核

**最終封存格式修正**：package-attempt1發現audit-local helper多一個EOF空行。
舊default／seed17／root source與全部結果保持；只修目前helper的EOF，
新版本／SHA256见`STYLE_PROVENANCE.json`。最後使用`attempts/0006-style-default`、
`attempts/0007-style-seed17`及root style-final replay；原三份semantic檔案
逐byte保持，results只更新helper source hash與耗時，最新比較由D₅主報告索引。
以下保留首次最終版本的驗證語境。

驗收 **PASS**。只接受原 mixed-(1,2)+a-unary 的 04／04、含整對 root 身份交換；不搬運其他入口的來源排除。固定輸入是 D₅ 的 `snapshot`，正式 A₄ 報告、checker、helper 與 artifact 原 bytes 保持。

獨立程式是 `audit_a4.py` 與 `independent_core.py`。兩者以 D₄ 的 a3 獨立稽核為起點；來源與改動、精確 SHA256 在 `PROVENANCE.json`。沒有 import producer、helper 的 relation／join／search／validator。它以字面四色 MRV 全圖枚舉重建完整 relations，再用獨立的原 incidence guards 接合核對；沒有以 marginals 或分量重新正規化代替 joint。24 張控制另從明列的原 C／U 邊重建，並逐條驗證所有序列化 coloring witnesses。

| 同一原身份 ledger，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| A₃ 保留框架 | 18 | 22 |
| A₄ 新排 04／04 框架 | 2 | 2 |
| 選定 actual U support records | 4 | 12 |
| 選定完整 singleton schedules | 6 | 18 |
| 原完整支援相容 records | 4 | 6 |
| 原完整支援相容 schedules | 6 | 10 |
| 此 key 來源殘留 | 0 | 0 |
| 原樣保存框架 | 16 | 20 |
| 原樣保存 actual U support records | 40 | 58 |
| 原樣保存完整 singleton schedules | 50 | 84 |

`attempts/0004-default/scope_ledger.json` 逐身份保存整份原 frame、SHA256、actual U supports 與完整 schedules，逐項比較 A→A₂→A₃→A₄ 的同一原 objects。Selected generic source indices 是 128／198，完整 root swap rotations 對應 `[1,0,3,2]`。

由原骨架邊重新枚舉每份 144 rotation assignments，恰四份 disk rotations。每份原 C 共同 faces 都是 0ab／4ab；完整 degree 握手式中三條 contact edges 與 boundary attachment 數的奇偶關係排除空 C support，故 actual support 為固定 {0} 或 {4}。Roots 只碰 04，C 只碰一個原 h，完整來源支援前提迫 U 實際含 123；U 必位於同份 rotation 的 a-incident 長 face。04 外側短 U 的部分外路徑只能由完整來源支援條件推得，且與本 key 的 C 幾何不相容；稽核逐項保留這個條件式，不偽造原 skeleton 邊。

三個 hubs 是原 singletons a,b,h，三條 hub 邊原本存在，不使用外點收縮代替原 C 邊。每列合法 root colors 恰兩份有序選擇，ab 與 04 spokes 迫三 hub 色互異。八份外鄰子集完整核對；x=yⱼ 時兩個 owner guards 同時扣除，原 degree 與 exact list 大小仍一致。24 個原有限控制另核對全部 2,080 頂點 degree-list instances、72 條避開 C 的原外部 hub 路徑及每份完整外部的連通性。

任意大小論證另作紙面檢查：拒絕的 connected degree assignment 給 Gallai tree 及 blockwise-uniform lists。K₄ block 的每個 clique 點只有一條離開 Q 的原方向；其 bridge 外側各自互斥，slack coloring／singleton domains 與四色置換迫四個方向都抵達連通的原 hub triangle。Q 的四個 singleton 與該原外部連通 bag 給 K₅ minor。K₄-free 後末端 odd cycle 的相鄰 private vertices 見同一對 hubs；第三 hub 若碰 C，與剩餘原 C 構成第五 bag，否則套兩-hub 分支。末端 bridge 的 private vertex 見全部三 hubs；刪 bridge 後的 slack coloring 使另一側完整 endpoint domain 為唯一未用色，漏一個 hub 即可交換整側兩色而矛盾，所以第五 bag 鄰接全部 hubs。這些 branch sets 的非空、互斥、連通與原邊鄰接由上述原 block／degree／triangle 論證承擔，沒有將固定 Python 控制外推為無界 theorem。

外部 theorem 使用 D₄ 已保存、SHA256 不變的 Dvořák *List coloring and Gallai trees*（2018-03-24）：PDF 第 5 頁 Lemma 7 與第 6 頁 Theorem 10；全文 extract 與精確來源記錄在 `gallai-primary.txt`、`PROVENANCE.json`。不使用 minimal q-core／Corollary 11 前提。Disk 拓撲、原外部連通 K₄ 排除與 K₅ minor 仍屬紙面層。

固定 Python 稽核結果：

- 24 張完整 degree 圖；x、y₀、y₁ 互異／x=y₀／x=y₁ 各 8 張；12 對整份 root swaps。
- 1,920 完整六／五角色 joins，30,720 pinned root-pair fibres，其中 25,632 空 fibres。
- 25,568 六角色與 1,600 五角色 tuple witnesses；**47,149 個全部序列化 coloring fields**逐份驗證原邊、boundary 與有序 contacts。
- 240 份 ax 的 (a,b,u) 投影等式、2,912 份完整 C 替換 witnesses。每份替換逐點固定 C 外所有頂點，包括 U 全部頂點。
- 獨立增加 240 份**完整外部所有頂點**的投影等式，重建並保留 804 份完整外部 coloring assignments，核對 G 與 G−ax 全部 exterior fibres 相同。
- 480 份合法 root pairs 的完整 C extension，沒有將六角色 joints 宣稱相等。

六角色負控制的 control 4、row 01012：G−ax 獨有 `(1,3,1,1,0,0)`；原 ax 因 X=A 不合法。完整 C 替換後得 `(1,3,0,0,1,0)`，固定完整原 exterior，兩份原 coloring witnesses 均驗證。另保存 marginal 假接合負控制，原 root-spoke 資格另行核對。

共同拒絕 row 01202 的 U singleton 是 **1／3**。繼承必要 schedules 中 d=1 共 14 份、d=3 共 10 份；兩者的紙面原 joint 外部 colors 都是 `(4-d,d,d)`。24 個有限 controls 對 singleton1／3 各 12 張。Singleton1 控制的實際 U 支援 124 缺必要 endpoint3；singleton3 控制支援123符合含支援條件，但123沒有繼承必要 schedules。全部控制的完整 Σ 是1023，皆不宣稱 disk、來源933／941、Σ-critical 或 ledger schedule 實現。

01→04 的兩份幾何 diagnostics 獨立核對十列、單一共同 S₄ 色置換與完整 mask image：933→948／934，941→950／950，均不是固定來源 mask。因此没有 D₅ 來源搬運；字面 boundary 色框、C、U、所有六角色必共用同一份色置換，diagnostics 不登記來源結論。

最终 source 的 default `attempts/0004-default` 與 seed17 `attempts/0005-seed17` 均 PASS。完整 relations、counterexamples、scope ledger 及 source versions 逐 byte 相等；`final_comparison.json` 另核對排除 elapsed time／snapshot path 之後的結果完全相等。`attempts/0001`、`0002` 是獨立 adapter 的兩次失敗，精確執行 source／helper bytes、run.log、錯誤與 counters 全數保留，見 `FAILURES.json`；`0003` 的早一版成功也保留。原 certificates 與 D₄ 沒有覆寫。

重播（output 必須是新目錄）：

```bash
python3 audits/2026-10-04-task-d5/a4/audit_a4.py \
  --repo audits/2026-10-04-task-d5/snapshot \
  --output audits/2026-10-04-task-d5/a4/replay-fresh
```

停止於本 key 的條件式原來源排除與 ledger 16／20。現有具名下一入口是原 **12／12**（仍須逐份核對原幾何、lists、外部路徑與完整 joint）；本稽核沒有開啟該研究。Mixed12 整型、任意来源實現、ε≥3、一般出口、K∞=K≤5 及新增 Lean theorem 仍未證。Root 的 `lake build` 與文件／artifact／封存驗證另行記錄，不形式化本頁紙面拓撲。
