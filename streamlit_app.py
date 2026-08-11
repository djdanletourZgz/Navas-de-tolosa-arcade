import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Navas de Tolosa Arcade", page_icon="⚔️", layout="wide")
st.markdown("""
<style>
html, body, [data-testid='stAppViewContainer'] { background:#0d0b09; margin:0; overflow:hidden; }
.block-container { padding:0 !important; max-width:100% !important; }
header, footer { display:none !important; }
iframe { border:0 !important; display:block; margin:0 auto; }
</style>
""", unsafe_allow_html=True)

html = Path("game/index.html").read_text(encoding="utf-8")

responsive_ui = r"""
<style>
html,body{width:100%;height:100%;margin:0!important;overflow:hidden!important;background:#0b0907!important}
#w{width:100%!important;height:100vh!important;max-width:none!important;padding:0!important;position:relative!important;overflow:hidden!important;display:flex!important;align-items:center!important;justify-content:center!important}
#box{width:min(100vw,860px)!important;height:auto!important;aspect-ratio:15/11!important;margin:0 auto!important;border:0!important;box-shadow:none!important;position:relative!important}
canvas{width:100%!important;height:100%!important;object-fit:contain!important}
#hud{position:absolute!important;z-index:30!important;top:6px!important;left:50%!important;transform:translateX(-50%)!important;width:min(97vw,830px)!important;padding:5px!important;border:1px solid rgba(222,181,95,.65)!important;border-radius:12px!important;background:rgba(24,18,13,.80)!important;backdrop-filter:blur(6px)!important;font-size:10px!important;gap:3px!important}
#hud .b{border:0!important;border-radius:7px!important;background:rgba(76,57,37,.74)!important;padding:4px 5px!important}
#mob{position:absolute!important;z-index:35!important;left:0!important;bottom:8px!important;width:100%!important;padding:0 10px!important;margin:0!important;display:flex!important;align-items:flex-end!important;justify-content:space-between!important;pointer-events:none!important}
#pad,#fire{pointer-events:auto!important}
#pad{display:grid!important;grid-template-columns:72px 72px 72px!important;grid-template-rows:59px 59px!important;gap:5px!important;filter:drop-shadow(0 5px 8px rgba(0,0,0,.45))}
.ctrl{min-width:72px!important;min-height:59px!important;font-size:30px!important;border:2px solid rgba(231,189,99,.9)!important;border-radius:15px!important;background:rgba(31,25,20,.88)!important;box-shadow:0 4px 0 rgba(0,0,0,.55)!important}
#fire{width:142px!important;height:120px!important;border-radius:26px!important;font-size:18px!important;border:3px solid #d8a540!important;background:linear-gradient(180deg,rgba(154,55,42,.96),rgba(91,27,21,.97))!important;box-shadow:0 6px 0 rgba(0,0,0,.55)!important}
#hint{display:none!important}
.storyOverlay{position:absolute;inset:0;z-index:90;background:linear-gradient(rgba(9,7,5,.96),rgba(25,17,10,.97));display:flex;align-items:center;justify-content:center;padding:14px;color:#f8e7b6;text-align:center}
.storyCard{width:min(92%,650px);max-height:94%;overflow:auto;background:rgba(39,27,18,.98);border:2px solid #c59a43;border-radius:18px;padding:18px;box-shadow:0 14px 40px #000}
.storyCard h1,.storyCard h2{color:#f1c24d;margin:5px 0 10px}.storyCard p{line-height:1.4;margin:8px 0}.storyCard button{margin-top:12px;padding:11px 18px;border:2px solid #d8a540;border-radius:11px;background:#7d2b22;color:#fff0c2;font:900 16px monospace}
.weaponIcon{font-size:50px;line-height:1;margin:2px 0 8px}.weaponStat{display:inline-block;margin:3px;padding:5px 8px;border-radius:8px;background:#4b3825;color:#ffe6a0;font-weight:900}
#bossPortrait{width:min(62vw,260px);height:auto;image-rendering:pixelated;border:2px solid #76552e;border-radius:12px;background:#140d08;margin:7px auto;display:block}
@media(max-width:650px){#box{width:100vw!important;aspect-ratio:15/11!important}#hud{top:3px!important;width:99vw!important;font-size:9px!important;padding:3px!important}#mob{bottom:5px!important;padding:0 7px!important}#pad{grid-template-columns:68px 68px 68px!important;grid-template-rows:56px 56px!important;gap:4px!important}.ctrl{min-width:68px!important;min-height:56px!important;font-size:29px!important}#fire{width:130px!important;height:112px!important;font-size:17px!important}.storyCard{padding:14px;font-size:12px}.storyCard h1{font-size:23px}.storyCard h2{font-size:19px}}
</style>
"""

game_patch = r"""
<script>
(() => {
  let paused=false,pauseStarted=0,longUnlocked=false,ristras=0,longPick=null,charging=false,chargeStart=0,thrown=[];
  const shownLevels=new Set(),shownWeapons=new Set();
  const tileIn=(cells,e)=>!!e&&!!cells&&cells.some(c=>c.x===e.x&&c.y===e.y);
  const baseLevel=level,baseUpdate=update,baseDrawWorld=drawWorld,baseTouch=touch,baseFire=fire,baseDamage=damageCells,baseBlast=blast,baseHud=hud;

  const HIST=[
    {year:'1086',place:'Sagrajas / az-Zallaqa',boss:'MEHMET',lines:['Alfonso VI había extendido su poder sobre Toledo y presionaba a las taifas peninsulares.','Varios gobernantes andalusíes pidieron ayuda al emir almorávide Yusuf ibn Tashfin, llegado desde el norte de África.','Los ejércitos se encontraron cerca de Badajoz en 1086.','La batalla terminó con una dura derrota de las fuerzas cristianas y frenó temporalmente la expansión castellano-leonesa.','Nuestra campaña convierte aquel choque histórico en la primera prueba de esta crónica fantástica.']},
    {year:'1108',place:'Uclés',boss:'AMIR',lines:['En 1108, las fuerzas almorávides avanzaron sobre Uclés, una posición estratégica de la frontera castellana.','El ejército cristiano acudió para responder a la ofensiva.','En la batalla murió Sancho Alfónsez, único hijo varón de Alfonso VI.','La derrota tuvo consecuencias políticas profundas para la sucesión del reino.','En esta fase, la noche y el candil recuerdan la incertidumbre de una frontera siempre amenazada.']},
    {year:'1195',place:'Alarcos',boss:'MOHAMED',lines:['Alfonso VIII de Castilla se enfrentó en 1195 al ejército almohade dirigido por Yaqub al-Mansur.','El choque tuvo lugar cerca de Alarcos, junto al Guadiana.','La caballería castellana atacó con fuerza, pero el ejército almohade resistió y contraatacó.','La derrota cristiana alteró durante años el equilibrio militar de la Meseta Sur.','Aquella herida sería uno de los antecedentes directos de la gran campaña de 1212.']},
    {year:'1212',place:'Las Navas de Tolosa',boss:'HASSAN',lines:['En 1212 una coalición encabezada por Alfonso VIII de Castilla, Pedro II de Aragón y Sancho VII de Navarra marchó hacia el sur.','Frente a ellos estaba el gran ejército almohade del califa Muhammad al-Nasir.','Tras atravesar Sierra Morena, ambos bandos chocaron en Las Navas de Tolosa.','La victoria de la coalición cristiana debilitó decisivamente el poder almohade en la península.','Es el corazón histórico de nuestra aventura y el duelo que da nombre al juego.']},
    {year:'1340',place:'Río Salado',boss:'AHMED',lines:['En 1340, una nueva gran ofensiva norteafricana llegó a la península bajo los benimerines, aliados con Granada.','Alfonso XI de Castilla y Afonso IV de Portugal reunieron fuerzas para detenerla.','Los ejércitos se enfrentaron cerca del río Salado, junto al Estrecho.','La victoria cristiana limitó las grandes intervenciones militares norteafricanas en la península durante las décadas siguientes.','Aquí termina nuestro viaje legendario a través de más de dos siglos de combates fronterizos.']}
  ];

  const WEAPONS={
    cross:{icon:'✝️',title:'CRUCIFIJO',body:'Tu arma inicial. Déjalo en el suelo y aléjate antes de que estalle. Su fogonazo avanza una casilla en cada dirección y permanece peligroso mientras siga visible.',stats:['ALCANCE: 1','ACTIVOS: 1','MECHA: 1,5 s']},
    torrezno:{icon:'🥓',title:'TORREZNO',body:'Más contundente que el crucifijo. El fuego alcanza dos casillas en cada dirección. Sigue siendo una sola carga activa, así que coloca y muévete.',stats:['ALCANCE: 2','ACTIVOS: 1','MÁS POTENCIA']},
    soria:{icon:'🥓🥓',title:'TORREZNO DE SORIA',body:'La evolución definitiva del torrezno. Puedes mantener dos cargas activas a la vez. Si sus fogonazos se encuentran, provocan una EXPLOSIÓN SAGRADA que extiende el fuego.',stats:['ALCANCE: 2','ACTIVOS: 2','EXPLOSIÓN SAGRADA']},
    long:{icon:'🌭',title:'LONGANIZA DE FUENTES',body:'Arma arrojadiza. Mantén PEPINAZO pulsado aproximadamente un segundo y suelta: la ristra vuela hasta cuatro casillas y explota con alcance de dos casillas por lado. Cada enemigo eliminado te concede una ristra nueva y la munición se conserva entre fases.',stats:['VUELO: 4','EXPLOSIÓN: 2','MANTENER 1 s']}
  };

  const hudNode=document.getElementById('hud'),ammo=document.createElement('span');ammo.className='b';ammo.id='ristras';hudNode.insertBefore(ammo,document.getElementById('sc'));
  function hudExtra(){ammo.textContent=longUnlocked?`🌭 ${ristras}`:'🌭 —';}
  hud=function(){baseHud();hudExtra();};

  function shiftTime(ms){
    if(!ms||ms<1)return;
    if(p){p.next=(p.next||0)+ms;}
    if(boss){for(const k of ['next','nextSpecial','nextTele','nextElite','sprintAt','sprintUntil','restUntil'])if(boss[k])boss[k]+=ms;}
    for(const e of enemies)if(e.next)e.next+=ms;
    if(elite&&elite.next)elite.next+=ms;
    for(const s of sappers){if(s.next)s.next+=ms;if(s.fuse)s.fuse+=ms;if(s.explodeUntil)s.explodeUntil+=ms;}
    for(const b of bombs){if(b.boom)b.boom+=ms;if(b.until)b.until+=ms;}
    for(const r of thrown){if(r.start)r.start+=ms;if(r.land)r.land+=ms;if(r.until)r.until+=ms;}
    if(darkUntil)darkUntil+=ms;if(nextDark)nextDark+=ms;
  }
  function pauseGame(){if(!paused){paused=true;pauseStarted=performance.now();}}
  function resumeGame(){if(!paused)return;const now=performance.now();shiftTime(now-pauseStarted);paused=false;last=now;}

  function portrait(canvas,idx){const c=canvas.getContext('2d'),cols=['#68422f','#6c2f37','#4d6330','#7a4b26','#3c536d'];c.clearRect(0,0,240,180);c.fillStyle='#130c08';c.fillRect(0,0,240,180);c.fillStyle=cols[idx];c.fillRect(55,68,130,82);c.fillStyle='#c99569';c.beginPath();c.arc(120,70,50,0,7);c.fill();c.fillStyle='#eee0b9';c.fillRect(63,34,114,25);c.fillRect(78,21,84,19);c.fillStyle='#20130e';c.fillRect(82,66,18,10);c.fillRect(140,66,18,10);c.fillRect(92,96,56,7);c.fillStyle='#fff1cf';c.fillRect(99,97,12,5);c.fillRect(129,97,12,5);c.fillStyle='#3b2418';c.fillRect(88,118,64,25);c.fillStyle='#d0a53b';c.fillRect(48,147,144,9);c.fillStyle='#f1c24d';c.font='bold 17px monospace';c.textAlign='center';c.fillText(HIST[idx].boss,120,173);}

  function overlay(html,buttonText,onClose,idx=null){pauseGame();const o=document.createElement('div');o.className='storyOverlay';o.innerHTML=`<div class="storyCard">${html}<button class="storyGo">${buttonText}</button></div>`;document.getElementById('box').appendChild(o);if(idx!==null){const pc=o.querySelector('#bossPortrait');if(pc)portrait(pc,idx);}o.querySelector('.storyGo').onclick=()=>{o.remove();resumeGame();if(onClose)onClose();};}

  function weaponTutorial(type){if(shownWeapons.has(type))return;shownWeapons.add(type);const w=WEAPONS[type],stats=w.stats.map(s=>`<span class="weaponStat">${s}</span>`).join('');overlay(`<div class="weaponIcon">${w.icon}</div><h2>¡${w.title}!</h2><p>${w.body}</p><div>${stats}</div>`,'¡ENTENDIDO!');}

  function battleIntro(idx){const h=HIST[idx],paras=h.lines.map(x=>`<p>${x}</p>`).join('');overlay(`<div style="font-size:12px;color:#bda36d">AÑO ${h.year}</div><h2>${h.place}</h2>${paras}<canvas id="bossPortrait" width="240" height="180"></canvas><h2 style="color:#ff9b55">TE ESPERA ${h.boss}</h2><p><b>El malo malísimo ya se ríe. Haz que deje de hacerlo.</b></p>`,'¡A LA BATALLA!',()=>{if(idx===0)weaponTutorial('cross');},idx);}

  function chooseLong(){if(longUnlocked){longPick=null;return;}const a=[];for(let y=1;y<R-1;y++)for(let x=1;x<C-1;x++)if(g[y][x]===2&&!picks.some(pk=>pk.x===x&&pk.y===y))a.push({x,y});if(a.length)longPick={...a[Math.floor(Math.random()*a.length)],hidden:true,taken:false,t:0};}
  level=function(){baseLevel();chooseLong();hudExtra();if(!shownLevels.has(L)){shownLevels.add(L);battleIntro(L-1);}};

  function unlockLong(){if(longUnlocked)return;longUnlocked=true;ristras+=2;hudExtra();weaponTutorial('long');}

  damageCells=function(cells,allow=true){
    const before=enemies.filter(e=>e.alive).length+(elite&&elite.alive?1:0)+sappers.filter(s=>s.alive).length;
    baseDamage(cells,allow);
    const after=enemies.filter(e=>e.alive).length+(elite&&elite.alive?1:0)+sappers.filter(s=>s.alive).length;
    if(longUnlocked&&before>after){ristras+=before-after;hudExtra();}
    if(longPick&&longPick.hidden&&cells.some(c=>c.x===longPick.x&&c.y===longPick.y)&&g[longPick.y][longPick.x]===0){longPick.hidden=false;say('¡ALGO HUELE A FUENTES!','#ffd95c',650);}
  };

  touch=function(){
    if(longPick&&!longPick.hidden&&!longPick.taken&&p.x===longPick.x&&p.y===longPick.y){longPick.taken=true;unlockLong();}
    const before=weapon;
    baseTouch();
    if(weapon!==before){if(weapon===1)weaponTutorial('torrezno');else if(weapon===2)weaponTutorial('soria');}
  };

  function dir(){const d=p.dir||p.lastDir||'down';return d==='left'?[-1,0]:d==='right'?[1,0]:d==='up'?[0,-1]:[0,1];}
  function throwLong(){if(!longUnlocked||ristras<=0||paused||over||trans)return;ristras--;hudExtra();const[dx,dy]=dir();let tx=p.x,ty=p.y;for(let i=0;i<4;i++){const nx=tx+dx,ny=ty+dy;if(nx<=0||ny<=0||nx>=C-1||ny>=R-1||g[ny][nx]===1||g[ny][nx]===3)break;tx=nx;ty=ny;}const n=performance.now();thrown.push({sx:p.x,sy:p.y,x:tx,y:ty,px:p.px,py:p.py,start:n,land:n+420,cells:null,until:0});say('¡LONGANIZA VOLADORA!','#ffcf61',420);}
  function beginCharge(){if(paused||charging||over||trans)return;charging=true;chargeStart=performance.now();document.getElementById('fire').textContent=longUnlocked&&ristras>0?'🌭 CARGANDO…':'💥 PEPINAZO';}
  function release(){if(!charging)return;const held=performance.now()-chargeStart;charging=false;document.getElementById('fire').innerHTML='💥<br>PEPINAZO';if(held>=950&&longUnlocked&&ristras>0)throwLong();else baseFire();}
  fire=beginCharge;
  addEventListener('keyup',e=>{if(e.key===' ')release();});
  const fb=document.getElementById('fire');fb.onclick=null;fb.addEventListener('pointerdown',e=>{e.preventDefault();beginCharge();});fb.addEventListener('pointerup',e=>{e.preventDefault();release();});fb.addEventListener('pointercancel',release);fb.addEventListener('pointerleave',()=>{if(charging)release();});

  blast=function(b){const pre=traceBlast(b),hit=boss&&boss.alive&&duel&&tileIn(pre,boss);baseBlast(b);b._bossHazardHit=hit;};
  function lingering(now){let kills=0;for(const b of bombs){if(!b.ex||now>=b.until)continue;const cells=b.sacredCells?b.cells.concat(b.sacredCells):b.cells;for(const e of enemies)if(e.alive&&tileIn(cells,e)){e.alive=false;score+=200;kills++;}if(elite&&elite.alive&&tileIn(cells,elite)){elite.alive=false;score+=500;kills++;}for(const s of sappers)if(s.alive&&tileIn(cells,s)){s.alive=false;score+=120;leaveBlood(s.x,s.y);kills++;}if(p&&tileIn(cells,p))hurt();if(boss.alive&&duel&&!b._bossHazardHit&&tileIn(cells,boss)){b._bossHazardHit=true;boss.hp--;score+=350;if(boss.hp<=0){boss.alive=false;score+=1000;say('¡'+BOSSES[L-1].name+' REVENTADO!','#ff8c42',700);setTimeout(win,720);}else say(`¡PEPINAZO! ${boss.hp} ♥`,'#ff8c42',580);}}
    if(kills&&longUnlocked){ristras+=kills;hudExtra();}if(kills){hud();checkDuel();}
  }

  update=function(dt,now){if(paused)return;baseUpdate(dt,now);lingering(now);for(const r of thrown){if(!r.cells){const t=Math.min(1,(now-r.start)/(r.land-r.start));r.px=tcx(r.sx)+(tcx(r.x)-tcx(r.sx))*t;r.py=tcy(r.sy)+(tcy(r.y)-tcy(r.sy))*t-Math.sin(Math.PI*t)*TH*.7;if(t>=1){r.cells=traceBlast({x:r.x,y:r.y,range:2});r.until=now+520;damageCells(r.cells,true);}}}thrown=thrown.filter(r=>!r.cells||now<r.until);if(longPick&&!longPick.hidden&&!longPick.taken)longPick.t+=dt*.004;};

  function drawLong(cx,cy,s=1,a=0){ctx.save();ctx.translate(cx,cy);ctx.rotate(a);ctx.strokeStyle='#ead39b';ctx.lineWidth=3*s;ctx.beginPath();ctx.moveTo(-37*s,0);ctx.lineTo(37*s,0);ctx.stroke();ctx.fillStyle='#c96534';for(let i=-2;i<=2;i++){ctx.beginPath();ctx.ellipse(i*14*s,0,10*s,7*s,0,0,7);ctx.fill();}ctx.restore();}
  drawWorld=function(now){baseDrawWorld(now);if(longPick&&!longPick.hidden&&!longPick.taken)drawLong(tcx(longPick.x),tcy(longPick.y)+Math.sin(longPick.t)*4,1,0);for(const r of thrown){if(!r.cells)drawLong(r.px,r.py,.9,(now-r.start)/90);else for(const c of r.cells){ctx.fillStyle='#fff0a7';ctx.fillRect(c.x*TW+7,c.y*TH+7,TW-14,TH-14);ctx.fillStyle='#ff7b32';ctx.fillRect(c.x*TW+TW*.22,c.y*TH+TH*.22,TW*.56,TH*.56);}}};

  lantern=function(side=1){const f=1+Math.sin(performance.now()/70)*.08;ctx.save();ctx.translate(35*side,3);ctx.scale(side,1);ctx.strokeStyle='#8a5a28';ctx.lineWidth=4;ctx.beginPath();ctx.arc(0,-13,11,Math.PI,0);ctx.stroke();ctx.fillStyle='#5c371a';ctx.fillRect(-4,-14,8,22);ctx.fillStyle='#9b682c';ctx.fillRect(-12,5,24,6);ctx.fillRect(-13,29,26,6);ctx.fillStyle='#e5b75b';ctx.fillRect(-10,10,20,19);ctx.fillStyle='#fff0a0';ctx.fillRect(-6,12,12,15);ctx.fillStyle='#ffb52f';ctx.beginPath();ctx.ellipse(0,19,5*f,8*f,0,0,7);ctx.fill();ctx.restore();};
  drawLightOverlay=function(){if(!(darkMode||L===2))return;const rad=TW*6;ctx.save();const g=ctx.createRadialGradient(p.px,p.py,0,p.px,p.py,rad);g.addColorStop(0,'rgba(0,0,0,.20)');g.addColorStop(.78,'rgba(0,0,0,.20)');g.addColorStop(1,'rgba(0,0,0,.90)');ctx.fillStyle=g;ctx.fillRect(-cv.width,-cv.height,cv.width*3,cv.height*3);ctx.restore();ctx.save();ctx.globalCompositeOperation='screen';const glow=ctx.createRadialGradient(p.px,p.py,0,p.px,p.py,TW*2.4);glow.addColorStop(0,'rgba(255,205,82,.25)');glow.addColorStop(1,'rgba(255,170,40,0)');ctx.fillStyle=glow;ctx.beginPath();ctx.arc(p.px,p.py,TW*2.4,0,7);ctx.fill();ctx.restore();};

  // Corrige el patrón de Amir: 2 s de sprint y después 1 s inmóvil.
  updateAmir=function(now){if(L!==2||!boss.alive||!duel)return 1;if(now<boss.sprintUntil)return .42;if(now<boss.restUntil)return 0;if(now>=boss.sprintAt){boss.sprintUntil=now+2000;boss.restUntil=now+3000;boss.sprintAt=now+3000+rnd(4000,6000);say('¡AMIR SPRINT!','#ffb657',450);return .42;}return 1;};

  const start=document.getElementById('start');start.innerHTML=`<div class="card"><h1>NAVAS DE TOLOSA</h1><h2>CRÓNICA DEL REY</h2><p>En esta crónica fantástica, un rey cristiano atraviesa cinco batallas separadas por generaciones.</p><p>Su juramento es abrir camino allí donde los ejércitos chocan y la frontera cambia de manos.</p><p>Porta un crucifijo como símbolo de su causa y descubre por el camino el poder improbable de los torreznos y otras armas legendarias.</p><p>Entre polvo, agua, noche y acero, cada victoria lo acerca al siguiente malo malísimo.</p><p><b>La historia inspira el viaje; el disparate arcade hace el resto.</b></p><button id="play">COMENZAR LA CRÓNICA</button></div>`;
  document.getElementById('play').onclick=()=>{start.style.display='none';L=1;score=0;shownLevels.clear();shownWeapons.clear();longUnlocked=false;ristras=0;longPick=null;thrown=[];level();last=performance.now();requestAnimationFrame(loop);};
  hudExtra();
})();
</script>
"""

html = html.replace("</head>", responsive_ui + "\n</head>")
html = html.replace("</body>", game_patch + "\n</body>")
st.components.v1.html(html, height=590, scrolling=False)
