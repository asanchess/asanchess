"""Builds the Gazhap-AI banners (KZ + RU, 4:5 / 1:1 / 9:16) from HTML and renders PNGs.

Usage: python3 banner/build.py && node banner/render.js
"""
import base64
import pathlib


ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)


def data_uri(name):
    return "data:image/jpeg;base64," + base64.b64encode((SRC / name).read_bytes()).decode()


COPY = {
    "kz": {
        "kicker": "Telegram-бот",
        "h1": "Ертегінің басты кейіпкері —",
        "h1em": "сіздің балаңыз.",
        "before": "Фото",
        "after": "Ертегі",
        "title": "«Рәбия және жұлдыз құлыншақ»",
        "seal_top": "небәрі",
        "seal_unit": "минут",
        "lead": "Балаңыздың фотосын жүктеңіз — жеке ертегі 10 минутта дайын.",
        "formats": ["PDF кітапша", "Видео ертегі", "Мультфильм"],
        "cta": "Қазір бастаңыз",
    },
    "ru": {
        "kicker": "Telegram-бот",
        "h1": "Главный герой сказки —",
        "h1em": "ваш ребёнок.",
        "before": "Фото",
        "after": "Сказка",
        "title": "«Рәбия и звёздный жеребёнок»",
        "seal_top": "всего",
        "seal_unit": "минут",
        "lead": "Загрузите фото ребёнка — личная сказка будет готова за 10 минут.",
        "formats": ["PDF-книжка", "Видеосказка", "Мультфильм"],
        "cta": "Начать сейчас",
    },
}

FORMATS = {
    # name: (width, height, css overrides)
    "4x5": (1080, 1350, """
        :root{--pad:68px;--h1:76px;--inset:250px;--lead:30px}
    """),
    "1x1": (1080, 1080, """
        :root{--pad:60px;--h1:64px;--inset:210px;--lead:27px}
        .lead{display:none}
        .seal{width:150px;height:150px}
        .seal b{font-size:62px}
    """),
    "9x16": (1080, 1920, """
        :root{--pad:76px;--h1:92px;--inset:300px;--lead:34px}
        .head{padding-top:70px}
        h1{margin:58px 0 46px}
        .plate img.art{object-position:22% 50%}
        .bottom{padding-bottom:60px}
        .formats li{padding:30px 0}
    """),
}

GRAIN = (
    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>"
    "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
    "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/></filter>"
    "<rect width='100%' height='100%' filter='url(%23n)'/></svg>"
)

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400;1,7..72,500&family=Golos+Text:wght@400;500;600&display=block" rel="stylesheet">
<style>
:root{
  --paper:#F3ECDF; --ink:#1E2944; --muted:#5E6276; --red:#A3262A; --gold:#B5873A; --rule:rgba(30,41,68,.22);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:__W__px;height:__H__px}
body{background:var(--paper);color:var(--ink);font-family:'Golos Text',sans-serif;position:relative;overflow:hidden}
body:after{content:"";position:absolute;inset:0;background:url("__GRAIN__");opacity:.07;mix-blend-mode:multiply;pointer-events:none}
.page{position:absolute;inset:0;padding:0 var(--pad);display:flex;flex-direction:column}
.head{display:flex;justify-content:space-between;align-items:baseline;padding:var(--pad) 0 18px;border-bottom:1.5px solid var(--ink)}
.brand{font-family:'Literata',serif;font-weight:600;font-size:30px;letter-spacing:.14em}
.brand i{font-style:normal;color:var(--red)}
.kicker{font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:500}
h1{font-family:'Literata',serif;font-weight:400;font-size:var(--h1);line-height:1.04;letter-spacing:-.018em;margin:40px 0 34px}
h1 em{font-style:italic;font-weight:500;color:var(--red)}
.stage{flex:1;position:relative;min-height:0;margin-bottom:calc(var(--inset)*.42)}
.plate{position:absolute;inset:0 0 0 calc(var(--inset)*.36);border:1.5px solid var(--ink);padding:12px;background:var(--paper)}
.plate img.art{width:100%;height:100%;object-fit:cover;object-position:30% 50%;display:block}
.cap{position:absolute;font-size:19px;letter-spacing:.16em;text-transform:uppercase;font-weight:600}
.cap.after{right:0;bottom:calc(-1 * 40px)}
.cap.after span{font-family:'Literata',serif;text-transform:none;letter-spacing:0;font-style:italic;font-weight:400;font-size:22px;color:var(--muted);margin-left:10px}
.inset{position:absolute;left:0;bottom:calc(var(--inset)*-.42);width:var(--inset)}
.inset .photo{background:#fff;padding:10px 10px 10px;box-shadow:0 1px 0 rgba(0,0,0,.08),0 14px 30px -12px rgba(30,41,68,.45)}
.inset img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 20%}
.inset .cap{position:static;display:block;margin-bottom:10px;color:var(--ink)}
.arrow{position:absolute;left:calc(var(--inset) + 14px);bottom:calc(var(--inset)*-.30);width:120px;height:70px}
.seal{position:absolute;right:-22px;top:-30px;width:176px;height:176px;border-radius:50%;background:var(--red);color:var(--paper);
  display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(8deg);
  box-shadow:0 0 0 6px var(--paper),0 0 0 7.5px var(--red)}
.seal small{font-size:16px;letter-spacing:.2em;text-transform:uppercase;font-weight:500;opacity:.9}
.seal b{font-family:'Literata',serif;font-weight:600;font-size:74px;line-height:.95}
.seal span{font-family:'Literata',serif;font-style:italic;font-size:22px}
.bottom{padding:44px 0 var(--pad)}
.lead{font-size:var(--lead);line-height:1.3;max-width:20em;margin-bottom:26px}
.formats{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);border-top:1.5px solid var(--ink);border-bottom:1px solid var(--rule);margin-bottom:30px}
.formats li{padding:20px 0;font-size:25px;font-weight:500;display:flex;gap:12px;align-items:baseline}
.formats li+li{border-left:1px solid var(--rule);padding-left:22px}
.formats li i{font-family:'Literata',serif;font-style:italic;color:var(--gold);font-size:24px}
.cta{display:flex;align-items:center;justify-content:space-between}
.btn{background:var(--ink);color:var(--paper);font-size:30px;font-weight:600;padding:24px 40px;border-radius:999px;display:flex;gap:18px;align-items:center}
.btn svg{width:34px;height:20px}
.handle{font-family:'Literata',serif;font-size:27px;text-align:right;line-height:1.25}
.handle small{display:block;font-family:'Golos Text';font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
__CSS__
</style></head><body><div class="page">
  <div class="head"><div class="brand">GAZHAP<i>·</i>AI</div><div class="kicker">__kicker__</div></div>
  <h1>__h1__<br><em>__h1em__</em></h1>
  <div class="stage">
    <div class="plate"><img class="art" src="__AFTER__"></div>
    <div class="cap after">__after__<span>__title__</span></div>
    <div class="seal"><small>__seal_top__</small><b>10</b><span>__seal_unit__</span></div>
    <svg class="arrow" viewBox="0 0 120 70" fill="none" stroke="#1E2944" stroke-width="2.2" stroke-linecap="round">
      <path d="M4 60 C 30 62, 70 50, 104 18"/><path d="M90 16 L105 17 L102 32"/></svg>
    <div class="inset"><span class="cap">__before__</span><div class="photo"><img src="__BEFORE__"></div></div>
  </div>
  <div class="bottom">
    <p class="lead">__lead__</p>
    <ul class="formats"><li><i>01</i>__f0__</li><li><i>02</i>__f1__</li><li><i>03</i>__f2__</li></ul>
    <div class="cta">
      <div class="btn">__cta__<svg viewBox="0 0 34 20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2 10h29M22 2l9 8-9 8"/></svg></div>
      <div class="handle"><small>Telegram</small>@GazhapAIbot</div>
    </div>
  </div>
</div></body></html>"""


def render_html(lang, fmt):
    w, h, css = FORMATS[fmt]
    c = COPY[lang]
    html = TEMPLATE
    repl = {
        "__W__": str(w), "__H__": str(h), "__CSS__": css, "__GRAIN__": GRAIN,
        "__AFTER__": data_uri("after_night.jpg"), "__BEFORE__": data_uri("before.jpg"),
        "__f0__": c["formats"][0], "__f1__": c["formats"][1], "__f2__": c["formats"][2],
    }
    for k, v in c.items():
        if isinstance(v, str):
            repl[f"__{k}__"] = v
    for k, v in repl.items():
        html = html.replace(k, v)
    return html, w, h


def main():
    for lang in COPY:
        for fmt in FORMATS:
            html, w, h = render_html(lang, fmt)
            (OUT / f"gazhap_{lang}_{fmt}.html").write_text(html, encoding="utf-8")
            print(f"gazhap_{lang}_{fmt}", w, h)


main()
