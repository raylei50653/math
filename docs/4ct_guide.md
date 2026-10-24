# 四色定理（4CT）主目標與可約性路線導覽

## 最新進度

現況核對：2026-10-24。研究主目標改為**在本 repo 的邊界關係框架內建立四色定理的證明路線**；
既有 `K∞=K≤5` 各線保留為工具與子問題，不改寫其 OPEN／CLOSED。
本頁只重新定位目標與證明規格，**沒有新證明、新證書或新 Lean**；4CT 本身是已知定理
（Appel–Haken、RSST、Gonthier 的 Coq 形式化），本線不以它為前提或搜尋 oracle。

| 欄位 | 現況 |
| --- | --- |
| 階段／生命週期 | 方向轉換與規格化：寫定強歸納／可約性規格，並把既有最小來源結果對照為部分不可避免性。 |
| 最近研究更新 | 2026-10-24：確認 [E932⇔4CT](c5_kempe_screen.md) 與 Kempe screen 153 masks 中 T₃ 全拒的非空 mask 只有 932；寫定 §2–§4。 |
| 上次完成 | 單刪五度點的 Kempe 出口在 01232 只剩兩條共點鏈，平面性不禁止（§3）；既有度數／弦結論已列入 §4 ledger。 |
| 目前停止點 | 不可避免性（覆蓋）與可約性（還原）兩項普遍定理均 OPEN；五環 Σ 只描述環長 5，大於 5 的構形需新框架（§5）。 |
| 下一步 | 逐列核對 §4 ledger 的前提差異（全域目錄外最小 vs 4CT 最小反例），再選定 §5 的 A／B 路線。 |
| 接手入口 | 本頁 §2–§5、[E932⇔4CT](c5_kempe_screen.md)、[Kempe 連通性停止點](c5_kempe_connectivity.md)、[無 4CT 前提路線](tasks/c5_no4ct_handoff.md)。 |

### 近期里程碑

| 日期／階段 | 進展與來源 |
| --- | --- |
| 2026-10-24／主目標改為 4CT | 依 [E932⇔4CT](c5_kempe_screen.md) 確認 932 分支即五度點處的 4CT，寫定本頁 §1–§5；原 P/R 文法可達性不是瓶頸。 |
| 2026-10-19／文法內 Dead 集合 | [319 的 56 Live／76 Dead 封閉證書](sources/2026-10-19-c5-grammar-v02/RESULTS.md)；932／933／941 於文法內 0 Live，一般來源覆蓋 OPEN。 |
| 2026-10-14／K≤22 | [C5→C4 來源橋](c5_c4_boundary_pivot.md) 接外部 ≤28 點計算得 `K≤22=K≤5`，三支共同 k≥23。 |
| 2026-10-13／無 4CT 前提度數界 | [最小來源度數界](c5_saturation_degree_bound.md) 及替代鏈：框點度數 ≥4、內點度數 ≥5、n₅≥6。 |
| 2026-09-15／Kempe 單鏈界線 | [Kempe 連通性](c5_kempe_connectivity.md) 與 Errera disk 控制：介面阻擋兩個操作不控制第三色對。 |

研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

**主目標。** 證明每個有限平面圖可四著色，證明在本 repo 的完整邊界關係 Σ、
最小來源與 Kempe 工具上組織，最終可紙面審閱並逐步 Lean 化。
mathlib 目前沒有 4CT；已知證明需要數百個可約構形與電腦驗證，
所以只靠 Kempe 交換、守在五環內的短證明應視為高風險目標，不作排程承諾。

**與既有主命題的關係。**

- `K∞=K≤5` 蘊含 4CT（[無 4CT 前提路線](tasks/c5_no4ct_handoff.md) 的 OPEN 表）；
  反方向未知：即使假設 4CT，原證明鏈的 933／941 仍 OPEN，`K∞=K≤5` 是更強的分類命題。
- [Kempe screen](c5_kempe_screen.md) 已證 `E932⇔4CT`：
  E932 為「沒有合法 disk 的完整關係恰為 T₄=932」。
- 因此 933／941 等其他分支屬於 `K∞=K≤5` 的額外內容，不是 4CT 所需；
  4CT 只需要 932 分支（或等價的最小反例論證）。

**不涵蓋。** 本頁不改寫任何既有報告的結論或停止點；不把文獻結果算成本 repo 已重播證據。

## 2. 證明規格：強歸納與可約性

令 \(\operatorname{Col}_4(H)\) 為 \(H\) 的全部四著色，\(\mu\) 為嚴格下降的大小（例如頂點數）。
足夠證明：

1. 基底圖可四著色；
2. **不可避免性（覆蓋）**：每張非基底平面圖 \(H\) 都含某個指定構形；
3. **可約性（還原）**：對每個指定構形給出較小的 \(G\)，且
   \(\operatorname{Col}_4(G)\neq\varnothing\Rightarrow\operatorname{Col}_4(H)\neq\varnothing\)。

這與「最小反例不存在」同一件事。量詞方向：

| 命題 | 是否足夠 |
| --- | --- |
| 每張目標圖都有一個可還原的較小前身 | 足夠（加基底與嚴格下降） |
| 每張可著色圖都有至少一個安全後繼 | 不足，後繼可能只覆蓋子家族 |

**還原的兩種證法。** 歸納假設只給 \(G\) 至少一份著色，不能指定是哪一份：

- **D-可約**：從任意給定著色出發，以 Kempe 交換走到可延伸的著色；
- **C-可約**：設計 \(G\)，使其每份著色限制到環上都可延伸。

「重新選一份合適的著色」不是免費步驟，必須落在上面兩種之一。

**出口必須是具名有限清單。** 若「可修復」定義為「存在任意有限次合法重染使框只用三色」，
它就等價於 Σ≠932，「最小 932 ⇒ 可修復」只是重述待證命題。
有效的規格是事先列出 E₁…Eₙ（各有前提與下降量），再證幾何限制迫使其一成立。

## 3. 五環切口：目標與已知界線

932 接受的五列 T₄ = {01023, 01203, 01213, 01231, 01232} 恰為框上用滿四色的列；
拒絕的 T₃ = {01012, 01021, 01201, 01202, 01212} 恰為三色列。
在 [Kempe screen](c5_kempe_screen.md) 的 153 個 Kempe 可容 masks
（`artifacts/c5_cells/kempe_screen.json` 的 `kempe_masks`）中，T₃ 全拒的非空 mask 只有 932；
故對可四著色的 disk \(D\)，\(\Sigma(D)\cap T_3=\varnothing\iff\Sigma(D)=932\)。

刪五度點 \(v\) 得 disk \(D=H-v\)，接回 \(v\) 的充分條件是 \(\Sigma(D)\cap T_3\neq\varnothing\)。
只用「\(D\) 可著色」證此條件，就是 Kempe（1879）的論證：

- 以 01232（b₀…b₄ = 0,1,2,3,2）為例，框上相鄰色對的鏈天生連通，交換後仍是四色；
- 非平凡出口只剩 0–3 鏈 b₀⇝b₃ 與 1–3 鏈 b₁⇝b₃；兩者共用 b₃、不交叉，平面性不禁止；
- 這是 Heawood（1890）指出的漏洞；repo 的 [Errera disk 控制](c5_kempe_connectivity.md)
  亦顯示通過全部 AB 狀態仍需 CD 起始三步才逃逸。

所以**單一五度點不是可約構形**；目標引理對每個 \(D\) 為真（因 4CT 為真），但不能靠這一刀證明。
已知證明使用環長至多 14 的構形（RSST），超出 C5 Σ 的描述範圍。

## 4. 既有成果對照（部分不可避免性 ledger）

讀法：以 932 disk \(D\) 加 apex \(v\) 得 \(H\)，\(|V(H)|=k+6\)。
「對應狀態」只記本頁紙面判讀，未經獨立審閱；精確前提以原報告為準。

| repo 結果 | 4CT 語言 | 對應狀態 |
| --- | --- | --- |
| [E932⇔4CT](c5_kempe_screen.md) | 五度點的 link disk | repo 紙面已證 |
| T₄ 全收 ⇒ 外框無 chord | apex 處無分離三角形 | 紙面對應，待審 |
| [共面正規形](c5_cofacial_normal_form.md)：簡單、二連通、內面全三角 | \(H\) 為三角化 | 前提不同：repo 由全域最小加最大邊數取得，待核 |
| [度數界](c5_saturation_degree_bound.md)：框點 ≥4、內點 ≥5 | 最小度 5（Kempe 對 ≤4 正確） | 結論同型；repo 最小性是目錄外全域最小，不是 4CT 最小反例 |
| 同頁 §2／§4：C4 cap 與四度點排除 | Birkhoff：無分離四環 | 待核 |
| [K≤22=K≤5](c5_c4_boundary_pivot.md)，k≥23 | 最小反例至少 29 頂點 | 依外部 ≤28 點完整計算 |
| [C8 剝層](c5_c8_peeling.md)、T2 的 932 h=4 apex 度數 | 五度點附近的局部結構 | 待與 Wernicke／Birkhoff diamond 型構形比較 |
| [319 Dead 集合](sources/2026-10-19-c5-grammar-v02/RESULTS.md) | 無直接對應 | 文法內可達性，不是來源覆蓋；不搬用 |

**最小性差異（必查）。** 只以「最小 932 來源」或「4CT 最小反例」為前提時：

- 度數 ≤3 內點可刪：只用 Σ 不變，可直接搬用；
- 四度點排除：原證明以 s<k 的增廣 C5 進入目錄 K，依賴三支共同的全域最小性；
  只對 932 最小時，增廣圖可能是較小的 933／941 來源，需重證；
- k≥23、h≥4、n₅≥10 等：均建立在全域最小上，需逐條重核。

改以 4CT 最小反例（最少頂點的不可四色平面三角化）在五度點處定義 932 disk 時，
可直接使用 Birkhoff 的古典結論（最小度 5、無分離三角形與分離四環），但須保留文獻信任標示。

## 5. 停止點與候選路線

**OPEN。** 不可避免性與可約性兩項普遍定理；本 repo 尚無任何環長大於 5 的可約性證書。

候選路線（待選定）：

- **A. 可約性框架推廣**：把完整邊界關係 Σ 從 C5 推廣到 Ck（k≤14），
  以既有 D-／C-可約判準建立構形證書，再接 discharging 的不可避免性。
  重用 repo 的完整關係、Kempe screen 與證書基礎設施；工作量接近重做 RSST。
- **B. 五環內具名出口清單**：以 §2 的 E₁…Eₙ 規格，在 Errera 等近反例染色上量測觸發，
  找清單缺口。風險高，成功即為 4CT 的新短證明。

兩條路線都要先完成 §4 的前提核對，避免把全域最小的結論搬到不同的最小性上。

## 6. 文獻（未在本 repo 重播）

- A. B. Kempe, *On the geographical problem of the four colours*, Amer. J. Math. 2 (1879).
- P. J. Heawood, *Map-colour theorem*, Quart. J. Pure Appl. Math. 24 (1890).
- G. D. Birkhoff, *The reducibility of maps*, Amer. J. Math. 35 (1913).
- K. Appel, W. Haken, *Every planar map is four colorable*, Illinois J. Math. 21 (1977).
- N. Robertson, D. Sanders, P. Seymour, R. Thomas, *The four-colour theorem*, J. Combin. Theory Ser. B 70 (1997).
- G. Gonthier, *Formal proof — the four-color theorem*, Notices AMS 55 (2008).
