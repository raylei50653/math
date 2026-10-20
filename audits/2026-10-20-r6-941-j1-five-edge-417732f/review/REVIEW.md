# 主審：完整cap獨立重建及數學界線

[獨立checker](caps.py)沒有匯入counting的cap生成器；直接列出原被刪點的
全部原邊，逐點由原框鄰點建合法色list，再測全部cap內邊，對G/Q1/J1重新
枚舉全部左右lifts。canonical C13亦獨立依restricted-growth規則生成。
全部66,430個states與三份10×66,430矩陣的canonical JSON SHA256，與
counting/caps.json.gz完全相同。對比由頂層check.py每次重新執行。
證書見[caps.json](caps.json)。

紙面審查確認：一般五邊路C7 induced不依賴only-R或R五度；only-R的W7
必先用無三邊路排C7弦才成立。原C13不要求induced，n及其餘私有附件均在。
完整來源Z與選路候選R的量詞分開；源零值可限制其子集，正性、S4及完整
orbit方程不能任意限制。cap與核心Kempe交換沒有被假定可交換。

counting的C11全欄校準是生成器校準，並非C13來源覆蓋的替代證明；來源到
必要家族的覆蓋由counting/PROOF中的三角disk與完整orbits紙證承擔。
61,308存活格不提供共同可行計數點；數值探索無結論。未找到W7或一般J1
的來源矛盾，不聲稱較小bad或新Lean。
