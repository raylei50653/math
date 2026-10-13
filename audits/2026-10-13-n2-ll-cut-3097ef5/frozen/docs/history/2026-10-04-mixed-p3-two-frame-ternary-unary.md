# C₃：雙框點三接點 unary 的原 tight bridges／葉 block 與 K₅

2026-10-04，Git 基準 `0e3812712b68f57927df86f30a07bb8074e090f9`。
工作目錄 `/home/ray/developer/ai/math`；起始已有四-spoke、共鄰 P₃、D₂
整合及索引的未提交成果。本輪新增固定 C₃ 證據與相連文件，未 commit／push。
完整前提與任意大小證明見[報告](../c5_mixed_p3_two_frame_ternary_unary.md)。

## 結論及具名來源

固定 **CPP-134-1／geometry 34／side_join_id 20**；case ID=86、local ID=134、
branch=1、side IDs=(8,1)。保留原 S₀=014、S₁=14、S₂=4，完整 P₃ triples
={(3,0,1),(3,0,3)}、禁對 {(1,3),(3,1)}，原 zw／zx₂／wx₂、六份附件及同一 q=01012。
兩 root 無 spoke、各一份原三接點 unary；z 側自身支援 {b₁,b₂}、禁色
{0,2,3}，w 側自身支援 {b₂,b₄}、禁色 {0,2}，E_z={1}、E_w={1,3}。
w 側完整原關係與其 fibres 保留為同一圖上的未知 relation，沒有替換 tuples。

完整 degree 四給 d_D=4−p−s₁−s₂；固定禁色 z=0 時，
|L₀|=d_D+ps₂。connected strict-list 貪婪法迫 ps₂=0，接點不能碰 b₂，
遂恢復 d_D≥2。固定 z=2 為原不可染 tight degree assignment；
Gallai 使原 blocks／palettes 為 blockwise-uniform。
原 z–x₂–b₄ 與 B 構成連通外部，原 bridge singleton／tether 法排 K₄。

leaf odd cycle 的 degree 二 private vertices 有 T=接點＋b₁、N=非接點＋
b₁＋b₂ 兩型；L₂ 分別 {0,3}、{2,3}，原 leaf palette uniform 迫純型。
純 N 葉選相鄰 private a,b；D−{a,b} 連通且留全部三個接點。
X=(D−{a,b})∪{z,x₂,b₀,b₄,b₃} 連通；五個 branches a,b,b₁,b₂,X
的十對原邊鄰接給 K₅ minor，排除原任意大小 N 葉。
此後每個剩餘 T 葉至少耗兩個互異接點；兩葉需四點，故原 D 只有一個
odd-cycle block，再由 uniform palette 及三接點身份迫回只碰 b₁ 的 triangle，
與指定雙框點支援矛盾；原外路亦給 C₂ 的 K₅ subdivision。

這是任意大小紙面來源排除；只用原禁色 0、2，第三禁色 3 仍保存。
非接點同碰兩框點的內度二並未被 degree 限制直接刪去；本輪重新證明
其原葉幾何矛盾後，才使用接點葉數預算。
前層 36 cases／140 geometries／900 joins 保持原 artifact，零表格刪除。
本輪只記固定 geometry 34／side_join 20 完成，未算整個 CPP-134-1、
其他 w 角色或 geometry 35 完成，0 target，未新增 Lean theorem。

## 證書及局部正控制

新增 [checker](../../scripts/c5_mixed_p3_two_frame_ternary_unary.py) 與
[observations](../../artifacts/c5_mixed_p3_two_frame_ternary_unary/observations.json)。
證書綁定自身、C₂、common-endpoint、capacity、base scripts、兩份 predecessor
observations 及原 rotation input 的 SHA256，且重新核對 predecessor 的 input hashes。
geometry 34 的原 rotation 正控制保持；收縮骨架 root degrees=(4,4)，
不稱為原 root degrees=(5,5) 的來源實現。

- 八個原 (p,s₁,s₂) 點身份、32 個 pinned-list 核對；兩個 p=s₂=1
  身份由 z=0 strict-list 紙面引理排除，其他六型保留。
  z=2、3 兩份 T／N leaf palette 對比；任意 blocks／葉數由紙面證明。
- 162 份 K₄ tethers／外部 hub minor 控制：四個原 clique 方向可到
  z、b₁、b₂，兩種 tether 長度；每份五組 branches 連通、不交且十對鄰接。
  它們是有限原路控制，不是 degree 四或 source 實現。
- 四份 N 奇環＋原 bridge＋T triangle 模型，n=3,5,7,9，D 大小
  6/8/10/12、每點完整 degree 四、自身支援 {b₁,b₂}。
  每份完整接點關係恰為六個 permutations(0,2,3)，保存 24 份 tuples 的內點 lifts。
  同一模型中，N leaf 的 cut c 強制取 1；三拒絕 pins 下 T triangle 的
  bridge 端 d 也強制取 1。因此新 N 葉與原 bridge 確能通過 tight 色限制。
  刪原 bridge 後，對同一圖、同一 q／root pin 測試全部 16 個有序 (c,d)
  pins，完整端點 relation 恰 {(1,1)}，共 12 份關係與完整局部 coloring lifts；
  未以獨立端點 marginals 拼接，不宣稱這些 pins 皆能接上原 P₃／w。
- 原 unary 邊數 17/23/29/35，共 104；逐邊刪除的完整 root-pair relation
  均為 U²，共 416 份局部四色 witnesses，312 份拒絕 pin witnesses 的刪邊兩端同色。
  另有 104 份保留原 B、P₃、zw／wx₂ 的 context partial witnesses，
  固定 z=0、w=1、P₃=(3,0,3)。原 D_w 的避 w=1 fibre 由禁色 {0,2}
  保證非空，內點不在此枚舉，不冒充整份 M 的逐邊 minimality。
- 四份原 N leaf 的 K₅ minor、162 份 K₄ route minor、條件 T triangle 的
  六份 tuples／九條刪邊／36 局部 witnesses／九份 context partial witnesses、
  兩份原外路 K₅ subdivisions。條件 triangle 明標自身支援只為 {b₁}，
  不符合 geometry 34 指定支援，不用它取代原 unary。

以上固定控制的 degree、完整關係及局部刪邊都可成立；它們共同嵌入原
外路時失敗於平面性。任意大小引理不是對四個奇環模型作外推。
外部依賴為 [Dvořák Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪 live 核對 connected degree assignment、strict-list 與原 block palette 定義。
未用 critical-graph corollary、T4 或 target 拒絕假設。

## 重播與實際驗證

```bash
python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py
python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
python3 scripts/c5_mixed_p3_common_endpoint.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

C₂ 及 common-endpoint 前層逐 byte 重播通過；新 checker 生成與一般／seed=17
逐 byte 重播通過。既有 Lean build 通過 8,831 jobs，保留既有 linter warnings，
本輪未改 Lean 檔。最終新證書 760,148 bytes，小於大型 manifest 門檻，
可直接追蹤，未更動 manifest／ignore 規則。
`check_docs.py` 通過 529 份 Markdown／5,477 本地連結，anchors／直接索引／
HANDOFF 均通過；DocGraph 通過 62 documents／213 relations／5 families，
零 errors／notes。`git diff --check` 通過。

未重跑：capacity 全表 standalone、其餘 P₃ 對稱／非對稱／中點端點
standalone、no-mixed 十五類、singleton／K₂ 完成表、933／941 excess、
R 系列、atlas／profiles／閉包及 Lean axiom audit。
新 checker 的固定入口仍重算 capacity join 與完整有序介面，不表示
上述 standalone 全部已重新驗證。
HANDOFF 的研究線／tag 不變，依文件治理更新 weak-deletion guide；
README 新增證據入口，STATUS 直接索引新報告及本歷史。

## 停止點與貼上式交接

C₃ 固定 **CPP-134-1／geometry 34／side_join 20** 的來源排除完成。
下一入口為同一 case／geometry 的 **side_join 60**、side IDs=(27,1)：
原 z 側改為兩份 unary，接點數 (2,1)、禁色 ({0,3},{2})、無 spoke；
w 側仍是原三接點、禁色 {0,2}、無 spoke，兩側 residuals {1}/{1,3}。
下一型未分析，須保留各分量自身支援、原接點、完整 tuples、bridges 及原外路。
原整側支援 {b₁,b₂}/{b₂,b₄} 不能任意分派給兩份 z unary。
其他 w 角色／geometry 的同引理覆蓋亦未另行逐份證書化。
目前入口見 [weak-deletion §3](../c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)。

> 先讀 docs/HANDOFF.md、docs/STATUS.md 與 weak-deletion guide §3。
> C₃ 已排除 CPP-134-1／geometry34／side_join20 的原三接點 unary：
> 原 own support={b1,b2}、f={0,2,3}。禁色0 strict list先排contact-b2，
> pin2 Gallai的leaf private分T(contact+b1)／N(noncontact+b1+b2)。
> N葉相鄰a,b與原D−a,b、z-x2-b4、frame b0-b4-b3組K5 branches，
> 然後才用T葉接點預算，迫只碰b1的triangle與指定支援矛盾。
> 完整P3、w未知原relation、兩側接點與同框保留；原表36/140/900不刪。
> n3/5/7/9的N葉+bridge+T triangle有degree4、六tuples及104刪邊控制，
> 但原外路K5使它們非disk。0 target，外部Gallai+紙面+Python，未Lean化。
> 下一題同case／geometry34／side_join60：z兩原unary(2,1)，f({0,3},{2})，
> w原ternary f{0,2}，自身支援與完整同圖關係不可拆。
> python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check。
