# 2026-10-03：四-spoke (3,1) 兩原 unary 的六跨度排除

使用者要求讀取 [雙 root 提交紀錄](2026-10-03-excess-two-dual-root-progress-commit.md)
並開始推進四-spoke 子型。接手基準 `b63a096`，工作目錄
`/home/ray/developer/ai/math`；工作樹乾淨，main 比 origin/main 多一份
既有本地提交。本輪未要求 commit／push，成果留在工作樹。

## 本輪完成範圍

固定完整 Σ=933／941 或整圖 D₅ 像、每條非框邊 Σ-critical、
有序 induced-C₅ disk、ε=2；相鄰唯一 mixed，兩個完整 degree-5
roots 的 spokes 分拆 (3,1)。選定原 mixed incidence-(1,1)，
一-spoke 側有兩份原單接點 unary U、V，含 root 交換。

[新報告](../c5_excess_two_mixed_core_four_spoke_singles.md)完成此整份
選定子型的任意大小來源排除。原 H−b 恰為 K=C∪{a}、U、V：
K 保留原三-spoke root a，支援跨度至少二；原 bu、bv 的整圖
Σ-critical witnesses 各迫 unary 有非空禁色見證。若 unary 支援
含於原框邊，原 b–a–b_h 路徑恢復短支援定理的全部外部前提，
反而迫禁色恆空，故兩份 unary 跨度都至少二。

重新證明不依賴分量 degree 的共同 lifts，容許 K 含原 degree-5
點；三份原支援遂要求六段，但同一框線只有五段。拓撲收縮只用於
這份幾何反證，不保持完整 Σ，也沒有替換原染色 relation。
主證明不需要候選特定拒絕位置、T4 或指定列 minimality。

## 完整關係與固定核對

新 [checker](../../scripts/c5_excess_two_mixed_core_four_spoke_singles.py)
與 [joint helper](../../scripts/c5_excess_two_four_spoke_joint_controls.py)
保留原 contacts、全部實際 attachments、ownership、root 交換、
同一字面色框、完整 C tuple 及每份 joint coloring witness。

- 156 份繼承支援 records，含整圖反射與來源 artifact index。
- 80 份有序附件、200 份原 spoke 省略／拒絕列查詢；688 份
  child records 合成 288 份同源 C／U／V 支援域。
- 每份域的兩 unary 均短支援；576 份原 b–a–b_h 路徑前提
  核對後由紙面定理全部排除。此域是必要放寬，不是來源圖。
- 全部 21 份長支援、五個原 spoke 位置，共 46,305 組共同
  lifts 核對無解；保留 (1,2,2) 正控制及 50 份原外路徑選擇。
- 十二張含 root 交換的固定完整度數圖、360 次整圖接合、
  5,760 次 pinned (b,a) 的完整 (y,u,v) 色纖維、72 份同色 spoke
  等式均與獨立回溯一致。兩份 unary 始終保留各自原 identity。

完整 C 的 `(0,0)/(3,3)` shared-contact 負控制，與非空省略圖
接回原 spoke 全濾空的實際控制都保存。這些固定圖沒有 disk、
Σ-critical 或候選實現聲明；不得以 marginals 代替 complete joint。

## 重播時發現的前序來源雜湊漂移

既有 leaf-fibers 的 `--check` 首次失敗。將當前 `build()` 與既存
JSON 逐欄比對，**唯一差異**是
`input_sha256/docs/c5_excess_two_mixed_core_single_spoke.md`。
該報告刪去前序 commit 所加的「提交整理」導覽段落後，SHA256
恰為證書記錄的
`75d5ef5715da6134e1778f218d4f18843875a0d45f58adf51692777f994503e5`；
當前完整文件 SHA256 是
`bd2ba3c728c89bf5da601a26293ca52a033fe64252526a2187db53a433cdfe7e`。
本輪沒有改動該單-spoke 報告。

只修正 leaf observations 的這一份 doc hash；全部 relations、fibres、
witnesses、minor、summary、長度與既存計算資料不變。原產物
2,397,122 bytes，整檔 SHA256 從
`a9be10516fa2acf4960a793037d51da4588db65ac4d2e061279c236acafe0cce`
更新為
`f39f18c0955e470927ad7468356cf3d3627c9522b7563d0c9d05b98862e3c8ef`。
修正後 pinned `--check` 通過。這是 provenance 修正，不是新的
五-spoke 計算結果，也不改寫前輪的實際驗證時間。

## 實際重播與檔案政策

以下均在本輪實際通過：

```bash
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_singles.py --check
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_singles.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
lake build
```

兩份新 `--check` 逐 byte 比對既存新證書，沒有覆寫。`lake build`
通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel linter warnings。
新 observations 為 **13,771,331 bytes**，SHA256
`26ffc72f2b501aedfb23525cf1ed7d7c8059b5ac496deb9439befa44c74e6e5a`。
依既有政策置於本地、由 `.gitignore` 排除；MANIFEST 登錄 producer、
完整 bytes／SHA256／fingerprint 與依賴順序。前序 leaf 只更新上述
一份來源 hash 及其 manifest digest。

文件檢查通過 **487 份 Markdown／4,998 個本地連結**，anchors、
直接索引與 HANDOFF 全通過；DocGraph 通過 **62 documents／213 relations／
5 families**，零 errors／notes。大型產物 `ok=126`，無 missing／changed／
stale；`git diff --check` 通過。
本輪未重播全部九份雙 root checker、全部唯一 degree-6 分拆、歷史
catalogue／Gallai／weak-deletion／Kempe／R-series 或 Lean axiom audit；
按原報告範圍沿用。有限支援、graph controls 及 `lake build` 均不
形式化新紙面 topology 或證明任意 abstract relation 的 disk 實現。

README、STATUS、Kempe 導覽、全線整合頁及前序 leaf 的後續連結同步。
HANDOFF 的研究線與進行中 tag 不變，依薄索引治理保留原檔。

## 停止點與跨對話摘要

**本輪停於可證的選定子型排除。** 下一入口是四-spoke (3,1)
的 mixed-(1,1) 加一原 binary unary，省略同色 spoke 得 t=1、
(2,2) core；尚未啟動新搜尋。原 binary 的完整兩接點 relation
不能拆成兩份 unary。另兩份 mixed incidence 分拆及其他來源均保留。
共同下界仍 ε≥2；ε≥3、一般出口及 K∞=K≤5 未證，未新增 Lean theorem。

```text
工作目錄 /home/ray/developer/ai/math；先讀 docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md 及本輪紀錄，再查即時 Git。接手 b63a096；本輪未commit/push。
固定933/941完整Σ、edge-minimal induced-C5 disk，ε≥2；唯一degree6的ε=2全排。
相鄰唯一mixed的五spoke全排；本輪進一步全排四spoke(3,1)、mixed(1,1)
加兩單接點unary，含root交換。原H-b三分量K=C+a、U、V各跨度≥2，
短支援原外路徑及同圖共同lifts給6≤5。288同源支援全排；360 joints、
5760 pinned完整(y,u,v)纖維及46305支援核對通過。前序leaf只修正doc hash漂移。
下一窄入口：(3,1)+mixed(1,1)+一原binary，省略同色spoke得到t=1,(2,2)，
保留原leaf、C、binary完整joint、附件、ownership與同一色框。
mixed(1,2)+unary、mixed(1,3)、其他四spoke/較少spokes、原(5,5) core、
多mixed/no-mixed/非相鄰roots及單省略保留；ε≥3與K∞=K≤5未證。
紙面+固定Python，未新增Lean theorem，不重開來源圖枚舉。
重播：PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_singles.py --check
```
