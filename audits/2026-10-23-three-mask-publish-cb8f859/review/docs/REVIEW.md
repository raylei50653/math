# Publication 文件唯讀審核

2026-10-23；入場 HEAD `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

**PASS：最終五份既有 dirty docs、發布 history 與五輪直接來源的語義一致；沒有尚需修正的數學 scope。** 本審核只寫本 `review/docs/`，未改共享文件、738份歷史 audit、Git index，未 commit／push。精確受審 bytes／SHA、40份來源對照及 fresh checks 見 [receipt.json](receipt.json)。

## 1. 已修正並重讀的三項

1. **D1：932 的 h=4 範圍。** 初讀 STATUS／guide 頁首及 peeling 的 h≥4 列時，s≥1／d≥2／Q≥10 未全部字面限定 h=4。root 已明示原 h=4 C9-932；重讀位置為 `docs/STATUS.md:3,10`、`docs/c5_kempe_guide.md:5,11,13,114`、`docs/c5_c8_peeling.md:245`。原 h≥5 與一般932仍 OPEN。
2. **D2：STATUS 的責任。** root 已把第一／二／五輪長敘述收成第五輪短結果與前四輪直接 links（STATUS:9–11），逐輪與發布核對移至 history，並在 STATUS:853 與 guide:28 連入。符合 [DOCUMENTATION](../../../../docs/DOCUMENTATION.md):25–47,84–107 的 Routing／History 分工。
3. **D3：933 的最小性前提。** guide:113 已明示「原全域最小r6／933兩星來源下」。H* 支持限271／314／319的分類及後續正族依賴此原前提，不是必要零座標單獨給出的可行性／來源結果。

## 2. 五份文件與 source 邊界

| 受審文件 | 結論與關鍵邊界 | 直接證據位置 |
| --- | --- | --- |
| [STATUS](../../../../docs/STATUS.md):3–11 | h=4的932 single／deep、933新換框圖與兩OR、941兩patch只作短索引；一般三支、實際較小bad、新Lean及共同k≥23均未升級。 | [第五輪總報告](../../../2026-10-23-three-mask-round5-cb8f859/REPORT.md):10–14。 |
| [C8 peeling](../../../../docs/c5_c8_peeling.md):245 | h≥4列內只把本次C9結論施於原h=4；h≥5另列OPEN。Q仍可有弦，未沿用h=3的19內點界。 | [932第五輪紙證](../../../2026-10-23-three-mask-round5-cb8f859/932/paper/PROOF.md):3–9,20–29,57–80。 |
| [Kempe guide](../../../../docs/c5_kempe_guide.md):48,65,113–115,128–131,179–184 | H*新外框、原最小性、非crossed長路與V crossed保留；固定Q1／Q2／fan-B方法關閉。941不把六原點算六私有點，R/r可同可異。 | [933第五輪紙證](../../../2026-10-23-three-mask-round5-cb8f859/933/PROOF.md):3–21,43–70,100–154,173–211；[941第五輪報告](../../../2026-10-23-three-mask-round5-cb8f859/941/REPORT.md):5–27,46–49。 |
| [no4ct handoff](../../../../docs/tasks/c5_no4ct_handoff.md):164,204–215 | 明列h=4，保proper Q的空band，未把Q當induced；raw C6／C7 counts僅rank≤2／3，只有群和folded rank-one。一般三支／K∞／Lean仍OPEN。 | [932第四輪紙證](../../../2026-10-23-three-mask-round4-cb8f859/932/paper/PROOF.md):18–39,71–112；[932第五輪紙證](../../../2026-10-23-three-mask-round5-cb8f859/932/paper/PROOF.md):82–112。 |
| [common language](../../../../docs/c5_common_language.md):111–174,210–231 | 原有85行新增與本批同一外側、單向回填的接口直接相關，納入合理；它摘錄一般原理，未新增來源排除或新Lean theorem。 | [A原定理](../../../2026-10-18-abstraction-bottleneck-9f1fe84/A/ANALYSIS.md):74–180；[W5逐fibre公式](../../../../docs/c5_w5_marked_relation.md):102–125；[Kempe surgery](../../../../docs/c5_kempe_connectivity.md):15–43,81–104。 |

共通語言§3.1的全稱負列回填方向正確：同一候選H各拒絕列的每份完整著色都可回原G，即迫該列空。密封版本比較同一實際外側的完整接點關係，接受只保一份共同tuple，拒絕用 `A_q∩R_Q⊆A_q∩R_P`；私有點、接點及字面色框均未丟掉。四列「最少」只限定逐列布林觀察，並非所有不變量的下界。完整關係相等不是必要條件，合法嵌入與完成大小仍另證。

§3.2的封閉換色適用多個完整分量聯集；Lean的 `KempeSet`／`swapOn_proper` 名稱可在 `Math/KempeSurgery.lean:146,177` 查得。五度補回指示式在完整五鄰點形成proper C5時，由(2,2,1)／(2,1,1,1)兩種色重數給1／0；此著色恆等式本身不需平面性／最小性，商圖幾何仍另證。H*改用新外框，因此沒有把這一「同有序外框」四列替換定理直接當作H*的bad證書。

## 3. 五輪直接關聯核對

| 輪次 | source中實際成立、被本批文件使用的範圍 | 保留義務 |
| --- | --- | --- |
| [第一輪](../../../2026-10-23-three-mask-methods-cb8f859/REPORT.md):11–13,25–41 | 933 fan-B全部支持證書排除；Q1／Q2各留兩條未排證書；932原三接點幾何、941完整分量禁邊。 | 當輪未排證書非可行；沒有一般三支／較小bad。 |
| [第二輪](../../../2026-10-23-three-mask-round2-cb8f859/REPORT.md):11–13,28–37 | 932原h=4三接點180假設全排；933兩商圖四條殘餘全排，合fan-B三圖完整支持皆K132；941原分量樹與真出口。 | 關閉的是三張固定圖的支持方法，並非一般933。 |
| [第三輪](../../../2026-10-23-three-mask-round3-cb8f859/REPORT.md):12–14,26–42 | 932同一pair至多兩中心；933兩個合法k−2新填片，共同四查詢義務U=V=0，原全域最小性迫U+V>0；941可指定最後橋點。 | 另12填片只排指定四查詢合同，未說其full support皆K132；未證U=V=0。 |
| [第四輪](../../../2026-10-23-three-mask-round4-cb8f859/REPORT.md):12–14,36–65 | 932距四全排成零pair；933在同一原D保全部帽lifts，由24相關項排18、留六完整fibre及條件雙射；941原B側／wrong-side二分。 | 六fibre未全空；必要存活不代表共同可行／來源，941兩支均未排。 |
| [第五輪](../../../2026-10-23-three-mask-round5-cb8f859/REPORT.md):10–14,36–76 | 932 s=0排除、h=4下s≥1／d≥2；933合法H*及兩個16-OR正族；941兩個真橫穿與共同原面至少六原點。 | 一般三支、bad、K∞與新Lean均未完成。 |

H*在同一D上先合a=c，選outer `(A,s,v,w,t)`，再於真空面合A=R；原aR／Rc／ac非邊、平行副本及指定outer copy處理均由933紙證:23–70承擔。兩次merge後總點k−3、外框五點，故內點k−8。`{m∈K132:m⊆319}={271,314,319}` 使用全域最小性；前兩正族沒有rxy帽lift，仍可且必須是正D fibres。三split的36-target測試只增加四個零字，兩組各16項OR為必要正義務，未聲稱可行。

933的原induced C7只在非crossed attached C的同一完整E著色及指定r–a/c最短02路恰五邊時成立；原s,t≥6、完整r/x/y stars、原rotation、small-cap來源前提均保留。該E著色未必能補bph回G。V crossed及free-C、A支均未被長路引理排除。

941的第五輪只承接ordinary short Type-I、初始02型13／36；wrong-side是同一指定T的原02分量不在J_B。至少兩次真橫穿不把相切計入，每份是同一原邊兩實際三角面的四色patch。任兩不同中心合至少六原點；只有各k2必私有，U、V/Y、q例外保留。`R=r`或`R≠r`均未證；第五輪紙證:29–32已明確澄清第四輪末句，舊audit原文保留。

## 4. History／Routing與執行界線

[新history](../../../../docs/history/2026-10-23-three-mask-five-rounds-publish.md):10–19逐線保留來源前提、H*新色框、E與G回填方向及六原點邊界；:23–27直接連到五輪；:29–39把738檔凍結、執行回執、Lean與push／CI各自分開。未把規劃中的發布檢查寫成已PASS。README用途／閱讀路徑及HANDOFF研究線／tag無變動，依DOCUMENTATION:25–26,93,103，兩份reviewed-unchanged合理；無需為本批增加研究線或改活躍排程。

本review fresh執行：

- `python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/A/check_signed_interface.py`：PASS，132 masks、528個≤3-query countermodels、64 raw四查詢masks且0 catalogue matches。
- `git diff --check`：PASS。
- 對publication BASE逐檔重算738份、69,861,223 bytes的SHA：drift0；HEAD保持cb8f859，Git index SHA保持 `79571a80110f4f8b24484a9152287786337081180bf4c9bbba036825c51306da`。

沒有在本review重跑五輪數學checkers、lake build、94項工具測試、全樹docs／DocGraph、artifact policy或任何Git寫入；這些由root的publication報告及實際回執承擔。history:36所連publication REPORT尚待root在真實重播後產生；本PASS不代表該待建目標或尚未執行的檢查已完成。其既定目標不是數學scope阻塞，但最終連結檢查須在REPORT落地後執行。
