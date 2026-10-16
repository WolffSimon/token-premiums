# Parity premium: tokens for a language divided by tokens for English on the same tokenizer.
import json
counts = {**json.load(open("gpt_counts.json")), **json.load(open("hf_counts.json"))}
order = ["cl100k", "o200k", "llama3", "qwen3", "gemma3"]
langs = ["arb", "urd", "hin", "nep", "ben", "tam", "mal", "tgl", "kat"]
prem = {l: {m: round(counts[m][l]["tokens"] / counts[m]["eng"]["tokens"], 2) for m in order} for l in langs}
assert all(v["roundtrip"] for m in counts.values() for v in m.values()), "a tokenizer failed to round-trip"
json.dump(prem, open("premiums.json", "w"), indent=1)
with open("premiums.csv", "w") as f:
    f.write("language," + ",".join(order) + "\n")
    for l in langs:
        f.write(l + "," + ",".join(str(prem[l][m]) for m in order) + "\n")
print(open("premiums.csv").read())
