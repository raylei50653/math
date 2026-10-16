# R6-SEVEN-DISK-RIGIDITY 研究報告

2026-10-16；BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`。
**普通 101 匹配存在性已證。全部剩餘七割障礙任意大小排除。**
本輪的窄問題閉合；偶補正值及完整319仍 OPEN。

## 主定理

在原全域最小、次級最大邊數的 no4ct C5 來源、原四度 x,y,b、六度 r、
同一合法 J、實際 D、原具名 e,f,g 與全部完整 fibres 的契約下，

**`P101={M∈PM(D):e,g∈M，f∉M}≠∅`。**

證明不只提高內點下界。對假設存在的任意七割 disk，
令 Δ_i 為其嚴格內點的完整度數 excess，h 為普通外耳數，得到

`8+I−Δ_i = Σ_Q t_u ≤ I+2−Δ_i+2h`。

因此 h≥3。七邊界至多容納三個互不相鄰的耳中心，故恰有三個。
填入其實際外側三角面後得到 induced C4；無 forced 耳、只有 e 耳、
只有 g 耳及兩者都有，全部被原 m/z 扇區與具名面位置排除。
接上既有窮盡 Tutte 分類、singleton、五割及雙 W5 排除，普通 101 非空。

關鍵是任意 excess 的完整計算與抵消。沒有假定 I=5、曲率取等號、
內部大小有界，亦未以有限控制外推一般來源。

[完整證明](PROOF.md) · [幾何完整推導](GEOMETRY.md) · [獨立審查](REVIEW.md)

## 匹配介面的附帶結果

假設七割障礙時，其實際外部具有精確 A/B 二分結構：
同一 P111 每個外部 complement path 和 cycle 皆偶長，含重複外端點的零長 path。
even111 接合前至多 140 個 eligible 內簽名；普通 420 簽名及全部空 fibres 仍保留。
同一外部的全部 128 個 101 外 fibres 皆因 singleton 缺額為空，
說明僅替換內部的方向不足；真正來源排除由上述幾何完成。
詳見 [MATCHING](MATCHING.md)。這些條件式介面引理不聲稱產生被主定理排除的來源。

## 證據與剩餘義務

| 層級 | 結果與界線 |
| --- | --- |
| 普通 101 任意大小存在性 | 紙面證明；兩份最終獨立審查 PASS |
| 有限幾何與匹配控制 | 正常／seed17、完整 lifts 與空 fibres、負控制通過 |
| 任意 excess 公式 | 精確 affine 係數核對與局部算術校準；一般證明仍由紙面負責 |
| 真正最小來源數值測試 | 0，not triggered |
| Lean | 既有 build 通過；未新增本輪 theorem |
| 封存與版本管理 | 626 個原輸入無漂移；新 audit 封存，未 commit、未 push |

普通 P101 非空保證聯合普通族 `P110∪P101` 非空，
**尚未證明其中有偶補 matching**。
下一個窄義務是同一 D、同一完整匹配族的 `omega_e=0`，等價的加權聯合正值
`W110+W101>0` 仍 OPEN；101 單族偶補正值、完整319及一般無界主命題也未證。
`K≤22=K≤5`、固定 r6 的 `k≥25`、completed-source 接回成本 `k+5` 均不變。

## 驗證、歷史推導與文件邊界

[VERIFICATION](VERIFICATION.md) 分列紙面、有限校準、Lean、文件與封存身份。
scoped DocGraph 通過；全樹仍有 BASE 相同的 70 個歷史重複 ID。
未刪除歷史證據或更改前輪 audit。

[RIGIDITY](RIGIDITY.md) 與 [等號延伸](matching_EQUALITY.md) 保留早期有效中間結果；
其當時的 OPEN 說法不取代本輪最終 [PROOF](PROOF.md)。
已核對 HANDOFF、Kempe guide、STATUS 與直接 C4 父題；
本輪為獨立 audit，未修改共用 routing 或把普通匹配採納成偶補／父題 closure。
無新外部定理、來源替換或 completed-source 下降。
