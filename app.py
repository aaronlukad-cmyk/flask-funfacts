from flask import Flask, render_template_string, url_for

app = Flask(__name__)

# ---------- Basis Template (Navbar, Styles, gemeinsame JS) ----------
BASE = r"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{{ title }}</title>
<style>
  :root{ --bg:#0a1020; --card:#0e1628; --muted:#1d2740; --text:#c9d3ef; --accent:#1c70f8; }
  html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font:16px/1.5 Inter,system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
  a{color:#9bc1ff;text-decoration:none} a:hover{text-decoration:underline}
  .wrap{max-width:1100px;margin:0 auto;padding:16px}
  .title{font-weight:800;margin:8px 0 16px}
  .section{margin:24px 0}
  .card{background:var(--card);border:1px solid var(--muted);border-radius:12px;padding:14px}
  .row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
  .btn{background:var(--accent);border:1px solid #1761d6;color:#fff;border-radius:8px;padding:8px 12px;cursor:pointer}
  .btn[disabled]{opacity:.55;cursor:not-allowed}
  input,select{background:#091129;color:var(--text);border:1px solid var(--muted);border-radius:8px;padding:6px 8px}
  .muted{color:#92a0c6}
  .msg{min-height:22px}
  .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  .hidden{display:none}

  /* Navbar */
  .nav{position:sticky;top:0;z-index:20;background:#0b1326;border-bottom:1px solid var(--muted)}
  .nav-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;gap:14px;padding:10px 16px}
  .brand{font-weight:900;letter-spacing:.3px}
  .sp{flex:1}
  .drop{position:relative}
  .drop > button{background:#10203d;border:1px solid var(--muted);color:#eaf1ff;border-radius:8px;padding:8px 12px}
  .menu{position:absolute;inset:auto auto auto 0;transform:translateY(8px);min-width:210px;background:#0e1628;border:1px solid var(--muted);border-radius:10px;padding:6px;display:none}
  .menu a{display:block;padding:8px;border-radius:8px}
  .menu a:hover{background:#0f1a34}
  .drop.open .menu{display:block}

  /* Tabs */
  .tabs{display:flex;gap:8px;margin:8px 0 12px}
  .tab-btn{padding:8px 12px;border:1px solid var(--muted);background:#0b1220;border-radius:8px;color:#c9d3ef;cursor:pointer}
  .tab-btn.is-active{border-color:var(--accent);color:#fff}
  .tab-panel{display:none}
  .tab-panel.is-active{display:block}

  /* TicTacToe */
  .ttt-board{display:grid;grid-template-columns:repeat(3,92px);gap:8px;justify-content:center;margin:10px 0}
  .ttt-cell{
    width:92px;height:92px;border-radius:12px;border:1px solid #2d3c6a;display:flex;align-items:center;justify-content:center;
    background:#0e162a;font-size:44px;font-weight:900;cursor:pointer;color:#fff
  }
  .ttt-cell:disabled{opacity:.55;cursor:not-allowed}
  .ttt-row{display:flex;gap:12px;align-items:center;justify-content:center}

  /* Blackjack */
  .bj-table{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  .hand-title{font-weight:700;margin-bottom:4px}
  .cards{display:flex;gap:8px;flex-wrap:wrap;min-height:86px}
  .card-ui{
    width:60px;height:86px;border-radius:8px;border:1px solid #2a3553;
    display:flex;flex-direction:column;justify-content:space-between;padding:6px;background:#fff;color:#111;font-weight:700;
  }
  .card-ui.red{color:#d90f2f}
  .card-ui .rank{font-size:18px}
  .card-ui .suit{font-size:20px;text-align:right}
  .card-back{
    width:60px;height:86px;border-radius:8px;border:1px solid #2a3553;
    background:repeating-linear-gradient(45deg,#223,#223 6px,#2d3c6a 6px,#2d3c6a 12px);
  }

  /* Roulette Wheel */
  .roulette-wrap{display:flex;justify-content:center;align-items:center;margin:10px 0}
  .wheel{position:relative;width:260px;height:260px}
  .wheel-disc{
    position:absolute;inset:0;border-radius:50%;
    background:conic-gradient(
      #0a0 0 9.73deg,#000 9.73deg 19.46deg,#0a0 19.46deg 29.19deg,#000 29.19deg 38.92deg,
      #0a0 38.92deg 48.65deg,#000 48.65deg 58.38deg,#0a0 58.38deg 68.11deg,#000 68.11deg 77.84deg,
      #0a0 77.84deg 87.57deg,#000 87.57deg 97.3deg,#0a0 97.3deg 107.03deg,#000 107.03deg 116.76deg,
      #0a0 116.76deg 126.49deg,#000 126.49deg 136.22deg,#0a0 136.22deg 145.95deg,#000 145.95deg 155.68deg,
      #0a0 155.68deg 165.41deg,#000 165.41deg 175.14deg,#0a0 175.14deg 184.87deg,#000 184.87deg 194.6deg,
      #0a0 194.6deg 204.33deg,#000 204.33deg 214.06deg,#0a0 214.06deg 223.79deg,#000 223.79deg 233.52deg,
      #0a0 233.52deg 243.25deg,#000 243.25deg 252.98deg,#0a0 252.98deg 262.71deg,#000 262.71deg 272.44deg,
      #0a0 272.44deg 282.17deg,#000 282.17deg 291.9deg,#0a0 291.9deg 301.63deg,#000 301.63deg 311.36deg,
      #0a0 311.36deg 321.09deg,#000 321.09deg 330.82deg,#0a0 330.82deg 340.55deg,#000 340.55deg 350.28deg,
      #0a0 350.28deg 360deg);
    border:10px solid #2d3c6a;
  }
  .pointer{
    position:absolute;top:-6px;left:50%;transform:translateX(-50%);
    width:0;height:0;border-left:10px solid transparent;border-right:10px solid transparent;
    border-bottom:14px solid #ffc107;filter:drop-shadow(0 0 2px #000);
  }
  .ball{
    position:absolute;inset:0;margin:auto;width:10px;height:10px;border-radius:50%;background:#fff;box-shadow:0 0 4px #000;
    transform-origin:130px 130px;
  }

  /* footer */
  footer{margin:40px 0 10px;text-align:center;color:#8fa0c8}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <div class="nav-inner">
    <div class="brand">aaron-sigma.de</div>
    <div class="sp"></div>
    <div class="drop" id="dd">
      <button type="button">Bereiche ▾</button>
      <div class="menu">
        <a href="{{ url_for('home') }}">🏠 Start</a>
        <a href="{{ url_for('tictactoe') }}">❌⭕ Tic-Tac-Toe</a>
        <a href="{{ url_for('casino') }}">🎰 Casino</a>
      </div>
    </div>
  </div>
</nav>

<div class="wrap">
  {{ content|safe }}
  <footer>Made by Aaron ✨</footer>
</div>

<script>
/* Dropdown */
const dd = document.getElementById('dd');
dd?.querySelector('button')?.addEventListener('click',()=>dd.classList.toggle('open'));
document.addEventListener('click',e=>{ if(!dd.contains(e.target)) dd.classList.remove('open'); });

/* Uhr */
function clock(){
  const d = new Date();
  const pad=n=>(''+n).padStart(2,'0');
  const c = document.getElementById('clock'); if(c) c.textContent=`${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  const dt = document.getElementById('date'); if(dt) dt.textContent=d.toLocaleDateString('de-DE',{weekday:'long',day:'2-digit',month:'2-digit',year:'numeric'});
}
setInterval(clock,1000); clock();

/* Balance */
function getBalance(){ return Number(localStorage.getItem('balance')||0); }
function setBalance(v){
  v=Math.max(0,Math.floor(v));
  localStorage.setItem('balance',String(v));
  const ids=['balance','balance2'];
  ids.forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent=v; });
}
setBalance(getBalance());

/* Codes – hier neue hinzufügen */
const REDEEM_CODES = {
  "AARON-START-1000": 1000,
  // "MEGA-50": 50,
  // "VIP-777": 777,
};

function redeem(){
  const input=document.getElementById('code'); const msg=document.getElementById('redeem-msg');
  const code=(input.value||'').trim().toUpperCase();
  if(!code){ msg.textContent='Bitte Code eingeben.'; return; }
  const amount=REDEEM_CODES[code];
  if(!amount){ msg.textContent='Ungültiger Code.'; return; }
  if(localStorage.getItem('code:'+code)){ msg.textContent='Code bereits verwendet.'; return; }
  localStorage.setItem('code:'+code,'used');
  setBalance(getBalance()+amount);
  msg.textContent=`+${amount} A$ gutgeschrieben!`;
  input.value='';
}
const rbtn=document.getElementById('redeem'); if(rbtn) rbtn.addEventListener('click',redeem);
</script>

<!-- Seiten-Skripte -->
{{ page_js|safe }}
</body>
</html>
"""

# ---------- Startseite ----------
HOME = r"""
<section id="home" class="section">
  <h2 class="title">Willkommen 👋</h2>
  <div class="grid-2">
    <div class="card">
      <b>Uhrzeit</b>
      <div id="clock" style="font-weight:900;font-size:38px;margin:6px 0 2px"></div>
      <div id="date" class="muted"></div>
    </div>

    <div class="card">
      <b>Guthaben</b>
      <div class="row">
        <div>Aktuell: <b><span id="balance">0</span> A$</b></div>
      </div>
      <div class="row">
        <input id="code" placeholder="Gutschein-Code">
        <button class="btn" id="redeem">Einlösen</button>
        <div id="redeem-msg" class="msg muted"></div>
      </div>
      <div class="muted" style="margin-top:6px">Tipp: Start-Code <code>AARON-START-1000</code> (+1000 A$)</div>
    </div>
  </div>
</section>
"""

# ---------- TicTacToe Seite ----------
TTT = r"""
<section id="tictactoe" class="section">
  <h2 class="title">❌⭕ Tic-Tac-Toe</h2>
  <div class="card">
    <div class="ttt-row">
      <label>Modus:
        <select id="ttt-level">
          <option value="easy">Leicht</option>
          <option value="normal">Normal</option>
          <option value="hard">Schwer</option>
          <option value="impossible" selected>Unmöglich</option>
        </select>
      </label>
      <button class="btn" id="ttt-new">Neue Runde</button>
      <div id="ttt-msg" class="msg muted"></div>
    </div>
    <div class="ttt-board" id="board"></div>
  </div>
</section>
"""

TTT_JS = r"""
<script>
const boardEl = document.getElementById('board');
const tttMsg = document.getElementById('ttt-msg');
const levelSel = document.getElementById('ttt-level');
const newBtn   = document.getElementById('ttt-new');

let tBoard = Array(9).fill(null);
let human='X', ai='O', tOver=false;

function renderBoard(){
  boardEl.innerHTML='';
  for(let i=0;i<9;i++){
    const b=document.createElement('button');
    b.className='ttt-cell';
    b.textContent=tBoard[i]||'';
    b.disabled=!!tBoard[i]||tOver;
    b.addEventListener('click',()=>humanMove(i));
    boardEl.appendChild(b);
  }
}
function win(b,p){ const L=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]; return L.some(([a,c,d])=>b[a]===p&&b[c]===p&&b[d]===p); }
function emptyIdx(b){ return b.map((v,i)=>v?null:i).filter(v=>v!==null); }
function score(b){ if(win(b,ai))return 10; if(win(b,human))return -10; return 0; }
function minimax(b,depth,alpha,beta,maximizing,maxDepth=Infinity){
  const scr=score(b);
  if(scr!==0||emptyIdx(b).length===0||depth===maxDepth) return scr;
  if(maximizing){
    let best=-Infinity;
    for(const i of emptyIdx(b)){ b[i]=ai; best=Math.max(best,minimax(b,depth+1,alpha,beta,false,maxDepth)); b[i]=null; alpha=Math.max(alpha,best); if(beta<=alpha)break; }
    return best-(depth*0.01);
  }else{
    let best=+Infinity;
    for(const i of emptyIdx(b)){ b[i]=human; best=Math.min(best,minimax(b,depth+1,alpha,beta,true,maxDepth)); b[i]=null; beta=Math.min(beta,best); if(beta<=alpha)break; }
    return best+(depth*0.01);
  }
}
function bestMove(level){
  const empties=emptyIdx(tBoard);
  if(level==='easy'){
    if(Math.random()<0.7) return empties[Math.floor(Math.random()*empties.length)];
    return heuristicMove();
  }
  if(level==='normal'){
    return empties[Math.floor(Math.random()*empties.length)];
  }
  if(level==='hard'){
    let bi=-1,bv=-Infinity;
    for(const i of empties){ tBoard[i]=ai; const v=minimax(tBoard,0,-Infinity,Infinity,false,2); tBoard[i]=null; if(v>bv){bv=v;bi=i;} }
    return bi;
  }
  let bi=-1,bv=-Infinity;
  for(const i of empties){ tBoard[i]=ai; const v=minimax(tBoard,0,-Infinity,Infinity,false,Infinity); tBoard[i]=null; if(v>bv){bv=v;bi=i;} }
  return bi;
  function heuristicMove(){
    for(const i of empties){ tBoard[i]=ai; if(win(tBoard,ai)){ tBoard[i]=null; return i; } tBoard[i]=null; }
    for(const i of empties){ tBoard[i]=human; if(win(tBoard,human)){ tBoard[i]=null; return i; } tBoard[i]=null; }
    if(tBoard[4]==null) return 4;
    const corners=[0,2,6,8].filter(i=>tBoard[i]==null);
    if(corners.length) return corners[Math.floor(Math.random()*corners.length)];
    return empties[Math.floor(Math.random()*empties.length)];
  }
}
function humanMove(i){
  if(tOver||tBoard[i])return;
  tBoard[i]=human; renderBoard();
  if(win(tBoard,human)){ tttMsg.textContent='Du gewinnst!'; tOver=true; return; }
  if(emptyIdx(tBoard).length===0){ tttMsg.textContent='Unentschieden.'; tOver=true; return; }
  const mv=bestMove(levelSel.value); tBoard[mv]=ai; renderBoard();
  if(win(tBoard,ai)){ tttMsg.textContent='Computer gewinnt.'; tOver=true; return; }
  if(emptyIdx(tBoard).length===0){ tttMsg.textContent='Unentschieden.'; tOver=true; }
}
function tttNew(){
  tOver=false; tBoard=Array(9).fill(null); tttMsg.textContent=''; renderBoard();
  if(levelSel.value==='hard'||levelSel.value==='impossible'){ if(Math.random()<0.5){ const mv=bestMove(levelSel.value); tBoard[mv]=ai; renderBoard(); } }
}
document.getElementById('ttt-new')?.addEventListener('click',tttNew);
renderBoard();
</script>
"""

# ---------- Casino Seite ----------
CASINO = r"""
<section id="casino" class="section">
  <h2 class="title">🎰 Casino</h2>
  <div class="card" style="margin-bottom:16px">
    Guthaben: <b><span id="balance2">0</span> A$</b>
  </div>

  <div class="tabs">
    <button class="tab-btn is-active" data-tab="blackjack">Blackjack</button>
    <button class="tab-btn" data-tab="roulette">Roulette</button>
  </div>

  <!-- BLACKJACK -->
  <div class="tab-panel is-active" id="tab-blackjack">
    <div class="card" style="gap:16px">
      <div class="row">
        <label>Einsatz: <input id="bj-bet" type="number" min="1" step="1" value="10" style="width:100px"> A$</label>
        <button id="bj-deal" class="btn">🔄 Neue Runde</button>
        <button id="bj-hit" class="btn" disabled>🃏 Hit</button>
        <button id="bj-stand" class="btn" disabled>✋ Stand</button>
      </div>
      <div class="bj-table">
        <div>
          <div class="hand-title">Dealer</div>
          <div id="bj-dealer" class="cards"></div>
          <div id="bj-dealer-total" class="muted">–</div>
        </div>
        <div>
          <div class="hand-title">Spieler</div>
          <div id="bj-player" class="cards"></div>
          <div id="bj-player-total" class="muted">–</div>
        </div>
      </div>
      <div id="bj-msg" class="msg muted"></div>
    </div>
  </div>

  <!-- ROULETTE -->
  <div class="tab-panel" id="tab-roulette">
    <div class="card" style="gap:16px">
      <div class="row" style="flex-wrap:wrap">
        <label>Einsatz:
          <input id="rl-bet" type="number" min="1" step="1" value="10" style="width:100px"> A$
        </label>
        <label>Wette:
          <select id="rl-type">
            <option value="single">Zahl (0–36)</option>
            <option value="red">Rot</option>
            <option value="black">Schwarz</option>
            <option value="even">Gerade</option>
            <option value="odd">Ungerade</option>
            <option value="dozen1">1st 12 (1–12)</option>
            <option value="dozen2">2nd 12 (13–24)</option>
            <option value="dozen3">3rd 12 (25–36)</option>
          </select>
        </label>
        <label id="rl-number-wrap">Zahl:
          <input id="rl-number" type="number" min="0" max="36" value="7" style="width:80px">
        </label>
        <button id="rl-spin" class="btn">🎡 Spin</button>
      </div>

      <div class="roulette-wrap">
        <div class="wheel" id="rl-wheel">
          <div class="wheel-disc"></div>
          <div class="ball" id="rl-ball"></div>
          <div class="pointer"></div>
        </div>
      </div>

      <div>Ergebnis: Zahl <b><span id="rl-result">–</span></b>, Farbe <b><span id="rl-color">–</span></b></div>
      <div id="rl-msg" class="msg muted"></div>
    </div>
  </div>
</section>
"""

CASINO_JS = r"""
<script>
/* Tabs */
document.querySelectorAll('.tab-btn').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('.tab-btn').forEach(x=>x.classList.remove('is-active'));
    b.classList.add('is-active');
    document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('is-active'));
    document.getElementById('tab-'+b.dataset.tab).classList.add('is-active');
  });
});

/* Blackjack */
(function blackjack(){
  const suits=['♠','♥','♦','♣'], ranks=['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
  const elDealer=document.getElementById('bj-dealer');
  const elPlayer=document.getElementById('bj-player');
  const elDT=document.getElementById('bj-dealer-total');
  const elPT=document.getElementById('bj-player-total');
  const msg=document.getElementById('bj-msg');
  const btnDeal=document.getElementById('bj-deal');
  const btnHit=document.getElementById('bj-hit');
  const btnStand=document.getElementById('bj-stand');
  const betInput=document.getElementById('bj-bet');

  let deck=[], dealer=[], player=[], dealerHidden=true, inRound=false;

  function newDeck(){
    const d=[]; for(const s of suits){ for(const r of ranks){ d.push({r,s}); } }
    return Array(6).fill(0).flatMap(()=>shuffle([...d]));
  }
  function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]];} return a; }
  function val(c){ if(c.r==='A')return 11; if(['K','Q','J'].includes(c.r))return 10; return Number(c.r); }
  function total(h){ let t=h.reduce((s,c)=>s+val(c),0); let ac=h.filter(c=>c.r==='A').length; while(t>21&&ac>0){t-=10;ac--;} return t; }
  function renderCard(c,down=false){ if(down) return `<div class="card-back"></div>`; const red=(c.s==='♥'||c.s==='♦')?' red':''; return `<div class="card-ui${red}"><div class="rank">${c.r}</div><div class="suit">${c.s}</div></div>`; }
  function render(){
    elPlayer.innerHTML=player.map(renderCard).join(''); elPT.textContent=total(player);
    if(dealerHidden&&dealer.length){ elDealer.innerHTML=renderCard(dealer[0],true)+dealer.slice(1).map(renderCard).join(''); elDT.textContent='–'; }
    else{ elDealer.innerHTML=dealer.map(renderCard).join(''); elDT.textContent=total(dealer); }
  }
  function setUI(r){ btnHit.disabled=!r; btnStand.disabled=!r; }
  function canBet(){ const b=Number(betInput.value||0); return b>=1 && b<=getBalance(); }

  function startRound(){
    if(!canBet()){ msg.textContent='Nicht genug Guthaben oder ungültiger Einsatz.'; return; }
    setUI(true); msg.textContent=''; inRound=true; dealerHidden=true;
    if(deck.length<40) deck=newDeck();
    dealer=[deck.pop(),deck.pop()]; player=[deck.pop(),deck.pop()]; render();

    if(total(player)===21 && total(dealer)===21){ dealerHidden=false; render(); msg.textContent='Beide Blackjack – Push.'; inRound=false; setUI(false); return; }
    if(total(player)===21){ dealerHidden=false; render(); const win=Math.floor(Number(betInput.value)*1.5); setBalance(getBalance()+Number(betInput.value)+win); msg.textContent=`Blackjack! Gewinn: ${win} A$`; inRound=false; setUI(false); return; }
  }
  function dealerPlay(){ dealerHidden=false; render(); while(total(dealer)<17){ dealer.push(deck.pop()); render(); } }
  function finishRound(){
    const p=total(player), d=total(dealer), bet=Number(betInput.value);
    if(p>21){ msg.textContent='Bust! Verloren.'; inRound=false; setUI(false); return; }
    if(d>21){ msg.textContent='Dealer bust – du gewinnst!'; setBalance(getBalance()+bet*2); inRound=false; setUI(false); return; }
    if(p>d){ msg.textContent='Du gewinnst!'; setBalance(getBalance()+bet*2); }
    else if(p<d){ msg.textContent='Verloren.'; }
    else { msg.textContent='Push – Einsatz zurück.'; setBalance(getBalance()+bet); }
    inRound=false; setUI(false);
  }

  btnDeal?.addEventListener('click', ()=>{ const b=Number(betInput.value||0); if(b<1){ msg.textContent='Einsatz angeben.'; return; } if(b>getBalance()){ msg.textContent='Nicht genug Guthaben.'; return; } setBalance(getBalance()-b); startRound(); });
  btnHit?.addEventListener('click', ()=>{ if(!inRound)return; player.push(deck.pop()); render(); if(total(player)>21){ dealerHidden=false; render(); msg.textContent='Bust! Verloren.'; inRound=false; setUI(false); } });
  btnStand?.addEventListener('click', ()=>{ if(!inRound)return; dealerPlay(); finishRound(); });

  deck=newDeck();
})();

/* Roulette */
(function roulette(){
  const wheelEl=document.getElementById('rl-wheel');
  const ballEl=document.getElementById('rl-ball');
  const resEl=document.getElementById('rl-result');
  const colEl=document.getElementById('rl-color');
  const msg=document.getElementById('rl-msg');
  const spinBtn=document.getElementById('rl-spin');
  const betInp=document.getElementById('rl-bet');
  const typeSel=document.getElementById('rl-type');
  const numWrap=document.getElementById('rl-number-wrap');
  const numInp=document.getElementById('rl-number');

  const redNums=new Set([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]);
  const color=n=> n===0?'grün':(redNums.has(n)?'rot':'schwarz');

  typeSel?.addEventListener('change',()=>{ numWrap.style.display=(typeSel.value==='single')?'inline-block':'none'; });

  function canBet(){ const b=Number(betInp.value||0); return b>=1 && b<=getBalance(); }

  function spin(){
    if(!canBet()){ msg.textContent='Nicht genug Guthaben oder ungültiger Einsatz.'; return; }
    msg.textContent=''; const bet=Number(betInp.value); setBalance(getBalance()-bet);

    const target=Math.floor(Math.random()*37);
    const base=360*6;
    const wheelRot=base + (360/37)*target;
    const ballRot=-(base*1.4 + (360/37)*target);

    wheelEl.style.transition='transform 3.2s cubic-bezier(.22,.61,.36,1)';
    ballEl.style.transition='transform 3.2s cubic-bezier(.22,.61,.36,1)';
    wheelEl.style.transform=`rotate(${wheelRot}deg)`;
    ballEl.style.transform=`rotate(${ballRot}deg)`;

    setTimeout(()=>{
      resEl.textContent=String(target);
      const c=color(target); colEl.textContent=c;
      const t=typeSel.value; let win=0;

      if(t==='single'){ const n=Number(numInp.value); if(n===target) win=bet*35; }
      else if(t==='red' && c==='rot') win=bet;
      else if(t==='black' && c==='schwarz') win=bet;
      else if(t==='even' && target!==0 && target%2===0) win=bet;
      else if(t==='odd' && target%2===1) win=bet;
      else if(t==='dozen1' && target>=1 && target<=12) win=bet*2;
      else if(t==='dozen2' && target>=13 && target<=24) win=bet*2;
      else if(t==='dozen3' && target>=25 && target<=36) win=bet*2;

      if(win>0){ setBalance(getBalance()+bet+win); msg.textContent=`Gewonnen: +${win} A$`; }
      else{ msg.textContent='Leider verloren.'; }

      setTimeout(()=>{ wheelEl.style.transition='none'; ballEl.style.transition='none'; }, 200);
    },3300);
  }
  spinBtn?.addEventListener('click', spin);
})();
</script>
"""

def render_page(title, content_html, page_js=""):
    return render_template_string(
        BASE, title=title, content=content_html, page_js=page_js
    )

# ---------- Routes ----------
@app.route("/")
def home():
    return render_page("Start · Aaron", HOME, "")

@app.route("/tictactoe")
def tictactoe():
    return render_page("Tic-Tac-Toe · Aaron", TTT, TTT_JS)

@app.route("/casino")
def casino():
    return render_page("Casino · Aaron", CASINO, CASINO_JS)

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
