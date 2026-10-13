# C₄：geometry34／join60 兩份原 unary 的逐分量完整 relation 排除

2026-10-04，Git 基準 `0e3812712b68f57927df86f30a07bb8074e090f9`。
工作目錄 `/home/ray/developer/ai/math`；起始已有四-spoke、C／C₂／C₃、D₂–D₄
稽核及索引的未提交研究成果。本輪新增固定 C₄ 證據與相連入口；未 commit／push。
完整前提與任意大小證明見[報告](../c5_mixed_p3_two_frame_two_unary.md)。

## 固定身份及結論

只處理 **CPP-134-1／geometry34／side_join60、side IDs=(27,1)**，
case ID=86、local ID=134、branch=1。保留原 P₃、S₀=014、S₁=14、S₂=4，
完整 triples={(3,0,1),(3,0,3)}、禁對 {(1,3),(3,1)}，同一 q=01012。
兩 root 無 spoke，E_z={1}、E_w={1,3}，整側 A_z={b₁,b₂}、A_w={b₂,b₄}。
原 zw、zx₂、wx₂、框環序、J=b₁b₂b₃b₄ 及原外路保持。
w 的原三接點 relation、禁色 {0,2} 及 fibres 保持符號身份，不替換 tuples。

z 的兩份原 unary 為 D₂、D₁，接點分別 (u₀,u₁)、(r₀)，禁色 {0,3}、{2}。
自身支援 A₂、A₁ 只知各自包含於 {b₁,b₂} 且聯集恰為 {b₁,b₂}；
全部九份 ordered 必要配置都保留，不替原分量挑選其中一份。
完整 degree 前提與每份原內邊／bridges 保持，沒有合成 C₃ 的一份 ternary。

每份自身附件框色都由 0、1 組成。σ=(2 3) 只作用於一份 detached unary
的完整染色 lift，保留原頂點、有序 contacts、每條原內邊及 bridge、實際框附件；
完整 relation 因此 σ-封閉。指定禁色 {0,3}→{0,2}、{2}→{3} 都不封閉，
兩份原分量各自已矛盾，故固定 key 沒有來源，更不可能共同嵌入 disk。
這個任意大小紙面雙射不用 Gallai、T4 或 minor 定理。

飽和接點數給 D₂ 恰三份完整 relation 候選：{(0,3)}、{(3,0)} 或兩者；
D₁ 恰為 {(2)}。證書保存各候選所有四個 root pins 的完整 fibres，
逐份 σ 像及必缺 tuples；九份支援配置 × 三份 binary × 一份 unary
共 27 份必要組合均無 survivor。這不是 27 份實際原圖枚舉。

## 原 bridges、完整 lifts 與整側資料負控制

新增 [checker](../../scripts/c5_mixed_p3_two_frame_two_unary.py) 及
[observations](../../artifacts/c5_mixed_p3_two_frame_two_unary/observations.json)。
固定入口重算既有 capacity join／P₃ 完整有序介面，核對 C₃ 的 next_entry；
保存自身、C₃／C₂／common／capacity／base scripts、三份 predecessor observations
與原 rotation input 的 SHA256，並核對前層 input hashes。

- 4 份各自支援候選、9 份 ordered covers、3 份 binary 完整 relations、
  1 份 unary 完整 relation，27 份具名接合檢查、0 survivors。
- 20 份完整有序 contact 座標域、16 份內邊／bridge 端色真值、8 份
  實際 b₁／b₂ 附件色真值。16 是所有端色組合，**不是 16 條已知原 bridges**；
  任意大小原 bridges 的保持由完整 lift 紙面證明，未假造未知原分量的圖。
- 三份保留 ownership 的 product relations：整側禁色 {0,2,3} σ-不變，
  逐份 tuple ownership 不封閉。沒有加入對稱閉包當成原 relation。
- 一份局部負控制有兩份 degree 四、各自 support={b₁,b₂} 的原模型：
  二接點 edge 的完整 relation={(2,3),(3,2)}、禁色 {2,3}、2 份 lifts；
  單接點雙 N triangles＋bridge 的完整 relation={(0)}、禁色 {0}、4 份 lifts。
  共 8 份完整聯合 lifts，整側禁色仍 {0,2,3}，卻與指定 join60 的逐份禁色不同。
  只用來顯示整側摘要遺失 ownership，不當成指定來源的替換。
- 負控制的兩條實際原 bridges、四 pins 下八份完整刪橋端點 relations、
  34 份完整同一刪邊模型 lifts 全部保存。單接點模型 z=0 的 dc 刪橋 relation
  恰為 {(1,1)}；保留完整兩 triangles 及附件，不拼接獨立端點 marginals。
- 一份刪 zw、取 z=w=1、保留 P₃=(3,0,3) 的 context partial witness，
  D_w 內點仍符號 fibre；原 zw 保存於邊資料，省邊在 witness 中明列。
  原 context 與控制給 z degree=5、P₃ degree=4；沒有聲稱 w 的未知內點被枚舉。
- 負控制中相鄰 N private e,f 與原外路給一份 K₅ minor；五袋連通、不交，
  十對原邊鄰接全部核對。它是非平面控制，不是 disk source、整份 M 的
  逐邊 minimality 或未知 D_w 的具體 relation 證書。

## 重播與實際驗證

```bash
python3 scripts/c5_mixed_p3_two_frame_two_unary.py
python3 scripts/c5_mixed_p3_two_frame_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_two_frame_two_unary.py --check
python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
python3 scripts/c5_mixed_p3_common_endpoint.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 生成、一般／seed=17 逐 byte 重播均通過，證書 49,886 bytes，
小於大型 manifest 門檻，沒有修改 manifest／ignore。C₃、C₂、common 前層
逐 byte 重播通過；原 common artifact 的 36／140／900 及 rotation 保持原 hash。
既有 Lean build 通過 8,831 jobs，保留既有 linter warnings；本輪未改 Lean，
沒有新增 theorem 或將 lift 雙射／拓撲控制形式化。
文件、DocGraph 及 diff 的最終核對數字於本紀錄末段保存。

未重跑：mixed capacity standalone、其餘 P₃ 對稱／非對稱／中點端點
standalone、no-mixed 十五類、singleton／K₂ 完成表、933／941 excess、
R 系列、atlas／profiles／閉包、Lean axiom audit 及 D₂–D₄ 全輪稽核。
沒有再搜尋新 graph catalogue，也沒有把前層 checker 的入口重算視為上述全表驗證。
沒有使用外部文獻定理；未重播 C₃ 的 Gallai 文獻本身。

## 停止點與貼上式交接

只新增固定 key **(CPP-134-1,34,60)** 的來源排除。原 C₂ key (30,20)、
C₃ key (34,20) 的證據及稽核快照保持，全部其他 joins 仍留在原表，
不登記整份 case、geometry35、root 交換型或同一 z 角色的其他 keys 完成。
目前精確入口見 [weak-deletion §3](../c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)。
更新報告、C₃ 頁首後續、weak-deletion guide、README／STATUS 及本紀錄。
HANDOFF 的研究線及 tag 未變，按文件治理不改其導覽清單。
工作樹原有未提交成果保留；本輪未 commit／push。

> 接續 C₄：CPP-134-1／geometry34／join60、side IDs=(27,1) 已來源排除。
> 原 P₃／附件／q=01012／外路／w ternary 未改。z 保留兩原 unary：
> D₂ contacts(u0,u1)、f{0,3}；D₁ contact(r0)、f{2}。
> 各自 own support⊆{b1,b2}，聯集恰{b1,b2}，九份必要配置全部保存。
> 只在一份原 unary 完整 lift 交換2↔3，保持全部內邊／bridges／附件／contact次序，
> 迫完整 relations 封閉；三份 binary 候選03/30及唯一singleton2都不封閉。
> 27份支援×完整relation必要組合、0survivor；任意大小紙面雙射，不需Gallai。
> 整側f{0,2,3}本身不變，不能抹去ownership或合成C₃一份ternary。
> degree4兩分量負控制的f{2,3}/{0}有相同整側禁色，保存完整lifts／兩bridges及原外路K5；
> 它非平面、不同ownership，不能替換原來源。0target，未Lean化，原36/140/900不刪。
> python3 scripts/c5_mixed_p3_two_frame_two_unary.py --check。

最終文件核對通過：536 份 Markdown／5,565 本地連結，anchors／直接索引／
HANDOFF 均通過；DocGraph 為 62 documents／213 relations／5 families，
0 errors、0 notes。`git diff --check` 通過；新建檔另作 whitespace 核對。
獨立 read-only 審閱核實完整 lift 雙射、所有必要配置、完整 fibres 及負控制，
沒有擴大完成 keys。原四份前層資料與開工時 hash 相同：

| 原資料 | 保持的 SHA256 |
| --- | --- |
| common-endpoint observations | `0f8cd30f22eae684f8b1691596d7ee83576c1f7d13052f01d878cda97ec73d8f` |
| common-endpoint rotations | `c02b4d6b578c6284bbb22c10ae247b111c258f19f557d231b0a79199eecb2ef4` |
| C₂ observations | `6e01211b2445219854b5fb361600e4e0a35bf0e4dd9707789d90036d1750435c` |
| C₃ observations | `4ad34a599bb07c501c80c23c2e0460f21ebd77808f8c498e08f4ec1c46d20784` |
