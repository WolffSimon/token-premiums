import fs from 'fs';
import * as o200k from 'gpt-tokenizer/encoding/o200k_base';
import * as cl100k from 'gpt-tokenizer/encoding/cl100k_base';
const langs = ["eng","arb","urd","hin","nep","ben","tam","mal","tgl","kat"];
const out = {};
for (const [name, enc] of [["o200k", o200k], ["cl100k", cl100k]]) {
  out[name] = {};
  for (const l of langs) {
    const t = fs.readFileSync(`corpus/udhr2/${l}.txt`, 'utf8').normalize('NFC');
    const ids = enc.encode(t);
    out[name][l] = { tokens: ids.length, roundtrip: enc.decode(ids) === t };
  }
}
fs.writeFileSync('gpt_counts.json', JSON.stringify(out, null, 1));
console.log(JSON.stringify(Object.fromEntries(Object.entries(out).map(([k,v])=>[k,Object.fromEntries(Object.entries(v).map(([l,x])=>[l,x.tokens]))]))));
