from flask import Flask, session, request, jsonify, render_template_string
import random

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-32bytes"

# ------------------- Guthaben -------------------
def get_balance():
    if "balance" not in session:
        session["balance"] = 100
    return session["balance"]

def set_balance(v):
    session["balance"] = int(v)
    return session["balance"]

def add_balance(v):
    return set_balance(get_balance() + int(v))

# ------------------- Codes ----------------------
CODES = {
    "LEON": 100, "ARMIN": 101,
    "EAGLE": 200, "RIVER": 200, "COMET": 200,
    "MANGO": 75, "DRAGON": 75,
    "PINE": 50, "WOLF": 50,
    "JACKPOT": 1000
}
USED = set()

# ------------------- Funfacts -------------------
FUNNY_FACTS = [
    "Ein Seeigel hat kein Gehirn – organisiert aber besser als ich.",
    "Der Eiffelturm wächst im Sommer bis zu 15 cm. Meine Motivation nicht.",
    "Hummeln fliegen, obwohl die Aerodynamik dagegen ist. Einfach machen!",
    "Im Weltall riecht es nach verbranntem Steak. Veggies win.",
    "Honig verdirbt nie. Wenn er alt ist, gehört er vermutlich Mumien.",
    "Schafe erkennen Gesichter. Trotzdem ignorieren sie deine DMs.",
    "Goldfische haben ein Gedächtnis – die Ausrede ist hinüber.",
    "Faultiere brauchen eine Woche für die Verdauung. Ich für Montag.",
    "Katzen haben 100+ Laute. Menschen nur ‚Miau – aufstehen!‘",
    "Enten quaken ohne Echo. Behaupten Enten zumindest."
]

# ------------------- Templates ------------------
BASE = r"""
<!doctype html><html lang="de"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }}</title>
<style>
:root{
  --bg:#0f172a; --card:#111827; --muted:#9ca3af; --accent:#2563eb;
  --good:#22c55e; --bad:#ef4444; --text:#e5e7eb;
  --black:#0b1220; --red:#7f1d1d; --green:#065f46;
}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,system-ui,Segoe UI,Roboto,Arial,sans-serif}
a{color:inherit;text-decoration:none} .wrap{max-width:980px;margin:0 auto;padding:16px}
.nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.brand{font-weight:800;font-size:22px} .dd{position:relative}
.dd-btn{background:#1f2937;border:0;border-radius:12px;color:#e5e7eb;padding:10px 16px;cursor:pointer}
.dd-menu{position:absolute;right:0;top:44px;background:#0b1220;border:1px solid #1f2937;border-radius:12px;min-width:200px;display:none}
.dd-menu a{display:block;padding:10px 14px;border-bottom:1px solid #111827}
.dd:hover .dd-menu{display:block}
.card{background:var(--card);border:1px solid #1f2937;border-radius:16px;padding:16px}
.row{display:flex;gap:16px;flex-wrap:wrap} .col{flex:1 1 300px}
.hr{height:1px;background:#1f2937;margin:18px 0}
.btn{background:var(--accent);border:0;color:#fff;border-radius:12px;padding:10px 16px;cursor:pointer}
.btn.secondary{background:#1f2937} .btn.ghost{background:#0b1220}
input,select{background:#0b1220;border:1px solid #1f2937;border-radius:10px;color:#e5e7eb;padding:10px 12px}
.msg{margin-top:10px;font-weight:600}
.muted{color:var(--muted)} h1,h2,h3{margin:8px 0 12px}
.clock{font-size:54px;font-weight:800;background:linear-gradient(90deg,#22c55e,#06b6d4,#2563eb,#a855f7,#f59e0b);
       -webkit-background-clip:text;background-clip:text;color:transparent;animation:hue 6s linear infinite}
.clock-date{color:#94a3b8} @keyframes hue{0%{filter:hue-rotate(0)}100%{filter:hue-rotate(360deg)}}
.cards{display:flex;gap:10px}
.card-face{width:118px;height:160px;border-radius:14px;border:1px dashed #2a3344;background:
  repeating-linear-gradient(45deg,#0b1220,#0b1220 6px,#12192a 6px,#12192a 12px);display:flex;align-items:center;justify-content:center}
.card-num{font-size:34px} .red{color:#ef4444}

.tabs{display:flex;gap:8px;margin-bottom:12px}
.tab{padding:10px 14px;border-radius:10px;background:#0b1220;border:1px solid #1f2937;color:#cbd5e1;cursor:pointer}
.tab.active{background:var(--accent);color:#fff;border-color:transparent}
.tab-panel{display:none} .tab-panel.active{display:block}

/* Roulette – QUADRATISCH stabil */
.wheel-wrap{position:relative;width:360px;aspect-ratio:1;background:var(--black);border-radius:50%;border:10px solid var(--black);overflow:hidden}
.pointer{position:absolute;left:50%;top:-6px;transform:translateX(-50%); width:0;height:0;
  border-left:12px solid transparent;border-right:12px solid transparent;border-bottom:20px solid #fbbf24;z-index:10}
#wheel{position:absolute;inset:0;border-radius:50%;display:flex;align-items:center;justify-content:center}
#disc{position:absolute;width:320px;height:320px;border-radius:50%;background:#111827}
#ball{position:absolute;left:50%;top:50%;width:18px;height:18px;border-radius:50%;background:#fff;
  transform:translate(-50%,-50%) rotate(0deg) translate(138px);box-shadow:0 0 8px rgba(255,255,255,.6);z-index:8}
#labels{position:absolute;inset:0} .lbl{position:absolute;left:50%;top:50%;transform-origin:0 -145px;color:#e5e7eb;font-weight:700;font-size:12px;text-shadow:0 1px 2px #000}

.seg{position:absolute;width:360px;height:360px;border-radius:50%}
</style>
</head>
<body>
<div class="wrap">
  <div class="nav">
    <div class="brand">aaron-sigma.de</div>
    <div class="dd">
      <button class="dd-btn">Bereiche ▾</button>
      <div class="dd-menu">
        <a href="/">Start</a>
        <a href="/fun">Funfacts</a>
        <a href="/casino">Casino</a>
      </div>
    </div>
  </div>
  {% block body %}{% endblock %}
  <div style="text-align:center;margin:24px 0" class="muted">Made by Aaron ✨</div>
</div>
</body></html>
"""

INDEX = r"""
{% extends "base" %}{% block body %}
<section class="card">
  <h2>Willkommen!</h2>
  <div class="row">
    <div class="col">
      <div class="clock" id="clk">--:--:--</div>
      <div class="clock-date" id="dat">--.--.----</div>
    </div>
    <div class="col">
      <p class="muted">Dein kleines Universum: Uhrzeit, Funfacts, Casino & Aaron Dollar.</p>
      <p class="muted">Alles lokal gespeichert – bleibt im Browser erhalten.</p>
    </div>
  </div>
</section>
<script>
function p(n){return n<10?("0"+n):n}
function tick(){const d=new Date();clk.textContent=p(d.getHours())+":"+p(d.getMinutes())+":"+p(d.getSeconds()); dat.textContent=p(d.getDate())+"."+p(d.getMonth()+1)+"."+d.getFullYear()}
setInterval(tick,1000);tick();
</script>
{% endblock %}
"""

FUN = r"""
{% extends "base" %}{% block body %}
<section class="card">
  <h2>😂 Funfacts</h2>
  <div class="row"><div class="col">
    <div id="fact" class="card" style="padding:12px"></div>
    <div style="margin-top:10px"><button class="btn" id="newf">Neuen Funfact</button></div>
  </div></div>
</section>
<script>
const FACTS={{facts|tojson}};
function showF(){fact.textContent=FACTS[Math.floor(Math.random()*FACTS.length)]}
newf.addEventListener("click",showF);showF();
</script>
{% endblock %}
"""

CASINO = r"""
{% extends "base" %}{% block body %}
<section class="card">
  <h2>🎰 Casino</h2>

  <div class="card" style="margin-bottom:14px">
    <div><b>Guthaben:</b> <span id="bal">0</span> A$</div>
    <div class="row" style="margin-top:10px">
      <div class="col"><input id="code" placeholder="Gutschein-Code"></div>
      <div class="col" style="flex:0 0 auto"><button class="btn" id="redeem">Einlösen</button></div>
    </div>
    <div id="rmsg" class="msg"></div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="bj">Blackjack</button>
    <button class="tab" data-tab="rl">Roulette</button>
  </div>

  <!-- BLACKJACK -->
  <div id="p-bj" class="tab-panel active">
    <div class="row">
      <div class="col" style="flex:0 0 220px">
        <label>Einsatz:</label> <input id="bjbet" type="number" value="10" min="1" step="1" style="width:120px"> A$
      </div>
    </div>
    <div class="row"><button class="btn" id="bjnew">Neue Runde</button>
      <button class="btn secondary" id="bjhit">Hit</button>
      <button class="btn ghost" id="bjstand">Stand</button></div>

    <div class="row" style="margin-top:14px">
      <div class="col"><h3>Dealer</h3><div class="cards" id="dhand"></div><div id="dscore" class="muted">–</div></div>
      <div class="col"><h3>Spieler</h3><div class="cards" id="phand"></div><div id="pscore" class="muted">–</div></div>
    </div>
    <div id="bjmsg" class="msg"></div>
  </div>

  <!-- ROULETTE -->
  <div id="p-rl" class="tab-panel">
    <div class="row" style="gap:12px">
      <div class="col" style="flex:0 0 220px">
        <label>Einsatz:</label> <input id="rlbet" type="number" value="10" min="1" step="1" style="width:120px"> A$
      </div>
    </div>

    <div class="row" style="gap:10px">
      <div class="col" style="flex:0 0 220px">
        <label>Wette:</label>
        <select id="type" style="width:220px">
          <option value="single">Zahl (0–36)</option>
          <option value="red">Rot</option>
          <option value="black">Schwarz</option>
          <option value="even">Gerade</option>
          <option value="odd">Ungerade</option>
          <option value="dozen1">1–12</option><option value="dozen2">13–24</option><option value="dozen3">25–36</option>
          <option value="col1">Spalte 1</option><option value="col2">Spalte 2</option><option value="col3">Spalte 3</option>
        </select>
      </div>
      <div class="col" id="nwrap" style="flex:0 0 220px">
        <label>Zahl:</label>
        <input id="num" type="number" min="0" max="36" value="7" style="width:120px">
      </div>
    </div>

    <div style="margin:12px 0"><button id="spin" class="btn">Spin</button></div>

    <div class="row" style="align-items:flex-start">
      <div class="wheel-wrap">
        <div class="pointer"></div>
        <div id="wheel">
          <div id="disc"></div>
          <div id="labels"></div>
        </div>
        <div id="ball"></div>
      </div>
      <div class="col">
        <div id="res" class="msg">Ergebnis: –</div>
        <div id="rlm" class="msg"></div>
      </div>
    </div>
  </div>
</section>

<script>
// Tabs
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  b.classList.add("active");
  document.querySelectorAll(".tab-panel").forEach(p=>p.classList.remove("active"));
  document.getElementById("p-"+b.dataset.tab).classList.add("active");
}));

// Balance
function setBal(v){document.getElementById("bal").textContent=v}
fetch("/api/balance").then(r=>r.json()).then(j=>setBal(j.balance));

redeem.onclick=()=>{
  fetch("/api/redeem",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code:code.value.trim()})})
  .then(r=>r.json()).then(j=>{rmsg.style.color=j.ok?"#22c55e":"#ef4444"; rmsg.textContent=j.ok?("+"+j.amount+" A$"):j.error; if(j.ok) setBal(j.balance);});
};

// -------- Blackjack ----------
const SUITS=["♠","♥","♦","♣"];
function newDeck(){const d=[];for(let s of SUITS){for(let v=1;v<=13;v++)d.push({s,v})}
  for(let i=d.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[d[i],d[j]]=[d[j],d[i]]} return d;}
function val(c){if(c.v>=10)return 10;if(c.v===1)return 11;return c.v}
function sc(h){let t=0,a=0;for(let c of h){t+=val(c);if(c.v===1)a++}while(t>21&&a) {t-=10;a--}return t}
function draw(el,h,hide2=false){el.innerHTML="";h.forEach((c,i)=>{const d=document.createElement("div");d.className="card-face";
 if(hide2&&i===1){el.appendChild(d);return}
 const n=(c.v===1?"A":c.v===11?"J":c.v===12?"Q":c.v===13?"K":c.v);const red=(c.s==="♥"||c.s==="♦");
 d.innerHTML=`<div class="card-num ${red?'red':''}">${n}${red?'<span class="red"> '+c.s+'</span>':' '+c.s}</div>`;el.appendChild(d);});}
let deck=[], dh=[], ph=[], over=false, hide=true;
bjnew.onclick=()=>{
  const bet=parseInt(bjbet.value||"0",10);
  fetch("/api/bet-check",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({bet})})
  .then(r=>r.json()).then(j=>{
    if(!j.ok){bjmsg.style.color="#ef4444";bjmsg.textContent=j.error;return;}
    deck=newDeck(); dh=[deck.pop(),deck.pop()]; ph=[deck.pop(),deck.pop()]; over=false; hide=true;
    draw(dhand,dh,true); draw(phand,ph,false); dscore.textContent="–"; pscore.textContent=sc(ph); bjmsg.textContent="";
  });
};
bjhit.onclick=()=>{ if(over) return; ph.push(deck.pop()); draw(phand,ph,false); const s=sc(ph); pscore.textContent=s;
 if(s>21){over=true; hide=false; end(false,"Bust! Dealer gewinnt.")}};
bjstand.onclick=()=>{ if(over) return; hide=false; while(sc(dh)<17){dh.push(deck.pop())}
 const ps=sc(ph), ds=sc(dh); if(ds>21) end(true,"Dealer bust! Du gewinnst.");
 else if(ps>ds) end(true,"Du gewinnst."); else if(ps<ds) end(false,"Dealer gewinnt."); else {draw(dhand,dh,false); dscore.textContent=ds; bjmsg.style.color="#f59e0b"; bjmsg.textContent="Unentschieden. Einsatz zurück.";}
};
function end(win,txt){draw(dhand,dh,false); dscore.textContent=sc(dh); bjmsg.style.color=win?"#22c55e":"#ef4444"; bjmsg.textContent=txt;
 const bet=parseInt(bjbet.value||"0",10); fetch("/api/bet-result",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({bet,win})})
 .then(r=>r.json()).then(j=>{if(j.ok) setBal(j.balance)});}

// -------- Roulette -----------
const ORDER=[0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26];
const sector=360/37;
let rot=0, brot=0;

function buildLabels(){
  const L=document.getElementById("labels"); L.innerHTML="";
  ORDER.forEach((n,i)=>{
    const a=i*sector;
    const lbl=document.createElement("div"); lbl.className="lbl";
    lbl.style.transform=`translate(-50%,-50%) rotate(${a}deg) translate(0,-145px) rotate(${-a}deg)`;
    lbl.textContent=n; L.appendChild(lbl);
  });
  // Segmente als conic-gradient: Grün/Rot/Schwarz
  const wheel=document.getElementById("wheel");
  let grad="conic-gradient(";
  for(let i=0;i<37;i++){
    const n=ORDER[i];
    const col = (n===0) ? "var(--green)" : ([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(n) ? "var(--red)" : "var(--black)");
    const start=i*sector, end=(i+1)*sector;
    grad += `${col} ${start}deg ${end}deg,`;
  }
  grad = grad.replace(/,$/,"") + ")";
  wheel.style.background = grad;
}
buildLabels();

function showNumField(){nwrap.style.display = (type.value==="single")?"block":"none"}
type.addEventListener("change",showNumField); showNumField();

function rlMsg(t,ok){rlm.style.color=ok?"#22c55e":"#ef4444"; rlm.textContent=t}

spin.onclick=()=>{
  const bet=parseInt(rlbet.value||"0",10);
  fetch("/api/bet-check",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({bet})})
   .then(r=>r.json()).then(j=>{
     if(!j.ok){rlMsg(j.error,false);return;}
     spinNow(bet);
   });
};

function spinNow(bet){
  const t=type.value, choice=parseInt(num.value||"0",10);
  const idx=Math.floor(Math.random()*37); const number=ORDER[idx];
  const color=(number===0)?"grün":([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(number)?"rot":"schwarz");
  res.textContent="Ergebnis: Zahl "+number+", Farbe "+color;

  const target= 360 - (idx*sector) - sector/2;   // Zeiger oben
  const spins=5; const final= rot + spins*360 + target;
  const bfinal = brot + spins*360 + target + 720;

  wheel.style.transition="transform 3.6s cubic-bezier(.2,.9,.2,1)";
  ball.style.transition ="transform 3.6s cubic-bezier(.2,.9,.2,1)";
  requestAnimationFrame(()=>{
    wheel.style.transform = `rotate(${final}deg)`;
    ball.style.transform  = `translate(-50%,-50%) rotate(${bfinal}deg) translate(138px)`;
  });

  setTimeout(()=>{
    rot = final%360; brot = bfinal%360;
    const win = payout(t,choice,number,bet);
    fetch("/api/roulette-result",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({bet,win:(win>0),winAmount:win})})
      .then(r=>r.json()).then(j=>{ if(j.ok){setBal(j.balance); rlMsg(win>0?("Gewonnen: +"+win+" A$"):("Verloren: -"+bet+" A$"), win>0);} });
  },3700);
}
function payout(t,choice,n,bet){
  const reds=new Set([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]);
  const blacks=new Set([2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]);
  if(t==="single") return (n===choice)? bet*35:0;
  if(t==="red") return reds.has(n)? bet*2:0;
  if(t==="black") return blacks.has(n)? bet*2:0;
  if(t==="even") return (n!==0 && n%2===0)? bet*2:0;
  if(t==="odd") return (n%2===1)? bet*2:0;
  if(t==="dozen1") return (1<=n&&n<=12)? bet*3:0;
  if(t==="dozen2") return (13<=n&&n<=24)? bet*3:0;
  if(t==="dozen3") return (25<=n&&n<=36)? bet*3:0;
  if(t==="col1") return [1,4,7,10,13,16,19,22,25,28,31,34].includes(n)? bet*3:0;
  if(t==="col2") return [2,5,8,11,14,17,20,23,26,29,32,35].includes(n)? bet*3:0;
  if(t==="col3") return [3,6,9,12,15,18,21,24,27,30,33,36].includes(n)? bet*3:0;
  return 0;
}
</script>
{% endblock %}
"""

# ------------------- Routes -------------------
@app.route("/")
def index():
    return render_template_string(BASE.replace("{{ title }}","Start"), title="Start",
                                  **{"self":None}, **{"__builtins__":{}},
                                  **{"block_body":""}, **{"body":""},
                                  )

@app.route("/")
def _start():
    # Need separate to pass template inheritance: render two-step
    return render_template_string(BASE, title="Start") \
           .replace("{% block body %}{% endblock %}", INDEX)

@app.route("/fun")
def fun():
    html = render_template_string(BASE, title="Funfacts").replace(
        "{% block body %}{% endblock %}",
        render_template_string(FUN, facts=FUNNY_FACTS)
    )
    return html

@app.route("/casino")
def casino():
    html = render_template_string(BASE, title="Casino").replace(
        "{% block body %}{% endblock %}",
        CASINO
    )
    return html

# ---------- APIs ----------
@app.route("/api/balance")
def api_balance():
    return jsonify(ok=True, balance=get_balance())

@app.route("/api/redeem", methods=["POST"])
def api_redeem():
    data = request.get_json(force=True)
    code = (data.get("code") or "").strip().upper()
    if not code: return jsonify(ok=False, error="Kein Code eingegeben.")
    if code in USED: return jsonify(ok=False, error="Code bereits benutzt.")
    if code not in CODES: return jsonify(ok=False, error="Ungültiger Code.")
    USED.add(code)
    balance = add_balance(CODES[code])
    return jsonify(ok=True, amount=CODES[code], balance=balance)

@app.route("/api/bet-check", methods=["POST"])
def api_bet_check():
    bet = int(request.get_json(force=True).get("bet",0))
    if bet < 1: return jsonify(ok=False, error="Einsatz zu klein.")
    if get_balance() < bet: return jsonify(ok=False, error="Nicht genug Guthaben.")
    return jsonify(ok=True)

@app.route("/api/bet-result", methods=["POST"])
def api_bet_result():
    data = request.get_json(force=True)
    bet = int(data.get("bet",0)); win = bool(data.get("win"))
    bal = get_balance()
    if win: bal += bet
    else:   bal = max(0, bal - bet)
    set_balance(bal)
    return jsonify(ok=True, balance=bal)

@app.route("/api/roulette-result", methods=["POST"])
def api_rl_result():
    data = request.get_json(force=True)
    bet = int(data.get("bet",0)); win = bool(data.get("win")); win_amount = int(data.get("winAmount",0))
    bal = get_balance()
    if win: bal += win_amount
    else:   bal = max(0, bal - bet)
    set_balance(bal)
    return jsonify(ok=True, balance=bal)

if __name__ == "__main__":
    app.run(debug=True)
