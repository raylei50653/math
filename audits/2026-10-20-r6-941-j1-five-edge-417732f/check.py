#!/usr/bin/env python3
"""Connected read-only replay with frozen-source custody and exact scopes."""
from pathlib import Path
import argparse,gzip,hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent

def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def verify(rows,root):
 for row in rows:
  data=(root/row['path']).read_bytes()
  assert len(data)==row['bytes'],('size drift',row['path'])
  assert hashlib.sha256(data).hexdigest()==row['sha256'],('sealed drift',row['path'])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seal',type=Path,default=D/'OUTPUTS.json');a=ap.parse_args()
 inputs=json.loads((D/'INPUTS.json').read_text());seal=json.loads(a.seal.read_text())
 assert inputs['base']=='417732fc5ef0a012829fd6712333b1c906128d3a'
 verify(inputs['inputs'],D/'frozen');verify(seal,D)
 commands=json.loads((D/'REPLAYS.json').read_text());results=[]
 for command in commands:
  run=subprocess.run([sys.executable,'-B',str(D/command[0]),*command[1:]],capture_output=True,text=True)
  assert run.returncode==0,(command,run.stdout,run.stderr)
  events=[]
  for line in run.stdout.splitlines():
   try:events.append(json.loads(line))
   except json.JSONDecodeError:pass
  assert events,('no checker result',command)
  results.append({'command':command,'result':events[-1]})
 caps=json.load(gzip.open(D/'counting/caps.json.gz','rt'))
 independent=json.loads((D/'review/caps.json').read_text())
 assert hashlib.sha256(packed(caps['states'])).hexdigest()==independent['state_sha256']
 assert hashlib.sha256(packed(caps['matrices'])).hexdigest()==independent['matrices_sha256']
 verify(inputs['inputs'],D/'frozen');verify(seal,D)
 print(json.dumps({'status':'PASS connected exact W7 audit','frozen_inputs':len(inputs['inputs']),
  'sealed_outputs':len(seal),'results':results,'full_caps_independently_agree':True,
  'general_five_edge_source_excluded':False,'general_J1_excluded':False,
  'smaller_bad_constructed':False,'new_Lean':False},sort_keys=True))
if __name__=='__main__':main()
