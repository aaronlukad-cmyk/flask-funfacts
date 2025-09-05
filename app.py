from flask import Flask, render_template_string, url_for

app = Flask(__name__)

# ========================= Base Layout =========================
BASE = r"""
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{{ title }}</title>
<style>
  :root{ --bg:#0a1020; --card:#0e1628; --muted:#1d2740; --text:#c9d3ef; --accent:#1c70f8; }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font:16px/1.5 Inter,system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
  a{color:#9bc1ff;text-decoration:none} a:hover{text-decoration:underline}
  .wrap{max-width:1100px;margin:0 auto;padding:16px}
  .title{font-weight:800;margin:8px 0 16px}
  .section{margin:24px 0}
  .card{background:var(--card);border:1px solid var(--muted);border-radius:12px;padding:14px}
  .row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
  .btn{background:var(--accent);border:1px solid #1761d6;color:#fff;border-radius:8px;padding:8px 12px;cursor:pointer}
  .btn[disabled]{opacity:.55;cursor:not-allowed}
  input,select,textarea{background:#091129;color:var(--text);border:1px solid var(--muted);border-radius:8px;padding:6px 8px}
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
  .wheel{position:relative;width:300px;height:300px}
  .wheel-disc{
    position:absolute;inset:0;border-radius:50%;
    background:
      conic-gradient(
        #0fbf3a 0 9.73deg,
        #c1121f 9.73deg 19.46deg, #111 19.46deg 29.19deg, #c1121f 29.19deg 38.92deg, #111 38.92deg 48.65deg,
        #c1121f 48.65deg 58.38deg, #111 58.38deg 68.11deg, #c1121f 68.11deg 77.84deg, #111 77.84deg 87.57deg,
        #c1121f 87.57deg 97.3deg,  #111 97.3deg 107.03deg, #c1121f 107.03deg 116.76deg, #111 116.76deg 126.49deg,
        #c1121f 126.49deg 136.22deg, #111 136.22deg 145.95deg, #c1121f 145.95deg 155.68deg, #111 155.68deg 165.41deg,
        #c1121f 165.41deg 175.14deg, #111 175.14deg 184.87deg, #c1121f 184.87deg 194.6deg, #111 194.6deg 204.33deg,
        #c1121f 204.33deg 214.06deg, #111 214.06deg 223.79deg, #c1121f 223.79deg 233.52deg, #111 233.52deg 243.25deg,
        #c1121f 243.25deg 252.98deg, #111 252.98deg 262.71deg, #c1121f 262.71deg 272.44deg, #111 272.44deg 282.17deg,
        #c1121f 282.17deg 291.9deg,  #111 291.9deg 301.63deg, #c1121f 301.63deg 311.36deg, #111 311.36deg 321.09deg,
        #c1121f 321.09deg 330.82deg, #111 330.82deg 340.55deg, #c1121f 340.55deg 350.28deg, #111 350.28deg 360deg
      );
    border:12px solid #2d3c6a;
  }
  .wheel-label{
    position:absolute; left:50%; top:50%; width:0; height:0; transform-origin:0 0; z-index:1;
    font-weight:800; font-size:12px; color:#eee; pointer-events:none;
  }
  .wheel-label span{
    display:inline-block; transform:translate(118px, -6px) rotate(var(--r-rev));
    min-width:20px; text-align:center; padding:2px 4px; border-radius:4px;
  }
  .wheel-label.red span{ background:#c1121f; }
  .wheel-label.black span{ background:#111; }
  .wheel-label.green span{ background:#0fbf3a; color:#042; }

  .pointer{
    position:absolute;top:-6px;left:50%;transform:translateX(-50%);
    width:0;height:0;border-left:10px solid transparent;border-right:10px solid transparent;
    border-bottom:14px solid #ffc107;filter:drop-shadow(0 0 2px #000); z-index:4;
  }
  .ball{
    position:absolute;left:50%;top:50%;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:#fff;box-shadow:0 0 4px #000;
    transform-origin:0 0; z-index:3;
  }

  footer{margin:40px 0 10px;text-align:center;color:#8fa0c8}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <div class="brand">aaron-sigma.de</div>
    <div class="sp"></div>
    <div class="drop" id="dd">
      <button type="button">Bereiche ▾</button>
      <div class="menu">
        <a href="{{ url_for('home') }}">🏠 Start</a>
        <a href="{{ url_for('fun') }}">😂 Fun Facts</a>
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
  const c = document.getElementById('clock'); if(c) c.innerHTML = `
    <span style="background:linear-gradient(90deg,#60a5fa,#a78bfa,#22d3ee);-webkit-background-clip:text;background-clip:text;color:transparent">
      ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}
    </span>`;
  const dt = document.getElementById('date'); if(dt) dt.textContent=d.toLocaleDateString('de-DE',{weekday:'long',day:'2-digit',month:'2-digit',year:'numeric'});
}
setInterval(clock,1000); clock();

/* Balance */
function getBalance(){ return Number(localStorage.getItem('balance')||0); }
function setBalance(v){
  v=Math.max(0,Math.floor(v));
  localStorage.setItem('balance',String(v));
  ['balance','balance2'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent=v; });
}
setBalance(getBalance());

/* Codes (10 Stück, inkl. Leon/Armin) */
const REDEEM_CODES = {
  "LEON": 100,
  "ARMIN": 101,
  "COMET": 200,
  "RIVER": 200,
  "MOUNTAIN": 200,
  "FALCON": 75,
  "ORBIT": 75,
  "NEBULA": 50,
  "QUARTZ": 50,
  "TITAN": 1000
};
function redeem(){
  const input=document.getElementById('code'); const msg=document.getElementById('redeem-msg');
  const code=(input?.value||'').trim().toUpperCase();
  if(!code){ if(msg) msg.textContent='Bitte Code eingeben.'; return; }
  const amount=REDEEM_CODES[code];
  if(!amount){ if(msg) msg.textContent='Ungültiger Code.'; return; }
  if(localStorage.getItem('code:'+code)){ if(msg) msg.textContent='Code bereits verwendet.'; return; }
  localStorage.setItem('code:'+code,'used');
  setBalance(getBalance()+amount);
  if(msg) msg.textContent=`+${amount} A$ gutgeschrieben!`;
  if(input) input.value='';
}
</script>

{{ page_js|safe }}
</body>
</html>
"""

# ========================= Pages =========================

HOME = r"""
<section id="home" class="section">
  <h2 class="title">Willkommen 👋</h2>
  <div class="card" style="text-align:center">
    <div id="clock" style="font-weight:900;font-size:54px;margin:10px 0 4px"></div>
    <div id="date" class="muted" style="margin-bottom:10px"></div>
    <p style="max-width:700px;margin:10px auto 4px;">
      Wähle oben im Menü: <b>Fun Facts</b>, <b>Tic-Tac-Toe</b> oder <b>Casino</b> (Blackjack & Roulette).
    </p>
  </div>
</section>
"""

FUN = r"""
<section id="fun" class="section">
  <h2 class="title">😂 Fun Facts</h2>
  <div class="card">
    <div class="row">
      <button id="fact-new" class="btn">🎲 Neuen Fun Fact</button>
      <button id="fact-copy" class="btn">📋 Kopieren</button>
      <button id="fact-fav" class="btn">⭐ Favorit</button>
      <button id="fact-clear" class="btn">🗑️ Favoriten leeren</button>
    </div>
    <div id="fact-box" class="card" style="margin-top:10px">Klick auf „Neuen Fun Fact“ 🙂</div>

    <h3 style="margin-top:16px">⭐ Favoriten</h3>
    <div id="fact-favs" class="grid-2"></div>
  </div>
</section>
"""

FUN_JS = r"""
<script>
const FUN_FACTS = [
  "Kühe haben beste Freunde und werden gestresst, wenn man sie trennt. 🐮❤️",
  "Seesterne haben kein Gehirn – und trotzdem mehr Urlaubsfotos als wir.",
  "Schnecken haben über 14.000 Zähne. Stell dir die Zahnarztrechnung vor.",
  "Raben merken sich Gesichter. Sei nett – sie haben gutes Gedächtnis.",
  "Pinguine machen Heiratsanträge mit Kieselsteinen. 💍🐧",
  "Die Erdnuss ist keine Nuss. Die Erdbeere keine Beere. Trau niemandem.",
  "Koalas schlafen bis zu 22 Stunden am Tag. Produktivität optional.",
  "Faultiere können beim Klettern einschlafen. Relatable.",
  "Eine Wolke kann über eine Million Kilo wiegen – Gains.",
  "In Norwegen gibt es einen Pinguin mit Offiziersrang.",
  "Tintenfische schmecken mit den Armen. Handschuhe empfohlen.",
  "Bananen sind leicht radioaktiv. Superkräfte leider nicht inklusive.",
  "Katzen haben über 20 Ohrmuskeln. Um dich besser zu ignorieren.",
];
const favKey='fun_favs_v1';
function getFavs(){ try{return JSON.parse(localStorage.getItem(favKey)||'[]')}catch(e){return[]} }
function setFavs(a){ localStorage.setItem(favKey, JSON.stringify(a.slice(0,50))); }
function renderFavs(){
  const box=document.getElementById('fact-favs'); if(!box) return;
  box.innerHTML='';
  getFavs().forEach(f=>{ const d=document.createElement('div'); d.className='card'; d.textContent=f; box.appendChild(d); });
}
function newFact(){
  const f = FUN_FACTS[Math.floor(Math.random()*FUN_FACTS.length)];
  const fb=document.getElementById('fact-box'); if(fb) fb.textContent=f;
}
document.getElementById('fact-new')?.addEventListener('click', newFact);
document.getElementById('fact-copy')?.addEventListener('click', async ()=>{
  const t=document.getElementById('fact-box')?.textContent||''; if(!t) return;
  try{ await navigator.clipboard.writeText(t); }catch(e){}
});
document.getElementById('fact-fav')?.addEventListener('click', ()=>{
  const t=document.getElementById('fact-box')?.textContent.trim(); if(!t) return;
  const a=getFavs(); if(!a.includes(t)){ a.unshift(t); setFavs(a); renderFavs(); }
});
document.getElementById('fact-clear')?.addEventListener('click', ()=>{
  localStorage.removeItem(favKey); renderFavs();
});
renderFavs(); newFact();
</script>
"""

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

CASINO = r"""
<section id="casino" class="section">
  <h2 class="title">🎰 Casino</h2>

  <div class="card" style="margin-bottom:16px">
    <div class="row" style="width:100%">
      <div>Guthaben: <b><span id="balance2">0</span> A$</b></div>
      <span class="sp"></span>
      <input id="code" placeholder="Gutschein-Code" style="flex:1;min-width:180px">
      <button class="btn" id="redeem">Einlösen</button>
      <div id="redeem-msg" class="msg muted" style="flex:1"></div>
    </div>
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
          <!-- Labels kommen per JS -->
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
/* Tabs umschalten */
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
  function renderHands(){
    // Spieler
    elPlayer.innerHTML = player.map(c=>renderCard(c,false)).join('');
    elPT.textContent = total(player);
    // Dealer
    if(dealerHidden){
      elDealer.innerHTML = renderCard(dealer[0],true) + dealer.slice(1).map(c=>renderCard(c,false)).join('');
      elDT.textContent = '–';
    }else{
      elDealer.innerHTML = dealer.map(c=>renderCard(c,false)).join('');
      elDT.textContent = total(dealer);
    }
  }
  function setUI(active){ btnHit.disabled=!active; btnStand.disabled=!active; }
  function canBet(){ const b=Number(betInput.value||0); return b>=1 && b<=getBalance(); }

  function startRound(){
    if(!canBet()){ msg.textContent='Nicht genug Guthaben oder ungültiger Einsatz.'; return; }
    const b=Number(betInput.value); setBalance(getBalance()-b);
    msg.textContent=''; inRound=true; dealerHidden=true;

    if(deck.length<40) deck=newDeck();
    dealer=[deck.pop(),deck.pop()];
    player=[deck.pop(),deck.pop()];
    setUI(true);
    renderHands();

    // Sofortige Blackjacks prüfen
    const pt=total(player), dt=total(dealer);
    if(pt===21 || dt===21){
      dealerHidden=false;
      renderHands();
      if(pt===21 && dt===21){ msg.textContent='Beide Blackjack – Push.'; setBalance(getBalance()+b); }
      else if(pt===21){ const win=Math.floor(b*1.5); msg.textContent=`Blackjack! Gewinn: ${win} A$`; setBalance(getBalance()+b+win); }
      else { msg.textContent='Dealer hat Blackjack – verloren.'; }
      inRound=false; setUI(false);
    }
  }

  function dealerPlay(){
    dealerHidden=false; renderHands();
    while(total(dealer)<17){ dealer.push(deck.pop()); renderHands(); }
  }
  function finishRound(){
    const b=Number(betInput.value);
    const p=total(player), d=total(dealer);
    if(p>21){ msg.textContent='Bust! Verloren.'; inRound=false; setUI(false); return; }
    if(d>21){ msg.textContent='Dealer bust – du gewinnst!'; setBalance(getBalance()+b*2); inRound=false; setUI(false); return; }
    if(p>d){ msg.textContent='Du gewinnst!'; setBalance(getBalance()+b*2); }
    else if(p<d){ msg.textContent='Verloren.'; }
    else { msg.textContent='Push – Einsatz zurück.'; setBalance(getBalance()+b); }
    inRound=false; setUI(false);
  }

  btnDeal?.addEventListener('click', ()=>{ if(inRound)return; startRound(); });
  btnHit?.addEventListener('click', ()=>{
    if(!inRound)return;
    player.push(deck.pop()); renderHands();
    if(total(player)>21){ dealerHidden=false; renderHands(); msg.textContent='Bust! Verloren.'; inRound=false; setUI(false); }
  });
  btnStand?.addEventListener('click', ()=>{
    if(!inRound)return;
    dealerPlay(); finishRound();
  });

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

  // Zahl-Labels erzeugen (0–36)
  function buildLabels(){
    [...wheelEl.querySelectorAll('.wheel-label')].forEach(n=>n.remove());
    const total=37, step=360/total;
    for(let i=0;i<total;i++){
      const lab=document.createElement('div');
      lab.className='wheel-label';
      const ang=i*step;
      lab.style.transform=`rotate(${ang}deg)`;
      lab.style.setProperty('--r-rev', `${-ang}deg`);
      const span=document.createElement('span');
      span.textContent=String(i);
      if(i===0){ lab.classList.add('green'); }
      else if(redNums.has(i)){ lab.classList.add('red'); }
      else { lab.classList.add('black'); }
      lab.appendChild(span);
      wheelEl.appendChild(lab);
    }
  }
  buildLabels();

  typeSel?.addEventListener('change',()=>{ numWrap.style.display=(typeSel.value==='single')?'inline-block':'none'; });

  function canBet(){ const b=Number(betInp.value||0); return b>=1 && b<=getBalance(); }

  let currentWheel=0, currentBall=0;
  const step=360/37;
  const ballRadius=130;

  function setTransforms(wDeg, bDeg){
    wheelEl.style.transform = `rotate(${wDeg}deg)`;
    ballEl.style.transform  = `rotate(${bDeg}deg) translateX(${ballRadius}px)`;
  }
  setTransforms(0,0);

  function spin(){
    if(!canBet()){ msg.textContent='Nicht genug Guthaben oder ungültiger Einsatz.'; return; }
    msg.textContent=''; const bet=Number(betInp.value); setBalance(getBalance()-bet);

    const target=Math.floor(Math.random()*37);
    // Wir richten am Ende so aus, dass der Pointer (oben) GENAU auf der Zielzahl steht.
    const baseTurns=360*6;  // volle Drehungen fürs Feeling
    const targetAngle = (360 - target*step); // Ziel unter dem Pointer (0deg)
    const finalWheel = currentWheel + baseTurns + targetAngle;
    const finalBall  = currentBall  - (baseTurns*1.4); // gegenläufig

    wheelEl.style.transition='transform 3.2s cubic-bezier(.22,.61,.36,1)';
    ballEl .style.transition='transform 3.2s cubic-bezier(.22,.61,.36,1)';
    setTransforms(finalWheel, finalBall);

    setTimeout(()=>{
      // Ergebnis anzeigen
      resEl.textContent=String(target);
      const c=color(target); colEl.textContent=c;

      const t=typeSel.value; let win=0;
      if(t==='single'){ const n=Number(numInp.value); if(n===target) win=bet*35; }
      else if(t==='red' && c==='rot') win=bet;
      else if(t==='black' && c==='schwarz') win=bet;
      else if(t==='even' && target!==0 && target%2===0) win=bet;
      else if(t==='odd' && target%2===1) win=bet;
      else if(t==='dozen1' && target>=1 && target<=12) win=bet*3;
      else if(t==='dozen2' && target>=13 && target<=24) win=bet*3;
      else if(t==='dozen3' && target>=25 && target<=36) win=bet*3;

      if(win>0){ setBalance(getBalance()+bet+win); msg.textContent=`Gewonnen: +${win} A$`; }
      else{ msg.textContent='Leider verloren.'; }

      // Sauberer Reset: Winkel normieren und ohne Transition setzen
      setTimeout(()=>{
        currentWheel = (finalWheel % 360 + 360) % 360;
        currentBall  = (finalBall  % 360 + 360) % 360;
        wheelEl.style.transition='none'; ballEl.style.transition='none';
        // Kugel genau zum Pointer (oben) – leicht versetzt, damit sie sichtbar vor dem Label liegt
        currentBall = 0;
        setTransforms(currentWheel, currentBall);
        void wheelEl.offsetWidth; void ballEl.offsetWidth; // reflow
      }, 100);
    }, 3300);
  }
  spinBtn?.addEventListener('click', spin);

  document.getElementById('balance2').textContent = getBalance();
  document.getElementById('redeem')?.addEventListener('click', redeem);
})();
</script>
"""

# ========================= Render helper =========================
def render_page(title, content_html, page_js=""):
    return render_template_string(BASE, title=title, content=content_html, page_js=page_js)

# ========================= Routes =========================
@app.route("/")
def home():
    return render_page("Start · Aaron", HOME, "")

@app.route("/fun")
def fun():
    return render_page("Fun Facts · Aaron", FUN, FUN_JS)

@app.route("/tictactoe")
def tictactoe():
    return render_page("Tic-Tac-Toe · Aaron", TTT, TTT_JS)

@app.route("/casino")
def casino():
    return render_page("Casino · Aaron", CASINO, CASINO_JS)

if __name__ == "__main__":
    app.run(debug=True)
