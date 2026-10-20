# B 獨立重播與交叉審查

B 的完整局部編譯器重播通過：5120 份全指派、P 的 312／R 的 240 份 proper 指派、
每操作 240 份 proper 目標字面外框及每份十個完整來源 fibre（含空者）。
200 格整數矩陣、2048 次形式 mask 轉移、264 條來源轉移均一致；四項污染拒絕。

普通 `--check` 及從 `/tmp` 使用 `PYTHONHASHSEED=17` 的 `--check` 均逐位元組通過。
已存在證書時再次 `--write` 會拒絕，並核對編譯器與證書的雜湊未改變。

固定輸出：

- `check_local_operators.py` SHA-256：`d742430591bd59407f5a4b191420c4370ff409d5afe983a449122baf40984e6c`
- `certificate.json` SHA-256：`c24e86ed7dda5d274a344823955bbf32e05030d3a0d5419d9201b1796e58c573`

A 獨立讀取 B 的圖編譯及完整 fibre／色置換邏輯，重播 `--check`，沒有實質發現。
唯一措辭建議是將 docstring 的「colour 4」改為「fourth colour」；已修正並重新產生證書，
上述雜湊及兩次重播均為修正後版本。

B 另獨立審查 C 的 `check_full_graph.py`，並重播 `--check`：

- `make_disk` 不讀矩陣，保留全部舊邊，附加三邊及兩個定向三角面，P/R/F/C 與 B 一致。
- 驗證器檢查連通、每邊的定向面 incidence、每點 link 為路徑／圈，以及 Euler 特徵 1；
  連同單一簡單五邊形外框，給出連通定向 disk cellulation。
- `full_fibre` 在同一字面外框上保留所有內點指派，空 fibre 是空陣列；與矩陣預測分開計算。
- 792 個圖案例、7920 份 canonical 字面完整 fibres、10642 份全著色、
  80 份獨立 Cartesian-product fibre 核對與七項控制均通過。

C 審查時證書 SHA-256：`e426653ac4a047c9e21175c215a7ef0e5025fbd812bab4c327282cbba613e321`。
沒有實質發現。C 的有限全圖重播與 B 的局部編譯互相支持；任意 disk 的普遍結論仍須引用 A 的
同一完整 fibre 雙射證明，而一般 disk 的 F/C 文法來源覆蓋仍 OPEN。
