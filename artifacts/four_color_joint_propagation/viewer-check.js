const fs = require('node:fs');
const path = require('node:path');
const zlib = require('node:zlib');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const artifact = process.argv[2] || 'artifacts/four_color_joint_propagation';
const html = fs.readFileSync('tools/four_color_lab_viewer.html', 'utf8');
const runtime = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
new vm.Script(runtime);
const start = runtime.indexOf('  function drawConstraints(event) {');
const end = runtime.indexOf('  function drawConflictSubgraph(event) {', start);
assert(start >= 0 && end > start);
const functionCode = runtime.slice(start, end);
const helperNames = ['constraints', 'isLocalC5', 'isStructuralC5', 'c5Action', 'isC5Event'];
const helperCode = helperNames.map(name => runtime.split('\n').find(line => line.startsWith(`  const ${name} =`))).join('\n');
assert.equal(helperCode.split('\n').length, helperNames.length);
const report = JSON.parse(fs.readFileSync(path.join(artifact, 'report.json'), 'utf8'));
const panels = [];
let inspected = 0;
function node(tag = 'div') {
 return {tag, textContent:'', hidden:false, children:[], style:{}, append(...children) { this.children.push(...children); }, replaceChildren(...children) { this.children = children; }, setAttribute(key, value) { this[key] = value; }};
}
for (const item of report.cases) {
 const record = item.results.joint;
 const run = JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(artifact, record.full_record))));
 const nodes = new Map();
 const get = id => {if (!nodes.has(id)) nodes.set(id, node()); return nodes.get(id);};
 const context = vm.createContext({run, step:0, $:get, document:{createElement:node}, palette:['a','b','c','d']});
 new vm.Script(helperCode + '\n' + functionCode + '\nthis.drawConstraints = drawConstraints;').runInContext(context);
 for (let index = 0; index < run.events.length; index++) {
  const event = run.events[index];
  if (event.relation_kind !== 'joint_constraint') continue;
  context.step = index;
  context.drawConstraints(event);
  assert.equal(get('relation-title').textContent, '九點構型推出的三點等色關係');
  assert.equal(get('relation-table').hidden, false);
  assert.equal(get('c5-table').hidden, true);
  assert.equal(get('relation-color-head').textContent, '共同支援');
  assert.equal(get('relation-body').children.length, 4);
  for (const row of get('relation-body').children) assert.equal(row.children[1].textContent, '三點同色');
  assert(get('relation-note').textContent.includes('尚未消去頂點或寫色'));
  assert(get('phase-written').textContent.startsWith('新寫入顏色：0 /'));
  panels.push({case:item.name,event_index:index,frontier:event.frontier,rows:4});
  inspected++;
 }
}
assert.equal(inspected, 10);
const receipt = {status:'PASS',kind:'Node VM syntax and original drawConstraints function with minimal DOM; no browser layout coverage',syntax_verified:true,joint_panels:inspected,panels,browser_rendering:'not run: Chromium could not start in this sandbox (shutdown EPERM)'};
fs.writeFileSync(path.join(artifact, 'viewer-verification.json'), JSON.stringify(receipt,null,2)+'\n');
process.stdout.write(JSON.stringify({syntax:true,joint_panels:inspected})+'\n');
