#!/usr/bin/env python3
"""Deterministic, dependency-free views of the generated C5 atlas.

The mathematical data belongs to c5_combinatorial_atlas.py and its inputs.
Call ``render(atlas)`` and write the returned filenames and text verbatim.
This module never reads or modifies an existing witness or proof artifact.
"""

from __future__ import annotations

import html
import json
from collections import Counter


STATUS = {
    "kempe_rejected": ("Kempe 必要條件排除", "#b64a4a"),
    "exterior_rejected": ("外部接合必要條件排除", "#cb8b26"),
    "realized": ("已有 disk witness", "#257c67"),
    "open": ("候選 · OPEN", "#5464bd"),
}


def _compact(atlas: dict) -> dict:
    """Keep all display evidence and raw labels, but omit unused large fields."""
    class_keys = (
        "canonical", "orbit_members", "orbit_size", "stabilizer", "allowed_bits",
        "forbidden_bits", "three_count", "four_count", "status", "features",
        "minimum_known_inner_vertices", "witnesses", "screens", "evidence",
        "nearest_known_masks", "aligned_immediate_subsets", "aligned_immediate_supersets",
    )
    mask_keys = (
        "mask", "canonical", "to_canonical", "kempe_failure",
        "exterior_disjoint_witness", "status", "separating_witness",
    )
    return {
        "summary": atlas["summary"],
        "orbit_size_histogram": atlas["orbit_size_histogram"],
        "patterns": atlas["patterns"],
        "group": atlas["group"],
        "classes": [{k: c[k] for k in class_keys if k in c}
                    for c in atlas["classes"]],
        "labelled_masks": [{k: row[k] for k in mask_keys if k in row}
                           for row in atlas["labelled_masks"]],
    }


def _svg(atlas: dict) -> str:
    s = atlas["summary"]
    classes = atlas["classes"]
    rows = atlas["labelled_masks"]
    count = Counter(c["status"] for c in classes)
    opens = [c for c in classes if c["status"] == "open"]
    esc = html.escape
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="970" '
           'viewBox="0 0 1200 970" role="img" aria-labelledby="title description">',
           '<title id="title">C5 邊界染色關係分類圖譜</title>',
           '<desc id="description">由 atlas 資料產生的組合、對稱、必要條件、'
           '實現狀態與候選結構總覽。必要條件通過並不表示 disk 實現。</desc>',
           '<style>text{font-family:system-ui,sans-serif;fill:#172c37}'
           '.h{font-size:23px;font-weight:700}.t{font-size:16px}'
           '.small{font-size:13px}.num{font-size:31px;font-weight:700}'
           '.box{fill:#fff;stroke:#c9d6dc;rx:12}.line{stroke:#5c7480;stroke-width:2;fill:none}'
           '</style>',
           '<rect width="1200" height="970" fill="#f1f5f5"/>',
           '<text x="32" y="43" class="h">C5 邊界四色染色：可重播分類圖譜</text>',
           '<text x="32" y="70" class="t">原始帶標號 Σ 保留；D5 canonical 僅供分類與導航。</text>']

    def text(x: int, y: int, value: object, cls: str = "t") -> None:
        out.append(f'<text x="{x}" y="{y}" class="{cls}">{esc(str(value))}</text>')

    def rect(x: int, y: int, w: int, h: int) -> None:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="box"/>')

    rect(24, 91, 558, 295)
    text(42, 122, "1 · Combination Map", "h")
    text(42, 149, f'{s["proper_colourings"]} proper colourings → '
         f'{s["s4_orbits"]} S4 模式 → {s["nonempty_masks"]} 非空 masks')
    # Every rectangle corresponds to one labelled relation, in increasing order.
    cols, cell = 55, 9
    for index, row in enumerate(sorted(rows, key=lambda r: r["mask"])):
        color = STATUS[row["status"]][1]
        x, y = 42 + (index % cols) * cell, 170 + (index // cols) * cell
        out.append(f'<rect x="{x}" y="{y}" width="7" height="7" fill="{color}">'
                   f'<title>Σ={row["mask"]}; canonical={row["canonical"]}; '
                   f'{esc(STATUS[row["status"]][0])}</title></rect>')
    text(42, 361, f'{s["nonempty_masks"]} 個原始 Σ → {s["d5_orbits"]} 個 D5 等價類')

    rect(596, 91, 580, 295)
    text(614, 122, "2 · Symmetry Map", "h")
    text(614, 151, "S4：顏色重命名。D5：整份邊界旋轉／鏡射。")
    text(638, 179, "orbit size", "small")
    text(780, 179, "類數", "small")
    text(902, 179, "stabilizer size", "small")
    for i, (size, amount) in enumerate(sorted(atlas["orbit_size_histogram"].items(),
                                             key=lambda x: int(x[0]))):
        text(638, 211 + i * 30, size)
        text(780, 211 + i * 30, amount)
        text(902, 211 + i * 30, len(atlas["group"]) // int(size))
    text(614, 304, "canonical = 同一 orbit 中最小的十進位 mask")
    for i, g in enumerate([g for g in atlas["group"] if g["name"] in ("r1s0", "r0s1")]):
        text(614, 332 + 23 * i, f'{g["name"]}: bit → {g["bit_permutation"]}', "small")

    rect(24, 403, 1152, 238)
    text(42, 435, "3 · Screening Map", "h")
    steps = [(45, s["nonempty_masks"], "非空 masks"),
             (314, s["kempe_masks"], "Kempe 必要條件通過"),
             (630, s["screened_masks"], "外部必要條件亦通過")]
    for x, n, label in steps:
        text(x, 489, n, "num")
        text(x, 518, label)
    for x, key in [(45, "d5_orbits"), (314, "kempe_orbits"), (630, "screened_orbits")]:
        text(x, 546, f'{s[key]} 個 D5 類', "small")
    out += ['<path d="M170 483H292m-9-6 9 6-9 6" class="line"/>',
            '<path d="M496 483H608m-9-6 9 6-9 6" class="line"/>',
            '<path d="M850 483H886V459H923M886 483V546H923" class="line"/>']
    text(932, 469, f'{s["known_masks"]} 已知實現', "h")
    text(932, 554, f'{s["screened_masks"] - s["known_masks"]} 候選 OPEN', "h")
    text(45, 575, f'排除 {s["nonempty_masks"] - s["kempe_masks"]}', "small")
    text(314, 575, f'再排除 {s["kempe_masks"] - s["screened_masks"]}', "small")
    text(45, 612, "最後分支是證據狀態分類；必要條件通過不等於存在單側 disk。")

    rect(24, 658, 558, 218)
    text(42, 691, "4 · Realization Map", "h")
    text(42, 727, f'{s["known_orbits"]} 已知 disk 類；{s["open_orbits"]} 候選類')
    for i, status in enumerate(STATUS):
        out.append(f'<rect x="42" y="{748 + i * 26}" width="12" height="12" '
                   f'fill="{STATUS[status][1]}"/>')
        text(65, 759 + i * 26, f'{STATUS[status][0]}：{count[status]} 類', "small")

    rect(596, 658, 580, 218)
    text(614, 691, "5 · Structure Comparison", "h")
    for i, c in enumerate(opens):
        y = 728 + i * 66
        text(614, y, f'候選 Σ={c["canonical"]}；orbit={c["orbit_size"]}；'
             f'三色／四色={c["three_count"]}/{c["four_count"]}')
        text(614, y + 25, f'允許 bits={c["allowed_bits"]}；已知 disk witness：無', "small")
        text(614, y + 47, f'singleton={c["features"]["singleton_support"]}；'
             f'全部四色={c["features"]["all_four"]}；'
             f'chord={c["features"]["chord_compatible_pairs"]}', "small")
    text(32, 909, "詳細資料：index.html 可選取每個原始 mask、完整 orbit、置換與 witness。", "t")
    text(32, 936, "separating C5 兩側的對齊交集與單側 disk relation 分開記錄；K∞ = K≤5 保持 OPEN。", "small")
    out.append('</svg>')
    return "\n".join(out) + "\n"


HTML = r'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>C5 組合與結構分類圖譜</title>
<style>
:root{font-family:system-ui,sans-serif;color:#172c37;background:#f1f5f5;line-height:1.55;color-scheme:light}*{box-sizing:border-box}body{max-width:1320px;margin:0 auto;padding:24px}h1{font-size:28px;margin:0 0 6px}h2{font-size:22px;margin:0 0 12px}h3{font-size:17px;margin:14px 0 8px}p{margin:8px 0}a{color:#335da8}nav{display:flex;gap:16px;flex-wrap:wrap;margin:20px 0}section,.panel{background:white;border:1px solid #ccd9de;border-radius:12px;padding:20px;margin-bottom:20px}.tiles{display:flex;gap:12px;flex-wrap:wrap}.tile{padding:12px 16px;border-left:4px solid #668b9c;min-width:155px;background:#f5f8fa}.tile b{display:block;font-size:26px}.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px}.muted,.small{color:#526974;font-size:13px}.note{padding:10px 14px;background:#eaf1f5;border-radius:6px}input,select,button{font:inherit;border:1px solid #aebfc8;border-radius:5px;padding:5px 9px;background:white;color:inherit}button{cursor:pointer}button:hover,button:focus{background:#eaf1f5}button.active{border:2px solid #203c4a;background:#e6edf1}.controls{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:12px 0}.chips{display:flex;gap:6px;flex-wrap:wrap}.chips button{font-family:ui-monospace,monospace;font-size:13px}.status{white-space:nowrap}.dot{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px}.tablewrap{overflow:auto;max-height:560px;border:1px solid #dce5e8}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #e4ebee;white-space:nowrap}th{position:sticky;top:0;background:#f3f7f9;z-index:1}th button{border:0;padding:0;background:none;font-weight:700}.feature-table{table-layout:fixed}.feature-table td{white-space:normal;overflow-wrap:anywhere}.feature-table td:first-child{width:42%}.feature-table summary{cursor:pointer}tr.selectable{cursor:pointer}tr.selectable:hover{background:#eef5f8}tr.selected{background:#e3edf2}.pattern-grid{display:grid;grid-template-columns:repeat(5,minmax(105px,1fr));gap:10px}.pattern{padding:8px;background:#f7f9fa;border:1px solid #dce5e8;border-radius:7px;text-align:center}.pattern svg{width:100%;height:125px}.pattern.blocked{opacity:.48}.pattern strong{font-family:ui-monospace,monospace}.pattern em{font-size:12px;font-style:normal}.gridwrap{max-width:660px}canvas{display:block;width:100%;image-rendering:auto;border:1px solid #dce5e8;touch-action:manipulation}.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;margin:10px 0}.mono{font-family:ui-monospace,monospace;overflow-wrap:anywhere}.graph{width:100%;max-width:440px;height:340px}.screen{width:100%;min-width:850px;height:245px}.wide{overflow:auto}ul{padding-left:22px}.evidence li{font-size:13px}.nowrap{white-space:nowrap}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}#classcount{margin-left:auto}@media(max-width:850px){body{padding:12px}.two{grid-template-columns:1fr}.pattern-grid{grid-template-columns:repeat(2,minmax(110px,1fr))}h1{font-size:24px}.screen{height:220px}}
</style></head><body>
<header><h1>C5 組合、對稱與結構分類圖譜</h1><p>從完整合法邊界模式重新分類。全部資料內嵌，開啟本檔即可操作。</p>
<p class="note">帶標號 Σ 與原 bit index 原樣保留。D5 canonical 用於分類；接合前仍須搬運整份邊界與實際附件。必要條件通過只代表候選。</p><div id="summary" class="tiles"></div></header>
<nav aria-label="圖譜導覽"><a href="#combination">Combination</a><a href="#symmetry">Symmetry</a><a href="#screening">Screening</a><a href="#realization">Realization</a><a href="#structure">Structure</a></nav>
<section id="combination"><h2>1 · Combination Map</h2><p id="combination-text"></p><div class="two"><div class="gridwrap"><div id="legend" class="legend"></div><canvas id="maskgrid" width="660" height="620" tabindex="0" aria-label="全部非空帶標號 mask；點選方格或使用右側 mask 輸入選取"></canvas><p class="small">依十進位 Σ 由左至右、由上至下。深色框標出所選 orbit；白色框標出所選原始 Σ。鍵盤方向鍵可移動。</p></div><div><div class="controls"><label for="mask">原始 Σ</label><input id="mask" type="number" min="1" max="1023" value="1" style="width:110px"><button id="selectmask">選取</button><span id="inputerror" role="status"></span></div><div id="selected-summary"></div><h3>完整 orbit members</h3><div id="members" class="chips"></div><h3>orbit size 分布</h3><div id="histogram"></div><p class="note">同一 orbit 中的關係以 D5 等價；各 member 的邊界頂點與接合座標仍有區別。</p><h3>separating C5 兩側對齊交集</h3><div id="separating"></div></div></div></section>
<section id="symmetry"><h2>2 · Symmetry Map</h2><p>S4 先將顏色名稱正規化，D5 再對邊界頂點作用。下表列完整 bit 置換；來源座標與 canonical 轉換皆可核對。</p><div class="controls"><label for="group">所選原始 Σ 的 D5 搬運</label><select id="group"></select><div id="transport"></div></div><div class="tablewrap"><table id="group-table"></table></div><h3>bit index 與合法模式</h3><div id="patterns" class="pattern-grid"></div><p class="small">word 使用既有 S4 正規化字母；b0…b4 是帶標號邊界位置。虛線連結 word 中同色的位置。</p></section>
<section id="screening"><h2>3 · Screening Map</h2><div id="screen-chart" class="wide"></div><p class="note">最後一步將必要條件通過者分成已有證據與 OPEN，並非另一次不可實現性篩選。單側 disk 與兩側對齊交集的實現語義分開記錄。</p></section>
<section id="realization"><h2>4 · Realization Map</h2><p id="realization-text"></p><div class="two"><div><h3>已有單側 disk witness 的 D5 類</h3><div class="tablewrap"><table id="known-table"></table></div></div><div><h3>剩餘候選 D5 類</h3><div id="open-cards"></div><p class="note">候選的描述性特徵可提出研究假說；相似特徵本身不提供一般可實現性判準。K∞ = K≤5 保持 OPEN。</p></div></div></section>
<section id="structure"><h2>5 · Structure Comparison</h2><div class="controls"><label for="statusfilter">狀態</label><select id="statusfilter"><option value="all">全部</option></select><label for="threefilter">三色數</label><select id="threefilter"><option value="all">全部</option></select><label for="fourfilter">四色數</label><select id="fourfilter"><option value="all">全部</option></select><label for="query">搜尋 Σ／word／bit</label><input id="query" placeholder="如 933、01202、bit:0"><span id="classcount" class="small"></span></div><div class="tablewrap"><table id="class-table"></table></div><p class="small">點選列進入 canonical frame；再選 orbit member 可檢查原始帶標號 frame。</p><div id="detail"></div></section>
<footer class="small"><p>資料来源：本目錄 atlas.json。此檔與 overview.svg 由同一分類資料自動產生；圖示並非另一份數學真相來源。內點數是現有目錄的最小已知值。</p></footer>
<script id="atlas-data" type="application/json">__ATLAS_DATA__</script>
<script>
"use strict";
const A=JSON.parse(document.getElementById('atlas-data').textContent), S=A.summary;
const statusInfo={kempe_rejected:['Kempe 排除','#b64a4a'],exterior_rejected:['外部必要條件排除','#cb8b26'],realized:['已有 disk witness','#257c67'],open:['候選 · OPEN','#5464bd']};
const C=new Map(A.classes.map(c=>[c.canonical,c])), M=new Map(A.labelled_masks.map(m=>[m.mask,m]));
const el=id=>document.getElementById(id), esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const json=x=>esc(JSON.stringify(x)), bitword=m=>m.toString(2).padStart(A.patterns.length,'0'), bits=m=>A.patterns.filter(p=>m&(1<<p.bit)).map(p=>p.bit);
const statusBadge=s=>'<span class="status"><span class="dot" style="background:'+statusInfo[s][1]+'"></span>'+statusInfo[s][0]+'</span>';
let selected=A.classes.find(c=>c.status==='open')?.canonical||1, sortKey='canonical', sortAscending=true;
const pairsText=p=>(p||[]).map(v=>'b'+v[0]+'–b'+v[1]).join(', ')||'無';
function makePattern(p,active=true){
const colours=['#e9965c','#6c9eda','#83b98b','#b891c8'];
const points=Array.from({length:5},(_,i)=>[65+45*Math.cos(-Math.PI/2+i*2*Math.PI/5),61+45*Math.sin(-Math.PI/2+i*2*Math.PI/5)]);
let v='<svg viewBox="0 0 130 125" role="img" aria-label="bit '+p.bit+'，模式 '+esc(p.word)+'">';
for(let i=0;i<5;i++){let a=points[i],b=points[(i+1)%5];v+='<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="#8195a0"/>'}
for(const [i,j]of(p.equal_pairs||[])){let a=points[i],b=points[j];v+='<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="#627987" stroke-dasharray="3,3"/>'}
points.forEach((q,i)=>{v+='<circle cx="'+q[0]+'" cy="'+q[1]+'" r="11" fill="'+colours[Number(p.word[i])]+'" stroke="#263e4c"/><text x="'+q[0]+'" y="'+(q[1]+4)+'" text-anchor="middle" font-size="11">'+esc(p.word[i])+'</text><text x="'+(65+(q[0]-65)*1.29)+'" y="'+(61+(q[1]-61)*1.29+4)+'" text-anchor="middle" font-size="10">b'+i+'</text>'});
return '<div class="pattern'+(active?'':' blocked')+'">'+v+'</svg><strong>bit '+p.bit+' · '+esc(p.word)+'</strong><br><em>'+p.colours+' 色'+(p.singleton===null?'':' · singleton b'+p.singleton)+'</em></div>';
}
function transport(m,g){return bits(m).reduce((v,b)=>v|(1<<g.bit_permutation[b]),0)}
function showTransport(){const g=A.group.find(g=>g.name===el('group').value), target=transport(selected,g);el('transport').innerHTML='<span class="mono">Σ'+selected+' → Σ'+target+'</span> <button data-mask="'+target+'">查看搬運後原始 Σ</button>';bindMaskButtons(el('transport'))}
function bindMaskButtons(root){root.querySelectorAll('[data-mask]').forEach(b=>b.onclick=()=>select(Number(b.dataset.mask)))}
function drawGrid(){const canvas=el('maskgrid'),ctx=canvas.getContext('2d'),c=C.get(M.get(selected).canonical),orbit=new Set(c.orbit_members);ctx.clearRect(0,0,canvas.width,canvas.height);for(const m of A.labelled_masks){const i=m.mask-1,x=(i%33)*20,y=Math.floor(i/33)*20;ctx.fillStyle=statusInfo[m.status][1];ctx.fillRect(x+2,y+2,16,16);if(orbit.has(m.mask)){ctx.strokeStyle='#152e3b';ctx.lineWidth=2;ctx.strokeRect(x+1,y+1,18,18)}if(m.mask===selected){ctx.strokeStyle='white';ctx.lineWidth=2;ctx.strokeRect(x+5,y+5,10,10)}}}
function graph(w){
if(!w||!Array.isArray(w.edges))return '<p class="small">此記錄未內嵌可畫出的原邊集合；請開啟證據來源。</p>';
const ids=[...new Set([0,1,2,3,4,...w.edges.filter(e=>Array.isArray(e)).flat()])].sort((a,b)=>a-b),inner=ids.filter(i=>i>=5),points={};ids.forEach(i=>{const k=inner.indexOf(i),radius=inner.length===1?0:57;points[i]=i<5?[210+126*Math.cos(-Math.PI/2+i*2*Math.PI/5),160+126*Math.sin(-Math.PI/2+i*2*Math.PI/5)]:[210+radius*Math.cos(-Math.PI/2+k*2*Math.PI/inner.length),160+radius*Math.sin(-Math.PI/2+k*2*Math.PI/inner.length)]});
let v='<svg class="graph" viewBox="0 0 420 340" role="img" aria-label="Σ'+w.mask+' witness 原邊集合示意">';
for(const e of w.edges){if(!Array.isArray(e)||e.length!==2||!points[e[0]]||!points[e[1]])continue;const[a,b]=e.map(i=>points[i]),boundary=e[0]<5&&e[1]<5,cycle=boundary&&((Math.abs(e[0]-e[1])===1)||Math.abs(e[0]-e[1])===4),stroke=cycle?'#67818d':boundary?'#9871b6':e[0]<5||e[1]<5?'#ca8151':'#2e4f5e';v+='<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+stroke+'" stroke-width="'+(cycle?3:2)+'"/>'}
ids.forEach(i=>{const p=points[i];v+='<circle cx="'+p[0]+'" cy="'+p[1]+'" r="14" fill="'+(i<5?'#e4eef2':'#fff0dd')+'" stroke="#2e4f5e"/><text x="'+p[0]+'" y="'+(p[1]+4)+'" text-anchor="middle" font-size="12">'+(i<5?'b'+i:'v'+i)+'</text>'});return v+'</svg><p class="small">原邊集合示意；圖上位置不代表平面 embedding。邊界／chord／附件／內邊分色。</p>';
}
function sourceLink(path){return /^(docs|artifacts|scripts|audits)\//.test(path)?'<a href="../../'+esc(encodeURI(path))+'">'+esc(path)+'</a>':esc(path)}
function featureTable(f){const names={singleton_support:'三色 singleton 位置',singleton_adjacent_edges:'singleton 相鄰邊',singleton_pair_distances:'singleton 位置對的環距離',all_four:'包含全部四色模式',forced_equal_pairs:'非相鄰點共同強迫同色',forced_unequal_pairs:'非相鄰點共同強迫異色',chord_compatible_pairs:'相容 chord 位置對',minimum_projection_arity:'最小投影重建階數',nearest_known_masks:'最近已知關係（bit 差距）',aligned_immediate_subsets:'對齊直接子關係',aligned_immediate_supersets:'對齊直接超關係',known_subsets:'目錄內的子關係',known_supersets:'目錄內的超關係'};const order=['singleton_support','singleton_pair_distances','singleton_adjacent_edges','all_four','minimum_projection_arity','forced_equal_pairs','forced_unequal_pairs','chord_compatible_pairs','nearest_known_masks','aligned_immediate_subsets','aligned_immediate_supersets','known_subsets','known_supersets'];return '<table class="feature-table"><tbody>'+Object.entries(f||{}).sort(([a],[b])=>order.indexOf(a)-order.indexOf(b)).map(([k,v])=>{let value=k.endsWith('_pairs')?pairsText(v):json(v);if(Array.isArray(v)&&v.length>12)value='<details><summary>'+v.length+' 個；展開</summary>'+value+'</details>';return '<tr><td>'+esc(names[k]||k)+'</td><td class="mono">'+value+'</td></tr>'}).join('')+'</tbody></table>'}
function rawFeatures(m){const ps=A.patterns.filter(p=>m&(1<<p.bit)),same=[],diff=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){if(ps.every(p=>p.word[i]===p.word[j]))same.push([i,j]);if(ps.every(p=>p.word[i]!==p.word[j]))diff.push([i,j])}return {same,diff,singletons:[...new Set(ps.map(p=>p.singleton).filter(x=>x!==null))].sort((a,b)=>a-b)}}
function select(m){
if(!Number.isInteger(m)||!M.has(m)){el('inputerror').textContent='請輸入 1…'+S.nonempty_masks+' 的整數';return}selected=m;el('inputerror').textContent='';el('mask').value=m;const row=M.get(m),c=C.get(row.canonical),f=rawFeatures(m);
el('selected-summary').innerHTML='<h3>原始 Σ='+m+' <span class="mono">'+bitword(m)+'</span></h3><p>'+statusBadge(c.status)+'</p><p>canonical Σ='+c.canonical+'；orbit size='+c.orbit_size+'；stabilizer size='+c.stabilizer.length+'</p><p>到 canonical 的全部群元素：<span class="mono">'+esc(row.to_canonical.join(', '))+'</span></p>';
el('members').innerHTML=c.orbit_members.map(x=>'<button class="'+(x===m?'active':'')+'" data-mask="'+x+'">Σ'+x+'</button>').join('');bindMaskButtons(el('members'));
const sw=row.separating_witness;el('separating').innerHTML=sw?'<p class="mono">'+json(sw)+'</p><p class="small">這是兩側關係對齊後的交集證據；不將它當成單側 disk witness。</p>':'<p>無內嵌接合證據。</p>';
const w=(c.witnesses||[]).find(w=>w.mask===m), inner=c.minimum_known_inner_vertices;
let detail='<h3>所選原始 Σ='+m+' 的限制模式與原邊證據</h3><p>允許 bits：<span class="mono">'+bits(m).join(', ')+'</span>；禁止 bits：<span class="mono">'+A.patterns.filter(p=>!(m&(1<<p.bit))).map(p=>p.bit).join(', ')+'</span></p><div class="pattern-grid">'+A.patterns.map(p=>makePattern(p,!!(m&(1<<p.bit)))).join('')+'</div><div class="two"><div><h3>所選帶標號 frame 的共同限制</h3><p>強迫同色：'+pairsText(f.same)+'<br>強迫異色：'+pairsText(f.diff)+'<br>三色 singleton 位置：'+(f.singletons.map(x=>'b'+x).join(', ')||'無')+'</p><h3>canonical frame 的分類特徵</h3>'+featureTable(c.features)+'<p>穩定子：<span class="mono">'+esc(c.stabilizer.join(', '))+'</span></p><p>Kempe：'+(c.screens.kempe?'通過':'未通過')+'；exterior：'+(c.screens.exterior?'通過':'未通過')+'</p>';
for(const k of ['nearest_known_masks','aligned_immediate_subsets','aligned_immediate_supersets'])if(c[k]!==undefined)detail+=featureTable({[k]:c[k]});
if(row.kempe_failure)detail+='<p>Kempe 拒絕證據：<span class="mono">'+json(row.kempe_failure)+'</span></p>';
if(row.exterior_disjoint_witness!==null&&row.exterior_disjoint_witness!==undefined)detail+='<p>外部不交關係：Σ'+row.exterior_disjoint_witness+'</p>';
detail+='<h3>分類證據來源</h3><ul class="evidence">'+(c.evidence||[]).map(path=>'<li>'+sourceLink(path)+'</li>').join('')+'</ul></div><div><h3>單側 disk witness</h3><p>'+statusBadge(c.status)+'；最小已知內點：'+(inner===null?'無已知 witness':inner)+'</p>';
if(w)detail+='<p>原始 Σ='+w.mask+'；'+w.inner_vertices+' 內點；來源：'+sourceLink(w.source)+'</p>'+graph(w)+'<p class="mono small">chords='+json(w.chords)+'<br>attachments='+json(w.attachments)+'<br>interior components='+json(w.interior_components)+'<br>interior degree sequence='+json(w.interior_degree_sequence)+'</p>'+(w.interior_skeleton_key?'<p class="small">此份 witness 的內圖同構 key：<span class="mono">'+esc(w.interior_skeleton_key)+'</span>。僅描述私人內圖；不包含邊界附件，也不斷言同一關係只能由此形狀實現。</p>':'');
else detail+='<p>這個原始 Σ 沒有內嵌單側 disk witness。OPEN 僅表示已通過必要條件。</p>';
detail+='</div></div><p class="note">包含、交集、聯集及共同限制都是關係本身的描述。兩側交集、目錄內的聯集證據與一般 disk 實現是不同敘述，不能由此圖直接互相推論。</p>';
el('detail').innerHTML=detail;drawGrid();showTransport();document.querySelectorAll('#class-table tr[data-mask]').forEach(r=>r.classList.toggle('selected',Number(r.dataset.mask)===c.canonical));
}
function renderClassTable(){const query=el('query').value.trim(),filter=el('statusfilter').value;let rows=A.classes.filter(c=>(filter==='all'||c.status===filter)&&(el('threefilter').value==='all'||c.three_count===Number(el('threefilter').value))&&(el('fourfilter').value==='all'||c.four_count===Number(el('fourfilter').value)));if(query){if(/^\d+$/.test(query)){const m=Number(query);rows=rows.filter(c=>c.canonical===m||c.orbit_members.includes(m))}else if(/^bit:\d+$/.test(query)){const b=Number(query.slice(4));rows=rows.filter(c=>c.allowed_bits.includes(b))}else rows=rows.filter(c=>c.allowed_bits.some(b=>A.patterns[b].word.includes(query))||JSON.stringify(c.features).includes(query))}rows.sort((a,b)=>{let av=a[sortKey],bv=b[sortKey];if(av===null)av=Infinity;if(bv===null)bv=Infinity;return(typeof av==='string'?av.localeCompare(bv):av-bv)*(sortAscending?1:-1)});el('classcount').textContent=rows.length+' / '+A.classes.length+' 類';const heads=[['canonical','canonical Σ'],['orbit_size','orbit size'],['three_count','三色數'],['four_count','四色數'],['status','狀態'],['minimum_known_inner_vertices','最小已知內點']];el('class-table').innerHTML='<thead><tr>'+heads.map(([k,v])=>'<th><button data-sort="'+k+'">'+v+(sortKey===k?(sortAscending?' ↑':' ↓'):'')+'</button></th>').join('')+'<th>允許 bits</th><th>stabilizer</th></tr></thead><tbody>'+rows.map(c=>'<tr class="selectable'+(c.canonical===M.get(selected).canonical?' selected':'')+'" data-mask="'+c.canonical+'"><td class="mono">'+c.canonical+'</td><td>'+c.orbit_size+'</td><td>'+c.three_count+'</td><td>'+c.four_count+'</td><td>'+statusBadge(c.status)+'</td><td>'+(c.minimum_known_inner_vertices??'—')+'</td><td class="mono">'+c.allowed_bits.join(',')+'</td><td class="mono">'+c.stabilizer.join(',')+'</td></tr>').join('')+'</tbody>';bindMaskButtons(el('class-table'));el('class-table').querySelectorAll('[data-sort]').forEach(b=>b.onclick=()=>{if(sortKey===b.dataset.sort)sortAscending=!sortAscending;else{sortKey=b.dataset.sort;sortAscending=true}renderClassTable()})}
function setup(){
const tiles=[['proper_colourings','proper colourings'],['s4_orbits','S4 模式'],['nonempty_masks','非空帶標號 masks'],['d5_orbits','D5 類'],['known_orbits','已有 disk 類'],['open_orbits','OPEN 類']];el('summary').innerHTML=tiles.map(([k,v])=>'<div class="tile"><b>'+S[k]+'</b>'+v+'</div>').join('');
el('combination-text').textContent=S.all_masks+' 個十進位 masks 含空集合；'+S.nonempty_masks+' 個非空 masks 恰好分成 '+S.d5_orbits+' 個 D5 orbits。下圖每格保留一個原始帶標號 Σ。';
el('legend').innerHTML=Object.keys(statusInfo).map(statusBadge).join('');el('histogram').innerHTML='<table><thead><tr><th>orbit size</th><th>類數</th><th>stabilizer size</th></tr></thead><tbody>'+Object.entries(A.orbit_size_histogram).map(([n,v])=>'<tr><td>'+n+'</td><td>'+v+'</td><td>'+A.group.length/Number(n)+'</td></tr>').join('')+'</tbody></table>';
el('group').innerHTML=A.group.map(g=>'<option value="'+g.name+'">'+g.name+'</option>').join('');el('group').onchange=showTransport;
el('group-table').innerHTML='<thead><tr><th>D5 元素</th><th>輸出 b0…b4 的來源 index</th>'+A.patterns.map(p=>'<th>bit '+p.bit+' →</th>').join('')+'</tr></thead><tbody>'+A.group.map(g=>'<tr><td class="mono">'+esc(g.name)+'</td><td class="mono">'+g.source_indices.join(', ')+'</td>'+g.bit_permutation.map(b=>'<td>'+b+'</td>').join('')+'</tr>').join('')+'</tbody>';
el('patterns').innerHTML=A.patterns.map(p=>makePattern(p)).join('');
el('screen-chart').innerHTML='<svg class="screen" viewBox="0 0 1120 245" role="img" aria-label="必要條件篩選與證據狀態分支"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#64818e"/></marker></defs><g font-family="system-ui,sans-serif" fill="#18353f"><g font-size="34" font-weight="700"><text x="35" y="97">'+S.nonempty_masks+'</text><text x="310" y="97">'+S.kempe_masks+'</text><text x="610" y="97">'+S.screened_masks+'</text></g><g font-size="16"><text x="35" y="126">非空 masks</text><text x="310" y="126">Kempe 必要條件</text><text x="610" y="126">外部接合必要條件</text><text x="35" y="151">'+S.d5_orbits+' 個 D5 類</text><text x="310" y="151">'+S.kempe_orbits+' 個 D5 類</text><text x="610" y="151">'+S.screened_orbits+' 個 D5 類</text><text x="35" y="183">排除 '+(S.nonempty_masks-S.kempe_masks)+'</text><text x="310" y="183">再排除 '+(S.kempe_masks-S.screened_masks)+'</text><text x="902" y="69" fill="'+statusInfo.realized[1]+'">'+S.known_masks+' 已知 disk 關係</text><text x="902" y="91">'+S.known_orbits+' 個 D5 類</text><text x="902" y="166" fill="'+statusInfo.open[1]+'">'+(S.screened_masks-S.known_masks)+' 候選 · OPEN</text><text x="902" y="188">'+S.open_orbits+' 個 D5 類</text></g><g fill="none" stroke="#64818e" stroke-width="2" marker-end="url(#arrow)"><path d="M145 90H275"/><path d="M440 90H575"/><path d="M775 90H842V63H888"/><path d="M842 90V160H888"/></g><text x="35" y="229" font-size="14">必要條件通過 ≠ 已實現；最後分支記錄證據狀態。</text></g></svg>';
const known=A.classes.filter(c=>c.status==='realized'),open=A.classes.filter(c=>c.status==='open');el('realization-text').textContent=S.known_masks+' 個帶標號既有關係覆蓋 '+known.length+' 個 D5 類。以下內點数是原目錄的最小已知值，不主張一般下界。';
el('known-table').innerHTML='<thead><tr><th>canonical Σ</th><th>orbit size</th><th>三色／四色</th><th>最小已知內點</th></tr></thead><tbody>'+known.map(c=>'<tr class="selectable" data-mask="'+c.canonical+'"><td>'+c.canonical+'</td><td>'+c.orbit_size+'</td><td>'+c.three_count+' / '+c.four_count+'</td><td>'+c.minimum_known_inner_vertices+'</td></tr>').join('')+'</tbody>';bindMaskButtons(el('known-table'));
el('open-cards').innerHTML=open.map(c=>'<div class="panel"><h3><button data-mask="'+c.canonical+'">Σ'+c.canonical+'</button> '+statusBadge(c.status)+'</h3><p>orbit members：<span class="mono">'+c.orbit_members.join(', ')+'</span><br>三色／四色：'+c.three_count+' / '+c.four_count+'；orbit size：'+c.orbit_size+'<br>允許 bits：'+c.allowed_bits.join(', ')+'</p>'+featureTable(c.features)+(c.nearest_known_masks?featureTable({nearest_known_masks:c.nearest_known_masks}):'')+'</div>').join('');bindMaskButtons(el('open-cards'));
Object.entries(statusInfo).forEach(([k,[name]])=>el('statusfilter').insertAdjacentHTML('beforeend','<option value="'+k+'">'+name+'</option>'));for(const[id,key]of[['threefilter','three_count'],['fourfilter','four_count']]){el(id).insertAdjacentHTML('beforeend',[...new Set(A.classes.map(c=>c[key]))].sort((a,b)=>a-b).map(n=>'<option value="'+n+'">'+n+'</option>').join(''));el(id).onchange=renderClassTable}el('query').oninput=renderClassTable;el('statusfilter').onchange=renderClassTable;
el('selectmask').onclick=()=>select(Number(el('mask').value));el('mask').onkeydown=e=>{if(e.key==='Enter')select(Number(el('mask').value))};el('mask').max=S.nonempty_masks;
el('maskgrid').onclick=e=>{const r=e.target.getBoundingClientRect(),col=Math.floor((e.clientX-r.left)/r.width*33),row=Math.floor((e.clientY-r.top)/r.height*31),m=row*33+col+1;if(M.has(m))select(m)};
el('maskgrid').onmousemove=e=>{const r=e.target.getBoundingClientRect(),m=Math.floor((e.clientY-r.top)/r.height*31)*33+Math.floor((e.clientX-r.left)/r.width*33)+1,row=M.get(m);el('maskgrid').title=row?'Σ'+m+' · canonical '+row.canonical+' · '+statusInfo[row.status][0]:''};
el('maskgrid').onkeydown=e=>{const shift={ArrowLeft:-1,ArrowRight:1,ArrowUp:-33,ArrowDown:33}[e.key];if(shift){e.preventDefault();select(Math.min(S.nonempty_masks,Math.max(1,selected+shift)))}};
renderClassTable();select(selected);
}
setup();
</script></body></html>
'''


def render(atlas: dict) -> dict[str, str]:
    """Return reproducible filenames → UTF-8 text for a single source atlas."""
    data = json.dumps(_compact(atlas), ensure_ascii=False, separators=(",", ":"),
                      sort_keys=True).replace("<", "\\u003c").replace("&", "\\u0026")
    return {"overview.svg": _svg(atlas),
            "index.html": HTML.replace("__ATLAS_DATA__", data)}
