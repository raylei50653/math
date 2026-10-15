# 第三輪：兩環同步交換消除方向隔離

2026-10-15；BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
唯一寫入本 audit，前輪與 shared docs 皆唯讀；未 commit／push。

**已證：加入「各含一條指定邊的兩個不交交替環同步翻轉」後，普通
XOR 分離 PM 的交換圖必連通。** 對稱差中 e,f 同環／異環的分類直接
給構造證明，不假設任何偶補終點已存在。

**新有限退出：第二輪46點控制的37個單環鄰居都停住，但38個新增
雙環鄰居中恰有2個直接偶補。** 起點0直接到PM索引397或434，補環
長度從 `(26,7,8,5)` 變成 `(34,4,8)`。任一單翻中間狀態都違反 XOR，
因此必須把兩環作一份同步交換。兩環接觸同一舊補環，證書保存聯合
路徑手術，沒有把兩個獨立數字誤作可相加的下降證明。

[PROOF.md](PROOF.md) 另證完整批次奇偶公式、接觸舊補環不交時的
伴環下降條件，以及每舊補環只切一次的批次下降公式。
已有偶補的完整 Tait 色交換亦可只用含 e/f 的一或兩個雙色環，
形成兩方向完整染色集合的局部 involution；加權量相等仍不證其正值。

| 固定控制／標記 | 全部 PM | XOR PM／偶補 | 起點單環鄰居／偶補 | 起點新增雙環鄰居／偶補 |
| --- | ---: | ---: | ---: | ---: |
| 36點原標記 e16,f26 | 365 | 109／44 | 26／11 | 6／5 |
| 同36點強具名標記 e0,f10 | 365 | 194／83 | 54／26 | 7／6 |
| 46點 e0,f8 | 960 | 322／39 | 37／0 | 38／2 |
| Petersen10點 e0,f1 | 6 | 4／0 | 3／0 | 0／0 |

第二份36點標記有原角色 `(z,x,y,b)=(1,0,2,6)`，保持 zxy 原面、zb
原邊、bx/by 原非邊及 d(z)=8；完整≤3割只有單點3割、對偶原圖最小度
至少5。其完整原最小來源、附件與空 fibres 未建立，不能視為來源實現。
Petersen 控制則使已連通交換圖與兩方向零權重同時存在，明確阻止由
交換連通偷渡偶補存在性；checker 也直接以 girth／Euler 排除其平面性。
四份標記均 source `not triggered`。

正式 [certificate.json](certificate.json) 包含：三張固定原圖上的四份
具名標記、全部PM與完整補環、全部完整Tait fibres（含空列）、平面控制
的 face/rotation/對偶邊對應、全部基本交換與起點所有手術、全部完整
色 involution。共核28,024條基本交換與76,294對PM的構造連通路徑；
沒有擴大來源枚舉界。同一36點圖的PM在兩份標記中重複列出。

```sh
python3 -B audits/2026-10-15-xor-batch-descent-6ddea32/check.py --check audits/2026-10-15-xor-batch-descent-6ddea32/certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-xor-batch-descent-6ddea32/check.py --check audits/2026-10-15-xor-batch-descent-6ddea32/certificate.json
```

[INPUTS.json](INPUTS.json) 固定 BASE、前輪權威與具名圖 hashes。
[VERIFICATION.json](VERIFICATION.json) 記錄正常／seed17、漏一條真正
雙環交換與錯聯合奇偶的損壞證書拒絕，以及 exclusive-create 拒覆寫。
重播只需 Python 標準庫，正式 checker 不讀探測結果或外部圖庫。

本輪沒有來源大小下降：所有交換在同一 Q 上，完成成本與頂點差都為零。
原來源是否必供應奇環下降批次或有限平台出口，仍是精確剩餘義務。
ω=0、完整319來源排除及一般 `K∞=K≤5` 仍 OPEN；沒有新 Lean theorem、
來源實現或點數界。
