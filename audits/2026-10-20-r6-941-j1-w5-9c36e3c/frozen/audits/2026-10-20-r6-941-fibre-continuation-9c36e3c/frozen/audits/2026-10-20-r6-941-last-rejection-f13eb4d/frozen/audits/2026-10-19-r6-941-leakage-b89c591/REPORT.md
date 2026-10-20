# 完整 r6／941：強制雙接受扇區、fan-B 洩漏與共同十圈接口

2026-10-19。起始 HEAD 與本輪 BASE 均為
`b89c5913cea9df2305845be0f65fa6f1c1aaf55f`，起始工作樹乾淨，
沒有後續提交需合併。238 份輸入 SHA 見 [INPUTS.json](INPUTS.json)，
其他原來源的 BASE SHA 見 [B/additional-inputs.json](B/additional-inputs.json)。
本輪輸出限本獨立 audit，另更新直接 [Kempe 導覽](../../docs/c5_kempe_guide.md)
及 [STATUS](../../docs/STATUS.md)；所有舊 audit 證據 bytes 保留。

**新增已證：941 具名原位置的 G_B 必接受 01232，也必洩漏 01212；
其指定四列合同不可行。尚未得到嚴格較小 bad 或原來源矛盾。**
本輪沒有證明整個三候選族失效，也沒有證明 `Sigma(G_B)∈K132`。

## 1. 證據及適用範圍

| 結果 | 層級與限制 | 入口 |
| --- | --- | --- |
| 原 alpha 的 h=a、h=b 扇區都非空；G_B 必接受，Q1/Q2 至少一張接受 | 已證，任意大小具名原來源；兩個存在 witness 分開量化 | [原強制 fibres 與全部回填](B/FORCED_SECTORS.md) |
| `A_a=T+2U`、`V=T+U`，其中 T/U/V 是同一 G_B 的三個洩漏數 | 已證，任意大小實際 E 的平面展開＋精確有限線性代數 | [主證明](PROOF.md)、[C 證書](C/gb941-identities.json) |
| G_B 必洩漏 01212，並至少洩漏 01021／01202 之一 | 已證；只排除此候選的指定四列合同 | [主證明 §1](PROOF.md#1-定理與精確範圍) |
| 同一實際 C10 disk，完整兩側 cap fibres 逐份直積，保留空者 | 已證幾何與完整 fibre 雙射；2,461 色軌道的局部代數有限驗證 | [C10 引理](B/CORE.md)、[全 lifts 證書](B/core-certificate.json) |
| `2(N01212(U)+N01213(U)+N01232(U))≤N01202(G)+N01212(G)` | 已證，完整著色二重單射；解釋 U 三禁列在精確雙 cap 模型中的冗餘 | [C 證明](C/PROOF.md) |
| 先前三份指定候選的控制均缺一個真實強制正扇區 | 已證該三份不能代表此來源；不是原來源排除 | [C 完整投影](C/old-controls-projected.json) |
| 強化後共同模型仍容許 Q2 合同，也容許三張全部在 K132 | 有限精確控制，非實際圖、非來源反例、非縮減 | [A 證明](A/PROOF.md)、[來源正值控制](A/source-positive-certificate.json) |

來源是全域最小內點、再最大邊數的 no4ct C5 disk，原完整支持恰 941。
保留原框 `(x,y,a,b,c)`、同一 E、全部附件與旋轉、原 x,y,b 四度、r 六度、
s,t 至少六度、p,h 五度、原三角面與 C4/C5 限制。完整逐項來源、字面
別名及必要非邊見 [來源契約](B/SOURCE_CONTRACT.md)。只涵蓋原
`(p,h)=(p,ell)`；普遍位置存在仍是另一個問題。

## 2. 與前輪的實質差異

前輪已證 932 三候選完整支持皆在 K132，932／933 接受者必洩漏 01212；
其封存證據及停止點不改。本輪追溯原 low-p 的兩份**已證非空完整 fibre**，
把它們實際回填到原 G，得到以前 941 控制未保留的 `A_a>0,A_b>0`。
從同一外側的完整計數再證兩條恆等式，因而關閉 941 的 G_B 指定合同。

僅有舊 C8 條件時，三份分別指定候選的控制有原扇區數
`(A_a,A_b)=(4,0),(4,0),(0,4)`；它們各漏一項已證來源正值。
但不能只刪掉這三份控制便宣稱閉合。[新共同控制](A/source-positive-certificate.json)
保留同一 C10 向量、全部 count/spans、完整 U=319 與兩份真實指定 fibre
的正值，仍有 Q2 指定合同及三圖全 1023 的兩種情況。故新定理不能推升
為三圖全在 K132，也不能推出總有較小 bad。

所有支持由同一向量的十列完整計數直接計算；本輪未使用三探測後的圖
作縮減候選，沒有 P 改框或逆 P 存在性假設。既有 P/R 任意 disk 語義與
RR／PRR／RRR 解碼保持原地位，沒有推出一般文法代表。

## 3. 完整證據與唯讀重播

```bash
python3 -B audits/2026-10-19-r6-941-leakage-b89c591/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-19-r6-941-leakage-b89c591/check.py
```

checker 核對 BASE 輸入 SHA、來源追加輸入、兩側完整 cap lifts、所有
原圖／三候選十列投影、Q2 的 a=q 分支、共同 C10 控制與計數恆等式。
破損證書及論證風險負控制包含漏邊、跨著色直積、跨候選拼拒絕、漏掉
強制正扇區、漏一個完整 lift 及錯誤倍數。具體正常／seed17 重播與檢查
範圍見 [checks.json](checks.json)，主證明與實作交叉審查見 [REVIEW.md](REVIEW.md)。

發現用 LP、二進位中間檔及探索輸出與正式證書分開；正式 checker 只用
Python 標準函式庫和精確整數／有理數，不用浮點容差。必要條件向量從未
被標成實際 D10 或原 G。

## 4. 工程及文件傳播

實際檢查、既有警告／例外與產物政策結果見 [checks.json](checks.json)。
正常／seed17 唯讀輸出逐 byte 一致；文件、正式 docs DocGraph、94 項工具
測試、產物政策及差異空白檢查通過。全工作樹 DocGraph 仍失敗，72 個
既有錯誤與 BASE 的完整 error multiset 一致，沒有新增；沒有刪封存檔遮蔽。
產物政策用包含本輪成果的暫存 index 核對，真實 index 未改。Lean build
通過，保留 AttachmentOrder／SymRelabel 原有 linter 警告。
本輪沒有新增 Lean theorem；`lake build` 只驗證既有 Lean 工程。
README／HANDOFF 的入口、研究線及活躍標記未改，依現行文件治理核對後保留。
主來源及本輪證據先完成，再更新 guide 的直接停止點與 STATUS 索引；
沒有覆寫舊報告的封存正文。未 commit／push。

## 5. 明確量化的下一缺口

令 C 為 [完整來源契約](B/SOURCE_CONTRACT.md)所定的具名來源類。
本輪之後，指定四列路線的未解命題精確為

\[
\forall G\in C\ \exists i\in\{1,2\}:\quad
F_{01232}(Q_i)\ne\varnothing\quad\land\quad
\bigwedge_{w\in\{01021,01202,01212\}}F_w(Q_i)=\varnothing.
\]

這與原三候選的指定四列命題等價，因為 G_B 已證不可能滿足該合同。
另一條仍有效但不同的目標是同一來源某張合法完成候選的**完整支持**在
K132 外；本輪沒有排除 G_B 由其他列提供這種證書。

若以共同向量繼續，尚缺的是一項能對所有實際 D10 證明、且排除新
三圖全 1023 控制的來源條件。現有模型沒有實現同一張原圖的全部
原度數／C4、C5 結構、全域最小性比較、以及不同色對交換在同一完整著色
上的共同分量資料。不能把這些條件的分別可行性當成來源實現。

Q1/Q2 三負 fibres、完整支持替代證書、嚴格較小 bad、普遍位置存在、
完整319、W110+W101>0、omega_e=0 及一般 K∞ 結論，依原證據維持 OPEN；
一般 K≤22、固定 r6 的 k≥25 不變。目前接續入口由 [Kempe 導覽](../../docs/c5_kempe_guide.md)
維護。
