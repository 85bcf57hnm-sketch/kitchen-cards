"""Add US/imperial equivalents after metric amounts, e.g. "400g" -> "400g (14 oz)".
Mirrors toImperial() in the My Recipe Box app."""
import re

FR = {"½": .5, "¼": .25, "¾": .75, "⅓": 1/3, "⅔": 2/3}
NUM = r"(\d+(?:[.,]\d+)?|[½¼¾⅓⅔])"
DONE = r"(?!\s*\(\s*(?:about |≈ ?)?[\d½¼¾⅓⅔⅛])(?!\s*/\s*[\d.½¼¾⅓⅔]+\s*(?:oz|lb|cups?|tbsp|tsp|fl|in|qt|°?F\b))"  # skip if an equivalent already follows

def num(s):
    return FR.get(s) or float(s.replace(",", "."))

def frac(n, step):
    n = round(n / step) * step
    w = int(n); r = round(n - w, 3)
    f = {0: "", .25: "¼", .5: "½", .75: "¾", .125: "⅛", .375: "⅜", .625: "⅝", .875: "⅞"}.get(r, "")
    if not w and not f: return None
    return (str(w) if w else "") + f

def weight(g):
    oz = g / 28.35
    if oz >= 16:
        return f"{frac(oz / 16, .25)} lb"
    v = frac(oz, .25 if oz < 1 else .5 if oz < 4 else 1)
    return f"{v or '¼'} oz"

def volume(ml):
    if ml < 15:
        return f"{frac(ml / 4.93, .25) or '¼'} tsp"
    if ml < 60:
        return f"{frac(ml / 14.79, .5)} tbsp"
    if ml >= 1900:
        return f"{frac(ml / 946.4, .25)} qt"
    v = frac(ml / 236.6, .25)
    return f"{v} cup" if v in ("1", "¼", "½", "¾") else f"{v} cups"

def inches(cm):
    v = frac(cm / 2.54, .5)
    return f"{v or '½'} in"

def temp(c):
    f = c * 9 / 5 + 32
    return f"{int(round(f / 25) * 25) if c >= 100 else int(round(f / 5) * 5)}°F"

def to_imperial(s):
    if not s: return s
    # dish sizes: 30 x 20cm
    s = re.sub(NUM + r"\s?[x×]\s?" + NUM + r"\s?cm\b" + DONE,
               lambda m: f"{m[0]} ({inches(num(m[1]))[:-3]} x {inches(num(m[2]))})", s)
    # temperatures: 200°C, 180C fan
    s = re.sub(r"(\d+)\s?°\s?C\b" + DONE, lambda m: f"{m[0]} ({temp(int(m[1]))})", s)
    # weights, volumes, lengths
    def unit(m):
        n, u = num(m[1]), m[2].lower()
        eq = {"g": lambda: weight(n), "kg": lambda: weight(n * 1000), "ml": lambda: volume(n),
              "cl": lambda: volume(n * 10), "l": lambda: volume(n * 1000), "cm": lambda: inches(n)}[u]()
        return f"{m[0]} ({eq})"
    s = re.sub(NUM + r"\s?(kg|g|ml|cl|l|cm)\b(?![-–]\d)" + DONE, unit, s, flags=re.I)
    return s

if __name__ == "__main__":
    for t in ["400g cherry tomatoes", "2 x 400g tins chopped tomatoes", "75g Parmesan, finely grated", "50g unsalted butter",
              "500ml whole milk", "100ml water", "750 ml dry red wine", "Preheat the oven to 200°C/180°C fan.",
              "a baking dish, approx. 30 x 20cm.", "1 kg flour", "1.5 l stock", "5ml vanilla", "30 ml oil", "2.5cm ginger",
              "1 large onion", "1 1/2 lb potatoes", "400g (14 oz) already done", "Approximately 9–12 lasagne sheets"]:
        print(to_imperial(t))
