# 獨立審查：全內部 W5 的具名完整關係

2026-10-12。審查 BASE `e299ae987fcc4cdeb55dd41bede0a3a7c9d9db86` 的
上游契約、[本輪 REPORT](../REPORT.md)、[THEORY](THEORY.md) 及正式 controls。
結論：目前紙面主張在明列範圍內成立；完整關係消去已有精確解碼，普通平面
disk 關係的正聯集縮減與一般 annulus 小代表仍 OPEN。

## 1. 紙面審查

1. **中心與完整 fibres。** 在 induced C5 上，proper 四色染色只可能用三色或
   四色。前者恰有唯一缺色可補 v，後者沒有。限制映射由 G 的完整 lifts 到
   H 的可延伸完整 lifts 是雙射；不能只保留外 B 的接受 bits 或 U 的獨立正規形。
2. **合法單對 quotient。** 空五邊面內加入一條對角弧再收縮，得到 Q_j。
   原端點非鄰接，所以沒有 loop；平行邊簡化不影響染色，但需保留原邊 preimages。
   B 不參與識別。兩個 U pin 在商圖同頂點，仍是兩個原名稱，經固定 pi_j 拉回。
   此拉回與原 H 中相應等式成立的完整 lifts 雙射。
3. **逐 lift 重數。** 五環的獨立集大小至多二。三色類大小為 (2,2,1)，
   因此一份 H lift 屬於兩個 quotient pullbacks；四色類大小為 (2,1,1,1)，
   因此恰屬於一個。逐項係數 `sum_j 1[eta in S_j] - 1` 恰為 0 或 1。
   保留係數 1 並補唯一缺色，重建每份 G lift，包含每個空 cell 的正確處理。
   因重數永不為零，五個 pullbacks 的聯集恰為全部 H lifts；給定五份 Q 的
   完整資料及固定映射，即可重建 H 與 G，不必另枚舉 H。
4. **計數的確切能力。** 若知道各固定 beta 的實際完整染色數，帶符號計數式
   足以用結果是否大於零判定該 beta 是否可延伸。十個非空 bits 不足以計算該數；
   計數本身也不重建具體 full lifts。REPORT 將這三層分開是必要且正確的。
5. **五個 sector。** 三色五環有唯一 singleton；對應的兩個等式同時由同一
   eta 成立。五 sector 互斥並完整覆蓋 G 的限制 lifts。各等式分別有 witness，
   或各 quotient 的外框關係都接受同一 beta，不能代替同一 eta 的聯立等式。
6. **零新頂點局部限制。** 保留 U 五環、僅加邊的圖，只要有一個非邊，即可讓
   該兩端同色、另三點各用不同色，得到四色著色；K5 則根本沒有四色著色。
   因此所有非空關係分支都包含 wheel 不接受的四色 tuple。允許面內非交叉
   識別後，至少仍有四個 blocks；若已有三色著色，拆開兩個同色 blocks 中
   之一並用缺色即可得到四色著色。這只排除普遍適用於所有 annulus contexts 的
   此類局部正聯集，不排除指定 H 自身的額外限制或可改動 annulus 的操作。
7. **代表的兩向 lifts。** (beta,tau) support 相等，足以選另一側同 cell 的
   lift 並補中心，得到雙向延伸存在性。原、新私人頂點不同，不能因此宣稱
   fibres 等基數或一對一。十 pins 與嵌入槽位保留後，r<=6 才給 6+r<=12。

## 2. 雙對 quotient 的明確非平面反控制

取普通五角柱 annulus：B、U 各為五環，加五條 `b_i u_i`。
在 U 內補中心即為符合本輪幾何前提的全內部 induced W5 控制來源。
同時識別 `a=u1=u3`、`c=u2=u4`。刪去 `u0` 後得到一個 K3,3 subdivision：

| 左側 | 右側 a | 右側 b2 | 右側 b4 |
| --- | --- | --- | --- |
| c | c-a | c-b2 | c-b4 |
| b1 | b1-a | b1-b2 | b1-b0-b4 |
| b3 | b3-a | b3-b2 | b3-b4 |

九條 paths 的內點互不重複，唯一非空內點集合是 `{b0}`。所以這個雙對商圖
本身已非平面，不只是原空五邊面的畫法有困難。這不反駁五個單對 Q_j 各自
合法，也不表示每個特殊 H 的雙對抽象商圖都必非平面。

## 3. 獨立 checker 與另一個有私人頂點的來源

[independent_check.py](independent_check.py) 僅用 Python standard library，
不匯入正式 checker 的任何 helper。它以不同的 degree 優先 DFS 直接枚舉圖著色，
預設只讀重算 [independent_results.json](independent_results.json)；
`--write PATH` 只允許 exclusive 新建，`--check PATH` 不寫證據。

獨立來源將普通 prism 的 `b0-u0` 細分為 `b0-x-u0`，而不是正式 decorated
來源的加點保留原邊操作。編號 B=0..4、U=5..9、x=10、v=11。H 的面表為：

```text
外面: (4,3,2,1,0)
annulus: (0,1,6,5,10), (1,2,7,6), (2,3,8,7),
         (3,4,9,8), (4,0,10,5,9)
內面: (5,6,7,8,9)
```

這是兩個同心五環加匹配邊，再細分一條匹配邊的明確平面構造；H 有
V=11、E=16、F=7。用五個 `(11,5+i,5+(i+1 mod 5))` 三角面取代內面，
得到 G 的 V=12、E=21、F=11。所有 U 點皆為原內點，且內側只放 v。

| 獨立有限檢查 | 結果 |
| --- | --- |
| 全部 rim tuples | 1024；proper 240，其中三色 120、四色 120 |
| 五個等式重數及五個互斥 sector | 240 個 proper tuples 全數相符 |
| 原 U 上全部對角邊子集 | 32；零個等同 wheel 關係；零個非空 sound 分支 |
| 細分 prism 的完整 cells | 10 列乘 1024，共 10,240；包含每個空格 |
| H 完整 lifts | 1853 |
| G 完整 lifts | 932 |
| 五個 Q 的完整 lifts 總數 | 2785 = 1853 + 932 |
| 各 Q 直接 DFS 與原 H 等式過濾 | 完整集合一致，拉回為雙射 |
| 逐 lift 解碼後與直接 G DFS | 完整集合一致 |
| 雙對 quotient 非平面證據 | 上述九條 K3,3 paths 全數核對 |

## 4. 正式全量證書的獨立再枚舉

`--primary` 直接讀取正式 gzip certificate 的 literal graphs，以獨立 DFS
重算所有 H、G、Q 著色，逐個 beta、tau cell 比較完整向量列表，包含空格；
另重建每個商圖的頂點映射、邊集與固定原 pin 次序。沒有匯入、呼叫或共用
正式 checker 的列舉函式。

本次執行 PASS：34 個來源、340 個 rows、348,160 個 cells、3250 個 H lifts、
1620 個 G lifts、4870 個 quotient lifts。正式 sources 的嵌入由原 checker 的
面 darts、頂點 link 及 Euler 條件檢查；獨立比較的重點是完整關係與 lifts，
不將第二份 DFS 稱為另一套一般平面嵌入驗證器。

```bash
python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/review/independent_check.py --primary audits/2026-10-12-w5-marked-relation-e299ae98/controls/certificate.json.gz
```

本次正式 gzip certificate SHA256：
`3f5c943c72c206e89b6efcef688f107a9b1c8459d0a5c1b4a61a02f759123a8d`。
獨立 certificate SHA256：
`1903e30be8a2e5426bedbd497fae5ce18e20dc54c322926c6e96a8dc25ad3740`。

## 5. 審查範圍

上述合法 synthetic 控制均有實際觸發；不是最小目錄外來源或 933／941
實例。後者維持 `not triggered`。一般五度縮減、普通合法正聯集、r<=6
annulus 代表及 K∞=K<=5 都維持 OPEN；本輪沒有 Lean theorem、共享文件
採納、commit 或 push。有限枚舉核對本輪恆等式，不補足這些剩餘義務。
