const assert=require('node:assert/strict'), fs=require('node:fs'), crypto=require('node:crypto');
const core=require('../assets/js/assessment-core.js');
const index=JSON.parse(fs.readFileSync('data/learning-audit/banks.json'));
let finals=0,units=0,items=0;
for(const c of index.courses){
 const banks=c.units.map(u=>{
  const bytes=fs.readFileSync(u.source);assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),u.sha256,`Stale bank ${u.source}`);
  const b=core.buildBank(JSON.parse(bytes));assert.equal(b.items.length,u.questions);assert.equal(b.blocked,u.blocked);
  for(const q of b.items){assert(q.answer.trim());assert(q.prompt.trim());assert(!/undefined|\[object Object\]/.test(q.prompt+q.answer+q.explanation));assert(q.source===u.source);assert(q.pointer.startsWith('/'));}items+=b.items.length;
  if(u.unit_test_available){for(let seed=0;seed<5;seed++)check(core.select([b],15,String(seed)),15,[u.unit]);units++;}
  if(u.blocked)assert.throws(()=>core.select([b],15,'blocked'));
  return b;
 });
 if(c.final_test_available){
  for(let seed=0;seed<30;seed++)check(core.select(banks,50,String(seed)),50,c.units.map(u=>u.unit));
  assert.deepEqual(core.select(banks,50,'same'),core.select(banks,50,'same'));
  assert.notDeepEqual(core.select(banks,50,'one').map(q=>q.id),core.select(banks,50,'two').map(q=>q.id));finals++;
 } else assert.throws(()=>core.select(banks,50,'blocked'));
}
function check(qs,n,expectedUnits){
 assert.equal(qs.length,n);assert.equal(new Set(qs.map(q=>q.id)).size,n);assert.equal(new Set(qs.map(q=>core.norm(q.prompt))).size,n);
 assert.deepEqual([...new Set(qs.map(q=>q.unit))].sort((a,b)=>a-b),[...expectedUnits].sort((a,b)=>a-b));
 assert(qs.filter(q=>q.kind==='glossary').length<=Math.floor(n*.4));
 for(const q of qs)if(q.options){assert.equal(q.options.length,4);assert.equal(new Set(q.options).size,4);assert.equal(q.options.filter(x=>x===q.answer).length,1);}
}
assert.throws(()=>core.select([],50,'empty'));assert.throws(()=>core.select([{unit:1,blocked:false,items:[]}],50,'short'));
console.log(JSON.stringify({finals,units,items}));

// This course has an internally reviewed blueprint: all 36 declared objectives
// must appear, rather than inferring coverage from unit presence alone.
const modeling=index.courses.find(c=>c.id==='modelado-simulacion-biomedicina');
const modelingBanks=modeling.units.map(u=>core.buildBank(JSON.parse(fs.readFileSync(u.source))));
for(const bank of modelingBanks){
 assert.equal(bank.items.length,60);assert.equal(bank.requiredObjectives.length,6);
 for(let seed=0;seed<40;seed++){
  const qs=core.select([bank],15,'unit-objectives-'+seed);
  for(const id of bank.requiredObjectives)assert(qs.some(q=>q.objectiveIds?.includes(id)),id);
 }
}
for(let seed=0;seed<100;seed++){
 const qs=core.select(modelingBanks,50,'final-objectives-'+seed);check(qs,50,[1,2,3,4,5,6]);
 for(const b of modelingBanks){
  for(const id of b.requiredObjectives)assert(qs.some(q=>q.unit===b.unit&&q.objectiveIds?.includes(id)),id);
  for(const kind of ['common_errors','worked_examples'])assert(qs.some(q=>q.unit===b.unit&&q.kind===kind));
 }
}
assert.throws(()=>core.select(modelingBanks,35,'insufficient-coverage'),/objetivo/);
const missing=JSON.parse(JSON.stringify(modelingBanks[0]));missing.items=missing.items.filter(q=>!q.objectiveIds?.includes('U1-LO1'));
assert.throws(()=>core.select([missing],15,'missing-objective'),/objetivo/);
