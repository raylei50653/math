# 本輪固定來源與量詞

BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。
本輪在證據工作前凍結前輪 transport 與 last-rejection 的1082份檔案；
逐份 SHA256 見 [INPUTS](INPUTS.json)，原工作樹狀態見 [BASE](BASE.md)。

完整承接[前輪契約](frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/SOURCE_CONTRACT.md)
及其[存在性輪契約](frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen/audits/2026-10-19-r6-941-existence-f13eb4d/SOURCE_CONTRACT.md)
與全部上游前提：同一有限簡單 plane C5 disk G，原有序框
`(x,y,a,b,c)`、完整支持941、全域最小內點數 k 再最大邊數，
原 r 六度、p 與 h=ell 均五度的具名位置；原 stars、附件、旋轉、
相異性、非邊、私有點及 C3/C4/C5 pocket 定理全部保留。
不加 active-f matching 前提，不使用四色定理。

共同實際核心為 `F=G−{b,p,h,x,y,r}`，induced rim 依序為
`(a,n,R,L,q,c,s,v,w,t)`。每個固定字面 fibre 包含 F 的全部私有點
完整著色；空者計零。全域色置換亦作用於全部私有點。

```
Q1=(G−{p,h})/(n=b,R=q),   Q2=(G−{p,h})/(n=L=b);
J1=(G−{p,h})/(b=L)+aR,   J2=(G−{p,h})+aL+aR+bL.
```

只在 `a1=N01232(Q1)=0` 下使用 J1 分支，在
`a2=N01232(Q2)=0` 下使用 J2 分支，不混合兩個分支的著色。
原 Ji 的完整接受正性及01202、01212零值沿用前輪定理。
本輪沒有證得最後01021零值。

來源定理的量詞是任意大小、滿足上述全部前提的同一實際 G。
有限分割核對只驗證作用於每個實際完整分量的公式；必要支持閉包與
整數控制都不提供一張共同私有圖。紙面、有限核對、來源實現及
Lean 形式化分開，沒有新 Lean 或 commit／push。
