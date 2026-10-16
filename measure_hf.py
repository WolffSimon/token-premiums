import json, sys, unicodedata
from tokenizers import Tokenizer
langs = ["eng","arb","urd","hin","nep","ben","tam","mal","tgl","kat"]
texts = {l: unicodedata.normalize("NFC", open(f"corpus/udhr2/{l}.txt", encoding="utf8").read()) for l in langs}
out = {}
for m in ["gemma3","qwen3","llama3"]:
    tk = Tokenizer.from_file(f"node_modules/@lenml/tokenizer-{m}/models/tokenizer.json")
    res = {}
    for l,t in texts.items():
        enc = tk.encode(t, add_special_tokens=False)
        rt = tk.decode(enc.ids, skip_special_tokens=False) == t
        res[l] = {"tokens": len(enc.ids), "roundtrip": rt}
    out[m] = res
json.dump(out, open("hf_counts.json","w"), indent=1)
print(json.dumps({m:{l:v["tokens"] for l,v in r.items()} for m,r in out.items()}))
print({m:[l for l,v in r.items() if not v["roundtrip"]] for m,r in out.items()})
