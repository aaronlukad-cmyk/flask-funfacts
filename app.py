import os
import random
import datetime
from flask import Flask, jsonify, render_template_string, request
from flask_mail import Mail, Message

app = Flask(__name__)

# -----------------------------
#  Mail-Config aus Umgebungsvariablen
# -----------------------------
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", "465"))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "False") == "True"
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL", "True") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", "")
MAIL_TO = os.environ.get("MAIL_TO", app.config["MAIL_DEFAULT_SENDER"])

mail = Mail(app)

# -------------------------------------------------
#   HTML-Template (Seite, Stil, JS)
# -------------------------------------------------
HTML = r"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>🎉 Fun-Facts • Smooth Clock • Mini-Games</title>
<style>
  :root {
    --bg: #0f172a;
    --card: #111827;
    --text: #e5e7eb;
    --muted: #9ca3af;
    --primary: #60a5fa;
    --success: #22c55e;
    --danger: #ef4444;
    --accent: #34d399;
  }
  html, body {
    margin: 0; padding: 0;
    background: var(--bg); color: var(--text);
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial, sans-serif;
  }
  .wrap { max-width: 1100px; margin: 24px auto; padding: 0 16px;}
  .title { font-size: clamp(28px, 4vw, 42px); line-height: 1.2; margin: 0 0 12px}
  .subtitle { color: var(--muted); margin: 0 0 32px; }
  .grid { display: grid; gap: 18px; grid-template-columns: repeat(12,1fr);}
  .col-12 { grid-column: span 12; } .col-6 { grid-column: span 6; }
  .card { background: var(--card); border-radius: 16px; padding: 18px; box-shadow: 0 12px 40px rgba(0,0,0,.25);}
  .hl { color: #93c5fd; }
  .btn { background: var(--accent); color: #052e22; border:0; border-radius: 12px; padding: 12px 16px; font-weight: 700; cursor:pointer; transition: .2s transform, .2s opacity;}
  .btn:hover { transform: translateY(-1px); opacity: .95;}
  .btn-ghost { background: #1f2937; color: var(--text);}
  .row { display:flex; gap:10px; flex-wrap: wrap; align-items: center}
  input, textarea, select {
    width:100%; box-sizing:border-box; background:#0b1220; border:1px solid #25324a;
    color:var(--text); border-radius:12px; padding:12px 14px; font-size:16px; outline: none;
  }
  .label { font-weight:700; margin: 8px 0 6px; display:block;}
  .muted { color: var(--muted); font-size: 14px;}
  .footer { text-align:center; color:var(--muted); margin: 26px 0 40px}
  .badge { padding: 6px 10px; border-radius: 999px; background:#1f2937; color:#cbd5e1; font-size:12px; font-weight:700;}
  /* Clock */
  .clock { font-size: clamp(36px, 6vw, 72px); letter-spacing: 1px; text-align:center; font-weight:900;}
  .date { text-align:center; color: var(--muted); margin-top: 6px; font-weight:600;}
  /* Fact box */
  .fact { font-size: 20px; line-height:1.6; }
  .pill { background:#0b1220; padding:8px 12px; border-radius:999px; border:1px solid #243149; }
  /* Tic tac toe */
  .ttt-grid { display:grid; grid-template-columns: repeat(3, 100px); gap:10px; justify-content:center; padding:12px 0}
  .ttt-cell { width:100px; height:100px; background:#0b1220; border:1px solid #243149; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:42px; font-weight:900; cursor:pointer; user-select:none;}
  .ttt-info { text-align:center; margin-top:8px; font-weight:700 }
  .ok { color: var(--success);} .err { color: var(--danger);}
  @media (max-width: 900px) { .col-6 { grid-column: span 12; } }
</style>
</head>
<body>
<div class="wrap">
  <h1 class="title">🎉 Fun-Facts • Smooth <span class="hl">Clock</span></h1>
  <p class="subtitle">Uhrzeit + Datum, zufällige Fakten, Tic-Tac-Toe & Ideenformular</p>

  <div class="grid">
    <!-- Clock -->
    <div class="col-6 card">
      <div class="row" style="justify-content:space-between">
        <span class="badge">⏰ Aktuelle Zeit</span>
        <span id="tz" class="muted"></span>
      </div>
      <div id="clock" class="clock">--:--:--</div>
      <div id="date" class="date">--.--.----</div>
    </div>

    <!-- Facts -->
    <div class="col-6 card">
      <div class="row" style="justify-content:space-between; margin-bottom:12px">
        <span class="badge">💡 Fun-Facts</span>
        <div class="row">
          <select id="cat" class="pill">
            <option value="random">Zufällig</option>
            <option value="lustig">Lustig</option>
            <option value="tiere">Tiere</option>
            <option value="wissenschaft">Wissenschaft</option>
            <option value="misc">Misc</option>
          </select>
          <button id="btn-new" class="btn">🎲 Neuen Fakt</button>
        </div>
      </div>
      <div id="fact" class="fact">Klick auf „Neuen Fakt“ 🎲</div>
    </div>

    <!-- Tic tac toe -->
    <div class="col-6 card">
      <div class="row" style="justify-content:space-between">
        <span class="badge">🎮 Mini-Game</span>
        <button id="ttt-reset" class="btn btn-ghost">↺ Reset</button>
      </div>
      <div class="ttt-grid" id="ttt">
        <div class="ttt-cell" data-i="0"></div>
        <div class="ttt-cell" data-i="1"></div>
        <div class="ttt-cell" data-i="2"></div>
        <div class="ttt-cell" data-i="3"></div>
        <div class="ttt-cell" data-i="4"></div>
        <div class="ttt-cell" data-i="5"></div>
        <div class="ttt-cell" data-i="6"></div>
        <div class="ttt-cell" data-i="7"></div>
        <div class="ttt-cell" data-i="8"></div>
      </div>
      <div class="ttt-info" id="ttt-info">Du bist <b>X</b>. Viel Spaß!</div>
    </div>

    <!-- Idea form -->
    <div class="col-6 card">
      <span class="badge">💡 Deine Idee für die Website</span>
      <label class="label" for="idea-name">Name</label>
      <input id="idea-name" placeholder="Dein Name"/>
      <label class="label" for="idea-text">Deine Idee</label>
      <textarea id="idea-text" rows="6" placeholder="Was sollen wir bauen?"></textarea>
      <div class="row" style="margin-top:10px">
        <button id="idea-send" class="btn">📧 Idee absenden</button>
        <span id="idea-msg" class="muted"></span>
      </div>
      <div id="mailer-warning" class="muted" style="margin-top:8px;"></div>
    </div>
  </div>

  <p class="footer">Made by Aaron ✨</p>
</div>

<script>
/* ---------- Clock ---------- */
function pad(n){return ("0"+n).slice(-2)}
function tick(){
  const d = new Date();
  document.getElementById("clock").textContent =
    pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
  document.getElementById("date").textContent =
    pad(d.getDate()) + "." + pad(d.getMonth()+1) + "." + d.getFullYear();
}
setInterval(tick,1000); tick();
document.getElementById("tz").textContent = Intl.DateTimeFormat().resolvedOptions().timeZone;

/* ---------- Facts ---------- */
async function loadFact(){
  const cat = document.getElementById("cat").value;
  const r = await fetch("/api/fact?cat="+encodeURIComponent(cat));
  const j = await r.json();
  document.getElementById("fact").textContent = j.fact || "—";
}
document.getElementById("btn-new").addEventListener("click", loadFact);

/* ---------- TicTacToe ---------- */
const cells = [...document.querySelectorAll(".ttt-cell")];
const info  = document.getElementById("ttt-info");
let board = Array(9).fill(null);
let player = "X";
const wins = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6]
];
function winner(b){
  for(const [a,b2,c] of wins){
    if(b[a] && b[a]===b[b2] && b[a]===b[c]) return b[a];
  }
  if(b.every(Boolean)) return "draw";
  return null;
}
function aiMove(){
  // sehr einfach: nimm erste freie Zelle
  const i = board.findIndex(v => !v);
  if(i>=0){ board[i] = "O"; cells[i].textContent = "O"; }
}
function handleClick(e){
  const i = +e.target.dataset.i;
  if(board[i] || winner(board)) return;
  board[i] = "X"; e.target.textContent = "X";
  let w = winner(board);
  if(w){
    info.innerHTML = (w==="draw") ? "Unentschieden!" : "Gewonnen: <b>"+w+"</b>";
    return;
  }
  aiMove();
  w = winner(board);
  if(w){
    info.innerHTML = (w==="draw") ? "Unentschieden!" : "Gewonnen: <b>"+w+"</b>";
  }
}
cells.forEach(c => c.addEventListener("click", handleClick));
document.getElementById("ttt-reset").addEventListener("click", () => {
  board = Array(9).fill(null);
  cells.forEach(c => c.textContent = "");
  info.innerHTML = "Du bist <b>X</b>. Viel Spaß!";
});

/* ---------- Idea form ---------- */
async function sendIdea(){
  const name = document.getElementById("idea-name").value.trim();
  const idea = document.getElementById("idea-text").value.trim();
  const msg  = document.getElementById("idea-msg");
  msg.textContent = "Sende...";
  try{
    const r = await fetch("/send_idea", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({name, idea})
    });
    const j = await r.json();
    if(j.ok){
      msg.textContent = "Danke! Idee wurde gesendet.";
      msg.className = "ok";
      document.getElementById("idea-name").value = "";
      document.getElementById("idea-text").value = "";
    } else {
      msg.textContent = "Fehler: " + (j.error || "Mailer nicht konfiguriert.");
      msg.className = "err";
    }
  }catch(e){
    msg.textContent = "Fehler beim Senden.";
    msg.className = "err";
  }
}
document.getElementById("idea-send").addEventListener("click", sendIdea);
</script>
</body>
</html>
"""

# -------------------------------------------------
#  Spaß-Fakten (ein paar Beispiele + Kategorien)
# -------------------------------------------------
FACTS = {
    "lustig": [
        "Kühe haben beste Freunde und werden gestresst, wenn man sie trennt. 🐄❤️",
        "Wenn Katzen glücklich sind, treten sie mit ihren Pfoten – als würden sie Teig kneten. 🐱🍞",
        "Eine Schnecke kann bis zu drei Jahre schlafen. 😴🐌",
    ],
    "tiere": [
        "Tintenfische haben drei Herzen. 🐙",
        "Pinguine machen ihren Partnern Heiratsanträge mit einem Kieselstein. 🐧💎",
        "Eine Honigbiene besucht bis zu 500 Blumen am Tag. 🐝🌼",
    ],
    "wissenschaft": [
        "Wasser kann gleichzeitig kochen und frieren – Triple Point! 💧",
        "Banane ist leicht radioaktiv (Kalium-40). 🍌",
        "Menschen und Giraffen haben die gleiche Anzahl an Halswirbeln: 7. 🦒",
    ],
    "misc": [
        "Die erste Webseite der Welt ist immer noch online (info.cern.ch). 🌐",
        "„Monty Python“ gab der Programmiersprache Python ihren Namen – nicht die Schlange. 🐍",
        "Der Eiffelturm wird im Sommer bis zu 15 cm höher (Wärmeausdehnung). 🗼",
    ]
}

ALL_FACTS = [f for arr in FACTS.values() for f in arr]

# -------------------------------------------------
#  Routes
# -------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)

@app.route("/api/fact")
def api_fact():
    cat = (request.args.get("cat") or "random").lower()
    if cat == "random" or cat not in FACTS:
        fact = random.choice(ALL_FACTS)
    else:
        fact = random.choice(FACTS[cat])
    return jsonify({"fact": fact})

@app.route("/send_idea", methods=["POST"])
def send_idea():
    """Nimmt JSON {name, idea} entgegen und sendet E-Mail.
       Gibt {ok:true} zurück, wenn erfolgreich.
    """
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip() or "Anonym"
    idea = (data.get("idea") or "").strip()

    if not idea:
        return jsonify({"ok": False, "error": "Idee fehlt."}), 400

    # Prüfen, ob Mail konfiguriert ist
    required = [
        app.config.get("MAIL_SERVER"),
        app.config.get("MAIL_DEFAULT_SENDER"),
        app.config.get("MAIL_USERNAME"),
        app.config.get("MAIL_PASSWORD"),
    ]
    if any(not v for v in required):
        return jsonify({"ok": False, "error": "Mailer nicht konfiguriert."}), 200

    try:
        subject = "Neue Website-Idee von {}".format(name)
        body = f"Name: {name}\n\nIdee:\n{idea}\n\n— aaron-sigma.de"
        msg = Message(subject=subject, recipients=[MAIL_TO], body=body)
        mail.send(msg)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 200


# Optional: einfacher Test-Endpoint zum Prüfen der Mail-Config
@app.route("/testmail")
def testmail():
    """ /testmail?to=foo@bar.de """
    to = request.args.get("to") or MAIL_TO
    try:
        msg = Message(subject="Testmail von aaron-sigma.de",
                      recipients=[to],
                      body="Wenn diese Mail ankommt, ist die Mail-Konfiguration okay. ✨")
        mail.send(msg)
        return "OK – Mail verschickt an {}".format(to)
    except Exception as e:
        return "Fehler: {}".format(e), 500


if __name__ == "__main__":
    # Lokaler Start (Render startet über gunicorn)
    app.run(host="0.0.0.0", port=5000, debug=False)
