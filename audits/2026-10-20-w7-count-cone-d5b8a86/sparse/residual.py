#!/usr/bin/env python3
"""Export and exactly price a rounded exploratory dual. Never a cone verdict."""
import argparse,gzip,hashlib,json,math,pickle
from collections import Counter
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parent;S=P.parents[1]/'2026-10-20-r6-941-j1-five-edge-417732f/counting'
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('result',type=Path);args=ap.parse_args();d=pickle.load(args.result.open('rb'));out=args.result.parent
 o=json.load(gzip.open(S/'orbits.json.gz','rt'));live=o['live'];li={s:i for i,s in enumerate(live)};sr={s:[] for s in live}
 for r,s in o['rowids']:
  if s in sr:sr[s].append(r)
 for rs in sr.values():rs.sort()
 y={i:Fraction(v).limit_denominator(1000000) for i,v in enumerate(d['full_row_dual']) if abs(v)>1e-9};den=math.lcm(*(v.denominator for v in y.values()));ints={i:int(v*den) for i,v in y.items()};g=math.gcd(*ints.values());scale=Fraction(den,g);ints={i:v//g for i,v in ints.items()}
 rc={}
 for s,rs in sr.items():
  i=li[s];rc[rs[0]]=ints.get(2*i,0);rc[rs[1]]=ints.get(2*i+1,0);rc[rs[2]]=-ints.get(2*i,0)-ints.get(2*i+1,0)
 tr=2*len(live);targetref=sr[d['target']][2];prices=[]
 for col in o['columns']:
  prices.append(sum(rc[r] for r in col)+ints.get(tr,0)*(targetref in col))
 last=d['history'][-1];n=last['columns'];selected=d['selected_columns'][:n];violators=[[j,v] for j,v in enumerate(prices) if v>0]
 halfweights=dict(rc);halfweights[targetref]+=ints.get(tr,0)
 stateweights=[[s,2*sum(halfweights[r] for r in sr[s])] for s in live]
 payload={'status':'exploratory exact residual; positive-priced columns prohibit this from being a full-cone dual certificate','target':d['target'],'target_reference_halfrow':targetref,'direction':'A times X = b; desired Farkas y has b.y > 0 and all A_col.y <= 0','row_reference':'sorted halfrow index2 per live canonical state','integer_dual_terms':sorted(ints.items()),'halfrow_integer_weights':sorted((r,v) for r,v in halfweights.items() if v),'state_integer_coefficients':stateweights,'exact_conservation':'sum(state_coefficient[s] * Z[s]) = sum(column_price[j] * X[j])','rounded_rational_to_integer_scale':str(scale),'target_dual_integer':ints.get(tr,0),'all_column_integer_prices':prices,'positive_price_columns':violators,'selected_columns':selected,'selected_positive_prices':[[j,prices[j]] for j in selected if prices[j]>0],'source_orbits_sha256':hashlib.sha256((S/'orbits.json.gz').read_bytes()).hexdigest(),'numerical_stop':last}
 raw=canonical(payload);artifact=out/'exact-dual-residual.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));summary={k:v for k,v in payload.items() if k not in ('all_column_integer_prices','positive_price_columns','selected_columns','integer_dual_terms','halfrow_integer_weights','state_integer_coefficients')};summary.update({'integer_dual_support':len(ints),'halfrow_weight_support':sum(bool(v) for v in halfweights.values()),'nonzero_state_coefficients':[[s,v] for s,v in stateweights if v],'positive_price_columns_count':len(violators),'maximum_integer_price':max(prices),'integer_price_histogram':dict(Counter(prices)),'artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()});(out/'exact-dual-residual-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
