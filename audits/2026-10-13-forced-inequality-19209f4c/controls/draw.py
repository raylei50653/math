"""Standalone SVG of literal graphs; positions do not encode graph distance."""
from pathlib import Path
import networkx as nx
from checker import path_cube

out = Path(__file__).resolve().parent / 'constructions.svg'
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480">',
         '<rect width="1200" height="480" fill="#f8fafc"/>',
         '<style>text{font-family:Arial,sans-serif;fill:#172033}.title{font-size:20px;font-weight:700}.note{font-size:14px}.node{font-size:12px;text-anchor:middle;dominant-baseline:central}</style>']
palette = ['#fb7185', '#60a5fa', '#fbbf24', '#86efac']

def text(x,y,value,kind='note'):
    parts.append(f'<text x="{x}" y="{y}" class="{kind}">{value}</text>')

def graph(edges, positions, colors=None, radius=13):
    for u,v in edges:
        x,y=positions[u]; a,b=positions[v]
        parts.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="#64748b" stroke-width="1.5"/>')
    for v,(x,y) in positions.items():
        color=palette[colors[v]] if colors else '#e2e8f0'
        parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="#0f172a" stroke-width="1.3"/>')
        text(x,y,str(v),'node')

text(30,35,'A. Stacked triangle chain','title')
g=path_cube(10)
pos=nx.planar_layout(g)
xs=[float(p[0]) for p in pos.values()]; ys=[float(p[1]) for p in pos.values()]
positions={v:(35+330*(float(p[0])-min(xs))/(max(xs)-min(xs)),
              80+280*(float(p[1])-min(ys))/(max(ys)-min(ys))) for v,p in pos.items()}
graph(g.edges,positions,{v:v%4 for v in g})
text(30,409,'All colorings: c(i) = c(i mod 4).')
text(30,432,'0 and 9 differ; graph distance = 3.')
text(30,455,'Continue stacking: no distance bound.')

text(425,35,'B. Shared two-color support','title')
positions={'a':(435,105),'b':(435,355)}
positions.update({f'x{i}':(475+55*i,230) for i in range(5)})
edges=[('a','b')]+[(h,f'x{i}') for h in ('a','b') for i in range(5)]+[(f'x{i}',f'x{i+1}') for i in range(4)]
colors={'a':0,'b':1,**{f'x{i}':2+i%2 for i in range(5)}}
graph(edges,positions,colors)
text(425,409,'The path alternates between two colors.')
text(425,432,'Its endpoints still have distance 2.')
text(425,455,'Shared support creates shortcuts.')

text(820,35,'C. A three-way fork fails','title')
positions={v:(855,105+i*110) for i,v in enumerate(('a','b','v'))}
positions.update({v:(1130,105+i*110) for i,v in enumerate(('x','y','z'))})
edges=[(u,v) for u in ('a','b','v') for v in ('x','y','z')]
graph(edges,positions)
text(820,409,'Two hubs a,b plus branch vertex v')
text(820,432,'connect to all three neighbors x,y,z.')
text(820,455,'This is K3,3: crossings are unavoidable.')
parts.append('</svg>')
with out.open('x') as stream:
    stream.write('\n'.join(parts)+'\n')
print(out)
