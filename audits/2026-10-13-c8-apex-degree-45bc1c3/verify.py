#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
 out=HERE/'validation';out.mkdir(exist_ok=True);env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 commands=[('check',[sys.executable,'-B',str(HERE/'check.py'),'--check'],{}),('check.seed17',[sys.executable,'-B',str(HERE/'check.py'),'--check'],{'PYTHONHASHSEED':'17'}),('controls',[sys.executable,'-B',str(HERE/'controls.py')],{}),('review.support',[sys.executable,'-B',str(HERE/'review/check_support.py')],{}),('review.dual-c04',[sys.executable,'-B',str(HERE/'review/check_dual.py'),'dual-c04-a1.json'],{}),('review.dual-c07',[sys.executable,'-B',str(HERE/'review/check_dual.py'),'dual-c07-a4.json'],{})]
 results=[]
 for name,cmd,extra in commands:
  proc=subprocess.run(cmd,cwd=HERE,env=env|extra,text=True,capture_output=True)
  (out/(name+'.stdout')).write_text(proc.stdout);(out/(name+'.stderr')).write_text(proc.stderr)
  results.append({'name':name,'command':cmd,'environment_overrides':extra,'returncode':proc.returncode,'stdout':name+'.stdout','stderr':name+'.stderr'})
  print(name,proc.returncode,flush=True)
  assert proc.returncode==0,proc.stderr
 result={'schema':'c8-apex-verification-v1','checks':results,'all_pass':True}
 (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
