# 941：同一 U02 分量的完整鄰接禁制

2026-10-23；exclusive BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

**新增一項同源幾何限制，沒有排掉任何初始配對。** 普通短型 I 的02型13／36，
令 K 為同一份實際 F 著色的完整 U02 分量。K 與含 z1、z3 的兩個完整13
分量均無原邊，連那些分量的私有點也不能接。這適用兩種初始03型；不是只
排 U—z1、U—z3 兩條邊。

若另為03型4，任意 U→z4 的03路都有一個可指定的「最後離開 K0」私有
色3點 X；X 在完整 K 交換前、後皆接原 a 弧。其原五度 link 的第五色2
鄰點是否屬 K，精確由它相鄰的色0 link 鄰點決定。第五鄰點兩側及偶數度
至少六都保留。完整證明見 [PROOF](PROOF.md)。

## 固定來源與新舊差異

本項只看 U、V 均為原 E 私有點的普通六度短型 I，同一 F／有序B14／原
色框／全部原附件／原 stars 與 rotation 不變。原01四型、03二型、02四型
都保留；未把獨立 survivors 拼成一份來源。來源由凍結的
[六度完整報告](frozen/audits/2026-10-21-w7-L-path-30dde27/six_degree/REPORT.md)
及[原joint報告](frozen/audits/2026-10-21-w7-I-joint-2c38d1d/REPORT.md)限定。

舊結果已有混合配對的某個私有交錯點、五度第五色，以及 U02 交換後唯一
03後繼。本項新增的是：完整 U02 分量與兩個完整13分量的**跨分量原邊
禁制**；以及帶有實際 K membership 的最後離開點與交換前後03同屬性。
此點沒有被冒認成任取 V→Y 路的交會點。

證書逐份保留四個 target／02型的完整初始02 contacts、原01四型、兩種03
選擇、唯一後繼的全部 boundary blocks、同一全域 inverse、該像全部七點
共同 lifts 與其完整 G／Q1／J1 cap records。上游完整二步證書按 bytes 凍結，
包含全部空 fibre；本項沒有重寫上游計數或任意選一份 cap lift。

## 有限核對與界線

[check.py](check.py)核四份具名02型的完整分量、每份兩個 anticomplete
義務、交替端序及 barrier 的完整 V,Y,q,c contacts；也核唯一後繼與 full
kernel/cap引用。有限完整原 link 校準分別遍歷 degree5／6的 proper 鄰色
及相容 K membership，不枚舉來源 disk。六個 palette 的精確刪除／插入
公式另在顯式 wheel 上與直接完整交換逐項比較，rootless 分量保留。
結果為20份五度與84份六度相容 marked links；六度中12份沒有色2，兩個
第五鄰點 membership side 都保留。六palette直接交換校準共432項。

這些 wheel 是局部 operator／link 控制；完整941來源前提 **not triggered**。
它們不提供來源、較小bad或全稱排除。原小盤02／03正控制仍敗於01與最低
度數，本項未將它們提升為來源反例。全稱無邊與 privacy 推論由紙證承擔，
沒有形式化為 Lean。

```sh
python3 -B audits/2026-10-23-three-mask-methods-cb8f859/941/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-three-mask-methods-cb8f859/941/check.py --seed 17
```

正常／seed17、負控制與 input drift receipt 見 [verification](verification.json)。
負控制包含刪除 barrier 的 Y、刪完整13禁制、假造 K 的第二個框接點、刪
完整七點 lift／cap lift、排掉高度數分支及冒稱已排配對；另拒絕漏掉插入
私有點的錯誤交換公式，合計九項。外部破壞 barrier 證書亦以非零退出拒絕。

## 凍結與停止點

[INPUTS](INPUTS.json)記錄九份 BASE authority 的 bytes／SHA及三份已 dirty
shared routing docs 的 entry bytes。三份 dirty routing docs 只供路由背景，
不作新數學前提；沒有寫入 shared docs、舊 audit 或其他工作者目錄。
checker 核 frozen bytes 並比較 live mathematical authority，input drift為零。
未 commit／push。

兩 target 各八配對仍 OPEN，原 W7仍38／40；一般J1／J2、完整來源實現與
較小bad均未完成。本項沒有轉攻 J2 III，因為主線已取得上述具名新限制。
下一步可用實際私有鄰接圖把 anticompleteness、最後離開點與唯一後繼一起
套入；仍須保留任意大小私有分量、兩個第五鄰點 side 及原度數至少六分支。
