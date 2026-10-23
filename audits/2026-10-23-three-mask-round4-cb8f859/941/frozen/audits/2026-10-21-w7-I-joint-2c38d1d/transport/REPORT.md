# 同一 F 的 03→02／02→03 二步必要分量審核

2026-10-21；exclusive BASE `2c38d1dcb4490017312467deb19d9da02b7bb2a6`。
只承接普通 U、V 均為原 E 私有點的型 I；固定原 `F=D−(V(P)∪{z5})`、
有序 B14、所有原附件、原 z5 完整六度 star、七點共同完整 fibre 及全部原 cap。
V=w 別名沒有套用本審核。

**這個二步必要審核沒有排掉 03 的任一型，也沒有排掉 02 的任一型。**
它不證明初始 03×02 的八個配對能在同一來源實現；另一 split 在各動作後的
實際分量更新仍未由初始 boundary partitions 決定。

## 1. 審核的全稱／存在次序

固定同一份實際原 F 著色。第一 split 的每個選定分量都連同全部原私有點翻色，
未選分量保色。對每一個第一步所得的實際完整 F 著色，第二 split 的實際
boundary partition 必落在該字面輸入的全部必要 NC 型內。因此若其中某個
第一步像的第二 split **沒有任何**完整作用皆不觸犯原 cap 的必要型，才可排
初始第一 split 型。

本項分別核：

* 03 的兩個必要型，逐型全部 32 個完整 F 分量作用；每個像再核 02。
* 02 的四個必要型，逐型全部 64 個完整 F 分量作用；每個像再核 03。

第二步每個 NC 型都保全部碰框的實際分量作用。對每個像固定同一份完整 F，
枚舉 `(n,u4,u3,u2,u1,L,z5)` 的全部 proper 七點共同延伸，再逐份接原完整
G／Q1／J1 cap。空七點 fibre 照樣保留，沒有當作外側零。

這是合法必要覆蓋：真實第二步分量型必在枚舉家族內。它不替真實來源選定或
拼接各像的分量型；同一像的不同 candidate 也不被當成可以共同存在。

## 2. 結果

兩個 target `44459`、`44466` 結果各自相同：

| 第一 split | 初始必要型數 | 二步後仍留 | 各初始型在所有第一步像上的第二 split 存活型最小數 |
| --- | ---: | ---: | --- |
| 03→02 | 2 | 2 | 4、3 |
| 02→03 | 4 | 4 | 2、1、2、1 |

型順序逐字使用父 `certificate-v2.json.gz` 的
`surviving_types_after_same_initial_E_gate`，沒有換初始原 E 見證或重套 residual gate。
所有第一步像皆至少容許一個第二 split 必要型，故這條二步測試沒有新排除。

共核 214 份經全域色置換歸一的中間字面／第二 split 輸入、99,009 個所用的
字面作用像、23,152 份完整七點 kernel，以及 28,987 個原 canonical D cap
states 的全部完整 cap assignments。kernel 中有 1,186 份空七點 fibre，全部保留。
這些家族只由上述初始型的第一步像產生；沒有枚舉通用 C14 family 或來源圖。

## 3. U 的 02 分量單翻後，一支強迫唯一的 03 型

02 第 2、4 型都是 U 的 02 塊僅有 `{U}` 這個 boundary contact，而 V 的
13 塊接 Y。只翻同一個完整 U02 分量（原 partition 標號的 `mask=32`），
其餘原分量保色。boundary 中恰 U 由 0 變 2；它的全部私有點仍一起翻色。
此時 03 的全部必要型經完整作用＋七點＋cap 後，唯一留下：

```text
target44459：{a,z1,z2,z3,z4} | {V,U,Y,w,t} | {q,v} | {c,s}
target44466：{a,z1,z2,z3,z4} | {V,U,Y,t}   | {q,w} | {c,s,v}
```

這是同一 F 的真實動作後必須符合的新分量義務；單一 boundary contact
仍不表示 U02 沒有其他原私有點。`mask=31` 為此動作再作全域 XOR2 的等價
另一像，亦只有同一 boundary partition 通過。它尚不排初始 03 的兩型。

## 4. 為何仍不能任意更新第二 split

例如只翻某個完整 03 分量：其中原色 0 點離開 02，原色 3 點進入 02；
原 02 邊可能消失，原 23 邊可能成為新的 02 邊。初始 02 與 03 的 boundary
partitions 不記錄它們在私有點上的交會、分量內部路線或這些邊。故單靠兩份
初始 boundary partitions，不能唯一推出第二 split 的更新 partition。

本項保留該未知量，對真實更新所有可能落入的必要 NC 型作覆蓋。各第一步像
至少一型通過，只代表此覆蓋未導出矛盾；不能宣稱同一來源已實現這些選擇。

## 5. 同一全域逆色置換與重播

每個字面像保完整 boundary word、一個作用於全圖的四色色置換 inverse，及
完整歸一 kernel 的參照。這同一 inverse 逐點還原 boundary、全部七點 tuple
與每份原 cap assignment。cap canonical rim 的逆色置換也依同一 D tuple
決定；沒有獨立挑 cap 色框或只留一份內 lift。

```sh
python3 -B audits/2026-10-21-w7-I-joint-2c38d1d/transport/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-I-joint-2c38d1d/transport/check.py --seed 17
```

normal／seed17 均完整重算並核對同一 [certificate.json.gz](certificate.json.gz)。
十個負控制拒絕：補造未知跨 palette 更新、拼接獨立 survivors、冒稱型 I 排除、
冒稱原來源實現、冒稱通用 C14、冒用 V=w、刪七點完整 lift、破壞全域 inverse、
刪完整分量作用、刪原完整 cap assignment。

本項沒有證明或排除任一 03×02 初始配對的同源實現，沒有新 source exclusion、
LP、Lean 或 matching 結論。必要的同源交會幾何仍須由其他原 F 證據建立。
