#!/usr/bin/env python3
"""Build static recipe pages (with schema.org Recipe JSON-LD) from Recipe Box data.
Usage: python3 build.py recipes.json out_dir [site_url]
"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art
from units import to_imperial
APP = "https://claude.ai/artifact/FUn136U2aoJBKZ9ieSs3Xf"

src, out = sys.argv[1], sys.argv[2]
SITE = (sys.argv[3] if len(sys.argv) > 3 else "https://85bcf57hnm-sketch.github.io/kitchen-cards").rstrip("/")
recipes = json.load(open(src, encoding="utf-8"))
os.makedirs(os.path.join(out, "img"), exist_ok=True)
try:
    import cairosvg
    EXT = "png"
    for k, svg in art.ART.items():
        cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(out, "img", k + ".png"), output_width=640, output_height=360)
except ImportError:
    EXT = "svg"
    for k, svg in art.ART.items():
        open(os.path.join(out, "img", k + ".svg"), "w").write(svg)
def img(r):
    k = r.get("art") if r.get("art") in art.ART else art.pick(r)
    return f"img/{k}.{EXT}"
e = lambda s: html.escape(str(s or ""), quote=True)

def slug(t, used):
    s = re.sub(r"[^a-z0-9]+", "-", (t or "recipe").lower()).strip("-")[:60] or "recipe"
    base, n = s, 2
    while s in used:
        s = f"{base}-{n}"; n += 1
    used.add(s)
    return s

def mins(m):
    if not m: return ""
    return f"{m} min" if m < 60 else f"{m//60} hr" + (f" {m%60} min" if m % 60 else "")

CSS = """
:root{color-scheme:light dark;--bg:#ececee;--card:#fff;--ink:#22201e;--mute:#6b645e;--red:#c7362b;--blue:#2856a8;--rule:#dfe6f3}
@media(prefers-color-scheme:dark){:root{--bg:#1c1816;--card:#2a2522;--ink:#efe9e4;--mute:#a89f98;--red:#ff6f61;--blue:#8fb0ff;--rule:#34405a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.55 "Work Sans",system-ui,-apple-system,sans-serif}
main{max-width:760px;margin:0 auto;padding:clamp(16px,4vw,40px)}
h1,h2{font-weight:700;letter-spacing:-.01em;line-height:1.1;margin:0}
h1{font-size:clamp(28px,6vw,44px);padding-bottom:12px;border-bottom:2px solid var(--red)}
h2{font-size:24px;margin:28px 0 10px}
a{color:var(--blue)}
.meta{color:var(--mute);margin:12px 0;display:flex;flex-wrap:wrap;gap:4px 16px}
.back{display:inline-block;margin-bottom:16px;font-weight:600;text-decoration:none}
ul.ing{list-style:none;padding:0;margin:0}ul.ing li{padding:8px 0;border-bottom:1px solid var(--rule)}
ul.ing li.hd{font-weight:600;border:0;padding-top:16px}
ol.steps{padding-left:1.4em;margin:0}ol.steps li{padding:6px 0 10px}ol.steps li::marker{color:var(--red);font-weight:600}
.notes{background:color-mix(in srgb,var(--blue) 9%,transparent);border-radius:8px;padding:14px 16px;margin-top:24px}
main.wide{max-width:1100px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),1fr));gap:14px;margin-top:18px}
.panel{display:flex;flex-direction:column;gap:6px;min-height:120px;padding:16px;border-radius:12px;text-decoration:none;color:var(--ink);
 background:var(--card);border:0;box-shadow:0 1px 2px rgba(0,0,0,.06),0 4px 14px -6px rgba(0,0,0,.18)}
.panel:active{transform:scale(.98)}
.panel .ty{color:var(--red);font-size:13px;font-weight:600}
.panel b{font-size:20px;line-height:1.2}
.panel span{color:var(--mute);font-size:14px;margin-top:auto}
.chips{display:flex;gap:8px;overflow-x:auto;margin-top:16px;scrollbar-width:none}
.chips button{flex:none;font:inherit;font-size:16px;font-weight:600;min-height:44px;padding:0 16px;border-radius:999px;border:0;background:var(--card);color:var(--ink)}
.chips button[aria-pressed=true]{background:var(--red);border-color:var(--red);color:#fff}
.chips small{opacity:.75;margin-left:6px;font-weight:500}
.panel{padding:0;overflow:hidden}.panel img{width:100%;height:90px;object-fit:cover;display:block}
.panel .pb{display:flex;flex-direction:column;gap:6px;padding:12px 16px 16px;flex:1}
.hero{width:100%;height:clamp(100px,22vw,150px);object-fit:cover;border-radius:12px;display:block;margin-bottom:18px}
.top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.top h1{flex:1;border:0;padding:0}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;background:var(--red);color:#fff;font-weight:600;text-decoration:none}
.bar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:16px}.bar .back{margin:0}
"""

def head(title, extra=""):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{e(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="icon" type="image/png" href="favicon.png">
<meta name="apple-mobile-web-app-title" content="My Recipe Box"><style>{CSS}</style>{extra}</head><body><main>"""

used, index = set(), []
for r in recipes:
    s = slug(r.get("title"), used)
    ings = [to_imperial(i) for i in (r.get("ingredients") or [])]
    r = {**r, "steps": [to_imperial(t) for t in (r.get("steps") or [])], "notes": to_imperial(r.get("notes") or "")}
    ld = {"@context": "https://schema.org", "@type": "Recipe", "name": r.get("title", ""),
          "recipeIngredient": [i for i in ings if not i.endswith(":")],
          "recipeInstructions": [{"@type": "HowToStep", "text": t} for t in (r.get("steps") or [])]}
    if r.get("serves"): ld["recipeYield"] = f'{r["serves"]} servings'
    if r.get("time"): ld["totalTime"] = f'PT{r["time"]}M'
    if r.get("course"): ld["recipeCategory"] = r["course"]
    if r.get("cuisine"): ld["recipeCuisine"] = r["cuisine"]
    if r.get("tags"): ld["keywords"] = ", ".join(r["tags"])
    if r.get("notes"): ld["description"] = r["notes"]
    ld["image"] = f"{SITE}/{img(r)}"
    ldj = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    meta = [x for x in [r.get("course"), r.get("cuisine"), mins(r.get("time")), f'Serves {r["serves"]}' if r.get("serves") else ""] if x]
    ing_html = "".join(f'<li class="hd">{e(i[:-1])}</li>' if i.endswith(":") else f"<li>{e(i)}</li>" for i in ings)
    steps_html = "".join(f"<li>{e(t)}</li>" for t in (r.get("steps") or []))
    srcline = ""
    if r.get("source"):
        sv = r["source"]
        srcline = f'<p style="color:var(--mute)">Source: ' + (f'<a href="{e(sv)}">{e(sv)}</a>' if re.match(r"https?://", sv) else e(sv)) + "</p>"
    page = head(r.get("title", "Recipe"), f'<script type="application/ld+json">{ldj}</script>') + f"""
<div class="bar"><a class="back" href="./">← My Recipe Box</a><a class="back" href="{APP}#{e(r.get('id',''))}">Edit in app</a></div>
<img class="hero" src="{img(r)}" alt="">
<h1>{e(r.get("title"))}</h1>
<div class="meta">{"".join(f"<span>{e(m)}</span>" for m in meta)}</div>
<h2>Ingredients</h2><ul class="ing">{ing_html}</ul>
<h2>Method</h2><ol class="steps">{steps_html}</ol>
{f'<div class="notes"><b>Notes</b><br>{e(r["notes"])}</div>' if r.get("notes") else ""}
{srcline}
</main></body></html>"""
    open(os.path.join(out, s + ".html"), "w", encoding="utf-8").write(page)
    index.append((r.get("course") or "Other", r.get("title", ""), s, " · ".join(meta[1:]), img(r)))

order = ["Breakfast","Starter","Main","Side","Salad","Soup","Dessert","Baking","Sauce","Drink","Other"]
index.sort(key=lambda x: (order.index(x[0]) if x[0] in order else 99, x[1].lower()))
types = [t for t in order if any(i[0] == t for i in index)]
chips = f'<button aria-pressed="true" data-t="All">All<small>{len(index)}</small></button>' + "".join(
    f'<button aria-pressed="false" data-t="{e(t)}">{e(t)}<small>{sum(1 for i in index if i[0]==t)}</small></button>' for t in types)
panels = "".join(f'<a class="panel" data-t="{e(c)}" href="{s}.html"><img src="{im}" alt="" loading="lazy"><div class="pb"><span class="ty">{e(c)}</span><b>{e(t)}</b><span>{e(sub)}</span></div></a>'
                 for c, t, s, sub, im in index)
script = """<script>{const b=[...document.querySelectorAll('.chips button')],p=[...document.querySelectorAll('.panel')];
function f(t){b.forEach(x=>x.setAttribute('aria-pressed',x.dataset.t===t));p.forEach(x=>x.hidden=!(t==='All'||x.dataset.t===t));
try{sessionStorage.setItem('type',t)}catch(e){}}
b.forEach(x=>x.addEventListener('click',()=>f(x.dataset.t)));
let s='All';try{s=sessionStorage.getItem('type')||'All'}catch(e){}if(b.some(x=>x.dataset.t===s))f(s)}</script>"""
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(
    head("My Recipe Box").replace("<main>", '<main class="wide">') + f'<div class="top"><h1>My Recipe Box</h1><a class="btn" href="{APP}">+ Add a recipe</a></div><div class="chips">{chips}</div><div class="grid">{panels}</div>{script}</main></body></html>')
open(os.path.join(out, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
open(os.path.join(out, ".nojekyll"), "w").write("")
print(f"built {len(index)} recipe pages")
