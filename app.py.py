# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template_string, request
import random
import datetime

app = Flask(__name__)

FACTS = {
    "lustig": [
        "In der Schweiz ist es illegal, nur ein Meerschweinchen zu halten – sie brauchen Freunde! 🐹",
        "Eine Gruppe Flamingos heißt tatsächlich 'Flamboyance'. 💅",
        "In Japan gibt es KitKat mit Sojasoße-Geschmack. 🍫🍱",
        "Kühe haben beste Freunde und werden gestresst, wenn man sie trennt. 🐄❤️",
        "Wombats kacken Würfel. Ernsthaft. 🧱",
    ],
    "tiere": [
        "Oktopusse haben drei Herzen und blaues Blut. 🐙",
        "Raben erkennen Gesichter und merken sich Feinde jahrelang. 🐦",
        "Pinguine schenken ihren Partnern schöne Kieselsteine. 🐧💎",
    ],
    "weltall": [
        "Ein Tag auf der Venus ist länger als ein Jahr auf der Venus. 😵‍💫",
        "Neutronensterne drehen sich bis zu 700 Mal pro Sekunde. 🌟",
    ],
    "essen": [
        "Ketchup wurde im 19. Jahrhundert als Medizin verkauft. 🍅",
        "Ananas enthält Bromelain, ein Enzym, das dich 'zurück-verdaut'. 🍍",
    ],
}
ALL_FACTS = [f for cat in FACTS.values() for f in cat]

HTML = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <title>🎉 Fun-Facts · Smooth Clock</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root { --bg:#0d1117; --panel:#161b22; --text:#e6edf3; --muted:#9da7b3; --brand:#58a6ff; --accent:#238636; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:system-ui, Segoe UI, Roboto, Arial, sans-serif; background:var(--bg); color:var(--text); }
    header { padding:18px 20px; text-align:center; border-bottom:1px solid #202734; }
    h1 { margin:0; color:var(--brand); font-size:26px; }
    main { max-width:900px; margin:28px auto; padding:0 16px; display:grid; gap:18px; }
    .card { background:var(--panel); border:1px solid #202734; border-radius:16px; padding:18px; box-shadow:0 6px 24px rgba(0,0,0,.25); }
    .row { display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
    select, button { background:#0f1523; color:var(--text); border:1px solid #2a3242; border-radius:10px; padding:10px 12px; }
    button { cursor:pointer; }
    button.primary { background:var(--accent); border-color:#2ea043; }
    button.ghost { background:transparent; border-color:#2a3242; }
    #fact { font-size:22px; line-height:1.4; margin:8px 0 14px; }
    .muted { color:var(--muted); font-size:13px; }

    /* Uhr */
    #clock { font-size:40px; font-weight:800; text-align:center; letter-spacing: .5px; }
    #date  { font-size:18px; text-align:center; color:var(--muted); margin-top:6px; }
    .tick  { animation: pop 180ms ease; }
    @keyframes pop {
      0%   { transform: scale(1);   text-shadow: 0 0 0 rgba(88,166,255,0);}
      50%  { transform: scale(1.03);text-shadow: 0 0 12px rgba(88,166,255,0.35);}
      100% { transform: scale(1);   text-shadow: 0 0 0 rgba(88,166,255,0);}
    }

    ul { list-style:none; margin:10px 0 0; padding:0; }
    li { padding:10px 12px; border:1px solid #202734; border-radius:10px; margin-bottom:10px; background:#0f1523; display:flex; justify-content:space-between; gap:10px; }
    .right { display:flex; gap:8px; }
    footer { text-align:center; color:var(--muted); margin:28px 0; }
  </style>
</head>
<body>
  <header>
    <h1>🎉 Fun-Facts · Smooth Clock</h1>
  </header>

  <main>
    <section class="card" id="time-card">
      <div>🕒 Aktuelle Zeit & Datum</div>
      <div id="clock">{{ time }}</div>
      <div id="date">{{ date }}</div>
    </section>

    <section class="card">
      <div class="row">
        <label for="cat">Kategorie:</label>
        <select id="cat">
          <option value="lustig" selected>Lustig</option>
          <option value="tiere">Tiere</option>
          <option value="weltall">Weltall</option>
          <option value="essen">Essen</option>
          <option value="random">Zufällig</option>
        </select>
        <button id="btn-new" class="primary">🎲 Neuen Fakt</button>
        <button id="btn-copy" class="ghost">📋 Kopieren</button>
        <button id="btn-fav"  class="ghost">⭐ Favorit</button>
      </div>
      <p id="fact">Lade Fakt…</p>
    </section>

    <aside class="card">
      <div class="row" style="justify-content:space-between;">
        <strong>⭐ Favoriten</strong>
        <button id="btn-clear" class="ghost">🗑️ Leeren</button>
      </div>
      <ul id="favs"></ul>
    </aside>
  </main>

  <footer>Made with Flask · Uhrzeit + Datum + Fun Facts ✨</footer>

  <script>
    const clockEl = document.getElementById('clock');
    const dateEl  = document.getElementById('date');
    const factEl  = document.getElementById('fact');
    const catEl   = document.getElementById('cat');
    const favList = document.getElementById('favs');

    // Helfer
    const pad = n => String(n).padStart(2,'0');

    // Smooth Clock mit requestAnimationFrame
    let lastSecond = null;
    function runClock(){
      const now = new Date();
      const h = pad(now.getHours()), m = pad(now.getMinutes()), s = pad(now.getSeconds());
      const text = h + ":" + m + ":" + s;

      // Schreibe nur, wenn sich der Text geändert hat (spart Repaints)
      if (clockEl.textContent !== text) {
        // Tick-Animation nur beim Sekundenwechsel
        if (lastSecond !== s) {
          lastSecond = s;
          clockEl.classList.remove('tick'); // re-trigger
          // kleines Timeout, damit der Browser die Klasse neu anwendet
          requestAnimationFrame(() => clockEl.classList.add('tick'));
        }
        clockEl.textContent = text;
      }
      // Datum fortlaufend mitführen
      dateEl.textContent = now.toLocaleDateString('de-DE');
      requestAnimationFrame(runClock);
    }

    async function loadFact(){
      const cat = catEl.value;
      const res = await fetch('/api/fact?cat=' + encodeURIComponent(cat));
      const data = await res.json();
      factEl.textContent = data.fact;
      factEl.dataset.fact = data.fact;
    }

    function renderFavs(){
      const favs = JSON.parse(localStorage.getItem('favs') || '[]');
      favList.innerHTML = '';
      favs.forEach((f, i) => {
        const li = document.createElement('li');
        li.textContent = f;
        favList.append(li);
      });
    }

    document.getElementById('btn-new').onclick = loadFact;
    document.getElementById('btn-copy').onclick = () => navigator.clipboard.writeText(factEl.dataset.fact || factEl.textContent);
    document.getElementById('btn-fav').onclick  = () => {
      const t = factEl.dataset.fact || factEl.textContent; if(!t) return;
      const favs = JSON.parse(localStorage.getItem('favs') || '[]');
      if(!favs.includes(t)) favs.unshift(t);
      localStorage.setItem('favs', JSON.stringify(favs.slice(0,50)));
      renderFavs();
    };
    document.getElementById('btn-clear').onclick = () => { localStorage.removeItem('favs'); renderFavs(); };

    // Initial
    renderFavs(); loadFact(); runClock();
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    now = datetime.datetime.now()
    return render_template_string(HTML, time=now.strftime("%H:%M:%S"), date=now.strftime("%d.%m.%Y"))

@app.get("/api/fact")
def api_fact():
    cat = (request.args.get("cat") or "random").lower()
    fact = random.choice(ALL_FACTS) if cat == "random" or cat not in FACTS else random.choice(FACTS[cat])
    return jsonify({"fact": fact})

if __name__ == "__main__":
    app.run(debug=True)
