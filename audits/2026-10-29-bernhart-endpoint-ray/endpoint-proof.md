# RIP 共同端點補證筆記

2026-10-29。供主報告整合；一般結論為紙面拓撲證明，固定來源重播為 Python，沒有新增 Lean。

固定一張有向 plane near-cubic disk、同一份 proper Tait 染色及同一條完整 ab
boundary-to-boundary 原路徑 S。切開 S，使用由原 rotation 決定的共同側別、每側真實環序。
P 是該側一個完整 retained ac 分量，Q 是一個完整 retained bc 分量；保留全部路徑及閉圈、
每條共同 c 原邊身份。一般定理不要求兩路端點互異。

## 正向與推離規則

每側邊界取正向，即該側內域在行進方向的左邊。令 ε(v)=+1 表示原 cubic 頂點
的逆時針色序為 (a,b,c)，反序為 −1。H=∂P∩∂Q 的共同端點只能是
cut port 或原始 c 邊界葉；兩個系統在每個共同端點都沿同一條原 c 邊結束。
不可能只有共同端點而沒有共同 c 邊：該端點剩餘度數為一且唯一邊色為 c。

共同端點用很小的邊界 collar 拆成 P、Q 的兩個終端。規則如下。

- rotation 推離：共同 cut port ε=+1 時沿正向排 P,Q，ε=−1 時排 Q,P；
  這相當於將 P 終端放在原 a dart 所在一側、Q 終端放在原 b dart 所在一側，
  保留原 (a,b,c) 的 cyclic rotation。
- 原始 c 葉沒有原 cubic ε，明定用正向 P,Q；不能把下面的人造 cap 符號說成原葉的 ε。
- canonical 推離：全部共同端點一律沿正向排 P,Q；與 rotation 推離相差的恰為
  ε=−1 的共同 cut ports。

為驗正負號，取局部座標：邊界為 y=0、內域 y>0、正向由左往右。
在 (0,δ) 放人造 cubic cap，a 支向 (−δ,0)、b 支向 (δ,0)、c 支向 (0,2δ)。
從 cap 觀看逆時針色序為 (a,b,c)，故正向 P,Q 的 cap 符號 η=+1。
互換兩終端則 cap 符號變 −1。這推導同時決定了公式中的號，沒有任選每個端點的 ε。

## 兩個等價公式及邊界修正

將原 cubic 頂點保留 ε，原始 c 葉的 cap 值明定為 +1，記為 barε。
令 C=E(P)∩E(Q) 是共同原 c 邊的集合，每條邊只計一次，定義

\[
L=\sum_{uv\in C}[\bar\epsilon(u)=\bar\epsilon(v)],\qquad
B=\sum_{v\in H\cap\operatorname{ports}(S)}[\epsilon(v)=-1]\quad(\bmod2).
\]

則完整 RIP 為

\[
\boxed{L=\operatorname{Alt}_{\rm rot}(P,Q)},\qquad
\boxed{L+B=\operatorname{Alt}_{\rm can}(P,Q)}\quad(\bmod2).
\]

Alt 是相應推離後四個互異終端的交錯指標。若至少一個分量是閉圈，沒有共同端點，
仍沿用舊 RIP、右側為零；兩個路徑在不同側時也無共同原邊，值為零。
四端點原本互異時 H 空、B=0，回到舊式。

**證明。** 先按 rotation 規則在每個共同端點添 cap、把同時結束的兩條曲線分開。
cap 是局部平面 collar 操作，不更改鄰域外的共同原 c 邊。每個 cut-port cap 的
cyclic 色序等於原頂點 ε，葉 cap 的符號依明定為 +1。新終端全部互異。
每條共同 c 邊的 ribbon 兩端附件交錯，當且僅當兩端 cap／內點符號相同；
不同 c 邊有不相交 ribbon 鄰域，鄰域外曲線不相交。故總交叉奇偶等於 L。
disk 中兩 proper arcs 的交叉奇偶等於邊界四端點的交錯，得到第一式。
此處引用舊 RIP 證明的局部 ribbon 計算，並沒有假設未知來源的特殊路徑長度。

從 rotation 推離改為 canonical 推離時，每個 ε=−1 的共同 cut port
恰互換一對相鄰的 P、Q 終端，交錯指標因此翻轉一次；其他端點不變。
因此 Alt_rot=Alt_can+B，得到第二式。
亦可直接把共同邊邊界端點的有效符號改成 +1：因為
[x=y] 對任一端點符號翻轉恰改一次，而每個共同端點恰接一條共同 c 原邊，
總交叉數從 L 改成 L+B。這給出同一公式的逐邊核對。

共同 c 邊兩端都在邊界時沒有例外：leaf–port 只累加 port 項；
port–port 分別累加兩個 port 項，即使落在同一條原邊仍不能漏一端；兩次翻轉會抵消；
leaf–leaf 的 barε 兩端皆 +1，該邊貢獻 1，P,Q,P,Q 恰交錯，B=0。
這也涵蓋 P、Q 是同一條單邊路徑的情形。

此定理只對同一實際 disk、同一染色、同一切口的具名完整分量成立；它是必要條件，
不證平面來源充分性，也不從一個失敗 extension 排除所有射線來源。

## 舊 representation 的轉向與重播

舊 checker 的兩側 order 都沿 S 的起點到終點列 ports，故只有 side=1 的內域在左，
side=0 的內域在右。這由原 CCW rotation 中 incoming→outgoing 是否相鄰計算，
不是一般 disk 的 side 編號慣例。新 checker 對這兩個 frozen 來源族把舊 side0 反轉、
side1 保留，得到上文正向環序。一般輸入須自行提供真實正向邊界。
所有原邊界葉按 frozen 證書的原葉序列，另用共同外部頂點收口，核實 disk rotation；
不能僅核 open ribbon graph 的 genus，因為翻轉可能保持 sphere 卻改變 marked 葉環序。

新 checker 先核兩份 frozen 證書原 bytes 的 SHA256，再以舊程式完整重建、逐項比對相等，
再核舊已涵蓋分支，
並對每個舊未涵蓋 pair 保存共同端點／原邊、L、B、兩個 Alt；全部通過。

| 來源 | 舊已覆蓋重核 | 共同端點新覆蓋 |
| --- | ---: | ---: |
| 兩份 ray-local、四條切口 | 40 | 16 |
| C8 wheel、43染色344切口 | 3,056 | 1,432 |
| C8 wheel stack、43染色344切口 | 4,068 | 1,560 |
| 合計 | 7,164 | 3,008 |

16 組 local 分成 12 組單 port、4 組雙 port；2,992 組 wheel/stack 分成
1,344 組單 port、144 組雙 port、672 組 port+leaf、832 組單 leaf。
另各來源保留一組**新共同端點分支**的 rotation 負控制，共四組：
只反轉非切口 cubic 頂點的 rotation，完整原圖／染色／retained 接線／環序不變；
兩個完整 RIP 式同時拒絕。含 marked 邊界收口的 genus 由 0 變 1。
舊 theta 與舊非共同端點正負控制由舊證書完整重播保留。

```bash
python3 scripts/ck_retained_endpoint_parity.py --check audits/2026-10-29-bernhart-endpoint-ray/endpoint-parity.json
```

結論：RIP 的原定 near-cubic disk 範圍內，共同端點分支補證完成；
新增必零座標及已排除 full-lift 射線仍為空。所有正偶比例來源是否排除由另一主研究負責。
