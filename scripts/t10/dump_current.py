"""Dump current Topic 10 content from content.json in readable form."""
import json

with open("/home/z/my-project/src/lib/site/content.json", encoding="utf-8") as f:
    data = json.load(f)

topics = data if isinstance(data, list) else data.get("topics", [])
t10 = None
for t in topics:
    if str(t.get("slug", "")) in ("halogenoalkanes-alcohols-spectra",) or str(t.get("number", "")) == "10":
        t10 = t
        break

if not t10:
    print("NOT FOUND"); raise SystemExit(1)

print("TOPIC:", t10.get("number"), t10.get("slug"), "|", t10.get("title"))
print("intro:", t10.get("intro", "")[:200])
print("estHours:", t10.get("estHours"), "| sections:", len(t10.get("sections", [])))
print("flashcards:", len(t10.get("flashcards", [])))
print("=" * 80)

def render_block(b, depth=2):
    pad = "  " * depth
    t = b.get("type")
    if t == "h3":
        print(f"\n{pad}[H3] {b.get('text','')}")
    elif t == "p":
        print(f"{pad}[P] {b.get('text','')}")
    elif t == "list":
        print(f"{pad}[LIST {b.get('ordered',False)}]")
        for it in b.get("items", []):
            print(f"{pad}  - {it if isinstance(it,str) else json.dumps(it, ensure_ascii=False)}")
    elif t == "callout":
        print(f"{pad}[CALLOUT {b.get('variant','')}] {b.get('title','')}: {b.get('text','')}")
    elif t == "figure":
        print(f"{pad}[FIGURE] {b.get('src','')} | caption: {str(b.get('caption',''))[:150]}")
    elif t == "table":
        print(f"{pad}[TABLE] {b.get('title','')}")
        for r in b.get("rows", []):
            cells = r.get("cells", r) if isinstance(r, dict) else r
            print(f"{pad}  | " + " | ".join(str(c) for c in cells))
    elif t == "worked":
        print(f"{pad}[WORKED {b.get('key','')}] {b.get('title','')}")
        print(f"{pad}  Q: {b.get('question','')}")
        for s in b.get("steps", []):
            print(f"{pad}  step: {s if isinstance(s,str) else json.dumps(s, ensure_ascii=False)[:300]}")
        print(f"{pad}  A: {b.get('answer','')}")
    else:
        print(f"{pad}[{t}] " + json.dumps({k: v for k, v in b.items() if k != 'type'}, ensure_ascii=False)[:400])

for sec in t10.get("sections", []):
    print(f"\n### SECTION {sec.get('number')} | {sec.get('title')} | estMinutes={sec.get('estMinutes')}")
    print(f"    specText: {str(sec.get('specText',''))[:220]}")
    print(f"    outline: {str(sec.get('outline',''))[:220]}")
    for b in sec.get("content", []):
        render_block(b)

print("\n\n===== FLASHCARDS =====")
for fc in t10.get("cards", []):
    print(f"- Q: {fc.get('front','')}\n  A: {fc.get('back','')}")
