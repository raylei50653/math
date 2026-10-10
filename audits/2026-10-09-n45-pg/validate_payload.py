#!/usr/bin/env python3
"""Read-only delivery text/JSON/link validation; checks.json and manifest are planned seal outputs."""
from pathlib import Path
import json,re,sys
D=Path(__file__).resolve().parent
fail=[];count=0;links=0
for p in D.iterdir():
 if not p.is_file() or p.suffix not in ['.py','.md','.json','.svg']:continue
 count+=1;s=p.read_text()
 if not s.endswith('\n'):fail.append([p.name,'missing final newline'])
 for n,line in enumerate(s.splitlines(),1):
  if line.rstrip()!=line:fail.append([p.name,n,'trailing whitespace'])
 if p.suffix=='.json':json.loads(s)
 if p.suffix=='.md':
  for ref in re.findall(r'\]\(([^)]+)\)',s):
   if re.match(r'https?://',ref):continue
   path=ref.split('#')[0]
   if not path:continue
   links+=1
   if not (p.parent/path).exists() and path not in ['checks.json','MANIFEST.sha256']:fail.append([p.name,'missing local path',path])
print(json.dumps({'authored_text_files_checked':count,'REPORT_local_links_checked':links,'failures':fail},indent=2));sys.exit(bool(fail))
