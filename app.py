from flask import Flask, request, session, jsonify, render_template_string
import random, math, time

app = Flask(__name__)
app.secret_key = "replace-this-with-any-secret-32bytes"

# ------------------------------
# Helper: Session Guthaben
# ------------------------------
def get_balance():
    if "balance" not in session:
        session["balance"] = 100  # Startguthaben
    return session["balance"]

def add_balance(amount):
    bal = get_balance()
    bal += int(amount)
    session["balance"] = bal
    return bal

# ------------------------------
# Gutscheincodes
# ------------------------------
CODES = {
    "LEON": 100,
    "ARMIN": 101,
    # 3x 200
    "EAGLE": 200, "RIVER": 200, "COMET": 200,
    # 2x 75
    "MANGO": 75, "DRAGON": 75,
    # 2x 50
    "PINE": 50, "WOLF": 50,
    # 1x 1000
    "JACKPOT": 1000,
}

USED = set()

# ------------------------------
# Lustige Funfacts
# ------------------------------
FUNNY_FACTS = [
    "Ein Seeigel hat kein Gehirn – und trotzdem bessere Wochenpläne als ich.",
    "Der Eiffelturm wird im Sommer bis zu 15 cm größer. Meiner Motivation passiert das nie.",
    "Katzen können über 100 Laute machen. Menschen nur einen: 'Miau, sofort aufstehen!'",
    "Im Weltall riecht es nach verbranntem Steak. Perfekter Ort für Vegetarier?",
    "Honig verdirbt nie. Wenn du ihn findest: Er gehört vermutlich Mumien.",
    "Schafe können Gesichter erkennen. Trotzdem ignorieren sie deine DMs.",
    "Hummeln können fliegen, obwohl die Aerodynamik dagegen spricht. Einfach machen!",
    "Enten quaken ohne Echo. Das behaupten Enten zumindest.",
    "Goldfische haben ein gutes Gedächtnis. Die Ausrede ist also geplatzt.",
    "Faultiere brauchen eine Woche für die Verdauung. Kein Kommentar.",
]

# ------------------------------
# HTML
# ------------------------------
HTML = r"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>aaron-sigma</title>
<style>
  :root{
    --bg:#0f172a;
    --card:#111827;
    --muted:#9ca3af;
    --accent:#2563eb;
    --good:#22c55e;
    --bad:#ef4444;
    --text:#e5e7eb;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial,sans-serif}
  a{color:inherit;text-decoration:none}
  .wrap{max-width:980px;margin:0 auto;padding:16px}
  .nav{display:flex;align-items:center;justify-content:space-between;padding:10px 0}
  .brand{font-weight:800;font-size:22px;letter-spacing:.3px}
  .dd{position:relative}
  .btn{background:var(--accent);color:#fff;border:0;border-radius:12px;padding:10px 16px;cursor:pointer}
  .btn.secondary{background:#1f2937;color:#fff}
  .btn.ghost{background:#111827;color:#e5e7eb}
  .dd-btn{background:#1f2937;border:0;border-radius:12px;padding:10px 16px;color:#e5e7eb;cursor:pointer}
  .dd-menu{position:absolute;right:0;top:44px;background:#0b1220;border:1px solid #1f2937;border-radius:12px;min-width:200px;display:none}
  .dd-menu a{display:block;padding:10px 14px;border-bottom:1px solid #111827}
  .dd-menu a:last-child{border-bottom:0}
  .dd:hover .dd-menu{display:block}
  .card{background:var(--card);border:1px solid #1f2937;border-radius:16px;padding:16px}
  .muted{color:var(--muted)}
  .row{display:flex;gap:16px;flex-wrap:wrap}
  .col{flex:1 1 300px}
  h1,h2,h3{margin:6px 0 14px}
  .hr{height:1px;background:#1f2937;margin:18px 0}
  .pill{display:inline-block;background:#0b1220;border:1px solid #1f2937;border-radius:999px;padding:6px 12px;color:#cbd5e1}
  .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
  input,select{background:#0b1220;border:1px solid #1f2937;border-radius:10px;color:#e5e7eb;padding:10px 12px}
  .msg{margin-top:10px;font-weight:600}
  /* clock */
  .clock{font-size:48px;font-weight:800;line-height:1.1;
         background:linear-gradient(90deg,#22c55e,#06b6d4,#2563eb,#a855f7,#f59e0b);
         -webkit-background-clip:text;background-clip:text;color:transparent;
         animation:hue 6s linear infinite;}
  @keyframes hue{0%{filter:hue-rotate(0deg)}100%{filter:hue-rotate(360deg)}}
  .clock-date{font-size:18px;color:#94a3b8}
  /* tabs */
  .tabs{display:flex;gap:8px;margin-bottom:12px}
  .tab{padding:10px 14px;border-radius:10px;background:#0b1220;border:1px solid #1f2937;color:#cbd5e1;cursor:pointer}
  .tab.active{background:var(--accent);color:#fff;border-color:transparent}
  .tab-panel{display:none}
  .tab-panel.active{display:block}
  /* cards visuals */
  .cards{display:flex;gap:10px}
  .card-face{width:118px;height:160px;border-radius:14px;border:1px dashed #2a3344;background:
     repeating-linear-gradient(45deg,#0b1220,#0b1220 6px,#12192a 6px,#12192a 12px);
     display:flex;align-items:center;justify-content:center;font-size:40px}
  .card-num{font-size:34px}
  .red{color:#ef4444}
  .green{color:#22c55e}
  /* roulette */
  .roulette-wrap{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
  .wheel-wrap{position:relative;width:380px;height:380px}
  .wheel{position:absolute;inset:0;border-radius:50%;background:#0b1220;border:10px solid #0b1220;
          display:flex;align-items:center;justify-content:center;overflow:hidden}
  .wheel-disc{position:absolute;width:340px;height:340px;border-radius:50%;background:#111827}
  .nums{position:absolute;inset:0;display:grid;place-items:center}
  .pointer{position:absolute;left:50%;top:-6px;transform:translateX(-50%);
           width:0;height:0;border-left:12px solid transparent;border-right:12px solid transparent;
           border-bottom:20px solid #fbbf24;z-index:10}
  .ball{position:absolute;left:50%;top:50%;width:18px;height:18px;border-radius:50%;
        background:white;box-shadow:0 0 8px rgba(255,255,255,.6);z-index:8;
        transform:translate(-50%,-50%) rotate(0deg) translate(145px);}
  .sector{position:absolute;width:340px;height:340px;border-radius:50%}
  .sec-label{position:absolute;left:50%;top:50%;transform-origin:0 -150px;
             color:#e5e7eb;font-size:12px;font-weight:700;
             text-shadow:0 1px 2px rgba(0,0,0,.7)}
  .r-red{background:conic-gradient(#111827 0 50%,#7f1d1d 50% 100%)}
  .r-black{background:conic-gradient(#111827 0 50%,#0b1220 50% 100%)}
  .r-green{background:conic-gradient(#111827 0 50%,#065f46 50% 100%)}
  .res{font-size:18px;margin-top:10px}
</style>
</head>
<body>
  <div class="wrap">
    <div class="nav">
      <div class="brand">aaron-sigma.de</div>
      <div class="dd">
        <button class="dd-btn">Bereiche ▾</button>
        <div class="dd-menu">
          <a href="#home">Start</a>
          <a href="#fun">Funfacts</a>
          <a href="#casino">Casino</a>
        </div>
      </div>
    </div>

    <!-- HOME -->
    <section id="home" class="card">
      <h2>Willkommen!</h2>
      <div class="row">
        <div class="col">
          <div class="clock" id="clock">--:--:--</div>
          <div class="clock-date" id="clock-date">--.--.----</div>
        </div>
        <div class="col">
          <p class="muted">Hier bauen wir Aarons Universum: Uhrzeit, Spiele, Casino und Aaron Dollar.</p>
          <p class="muted">Guthaben und Fortschritt bleiben im Browser erhalten.</p>
        </div>
      </div>
    </section>

    <div class="hr"></div>

    <!-- FUN -->
    <section id="fun" class="card">
      <h2>😂 Funfacts</h2>
      <div class="row">
        <div class="col">
          <div id="fact" class="pill" style="display:block;margin-bottom:10px"></div>
          <button class="btn" id="btn-fact">Neuen Funfact</button>
        </div>
      </div>
    </section>

    <div class="hr"></div>

    <!-- CASINO -->
    <section id="casino" class="card">
      <h2>🎰 Casino</h2>

      <div class="card" style="margin-bottom:14px">
        <div><b>Guthaben:</b> <span id="balance">0</span> A$</div>
        <div class="row" style="margin-top:10px">
          <div class="col"><input id="code" placeholder="Gutschein-Code"></div>
          <div class="col" style="flex:0 0 auto"><button class="btn" id="btn-redeem">Einlösen</button></div>
        </div>
        <div id="redeem-msg" class="msg"></div>
      </div>

      <div class="tabs">
        <button class="tab active" data-tab="bj">Blackjack</button>
        <button class="tab" data-tab="rl">Roulette</button>
      </div>

      <!-- BLACKJACK -->
      <div class="tab-panel active" id="panel-bj">
        <div class="row">
          <div class="col" style="flex:0 0 220px">
            <label>Einsatz:</label>
            <input type="number" id="bj-bet" value="10" min="1" step="1" style="width:120px"> A$
          </div>
        </div>
        <div class="row">
          <button class="btn" id="bj-new">Neue Runde</button>
          <button class="btn secondary" id="bj-hit">Hit</button>
          <button class="btn ghost" id="bj-stand">Stand</button>
        </div>

        <div class="row" style="margin-top:14px">
          <div class="col">
            <h3>Dealer</h3>
            <div class="cards" id="bj-dealer"></div>
            <div id="bj-dealer-score" class="muted">–</div>
          </div>
          <div class="col">
            <h3>Spieler</h3>
            <div class="cards" id="bj-player"></div>
            <div id="bj-player-score" class="muted">–</div>
          </div>
        </div>

        <div id="bj-msg" class="msg"></div>
      </div>

      <!-- ROULETTE -->
      <div class="tab-panel" id="panel-rl">
        <div class="row" style="gap:16px">
          <div class="col" style="flex:0 0 220px">
            <label>Einsatz:</label>
            <input id="rl-bet" type="number" min="1" step="1" value="10" style="width:120px"> A$
          </div>
        </div>

        <div class="row" style="gap:10px">
          <div class="col" style="flex:0 0 220px">
            <label>Wette:</label>
            <select id="rl-type" style="width:220px">
              <option value="single">Zahl (0–36)</option>
              <option value="red">Rot</option>
              <option value="black">Schwarz</option>
              <option value="even">Gerade</option>
              <option value="odd">Ungerade</option>
              <option value="dozen1">1st 12 (1–12)</option>
              <option value="dozen2">2nd 12 (13–24)</option>
              <option value="dozen3">3rd 12 (25–36)</option>
              <option value="col1">Spalte 1 (1/4/7/...)</option>
              <option value="col2">Spalte 2 (2/5/8/...)</option>
              <option value="col3">Spalte 3 (3/6/9/...)</option>
            </select>
          </div>
          <div class="col" id="rl-number-wrap" style="flex:0 0 220px">
            <label>Zahl:</label>
            <input id="rl-number" type="number" min="0" max="36" value="7" style="width:120px">
          </div>
        </div>

        <div class="row" style="margin-top:12px">
          <button id="rl-spin" class="btn">Spin</button>
        </div>

        <div class="roulette-wrap" style="margin-top:12px">
          <div class="wheel-wrap">
            <div class="pointer"></div>
            <div class="ball" id="rl-ball"></div>
            <div class="wheel" id="rl-wheel">
              <div class="wheel-disc" id="rl-disc"></div>
              <div class="nums" id="rl-nums"></div>
            </div>
          </div>
          <div class="col">
            <div id="rl-result" class="res">Ergebnis: –</div>
            <div id="rl-msg" class="msg"></div>
          </div>
        </div>
      </div>
    </section>

    <div style="text-align:center;margin:30px 0" class="muted">Made by Aaron ✨</div>
  </div>

<script>
/* -------- clock -------- */
function pad(n){return n<10?("0"+n):n}
function tick(){
  const d=new Date();
  document.getElementById("clock").textContent =
    pad(d.getHours())+":"+pad(d.getMinutes())+":"+pad(d.getSeconds());
  document.getElementById("clock-date").textContent =
    pad(d.getDate())+"."+pad(d.getMonth()+1)+"."+d.getFullYear();
}
setInterval(tick,1000); tick();

/* -------- tabs -------- */
document.querySelectorAll(".tab").forEach(btn=>{
  btn.addEventListener("click",()=>{
    document.querySelectorAll(".tab").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    const id=btn.dataset.tab==="bj"?"panel-bj":"panel-rl";
    document.querySelectorAll(".tab-panel").forEach(p=>p.classList.remove("active"));
    document.getElementById(id).classList.add("active");
  });
});

/* -------- funfacts -------- */
const FUNNY = {{ facts|tojson }};
function newFact(){
  const f=FUNNY[Math.floor(Math.random()*FUNNY.length)];
  document.getElementById("fact").textContent=f;
}
document.getElementById("btn-fact").addEventListener("click",newFact);
newFact();

/* -------- balance + redeem -------- */
function refreshBalance(v){document.getElementById("balance").textContent=v}
fetch("/api/balance").then(r=>r.json()).then(j=>refreshBalance(j.balance));

document.getElementById("btn-redeem").addEventListener("click",()=>{
  const code=document.getElementById("code").value.trim();
  fetch("/api/redeem",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code})})
    .then(r=>r.json()).then(j=>{
      const m=document.getElementById("redeem-msg");
      if(j.ok){m.style.color="#22c55e";refreshBalance(j.balance);m.textContent="+"+j.amount+" A$ gutgeschrieben";}
      else{m.style.color="#ef4444";m.textContent=j.error||"Ungültig";}
    });
});

/* -------- blackjack -------- */
const SUITS=["♠","♥","♦","♣"];
function newDeck(){
  const d=[];
  for(let s of SUITS){
    for(let v=1;v<=13;v++){d.push({s:s,v:v})}
  }
  for(let i=d.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));[d[i],d[j]]=[d[j],d[i]];
  }
  return d;
}
function cardVal(c){ if(c.v>=10) return 10; if(c.v===1) return 11; return c.v; }
function score(hand){
  let t=0, aces=0;
  for(let c of hand){ t+=cardVal(c); if(c.v===1) aces++; }
  while(t>21 && aces>0){ t-=10; aces--; }
  return t;
}
function renderHand(el,hand,hideSecond=false){
  el.innerHTML="";
  hand.forEach((c,idx)=>{
    const div=document.createElement("div");
    div.className="card-face";
    if(hideSecond && idx===1){
      div.innerHTML="";
    }else{
      const txt=(c.v===1?"A":c.v===11?"J":c.v===12?"Q":c.v===13?"K":c.v);
      const red=(c.s==="♥"||c.s==="♦");
      div.innerHTML = `<div class="card-num ${red?'red':''}">${txt}${red?'<span class="red"> '+c.s+'</span>':' '+c.s}</div>`;
    }
    el.appendChild(div);
  });
}
let bjDeck=[], bjDealer=[], bjPlayer=[], bjOver=false, bjHide=true;

function bjNew(){
  const bet=parseInt(document.getElementById("bj-bet").value||"0",10);
  if(bet<1){document.getElementById("bj-msg").style.color="#ef4444";document.getElementById("bj-msg").textContent="Einsatz zu klein.";return;}
  fetch("/api/bet-check",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({bet})})
   .then(r=>r.json()).then(j=>{
     if(!j.ok){document.getElementById("bj-msg").style.color="#ef4444";document.getElementById("bj-msg").textContent=j.error;return;}
     bjDeck=newDeck(); bjDealer=[bjDeck.pop(), bjDeck.pop()]; bjPlayer=[bjDeck.pop(), bjDeck.pop()]; bjOver=false; bjHide=true;
     renderHand(document.getElementById("bj-dealer"), bjDealer, true);
     renderHand(document.getElementById("bj-player"), bjPlayer, false);
     document.getElementById("bj-dealer-score").textContent="–";
     document.getElementById("bj-player-score").textContent=score(bjPlayer);
     document.getElementById("bj-msg").textContent="";
   });
}
function bjHit(){
  if(bjOver) return;
  bjPlayer.push(bjDeck.pop());
  renderHand(document.getElementById("bj-player"), bjPlayer, false);
  const s=score(bjPlayer);
  document.getElementById("bj-player-score").textContent=s;
  if(s>21){ bjOver=true; bjHide=false; endBj("Bust! Dealer gewinnt.", false); }
}
function endBj(text, playerWin){
  renderHand(document.getElementById("bj-dealer"), bjDealer, false);
  document.getElementById("bj-dealer-score").textContent=score(bjDealer);
  document.getElementById("bj-msg").style.color = playerWin ? "#22c55e" : "#ef4444";
  document.getElementById("bj-msg").textContent=text;
  const bet=parseInt(document.getElementById("bj-bet").value||"0",10);
  fetch("/api/bet-result",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({bet,win:playerWin})})
   .then(r=>r.json()).then(j=>{ if(j.ok) refreshBalance(j.balance); });
}
function bjStand(){
  if(bjOver) return;
  bjHide=false;
  while(score(bjDealer)<17){ bjDealer.push(bjDeck.pop()); }
  const ps=score(bjPlayer), ds=score(bjDealer);
  if(ds>21){ bjOver=true; endBj("Dealer bust! Du gewinnst.", true); return; }
  if(ps>ds){ bjOver=true; endBj("Du gewinnst.", true); }
  else if(ps<ds){ bjOver=true; endBj("Dealer gewinnt.", false); }
  else{ // push -> bet zurück
    bjOver=true; renderHand(document.getElementById("bj-dealer"), bjDealer, false);
    document.getElementById("bj-dealer-score").textContent=ds;
    document.getElementById("bj-msg").style.color="#f59e0b";
    document.getElementById("bj-msg").textContent="Unentschieden. Einsatz zurück.";
  }
}
document.getElementById("bj-new").addEventListener("click",bjNew);
document.getElementById("bj-hit").addEventListener("click",bjHit);
document.getElementById("bj-stand").addEventListener("click",bjStand);

/* -------- roulette -------- */
// echte EU-Reihenfolge (0-einarmig)
const RL_ORDER = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26];
const sector = 360/37;
let currentRot = 0;   // Grad accumuliert
let ballRot = 0;

function buildWheel(){
  const nums=document.getElementById("rl-nums");
  nums.innerHTML="";
  RL_ORDER.forEach((n,i)=>{
    const ang=i*sector;
    const lbl=document.createElement("div");
    lbl.className="sec-label";
    lbl.style.transform=`translate(-50%,-50%) rotate(${ang}deg) translate(0,-150px) rotate(${-ang}deg)`;
    lbl.textContent=n;
    nums.appendChild(lbl);
  });
}
buildWheel();

function showNumberFieldInput(){
  const type=document.getElementById("rl-type").value;
  document.getElementById("rl-number-wrap").style.display = (type==="single") ? "block" : "none";
}
document.getElementById("rl-type").addEventListener("change",showNumberFieldInput);
showNumberFieldInput();

function spin(){
  const bet=parseInt(document.getElementById("rl-bet").value||"0",10);
  if(bet<1){msg("rl","Einsatz zu klein",false);return;}
  fetch("/api/bet-check",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({bet})})
   .then(r=>r.json()).then(j=>{
     if(!j.ok){msg("rl",j.error,false);return;}
     doSpin(bet);
   });
}
document.getElementById("rl-spin").addEventListener("click",spin);

function msg(prefix,text,ok){
  const el=document.getElementById(prefix+"-msg");
  el.style.color = ok ? "#22c55e" : "#ef4444";
  el.textContent=text;
}
function setResult(num,color){
  document.getElementById("rl-result").textContent = "Ergebnis: Zahl "+num+", Farbe "+color;
}
function payout(type, choice, result, bet){
  // returns win amount (0 if lost). Odd/Even etc -> 2x, dozens/columns 3x, single 35x.
  const redSet = new Set([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]);
  const blackSet = new Set([2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]);
  if(type==="single"){
    return (result===choice) ? bet*35 : 0;
  }else if(type==="red"){ return redSet.has(result)? bet*2:0; }
  else if(type==="black"){ return blackSet.has(result)? bet*2:0; }
  else if(type==="even"){ return (result!==0 && result%2===0)? bet*2:0; }
  else if(type==="odd"){ return (result%2===1)? bet*2:0; }
  else if(type==="dozen1"){ return (result>=1 && result<=12)? bet*3:0; }
  else if(type==="dozen2"){ return (result>=13 && result<=24)? bet*3:0; }
  else if(type==="dozen3"){ return (result>=25 && result<=36)? bet*3:0; }
  else if(type==="col1"){ return ([1,4,7,10,13,16,19,22,25,28,31,34].includes(result))? bet*3:0; }
  else if(type==="col2"){ return ([2,5,8,11,14,17,20,23,26,29,32,35].includes(result))? bet*3:0; }
  else if(type==="col3"){ return ([3,6,9,12,15,18,21,24,27,30,33,36].includes(result))? bet*3:0; }
  return 0;
}
function doSpin(bet){
  const type=document.getElementById("rl-type").value;
  const numChoice=parseInt(document.getElementById("rl-number").value||"0",10);
  const resultIdx = Math.floor(Math.random()*37);
  const resultNum = RL_ORDER[resultIdx];
  const color = (resultNum===0) ? "grün" : ([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(resultNum) ? "rot" : "schwarz");
  setResult(resultNum, color);

  // Zielwinkel: Index-Sektor unter Zeiger (oben = 0deg)
  const targetAngle = 360 - (resultIdx*sector) - sector/2;
  // viele volle Umdrehungen + Ziel
  const wheel = document.getElementById("rl-wheel");
  const ball = document.getElementById("rl-ball");
  const spins = 5; // volle
  const target = currentRot + spins*360 + targetAngle;
  const ballTarget = ballRot + spins*360 + targetAngle + 720; // ball rotiert zusätzlich

  wheel.style.transition = "transform 3.6s cubic-bezier(.2,.9,.2,1)";
  ball.style.transition = "transform 3.6s cubic-bezier(.2,.9,.2,1)";
  requestAnimationFrame(()=>{
    wheel.style.transform = `rotate(${target}deg)`;
    ball.style.transform  = `translate(-50%,-50%) rotate(${ballTarget}deg) translate(145px)`;
  });

  setTimeout(()=>{
    currentRot = target%360;
    ballRot = ballTarget%360;
    const win = payout(type, numChoice, resultNum, bet);
    const won = win>0;
    fetch("/api/roulette-result",{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({bet,win:won,winAmount:win})})
      .then(r=>r.json()).then(j=>{
        if(j.ok){
          refreshBalance(j.balance);
          msg("rl", won? ("Gewonnen: +"+win+" A$") : ("Verloren: -"+bet+" A$"), won);
        } else {
          msg("rl", j.error||"Fehler", false);
        }
      });
  }, 3700);
}
</script>
</body>
</html>
"""

# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def home():
    return render_template_string(HTML, facts=FUNNY_FACTS)

@app.route("/api/balance")
def api_balance():
    return jsonify(ok=True, balance=get_balance())

@app.route("/api/redeem", methods=["POST"])
def api_redeem():
    data = request.get_json(force=True)
    code = (data.get("code") or "").strip().upper()
    if not code:
        return jsonify(ok=False, error="Kein Code eingegeben.")
    if code in USED:
        return jsonify(ok=False, error="Dieser Code wurde schon benutzt.")
    if code not in CODES:
        return jsonify(ok=False, error="Ungültiger Code.")
    amount = CODES[code]
    USED.add(code)
    balance = add_balance(amount)
    return jsonify(ok=True, amount=amount, balance=balance)

@app.route("/api/bet-check", methods=["POST"])
def api_bet_check():
    data = request.get_json(force=True)
    bet = int(data.get("bet", 0))
    if bet < 1:
        return jsonify(ok=False, error="Einsatz zu klein.")
    if get_balance() < bet:
        return jsonify(ok=False, error="Nicht genug Guthaben.")
    # Reservieren wir logik-seitig nichts – nur Check.
    return jsonify(ok=True)

@app.route("/api/bet-result", methods=["POST"])
def api_bet_result():
    data = request.get_json(force=True)
    bet = int(data.get("bet", 0))
    win = bool(data.get("win"))
    bal = get_balance()
    if bet < 1:
        return jsonify(ok=False, error="Ungültiger Einsatz")
    # Bei Blackjack: gewinnen +bet, verlieren -bet, push handled client-seitig ohne call
    if win:
        bal += bet
    else:
        if bal < bet:
            bet = bal
        bal -= bet
    session["balance"] = bal
    return jsonify(ok=True, balance=bal)

@app.route("/api/roulette-result", methods=["POST"])
def api_roulette_result():
    data = request.get_json(force=True)
    bet = int(data.get("bet", 0))
    win = bool(data.get("win"))
    win_amount = int(data.get("winAmount", 0))
    bal = get_balance()
    if bet < 1:
        return jsonify(ok=False, error="Ungültiger Einsatz")
    if win:
        bal += win_amount
    else:
        if bal < bet:
            bet = bal
        bal -= bet
    session["balance"] = bal
    return jsonify(ok=True, balance=bal)

if __name__ == "__main__":
    app.run(debug=True)
