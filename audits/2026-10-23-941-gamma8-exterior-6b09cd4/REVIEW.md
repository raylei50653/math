# Γ8 外側、B14 與完整分量交換：獨立審查及傳播

2026-10-23；限[PROOF](PROOF.md)明列合同，未commit／push。

三條獨立工作在同一凍結前提下交叉核對：[外側幾何](workers/geometry/PROOF.md)、
[B14端點](workers/b14/FINDINGS.md)、[完整交換](workers/stars/FINDINGS.md)。
幾何紙證由B14及stars覆核，端點／分離義務由geometry及stars覆核；最後
[主證與checker審查](workers/stars/FINAL_REVIEW.md)未見實質缺陷。

採納並明列的量詞修正：

- Γ 的 E 可rootless；只有碰框時才是 D，不能預填 c 的接點給 E。
- 完整 M2∩E 分離集的非空性另需 E 碰框；h=c 則自動 E=D。
- 交換保持同一boundary-indexed fibre／cap relation並給新完整witness，
  不宣稱固定M頂點集對每份其他著色都能作分量交換。
- O 五外點證明在 d=U 時用的是**u私有的完整原星**，沒有把 U 的 F link
  當完整cyclic link。其餘框外附件保留。

獨立producer圖遍歷與checker union-find在具名1,056端點列恰同保464、排592；
四份合同是兩target×02型13／36，每份均保初始03型4／9的兩選gate。
stars另獨立重建11×8份同圖限制，全部528份二色局部分量與正式證書相同。
兩個字面Γ框的完整二點fibres及全套前輪證書不改。

正常／seed17／`-O`結果相同；14項語義及2項外部反控制全拒絕，65份authority
與219份前輪輸出零漂移，見[VERIFICATION](VERIFICATION.json)。任意j交換、
四／五外點與分離義務屬紙證；端點域及局部作用屬有限校準，完整來源仍
`not triggered`。未新增來源、整型排除、原八配對排除、Lean、LP或較小bad。

保留早期`certificate.json`的四點版本；O五點完成後另發`certificate-v2.json`，
正式checker預設v2。`exploration/joins-v1-rejected-double-U-toggle.json` 是
早期端點識別程式重複翻U的錯誤試算，已排除於正式證據；修正後正式checker
另從凍結後繼字面框賦色，並檢查識別前後色一致。舊試算未作來源／排除宣稱。

Propagation：

- Updated：[Kempe導覽](../../docs/c5_kempe_guide.md)頁首、近期里程碑、Γ8停止點；
  [STATUS](../../docs/STATUS.md)短索引。原因是外側必要義務已實質收緊。
- Reviewed-unchanged：前輪報告／紙證／完整證書與所有輸出逐字保留；原內側
  分類、外耳2／4／6、父wrong-side及ζ五度兩側未被取代。[HANDOFF](../../docs/HANDOFF.md)、
  共通語言、932／933、W7的38／40、J1／J2與共同k≥23不變。
- Remaining OPEN：11型在同一外側disk的完整stars／M2分離集／B14接合、
  更多內點、較長Γ、B側、一般wrong-side、完整來源與較小bad。
- Propagation stop：L1 topic guide／index。必要義務收緊未收尾父來源命題，
  不升級跨線摘要，不展開原圖枚舉。

正式文件與scoped正式DocGraph見[DOC_CHECKS](DOC_CHECKS.json)。全樹DocGraph
未重跑，沒有全樹PASS宣稱。新audit本地連結另見[AUDIT_LINKS](AUDIT_LINKS.json)。
