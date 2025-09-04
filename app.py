from flask import Flask, jsonify, render_template_string, request
import random
import datetime

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# IDEEN-FORMULAR: sendet ohne Setup an deine Mailadresse über FormSubmit
FORMSUBMIT_URL = "https://formsubmit.co/info@aaron-sigma.de"
# ─────────────────────────────────────────────────────────────────────────────

# Kleine Fakten-Datenbank
FACTS = {
    "lustig": [
        "Kühe haben beste Freunde und werden gestresst, wenn man sie trennt. 🐮❤️",
        "Ein Straußenei braucht rund 40 Minuten, um weich zu kochen. 🥚",
        "Honig verdirbt nie — Archäologen fanden essbaren Honig in 3000 Jahre alten Gräbern. 🍯",
        "Koalas schlafen bis zu 22 Stunden am Tag. 😴🐨",
    ],
    "tiere": [
        "Oktopusse haben drei Herzen. 🐙",
        "Ein Tintenfisch kann durch ein Loch passen, das so groß ist wie sein Schnabel. 🦑",
        "Schmetterlinge schmecken mit ihren Füßen. 🦋",
        "Raben können menschliche Gesichter erkennen und sich merken. 🐦",
    ],
    "wissen": [
        "Die erste Website ging 1991 online. 🌐",
        "Der Eiffelturm wird im Sommer bis zu 15 cm höher. 🗼",
        "Banane ist eine Beere, die Erdbeere nicht. 🍓🍌",
        "Wasser dehnt sich beim Gefrieren aus. ❄️",
    ],
}
ALL_FACTS = sum(FACTS.values(), [])

HTML = r"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Fun-Facts • Smooth Clock • Mini-Game</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">

<style>
  :root{
    --bg:#0b0f14; --card:#121824; --muted:#9fb0c3; --text:#e8f1fb;
    --primary:#4aa3ff; --accent:#22c55e; --danger:#ef4444; --yellow:#facc15;
  }
  *{box-sizing:border-box}
  body{
    margin:0; font-family:Inter,system-ui,Segoe UI,Roboto,Arial,sans-serif;
    background:linear-gradient(180deg,#0b0f14 0%, #0d141f 100%); color:var(--text);
  }
  .wrap{max-width:980px;margin:40px auto;padding:0 16px}
  h1{font-size: clamp(28px, 4vw, 42px); line-height:1.15; margin:0 0 18px}
  .muted{color:var(--muted)}
  .card{
    background:var(--card);
    border:1px solid rgba(255,255,255,.06);
    border-radius:18px; padding:18px 16px; box-shadow:0 10px 24px rgba(0,0,0,.35);
  }

  /* Clock */
  .clock{ display:flex;flex-direction:column;align-items:center;gap:12px;padding:18px;text-align:center; }
  .time{ font-variant-numeric:tabular-nums; font-size: clamp(40px, 7vw, 72px); font-weight:800 }
  .date{ font-size:18px; color:var(--muted) }

  /* Facts */
  .facts .row{display:flex; gap:10px; flex-wrap:wrap; align-items:center}
  .select, .btn{
    appearance:none;border:1px solid rgba(255,255,255,.08); background:#0e1420; color:var(--text);
    padding:10px 14px;border-radius:12px; font-weight:600
  }
  .btn{ cursor:pointer; transition:.15s transform ease }
  .btn:hover{ transform: translateY(-1px); }
  .btn.primary{ background:var(--primary); border-color:transparent; color:#001022 }
  .btn.copy{ background:#142134 }
  .btn.fav{ background:#142b20 }
  .fact{ margin:14px 0 0; font-size: clamp(20px, 2.8vw, 28px); line-height:1.35; }

  /* Favorites */
  .favlist{display:flex; flex-direction:column; gap:8px}
  .favitem{ background:#0e1420; padding:10px 12px; border-radius:10px; border:1px solid rgba(255,255,255,.06) }

  /* TicTacToe */
  .ttt{ display:grid; grid-template-columns:repeat(3, 96px); gap:10px; justify-content:center }
  .ttt button{
    width:96px; height:96px; font-weight:800; font-size:42px; color:var(--text);
    background:#0e1420; border:1px solid rgba(255,255,255,.08); border-radius:12px; cursor:pointer;
  }
  .ttt .win{ background: #0f2a18; border-color:#1d6c3a; }
  .center{text-align:center}

  /* Idea form */
  label{ display:block; margin:10px 0 6px; font-weight:700 }
  input[type=text], textarea{
    width:100%; background:#0e1420; border:1px solid rgba(255,255,255,.08);
    color:var(--text); border-radius:12px; padding:12px 14px; outline:none;
  }
  textarea{ min-height:140px; resize:vertical }
  .ok{color:var(--accent); font-weight:700}
  .err{color:var(--danger); font-weight:700}

  footer{margin:28px 0 60px;text-align:center;color:var(--muted)}
  footer .brand{color:var(--text); font-weight:800}
</style>
</head>
<body>
  <div class="wrap">
    <h1>🎉 Fun-Facts • Smooth Clock</h1>

    <!-- Clock -->
    <div class="card clock">
      <div class="time" id="time">--:--:--</div>
      <div class="date" id="date">--.--.----</div>
    </div>

    <!-- Facts -->
    <div class="card facts" style="margin-top:16px">
      <div class="row">
        <span class="muted">Kategorie:</span>
        <select id="cat" class="select">
          <option value="lustig">Lustig</option>
          <option value="tiere">Tiere</option>
          <option value="wissen">Wissen</option>
          <option value="random">Zufällig</option>
        </select>
        <button class="btn primary" id="btn-new">🎲 Neuen Fakt</button>
        <button class="btn copy" id="btn-copy">📋 Kopieren</button>
        <button class="btn fav" id="btn-fav">⭐ Favorit</button>
      </div>
      <div class="fact" id="fact">Klicke auf „Neuen Fakt“ 🙂</div>
    </div>

    <!-- Favorites -->
    <div class="card" style="margin-top:16px">
      <div class="row" style="justify-content:space-between; align-items:center">
        <h3 style="margin:0">⭐ Favoriten</h3>
        <button class="btn" id="btn-clear">🗑️ Leeren</button>
      </div>
      <div class="favlist" id="favlist" style="margin-top:10px"></div>
    </div>

    <!-- TicTacToe -->
    <div class="card" style="margin-top:16px">
      <h3 style="margin-top:0">🎮 Mini-Game: Tic-Tac-Toe</h3>
      <div class="center muted" id="ttt-status">Du bist X. Viel Spaß!</div>
      <div class="ttt" id="ttt"></div>
      <div class="center" style="margin-top:10px">
        <button class="btn" id="ttt-reset">Neu starten</button>
      </div>
    </div>

   <!-- Ideen-Formular (funktioniert ohne Backend über FormSubmit) -->
<section id="idee" class="card">
  <h2>💡 Deine Idee für die Website</h2>

  {% if sent %}
    <div class="alert success">
      ✅ Danke! Deine Idee wurde gesendet. Prüfe dein Postfach – beim allerersten Mal
      musst du die kurze Bestätigung von FormSubmit bestätigen.
    </div>
  {% endif %}

  <form action="{{ form_url }}" method="POST" class="idea-form">
    <!-- FormSubmit Optionen -->
    <input type="hidden" name="_subject" value="Neue Idee von aaron-sigma.de">
    <input type="hidden" name="_template" value="box">
    <input type="hidden" name="_captcha" value="false">
    <!-- Nach dem Absenden zurück auf die Seite mit Erfolgs-Hinweis -->
    <input type="hidden" name="_next" value="https://aaron-sigma.de/?sent=1#idee">
    <!-- Honeypot gegen Bots -->
    <input type="text" name="_honey" style="display:none">

    <label for="name">Name</label>
    <input id="name" name="name" type="text" placeholder="Dein Name" required>

    <label for="message">Deine Idee</label>
    <textarea id="message" name="message" rows="5" placeholder="Schreib deine Idee hier rein..." required></textarea>

    <button type="submit" class="btn primary">📧 Idee absenden</button>
  </form>
</section>
    </div>

    <footer>
      <div class="muted">Made by <span class="brand">Aaron ✨</span></div>
    </footer>
  </div>

<script>
  // Uhr
  function runClock(){
    const now = new Date();
    const two = n => String(n).padStart(2, '0');
    const hh = two(now.getHours()), mm = two(now.getMinutes()), ss = two(now.getSeconds());
    const d = two(now.getDate()), m = two(now.getMonth()+1), y = now.getFullYear();
    document.getElementById("time").textContent = `${hh}:${mm}:${ss}`;
    document.getElementById("date").textContent = `${d}.${m}.${y}`;
  }
  setInterval(runClock, 1000); runClock();

  // Facts
  async function loadFact(){
    const cat = document.getElementById('cat').value;
    const url = cat === 'random' ? '/api/fact' : `/api/fact?cat=${encodeURIComponent(cat)}`;
    const res = await fetch(url); const data = await res.json();
    document.getElementById('fact').textContent = data.fact;
  }
  document.getElementById('btn-new').addEventListener('click', loadFact);
  document.getElementById('cat').addEventListener('change', loadFact);

  // Copy
  document.getElementById('btn-copy').addEventListener('click', async ()=>{
    const t = document.getElementById('fact').textContent;
    try{ await navigator.clipboard.writeText(t); flash("Kopiert!"); }catch(e){ flash("Kopieren fehlgeschlagen","err"); }
  });

  // Favoriten
  function getFavs(){ try{ return JSON.parse(localStorage.getItem('favs')||'[]'); }catch(e){ return []; } }
  function setFavs(a){ localStorage.setItem('favs', JSON.stringify(a.slice(0,50))); }
  function renderFavs(){
    const box = document.getElementById('favlist'); box.innerHTML='';
    getFavs().forEach((f,i)=>{
      const div = document.createElement('div'); div.className='favitem'; div.textContent = f;
      div.addEventListener('click', ()=>{ document.getElementById('fact').textContent = f; });
      box.appendChild(div);
    });
  }
  document.getElementById('btn-fav').addEventListener('click', ()=>{
    const t = document.getElementById('fact').textContent.trim(); if(!t) return;
    const favs = getFavs(); if(!favs.includes(t)){ favs.unshift(t); setFavs(favs); renderFavs(); flash("Favorit gespeichert","ok"); }
  });
  document.getElementById('btn-clear').addEventListener('click', ()=>{ localStorage.removeItem('favs'); renderFavs(); });

  // Mini Flash
  function flash(msg, cls='ok'){
    const n = document.createElement('div');
    n.textContent = msg; n.className=cls;
    n.style.position='fixed'; n.style.bottom='16px'; n.style.left='50%'; n.style.transform='translateX(-50%)';
    n.style.background = 'rgba(20,42,50,.9)'; n.style.border='1px solid rgba(255,255,255,.1)';
    n.style.padding='10px 14px'; n.style.borderRadius='10px'; n.style.zIndex='9999';
    document.body.appendChild(n); setTimeout(()=>n.remove(), 1600);
  }

  // TicTacToe
  const ttt = document.getElementById('ttt');
  let board = Array(9).fill(''); let current = 'X'; let lock=false;
  const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  function draw(){
    ttt.innerHTML='';
    board.forEach((val,i)=>{
      const b = document.createElement('button'); b.textContent = val;
      b.addEventListener('click', ()=>move(i));
      ttt.appendChild(b);
    });
  }
  function move(i){
    if(lock || board[i]) return;
    board[i] = current; draw();
    const w = winner(); if(w){ endGame(w); return; }
    if(board.every(v=>v)) { endGame('draw'); return; }
    current = current==='X' ? 'O':'X';
    document.getElementById('ttt-status').textContent = `Du bist ${current}. Viel Spaß!`;
  }
  function winner(){
    for(const [a,b,c] of wins){ if(board[a] && board[a]===board[b] && board[b]===board[c]) return [a,b,c]; }
    return null;
  }
  function endGame(res){
    lock = true;
    if(res==='draw'){ document.getElementById('ttt-status').textContent = 'Unentschieden!'; return; }
    document.getElementById('ttt-status').textContent = `${board[res[0]]} gewinnt!`;
    [...ttt.children].forEach((btn,i)=>{ if(res.includes(i)) btn.classList.add('win'); });
  }
  document.getElementById('ttt-reset').addEventListener('click', ()=>{ board = Array(9).fill(''); current='X'; lock=false; draw(); document.getElementById('ttt-status').textContent='Du bist X. Viel Spaß!'; });
  draw();

  // Ideen-Formular via Fetch zu FormSubmit (bleibt auf der Seite)
  const form = document.getElementById('idea-form');
  if(form){
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const msg = document.getElementById('idea-msg');
      msg.textContent = 'Sende ...'; msg.className='muted';
      try{
        const data = new FormData(form);
        const res = await fetch(form.action, { method:'POST', body:data, headers: { 'Accept':'application/json' } });
        if(res.ok){
          msg.textContent = 'Danke! Deine Idee wurde gesendet 🙌'; msg.className='ok';
          form.reset();
        }else{
          msg.textContent = 'Leider fehlgeschlagen. Versuche es später nochmal.'; msg.className='err';
        }
      }catch(err){
        msg.textContent = 'Netzwerkfehler. Bitte später erneut versuchen.'; msg.className='err';
      }
    });
  }

  // Start
  renderFavs();
  loadFact();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        time=now.strftime("%H:%M:%S"),
        date=now.strftime("%d.%m.%Y"),
        form_url=FORMSUBMIT_URL,
        sent=request.args.get("sent")  # optional für Erfolgsmeldung
    )


@app.route("/api/fact")
def fact_api():
    cat = request.args.get("cat", "random").lower()
    if cat == "random":
        text = random.choice(ALL_FACTS)
    else:
        if cat not in FACTS:
            cat = random.choice(list(FACTS.keys()))
        text = random.choice(FACTS[cat])
    return jsonify({"fact": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

