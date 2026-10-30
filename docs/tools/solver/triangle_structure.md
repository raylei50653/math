# 圓盤三角化：逐面編號與六例核對

2026-10-25。這是獨立的有限嵌入展示，保存六份明確原圖、面次序與編號；
不是圖枚舉，也不新增一般染色定理或 Lean 證明。
與[四色求解實驗](../four_color_guide.md)分開保存；不改變 C₅／W7 等研究停止點。

[互動展示](../../../artifacts/triangle_structure/triangle-numbering.html) ·
[完整原圖與編號](../../../artifacts/triangle_structure/examples.json) ·
[獨立 checker](../../../artifacts/triangle_structure/check_examples.py) ·
[有限驗證紀錄](../../../artifacts/triangle_structure/validation.json) ·
[歷史編號不變性紀錄](../../../artifacts/triangle_structure/numbering-validation.json)

## 嵌入與編號契約

每例是有限簡單圖的圓盤三角化，外界為簡單環；座標採右為 x 正向、上為 y 正向，
有界三角面與外界依逆時針列出。原頂點 ID 與幾何／面 incidence 一併保存，
不只保存抽象邊集合，也不從畫面線段相交自行推斷其他圖的平面性。

固定一條有向外界根邊及整體方向，從其左側有界面開始，按原面對偶作 BFS；
各面由進入邊開始依逆時針處理。頂點、無向邊、面各有獨立的 `v`／`e`／`f` 編號，
重遇同一原頂點或原邊時沿用既有編號，外面記作 `F∞`。
編號依賴根邊及嵌入方向，沒有聲稱是抽象圖的同構標準形式。

## 六份有限結果

染色數使用具名字面色，計算整張原圖的全部合法頂點染色，不把換色等價類或局部表列數混入。

| 原圖 ID | 點／邊／有界三角面 | 3 色染色數 | 4 色染色數 |
| --- | --- | ---: | ---: |
| `wheel6` | 7／12／6 | 6 | 264 |
| `wheel5` | 6／10／5 | 0 | 120 |
| `wheel7` | 8／14／7 | 0 | 504 |
| `k4` | 4／6／3 | 0 | 24 |
| `octahedron` | 6／12／7 | 6 | 96 |
| `octahedron-insert` | 7／15／9 | 0 | 96 |

checker 逐例核對面方向、共邊 incidence、內點 link 為環／界點 link 為路徑、幾何無交叉、
面積、Euler 與圓盤曲率和 6，再核對原 ID 對應、根邊、編號復用與對偶 BFS 層次。
染色數由原邊獨立窮舉；最後一例另保留三點 `a,b,c` 組成的非面三角環。
本次只讀重播六例全部通過，結果與保存的 `validation.json` 一致，輸入與 checker SHA-256 均吻合；
HTML 內嵌六圖的原資料亦與 `examples.json` 相同。

歷史 `numbering-validation.json` 記載 72 次來源 ID 改名、頂點／面順序及面循環起點擾動核對。
該檔沒有保存這 72 次測試的重播程式與來源 hash；本次六例 checker 核對不能冒充重新完成那 72 次測試。

## 只讀重播

以下命令呼叫 checker 的 `check()`，直接比對既有紀錄，不執行會覆寫 `validation.json` 的 `main()`：

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import runpy

base = Path('artifacts/triangle_structure')
saved = json.loads((base / 'validation.json').read_text())
data = json.loads((base / 'examples.json').read_text())
checker = runpy.run_path(str(base / 'check_examples.py'), run_name='readonly_check')
results = [checker['check'](graph) for graph in data['examples']]
assert results == saved['results']
for filename, field in [('examples.json', 'examples_sha256'),
                        ('check_examples.py', 'checker_sha256')]:
    assert hashlib.sha256((base / filename).read_bytes()).hexdigest() == saved[field]
print(f'PASS: {len(results)} examples; saved results and hashes match')
PY
```

直接執行 `python3 artifacts/triangle_structure/check_examples.py` 則會重建並覆寫驗證紀錄；
它是產生器入口，不是只讀命令。

## 外部來源與停止邊界

[Glen，Theorem 3](https://arxiv.org/html/1605.01688v4)給出 near-triangulation 的內點全偶度
與可 3 染之等價；六例只獨立檢查各自符合這個外部定理，沒有從六例推出一般敘述。
[plantri 原始使用手冊](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)
說明平面嵌入須保留各點的邊循環次序，以及圓盤三角化的生成接口；本展示不是 plantri 的完整生成結果。
上述來源已於 2026-10-25 對回原文。

目前完成的是六份明確資料的展示與有限核對；任意嵌入輸入、一般編號器、
72 次歷史不變性測試的可重播性及更大圖類的驗證，均不在這份證書的涵蓋範圍。
