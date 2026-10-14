# 返回證明的其他分支：低 p/q 的新介面與交換角色

2026-10-14。凍結 BASE `a11d4bb`；完整 commit、直接輸入 SHA256 及寫入範圍見
[INPUTS](INPUTS.json)。本輪回應「其他分支能不能用」，使用獨立 detached
worktree，保留原證書及失敗紀錄。研究階段未 commit／push；本次授權的
相接發布與實際檢查見 [發布紀錄](../../docs/history/2026-10-14-c4-return-branches-publish.md)。

**能用在交換角色後的雙低度支：若原 p=q=5，它們除 b 外的共同鄰點 l
必至少六度。另證 a=4⇒t≥6、c=4⇒s≥6，三種來源都適用。
單獨 p=5 則得到精確 mask14 的較小 C4 介面，但尚未排除。**
旋轉分支另給有完整色關係限制的 degree 下界。一般 K≤22／k≥23 不變；
mask13 六接點、一般 T／T0 延拓、任意大小目錄等式仍 OPEN。

## 固定的原來源與證據層

G 是所有完整 C5 關係不在 K132 的合法 disk 中，先全域最小內點 k、再最大
邊数的同一原圖。共同對齊 `B=(x,y,a,b,c)`、完整 `Σ∈{932,933,941}`，
固定 `d_G(x)=d_G(y)=d_G(b)=4`。原五個 apex 依序為 `(r,t,p,q,s)`。
沿已證幾何得到四連通三角化球面 T0、兩個具名三角面 zxy／zpq、
`R=T0−{x,y}` 的 induced 外框 `(z,s,r,t)`。

每份 R 完整染色共同滿足 ABAB→pq CD、ABAC 空、ABCB→CD 或 BD、
ABCD→BD。原返回證明已給 r≥6，r=6 時 s,t≥6。本輪維持原邊、rotation、
literal contacts、共同色框、完整 fibres（包含空）、全部同份接回色；
沒有以普通小代表代換內部 p,q，也沒有將不同列的 witnesses 拼接。

紙面新結論與有限局部控制分開：下列 source 度數界及介面化約是任意大小
條件式紙面論證；terminal partition／switch closure 只是必要有限模型。
保存的模型 survivor 不表示存在目標來源。沒有新增來源實現、外部枚舉或
Lean theorem，沒有使用四色定理。

## 逐支成果

| 嘗試的原分支 | 確實得到的結果 | 證明／控制入口 |
| --- | --- | --- |
| p=5；q=5 對稱 | 改以 T0−p 的原 link C4 為外框，完整支持恰 mask14；兩個 diagonal fibres 非空，rainbow fibre 分成兩個精確 palette sector | [低 p/q](pq/PROOF.md) |
| p=q=5 | 刪兩點後交換指定三角面的角色，得到同型 mask13；若另一個 pq apex l 原五度，原返回 lemma 直接矛盾，故 l≥6 | [交換角色](pq/PROOF.md) |
| 整份原圖旋轉 | 932／933 且 a=4⇒p≥6，p=6⇒t,q≥6；932 且 c=4⇒q≥6，q=6⇒p,s≥6 | [旋轉適用範圍](rotation/PROOF.md) |
| 一般 mask13 R | 補上兩個 ABCB sector 的缺色端點連通；可交換的 BC 子 fibres 有精確雙射，但返回到另一個允許 sector，未矛盾 | [一般返回](general/PROOF.md) |
| r≥6、t=5 的直接刪點；s 對稱 | a=4 的接點 h=p 子支恰424，被外面 z=r 商圖矛盾排除；一般 t=5 的完整支持只留956／1012／1020 | [較高 r](r_high/PROOF.md) |
| r=7 | 刪 r 露出真實 C6，31個外框型保留26型／111個 joint orbits；沒有 no-rainbow C4 前提 | [C6 前緣](r_high/PROOF.md) |

### 為何單獨 p=5 與雙低度不同

原 p 五度在 T0 中是四度內點，原 link 為 `(z,q,l,m)`。只從 R 刪 p
會留下內洞，不能直接套原 r 三度刪除的 C4 lemma。改在同一球面 T0 上
以 p 的 link 為新外框，得到真實較小 disk H=T0−p，保留原內部邊 xy。

H 的 ABAB 完整染色有兩個合法 p 色；它們的 pq palette 不同，卻必等於
同一份 H 染色固定的 xy palette，所以 ABAB 空。兩種外面 diagonal
identification 各得 k+1 點的 planar quotient；外加三點 C5 cap 後只有
k−1 內點，原全域最小性給可染性。兩份商圖分別強迫 H 的 ABAC 與 ABCB
非空；配相對 C4 七關係，H 的完整支持恰14。

這個 H 自己有非空 rainbow fibre，故不能用 no-rainbow 返回直接排除。
若 q 也五度，它與 p 在 T0 都四度；刪兩點露出另一個 C4，內部保留的是
xy。兩指定三角面的 palette equality 是對稱的，原 cap 表及 joint-fibre
證明可全套交換使用。其新外框的 apex 正是 l；l 若五度，刪 l 後形成
rainbow-free mask7，原返回 contradiction 適用。因此雙低度支給新的
`d_G(l)≥6`，沒有排除整個 p=q=5 支。

### 直接刪 t 的新排除

原 t=5 在 R 中四度，刪後 V 的外框為 `(z,s,r,w,h)`、總點 k。
原 zr 無邊，外面識別 z,r 得 k−1 點的 loopless planar quotient；外加
三點 C5 cap 得 k−3 內點，原最小性保證其關係在非空的 K132。商圖染色
接回 V 時 z=r；這種 proper C5 只有 ABABC／ABACB／ABACD 三型。
全部 t lifts 已排前兩型，故 **ABACD 必非空**。

若 h=p（恰 a=4），完整支持原已迫424，而424不含這三型，立即矛盾。
因此 `a=4⇒t≥6`，反射得 `c=4⇒s≥6`；這不需要搬運 singleton 假設，
所以三種來源都適用。若 h≠p，先前十個必要支持中含 ABACD 的只有
956／1012／1020，得到更窄的來源前緣，仍未全排 t=5。

### 旋轉不能只搬 degree

返回證明需要新相鄰 pair 的兩個完整 singleton fibres 皆空。932 的五個
singleton 全空；933 只允許 singleton4；941 允許 singleton2、4。
所以 a,b 這個 pair 的 failure 前提只適用932／933，b,c 只適用932。
本輪 checker 明列941／ab與933／bc的正 target，阻止錯誤搬運。

結合已有高 p,q 的 k≥28 條件界，在 k≤27 域進一步得到：

- 932／933 且 a=4：必 q=5、p≥7。
- 932 且 c=4：必 p=5、q≥7。

這些是特定低度子域的必要條件，不是新的全域下界。

## 接續義務與停止點

單低 p/q 的 mask14 保留真實較小 disk 及完整 fibre sector 搬運；整個來源分支
仍 OPEN。 雙低 p/q 則只排除
l=5，保留 l≥6。一般 mask13 的 BC 返回只有條件式子 fibre 雙射；仍須
證明所需子 fibre 非空，或用原幾何找到真正落入空 fibre 的返回。

r=6 已有的271／314／319及精確整數 count witnesses 仍存活；直接 t=5 的一般三候選與 r=7 新介面
沒有被有限零-hit 或 ordinary representatives 宣稱排除。
純刪點再按原圖接回保持完成內點數 k，沒有嚴格下降定理。
目前主線接續入口見 [Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)。

## 驗證與文件傳播

原返回 checker 的 default／seed17 replay 均 PASS，凍結輸入 drift 為0。
本輪各新局部 checker／certificate 的實際結果及獨立 review 見
[VERIFICATION](VERIFICATION.md)。保留初次 rotation replay 的 tuple/list
序列化失敗與原 script，修正後 replay及蓄意改壞證書的 negative control
分開留證；不覆寫原數學證書。

L1 核對並更新 C4 專題、Kempe 導覽和 STATUS 的直接條目，交付限定的新增
介面與度數界。父 mask13 義務仍 OPEN，沒有改變一般大小界或 T／T0 主命題；
上層 synthesis／no4ct handoff reviewed unchanged，不擴大到其他研究線。
