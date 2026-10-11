# N2-55 新 long 化約：獨立紙面採納

2026-10-11。審閱者 root；權威是 `../BASE.json` 的 13 份凍結輸入。
候選作者分別為 high_contact、synchrony；此審閱不以作者 checker 通過代替紙面推導。

## 1. 葉接點 tree 的任意接線數出口：ACCEPT

逐項重建 `../high-contact/REPORT.md` §1 的 H-TREE-LEAVES。
無 shared contact、全部 root 接點為 C 葉時，degree 四及框附件上限二使
「C 葉」與「root 接點」恰為同一點集。原未用色 D 的 bridge palettes
恰形成普通點誘導 forest 的 perfect matching；forest 的 perfect matching 若存在
必唯一，因兩份 matching 的對稱差只能由交替 cycles 組成。故三列使用同一
原 D 邊集。這是輔助計數資料，不修改原 C 的 edges 或 relations。

刪 contact 葉後的普通點圖連通；收縮其 matching 的 counting tree 也連通且無環。
末端 unit 至多一條邊通往其他 unit，因此可在另一原端點選到只有 contact 葉
及 matching 伴點的 y。原 y 至少有兩個 C 鄰點、至多四個，故 contact 葉數
恰為 1、2、3。三類分別迫同一實際框邊重複、第三色 signature 不存在、
三條原框邊的 T signatures 在三列均 rainbow。最後一類由字面表直接排除，
不依未知平面實現或有限圖枚舉。單bridge及無 ordinary 點另處理，無漏案。

因此原 C 在至少一指定列有完整 list coloring。無 U 一 long 的另一原 short
在該同列接回，完整 G coloring 矛盾，source corollary 成立。
另 long 有 shared contact 時的兩-long 接回也成立。含 U 的存在列仍須同步。

## 2. 兩邊盾弧的三類 mask：ACCEPT

逐項重建 `../synchrony/REPORT.md` §§1–4 的 M-LOW-ARC。
證明固定一個原拒絕列，未偷用三列共同拒絕。原 cycle 長度至多 1+k≤4；
contact triangle 不能含普通私有點，也不能在 cutpoint 上有額外 contact。
原 actual support 是兩邊弧，所以 H-degree-two 的實際附件只可能取這兩邊；
attachment injection 限制至多兩個這種原點。

三 leaf blocks 至少需三個 private bridge contacts 及三條附件邊，故不可能。
兩 bridge leaves 已花掉兩邊，任何普通 bridge cutpoint／普通 triangle 私有點
都會超支；contact triangle 的兩臂若直接接 leaf，又被 D palette 判定排除。
只剩單bridge與三contact三點path。

leaf triangle 加 bridge leaf 時，原 contacts 正好三個；bridge leaf 消耗一邊，
剩餘至多一個 ordinary bridge cutpoint 或普通 triangle 私有點。
兩原 triangles 必共享原 cutpoint；若以 bridge 相連，該橋從 contact triangle
端被迫 D，與普通 triangle palette 含 D 的互斥條件矛盾。因此五點 tail triangle
及六點兩 triangle 形均不可略去，也沒有更長原鏈或旁支漏列。

四形的完整 palette 條件分別给 Eq、Diff、Eq、Diff，或空 mask。
第三形保留全部 triangle 附件同在中點的合法局部模式；沒有錯誤排除它。
全部條件在同一原框色表計算。不可染 degree-list 的充分與必要 palette 刻畫
確定精確 mask，沒有只由必要條件宣稱等號。

五份邊互斥 arc pairs 的 Eq sets 兩兩互斥且各非空，所以混類 Eq／Diff
一定留有同列出口。含 U 的原盾弧長恰 2+2+1，使此條件可直接接入 (1,1)；
short 全 diagonal、spokes 避 D、原 pieces 互斥，完整 lifts 能在同列拼回 G。
七個同類必要模板不能稱來源，也不構成父族 closure。

## 3. 原相同 spoke 邊的 K5：独立來源

此命題由 root 起草，不能由本稿自稱另人審查。
`../high-contact/REPORT.md` §3 與 `../synchrony/REPORT.md` §5 是兩個
不同作者的獨立核對；它們接受原二點 fan、兩原 r–s 路及五袋十鄰接。
兩份 low-contact long 的 degree／shield 推論亦由 synchrony 獨立接受。

## 4. 範圍與停止規則

ACCEPT 只限以上紙面結論與所列完整來源 corollaries。
不採納「k=4 也一定 escape」：high-contact 的四contact path 保存全部原
fibres，三列均無 diagonal，是該純局部主張的 counterexample。
有限 target sources 仍零觸發；來源排除由任意大小紙面及已有依賴承擔。
沒有新 Lean theorem，一般原55、N2、E-ARC2 及其他圖類仍 OPEN。
