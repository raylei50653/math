# 一般 wrong-side branches 的獨立紙證覆核

2026-10-23。只審
[新 branches PROOF](../2026-10-23-941-wrong-side-branches-6b09cd4/PROOF.md)，
未改其文件／證書；有限 checker 僅作輔助。

結論：q 刪點附枝、完整 link 色數界及 U 框分支三部分均通過，未發現需改
的全稱論證。以下列明依賴的量詞及框例外。

- **q 刪點後的 b 附枝也避 c。** 反設 c 與 b 在同一 B−q 分量 A，取
  R:c→b 在 A，再接原 Y−q−c。因 Y∈C 而 A∩C空、q 已刪，此 S₀ 簡單，
  最後 C 點恰 Y。P[r,b] 原01，排 q；其最後 C 點 r∉B，排 Y；b≠c
  及同一 P 簡單又排 c。故首次 P 交點在 R，Γ 確含 boundary Yq、qc。
  Γ 在 q 只留一個 F 扇區為有界側；同一對中心對重選 S₀ 仍一內一外，
  外側 patch 的 q-incident 實際面給矛盾。沒有把 G 的 F 外原面借入。
  此後 A 避四個 B 框接點，只是 B 刪點後的附枝；整個 B 仍非 rootless。

- **私有共同 b3 的完整度數為至少6+m。** 兩個不同 patch 的 b1 皆在
  C，且彼此不同；B 連通給 v 在 A 中的原1鄰 f，f∉C。故完整 cyclic
  link 至少三個原1點。proper coloring 使1點獨立，每個貢獻兩條不同的
  incident link 邊；D0 各另給不 incident 於1的原02邊。兩 patch 僅共 v，
  這 m 邊不同，故 D−2n1≥m 的完整 link identity 正確。不是僅把局部
  已知鄰點相加，也未套給框 q。

- **q 的 F 路界。** F-link 端點是 Y1、c1；新附枝引理使 f≠c，且 f 不
  等於兩個在 C 的 b1，c 亦不等於兩 b1。故 n1≥4；兩 b1 都非 Y 時再
  有 n1≥5。路的原1 incident 邊數恰2n1−2，D0 邊仍不同，得到
  d_F(q)≥7+m 或9+m 正確。主稿只聲稱 F 度數，未誤用 G cyclic link。

- **U 兩支不能分別含 V／Y。** 在同一 C−U 的 R_C、E_C 分別取 r→V、
  Y→e 簡單路，兩分量不交，接 V−U−Y 確為同一 C 的簡單 r/e 路。
  因固定 S 後內外中心集合不隨 L 變，仍是同一對 patch 一內一外。
  Γ 在 U 用兩條 F boundary 邊，與兩個都含 U 的 patch 矛盾。
  e=V／Y 的零長端段亦無妨。至少一支避 V、Y 的等價敘述成立，但不能
  據此說它全無框，因 w／t 等其他 C 框接點仍可能在其中。

- **U 原度至少6+m₀。** 上述避 V／Y 分量必有真正的 U-C 鄰點 u1，
  原色1且不同 V、Y，故 F-link 原1點至少三個。每個 D0 在 U-link 給
  原23邊；即使兩 patch 另共01邊，兩條 D0 邊若相同就會使 D0 原中心
  U−b3 相同，違不同真交。故 d_F(U)≥5+m₀；再用已凍結 Uz5 原邊及
  z5∉F，得到 d_G(U)≥6+m₀。此處只需 G-star 包含 F-star 與 z5，未
  偷假設這就是全部 G-star。U5 排除、U6只能雙D1、U7不能雙D0均正確。

- **原01逃逸沒有補出 B 內路。** 在 P[b,c] 取第一個出 A 的 B 點 d、
  其前最後 A 點 a，兩點間內部避 B；原最後 K 出口及最後 C 橋使整段
  避 K、C。投影到原完整 J 樹，只推出同一 J−B 分支及同一 B 鄰02節點
  L₀，未誤推整條原路在 L₀，亦未把 L₀ 認成 M 或 z4 的原02分量。

正常 finite checker 重播通過；其控制仍不是完整941來源。上述新子支排除
及度數下界由原面的共同嵌入、完整原星及全路量詞支持，未推出一般
wrong-side、較小 bad 或 matching 已完成。
