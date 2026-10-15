"""Exact GF(2) classification of two-sheet visible-cube covers."""
import itertools
PERMS=tuple(itertools.permutations(range(4)))
def canonical(s):
    order=''.join(dict.fromkeys(s)); order+=''.join(c for c in 'ABCD' if c not in order)
    return ''.join('ABCD'[order.index(c)] for c in s),tuple('ABCD'.index(c) for c in order)
def rename(s,p):return ''.join('ABCD'[p['ABCD'.index(c)]] for c in s)
def add(basis,value):
    while value:
        pivot=value.bit_length()-1
        if pivot in basis:value^=basis[pivot]
        else:basis[pivot]=value;return True
    return False
def rank(rows):
    b={}
    for v in sorted(rows):add(b,v)
    return len(b)
def nullspace(n,rows):
    b={}
    for v in sorted(rows):add(b,v)
    result=[]
    for free in range(n):
        if free in b:continue
        v=1<<free
        for p in sorted(b):
            if (b[p]&v).bit_count()%2:v^=1<<p
        result.append(v)
    return result

def layer_space(states):
    byid={s['id']:s for s in states};reps=sorted({canonical(s['literal_row'])[0] for s in states})
    frame={s['id']:(reps.index(canonical(s['literal_row'])[0]),canonical(s['literal_row'])[1]) for s in states}
    def key(a,b):
        ra,rb=byid[a]['literal_row'],byid[b]['literal_row']
        return min(tuple(sorted((rename(ra,p),rename(rb,p)))) for p in PERMS)
    edge={};keys=set()
    for s in states:
        for j,p in enumerate(s['pairings']):
            for bit in range(sum(map(len,p['terminal_parts']))):
                k=key(s['id'],p['cube_targets_by_bitmask'][1<<bit]);keys.add(k);edge[s['id'],j,bit]=k
    keys=sorted(keys);index={k:i for i,k in enumerate(keys)};edge={k:index[v] for k,v in edge.items()};squares=set()
    for s in states:
        for j,p in enumerate(s['pairings']):
            for a,b in itertools.combinations(range(sum(map(len,p['terminal_parts']))),2):
                x,y=p['cube_targets_by_bitmask'][1<<a],p['cube_targets_by_bitmask'][1<<b];mask=0
                for i in [edge[s['id'],j,a],edge[s['id'],j,b],edge[x,j,b],edge[y,j,a]]:mask^=1<<i
                squares.add(mask)
    products=[]
    for s in states:
        if s['literal_row']!=canonical(s['literal_row'])[0]:continue
        for j,p in enumerate(s['pairings']):
            offset=0
            for blocks in p['terminal_parts']:
                mask=0;current=s['id']
                for bit in range(offset,offset+len(blocks)):
                    mask^=1<<edge[current,j,bit];current=byid[current]['pairings'][j]['cube_targets_by_bitmask'][1<<bit]
                offset+=len(blocks);products.append(mask)
    gauges=[]
    for r in reps:
        gauges.append(sum(1<<i for i,(a,b) in enumerate(keys) if (canonical(a)[0]==r)!=(canonical(b)[0]==r)))
    gb={}
    for v in gauges:add(gb,v)
    joint=squares|set(products);ns=nullspace(len(keys),joint);span=dict(gb);quotient=[]
    for v in ns:
        if add(span,v):quotient.append(v)
    # Every claimed gauge is in both kernels; quotient spans the entire kernel.
    assert all(not (a&g).bit_count()%2 for a in joint for g in gauges)
    assert len(span)==len(ns)
    record={'canonical_rows':reps,'state_count':len(states),'edge_orbits':[list(k) for k in keys],
      'square_equations':sorted(squares),'square_rank':rank(squares),'gauge_vectors':gauges,'gauge_rank':rank(gauges),
      'cover_dimension':len(keys)-rank(squares),'quotient_dimension':len(keys)-rank(squares)-rank(gauges),
      'visible_product_equations':products,'joint_rank':rank(joint),'zero_product_dimension':len(keys)-rank(joint),
      'zero_product_quotient_basis':quotient,'zero_product_quotient_dimension':len(quotient)}
    return record,byid,frame,edge
