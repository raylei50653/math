# C₅ 輪環與偶長雙扇之外的十三點非對稱四接點 disk

日期：2026-09-30。接續偶長雙扇定理；目前狀態由
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護，完整接線、前提及
紙面證明見[D₁₃ 報告](../c5_two_vertex_repair_caps.md)。

## 本輪成果

- 十三點三十二邊的固定 disk D₁₃ 與四輪星具有相同完整四接點關係。
  四色框的拒絕有直接迫色矛盾，三個接受框型有明列完整延拓；可接
  任意外部上下文，但所有九個局部內點須密封。
- 在 A 的 h5、B 的 v 作替換，並在指定新四度中心反覆施工，得到
  任意大小同 class disk 族。私有四度誘導圖只含孤點及配對，每個
  四度點至多鄰接一個私有五度點，故輪環與偶長雙扇均無縮減起點。
  所有三角形皆為面及保留的私有三角形另排除密封 clique 補片及
  整來源路徑；私有最低度數四亦阻止 degree≤3 消去。
- 完整 R127／R167、共同色框 J、全部可用框及 P 保留；十五組 repairs
  及 r*=4 保留。新 D₁₃ 逆化約可逐層回到原骨架，未證允許擴張的
  改寫完備性、正常形唯一或所有代表分類，也未聲稱最小反例。

探索只限既有輪環的小範圍局部翻邊；最終證書固定 D₁₃ 的原邊與面，
不依賴探索歷程或搜尋未找到其他圖。另保存一個失敗的十二點候選：
完整關係比四輪星多24份四色框賦色，未將它當同 class 替換。

## 證書與驗證範圍

新增[checker](../../scripts/c5_two_vertex_repair_caps.py)及
[完整 artifact](../../artifacts/c5_two_vertex_overlap/repair_caps.json)，302,644 bytes，低於1 MB。
兩方向各核對 `(d_A,d_B)=(1,0),(0,1),(1,1),(2,2)`，共八個23／31／47點圖。
Verifier 從全部實際鄰域逆序核對密封附件，再驗來源 ownership、來源
disk、全部五框、clique 完整分量及保持框點的舊核心單射；局部逆化約
障礙直接從最終圖計算，另用真正輪環及 F₄ 做 degree screen 正控制。

局部掃 `4^4`、每來源掃 `4^5`、全圖掃 `4^8`，原邊回溯不使用 class
或局部等式作接受 oracle。另驗11,520份構造完整延拓、88份稀疏補全、
全部 repairs／arity 下界及十六項結構負控制。所有任意大小推論仍由
紙面歸納負責，沒有新 Lean theorem 或 `native_decide`。

既有雙扇、輪環、來源及共同 lemma 的 `--check` 均已通過。
`lake build` 完成8,827 jobs，只有既有 `SymRelabel`／`AttachmentOrder`
linter warnings。未修改 Lean 檔案。

本輪未重跑整來源路徑、密封補片、六例 transport 的獨立 checker，
未重跑來源大枚舉、其他來源區域政策或 weak-deletion 線。新圖的全部
框與 repair 前提則已直接核對。確定性與文件檢查結果於下節記錄。

## 實際驗證

證書生成、預設 hash seed 與 seed=17 的兩次逐 byte 重播，以及以下
既有重播均已通過；兩次新 checker 都與保存 artifact 完全一致：

```bash
python3 scripts/c5_two_vertex_repair_caps.py
python3 scripts/c5_two_vertex_repair_caps.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_caps.py --check
python3 scripts/c5_two_vertex_repair_fans.py --check
python3 scripts/c5_two_vertex_repair_rings.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

文件 checker 核對401份 Markdown／4,067個本地連結、章節錨點、完整
索引與 HANDOFF 格式。DocGraph 核對62份文件／213條關係／五個
families，零錯誤、零 notes。新 checker、專題及歷史檔的行尾空白另行
核對，因 `git diff --check` 不涵蓋尚未追蹤的新檔。

## 停止點與工作區

下一窄題是加入 D₁₃ 化約後的局部四接點實現，或能統一這些實現的
可檢查結構條件。全部代表必要分類、一般出口及 `K∞=K≤5` 保留。

接手時已有共同 lemma、來源、補片、路徑、輪環及雙扇成果尚未提交；
本輪保留它們，新增 D₁₃ 證書、專題及紀錄，更新兩點重疊導覽、STATUS、
state 導覽及雙扇報告的後續入口。研究線及基本操作未變，依文件治理
保留 HANDOFF／README。本輪未 commit／push。
