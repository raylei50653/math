# 2026-10-03：四-spoke binary 同列端點 hub 整型排除

接手使用者指定原 012／2、S_C=04、S_U=234；基準
`b63a0965434d68a28292994638b2c98e848585b8`，工作目錄
`/home/ray/developer/ai/math`。保留原 singles／binary／star 未提交
成果；本輪未要求也未執行 commit／push。

## 結果、原圖與證據

[新報告](../c5_excess_two_mixed_core_four_spoke_hubs.md)／
[checker](../../scripts/c5_excess_two_four_spoke_binary_hubs.py)先關閉
指定入口：q=01021 下原完整 U 禁1，與原框點4同色。原拒絕
degree lists tight，故原 contacts u、v 不接框點4。將
{原b、原a、框點0、1、4} 合成外部 connected bag，另保留框點2、3，
原 U 的完整 degree四不降，lists 精確不變，三個 hubs 互鄰。
既有三hub Gallai引理給原 G 的 K₅ minor。

同一端點hub配方覆蓋原star全部96份殘留：933的32份與941的64份
各半為二hub／三hub，全部作來源排除，剩0／0，含root交換。
完成四-spoke (3,1)、mixed-(1,1) 加一原binary unary子型，
沒有新增跨列palette定理或ε≥3結論。其他原incidence型保留。

紙面證明沿用外部 degree-list／Gallai 定理、連通外部K₄排除及
短支援報告二／三hub引理；本輪重讀Dvořák講義Lemma7／Theorem10。
任意大小minor由末端odd-cycle／bridge的connected branch sets
承擔，沒有從短圖或schema數字外推。Hub只用於topology，不把
完整原U換成factor或拆開contacts，不改寫原C／U／joint／fibres。

192原query證書、10,752完整有序U schemas、2,208局部tightness
控制，保留每份frame、domain、assignment、candidate、完整K/C
反像、原support及共同lifts。96root交換、1,920整體D₅hub前提
核對。這些是原域適用任意大小紙面引理的證書，沒有捏造未知原U
的96份圖witnesses。另存42張完整degree圖（含root交換、C長度
0／2／4、U path／odd cycle／旁支）及逐tuple整份coloring、
空原joint、五connected bags／十對原鄰接、合併保degree核對；
固定圖不聲稱disk、候選Σ或Σ-criticality。

## 本輪實際驗證

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check
python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check
PYTHONHASHSEED=17 PYTHONPATH=/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f python3 scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

原binary使用前輪唯讀networkx3.5 cache，重播720全圖joints、
11,520 pinned fibres、144同色省略等式及舊two_two全部數學
payload／support table。原單一docs hash漂移仍保存；舊產物及
下游歷史證書不覆寫，未宣稱舊byte-check通過。新checker保留
inherited audit，其重新計算由本輪原binary重播承擔。

`lake build` 通過8,831jobs，只有既有AttachmentOrder／SymRelabel
linter warnings，未形式化本輪topology。沒有重跑歷史來源圖
catalogue、singles、其他雙root／唯一degree6分支、R-series、
weak-deletion或Lean axiom audit；既有三接點 (3,1) checker亦未重播，
它只是下個窄題的依賴入口，本輪不聲稱完成該銜接。

新checker以預設seed及PYTHONHASHSEED=17逐byte核對通過；原star、
binary及短支援checker重播通過。文件檢查通過493份Markdown／
5,053個本地連結；DocGraph通過62 documents／213 relations／
5 families，零errors／notes。產物status為`ok=129`，無missing／
changed／stale；`git diff --check`通過。
HANDOFF研究線／tag未變，維持薄索引；README、Kempe導覽、STATUS、
全線整合及相關前序報告已接上本輪後續，不改歷史正文的舊數字。
新observations按大型產物政策留本地，MANIFEST保存digest及producer。

新observations為 **7,345,191 bytes**，SHA256
`b4e2c4371a9fb8e635de5ffcd347abc2a2798116412ae2a97331e77b974e9cea`。

## 停止點與貼用摘要

```text
cwd=/home/ray/developer/ai/math；先讀docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md及docs/c5_excess_two_mixed_core_four_spoke_hubs.md。
保留b63a096上的原工作樹，本輪未commit/push。
原012/2、S_C04、S_U234入口已作同列tightness／三hub Gallai K5排除。
q01021的原U禁1；contacts不能接同色框點4，外部b+a+框014合併保degree。
原star剩933/941的32/64份域全由二/三hub排除，剩0/0，含root交換。
完成四-spoke(3,1)、mixed-(1,1)+一原binary unary子型，未新增Lean theorem。
192原queries、10752完整U schemas、2208 tightness、96 root交換、1920 D5核對；
42完整degree圖保存actual attachments、整份C/U tuples及原K5 branch sets。
重播：PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check。
前序star/binary/短支援亦重播；原binary720 joints/11520 fibres、舊payload/table一致。
單一舊docs hash漂移仍保留；原star/binary證書不覆寫，原32/64/116/256屬歷史層。
下一窄型mixed-(1,2)+一單接點unary，可先固定原a012/b2、q01021、省略a0或a2；
核對原K=C+a三接點(a,y0,y1)與(3,1) minimal q-core、既有active-triangle K5前提。
該身份銜接本輪尚未證；mixed-(1,3)、其他四/較少spokes、(5,5)、多mixed等保留。
共同ε>=2不變，跨列palette定理、ε>=3、一般出口及K∞=K≤5未證。
```
