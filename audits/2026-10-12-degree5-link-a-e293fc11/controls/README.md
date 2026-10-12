# 任務 A 有限位置控制

目前證書為 `certificate.v2.json`，重播器為 `check.py`；SHA256 為
`cb1f620e663e955b813b250e1360e9e49b8931568e65cf852ea861aa76ea20b6`。
`verification.v2.json` 記錄正常與 seed 17 重播，以及七種破損副本的拒絕。

`certificate.json`、`check.v1.py`、`verification.json` 是保留未覆寫的初版。
初版把不滿足接觸前提的編碼標成 `counterexample`；v2 改為
`not triggered` 並附 `rejection_reason`。它們不是合法圖的數學反例。
版本差別只是此證據分類及 schema；圖、relations、lift 與位置數均相同。

## 固定有限域

九份 literal skeleton 均保留 B=`(a,b,c,d,e)`、中心 v、原 L 順序、原邊，
有向面及所有點的 rotation。它們的 B、L 都 induced；v 的鄰點恰為 L。
未填入 cap 的私有頂點，故沒有捏造未知原來源的 supports 或 fibres。
m=0 另加入實際邊 a-x，歸 annulus 所有，使整張控制圖連通；此 bridge
不是原問題強加的通用邊。切開它後的 cellular face walk 重複此橋兩次。
m=1 的外側 face walk 重複 pin a；checker 允許面 walk 重複點，
但每個點的 rotation 仍須是一個完整鄰點循環。

| 證書 ID | L | 外側區域 | k | Sigma | 十列總 full lifts |
| --- | --- | --- | ---: | ---: | ---: |
| m0-annulus | x,y,z,w,t | annulus；diagnostic bridge a-x | 6 | 1023 | 900 |
| m1-pin | a,x,y,z,w | a 重複的非 Jordan 邊界 | 5 | 1023 | 300 |
| m2-shared-edge | a,b,x,y,z | C8；共享 ab | 4 | 1023 | 100 |
| m2-C4-C6 | a,x,c,y,z | C4+C6 | 4 | 1023 | 78 |
| m2-C5-C5 | a,x,y,c,z | C5+C5 | 4 | 1023 | 78 |
| m3-consecutive | a,b,c,x,y | C6；共享 ab,bc | 3 | 1023 | 33 |
| m3-edge-isolated | a,b,x,d,y | C4+C4；共享 ab | 3 | 1023 | 28 |
| m4 | a,b,c,d,x | C4；共享 ab,bc,cd | 2 | 255 | 12 |
| m5 | a,b,c,d,e | 無外側區域 | 1 | 91 | 5 |

這些圖不是三角化、全域內點最小化／同內點數邊最大化的目錄外來源。
它們的 k 全不超過六；933／941 實際條件來源一律 `not triggered`。
有限成功不證明全域來源存在，不證明其排除，也不證一般可縮減性。
紙面中 degree 三排除的型仍保留為合法平面幾何控制。

## 接觸編碼與共同搬運

固定兩個五位置循環，選 m 個 B 位置、m 個 L 位置及循環接合位移。
在兩圈同方向 traversal 下，候選數為 631；合法數為 181，分別按 m 為
`1,25,75,50,25,5`。每個候選另保存原 L 清單相對 B 的正／反方向符號，
因此完整檔包含 1262 個 orientation-tagged 記錄，其中 362 合法、900 拒絕。
方向標記不是新的拓撲型；即使 m≤2 兩個標記可能有相同共點清單，仍不丟棄它。

對 m≥2，精確測試是成對弧長 p,q 都為正、各圈總和五，且
`p=1 iff q=1`；非共邊對的兩個長度皆至少二。m=0,1 無此多接點測試。
所有 362 份合法記錄都保存**同一個全域頂點映射**，把代表的 B、L、v、
橋及面資料共同搬運至原 literal labels。B 與 L 的 orientation 同時改變，
L 的起點位移只是循環清單的記錄；沒有各自改色名或忽略附件。
紙面 Jordan 論證才負責證明實際來源必落在此編碼域；有限枚舉本身不替代它。

## 完整 relation 編碼與獨立核對

十個外圈列依 `pattern_order` 保留。介面是 B union L，private interface
順序是 L 中不在 B 的原點；其每一份四色指派按 Cartesian product 字典序列出。
`interface_edge_ok` 保留 G-v 上的完整 properness，`center_color_masks`
用 bit c 保存原中心色 c；零值是空 fibre，並保留 proper 介面但中心不能接回
與不 proper 介面這兩種不同原因。每列也逐份保存全圖 `full_lifts`，座標順序
是 private L 頂點接 v。這是完整 joint 關係，沒有使用 marginals。

checker 用三條路徑比較每一列的**全部** full lifts：

1. 原圖所有內點四色 Cartesian product。
2. G-v 的完整具名介面指派，再枚舉同色框中的 v 顏色。
3. 用 seed 改變變數／顏色順序的獨立 constraint backtracking。

幾何核對包括每個有向邊恰落一個面、完整 dart 集、Euler characteristic 二、
每個頂點只有一個完整 rotation，以及獨立 NetworkX 外加 apex 的平面性。
面 walk 與 rotation 是真正提供的嵌入資料；apex 平面性不取代它們。
手動閱讀面表時，外面沿 B 正向，star 面為 `(v,L[i+1],L[i])`；每個 cap
沿 B gap 反向再沿 L gap 正向，因此共有邊的兩側 dart 恰好反向。

## 重播與破損控制

從 Math repo 根執行：

```sh
.venv/bin/python audits/2026-10-12-degree5-link-a-e293fc11/controls/check.py --check audits/2026-10-12-degree5-link-a-e293fc11/controls/certificate.v2.json
.venv/bin/python audits/2026-10-12-degree5-link-a-e293fc11/controls/check.py --check audits/2026-10-12-degree5-link-a-e293fc11/controls/certificate.v2.json --seed 17
```

系統 `python` 沒有 NetworkX；repo `.venv/bin/python` 具有所需套件。
`--check` 全程唯讀；`--write` 只以 exclusive create 寫入不存在的路徑。
`run_checks.py` 已執行並以 exclusive create 留下 `verification.v2.json`；
再次執行須指定新的 log 版本或另行保存輸出，不覆寫既有驗證記錄。
七種破損為漏外圈列、錯 label、錯 full lift、漏空 fibre、錯 rotation、
錯全域搬運、漏 orientation 記錄；全部預期拒絕且確認未修改受檢檔案。
正常重播及破損拒絕均為 `triggered and holds`。Lean：未執行。
