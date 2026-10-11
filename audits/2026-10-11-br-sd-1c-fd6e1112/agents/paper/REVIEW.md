# BR-SD-1c：父端 PROOF 的獨立逐段審查

日期：2026-10-11。Reviewer：paper worker。研究 BASE：`fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69`。
審查輸入：父端 `PROOF.md`，SHA256
`649ad89d0f05de602ee29c13a2aba02eb1f2d72ec0edd4672b802e3d81288a25`。
以下行號指該精確版本。本文只寫在 reviewer 的專屬目錄。

判定：**精確 one-W source exclusion 證明成立；可重用局部引理須明列 terminal q 無額外 C 邊。**
這是局部引理文字的必要前提精度 finding；主命題的完整 one-W 骨架已具此前提，沒有主結論缺口。
沒有審查或確認來源實現、canonical 採納、一般 Gallai trees 或 Lean。

## 逐段核對

| 段落／行號 | 獨立核對 | 判定 |
| --- | --- | --- |
| §1，10–35 | 研究對象是保完整原身份、把 no-branch 形狀條件放寬為一份原 W 的來源家族；不是在某張 BR-SD-1a 已存在圖上增邊。W 的原 attachments 仍由候選自己供給，沒有以 palettes 推來源。接 J1/J2 分別保 L/S ownership。 | 成立 |
| §2，39–53 | r 的四 cycle neighbors 已飽和。a1 正臂：2 cycle+1 arm；零臂：2 cycle+1 s-edge。兩者有 m≥1 時皆 m=1、k=0。u 原 cycle2+uv1 同樣只容一條 W 邊。ordinary 私有點容 m≤2。 | 成立 |
| §3，58–85 | 同一完整 degree4 給 list 下界；s=D 對原 β 的三 spokes 合法；C sole 保完整拼接未漏分量。Theorem 10 的 palettes 分解與相交互斥使用正確，沒有先假 tight。 | 成立 |
| §4，89–99 | 未接入環排除至多兩點；受影響長環排除至多三點；triangle 只有唯一第三點被 W 佔用才可能失效。w 非 C 割點、非 s-contact，list=P_J。 | 成立 |
| §5，103–111 | J2 sole triangle witness 被佔用時 u 沒有 W。J3 的 w3 永遠存在、D∈P_J3，故 uv palette 不含 D；u 完整 incident list 只由 J2／uv 分解，迫 D∈P_J2。 | 成立 |
| §6，119–140 | 支援是全部實際 B 鄰點集合，exact-S 只刪 r-spoke，pair 添附不變。真 B edge 的 β 色異色。w3 dC2/t0/full-degree4 強制兩附件恰 pair，故實際 L(w3)={T,D}，P_J3={T,D}。triangle 及 a3=v 包含。 | 成立 |
| §6，144–152 | 零臂 q=a3 排 D；一邊臂 terminal q dC1/t1/k2 得 list {T}；長臂第一內點 z dC2/t0/k2 得 {T,D}。每個臂 bridge palette 非空且包含於此 list，均在 a3 與 J3 palette 衝突。 | 在明列原末端／simple bridge arm 合同下成立 |
| §7，160–175 | 所列 abstract palettes 相交互斥；x list {A,B,D} 的 D 只屬 xy。所有 non-s-contact lists 含 D，contacts a1/q 不含 D。撤 actual pair 的合成圖未被稱為原 disk source。 | 合法必要前提負控制 |
| §8，179–190 | 精確一份 W、J1/J2 接入、原 pair-supported J3/q 臂未動的 source exclusion 任意大小；一般父身份、來源實現與 Lean 均保留界線。 | 成立 |

## 唯一精度 finding：局部引理的臂端點

行127–130的獨立「局部引理」只寫「外臂內點沒有其他 C 邊」。普通 path 用語的
內點不含 terminal q，但行146明用 `d_C(q)=1`。若讓 q 同時 incident 另一個 C-block，
這個 degree 等式不再可用，其 list 也未必是 {T}。

建議精確補成：「外臂每個 a 以外的頂點在 C 中只有該臂的 path 鄰居；
正長時 q 是 C 的末端，d_C(q)=1，內部臂點 d_C=2，臂邊是 bridge blocks。」
主 theorem 的原外臂、唯一 W 僅接 J1/J2、沒有其他 blocks 接入骨架的合同已供此條件。
因此這是重用引理時需明列的必要前提，沒有撤銷主 theorem 的 scope。

另確認§1、§2不要求從既有來源刪附件以接 W。比較的是來源家族的 C-block 形狀，
每個候選從一開始就以自己的實際完整附件計 degree4；本文沒有給候選存在性。

## 審查方法與未查範圍

先獨立推導 `PAPER.md`，再讀父端上述 hash 版本逐段重算。Formal 外部依賴已即時重讀
[作者 PDF 第6頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，並對回舊凍結 SOURCE。
未新增枚舉或 Lean；controls 的原列表／完整 tuples 與 root MAPPING 交由各自 worker 保存。
當時 controls REPORT／root MAPPING 尚在交付，這些導航連結不被當作紙面推論錯誤。
本文沒有把未完成的導航資料視作已驗證來源證據。
