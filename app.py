from flask import Flask, jsonify, render_template_string, request
import random
import datetime
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# -----------------------------
#   Datenbasis: Fun-Facts
# -----------------------------
FACTS = {
    "lustig": [
        "Kühe haben beste Freunde und werden gestresst, wenn man sie trennt. 🐄❤️",
        "Ein Schneckenkuss kann bis zu drei Minuten dauern. 🐌💋",
        "Bananen sind Beeren – Erdbeeren nicht. 🍌🍓",
        "Wombat-Kot ist würfelförmig. ◼️",
        "Ein Oktopus hat drei Herzen. 🐙"
    ],
    "tiere": [
        "Raben können Gesichter erkennen und sich lange merken. 🐦",
        "Axolotl können ganze Gliedmaßen nachwachsen lassen. 🦎",
        "Seesterne haben kein Gehirn. ⭐",
        "Fische können Musik unterscheiden. 🎵🐟",
        "Koalas schlafen bis zu 22 Stunden am Tag. 😴"
    ],
    "space": [
        "Auf der Venus regnet es Metall. ☄️",
        "Ein Tag auf der Venus ist länger als ein Jahr auf der Venus. 🪐",
        "Es gibt mehr Sterne im Universum als Sandkörner auf allen Stränden der Erde. ✨",
        "Neutronensterne können 600 Umdrehungen pro Sekunde machen. 🌀",
        "Im All hört dich niemand schreien – Schall braucht ein Medium. 🌌"
    ],
    "wissen": [
        "Das Internet wiegt ungefähr so viel wie eine Erdbeere. 🍓",
        "Honig verdirbt praktisch nie – man fand essbaren Honig in Pyramiden. 🍯",
        "Die erste E-Mail wurde 1971 verschickt. 📧",
        "Menschen und Giraffen haben gleich viele Halswirbel: sieben. 🦒",
        "Der heißeste Chili misst über 2 Millionen Scoville. 🌶️"
    ]
}

ALL_CATS = list(FACTS.keys())
ALL_FACTS = sum(FACTS.values(), [])


# -----------------------------
#             HTML
# -----------------------------
HTML = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <title>🎉 Fun-Facts · Smooth Clock</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{
      --bg:#0d1117; --panel:#161b22; --text:#e6edf3; --muted:#9da7b3;
      --brand:#58a6ff; --ok:#22c55e; --btn:#23836c; --border:#202734;
    }
    *{box-sizing:border-box}
    body{ margin:0; font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;
          background:var(--bg); color:var(--text); }
    header{ padding:22px 16px; border-bottom:1px solid var(--border)}
    h1{ margin:0; font-size:clamp(1.3rem, 2.5vw, 1.8rem) }
    main{ max-width:980px; margin:24px auto; padding:0 16px; display:grid; gap:18px }
    .card{ background:var(--panel); border:1px solid var(--border); border-radius:16px; padding:18px }
    h2{ margin:0 0 12px 0; color:var(--brand) }
    .row{ display:flex; gap:12px; align-items:center; flex-wrap:wrap }
    .btn{
      padding:10px 14px; background:var(--btn); color:#fff; border:none; border-radius:12px;
      font-weight:600; cursor:pointer;
    }
    .btn:hover{ filter:brightness(1.05) }
    .pill{ display:inline-block; padding:6px 10px; border-radius:999px;
           background:#0f131a; border:1px solid var(--border); font-size:.9rem }
    .box{ background:#0f131a; border:1px solid var(--border); border-radius:12px; padding:12px }
    .muted{ color:var(--muted) }

    /* Uhr/Datum */
    .clock{ font-size: clamp(2rem, 7vw, 3.4rem); font-weight:800; letter-spacing:.03em }
    .date{ opacity:.85; margin-top:4px; font-size:1.1rem }

    /* TicTacToe */
    #t3-board{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; max-width:360px }
    .t3-cell{
      width:110px; height:110px; display:flex; align-items:center; justify-content:center;
      background:#0f131a; border:1px solid var(--border); border-radius:14px;
      font-weight:800; font-size:44px; user-select:none; cursor:pointer; transition:transform .05s;
    }
    .t3-cell:hover{ transform:scale(1.02) }
    .t3-x{ color:#f87171 }  /* X rot   */
    .t3-o{ color:#60a5fa }  /* O blau  */
    .t3-win{ box-shadow:0 0 0 2px var(--ok) inset }
    @media(max-width:520px){ .t3-cell{ width:92px;height:92px;font-size:38px } }

    /* Idee-Form */
    input[type="text"], textarea{
      width:100%; background:#0f131a; border:1px solid var(--border); color:var(--text);
      padding:10px 12px; border-radius:10px; outline:none;
    }
    textarea{ min-height:110px; resize:vertical }
    .ok{ color:var(--ok) }
    .err{ color:#f87171 }
    footer{ text-align:center; padding:18px; color:var(--muted) }
  </style>
</head>
<body>
  <header>
    <h1>🎉 Fun-Facts · Smooth Clock</h1>
  </header>

  <main>

    <!-- Uhr / Datum -->
    <section class="card">
      <h2>🕒 Aktuelle Zeit &amp; Datum</h2>
      <div class="box">
        <div id="clock" class="clock">--:--:--</div>
        <div id="date"  class="date">--.--.----</div>
      </div>
    </section>

    <!-- Fun Facts -->
    <section class="card">
      <h2>✨ Fun-Facts</h2>

      <div class="row" style="margin-bottom:10px">
        <label class="pill">Kategorie:
          <select id="cat"
            style="margin-left:8px;background:#0f131a;border:1px solid var(--border);color:var(--text);padding:6px 10px;border-radius:8px;">
            <option value="lustig">Lustig</option>
            <option value="tiere">Tiere</option>
            <option value="space">Space</option>
            <option value="wissen">Wissen</option>
            <option value="random">Zufällig</option>
          </select>
        </label>

        <button id="btn-new" class="btn">🎲 Neuen Fakt</button>
        <button id="btn-copy" class="btn" style="background:#444;">📋 Kopieren</button>
        <button id="btn-fav"  class="btn" style="background:#444;">⭐ Favorit</button>
      </div>

      <div id="fact" class="box" style="font-size:1.2rem; line-height:1.6">Klicke „Neuen Fakt“ 🙌</div>

      <div style="margin-top:14px">
        <h3 style="margin:0 0 8px 0" class="muted">⭐ Favoriten</h3>
        <div id="favs" class="box" style="min-height:52px"></div>
        <div class="row" style="margin-top:8px">
          <button id="btn-clear" class="btn" style="background:#444">🧹 Leeren</button>
        </div>
      </div>
    </section>

    <!-- Tic-Tac-Toe -->
    <section class="card" id="t3">
      <h2>🎮 Tic-Tac-Toe</h2>
      <div class="row" style="margin-bottom:10px">
        <label class="pill">Schwierigkeit:
          <select id="t3-level"
              style="margin-left:8px;background:#0f131a;border:1px solid var(--border);color:var(--text);padding:6px 10px;border-radius:8px;">
            <option value="easy">Easy</option>
            <option value="hard" selected>Hard (unbesiegbar)</option>
          </select>
        </label>
        <span id="t3-status" class="pill">Du bist ❌ – du beginnst!</span>
        <span id="t3-score"  class="pill">Siege: 0 | Niederl.: 0 | Remis: 0</span>
        <button id="t3-reset" class="btn">🔁 Neues Spiel</button>
        <button id="t3-clear" class="btn" style="background:#444;">🧹 Score löschen</button>
      </div>
      <div id="t3-board"></div>
    </section>

    <!-- Idee einsenden -->
    <section class="card">
      <h2>💡 Deine Idee für die Website</h2>
      <div class="row" style="margin-bottom:10px">
        <div style="flex:1; min-width:220px">
          <label for="idea-name" class="muted">Name</label><br>
          <input id="idea-name" type="text" placeholder="Dein Name" required />
        </div>
      </div>
      <div class="row" style="margin-bottom:10px">
        <div style="flex:1; min-width:220px">
          <label for="idea-text" class="muted">Deine Idee</label><br>
          <textarea id="idea-text" placeholder="Was soll auf die Seite?"></textarea>
        </div>
      </div>
      <div class="row">
        <button id="idea-send" class="btn">📨 Idee absenden</button>
        <span id="idea-msg" class="muted"></span>
      </div>
    </section>

  </main>

  <footer>Made by Aaron ✨</footer>

  <!-- =========================
            SCRIPTS
       ========================= -->
  <script>
    // ---------- Uhr ----------
    function pad(n){ return String(n).padStart(2, '0'); }
    function runClock(){
      const now = new Date();
      document.getElementById('clock').textContent =
        pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds());
      document.getElementById('date').textContent =
        pad(now.getDate()) + '.' + pad(now.getMonth()+1) + '.' + now.getFullYear();
    }
    runClock(); setInterval(runClock, 1000);

    // ---------- Fun Facts ----------
    const favKey = 'fun_facts_favs_v1';
    function renderFavs(){
      const box = document.getElementById('favs');
      const list = JSON.parse(localStorage.getItem(favKey) || '[]');
      if(!list.length){ box.innerHTML = '<span class="muted">Noch keine Favoriten.</span>'; return; }
      box.innerHTML = list.map(f => '<div style="margin:4px 0">'+ f +'</div>').join('');
    }
    async function loadFact(){
      const sel = document.getElementById('cat').value || 'random';
      const res = await fetch('/api/fact?cat=' + encodeURIComponent(sel));
      const data = await res.json();
      const el = document.getElementById('fact');
      el.textContent = data.fact;
      el.dataset.fact = data.fact;
    }
    document.getElementById('btn-new').onclick  = loadFact;
    document.getElementById('btn-copy').onclick = () => {
      const t = document.getElementById('fact').dataset.fact || document.getElementById('fact').textContent;
      navigator.clipboard.writeText(t);
    };
    document.getElementById('btn-fav').onclick = () => {
      const t = document.getElementById('fact').dataset.fact || document.getElementById('fact').textContent;
      if(!t) return;
      const list = JSON.parse(localStorage.getItem(favKey) || '[]');
      if(!list.includes(t)) list.unshift(t);
      localStorage.setItem(favKey, JSON.stringify(list.slice(0, 50)));
      renderFavs();
    };
    document.getElementById('btn-clear').onclick = () => {
      localStorage.removeItem(favKey); renderFavs();
    };
    renderFavs(); loadFact();

    // ---------- TicTacToe ----------
    (() => {
      const boardEl = document.getElementById('t3-board');
      const statusEl= document.getElementById('t3-status');
      const scoreEl = document.getElementById('t3-score');
      const resetBt = document.getElementById('t3-reset');
      const clearBt = document.getElementById('t3-clear');
      const levelSel= document.getElementById('t3-level');

      const W_KEY='t3_wins', L_KEY='t3_losses', D_KEY='t3_draws';
      let wins=+localStorage.getItem(W_KEY)||0,
          losses=+localStorage.getItem(L_KEY)||0,
          draws=+localStorage.getItem(D_KEY)||0;
      function updateScore(){ scoreEl.textContent = `Siege: ${wins} | Niederl.: ${losses} | Remis: ${draws}`; }
      updateScore();

      const combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
      ];

      let board, human='X', bot='O', running=true;

      function buildBoard(){
        boardEl.innerHTML='';
        for (let i=0;i<9;i++){
          const c=document.createElement('div');
          c.className='t3-cell';
          c.dataset.i=i;
          c.addEventListener('click', onHuman);
          boardEl.appendChild(c);
        }
      }

      function startGame(){
        board=Array(9).fill(null);
        running=true;
        buildBoard();
        statusEl.textContent='Du bist ❌ – du beginnst!';
      }

      function winner(b){
        for(const [a,b2,c] of combos){
          if(b[a] && b[a]===b[b2] && b[a]===b[c]) return {player:b[a], line:[a,b2,c]};
        }
        if(b.every(Boolean)) return {player:'draw'};
        return null;
      }

      function onHuman(e){
        if(!running) return;
        const i=+e.currentTarget.dataset.i;
        if(board[i]) return;
        place(i,human);
        const w=winner(board);
        if(endIfNeeded(w)) return;
        setTimeout(botMove, 320);
      }

      function place(i, p){
        board[i]=p;
        const cell=boardEl.children[i];
        cell.textContent=p==='X'?'✕':'◯';
        cell.classList.add(p==='X'?'t3-x':'t3-o');
      }
      function emptyIdx(b){ return b.map((v,i)=>v?null:i).filter(i=>i!==null); }

      function botMove(){
        let move;
        if(levelSel.value==='easy'){
          const free=emptyIdx(board);
          move=free[Math.floor(Math.random()*free.length)];
        }else{
          move = bestMove(board, bot).index;
        }
        place(move, bot);
        const w=winner(board);
        endIfNeeded(w);
      }

      // Minimax
      function bestMove(b, player){
        const w = winner(b);
        if(w){
          if(w.player===bot) return {score: 1};
          if(w.player===human) return {score:-1};
          return {score:0};
        }
        const moves=[];
        for(const i of emptyIdx(b)){
          const newB=b.slice(); newB[i]=player;
          const next = bestMove(newB, player===bot?human:bot);
          moves.push({index:i, score: next.score * (player===bot?1:-1)});
        }
        return player===bot
          ? moves.reduce((a,m)=> m.score>a.score?m:a)
          : moves.reduce((a,m)=> m.score<a.score?m:a);
      }

      function highlight(line){
        line.forEach(i=>boardEl.children[i].classList.add('t3-win'));
      }

      function endIfNeeded(w){
        if(!w) return false;
        running=false;
        if(w.player==='draw'){
          statusEl.textContent='Unentschieden.';
          draws++; localStorage.setItem(D_KEY,draws);
        }else if(w.player===human){
          statusEl.textContent='Du gewinnst! 🎉';
          highlight(w.line);
          wins++; localStorage.setItem(W_KEY,wins);
        }else{
          statusEl.textContent='Bot gewinnt 😅';
          highlight(w.line);
          losses++; localStorage.setItem(L_KEY,losses);
        }
        updateScore();
        return true;
      }

      resetBt.addEventListener('click', startGame);
      clearBt.addEventListener('click', ()=>{
        wins=losses=draws=0;
        localStorage.removeItem(W_KEY);
        localStorage.removeItem(L_KEY);
        localStorage.removeItem(D_KEY);
        updateScore();
      });

      startGame();
    })();

    // ---------- Idee senden ----------
    const ideaBtn  = document.getElementById('idea-send');
    const ideaName = document.getElementById('idea-name');
    const ideaText = document.getElementById('idea-text');
    const ideaMsg  = document.getElementById('idea-msg');

    ideaBtn.addEventListener('click', async () => {
      ideaMsg.textContent='';
      const name = (ideaName.value || '').trim();
      const text = (ideaText.value || '').trim();
      if(!name || text.length < 5){
        ideaMsg.textContent='Bitte Name angeben und eine sinnvoll lange Idee schreiben.';
        ideaMsg.className='err';
        return;
      }
      ideaBtn.disabled = true; ideaBtn.textContent='… wird gesendet';
      try{
        const res = await fetch('/submit_idea', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({name, idea:text})
        });
        const data = await res.json();
        if(data.ok){
          ideaMsg.textContent='Danke! Deine Idee wurde verschickt.';
          ideaMsg.className='ok';
          ideaText.value='';
        }else{
          ideaMsg.textContent='Fehler: ' + (data.error || 'Versand fehlgeschlagen.');
          ideaMsg.className='err';
        }
      }catch(e){
        ideaMsg.textContent='Netzwerkfehler – bitte später nochmal.';
        ideaMsg.className='err';
      }finally{
        ideaBtn.disabled=false; ideaBtn.textContent='📨 Idee absenden';
      }
    });
  </script>
</body>
</html>
"""

# -----------------------------
#            ROUTES
# -----------------------------
@app.route("/")
def home():
    return render_template_string(HTML)

@app.get("/api/fact")
def api_fact():
    cat = (request.args.get("cat") or "random").lower()
    if cat == "random" or cat not in FACTS:
        fact = random.choice(ALL_FACTS)
    else:
        fact = random.choice(FACTS[cat])
    return jsonify({"fact": fact})

# --------- Idee per Mail senden ----------
@app.post("/submit_idea")
def submit_idea():
    """
    Erwartet JSON: { "name": "...", "idea": "..." }
    Schickt die Idee per SMTP an MAIL_TO (default info@aaron-sigma.de).
    """
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    idea = (data.get("idea") or "").strip()

    if not name or len(idea) < 5:
        return jsonify({"ok": False, "error": "Ungültige Eingabe."}), 400

    # SMTP Konfiguration (über Env-Variablen)
    host = os.environ.get("SMTP_HOST", "smtp.hostinger.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "info@aaron-sigma.de")
    pwd  = os.environ.get("SMTP_PASS", "")
    to   = os.environ.get("MAIL_TO", "info@aaron-sigma.de")

    if not pwd:
        return jsonify({"ok": False, "error": "Mailer nicht konfiguriert."}), 500

    body = f"Neue Idee von {name}:\n\n{idea}\n\n— automatisch gesendet von aaron-sigma.de"
    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = "Neue Website-Idee"
    msg["From"] = user
    msg["To"] = to

    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            server.login(user, pwd)
            server.send_message(msg)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
