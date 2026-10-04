#!/usr/bin/env python3
"""E4C: fixed 54 NA controls, literal relations and exhaustive row cores.
No Four Color Theorem oracle. Generation is exclusive; replay compares bytes.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_e4c'
B = frozenset(range(5))
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in B)
ROOTS = (5, 6)
SINGLETON = {6: 0, 4: 1, 3: 2, 1: 3, 0: 4}
SELECTED = (1, 4, 6)
T4 = (2, 5, 7, 8, 9)

"""Independent deterministic four-colour and exhaustive row-core engine.

No four-colour theorem or E4 routines are used. Core search preserves the
literal boundary names and edges, and enumerates every minimal rejected
edge subset. A private vertex of current degree < 4 is removed because any
four-colouring of the remaining graph extends greedily to it.
"""

def e4c_colorings(vertices, edges, fixed, first_only=False):
    """Return literal colour dicts, sorted by the complete vertex-colour tuple."""
    vertices = tuple(sorted(vertices))
    vertex_set = set(vertices)
    edges = tuple(sorted({tuple(sorted(edge)) for edge in edges}))
    if any(a not in vertex_set or b not in vertex_set or a == b for a, b in edges):
        raise ValueError("invalid graph edge")
    if not set(fixed) <= vertex_set or any(c not in range(4) for c in fixed.values()):
        raise ValueError("invalid prescribed colours")
    neighbours = {v: set() for v in vertices}
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    colours = dict(fixed)
    if any(a in colours and b in colours and colours[a] == colours[b] for a, b in edges):
        return []
    out = []

    def visit():
        if len(colours) == len(vertices):
            out.append(dict(colours))
            return first_only
        uncoloured = [v for v in vertices if v not in colours]
        banned = {v: {colours[w] for w in neighbours[v] if w in colours}
                  for v in uncoloured}
        v = min(uncoloured, key=lambda u: (-len(banned[u]), -len(neighbours[u]), u))
        for colour in range(4):
            if colour in banned[v]:
                continue
            colours[v] = colour
            if visit():
                del colours[v]
                return True
            del colours[v]
        return False

    visit()
    return sorted(out, key=lambda colours: tuple(colours[v] for v in vertices))


def e4c_sigma(vertices, edges, rows):
    """Return complete Sigma mask and accepted-row full literal witnesses."""
    vertices = tuple(sorted(vertices))
    mask = 0
    witnesses = {}
    for i, row in enumerate(rows):
        found = e4c_colorings(vertices, edges, dict(enumerate(row)), first_only=True)
        if found:
            mask |= 1 << i
            witnesses[i] = tuple(found[0][v] for v in vertices)
    return mask, witnesses


def e4c_minimal_cores(vertices, edges, row):
    """All inclusion-minimal rejected subgraphs retaining B and its frame.

    Returned records contain named vertices/edges and a colouring witnessing
    acceptance after deleting each nonframe edge. The exhaustive recursion
    memoizes peeled literal edge sets. Peeling preserves rejection; all
    minimal rejected subgraphs have private degree at least four. Since a
    vertex deletion removes its incident edges, edge-minimality also implies
    vertex-minimality. The requested fixed row must be rejected initially.
    """
    frame = tuple(range(len(row)))
    if len(frame) != 5:
        raise ValueError("the boundary must be C5")
    frame_set = set(frame)
    fixed = dict(enumerate(row))
    mandatory = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in frame)
    vertices = tuple(sorted(vertices))
    if not frame_set <= set(vertices):
        raise ValueError("the graph must retain the boundary")
    edges = frozenset(tuple(sorted(edge)) for edge in edges)
    if not mandatory <= edges:
        raise ValueError("the graph must retain the C5 edges")
    if e4c_colorings(vertices, edges, fixed, first_only=True):
        return []
    seen = set()
    acceptance = {}
    minimal = set()

    def peel(current):
        current = set(current)
        while True:
            degree = {}
            for a, b in current:
                degree[a] = degree.get(a, 0) + 1
                degree[b] = degree.get(b, 0) + 1
            small = {v for v, d in degree.items() if v not in frame_set and d < 4}
            if not small:
                break
            current = {(a, b) for a, b in current if a not in small and b not in small}
        return tuple(sorted(current))

    def graph_vertices(current):
        return tuple(sorted(frame_set | {v for edge in current for v in edge}))

    def accepts(current):
        if current not in acceptance:
            acceptance[current] = bool(e4c_colorings(graph_vertices(current), current,
                                                    fixed, first_only=True))
        return acceptance[current]

    def recurse(current):
        current = peel(current)
        if current in seen:
            return
        seen.add(current)
        if accepts(current):
            return
        reduced = False
        for edge in current:
            if edge in mandatory:
                continue
            child = peel(e for e in current if e != edge)
            if not accepts(child):
                reduced = True
                recurse(child)
        if not reduced:
            minimal.add(current)

    recurse(edges)
    records = []
    for current in sorted(minimal):
        core_vertices = graph_vertices(current)
        witnesses = []
        for edge in current:
            if edge in mandatory:
                continue
            deleted = tuple(e for e in current if e != edge)
            found = e4c_colorings(core_vertices, deleted, fixed, first_only=True)
            assert found, ("nonminimal returned core", current, edge)
            witnesses.append({"edge": list(edge),
                              "colouring": [found[0][v] for v in core_vertices]})
        records.append({"vertices": list(core_vertices),
                        "edges": [list(edge) for edge in current],
                        "edge_deletion_witnesses": witnesses})
    return records


CATALOG = {'A1': {'conclusion': '有效 H 非空連通，全部有效內點 degree≥4',
        'premises': 'induced C₅ disk、T4、非空 Q、完整 Σ-critical',
        'scope': 'no-selected-triple',
        'source': 'E3 notes §1；CORE §1',
        'title': '有效內部／度數下限'},
 'A2': {'conclusion': 'G 碰齊五框點；單缺列不套這個推導',
        'premises': 'A1 且 |Q|≥2',
        'scope': 'no-selected-triple',
        'source': 'E3 notes §1',
        'title': '全 B-touch 推導'},
 'A3': {'conclusion': '每內點至多三條 actual spokes',
        'premises': 'T4 全收',
        'scope': 'no-selected-triple',
        'source': 'E4 §1；CORE §4',
        'title': 'spokes 上限'},
 'A4': {'conclusion': 'm≥1，兩側 mixed incidence 都≥1',
        'premises': '原 H 連通；z、w 非相鄰',
        'scope': 'no-selected-triple',
        'source': 'E3 notes §2；E4 §1',
        'title': 'mixed 必存在'},
 'A5': {'conclusion': '各 piece 完整 degree4、owner 非空；t_r+Σincidence=5；unary one-sided；sole mixed '
                      'separating；m≥2 則全 one-sided',
        'premises': '原 H−{z,w} 完整分量，H 連通、兩 roots 非相鄰',
        'scope': 'no-selected-triple',
        'source': 'E4 §3、§4.3；E3 notes §2–3',
        'title': '原 piece 分類與容量'},
 'A6': {'conclusion': '(E_z×E_w)∩⋂A_C 恰等於整圖 root-pair 延拓 relation；每非空 fibre 有整圖 lift',
        'premises': '每 β 的整份 R_P、distinct contacts、lifts、16 有序 pins，同一色框',
        'scope': 'no-selected-triple',
        'source': 'E4 §6；CORE §6',
        'title': '完整 literal join'},
 'A7': {'conclusion': 'contact 僅移除該 inequality；piece 內邊／框附件僅改該原局部 relation；join 精確等於 G−e 完整 Σ',
        'premises': '同一原圖／β；刪一條非框邊',
        'scope': 'no-selected-triple',
        'source': 'E4 §6',
        'title': '刪邊 relation 身份'},
 'B1': {'conclusion': '與 Σ-criticality 矛盾；此 forbidden 配置若出現即反例',
        'premises': '原 mixed C 的 actual N_B(C)=∅；原來源 Σ-critical',
        'scope': 'no-selected-triple',
        'source': 'E4 §2.1',
        'title': 'N-empty-separating'},
 'B2': {'conclusion': '每份合法 outside colouring 能填回 P；其 contact 不會 critical',
        'premises': 'degree4 mixed P 無框支援，G−P 有原 z–w 路（可走 B）',
        'scope': 'no-selected-triple',
        'source': 'E4 §2.1；CORE §3',
        'title': 'E4-N0／外路 hub 分袋'},
 'B3': {'conclusion': '不碰 B 的 root 側 A∪C 僅在另一 root 接合，可一次共同 S₄ 配上 pin；內部非框邊非critical',
        'premises': '無框 mixed C，G−C 不連通；原 H 連通、B 連通、原 G 可染',
        'scope': 'no-selected-triple',
        'source': 'E4 §2.1',
        'title': '無框 appendage 接回'},
 'B4': {'conclusion': '兩側有原 C 外 side 因子並經 B 原路連接，G−C 有 z–w 路',
        'premises': 'm=1，C 兩側 incidence≤4，原 unary support 非空',
        'scope': 'no-selected-triple',
        'source': 'CORE §3',
        'title': 'sole mixed 原外路充分條件'},
 'B5': {'conclusion': 'actual attachment 數2k+4，E=3k+8>disk上界3k+7，矛盾',
        'premises': '原 H 是 k 點 connected tree；內部完整 degree 和4k+2；五框 disk',
        'scope': 'no-selected-triple',
        'source': 'E4 §2.2',
        'title': 'tree-H Euler 排除'},
 'B6': {'conclusion': '三條 internally-disjoint 原 z–w 路至少困住一整原 piece；该 piece 的 actual support 空',
        'premises': '同一原 disk 有至少三份不同 mixed 原分量',
        'scope': 'no-selected-triple',
        'source': 'E4 §5',
        'title': 'N-theta'},
 'B7': {'conclusion': '全部 mixed actual support 非空；原 H 有 cycle；m≤2',
        'premises': '合格非相鄰 Σ-critical ε2 原圖（不預設 forbidden 配置）',
        'scope': 'no-selected-triple',
        'source': 'E4 §2、§5',
        'title': '無空支援／非樹／m≤2 必要條件'},
 'B8': {'conclusion': '收縮整原 pieces 的 K₂,m：V=m+2,E=2m,F=m，各面4環含2 mixed；B 在一面且所有 mixed 接 B，故 m≤2',
        'premises': 'm≥2；原 disk；每 mixed 有 actual support',
        'scope': 'no-selected-triple',
        'source': 'CORE §5',
        'title': 'E4-F：K₂,m 面容量'},
 'C1': {'conclusion': '原 σ 連續；|S|≥2 時每支援點incident σ；外部不碰 σ 內點（σ≠B）；互斥 pieces 的 σ 邊互斥',
        'premises': 'connected 原 P；H−P connected，P 及其附件同一 disk；比較互斥 pieces',
        'scope': 'no-selected-triple',
        'source': 'E4 §3.3、§4.3；shield Lemma1',
        'title': '盾弧純拓撲四項'},
 'C10': {'conclusion': '全部10 proper β、全部4色 a，(a,a)∈完整 A_C(β)，不要求 pins 延拓 outside',
         'premises': 'degree4 mixed one-sided；全 B-touch；actual support 含於真框邊',
         'scope': 'no-selected-triple',
         'source': 'E4 §4.1',
         'title': '局部 N-diagonal'},
 'C11': {'conclusion': '全部5個三色 β 可用未用色 D 接回 G，故全部接受',
         'premises': 'm=2，兩份 mixed 都短，無 unary；N-diagonal 前提含全 B-touch',
         'scope': 'no-selected-triple',
         'source': 'E4 §4.2；與三列矛盾是另一步',
         'title': 'N2-short-no-unary'},
 'C12': {'conclusion': 'E_z(β)∩E_w(β)=∅；off-diagonal joint 仍須完整保留',
         'premises': '全部原 mixed 都短且 one-sided；N-diagonal 全 B-touch 前提；β 實際拒絕',
         'scope': 'no-selected-triple',
         'source': 'E4 §4.2',
         'title': '短 mixed 的拒絕列側交集'},
 'C13': {'conclusion': '完整 P 可接回；不得只看 contact marginals',
         'premises': 'connected 原 degree4 piece；固定 β 及全部 root pins；至少一個點 lists 大於原內部 degree',
         'scope': 'no-selected-triple',
         'source': 'E4 §3.2；E3 root-deletion',
         'title': '局部 degree-list slack 接回'},
 'C14': {'conclusion': '每 β 的 side 至少一份完整延拓；不是任意預釘 root 色都可行',
         'premises': '原連通 side S_r：root degree≤3，其餘點 full degree4',
         'scope': 'no-selected-triple',
         'source': 'E4 §3.1；E3 root-deletion',
         'title': '低 degree root 完整側接回'},
 'C2': {'conclusion': 'S=V(σ)，故支援為完整連續區間；不從單缺列假設全框',
        'premises': 'C1；全 B-touch；|S|≥2',
        'scope': 'no-selected-triple',
        'source': 'E4 §3.3、§4.3；shield Lemma2',
        'title': '支援等於盾弧頂點'},
 'C2a': {'conclusion': '盾弧恰1邊',
         'premises': 'one-sided piece actual support恰真框邊兩點，且全B-touch',
         'scope': 'no-selected-triple',
         'source': 'E4 §4.3',
         'title': 'short adjacent-pair 盾長'},
 'C2b': {'conclusion': '盾弧0邊',
         'premises': 'one-sided piece actual support恰singleton，且全B-touch',
         'scope': 'no-selected-triple',
         'source': 'E4 §4.3',
         'title': 'singleton 盾長'},
 'C3': {'conclusion': '限制到 outside 後 P 不可接回；每 P 點 list 大小恰為原內部 degree',
        'premises': '原 piece degree4；G−contact 新接受 β 的 full lift；G 拒絕 β',
        'scope': 'no-selected-triple',
        'source': 'E4 §2.1、§4.1；shield TheoremA/B',
        'title': 'contact 拒絕見證的 tight lists'},
 'C3a': {'conclusion': '至少一實際 β 的完整 unary tuples 共同避色集合不是全4，即 F_U(β) 非空',
         'premises': 'unary 的 contact 是 Σ-critical',
         'scope': 'no-selected-triple',
         'source': 'E4 §4.3；shield TheoremA',
         'title': 'unary forbidden-root 見證'},
 'C4': {'conclusion': 'support 不含於任一框邊，至少3個連續框點，|σ_U|≥2',
        'premises': 'degree4 unary；critical contact；原 H 連通；全 B-touch',
        'scope': 'no-selected-triple',
        'source': 'E4 §4.3；E3 notes §3；shield TheoremA',
        'title': 'unary 支援／盾弧下界'},
 'C5': {'conclusion': 'Σ_P |σ_P|≤5',
        'premises': '原互斥 one-sided pieces，同一 disk',
        'scope': 'no-selected-triple',
        'source': 'E4 §4.3；shield Lemma1(d)',
        'title': '共同盾弧總預算'},
 'C6': {'conclusion': 'u≤2',
        'premises': 'C4 下界及 C5，同一原來源全 B-touch',
        'scope': 'no-selected-triple',
        'source': 'E4 §3、§4.3；shield TheoremA',
        'title': 'unary 個數上限'},
 'C7': {'conclusion': '盾長排序為(2,2)或(2,3)；所有 roots spokes／mixed support 避開兩 σ 的內點',
        'premises': '全 B-touch，恰兩 unary',
        'scope': 'no-selected-triple',
        'source': 'E4 §4.3；E3 notes §3；shield TheoremA',
        'title': '兩 unary 容量與外部附件限制'},
 'C8': {'conclusion': '|σ_C|≥2；此純拓撲步驟不需全 B-touch',
        'premises': '原 mixed one-sided，actual support 不含於任何框邊',
        'scope': 'no-selected-triple',
        'source': 'E4 §4.3；shield Lemma1(b)',
        'title': 'long mixed 盾弧下界'},
 'C9': {'conclusion': 'ℓ+u≤2；Σlong盾長+Σunary盾長+#short-pair≤5',
        'premises': 'm≥2，全 pieces one-sided，全 B-touch',
        'scope': 'no-selected-triple',
        'source': 'E4 §4.3',
        'title': 'long＋unary／short-pair 預算'},
 'D1': {'conclusion': 'Σ(G−w)=Σ(S_z)，保留原 z 色；S_z root degree=5−m_z',
        'premises': '同一原 β；完整 mixed／unary；刪 w（對稱）',
        'scope': 'no-selected-triple',
        'source': 'E4 §3、§6；E3 notes §2',
        'title': '原 root 刪除 Σ 身份'},
 'D10': {'conclusion': '取同Σ inclusion-minimal Y；Y 非框邊自己Σcritical，有效內點 degree≥4',
         'premises': '原unit derivative X 保留B，有效度數≥4；不預設 X critical',
         'scope': 'no-selected-triple',
         'source': 'CORE §2',
         'title': 'Σ-preserving minimalization'},
 'D11': {'conclusion': 'ε(X)−ε(Y)=被省頂點Σ(degX−4)+保留頂點Σ(degX−degY)≥0',
         'premises': 'D10；X 所有有效內點degree≥4',
         'scope': 'no-selected-triple',
         'source': 'CORE §2',
         'title': 'ε 單調的 exact identity'},
 'D12': {'conclusion': 'ε1的完整Q空／單點／相鄰二點，故不能同拒q₃與q₀／q₁；ε0的Q至多一點',
         'premises': '一原unit side省略ε1；兩側各unit或11mixed省略且有效度數≥4則ε0；同Σ minimalization',
         'scope': 'no-selected-triple',
         'source': 'CORE §2、§4',
         'title': 'unit derivative／E2 拒絕位置'},
 'D12a': {'conclusion': '同一原省略圖不會同拒q₃及q₀／q₁',
          'premises': 'D12的有效原unit derivative，不預設原G三列全拒',
          'scope': 'no-selected-triple',
          'source': 'CORE §2、§4',
          'title': 'E4-U literal單位導數列限制'},
 'D13': {'conclusion': '有效H非空連通、有效內點degree≥4、逐邊qcritical且自己Σcritical',
         'premises': '任意實際拒絕 β 的全部 inclusion-minimal qcores',
         'scope': 'no-selected-triple',
         'source': 'E4 §1、§6；CORE §1',
         'title': '每列 minimal core 自身前提'},
 'D14': {'conclusion': '恰原 S_r；另一root degree4，完整 Σ 只缺 β；m1且該側mixed incidence1',
         'premises': '實際拒絕 β 的 minimal qcore 省略一root',
         'scope': 'no-selected-triple',
         'source': 'E4 §6；CORE §6；E3 notes §2/5',
         'title': '省略 root 的 exact side core'},
 'D15': {'conclusion': 'terminal兩框附件在該β必異色；同色會讓connected C list slack而接回',
         'premises': 'D8 的原 terminal 两actual附件；β實際拒絕',
         'scope': 'no-selected-triple',
         'source': 'E4 §3.2 的單列部分',
         'title': 'N1 terminal 單拒絕列 slack 步驟'},
 'D16': {'conclusion': '兩原整側各one-sided，actual盾弧服從C1，邊互斥；此步不收separating C盾弧',
         'premises': 'D8；沿原terminal path中間bridge分原H為两connected互斥整側',
         'scope': 'no-selected-triple',
         'source': 'E4 §3.3 的拓撲部分',
         'title': 'N1 bridge 分兩整側的純盾弧'},
 'D16a': {'conclusion': '各整側one-sided，其原盾弧連續／支援標記／外部附件限制／邊互斥；全Btouch且支援≥2再得S=Vσ',
          'premises': '原H bridge兩側各connected且各含一root；兩側互斥coverH',
          'scope': 'no-selected-triple',
          'source': 'E4 §3.3 的純拓撲前提',
          'title': 'generic 原bridge兩整側盾弧'},
 'D1a': {'conclusion': 'G−w 與原 S_z 的每 β／a 接受性完全相同',
         'premises': 'D1 且指定 surviving root 的字面色 a',
         'scope': 'no-selected-triple',
         'source': 'E3 notes §2',
         'title': '原 root 刪除 pin 身份'},
 'D2': {'conclusion': 'm_r=1、原 side root degree4，完整 Σ 僅缺一列',
        'premises': '原 S_r 實際拒絕某 β',
        'scope': 'no-selected-triple',
        'source': 'E4 §3、§6；E3 notes §2',
        'title': 'root-deletion 单缺列例外'},
 'D3': {'conclusion': '兩 side 不會同拒；兩 root-deletion 的拒絕列合計≤1',
        'premises': '兩原 side 同一 disk，完整 root-deletion 身份',
        'scope': 'no-selected-triple',
        'source': 'E4 §3、§6；E3 notes §2',
        'title': '全部拒絕列至多一 root 例外'},
 'D4': {'conclusion': '兩個 G−root 均 Σ=1023；任何拒絕列 core 含兩 roots',
        'premises': 'm≥2，故兩側 mixed incidence≥2',
        'scope': 'no-selected-triple',
        'source': 'E4 §4.3；E3 notes §2',
        'title': 'm≥2 原 root 刪除全收'},
 'D4a': {'conclusion': 'Σ(G−另一root)=Σ(S_r)=1023；該root省略不能留下拒絕core',
         'premises': '任一原側r mixed incidence m_r≥2（允許m1）',
         'scope': 'no-selected-triple',
         'source': 'E3 notes §2；E4 §3、§6',
         'title': 'mixed incidence≥2 原刪root全收'},
 'D5': {'conclusion': 'P 完全省略或原頂點／內邊／框附件／root contacts 全保留',
        'premises': '任意實際拒絕 β 的 inclusion-minimal qcore；原 P full degree4',
        'scope': 'no-selected-triple',
        'source': 'E4 §3.1、§6；E3 notes §5',
        'title': '原 degree4 pieces 全取／全不取'},
 'D6': {'conclusion': '55=G；45/54恰一對應側unit spoke／整unary，所有mixed保留；44恰兩側各unit或一11mixed；保留mixed≥1',
        'premises': 'D5；qcore 保留两roots；root degrees只4/5',
        'scope': 'no-selected-triple',
        'source': 'E4 §6；CORE §6；E3 notes §5',
        'title': '完整原 core 省略身份'},
 'D7': {'conclusion': '恰一retained mixed且各側contacts≤2；m1不省soleC，m2只省一11mixed，m3無44',
        'premises': '兩roots degree4的minimal qcore，兩roots非相鄰',
        'scope': 'no-selected-triple',
        'source': 'E4 §3.1、§6；CORE §6',
        'title': 'nonadjacent44 retained-mixed 限制'},
 'D7a': {'conclusion': 'root有2contacts則原contact pair間有實際邊；雙2時兩contact '
                       'sets互斥，兩原roottriangles以直接原bridge相連且无tails',
         'premises': 'nonadjacent44 core之retained mixed',
         'scope': 'no-selected-triple',
         'source': 'E4 §3.1、§6；E3 notes §5',
         'title': '44 contact 原triangle／互斥身份'},
 'D8': {'conclusion': '整原 C 是4點 path；root 各接相鄰2點成互斥triangles，以直接原bridge相連，無tails；terminal各2框附件，內點各1',
        'premises': 'm=1；sole C incidences22；實際拒絕 β 有兩root44 core',
        'scope': 'no-selected-triple',
        'source': 'E4 §3.1',
        'title': 'N1 mixed22＋44 原 path 身份'},
 'D9': {'conclusion': '每側原capacity3；僅三spokes或兩spokes＋capacity1 unary；原 side 每 β 全收',
        'premises': 'D8，原 root degree5',
        'scope': 'no-selected-triple',
        'source': 'E4 §3.1',
        'title': 'N1 mixed22＋44 完整側身份'},
 'D9a': {'conclusion': '每側恰三spokes或兩spokes＋一整capacity1 unary；該unit是原core省略因子',
         'premises': 'N1 soleC22＋44core，无retained tails，原root5',
         'scope': 'no-selected-triple',
         'source': 'E4 §3.1',
         'title': 'N1 side only兩種原型'},
 'E1': {'conclusion': '刪任一其中spoke不改該β接受性',
        'premises': '同root两actual spokes在任意 proper β 同色',
        'scope': 'no-selected-triple',
        'source': 'CORE §4 E4-S 的局部步驟',
        'title': '逐列 redundant-spoke 身份'},
 'E2': {'conclusion': '該spoke至少在一份實際新接受拒絕列有private框色',
        'premises': '原spoke對完整Σ critical',
        'scope': 'no-selected-triple',
        'source': 'CORE §4 E4-S 的一般化',
        'title': '完整Q private-spoke'},
 'E2a': {'conclusion': '被刪spoke的框色不被同root任何其他原spoke重複',
         'premises': 'β∈Σ(G−spoke)∖Σ(G)',
         'scope': 'no-selected-triple',
         'source': 'CORE §4 E4-S 的局部必要條件',
         'title': '所有刪spoke新列均private'},
 'E3': {'conclusion': '每root在該qcore中保留的spokes框色均不同',
        'premises': '任一實際拒絕β的minimal qcore',
        'scope': 'no-selected-triple',
        'source': 'CORE §4 E4-D 證明中間步驟',
        'title': 'qcore 不能保留重色 spoke pair'},
 'E4': {'conclusion': '兩roots至多一root原spokes重色',
        'premises': 'm=2；β為任意實際拒絕列（不用三列身份）',
        'scope': 'no-selected-triple',
        'source': 'CORE §4 E4-D 的逐q一般化',
        'title': 'N2 每拒絕列至多一重色 root'},
 'E5': {'conclusion': '每 minimal qcore恰G減該pair一spoke，自身degree45/54；該derivative再受D12',
        'premises': 'E4 且恰一root r有原重色spoke pair',
        'scope': 'no-selected-triple',
        'source': 'CORE §4 E4-D 的逐q一般化',
        'title': 'N2 單重色 exact 原 spoke core'},
 'T1': {'conclusion': '每spoke在指定三列至少一次private；原3-spoke024／124被排除',
        'premises': 'q₀、q₁、q₃全拒絕且triple-critical',
        'scope': 'requires-selected-triple',
        'source': 'CORE §4 E4-S，明確使用三列',
        'title': '原三列 private-spoke 排除'},
 'T2': {'conclusion': 'terminal actual pair是框邊；兩整側盾弧各≥3；3+3>5整類排除',
        'premises': '原sole mixed22＋44 core且指定三列全拒絕',
        'scope': 'requires-selected-triple',
        'source': 'E4 §3.2–§3.3，明確使用三列',
        'title': 'N1-22-44 三列整類排除'}}


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')) + '\n').encode()


def ns_of(vertices, edges):
    ns = {v: set() for v in vertices}
    for a, b in edges:
        ns[a].add(b)
        ns[b].add(a)
    return ns


def comps(vertices, edges):
    left = set(vertices)
    ns = ns_of(left, [e for e in edges if set(e) <= left])
    out = []
    while left:
        todo, got = [min(left)], set()
        while todo:
            v = todo.pop()
            if v in got:
                continue
            got.add(v)
            todo.extend(sorted(ns[v] - got, reverse=True))
        left -= got
        out.append(sorted(got))
    return out


def short(support):
    return any(set(support) <= set(e) for e in FRAME)


def q_of(mask):
    return sorted(p for i, p in SINGLETON.items() if not mask >> i & 1)


def epsilon(vertices, edges):
    ns = ns_of(vertices, edges)
    return sum(len(ns[v]) - 4 for v in vertices if v not in B and ns[v])


def faces_of(rotation):
    plane = nx.PlanarEmbedding()
    plane.set_data({int(v): list(ns) for v, ns in rotation.items()})
    plane.check_structure()
    seen, faces, dart = set(), [], {}
    for a, b in sorted(plane.edges()):
        if (a, b) in seen:
            continue
        f = plane.traverse_face(a, b, seen)
        for u, v in zip(f, f[1:] + f[:1]):
            dart[u, v] = len(faces)
        faces.append(f)
    return faces, dart


def shield(vertices, edges, rotation, piece):
    """Merge original faces after removing everything outside B plus piece."""
    faces, dart = faces_of(rotation)
    own = B | set(piece)
    keep = {e for e in edges if set(e) <= own}
    parent = list(range(len(faces)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for a, b in sorted(edges - keep):
        parent[find(dart[a, b])] = find(dart[b, a])
    outside = set(vertices) - own
    regions = {find(i) for i, f in enumerate(faces) if set(f) & outside}
    if len(regions) != 1:
        raise ValueError('one-sided set has no unique original containing face')
    region = next(iter(regions))
    visible = {e for e in FRAME if any(find(dart[uv]) == region for uv in (e, e[::-1]))}
    sigma = FRAME - visible
    support = {a for a, b in edges if a in B and b in piece}
    outside_support = {a for a, b in edges if a in B and b in outside}
    counts = Counter(v for e in sigma for v in e)
    interiors = {v for v, n in counts.items() if n == 2} if len(sigma) < 5 else set()
    continuous = not sigma or len(comps({v for e in sigma for v in e}, sigma)) == 1
    return dict(edges=sorted(sigma), support=sorted(support), interiors=sorted(interiors),
                outside_support=sorted(outside_support), containing_faces=[f for i, f in enumerate(faces) if find(i) == region],
                continuous=continuous, support_incident=len(support) < 2 or support <= set(counts),
                outside_avoids_interiors=not (outside_support & interiors),
                vertices=sorted(counts))


def minimalize(vertices, edges, rows):
    """Greedy Sigma-preserving edge deletion, also removing isolated vertices."""
    vertices, edges = set(vertices), set(edges)
    target, _ = e4c_sigma(vertices, edges, rows)
    for e in sorted(edges - FRAME):
        trial = edges - {e}
        if e4c_sigma(vertices, trial, rows)[0] == target:
            edges = trial
    vertices = B | {v for e in edges for v in e}
    sig, witnesses = e4c_sigma(vertices, edges, rows)
    deletions = []
    for e in sorted(edges - FRAME):
        m, ws = e4c_sigma(vertices, edges - {e}, rows)
        deletions.append(dict(edge=e, sigma=m, witnesses=ws))
    return dict(vertices=sorted(vertices), edges=sorted(edges), sigma=sig, witnesses=witnesses,
                epsilon=epsilon(vertices, edges), deletions=deletions)


def verify_lift(vertices, edges, row, lift):
    f = dict(zip(vertices, lift))
    return all(f[i] == row[i] for i in B) and all(f[a] != f[b] for a, b in edges)


def graph_data(path, rows):
    raw = path.read_bytes()
    source = json.loads(raw)
    edges = {tuple(e) for e in source['canonical_edges']}
    vertices = tuple(range(max(v for e in edges for v in e) + 1))
    private = set(vertices) - B
    ns = ns_of(vertices, edges)
    rotation = source['embedding']['disk_rotation']
    faces, _ = faces_of(rotation)
    assert {tuple(sorted((int(v), w))) for v, ns1 in rotation.items() for w in ns1} == edges
    assert any(len(f) == 5 and set(f) == B for f in faces)
    assert len(vertices) - len(edges) + len(faces) == 2
    assert {e for e in edges if set(e) <= B} == FRAME
    assert [len(ns[r]) for r in ROOTS] == [5, 5] and (5, 6) not in edges
    assert all(len(ns[v]) == 4 for v in private - set(ROOTS))
    sigma, witnesses = e4c_sigma(vertices, edges, rows)
    assert sigma == source['sigma_mask'] and sigma & 932 == 932
    assert q_of(sigma) == source['Q'] and sigma != 1023
    assert all(verify_lift(vertices, edges, rows[int(i)], f) for i, f in witnesses.items())
    deletions = []
    for e in sorted(edges - FRAME):
        m, ws = e4c_sigma(vertices, edges - {e}, rows)
        assert m != sigma and m | sigma == m
        saved = next(x for x in source['deletion_sigmas'] if tuple(x['edge']) == e)
        assert m == saved['sigma_mask']
        deletions.append(dict(edge=e, sigma=m, gained=[i for i in range(10) if m >> i & 1 and not sigma >> i & 1], witnesses=ws))
    pieces = []
    for j, pv in enumerate(comps(private - set(ROOTS), edges)):
        own = set(pv)
        contacts = {r: sorted(ns[r] & own) for r in ROOTS}
        owners = [r for r in ROOTS if contacts[r]]
        coords = sorted(set().union(*(set(c) for c in contacts.values())))
        support = sorted({b for v in pv for b in ns[v] & B})
        local_edges = {e for e in edges if set(e) <= (own | B)}
        one_sided = len(comps(private - own, edges)) == 1
        piece = dict(id=f'P{j}', vertices=pv, internal_edges=sorted(e for e in edges if set(e) <= own),
                     attachments=sorted(e for e in edges if set(e) & own and set(e) & B),
                     contacts=contacts, contact_order=coords, owners=owners, incidences=[len(contacts[r]) for r in ROOTS],
                     kind='mixed' if len(owners) == 2 else 'unary', support=support,
                     one_sided=one_sided, short=short(support), rows=[])
        if one_sided:
            piece['shield'] = shield(vertices, edges, rotation, own)
        for qi, row in enumerate(rows):
            local = e4c_colorings(B | own, local_edges, dict(enumerate(row)))
            grouped = {}
            for f in local:
                key = tuple(f[v] for v in coords)
                grouped.setdefault(key, []).append([f[v] for v in pv])
            tuples = [dict(tuple=t, lifts=grouped[t]) for t in sorted(grouped)]
            fibres = []
            for a, b in product(range(4), repeat=2):
                pins = {5: a, 6: b}
                indices = [ti for ti, item in enumerate(tuples)
                           if all(item['tuple'][coords.index(v)] != pins[r] for r in owners for v in contacts[r])]
                fibres.append(dict(pins=[a, b], tuple_indices=indices))
            available = {str(r): [a for a in range(4) if any(all(item['tuple'][coords.index(v)] != a for v in contacts[r]) for item in tuples)]
                         for r in owners}
            piece['rows'].append(dict(index=qi, tuples=tuples, fibres=fibres, available=available))
        pieces.append(piece)
    mixed = [p for p in pieces if p['kind'] == 'mixed']
    unary = [p for p in pieces if p['kind'] == 'unary']
    joins = []
    for qi, row in enumerate(rows):
        side = {}
        for r in ROOTS:
            side[str(r)] = [a for a in range(4) if all(row[v] != a for v in ns[r] & B)
                            and all(a in p['rows'][qi]['available'][str(r)] for p in unary if r in p['owners'])]
        joined = []
        for a, b in product(range(4), repeat=2):
            if a not in side['5'] or b not in side['6']:
                continue
            if all(p['rows'][qi]['fibres'][4*a+b]['tuple_indices'] for p in mixed):
                joined.append([a, b])
        full = e4c_colorings(vertices, edges, dict(enumerate(row)))
        actual = sorted({(f[5], f[6]) for f in full})
        join_witnesses = [next([f[v] for v in vertices] for f in full if (f[5], f[6]) == pin) for pin in actual]
        assert joined == [list(pin) for pin in actual]
        joins.append(dict(index=qi, side_available=side, root_pairs=joined, lifts=join_witnesses))
    root_deletions = []
    for absent in ROOTS:
        other = 11 - absent
        vv = set(vertices) - {absent}
        ee = {e for e in edges if absent not in e}
        side_v = B | {other} | {v for p in unary if p['owners'] == [other] for v in p['vertices']}
        side_e = {e for e in edges if set(e) <= side_v}
        dm, dw = e4c_sigma(vv, ee, rows)
        sm, sw = e4c_sigma(side_v, side_e, rows)
        root_deletions.append(dict(absent=absent, sigma=dm, witnesses=dw,
                                   side_vertices=sorted(side_v), side_edges=sorted(side_e), side_sigma=sm, side_witnesses=sw,
                                   mixed_incidence=sum(len(p['contacts'][other]) for p in mixed)))
    cores = []
    for qi in range(10):
        if sigma >> qi & 1:
            cores.append(dict(index=qi, status='accepted; no rejected core', cores=[]))
        else:
            found = e4c_minimal_cores(vertices, edges, rows[qi])
            for c in found:
                cv, ce = set(c['vertices']), {tuple(e) for e in c['edges']}
                cn = ns_of(cv, ce)
                c['root_degrees'] = [len(cn[r]) if r in cv else None for r in ROOTS]
                c['omitted_vertices'] = sorted(set(vertices) - cv)
                c['omitted_edges'] = sorted(edges - ce)
                c['sigma'], c['accepted_witnesses'] = e4c_sigma(cv, ce, rows)
                c['retained_pieces'] = [p['id'] for p in pieces if set(p['vertices']) <= cv]
                c['omitted_pieces'] = [p['id'] for p in pieces if not set(p['vertices']) & cv]
            assert found
            cores.append(dict(index=qi, status='rejected', cores=found))
    factors = [dict(id=f's{r}_{b}', owners=[r], incidence=[int(r == 5), int(r == 6)],
                    vertices=[], edges=[tuple(sorted((r, b)))]) for r in ROOTS for b in sorted(ns[r] & B)]
    factors += [dict(id=p['id'], owners=p['owners'], incidence=p['incidences'], vertices=p['vertices'],
                    edges=sorted(e for e in edges if set(e) & set(p['vertices']))) for p in pieces]
    units = [f for f in factors if sum(f['incidence']) == 1]
    omissions = [(f,) for f in units]
    omissions += [(f, g) for f, g in combinations(units, 2) if f['owners'] != g['owners']]
    omissions += [(f,) for f in factors if f['incidence'] == [1, 1]]
    derivatives = []
    for fs in omissions:
        removed = {v for f in fs for v in f['vertices']}
        dv = set(vertices) - removed
        de = edges - {e for f in fs for e in f['edges']}
        dn = ns_of(dv, de)
        if not all(len(dn[v]) >= 4 for v in dv - B):
            continue
        dm, dw = e4c_sigma(dv, de, rows)
        y = minimalize(dv, de, rows)
        yn = ns_of(y['vertices'], y['edges'])
        removed_term = sum(len(dn[v]) - 4 for v in dv - set(y['vertices']) - B)
        retained_term = sum(len(dn[v]) - len(yn[v]) for v in set(y['vertices']) - B)
        derivatives.append(dict(factors=[f['id'] for f in fs], vertices=sorted(dv), edges=sorted(de),
                                sigma=dm, witnesses=dw, epsilon=epsilon(dv, de), minimal=y,
                                epsilon_difference_terms=[removed_term, retained_term]))
    touch = sorted({b for v in private for b in ns[v] & B})
    data = dict(id=f'NA{len(private)}-{path.stem.split("_")[-1]}', source=path.relative_to(ROOT).as_posix(),
                source_sha256=sha256(raw).hexdigest(), vertices=vertices, edges=sorted(edges), private_degrees=[len(ns[v]) for v in sorted(private)],
                rotation=rotation, faces=faces, sigma=sigma, Q=q_of(sigma), witnesses=witnesses,
                touch=touch, pieces=pieces, m=len(mixed), u=len(unary), joins=joins,
                deletions=deletions, root_deletions=root_deletions, row_cores=cores, derivatives=derivatives)
    data['lemmas'] = evaluate(data, rows)
    return data


def evaluate(g, rows):
    vv, ee = set(g['vertices']), {tuple(e) for e in g['edges']}
    h = vv - B
    ns = ns_of(vv, ee)
    ps, mixed, unary = g['pieces'], [p for p in g['pieces'] if p['kind'] == 'mixed'], [p for p in g['pieces'] if p['kind'] == 'unary']
    fulltouch = g['touch'] == list(range(5))
    cells = {}
    def add(key, evidence, missing):
        bad = [item for item in evidence if not item['ok']]
        cells[key] = dict(status='反例' if bad else '成立' if evidence else '不適用',
                          reason=missing if not evidence else f'實算 {len(evidence)} 項前提實例', evidence=evidence)
    def ev(**kw):
        return kw
    add('A1', [ev(ok=bool(h) and len(comps(h, ee)) == 1 and min(g['private_degrees']) >= 4)], '')
    add('A2', [ev(ok=fulltouch)] if len(g['Q']) >= 2 else [], '|Q|<2；此推導不適用')
    add('A3', [ev(ok=all(len(ns[v] & B) <= 3 for v in h))], '')
    add('A4', [ev(ok=g['m'] >= 1 and all(sum(len(p['contacts'][r]) for p in mixed) >= 1 for r in ROOTS))], '')
    add('A5', [ev(ok=all(p['owners'] and all(len(ns[v]) == 4 for v in p['vertices']) for p in ps)
                     and all(p['one_sided'] for p in unary)
                     and all(p['one_sided'] == (g['m'] >= 2) for p in mixed)
                     and all(len(ns[r] & B) + sum(len(p['contacts'][r]) for p in ps) == 5 for r in ROOTS))], '')
    add('A6', [ev(ok=bool(j['root_pairs']) == bool(g['sigma'] >> j['index'] & 1), row=j['index'], pairs=j['root_pairs']) for j in g['joins']], '')
    # Rebuild each deleted graph's full piece join, preserving literal contacts.
    update_checks = []
    for d in g['deletions']:
        de = ee - {tuple(d['edge'])}
        local_colours = {}
        for qi, row in enumerate(rows):
            pairset = []
            for a, b in product(range(4), repeat=2):
                pins = {5:a, 6:b}
                if any(row[t] == pins[r] for r in ROOTS for t in ns[r] & B if tuple(sorted((r,t))) in de):
                    continue
                possible = True
                for p in ps:
                    pvs = set(p['vertices'])
                    le = {e for e in de if set(e) <= (B | pvs)}
                    key = (p['id'], qi, tuple(sorted(le)))
                    if key not in local_colours:
                        local_colours[key] = e4c_colorings(B | pvs, le, dict(enumerate(row)))
                    if not any(all(f[v] != pins[r] for r in p['owners'] for v in p['contacts'][r]
                                   if tuple(sorted((r,v))) in de) for f in local_colours[key]):
                        possible = False
                        break
                if possible:
                    pairset.append([a,b])
            actual_colourings=e4c_colorings(vv,de,dict(enumerate(row)))
            actual_pairs=sorted({(f[5],f[6]) for f in actual_colourings})
            update_checks.append(ev(edge=d['edge'], row=qi, ok=pairset==[list(pin) for pin in actual_pairs] and bool(pairset) == bool(d['sigma'] >> qi & 1), pairs=pairset))
    add('A7', update_checks, '')
    empty = [p for p in mixed if not p['support']]
    add('B1', [ev(piece=p['id'], ok=False) for p in empty], '無空支援 mixed；反證配置仍缺控制')
    connected_empty, separating_empty = [], []
    for p in empty:
        outside = vv - set(p['vertices'])
        if any(set(ROOTS) <= set(c) for c in comps(outside, ee)):
            connected_empty.append(ev(piece=p['id'], ok=False))
        else:
            separating_empty.append(ev(piece=p['id'], ok=False))
    add('B2', connected_empty, '無空支援 mixed＋外部 z–w 原路；仍缺控制')
    add('B3', separating_empty, '無空支援 separating appendage；仍缺控制')
    candidates = [p for p in mixed if g['m'] == 1 and max(p['incidences']) <= 4 and all(u['support'] for u in unary)]
    add('B4', [ev(piece=p['id'], ok=any(set(ROOTS) <= set(c) for c in comps(vv - set(p['vertices']), ee))) for p in candidates], '非 sole mixed，或 incidence>4／unary無支援')
    he = {e for e in ee if set(e) <= h}
    tree = len(he) == len(h)-1 and len(comps(h, he)) == 1
    add('B5', [ev(ok=False, k=len(h), actual_edges=len(ee), forced_edges=3*len(h)+8, disk_bound=3*len(h)+7)] if tree else [], '原 H 有 cycle；tree 反證配置仍缺控制')
    add('B6', [ev(ok=bool(empty))] if g['m'] >= 3 else [], 'm<3；theta 前提仍缺控制')
    add('B7', [ev(ok=g['m'] <= 2 and all(p['support'] for p in mixed) and not tree)], '')
    quotient_evidence = []
    if g['m'] >= 2:
        qg = nx.Graph(); qg.add_nodes_from((5,6)); qg.add_edges_from((r, 20+j) for j in range(g['m']) for r in ROOTS)
        planar, pe = nx.check_planarity(qg)
        qfaces, _ = faces_of(pe.get_data())
        original_bags=[dict(quotient_vertex=20+j,piece=p['id'],vertices=p['vertices'],
                      retained_contacts=[tuple(sorted((r,min(p['contacts'][r])))) for r in ROOTS],
                      actual_attachments=p['attachments'],support=p['support']) for j,p in enumerate(mixed)]
        quotient_evidence.append(ev(ok=planar and len(qfaces) == g['m'] and all(len(f)==4 and len(set(f)-set(ROOTS))==2 for f in qfaces)
                                   and g['m'] <= 2 and all(p['support'] and p['one_sided'] for p in mixed), faces=qfaces,original_bags=original_bags))
    add('B8', quotient_evidence, 'm<2；K₂,m 面前提不適用')
    sided = [p for p in ps if p['one_sided']]
    add('C1', [ev(piece=p['id'], ok=p['shield']['continuous'] and p['shield']['support_incident'] and p['shield']['outside_avoids_interiors']) for p in sided]
        + [ev(pieces=[p['id'],q['id']], ok=not(set(map(tuple,p['shield']['edges'])) & set(map(tuple,q['shield']['edges'])))) for p,q in combinations(sided,2)], '無 one-sided piece')
    add('C2', [ev(piece=p['id'], ok=p['support'] == p['shield']['vertices']) for p in sided if fulltouch and len(p['support']) >= 2], '未碰齊五框點，或沒有支援≥2的 one-sided piece')
    tight = []
    for p in ps:
        pv = set(p['vertices'])
        for d in g['deletions']:
            if not (set(d['edge']) & pv and set(d['edge']) & set(ROOTS)):
                continue
            for qi in d['gained']:
                f = dict(zip(g['vertices'],d['witnesses'][qi]))
                lists = {v: sorted(set(range(4)) - {f[w] for w in ns[v]-pv}) for v in pv}
                tight.append(ev(piece=p['id'], edge=d['edge'], row=qi,
                                ok=all(len(lists[v]) == len(ns[v] & pv) for v in pv) and not p['rows'][qi]['fibres'][4*f[5]+f[6]]['tuple_indices'], lists=lists, outside_lift=d['witnesses'][qi]))
    add('C2a',[ev(piece=p['id'],ok=len(p['shield']['edges'])==1) for p in sided if fulltouch and len(p['support'])==2 and p['short']], '未全框，或無adjacent-pair支援的one-sided piece')
    add('C2b',[ev(piece=p['id'],ok=not p['shield']['edges']) for p in sided if fulltouch and len(p['support'])==1], '無singleton支援的one-sided piece；仍缺控制')
    add('C3', tight, '無 contact 刪邊拒絕見證')
    add('C3a', [ev(piece=p['id'], ok=any(len(p['rows'][qi]['available'][str(p['owners'][0])]) < 4 for qi in range(10))) for p in unary], '無 unary')
    slack_checks = []
    for p in ps:
        pv = set(p['vertices'])
        for qi, row in enumerate(rows):
            for a, b in product(range(4), repeat=2):
                f = dict(enumerate(row)) | {5:a, 6:b}
                sizes = [4-len({f[w] for w in ns[v]-pv}) for v in p['vertices']]
                inner = [len(ns[v]&pv) for v in p['vertices']]
                if any(s>d for s,d in zip(sizes,inner)):
                    slack_checks.append(ev(piece=p['id'],row=qi,pins=[a,b],ok=bool(p['rows'][qi]['fibres'][4*a+b]['tuple_indices']),list_sizes=sizes,internal_degrees=inner))
    add('C13', slack_checks, '局部lists全tight；無slack實例')
    side_slack = []
    for d in g['root_deletions']:
        sv,se=set(d['side_vertices']),set(map(tuple,d['side_edges']))
        sn=ns_of(sv,se); r=11-d['absent']
        if len(sn[r])<=3:
            side_slack.append(ev(root=r,degree=len(sn[r]),ok=d['side_sigma']==1023))
    add('C14',side_slack,'沒有root-degree≤3的完整側')
    add('C4', [ev(piece=p['id'], ok=not p['short'] and len(p['support']) >= 3 and len(p['shield']['edges']) >= 2) for p in unary if fulltouch], '未碰齊五框點，或無 unary')
    add('C5', [ev(ok=sum(len(p['shield']['edges']) for p in sided) <= 5, total=sum(len(p['shield']['edges']) for p in sided))], '')
    add('C6', [ev(ok=g['u'] <= 2)] if fulltouch else [], '未碰齊五框點')
    u2 = []
    if fulltouch and g['u'] == 2:
        lens = sorted(len(p['shield']['edges']) for p in unary)
        forbidden = set().union(*(set(p['shield']['interiors']) for p in unary))
        used = {v for r in ROOTS for v in ns[r] & B} | {v for p in mixed for v in p['support']}
        u2.append(ev(ok=lens in ([2,2],[2,3]) and not(used & forbidden), lengths=lens, forbidden=sorted(forbidden), other_used=sorted(used)))
    add('C7', u2, '未碰齊五框點，或 u≠2')
    add('C8', [ev(piece=p['id'], ok=len(p['shield']['edges']) >= 2) for p in mixed if p['one_sided'] and not p['short']], '無 one-sided long mixed')
    capacity = []
    if fulltouch and g['m'] >= 2:
        long = [p for p in mixed if not p['short']]
        charged = sum(len(p['shield']['edges']) for p in long+unary) + sum(len(p['support']) == 2 for p in mixed if p['short'])
        capacity.append(ev(ok=len(long)+g['u'] <= 2 and charged <= 5, long=len(long), unary=g['u'], charged=charged))
    add('C9', capacity, '未碰齊五框點，或 m<2')
    diagonals = [ev(piece=p['id'], row=qi, pins=[a,a], ok=bool(p['rows'][qi]['fibres'][5*a]['tuple_indices']))
                 for p in mixed if fulltouch and p['one_sided'] and p['short'] for qi in range(10) for a in range(4)]
    add('C10', diagonals, '未碰齊五框點，或無 one-sided short mixed')
    add('C11', [ev(row=qi, ok=bool(g['sigma'] >> qi & 1)) for qi in SINGLETON] if fulltouch and g['m']==2 and not unary and all(p['short'] for p in mixed) else [], 'm≠2／有 unary／未全框／並非兩份都短；仍缺控制')
    add('C12', [ev(row=j['index'], ok=not(set(j['side_available']['5']) & set(j['side_available']['6'])))
                for j in g['joins'] if not g['sigma'] >> j['index'] & 1]
        if fulltouch and all(p['one_sided'] and p['short'] for p in mixed) else [], '未全框，或存在 separating／long mixed')
    add('D1', [ev(root=d['absent'], ok=d['sigma']==d['side_sigma']) for d in g['root_deletions']], '')
    pin_deletions=[]
    for d in g['root_deletions']:
        absent=d['absent']; other=11-absent
        dv=vv-{absent}; de={e for e in ee if absent not in e}
        sv,se=set(d['side_vertices']),set(map(tuple,d['side_edges']))
        for qi,row in enumerate(rows):
            for a in range(4):
                fixed=dict(enumerate(row))|{other:a}
                df=e4c_colorings(dv,de,fixed,first_only=True)
                sf=e4c_colorings(sv,se,fixed,first_only=True)
                pin_deletions.append(ev(root=other,row=qi,pin=a,ok=bool(df)==bool(sf),deleted_lift=[df[0][v] for v in sorted(dv)] if df else None,side_lift=[sf[0][v] for v in sorted(sv)] if sf else None))
    add('D1a',pin_deletions,'')
    add('D2', [ev(root=d['absent'], ok=d['mixed_incidence']==1 and len(q_of(d['side_sigma']))==1)
               for d in g['root_deletions'] if d['side_sigma'] != 1023], '兩份原 root-deletion 都全收')
    add('D3', [ev(ok=sum(10-d['sigma'].bit_count() for d in g['root_deletions']) <= 1)], '')
    add('D4', [ev(root=d['absent'], ok=d['sigma']==1023) for d in g['root_deletions']] if g['m']>=2 else [], 'm<2')
    allcores = [(entry['index'],c) for entry in g['row_cores'] for c in entry['cores']]
    core_basic=[]
    root_omit=[]
    for qi,c in allcores:
        cv,ce=set(c['vertices']),set(map(tuple,c['edges']))
        cn=ns_of(cv,ce)
        edge_sigmas=[e4c_sigma(cv,ce-{tuple(e['edge'])},rows)[0] for e in c['edge_deletion_witnesses']]
        core_basic.append(ev(row=qi,ok=len(comps(cv-B,ce))==1 and all(len(cn[v])>=4 for v in cv-B) and all(m!=c['sigma'] for m in edge_sigmas),deletion_sigmas=edge_sigmas))
        if None in c['root_degrees']:
            present=[r for r,dg in zip(ROOTS,c['root_degrees']) if dg is not None]
            r=present[0] if len(present)==1 else None
            root_omit.append(ev(row=qi,ok=len(present)==1 and g['m']==1 and len(mixed[0]['contacts'][r])==1 and c['root_degrees'][ROOTS.index(r)]==4 and len(q_of(c['sigma']))==1))
    add('D13',core_basic,'没有拒絕列')
    add('D14',root_omit,'所有minimal qcores均保留兩roots；仍缺控制')
    add('D4a',[ev(root=d['absent'],ok=d['sigma']==1023) for d in g['root_deletions'] if d['mixed_incidence']>=2], '兩側mixed incidence皆<2')
    add('D5', [ev(row=qi, core_vertices=c['vertices'], ok=all((set(p['vertices']) <= set(c['vertices']) and all(tuple(e) in set(map(tuple,c['edges'])) for e in g['edges'] if set(e)&set(p['vertices'])))
                    or not(set(p['vertices'])&set(c['vertices'])) for p in ps)) for qi,c in allcores], '沒有拒絕列')
    identities = []
    core44 = []
    path44 = []
    triangle44 = []
    exact_sides = []
    low_side = []
    for qi,c in allcores:
        degrees = c['root_degrees']
        if None in degrees:
            present = [r for r,d in zip(ROOTS,degrees) if d is not None]
            expected = next(d for d in g['root_deletions'] if d['absent'] not in present)
            identities.append(ev(row=qi, ok=c['vertices']==expected['side_vertices'] and set(map(tuple,c['edges']))==set(map(tuple,expected['side_edges']))))
            continue
        omitted = set(map(tuple,c['omitted_edges']))
        fs = [f for f in ([dict(id=f's{r}_{b}', incidence=[int(r==5),int(r==6)], edges=[tuple(sorted((r,b)))]) for r in ROOTS for b in ns[r]&B]
              + [dict(id=p['id'],incidence=p['incidences'],edges=[tuple(e) for e in g['edges'] if set(e)&set(p['vertices'])]) for p in ps]) if set(f['edges']) <= omitted]
        total = [sum(f['incidence'][i] for f in fs) for i in range(2)]
        retained_mixed = [p for p in mixed if p['id'] in c['retained_pieces']]
        correct = total == [5-d for d in degrees] and set().union(*(set(f['edges']) for f in fs)) == omitted if fs else not omitted and degrees==[5,5]
        correct = correct and bool(retained_mixed)
        if degrees==[5,5]: correct = correct and c['vertices']==list(g['vertices']) and set(map(tuple,c['edges']))==set(map(tuple,g['edges']))
        elif degrees in ([4,5],[5,4]): correct = correct and len(fs)==1 and sum(fs[0]['incidence'])==1
        elif degrees==[4,4]: correct = correct and (len(fs)==2 and sorted(f['incidence'] for f in fs)==[[0,1],[1,0]] or len(fs)==1 and fs[0]['incidence']==[1,1])
        else: correct = False
        identities.append(ev(row=qi, ok=correct, root_degrees=degrees, omitted_factors=[f['id'] for f in fs]))
        if degrees==[4,4]:
            core44.append(ev(row=qi, ok=len(retained_mixed)==1 and all(n<=2 for n in retained_mixed[0]['incidences']), retained=[p['id'] for p in retained_mixed]))
            p44=retained_mixed[0] if len(retained_mixed)==1 else None
            if p44:
                double2=True
                if p44['incidences']==[2,2]:
                    own=set(p44['vertices']); pe=set(map(tuple,p44['internal_edges']))
                    zpair,wpair=set(p44['contacts'][5]),set(p44['contacts'][6])
                    double2=len(own)==4 and zpair|wpair==own and not(zpair&wpair) and len(pe)==3
                    double2=double2 and len([e for e in pe if set(e)&zpair and set(e)&wpair])==1 and set(c['vertices'])-B==set(ROOTS)|own
                triangle44.append(ev(row=qi,ok=double2 and all(len(p44['contacts'][r])<2 or tuple(p44['contacts'][r]) in ee for r in ROOTS)
                    and (p44['incidences']!=[2,2] or not(set(p44['contacts'][5])&set(p44['contacts'][6])))))
            if g['m']==1 and mixed[0]['incidences']==[2,2]:
                p=mixed[0]; pe={tuple(e) for e in p['internal_edges']}; pn=ns_of(p['vertices'],pe)
                ends=sorted(v for v in p['vertices'] if len(pn[v])==1)
                zpair,wpair=set(p['contacts'][5]),set(p['contacts'][6])
                cross=[e for e in pe if set(e)&zpair and set(e)&wpair]
                path44.append(ev(row=qi, ok=len(p['vertices'])==4 and len(pe)==3 and len(ends)==2
                    and not(zpair&wpair) and zpair|wpair==set(p['vertices'])
                    and tuple(sorted(zpair)) in pe and tuple(sorted(wpair)) in pe and len(cross)==1
                    and set(c['vertices'])-B==set(ROOTS)|set(p['vertices'])
                    and all(len(ns_of(c['vertices'],set(map(tuple,c['edges'])))[r]&B)==2 for r in ROOTS)
                    and all(len(ns[v]&B)==(2 if v in ends else 1) for v in p['vertices'])))
                for r in ROOTS:
                    sv=B|{r}|{v for u in unary if r in u['owners'] for v in u['vertices']}; se={e for e in ee if set(e)<=sv}
                    sm,sw=e4c_sigma(sv,se,rows)
                    own_unary=[u for u in unary if r in u['owners']]
                    spokes=len(ns[r]&B)
                    exact_sides.append(ev(root=r,ok=(spokes==3 and not own_unary) or (spokes==2 and len(own_unary)==1 and len(own_unary[0]['contacts'][r])==1 and own_unary[0]['id'] in c['omitted_pieces']),spokes=spokes,unary=[u['id'] for u in own_unary]))
                    low_side.append(ev(root=r, ok=len(ns_of(sv,se)[r])==3 and sm==1023, sigma=sm, witnesses=sw))
    add('D6', identities, '沒有拒絕列')
    add('D7', core44, '沒有兩-root (4,4) minimal core；仍缺控制')
    add('D7a',triangle44,'沒有兩-root44 core；原triangle／directbridge身份仍缺控制')
    add('D9a',exact_sides,'沒有sole mixed22＋44 core；side exact兩型仍缺控制')
    add('D8', path44, '沒有 sole mixed22＋(4,4) core；仍缺控制')
    add('D9', low_side, '沒有 sole mixed22＋(4,4) core；仍缺控制')
    terminal=[]; side_topology=[]
    for qi,c in allcores:
        if c['root_degrees']==[4,4] and g['m']==1 and mixed[0]['incidences']==[2,2]:
            p=mixed[0]; pn=ns_of(p['vertices'],set(map(tuple,p['internal_edges'])))
            ends=[v for v in p['vertices'] if len(pn[v])==1]
            for rejected in range(10):
                if not g['sigma']>>rejected&1:
                    terminal.append(ev(row=rejected,ok=all(len({rows[rejected][v] for v in ns[x]&B})==2 for x in ends),ends=ends))
            for e in p['internal_edges']:
                hc=comps(h,ee-{tuple(e)})
                if len(hc)==2 and all(len(set(cc)&set(ROOTS))==1 for cc in hc):
                    sh=[shield(vv,ee,g['rotation'],cc) for cc in hc]
                    side_topology.append(ev(row=qi,bridge=e,ok=all(x['continuous'] and x['support_incident'] and x['outside_avoids_interiors'] for x in sh) and not(set(map(tuple,sh[0]['edges']))&set(map(tuple,sh[1]['edges']))),shields=sh))
    add('D15',terminal,'沒有sole mixed22＋(4,4) core；單列terminal步驟仍缺控制')
    add('D16',side_topology,'沒有sole mixed22＋(4,4) core；整側盾弧步驟仍缺控制')
    generic_side=[]
    for e in sorted(he):
        hc=comps(h,he-{e})
        if len(hc)==2 and all(len(set(cc)&set(ROOTS))==1 for cc in hc):
            sh=[shield(vv,ee,g['rotation'],cc) for cc in hc]
            generic_side.append(ev(bridge=e,ok=all(x['continuous'] and x['support_incident'] and x['outside_avoids_interiors'] for x in sh) and not(set(map(tuple,sh[0]['edges']))&set(map(tuple,sh[1]['edges'])))
                 and (not fulltouch or all(x['support']==x['vertices'] for x in sh if len(x['support'])>=2)),shields=sh))
    add('D16a',generic_side,'原H無把兩roots分開的bridge；generic整側盾弧仍缺控制')
    add('D10', [ev(factors=d['factors'], ok=d['epsilon'] in (0,1) and {tuple(e) for e in d['edges'] if set(e)<=B}==FRAME and d['sigma']&932==932 and d['minimal']['sigma']==d['sigma'] and all(x['sigma']!=d['sigma'] for x in d['minimal']['deletions'])
                   and all(len(n)>=4 for v,n in ns_of(d['minimal']['vertices'],d['minimal']['edges']).items() if v not in B)) for d in g['derivatives']], '沒有有效 unit derivative')
    add('D11', [ev(factors=d['factors'], ok=d['epsilon']-d['minimal']['epsilon']==sum(d['epsilon_difference_terms']) and min(d['epsilon_difference_terms'])>=0) for d in g['derivatives']], '沒有有效 unit derivative')
    add('D12', [ev(factors=d['factors'], epsilon=d['epsilon'], Q=q_of(d['sigma']), ok=d['epsilon'] in (0,1) and (len(q_of(d['sigma']))<=1 if d['epsilon']==0 else len(q_of(d['sigma']))<=1 or len(q_of(d['sigma']))==2 and tuple(sorted(q_of(d['sigma']))) in FRAME)) for d in g['derivatives']], '沒有有效 ε≤1 derivative')
    add('D12a',[ev(factors=d['factors'],ok=not(not d['sigma']>>1&1 and (not d['sigma']>>4&1 or not d['sigma']>>6&1))) for d in g['derivatives']], '沒有有效unit derivative')
    private_checks=[]; duplicate_checks=[]
    for r in ROOTS:
        for b in sorted(ns[r]&B):
            private_rows=[qi for qi in range(10) if not g['sigma']>>qi&1 and all(rows[qi][b]!=rows[qi][v] for v in (ns[r]&B)-{b})]
            private_checks.append(ev(root=r,spoke=b,ok=bool(private_rows),private_rows=private_rows))
        for qi,row in enumerate(rows):
            dup=[b for b in ns[r]&B if any(row[b]==row[v] for v in (ns[r]&B)-{b})]
            for b in sorted(dup):
                ds=next(d['sigma'] for d in g['deletions'] if tuple(d['edge'])==tuple(sorted((r,b))))
                duplicate_checks.append(ev(root=r,spoke=b,row=qi,ok=bool(ds>>qi&1)==bool(g['sigma']>>qi&1)))
    gains_private=[]
    for d in g['deletions']:
        e=tuple(d['edge'])
        if len(set(e)&B)==1 and len(set(e)&set(ROOTS))==1:
            r=next(v for v in e if v in ROOTS); b=next(v for v in e if v in B)
            for qi in d['gained']:
                gains_private.append(ev(root=r,spoke=b,row=qi,ok=all(rows[qi][b]!=rows[qi][v] for v in (ns[r]&B)-{b})))
    add('E2a',gains_private,'')
    add('E1',duplicate_checks,'沒有任何重色 spoke')
    add('E2',private_checks,'')
    e3=[]
    for qi,c in allcores:
        cn=ns_of(c['vertices'],c['edges'])
        e3.append(ev(row=qi,ok=all(len({rows[qi][v] for v in cn[r]&B})==len(cn[r]&B) for r in ROOTS if r in cn)))
    add('E3',e3,'沒有拒絕列')
    e4=[]
    if g['m']==2:
        for qi in range(10):
            if g['sigma']>>qi&1: continue
            duplicates=[r for r in ROOTS if len({rows[qi][v] for v in ns[r]&B})<len(ns[r]&B)]
            cs=g['row_cores'][qi]['cores']
            ok=len(duplicates)<=1
            if len(duplicates)==1:
                r=duplicates[0]; pair=[v for v in ns[r]&B if any(rows[qi][v]==rows[qi][w] for w in (ns[r]&B)-{v})]
                ok=ok and all(len(c['omitted_edges'])==1 and tuple(c['omitted_edges'][0]) in {tuple(sorted((r,v))) for v in pair}
                              and c['root_degrees']==([4,5] if r==5 else [5,4]) for c in cs)
            e4.append(ev(row=qi,ok=ok,duplicate_roots=duplicates))
    add('E4',e4,'m≠2')
    exact_duplicate=[item for item in e4 if item['duplicate_roots']]
    add('E5',exact_duplicate,'所有m=2拒絕列都無重色spokes；exact spoke core仍缺控制')
    # Literal selected-triple deductions are listed separately, not generalized.
    triple=all(not g['sigma']>>qi&1 for qi in SELECTED)
    add('T1', [ev(ok=all(any(all(rows[qi][b]!=rows[qi][v] for v in (ns[r]&B)-{b}) for qi in SELECTED) for r in ROOTS for b in ns[r]&B) and all(ns[r]&B not in ({0,2,4},{1,2,4}) for r in ROOTS))] if triple else [], '指定 q₀、q₁、q₃ 並非全拒絕；024／124 的三列排除不適用')
    add('T2', [ev(ok=False)] if triple and path44 else [], 'N1-22-44 整類排除／真框邊／整側盾弧≥3 需要指定三列；所有控制不滿足')
    return cells


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); parser.add_argument('--output',type=Path,default=OUT)
    args=parser.parse_args()
    rows=[tuple(row) for row in json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())['pattern_order']]
    paths=[p for k in range(6,10) for p in sorted((ROOT/f'artifacts/c5_excess_two_finite_search/NA_k{k}_validate/crit_orbits').glob('orbit_*.json'))]
    assert len(paths)==54
    hex1='01 04 05 06 07 08 12 15 25 23 34 39 3a 47 49 58 5a 67 68 69 6a 79 8a'
    hex3='01 04 05 06 07 08 12 15 25 29 23 34 36 39 46 57 59 68 6a 78 7a 8a 9a'
    def hexedges(s): return {tuple(sorted(int(c,16) for c in e)) for e in s.split()}
    guide_graphs={1:hexedges(hex3),2:hexedges(hex1),3:hexedges(hex1)-{(0,6)}|{(3,6)}}
    for p in paths[:3]:
        assert set(map(tuple,json.loads(p.read_text())['canonical_edges']))==guide_graphs[int(p.stem.split('_')[-1])]
    results=[]; produced=[]; failure=None
    for path in paths:
        g=graph_data(path,rows); results.append(g)
        produced.append((f'controls/{g["id"]}.json',encoded(g)))
        failures=[dict(lemma=key,cell=cell) for key,cell in g['lemmas'].items() if cell['status']=='反例']
        if failures:
            failure=dict(control=g['id'], graph_vertices=g['vertices'],graph_edges=g['edges'],source=g['source'],failures=failures,
                         impact='Only identified E4 lemma dependencies are challenged; do not modify E4.')
            produced.append(('counterexample.json',encoded(failure)))
            break
    assert set(results[0]['lemmas']) == set(CATALOG)
    counts={key:dict(Counter(g['lemmas'][key]['status'] for g in results)) for key in results[0]['lemmas']}
    summary=dict(schema='c5-e4c-controls-v1', baseline='d00aba4e10ea2d05ab216fedd94f5a166b2777ad',
                 source_hashes={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in ('scripts/c5_excess_two_e4c_controls.py','artifacts/c5_cells/cells.json','artifacts/c5_excess_two_e4/REPORT.md','artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md','artifacts/c5_excess_two_e3/nonadjacent_notes.md','docs/c5_unary_shield_budget.md','docs/c5_kempe_guide.md')},
                 guide_aliases={'NA6-1':'NA6-0002','NA6-2':'NA6-0003','NA6-3':'NA6-0001'}, lemma_catalog=CATALOG, patterns=rows, controls=[dict(id=g['id'],source=g['source'],sha256=g['source_sha256'],sigma=g['sigma'],Q=g['Q'],m=g['m'],u=g['u'],touch=g['touch'],lemmas={k:dict(status=v['status'],reason=v['reason']) for k,v in g['lemmas'].items()}) for g in results],
                 lemma_counts=counts,still_missing=[k for k,c in counts.items() if not c.get('成立')],
                 counterexample=failure,processed=len(results),expected_controls=54,
                 core_degree_counts={str(k):v for k,v in sorted(Counter(tuple(c['root_degrees']) for g in results for row in g['row_cores'] for c in row['cores']).items())},
                 total_rejected_row_cores=sum(len(row['cores']) for g in results for row in g['row_cores']),
                 output_hashes={p:dict(bytes=len(raw),sha256=sha256(raw).hexdigest()) for p,raw in produced})
    produced.append(('summary.json',encoded(summary)))
    for name,raw in produced:
        path=args.output/name
        if args.check:
            if path.read_bytes()!=raw: raise AssertionError(f'byte replay differs: {path}')
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as f: f.write(raw)
    print(('CHECKED' if args.check else 'GENERATED')+f' {len(results)}/54 controls; {summary["total_rejected_row_cores"]} row cores; {len(produced)} byte files; counterexample={bool(failure)}')
    return 2 if failure else 0


if __name__=='__main__':
    raise SystemExit(main())
