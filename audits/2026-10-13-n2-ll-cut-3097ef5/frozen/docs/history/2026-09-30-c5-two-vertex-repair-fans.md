# C₅ 輪環逆化約之外的完整四接點偶長雙扇替換

日期：2026-09-30。接續輪環定理；目前狀態由
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護，完整前提與證明見
[雙扇報告](../c5_two_vertex_repair_fans.md)。

## 本輪成果

- 完整四接點雙扇 F_L 在兩 hub 異色時由二色交替決定端點奇偶；
  hub 同色時有任意長度至少二的三色 walk。因此偶長恰與四輪星等價，
  可接回任意外部上下文；奇長有相同60份賦色但完整關係不同。
- 在 A 的 h5 與 B 的 v 選用指定私有 hub，得到任意偶長的同 class
  disk 來源。兩側均擴張時無私有度數五點，既有輪環逆化約不能開始；
  亦無密封 clique 補片、整來源路徑或 degree≤3 消去起點。
- 私有共鄰數排除保持原框點及 ownership 的舊核心副本。來源的完整
  R127／R167、同一色框的 J、全部可用框及 P 都保留，故十五組 repairs
  及 r*=4 保留。任意大小結論是紙面證明，未分類全部代表。
- 新雙扇逆化約能帶回原骨架；舊規則無起點只針對縮減，未排除容許
  先擴張再縮減的任意操作序列，也未證改寫完備性或正常形唯一性。

## 證書與實際驗證

新增 [checker](../../scripts/c5_two_vertex_repair_fans.py) 與
[artifact](../../artifacts/c5_two_vertex_overlap/repair_fans.json)，233,047 bytes，
低於1 MB，完整保存。從實際邊核對附件、ownership、來源 disk、全部
框證書、clique 完整分量與舊核心單射，並列全部私有度數以阻斷輪環。

兩方向各驗 `(L_A,L_B)=(4,2),(2,4),(4,4),(6,8)`，共八個17／19／25點圖。
局部六種長度逐份掃 `4^4`，來源掃 `4^5`，全圖掃 `4^8`；原邊回溯不
使用已知 class 或局部等式作接受 oracle。11,520份構造完整延拓、88份
稀疏補全、所有十五組 repairs、arity 下界及十四項結構負控制通過。
中心色與漏路徑邊的界線另有完整關係／實際染色反例。

以下命令已實際通過；兩次新 checker 的結果與 artifact 逐 byte 相同：

```bash
python3 scripts/c5_two_vertex_repair_fans.py
python3 scripts/c5_two_vertex_repair_fans.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_fans.py --check
python3 scripts/c5_two_vertex_repair_rings.py --check
python3 scripts/c5_two_vertex_repair_strips.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
lake build
```

`lake build` 完成8,827 jobs，只有既有 `SymRelabel`／`AttachmentOrder`
linter warnings。未修改 Lean 檔案，未新增 Lean theorem 或 `native_decide`。
本輪未重跑密封補片、六例 transport 的獨立 checker、其他來源大枚舉、
其他區域政策或 weak-deletion 線；新圖的框與 repair 前提則已直接重驗。

文件與空白檢查亦實際通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

文件 checker 核對399份 Markdown／4,048個本地連結、章節錨點、直接
索引與 HANDOFF 格式；DocGraph 核對62份文件／213條關係／五個 families，
零錯誤、零 notes。這些檢查不把紙面定理升格為 Lean 證明。

## 停止點與工作區

下一窄題是輪環及偶長雙扇縮減後的其餘同 class disk 骨架，特別是
完整四接點關係的其他 disk 實現。全部代表必要分類、一般出口與
`K∞=K≤5` 保留。

接手時已有共同 lemma、來源、補片、奇偶路徑與輪環成果尚未提交；
本輪保留它們，新增雙扇證書、專題及紀錄，更新所屬導覽、STATUS、
state 導覽與輪環報告的後續入口。研究線與基本入口未變，依文件治理
保留 HANDOFF／README。本輪未 commit／push。
