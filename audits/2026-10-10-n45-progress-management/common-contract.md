# HIGH3 並行稽核共同契約

日期：2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
使用者授權監督／發布可並行任務；HIGH2 由使用者稍後交付，不讀取其在製作中內容。
本批只核 HIGH3 的既有 BASE 映射，所有結果先為候選，監督尚未採納。

## 凍結與輸出邊界

先讀本目錄 inputs.json，逐項核 current live pin／BASE blob／frozen 副本 SHA256。
任一不符即只在自己的專屬目錄交 finding 並 STOP，不自行刷新 pins。
自己的任務指定目錄以 exclusive create 建立；若已存在就 STOP，不覆寫或重用。
其他 worker 的目錄、舊 audits、所有 shared 文件與 HIGH2 目錄只讀且不得修改。
只 hash 本批 named inputs／自己的 immutable payload；不要把同時工作的 sibling 或 HIGH2
新增檔案當 input drift。不得 commit/push/PR、外部訊息或再委派。

## 全部 HIGH3 原來源契約

K1. G 是任意大小有限簡單 disk 圖；B=(b0,...,b4) 為有序 induced C5 外面。
K2. 完整有序 Σ(G)=933/941，或一次共同整圖 D5 像；每條非框邊 Σ-critical；ε(G)=2。
K3. 有效 H 忽略原孤立內點，連通、full B-touch；忽略點的四色 free factors 保留於全部 lifts。
K4. 恰兩原非相鄰 degree5 roots r,s；其他有效原內點完整 degree4。
K5. H−{r,s} 的完整原分量恰唯一 unary U 及 mixed P,Q；三份 connected、one-sided，actual support 非空。
K6. P/Q 各 actual support 恰真原框邊兩端；兩 root incidence 皆正，actual attachments／ownership 完整保留。
K7. 原 U 只接 s，contacts 恰 sx1,sx2,sx3，三點相異，無 U–r；U 整份保留。
K8. mixed incidence (m_r,m_s)=(3,2)：s 對 P/Q 各一，r 分配 1 和 2；原 identity／shared 頂點不合併。
K9. 原 r 恰兩 spokes rb_i,rb_j，i≠j；s 無 spoke。只省略 e=rb_i，X 保 rb_j。
K10. 固定原拒絕 literal β；X=G−e=M 自己是 β inclusion-minimal 45/54 core；root swap 只共同命名降度 r。
K11. 除 e 外全部原頂點、內邊、contacts、框附件與 spokes 完整保留；不縮 piece、刪 U 部分或新增邊。
K12. 原 named/ordered/shared contacts 單坐標、supports/ownership、bridges/rotation、共同 literal 四色框、
     十列完整 relations、全部 pins、ambient 空／非空 fibres 與 full lifts 保留。
K13. D5/S4/root swap 共同作用整圖與全部資料，保 933 q2；不假定 β 是 U 盾中點。
      原 G、X、刪 contact 圖各自的 vertices/edges/lifts 分明；minor 只反證平面性。

## 待核候選路徑（每一步均待獨立核）

由 K9/K10/K11，X 中 r 完整 degree4、s 完整 degree5、其他點完整 degree4。
H_X−s 恰 C={r}∪P∪Q 与 U，C/U 對 s 的原接點數為 (2,3)，N_B^X(s)=∅。
若 β 可共同整圖搬到 BASE q，X 自己滿足 BASE no-spoke exterior 的全部 core 前提，
BASE 已排除 (3,2)，可能直接得到限定 HIGH3 任意大小 paper 排除。
不得從 G 的 criticality 遺傳 X minimality；不得把指定 X 延拓當恢復 G 的 coloring。

## 回傳格式與驗證

交 REPORT.md、independent-judgment.json、frozen inputs／hash index、必要 proof witness／短 verifier。
JSON 必列每 claim 的完整量詞、K1–K13使用項、BASE精確章節、external trust、
verdict (holds under stated hypotheses / gap / counterexample)、新增充分前提及精確殘留。
至少四 claim：CORE / COMPONENT / task-specific / HIGH3 scoped conclusion。
所有 arbitrary-size paper、外部 Gallai、抽象算術、finite source、source realizability、Lean 分開。
未建立新 finite source 就寫未建立／未執行、無 trigger 數；控制若有，每項必標
triggered and holds / not triggered / counterexample，toy 不作 source。

只讀 verifier normal 與 PYTHONHASHSEED=17 實際執行，保 stdout/stderr/exit、核 frozen inputs 不漂移。
自己的 manifest 精確列 immutable payload；排除只限 exact top-level manifest／delivery／receipt
metadata，且 metadata 綁 hashes；nested 同名檔必列 payload。保失敗版本，不覆寫證書。
本地 Markdown links／whitespace 核回。純稽核無新 Lean，lake build 與無關枚舉明列未跑。
保歷史缺檔／E4 provenance／DocGraph 62 duplicates；不為通過檢查改 shared 或刪 scratch。
若不能满足父定理前提，交最小具名 finding 就 STOP；不擴 graph/k、不重開已採分支。
不自行採納 HIGH3，也不把候選提升為 HIGH、全部 S、N2／E 或一般核心存在性結論。
