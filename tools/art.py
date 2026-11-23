"""Recipe illustrations (original flat SVGs) and keyword matching, shared by the app and the site.
Run directly to print art.json for embedding in the app."""
import json, re

W = 'viewBox="0 0 320 180" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice"'

ART = {
"pasta": f'''<svg {W}><rect width="320" height="180" fill="#f4e3c3"/><ellipse cx="160" cy="132" rx="118" ry="26" fill="#d9c29a"/>
<path d="M58 96h204c0 44-46 66-102 66S58 140 58 96z" fill="#2f5d8a"/><ellipse cx="160" cy="96" rx="102" ry="22" fill="#f6efe2"/>
<g fill="none" stroke="#e8b84a" stroke-width="6" stroke-linecap="round"><path d="M88 96c18-22 40 10 58-8s38 12 54-6 30 6 42 4"/><path d="M96 104c22-14 34 6 56-6s36 10 56-4 26 4 34 2"/><path d="M120 86c14-10 30 8 44-2s28 6 40-2"/></g>
<g fill="#1f1d1b"><circle cx="128" cy="92" r="2.5"/><circle cx="170" cy="100" r="2.5"/><circle cx="196" cy="90" r="2.5"/><circle cx="148" cy="104" r="2.5"/></g>
<path d="M236 30l-36 64" stroke="#8c6a3f" stroke-width="7" stroke-linecap="round"/><path d="M256 34l-44 60" stroke="#8c6a3f" stroke-width="7" stroke-linecap="round"/></svg>''',
"potatoes": f'''<svg {W}><rect width="320" height="180" fill="#e6eddf"/><rect x="40" y="70" width="240" height="96" rx="10" fill="#3b3b3d"/><rect x="48" y="76" width="224" height="84" rx="6" fill="#4a4a4d"/>
<g><ellipse cx="98" cy="108" rx="30" ry="22" fill="#d9a441"/><ellipse cx="98" cy="106" rx="22" ry="15" fill="#f0c766"/>
<ellipse cx="160" cy="124" rx="30" ry="22" fill="#d9a441"/><ellipse cx="160" cy="122" rx="22" ry="15" fill="#f0c766"/>
<ellipse cx="222" cy="106" rx="30" ry="22" fill="#d9a441"/><ellipse cx="222" cy="104" rx="22" ry="15" fill="#f0c766"/>
<ellipse cx="128" cy="140" rx="24" ry="14" fill="#cf9536"/><ellipse cx="196" cy="142" rx="24" ry="14" fill="#cf9536"/></g>
<g fill="#4f8a3c"><circle cx="90" cy="102" r="3"/><circle cx="168" cy="118" r="3"/><circle cx="214" cy="100" r="3"/><circle cx="230" cy="110" r="2.5"/><circle cx="152" cy="126" r="2.5"/></g>
<path d="M250 28c20 6 30 22 24 40-14-4-26-18-24-40z" fill="#f2d64b"/></svg>''',
"pot": f'''<svg {W}><rect width="320" height="180" fill="#efe1d8"/><ellipse cx="160" cy="158" rx="120" ry="14" fill="#d8c2b4"/>
<rect x="72" y="70" width="176" height="84" rx="22" fill="#b8352b"/><rect x="52" y="86" width="28" height="14" rx="7" fill="#8f2820"/><rect x="240" y="86" width="28" height="14" rx="7" fill="#8f2820"/>
<ellipse cx="160" cy="70" rx="90" ry="16" fill="#5b2a1d"/><g fill="#7a3a26"><ellipse cx="130" cy="68" rx="22" ry="8"/><ellipse cx="182" cy="70" rx="24" ry="8"/></g>
<g fill="#e07b39"><circle cx="150" cy="66" r="5"/><circle cx="200" cy="64" r="4"/></g><g fill="#5c8c3a"><circle cx="118" cy="64" r="3"/><circle cx="168" cy="72" r="3"/></g>
<g fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="5" stroke-linecap="round"><path d="M130 44c-8-10 8-16 0-26"/><path d="M160 40c-8-10 8-16 0-26"/><path d="M190 44c-8-10 8-16 0-26"/></g></svg>''',
"bake": f'''<svg {W}><rect width="320" height="180" fill="#f3e6d6"/><ellipse cx="160" cy="156" rx="128" ry="14" fill="#dccab4"/>
<rect x="48" y="66" width="224" height="86" rx="14" fill="#f7f4ee"/><rect x="58" y="74" width="204" height="70" rx="8" fill="#c9442f"/>
<rect x="58" y="96" width="204" height="10" fill="#f3e2b8"/><rect x="58" y="116" width="204" height="10" fill="#f3e2b8"/>
<path d="M58 82c20-10 40 6 60-2s40 8 60 0 40 6 60-2 24 2 24 2v-8H58z" fill="#e9b04c"/>
<g fill="#b9772e"><circle cx="90" cy="80" r="4"/><circle cx="150" cy="78" r="5"/><circle cx="210" cy="80" r="4"/><circle cx="240" cy="78" r="3"/></g>
<g fill="#4f8a3c"><ellipse cx="120" cy="76" rx="6" ry="3"/><ellipse cx="186" cy="76" rx="6" ry="3"/></g></svg>''',
"salad": f'''<svg {W}><rect width="320" height="180" fill="#e3eee4"/><ellipse cx="160" cy="150" rx="112" ry="14" fill="#c9dccb"/>
<path d="M64 90h192c0 38-42 58-96 58S64 128 64 90z" fill="#f6efe2"/><g fill="#5f9c45"><ellipse cx="110" cy="84" rx="30" ry="16"/><ellipse cx="160" cy="76" rx="34" ry="18"/><ellipse cx="208" cy="84" rx="30" ry="16"/></g>
<g fill="#8cc163"><ellipse cx="134" cy="80" rx="18" ry="10"/><ellipse cx="188" cy="80" rx="18" ry="10"/></g>
<g fill="#d84a3a"><circle cx="124" cy="74" r="9"/><circle cx="196" cy="72" r="8"/></g><g fill="#f0a63a"><circle cx="160" cy="68" r="7"/></g>
<g fill="#7c3a6b"><ellipse cx="144" cy="86" rx="10" ry="5"/><ellipse cx="178" cy="88" rx="10" ry="5"/></g></svg>''',
"soup": f'''<svg {W}><rect width="320" height="180" fill="#f2e7cf"/><ellipse cx="160" cy="150" rx="116" ry="14" fill="#ddcfae"/>
<path d="M66 88h188c0 40-42 60-94 60S66 128 66 88z" fill="#2f6b5c"/><ellipse cx="160" cy="88" rx="94" ry="18" fill="#e58a3a"/>
<g fill="#f6c36b"><circle cx="130" cy="86" r="5"/><circle cx="184" cy="90" r="4"/></g><g fill="#5c8c3a"><circle cx="160" cy="84" r="3"/><circle cx="146" cy="92" r="2.5"/></g>
<g fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="5" stroke-linecap="round"><path d="M136 60c-8-10 8-16 0-26"/><path d="M184 60c-8-10 8-16 0-26"/></g></svg>''',
"dessert": f'''<svg {W}><rect width="320" height="180" fill="#f6e1e4"/><ellipse cx="160" cy="152" rx="104" ry="14" fill="#e6c6cb"/>
<path d="M96 140V92l128-40v88z" fill="#f4d9a8"/><path d="M96 92l128-40v14L96 106z" fill="#fff6ea"/><path d="M96 118l128-34v12L96 130z" fill="#8a4b2a"/>
<path d="M96 92l128-40c4 10-4 16-14 18l-102 30c-8 2-12-2-12-8z" fill="#fff"/><circle cx="196" cy="56" r="10" fill="#d7263d"/><path d="M196 46c2-10 8-14 14-16" stroke="#4f8a3c" stroke-width="3" fill="none"/></svg>''',
"bread": f'''<svg {W}><rect width="320" height="180" fill="#efe4d2"/><ellipse cx="160" cy="150" rx="120" ry="14" fill="#d9c7a8"/>
<path d="M66 140c0-50 40-84 94-84s94 34 94 84z" fill="#c98a3d"/><path d="M80 138c0-42 34-70 80-70s80 28 80 70z" fill="#dda257"/>
<g stroke="#a86a28" stroke-width="6" stroke-linecap="round"><path d="M110 92l20 26"/><path d="M150 80l20 30"/><path d="M190 88l20 28"/></g></svg>''',
"plate": f'''<svg {W}><rect width="320" height="180" fill="#e9e9ec"/><circle cx="160" cy="92" r="62" fill="#fff"/><circle cx="160" cy="92" r="46" fill="#f3f3f5"/>
<g fill="#b9b9bf"><rect x="74" y="40" width="8" height="104" rx="4"/><rect x="66" y="40" width="4" height="30" rx="2"/><rect x="86" y="40" width="4" height="30" rx="2"/><rect x="240" y="40" width="10" height="104" rx="5"/></g>
<g fill="#5f9c45"><ellipse cx="150" cy="86" rx="10" ry="5"/><ellipse cx="170" cy="96" rx="10" ry="5"/></g><circle cx="160" cy="92" r="7" fill="#d84a3a"/></svg>''',
"drink": f'''<svg {W}><rect width="320" height="180" fill="#e2ecf2"/><path d="M128 40h64l-8 110h-48z" fill="#fff" fill-opacity=".8"/><path d="M132 70h56l-6 80h-44z" fill="#e8784a"/>
<circle cx="182" cy="56" r="16" fill="#f2d64b"/><circle cx="182" cy="56" r="10" fill="#f7e48a"/><rect x="170" y="20" width="5" height="70" rx="2" fill="#d7263d" transform="rotate(14 172 55)"/></svg>''',
"breakfast": f'''<svg {W}><rect width="320" height="180" fill="#f4ecd8"/><circle cx="150" cy="96" r="58" fill="#3b3b3d"/><rect x="200" y="88" width="90" height="14" rx="7" fill="#3b3b3d"/>
<circle cx="150" cy="96" r="48" fill="#4a4a4d"/><path d="M114 96c0-24 18-36 38-34s36 16 32 36-22 30-40 28-30-10-30-30z" fill="#fff"/><circle cx="150" cy="96" r="14" fill="#f2b632"/></svg>''',
}

RULES = [  # first match wins; matched against title, tags and cuisine (lowercase)
    ("bake", r"lasagn|casserole|gratin|bake[d]?\b|enchilada|moussaka|pie\b|quiche|tart\b"),
    ("pasta", r"pasta|spaghetti|tonnarelli|linguine|noodle|penne|rigatoni|ramen|udon|cacio|carbonara|risotto"),
    ("potatoes", r"potato|fries|hash\b|roast(ed)? veg"),
    ("soup", r"soup|stock\b|broth|chowder|bisque|chili|curry|dal\b|stew"),
    ("pot", r"braise|short rib|pot roast|ragu|ragù|bourguignon|osso|beef|pork|lamb|chicken|duck"),
    ("salad", r"salad|slaw|greens"),
    ("dessert", r"cake|cookie|brownie|dessert|ice cream|pudding|crumble|cobbler|sweet"),
    ("bread", r"bread|loaf|focaccia|sourdough|bun|roll\b|biscuit|scone|muffin"),
    ("drink", r"cocktail|drink|smoothie|punch|spritz|lemonade"),
    ("breakfast", r"egg|omelet|pancake|waffle|frittata|breakfast|granola|oat"),
]
COURSE_ART = {"Soup": "soup", "Salad": "salad", "Dessert": "dessert", "Baking": "bread", "Drink": "drink", "Breakfast": "breakfast"}

def pick(r):
    text = " ".join([r.get("title", ""), " ".join(r.get("tags") or []), r.get("cuisine", "")]).lower()
    for key, pat in RULES:
        if re.search(pat, text):
            return key
    return COURSE_ART.get(r.get("course"), "plate")

if __name__ == "__main__":
    print(json.dumps({"art": ART, "rules": RULES, "course": COURSE_ART}))
