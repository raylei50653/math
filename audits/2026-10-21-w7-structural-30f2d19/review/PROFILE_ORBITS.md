# 每個固定原接觸型與完整 target orbit 的共同篩選

2026-10-21；Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。

承接 [原來源契約](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[本輪幾何](../geometry/PROOF.md)與[兩個 target 的完整 component 分類](PROOF.md)。
本項只讀 69 個已通過原幾何必要條件的固定 profiles，對每一份原 profile
**各自**篩選原 15 個 target orbit columns 的全部 16 個 half-rows。
不求解 LP、不枚舉新原圖、不混用不同 profiles 的可行片段。

生成後的幾何依賴為 `geometry/certificate.json`，611,832 bytes，SHA256
`ee7b544a16192a9e6d4b37682d7177f03981acc8e427bc188777ff6f942bdcba`。
[checker](profile_orbits.py) 另核對它消費的原輸入 bytes／SHA，與本輪 BASE
共有的依賴逐項相等；幾何所用另一份 frozen B/PROOF 也依該證書 hash 核對。
原 caps 與 complete orbit family 均另與 BASE 核對。

## 完整原邊篩選引理

固定一份原 profile，令 E 為其中全部可選但在該 profile 中實際存在的原弦。
若原 column C 中有任何一份 normalized half-row t 在某原弦 ij 上滿足
`t_i=t_j`，則實際原來源必有 `X_C=0`。因為完整 actual Kempe orbit 必須
含該投影；全域框色正規化保留同色關係，這份投影不可能是一份原圖著色。
所有 private components 的正重數均不會修復原邊上的同色衝突。

這要求核對 C 的**全部** rows；只核對所選 target tuple 不夠。等價的
component 判準是：不同 palette 的端點總合法；同 palette 的端點必須
在同一實際 component，且它們在 reference row 的顏色不同。若是不同
components，至少一個非 anchor component 可獨立翻轉，便產生同色 row。
若在同一 component，兩端共同翻色，原本異色即永遠異色。

[profile_orbits.json](profile_orbits.json) 逐 profile 保留全部原弦、三族
surviving column IDs，並為每個被刪欄保留一份實際同色 row／原弦見證。
checker 對所有 69×15 組同時比較「逐一完整 row」與「完整 component」
兩種判準，結果完全一致。空的 target fibres 按原方程保留為零。

## 結果：40 型未再減少，但 28 型僅剩兩個 joined columns

A 表示 target 44459，B 表示 target 44466。各 profile 固定後的完整支持為：

| 原 profile 數 | A 欄數 | B 欄數 | 共同欄數 | 結論 |
| ---: | ---: | ---: | ---: | --- |
| 12 | 10 | 10 | 5 | 原 15 欄全部保留 |
| 16 | 2 | 0 | 0 | 只可能有 A；K01(v,w) 接上 a,n,c 與一個 ui |
| 12 | 0 | 2 | 0 | 只可能有 B；K01(v,w) 接上 a,n,c 與一個 ui |
| 29 | 0 | 0 | 0 | 此固定 profile 不可能供應所需 target 正量 |

所以共同 target 支持仍是原來的 **40 個 profiles**（A 有 28，B 有 24），
本項沒有在幾何的「target 字面框合法」之外再排除新 profile。不能把這個
停止點描述成 W7 已排除或新幾何型已被消盡。

但 28 個單向 profiles 的完整支持從原 10 欄降為 **2 欄**，並排除整個
separated stratum。這些型可進一步精確分為：

| 固定原弦的必要特徵 | profile 數 | 保留欄 | 原中間 block 型 |
| --- | ---: | --- | --- |
| `u3v` | 8 | A: 66582, 67755 | 4 或 5 |
| `u1v` | 8 | A: 48617, 67755 | 3 或 5 |
| `u3w` | 8 | B: 66602, 67765 | 4 或 5 |
| `u1w` | 4 | B: 48647, 67765 | 3 或 5 |

表列 profile IDs 與每份的全部額外原弦均在 JSON 中；「必要特徵」不是以
該單邊取代完整 profile。例如原 profile 10 恰有 `u3v`。A 的字面框在此
原邊上合法，然而原本 10 個 A-support columns 中只有 66582、67755
在所有交換 rows 上保持合法。43330 雖含 A，仍有一份完整交換 row 在
`u3v` 同色，必須刪除；這是 checker 的 witness-only 負控制。

具體地，在任何一份 `u3v` 的上述固定 profile 上，完整同源方程變成

\[
2Z_{44459}=X_{66582}+X_{67755},\qquad Z_{44466}=0.
\]

另外三列同理：分別用該列的兩欄及其唯一 target。由已恢復的完整
component partitions，K01(v,w) 與 a,n,c、指定的 u3 或 u1 在同一
01-component，且 s,t 為不同 23-components。所有其餘原私有點與
component 重數仍留在同一實際核心和原 X 內。

這提供更窄的原來源待證命題：對這 28 個單向 profiles，研究可集中在
上述兩種 joined 接觸型；另外 12 型仍必須處理共同 separated 部分及
各五個 joined 型。不能將某 profile 的排除移用到另一個 profile。

## 重播與邊界

```
python3 -B audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.py
```

三次唯讀結果一致；完整 rows／component 兩法逐一相等，witness-only
負控制有效。這是逐固定原 profile 的必要 source-orbit 篩選，沒有求出共同
計數解，沒有證明原圖實現，也未證明剩下的欄能承載正量。嚴格 W7、
一般 J1/J2、smaller bad 及 Lean 仍未完成。
