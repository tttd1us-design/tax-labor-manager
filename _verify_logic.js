// Headless verification of the tax-labor-manager app logic using a minimal DOM stub.
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('C:/AI_산출물/개발/tax-labor-manager/prototype_20261013/index.html', 'utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
const js = m[1];

function El(id){ this.id=id; this.value=''; this.innerText=''; this.innerHTML='';
  this.style={}; this.className=''; this.classList={add(){},remove(){}};
  this.appendChild=()=>{}; this.click=()=>{}; this.href=''; this.download=''; }
const store = {};
const sandbox = {
  __els: {},
  console,
  document: {
    getElementById: (id) => (sandbox.__els[id] ||= new El(id)),
    querySelectorAll: () => [],
    createElement: () => new El('x'),
    body: { appendChild(){} },
  },
  window: {},
  localStorage: { getItem:k=>store[k]??null, setItem:(k,v)=>{store[k]=String(v)}, removeItem:k=>{delete store[k]} },
  sessionStorage: { getItem:()=>null, setItem(){} },
  alert: ()=>{}, confirm: ()=>true,
  setInterval: ()=>{}, setTimeout: (f)=>0,
  Blob: function(){}, URL: { createObjectURL:()=>'blob:x', revokeObjectURL(){} },
};
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(js, sandbox);

const S = sandbox;
const results = {};

// pure helpers
results.fmt = S.fmt(1234567);
results.tax_10m = S.incomeTaxByBracket(10000000).tax;      // expect 600000
results.tax_20m = S.incomeTaxByBracket(20000000).tax;      // expect 1740000
results.tax_60m = S.incomeTaxByBracket(60000000);          // rate .24 -> 60,000,000*.24-5,760,000=8,640,000
const defs = S.buildDefault();
results.default_schedule_count = defs.length;

// calculator outputs
function setVal(id,v){ S.__els[id] = new El(id); S.__els[id].value = String(v); }
function runCalc(type, vals){
  setVal('calc-type', type);
  for(const [k,v] of Object.entries(vals)) setVal(k,v);
  S.calculate();
  return (S.__els['calc-result'].innerHTML||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
}
results.vat_general = runCalc('vat', {"vat-supply":50000000, "vat-purchase":3000000});
results.vat_simple  = runCalc('vat-simple', {"vats-supply":40000000, "vats-rate":30});
results.income      = runCalc('income', {"income-annual":80000000,"income-expense":50000000,"income-deduct":1500000});
results.withholding = runCalc('withholding', {"wh-amount":3000000});
results.insurance   = runCalc('insurance', {"ins-month":3000000});

// disclaimer must appear inside a calc output
results.calc_has_disclaimer = results.income.includes('세무 대리 및 신고 대행 서비스를 제공하지 않으며');

console.log(JSON.stringify(results, null, 1));
