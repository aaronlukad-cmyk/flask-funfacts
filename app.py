from flask import Flask, jsonify, render_template_string, request, url_for
import random
import datetime

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────────────
#  EINLÖSECODES (einmalig, serverseitig – volatile; nach Neustart wieder da)
#  Du kannst hier beliebig Codes + Beträge eintragen. Jeder Code ist 1× einlösbar.
VALID_CODES = {
    "WELCOME50": 50,
    "AARON100": 100,
    "VIP500": 500,
}
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
#  IDEEN-FORMULAR (kein Setup): FormSubmit leitet an deine Mail weiter
FORMSUBMIT_URL = "https://formsubmit.co/info@aaron-sigma.de"
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
#  FUN FACTS
FACTS = {
    "lustig": [
        "Kühe haben beste Freunde und werden gestresst, wenn man sie trennt. 🐮❤️",
        "Ein Straußenei braucht rund 40 Minuten, um weich zu kochen. 🥚",
        "Honig verdirbt nie — man fand essbaren Honig in Pyramiden. 🍯",
        "Koalas schlafen bis zu 22 Stunden am Tag. 😴🐨",
    ],
    "tiere": [
        "Oktopusse haben drei Herzen. 🐙",
        "Schmetterlinge schmecken mit ihren Füßen. 🦋",
        "Raben erkennen Gesichter und merken sie sich. 🐦",
        "Pinguine machen Heiratsanträge mit einem Kieselstein. 🐧💎",
    ],
    "wissen": [
        "Die erste Website ging 1991 online. 🌐",
        "Der Eiffelturm wird im Sommer bis zu 15 cm höher. 🗼",
        "Banane ist eine Beere, die Erdbeere nicht. 🍓🍌",
        "Wasser dehnt sich beim Gefrieren aus. ❄️",
    ],
}
ALL_FACTS = sum(FACTS.values(), [])
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
#  LAYOUT (Top-Navigation + Styles + Dropdown)
LAYOUT = r"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{{ title }}</title>
<style>
  :root{
    --bg:#0b0f14; --card:#121824; --muted:#9fb0c3; --text:#e8f1fb;
    --primary:#4aa3ff; --accent:#22c55e; --danger:#ef4444; --yellow:#facc15; --border:#1c2433;
  }
  *{box-sizing:border-box}
  body{ margin:0; font-family:system-ui, Inter, Segoe UI, Roboto, Arial, sans-serif;
        background:linear-gradient(180deg,#0b0f14 0%, #0d141f 100%); color:var(--text); }
  header{ position:sticky; top:0; z-index:10; background:#0c131e; border-bottom:1px solid var(--border); }
  .nav{ max-width:1100px; margin:0 auto; padding:12px 16px; display:flex; gap:12px; align-items:center; }
  .brand{ font-weight:900; letter-spacing:.3px; }
  .spacer{ flex:1 }
  a.navlink{ color:#cfe3ff; text-decoration:none; padding:8px 12px; border-radius:10px; }
  a.navlink:hover{ background:#101a2a; }
  select.navsel{
    background:#0e1420; color:#e8f1fb; border:1px solid var(--border); border-radius:10px; padding:8px 10px;
  }
  .wrap{ max-width:1100px; margin:24px auto; padding:0 16px; }
  .card{ background:var(--card); border:1px solid var(--border); border-radius:16px; padding:18px; box-shadow:0 10px 28px rgba(0,0,0,.35); }
  .muted{ color:var(--muted); }
  .btn{ background:var(--primary); color:#021021; border:0; border-radius:12px; padding:10px 14px; font-weight:700; cursor:pointer; }
  .btn.sec{ background:#182335; color:#e8f1fb }
  .btn.danger{ background:#b91c1c; color:#fff }
  .row{ display:flex; gap:12px; align-items:center; flex-wrap:wrap }
  input,select,textarea{
    background:#0e1420; color:#e8f1fb; border:1px solid var(--border); border-radius:10px; padding:10px 12px;
  }
  .grid{ display:grid; gap:16px; grid-template-columns:repeat(12, 1fr); }
  .col-12{ grid-column: span 12; } .col-6{ grid-column: span 6; }
  @media (max-width: 900px){ .col-6{ grid-column: span 12; } }
  .clock{ font-variant-numeric:tabular-nums; font-size: clamp(36px, 6vw, 66px); font-weight:900; text-align:center }
  .date{ text-align:center; color:var(--muted); margin-top:6px }
  .fact{ font-size:20px; line-height:1.5 }
  /* TicTacToe */
  .ttt{ display:grid; grid-template-columns:repeat(3, 96px); gap:10px; justify-content:center }
  .ttt button{ width:96px; height:96px; font-size:42px; font-weight:900; background:#0e1420; border:1px solid var(--border); border-radius:12px; color:#e8f1fb; cursor:pointer; }
  .ttt .win{ background:#0f2a18; border-color:#1d6c3a; }
  /* Casino */
  .bank{ font-weight:900; font-size:20px }
  .hand{ display:flex; gap:8px; flex-wrap:wrap }
  .chip{ background:#0e1420; border:1px solid var(--border); border-radius:10px; padding:8px 10px; }
  .tag{ background:#0e1420; border:1px solid var(--border); border-radius:8px; padding:6px 8px; min-width:36px; text-align:center; }
  .hint{ color:#93c5fd; }
  .tabs{ display:flex; gap:8px; margin-bottom:10px }
  .tab{ padding:8px 12px; border-radius:10px; border:1px solid var(--border); background:#0f1624; cursor:pointer }
  .tab.active{ background:#152035; }
</style>
</head>
<body>
<header>
  <nav class="nav">
    <div class="brand">aaron-sigma.de</div>
    <a href="{{ url_for('home') }}" class="navlink">Start</a>
    <a href="{{ url_for('page_fun') }}" class="navlink">Fun Facts</a>
    <a href="{{ url_for('page_ttt') }}" class="navlink">Tic-Tac-Toe</a>
    <a href="{{ url_for('page_casino') }}" class="navlink">Casino</a>
    <div class="spacer"></div>
    <select class="navsel" id="navsel">
      <option value="{{ url_for('home') }}">Start</option>
      <option value="{{ url_for('page_fun') }}">Fun Facts</option>
      <option value="{{ url_for('page_ttt') }}">Tic-Tac-Toe</option>
      <option value="{{ url_for('page_casino') }}">Casino</option>
    </select>
  </nav>
</header>

<div class="wrap">
  {{ body|safe }}
</div>

<script>
  document.getElementById('navsel').addEventListener('change', e => { window.location.href = e.target.value; });
</script>

{{ extra|safe }}

</body>
</html>
"""

def render_page(title, body_html, extra_script=""):
    return render_template_string(LAYOUT, title=title, body=body_html, extra=extra_script)

# ─────────────────────────────────────────────────────────────────────────────
#  STARTSEITE
@app.route("/")
def home():
    body = f"""
      <div class='grid'>
        <section class='col-6 card'>
          <h2>Willkommen 👋</h2>
          <p class='muted'>Wähle oben im Menü: <b>Fun Facts</b>, <b>Tic-Tac-Toe</b> oder <b>Casino</b>.</p>
          <p>Hier bauen wir dein kleines Universum: Uhrzeit, Spiele & Aaron Dollar 🪙</p>
        </section>

        <section class='col-6 card'>
          <h2>⏰ Uhr & Datum</h2>
          <div class='clock' id='clk'>--:--:--</div>
          <div class='date' id='dat'>--.--.----</div>
        </section>

        <section class='col-12 card'>
          <h2>💡 Ideen einsenden</h2>
          <form action="{FORMSUBMIT_URL}" method="POST" class="row" style="align-items:flex-start">
            <input type="hidden" name="_subject" value="Neue Idee von aaron-sigma.de">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_template" value="box">
            <input type="hidden" name="_next" value="https://aaron-sigma.de/?thanks=1">
            <input type="text" name="name" placeholder="Dein Name" required style="flex:1;min-width:160px">
            <input type="text" name="message" placeholder="Deine Idee..." required style="flex:3;min-width:220px">
            <button class="btn" type="submit">✉️ Absenden</button>
          </form>
          <p class='muted' style='margin-top:6px'>Beim allerersten Eintrag bitte die Bestätigungs-Mail von FormSubmit bestätigen.</p>
        </section>
      </div>
    """
    extra = """
    <script>
      function two(n){return String(n).padStart(2,'0')}
      function tick(){
        const d=new Date();
        document.getElementById('clk').textContent = `${two(d.getHours())}:${two(d.getMinutes())}:${two(d.getSeconds())}`;
        document.getElementById('dat').textContent = `${two(d.getDate())}.${two(d.getMonth()+1)}.${d.getFullYear()}`;
      }
      setInterval(tick,1000); tick();
    </script>
    """
    return render_page("Start · aaron-sigma.de", body, extra)

# ─────────────────────────────────────────────────────────────────────────────
#  FUN FACTS
@app.route("/fun")
def page_fun():
    body = """
    <section class="card">
      <h2>✨ Fun Facts</h2>
      <div class="row" style="margin:10px 0">
        <label>Kategorie:
          <select id="cat" style="margin-left:8px">
            <option value="random">Zufällig</option>
            <option value="lustig">Lustig</option>
            <option value="tiere">Tiere</option>
            <option value="wissen">Wissen</option>
          </select>
        </label>
        <button id="btn" class="btn">🎲 Neuen Fakt</button>
        <button id="copy" class="btn sec">📋 Kopieren</button>
        <button id="fav" class="btn sec">⭐ Favorit</button>
      </div>
      <div id="fact" class="fact card" style="padding:14px">Klick auf „Neuen Fakt“ 🙂</div>

      <h3 style="margin-top:18px">⭐ Favoriten</h3>
      <div class="row" style="margin:6px 0">
        <button id="clear" class="btn sec">🗑️ Leeren</button>
      </div>
      <div id="favs" class="grid" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))"></div>
    </section>
    """
    extra = """
    <script>
      const favKey='aaron_favs';
      function getFavs(){try{return JSON.parse(localStorage.getItem(favKey)||'[]')}catch(e){return[]}}
      function setFavs(a){localStorage.setItem(favKey,JSON.stringify(a.slice(0,50)))}
      function renderFavs(){
        const box=document.getElementById('favs'); box.innerHTML='';
        getFavs().forEach(f=>{ const d=document.createElement('div'); d.className='card'; d.textContent=f; box.appendChild(d); });
      }
      async function loadFact(){
        const cat=document.getElementById('cat').value;
        const url=cat==='random'?'/api/fact':`/api/fact?cat=${encodeURIComponent(cat)}`;
        const r=await fetch(url); const j=await r.json();
        document.getElementById('fact').textContent=j.fact;
      }
      document.getElementById('btn').onclick=loadFact;
      document.getElementById('cat').onchange=loadFact;
      document.getElementById('copy').onclick=async()=>{try{await navigator.clipboard.writeText(document.getElementById('fact').textContent)}catch(e){}};
      document.getElementById('fav').onclick=()=>{ const t=document.getElementById('fact').textContent.trim(); if(!t) return; const a=getFavs(); if(!a.includes(t)){a.unshift(t); setFavs(a); renderFavs();} }
      document.getElementById('clear').onclick=()=>{localStorage.removeItem(favKey); renderFavs();}
      renderFavs(); loadFact();
    </script>
    """
    return render_page("Fun Facts · aaron-sigma.de", body, extra)

@app.get("/api/fact")
def api_fact():
    cat = (request.args.get("cat") or "random").lower()
    if cat == "random" or cat not in FACTS:
        fact = random.choice(ALL_FACTS)
    else:
        fact = random.choice(FACTS[cat])
    return jsonify({"fact": fact})

# ─────────────────────────────────────────────────────────────────────────────
#  TIC-TAC-TOE
@app.route("/tictactoe")
def page_ttt():
    body = """
    <section class="card">
      <h2>🎮 Tic-Tac-Toe</h2>
      <div class="muted" id="ttt-status">Du bist X. Computer ist O.</div>
      <div class="ttt" id="ttt"></div>
      <div class="row" style="margin-top:10px">
        <button class="btn" id="ttt-reset">Neu starten</button>
      </div>
    </section>
    """
    extra = """
    <script>
      // Starker Bot (Minimax)
      const ttt = document.getElementById('ttt');
      let board = Array(9).fill('');
      const HUMAN = 'X', AI = 'O';
      const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
      let lock = false;

      function draw(){
        ttt.innerHTML='';
        board.forEach((val,i)=>{
          const b = document.createElement('button');
          b.textContent = val;
          b.addEventListener('click', ()=>humanMove(i));
          ttt.appendChild(b);
        });
      }
      function emptyIdx(b){ return b.map((v,i)=>v===''?i:null).filter(i=>i!==null); }
      function winnerOf(b){ for(const [a,b2,c] of wins){ if(b[a] && b[a]===b[b2] && b[b2]===b[c]) return b[a]; } return null; }
      function winLine(b){ for(const L of wins){ const [a,b2,c]=L; if(b[a] && b[a]===b[b2] && b[b2]===b[c]) return L; } return null; }
      function endGame(res){
        lock = true;
        if(res==='draw'){ document.getElementById('ttt-status').textContent = 'Unentschieden!'; return; }
        const line = winLine(board) || [];
        document.getElementById('ttt-status').textContent = `${res} gewinnt!`;
        [...ttt.children].forEach((btn,i)=>{ if(line.includes(i)) btn.classList.add('win'); });
      }
      function humanMove(i){
        if(lock || board[i] || winnerOf(board)) return;
        board[i]=HUMAN; draw();
        const w=winnerOf(board); if(w){ endGame(w); return; }
        if(emptyIdx(board).length===0){ endGame('draw'); return; }
        lock = true; document.getElementById('ttt-status').textContent='Computer denkt …';
        setTimeout(aiMove, 200);
      }
      function aiMove(){
        const best = minimax(board.slice(), AI, 0);
        board[best.index] = AI; draw(); lock=false;
        const w=winnerOf(board); if(w){ endGame(w); return; }
        if(emptyIdx(board).length===0){ endGame('draw'); return; }
        document.getElementById('ttt-status').textContent='Du bist X. Computer ist O.';
      }
      function minimax(b, player, depth){
        const w = winnerOf(b);
        if(w===AI) return {score:10-depth};
        if(w===HUMAN) return {score:depth-10};
        const em = emptyIdx(b);
        if(!em.length) return {score:0};
        const moves=[];
        for(const idx of em){
          const move={index:idx}; b[idx]=player;
          move.score = minimax(b, player===AI?HUMAN:AI, depth+1).score;
          b[idx]=''; moves.push(move);
        }
        if(player===AI){ let best=-Infinity, mv; for(const m of moves){ if(m.score>best){best=m.score;mv=m} } return mv; }
        else{ let best=Infinity, mv; for(const m of moves){ if(m.score<best){best=m.score;mv=m} } return mv; }
      }
      document.getElementById('ttt-reset').onclick=()=>{board=Array(9).fill('');lock=false;draw();document.getElementById('ttt-status').textContent='Du bist X. Computer ist O.'}
      draw();
    </script>
    """
    return render_page("Tic-Tac-Toe · aaron-sigma.de", body, extra)

# ─────────────────────────────────────────────────────────────────────────────
#  CASINO – Auswahl Roulette / Blackjack + Guthaben + Code-Einlösung
@app.route("/casino")
def page_casino():
    body = """
    <section class="card">
      <h2>🎰 Casino</h2>
      <div class="row" style="justify-content:space-between">
        <div class="bank">Guthaben: <span id="bank">0</span> A$</div>
        <div class="row">
          <input id="redeem" placeholder="Code eingeben (z.B. AARON100)"/>
          <button class="btn sec" id="redeemBtn">Einlösen</button>
          <button class="btn danger" id="resetBank">Reset</button>
        </div>
      </div>
      <p class="muted" style="margin-top:6px">Hinweis: Guthaben wird lokal im Browser als „Aaron Dollar (A$)“ gespeichert.</p>

      <div class="tabs">
        <div class="tab active" data-tab="pick">Spiel wählen</div>
        <div class="tab" data-tab="bj">Blackjack</div>
        <div class="tab" data-tab="ru">Roulette</div>
      </div>

      <!-- Auswahl -->
      <div id="tab-pick">
        <p>Wähle dein Spiel:</p>
        <div class="row">
          <button class="btn" onclick="openTab('bj')">🃏 Blackjack</button>
          <button class="btn" onclick="openTab('ru')">🎡 Roulette</button>
        </div>
      </div>

      <!-- Blackjack -->
      <div id="tab-bj" style="display:none">
        <h3>🃏 Blackjack</h3>
        <div class="row">
          <input id="bjBet" type="number" min="1" placeholder="Einsatz (A$)"/>
          <button class="btn sec" id="bjDeal">Deal</button>
          <button class="btn sec" id="bjHit" disabled>Hit</button>
          <button class="btn sec" id="bjStand" disabled>Stand</button>
        </div>
        <div class="row" style="margin-top:8px">
          <div>
            <div><b>Spieler</b> – Summe: <span id="bjPS">0</span></div>
            <div class="hand" id="bjPH"></div>
          </div>
          <div>
            <div><b>Dealer</b> – Summe: <span id="bjDS">0</span></div>
            <div class="hand" id="bjDH"></div>
          </div>
        </div>
        <p class="hint" id="bjMsg"></p>
      </div>

      <!-- Roulette -->
      <div id="tab-ru" style="display:none">
        <h3>🎡 Roulette</h3>
        <div class="row">
          <select id="ruType">
            <option value="red">Rot (1:1)</option>
            <option value="black">Schwarz (1:1)</option>
            <option value="odd">Ungerade (1:1)</option>
            <option value="even">Gerade (1:1)</option>
            <option value="number">Zahl 0–36 (35:1)</option>
          </select>
          <input id="ruNum" type="number" min="0" max="36" placeholder="Zahl" style="width:100px;display:none"/>
          <input id="ruBet" type="number" min="1" placeholder="Einsatz (A$)"/>
          <button class="btn sec" id="ruSpin">Drehen</button>
        </div>
        <p class="hint" id="ruMsg"></p>
      </div>
    </section>
    """
    extra = """
    <script>
      // ───── Aaron Dollar (LocalStorage) ─────
      const BANK_KEY='aaron_bank_v1';
      const $bank = document.getElementById('bank');
      function getBank(){ return +localStorage.getItem(BANK_KEY) || 0; }
      function setBank(v){ localStorage.setItem(BANK_KEY, Math.max(0, Math.floor(v))); updateBank(); }
      function addBank(v){ setBank(getBank()+Math.floor(v)); }
      function subBank(v){ setBank(getBank()-Math.floor(v)); }
      function updateBank(){ $bank.textContent = getBank(); }
      updateBank();

      // Reset
      document.getElementById('resetBank').onclick = () => {
        if(confirm('Guthaben wirklich zurücksetzen?')) setBank(0);
      };

      // Codes einlösen → Server prüft, einmalig
      document.getElementById('redeemBtn').onclick = async () => {
        const code = (document.getElementById('redeem').value || '').trim();
        if(!code) return;
        const r = await fetch('/api/redeem', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({code})});
        const j = await r.json();
        if(j.ok){ addBank(j.amount); alert(`✅ +${j.amount} A$ gutgeschrieben!`); document.getElementById('redeem').value=''; }
        else { alert('❌ ' + (j.error || 'Code ungültig')); }
      };

      // Tabs
      const tabs = [...document.querySelectorAll('.tab')];
      function openTab(key){
        tabs.forEach(t=>t.classList.toggle('active', t.dataset.tab===key || (key==='pick'&&t.dataset.tab==='pick')));
        document.getElementById('tab-pick').style.display = key==='pick'?'block':'none';
        document.getElementById('tab-bj').style.display = key==='bj'?'block':'none';
        document.getElementById('tab-ru').style.display = key==='ru'?'block':'none';
      }
      tabs.forEach(t=>t.onclick=()=>openTab(t.dataset.tab));

      // ───── Blackjack ─────
      const bjPH=document.getElementById('bjPH'), bjDH=document.getElementById('bjDH');
      const bjPS=document.getElementById('bjPS'), bjDS=document.getElementById('bjDS');
      const bjMsg=document.getElementById('bjMsg');
      const bjBet=document.getElementById('bjBet');
      const bjDeal=document.getElementById('bjDeal'), bjHit=document.getElementById('bjHit'), bjStand=document.getElementById('bjStand');

      let deck=[], pHand=[], dHand=[], inRound=false, bet=0;

      function newDeck(){
        const ranks=['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
        const suits=['♠','♥','♦','♣'];
        deck=[];
        for(const r of ranks){ for(const s of suits){ deck.push(r+s); } }
        for(let i=deck.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [deck[i],deck[j]]=[deck[j],deck[i]]; }
      }
      function valCard(c){ const r=c.slice(0,-1); if(r==='A') return 11; if(['K','Q','J'].includes(r)) return 10; return +r; }
      function sum(hand){ let s=hand.reduce((a,c)=>a+valCard(c),0); let aces=hand.filter(c=>c[0]==='A').length; while(s>21 && aces>0){ s-=10; aces--; } return s; }
      function render(){
        bjPH.innerHTML=''; bjDH.innerHTML='';
        pHand.forEach(c=>{ const t=document.createElement('div'); t.className='tag'; t.textContent=c; bjPH.appendChild(t); });
        dHand.forEach(c=>{ const t=document.createElement('div'); t.className='tag'; t.textContent=c; bjDH.appendChild(t); });
        bjPS.textContent=sum(pHand); bjDS.textContent=sum(dHand);
      }
      function end(msg, delta){
        inRound=false; bjHit.disabled=bjStand.disabled=true; bjDeal.disabled=false;
        bjMsg.textContent=msg;
        if(delta>0) addBank(delta);
        if(delta<0) subBank(-delta);
      }

      bjDeal.onclick=()=>{
        bet = Math.max(1, Math.floor(+bjBet.value||0));
        if(getBank() < bet){ alert('Zu wenig Guthaben.'); return; }
        // Einsatz wird erst bei Ausgang verrechnet (bei Verlust abgezogen, bei Gewinn addiert)
        newDeck(); pHand=[deck.pop(),deck.pop()]; dHand=[deck.pop(),deck.pop()];
        inRound=true; bjHit.disabled=bjStand.disabled=false; bjDeal.disabled=true; bjMsg.textContent='';
        render();
        if(sum(pHand)===21){ // Natural
          const dealerBJ = (sum(dHand)===21);
          if(dealerBJ) end('Push (beide Blackjack).', 0);
          else end('Blackjack! Gewinn 1.5× Einsatz.', Math.floor(bet*1.5));
        }
      };
      bjHit.onclick=()=>{
        if(!inRound) return;
        pHand.push(deck.pop()); render();
        if(sum(pHand)>21) end('Bust! Du verlierst den Einsatz.', -bet);
      };
      bjStand.onclick=()=>{
        if(!inRound) return;
        // Dealer zieht bis 17
        while(sum(dHand)<17){ dHand.push(deck.pop()); }
        render();
        const ps=sum(pHand), ds=sum(dHand);
        if(ds>21) end('Dealer bust – du gewinnst!', bet);
        else if(ps>ds) end('Du gewinnst!', bet);
        else if(ps<ds) end('Dealer gewinnt.', -bet);
        else end('Push. Einsatz zurück.', 0);
      };

      // ───── Roulette ─────
      const redSet = new Set([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]);
      const ruType=document.getElementById('ruType'), ruNum=document.getElementById('ruNum'), ruBet=document.getElementById('ruBet'), ruMsg=document.getElementById('ruMsg');
      ruType.onchange = ()=>{ ruNum.style.display = (ruType.value==='number')?'inline-block':'none'; };
      document.getElementById('ruSpin').onclick=()=>{
        const bet = Math.max(1, Math.floor(+ruBet.value||0));
        if(getBank()<bet) { alert('Zu wenig Guthaben.'); return; }
        const n = Math.floor(Math.random()*37); // 0–36
        let win = 0, txt = `Gefallen: ${n} ${n===0?'(grün)':''}`;
        if(ruType.value==='number'){
          const pick = Math.max(0, Math.min(36, Math.floor(+ruNum.value||-1)));
          if(pick===n) win = bet*35;
        }else if(ruType.value==='red'){
          if(n!==0 && redSet.has(n)) win = bet;
        }else if(ruType.value==='black'){
          if(n!==0 && !redSet.has(n)) win = bet;
        }else if(ruType.value==='odd'){
          if(n!==0 && n%2===1) win = bet;
        }else if(ruType.value==='even'){
          if(n!==0 && n%2===0) win = bet;
        }
        if(win>0){ addBank(win); txt += ` – Gewinn: +${win} A$`; }
        else { subBank(bet); txt += ` – Verlust: -${bet} A$`; }
        ruMsg.textContent = txt;
      };

      // Standard: Auswahl-Tab
      openTab('pick');
    </script>
    """
    return render_page("Casino · aaron-sigma.de", body, extra)

# Redeem-API: prüft Code einmalig und gibt Betrag zurück
@app.post("/api/redeem")
def api_redeem():
    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip().upper()
    if not code:
        return jsonify({"ok": False, "error": "Kein Code übergeben."}), 400
    amount = VALID_CODES.pop(code, None)
    if amount is None:
        return jsonify({"ok": False, "error": "Ungültiger oder bereits benutzter Code."}), 200
    return jsonify({"ok": True, "amount": int(amount)})

# ─────────────────────────────────────────────────────────────────────────────
#  BOOTSTRAP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
