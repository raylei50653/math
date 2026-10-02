# C₅ 舊化約之外的完整四接點輪環替換

日期：2026-09-30。接續私有路徑奇偶定理；目前狀態由
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護，完整證明見
[輪環報告](../c5_two_vertex_repair_rings.md)。

## 本輪成果

- 四輪星與四環帶加中心有相同的完整具名四接點 relation：proper C₄
  且至多三色。紙面三行構造及 rainbow 阻斷證明可接回任意外部上下文；
  中心必須密封，五接點關係不相等。
- 原 A 的 h5、B 的 v 可反覆作輪環替換。任意有限層數保持來源
  R127／R167、完整 J/P、全部可用外框、十五組 repairs 及 r*=4。
- 每個來源三角形皆為面，故 clique 切口不能隔出密封私有補片。
  擴張側私有圖含三角形，不能套前輪整來源 path 接線；私有共鄰數
  排除保持原框點及 ownership 的舊核心子圖，最低私有度數至少四。
- 兩方向各驗深度 (1,0)、(0,1)、(1,1)、(2,3)，共八個19／23／35點圖。
  11,520份構造完整延拓、88份稀疏補全、完整四／八接點局部關係、
  七十份四點投影、每例十五組 repairs、十二項結構負控制均通過。

## 驗證與界線

本輪已生成新 [checker](../../scripts/c5_two_vertex_repair_rings.py)／
[artifact](../../artifacts/c5_two_vertex_overlap/repair_rings.json)。原邊回溯與
三行表構造獨立，完整來源掃 `4^5`，全圖掃 `4^8`。結構 verifier 核對全部
實際附件並逆序套新化約；clique 分量及舊核心單射另行窮盡檢查。

以下既有檢查已實際重播通過：

```bash
python3 scripts/c5_two_vertex_repair_strips.py --check
python3 scripts/c5_two_vertex_repair_patches.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
```

`lake build` 完成8,827 jobs；僅回報既有 `SymRelabel`／`AttachmentOrder`
linter warnings。沒有改 Lean 檔案，沒有新增 Lean theorem／`native_decide`。
沒有重跑來源大枚舉、其他區域政策或 weak-deletion 線。

新證書生成後，下列檢查亦實際通過：

```bash
python3 scripts/c5_two_vertex_repair_rings.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_rings.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

兩次新證書重播逐 byte 相同，artifact 為239,221 bytes，低於1 MB，完整
保存。文件檢查涵蓋397份 Markdown／4,028個本地連結；DocGraph 核對
62份文件／213條關係／五個 families，零錯誤、零 notes。這些檢查不把
新紙面定理升格為 Lean 證明。

## 停止點與工作區

新輪環逆化約處理了一個原密封 clique 補片及整來源奇偶路徑化約之外
的任意大小骨架族。加入此規則後的其他同 class disk 代表仍未分類；
未證三種規則的必要性、正常形唯一性或一般出口。

接手時 main 已領先 origin/main 一個提交，且已有共同 lemma、來源、
補片與奇偶路徑相關未提交成果；本輪保留這些內容。使用者只要求接續
研究，本輪未 commit／push。HANDOFF 的研究線與 README 入口未改變，
依文件治理更新專題、所屬導覽、STATUS 及本紀錄。
