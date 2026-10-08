# M2：U1 no-mixed 兩-root (4,4) 排除的獨立稽核

2026-10-07。**狀態：完成，交付使用者驗收。未發現新的阻斷缺口或數學反例。**
本包只稽核 [U1 報告](../../docs/c5_excess_two_no_mixed_core44.md)；
M3 的全分支還原／LC build、M4 的 PR／CI 及合併不在本次執行範圍。

| 項目 | 固定值 |
| --- | --- |
| 受驗候選 SHA | `ba0b447f09617591d9f2ba81c988f537af771791` |
| 候選 parent／M1 本地 base | `a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42` |
| checkout 的 origin/main 參照 | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`；只是本地參照，未查遠端即時狀態 |
| 獨立 checkout | `/tmp/math-m2-ba0b447-audit`，detached HEAD，沒有 scratch 交付 clone |
| 執行環境 | Python 3.14.7，獨立程式僅用標準函式庫 |
| 交付 SHA | 無新提交；候選來源與原證書未修改，本包是新 audit 輸出 |

## 1. 兩個分開的稽核結論

**任意大小化約：成立，限明列來源前提及繼承的分類／拓撲信任。**
原 zw 保留、原 pieces 全取／全不取、loss-(1,1) 身份完備性、941 三-spoke
更正、leaf D-forcer／triangle palette 矛盾，以及保留原 singleton bridge markers
的完整十列聯合 relation 化約均成立。被省略原 U 的大小沒有新增限制。
詳細逐項論證、候選行號及依賴分見 [身份紙面稽核](paper-identities.md) 與
[344 域紙面稽核](paper-reduction.md)。

**有限必要域：成立。** [獨立 verifier](verify.py) 對全部 344 核心及 3,498
具名雙-spoke 接回作全圖回溯；逐列完整有序 root pairs、所有存放的 witnesses、
空 fibres、接回索引及完整 Σ 與原證書一致。沒有 import 原 checker／producer
決策邏輯，沒有 planarity oracle。兩個正式輸出
[default](independent-default.json)／[seed17](independent-seed17.json) 完全逐 byte 相同。
程式策略與檢查細節見 [checker 說明](checker-notes.md)。

這些結論不構造完整 Σ933／941 的來源，不把有限控制當任意大小完備性證明，
不新增 Lean theorem。U1 的限定排除可交付；本報告不宣告整個 no-mixed 來源不存在。

## 2. 紙面逐項判定

共同前提是有限簡單圖、指定有序 induced C5 為 disk 外框、完整 Σ 為 933／941
或其整圖 D5 像、每條非框邊 Σ-critical、連通有效 H、相鄰原 degree-5 roots z,w、
其餘原有效內點完整 degree 四、H−{z,w} 沒有 mixed。M 是全體拒絕同一字面 q
的子圖中的 inclusion-minimal core，之後選取保留兩 roots 且 core degrees=(4,4)
的子型；不是限定保留 roots 才作 minimality。

| 核對項 | 判定 | 核心理由及依賴 |
| --- | --- | --- |
| 原 zw 保留 | 成立 | 若省略，固定同一 q 後兩原側獨立；某側單獨拒絕，便可去掉另一側，違反 M 的全域 minimality。沒有假设 G−zw 全收。 |
| 原 piece 全取／全不取 | 成立 | 留下的原 degree-4 點在 M 仍至少 degree 四，因此所有原 incident edges 飽和，沿同一原連通 piece 傳播。 |
| loss-(1,1) 身份完備性 | 成立 | zw 保留且 no-mixed；每側只可省略一 spoke 或整份 capacity-one U。E6-D 給每側恰一原 U，兩側都省略 U 需雙三-spoke，已排。 |
| 941 三-spoke 收窄更正 | 成立 | E6-D 容許 941 字面 013 型一側三 spokes；雙-spoke身份須包含 (2,3) 及交換。344 接回域不使用舊的 t≤2 錯誤限制。 |
| spoke＋unit-U 的 D-forcer | 成立 | M 的 leaf w 有三個互異 q-spoke 色，故只可 D；此 bridge 強迫 D。使用 M 自己逐邊 minimality，不使用 G 的 q-minimality。 |
| triangle palette 衝突 | 成立，繼承拓撲信任 | z 的兩個不同原 contacts 迫原 triangle；有第二 triangle 的分類與 leaf w 矛盾。唯一 triangle 的 palette P 含 D，每條 tree branch 強迫色不在 P，排 leaf D-forcer。 |
| 原 (2,2) 的六點化約 | 成立 | 保留兩 U，各有兩原 contacts，迫兩互斥原 triangles；双 triangle 分類給六個原內點、直接原 zw、無外掛樹。沒有把收縮圖作染色替換。 |
| 344 域可用於 no-mixed | 成立，繼承分類完備性 | generic 前提只是全 degree-4、T4、disk minimal q-core 及原相鄰 bridge markers；不需要外側存在 mixed C。 |
| singleton markers、零 gap、正奇偶 run | 成立 | roots／leaf／triangle 保持；正未標記 gap 壓為一／兩點，零 gap 保持直接邊，原 zw 不跨未標記 gap。 |
| 同源完整聯合 relation | 成立 | 同時固定全部保留座標後逐 gap 雙向延拓並拼回同一整圖；不把 endpoint marginals 獨立相乘，也不聲稱其他已收縮 contacts 坐標相等。 |
| 整圖 D5／S4 與字面 spoke 接回 | 成立 | 整個來源、roots、附件、列和色框共同搬運；在同一 root-pair tuple 上加兩條原 spoke guards。 |

Gallai／degree-list 全四分類、E6-D／盾弧、單 triangle 附件分類及雙 triangle
分類沿用既有證據。[既有 mixed 指定稽核](../2026-10-07-c44pp-mixed-audit/REPORT.md)
的 generic run／bridge-marker 覆蓋可沿用；其 mixed-specific 省略結論沒有套到 no-mixed。
Triangle palette 的 no-D 模板排除仍依賴 NetworkX planarity replay，沒有逐例
Kuratowski subdivision；本輪未重稽核全部上游拓撲枚舉。這些界線不是新補出的
純紙面或 Lean 證明。

## 3. 全部有限重算與 witnesses

獨立求解器對每個固定 boundary row，把所有 16 個有序 root 色對逐一 pin，
以 MRV／forward checking 在完整字面邊集上找全圖延拓。每份接回图重新解，
再與原核心 relation 的字面 spoke 過濾比較。十列先從所有 proper C5 色字獨立生成；
目標 D5 軌道也重新生成。核對原 unary 的連通分割、ownership、contacts、
actual support、逐點附件與全部 incident edges，並檢查每條原非框邊的 q-critical
刪邊 witness，沒有只信任輸入標記。

| 核心家族 | 核心數 | 完整接回數 |
| --- | ---: | ---: |
| 單 triangle、單 run | 160 | 1,440 |
| 單 triangle、兩 runs | 64 | 576 |
| 偶數 path | 56 | 458 |
| 兩 triangles、直接 bridge | 64 | 1,024 |
| 合計 | 344 | 3,498 |

| 檢查 | 數量／結果 |
| --- | ---: |
| 核心完整列查詢 | 3,440 |
| 接回完整列查詢 | 34,980 |
| 有序 root 色對 pin 查詢 | 614,720 |
| 核心 root pairs／存放的完整 witnesses | 9,096／9,096 |
| 接回 pairs／fresh 全圖 witnesses／原索引全圖 witnesses | 46,254／46,254／46,254 |
| 核心空 fibres／接回空 fibres | 344／12,938 |
| 原 q-critical 刪邊全圖 witnesses | 7,336 |
| Σ 或完整 pair／witness／索引不一致 | 0 |
| 目標完整 Σ 軌道交集 | 空 |

獨立重算 D5(933)={933,934,940,948,996}、D5(941)={941,949,950,998,1004}。
完整域的所有 51 個 Σ 桶均與原 summary 一致。另行核對 64 份雙 triangle
子型的 1,024 接回直方圖：

| 完整 Σ | 數量 |
| --- | ---: |
| 830 | 224 |
| 958 | 96 |
| 1016 | 224 |
| 1020 | 96 |
| 1022 | 384 |

沒有把此子型代替另外 280 核心／2,474 接回的稽核。原证书存放的 pairs／witnesses
全部直接驗證；fresh 結果保存每份同名圖與完整關係的 digest，可用獨立 verifier
重算並與原 immutable 證書逐項比對。

## 4. 實際控制分類

| 控制／前提 | 分類 | 實際覆蓋 |
| --- | --- | --- |
| 全部344／3498必要域完整關係與逐圖延拓 | `triggered and holds` | 全域，沒有反例或差異。 |
| 八份記憶體內證書破壞控制 | `triggered and holds` | pair 少列、witness 內點重色、偽造空 fibre、存活索引少列／偽造、接回圖少列、原邊少列、目標軌道少列均被拒絕；不修改原 bytes。 |
| 兩份顯式 solver 正／負圖 | `triggered and holds` | 完整可行有序關係與強迫同色相鄰 roots 的空關係均吻合。 |
| 標記 grammar 壓縮控制 | `triggered and holds` | run 長度到20，共12,282次；恰覆蓋344份模板，家族160／64／56／64。上游18＋8基底完備性仍沿用。 |
| 同色集 run transfer | `triggered and holds` | 所有大小2–4色集、左右端色、長度0–24，共4,400次。 |
| 將零 gap 誤作正偶 gap 的故意错误控制 | `counterexample` | A={0,1,2}、左右端同色0：零gap不可行、長度2可行。這反駁故意錯誤的替代規則；U1 保留零gap，未受影響。 |
| 整來源 D5×S4 雙-spoke 條件搬運 | `triggered and holds` | 10列×10位置作用×24色置換×16root色對×25spoke位置＝960,000次。 |
| 完整 Σ933／941、disk、Σ-critical 的实际來源正控制 | `not triggered` | 所有放寬接回圖皆無目標Σ；沒有滿足全部來源前提的正控制。 |
| 任意大小化約本身由有限控制建立 | `not triggered` | 有限長度控制不證無界完備性；結論依§2的紙面論證及明列依賴。 |
| 上游完整 topology／NetworkX 排除重稽核 | `not triggered` | 沿用其原有限枚舉及信任邊界。 |

[控制程式](run_controls.py) 的 default／seed17 stdout 逐 byte 相同。
既有 D9 的指定三拒絕來源前提 0/9 AD orbits、0/90 搬運 cases 沿用其原
`not triggered` 界線，不當成本輪 U1 來源正控制。本輪没有重跑 D9。

## 5. 命令、exit、logs、hash 及輸入不變性

完整實際 argv、cwd、環境、exit、耗時及 stdout／stderr SHA256 位於
[commands.json](commands.json)；每份 log 均保存於 [logs](logs)。
下面兩類正式重算均執行 default 與 `PYTHONHASHSEED=17`：

```sh
python3 audits/2026-10-07-m2-u1-audit/restore_input.py
python3 audits/2026-10-07-m2-u1-audit/verify.py --root /tmp/math-m2-ba0b447-audit --output /tmp/math-m2-ba0b447-audit/audits/2026-10-07-m2-u1-audit/independent-default.json
PYTHONHASHSEED=17 python3 audits/2026-10-07-m2-u1-audit/verify.py --root /tmp/math-m2-ba0b447-audit --output /tmp/math-m2-ba0b447-audit/audits/2026-10-07-m2-u1-audit/independent-seed17.json
python3 audits/2026-10-07-m2-u1-audit/run_controls.py
PYTHONHASHSEED=17 python3 audits/2026-10-07-m2-u1-audit/run_controls.py
git diff --exit-code ba0b447f09617591d9f2ba81c988f537af771791 --
git diff --check
python3 audits/2026-10-07-m2-u1-audit/check_bundle.py
```

正式 verifier default exit0／2.613750秒、seed17 exit0／2.607111秒。
正式 run controls default exit0／1.194903秒、seed17 exit0／1.197126秒。
兩份完整結果均為151,024 bytes，SHA256：
`b751c695d650625ba0be2724948b96167255d804e0b535c6f48c7cc087058fa1`。
所有命令實際 exit 見 commands；此數字只記本輪執行，不沿用歷史跑次。
新bundle檢查器首次exit1的開發診斷保留，修正後另存final命令；詳見下面開發紀錄。

| 關鍵輸入 | Bytes | SHA256 |
| --- | ---: | --- |
| 原344域 observations | 56,106,614 | `ded2ff09f1fba01426d801bfda0d975e9c52b5e89554538d9d963f5656db98cc` |
| 新U1 observations | 992,965 | `e2b74cc9516d2131b1ad53e98558d4a0131172a5d98e3fd828814ede9a795097` |
| U1原checker | 7,222 | `f5534863c0fa6779cd00f9cb304d8a3565cbaed239e7f1eb7276b356b0ceadc1` |
| U1原報告 | 8,880 | `ab3dcd2ff66ec3a2508f91d74991d8f04fa7f9446c2addf5430d5e1b5f798dab` |

封存輸入使用候選 MANIFEST／ARCHIVE 的原 gzip blob 還原，先核對壓縮 bytes
的大小／SHA256，再核對解壓大小／SHA256；只針對這一份M2所需大輸入，
沒有重生成任何原產物。最後 [32份輸入 baseline](input-before.json) 與
[32份 final inventory](input-after.json) 完全相同；31份 Git-tracked 來源另與候選
`git show SHA:path` 的完整 bytes 比對一致，大輸入與原封存 bytes 比對一致。
初始22／24／29份 inventory 亦留存，新增紙面依賴由候選Git原bytes補入baseline，
原hash未變；這包含最後彙整的三份唯讀文件，沒有更動任何檢查器的數學輸入。
`git diff --exit-code candidate --` 為空、exit0；候選 tracked bytes 無漂移。
新 audit 的 Python syntax、本地連結、逐檔 whitespace、命令log hashes及兩份結果
一致性另由 check_bundle 核對。最後 [DELIVERY.json](DELIVERY.json) 保存新輸出檔案清單、
大小及 SHA256；不納入 `.pyc`／`__pycache__`。

開發診斷如實保留：第一次新 restore helper 未建立父目錄，FileNotFoundError／exit1；
補 mkdir 後正式exclusive restore成功。run控制第一次scratch斷言把家族標籤誤寫
`even_path`，實際標籤是 `path`；更正新控制後重跑全域成功。這兩項是新稽核碼
的開發問題，不是候選來源／原證書的差異。Finite verifier 首次開發全域執行成功，
正式前僅強化 witness破壞控制以保持boundary／root pins；正式證據是其後凍結版兩次。
新bundle檢查器首次將 `git diff --no-index --check` 無whitespace診斷的正常差異
exit1誤判為錯誤；失敗log保留，更正判定為exit0／1且診斷必須為空後，另跑final檢查。

## 6. Findings、未跑項與停止點

沒有需要修正候選來源、checker或原證書的新finding。941三-spoke更正已在候選內，
本輪確認更正及新增域確實覆蓋，不新增來源實例。歷史 E4／E5／E4C byte FAIL
沒有改寫，也沒有在本輪轉成PASS。所有候選讀入 bytes保持。

未跑 M3 的全archive還原、原U1普通／seed17 producer replay、全部mixed verifier、
D9／C44／C44′重播、LC exporter、Lean／LC build及公理核對；未查PR、遠端CI，
未commit／push／merge。U1完整有限域已由本包自己的程式獨立重算；generic mixed
紙面與上游分類如§2明列沿用，M3仍須完成它自己的重播與工具鏈驗收。

**停止於M2交付。** U2–U4、其他no-mixed core型、單-root例外、(5,4)/(4,5)/(5,5)、
E5要求的新證明、三列推廣、ε≥3、猜想E任意大小、一般出口及K∞=K≤5均保留。
本輪結論是限定前提下U1排除的獨立紙面＋有限證書稽核，供後續M4整合。
