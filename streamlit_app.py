import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Navas de Tolosa Arcade", page_icon="⚔️", layout="wide")
st.markdown("""
<style>
html, body, [data-testid='stAppViewContainer'] {
    background:#0d0b09;
    margin:0;
    overflow:hidden;
}
.block-container {
    padding:0 !important;
    max-width:100% !important;
}
header, footer { display:none !important; }
iframe { border:0 !important; display:block; margin:0 auto; }
</style>
""", unsafe_allow_html=True)

html = Path("game/index.html").read_text(encoding="utf-8")

responsive_ui = r"""
<style>
html,body{width:100%;height:100%;margin:0!important;overflow:hidden!important;background:#0b0907!important;}
#w{width:100%!important;height:100vh!important;max-width:none!important;padding:0!important;position:relative!important;overflow:hidden!important;display:flex!important;align-items:center!important;justify-content:center!important;}
#box{width:min(100vw,860px)!important;height:auto!important;aspect-ratio:15/11!important;margin:0 auto!important;border:0!important;box-shadow:none!important;position:relative!important;}
canvas{width:100%!important;height:100%!important;object-fit:contain!important;}
#hud{position:absolute!important;z-index:30!important;top:8px!important;left:50%!important;transform:translateX(-50%)!important;width:min(96vw,820px)!important;padding:5px 7px!important;border:1px solid rgba(222,181,95,.65)!important;border-radius:12px!important;background:rgba(24,18,13,.78)!important;backdrop-filter:blur(6px)!important;box-shadow:0 4px 16px rgba(0,0,0,.35)!important;font-size:11px!important;gap:4px!important;}
#hud .b{border:0!important;border-radius:8px!important;background:rgba(76,57,37,.72)!important;padding:4px 6px!important;}
#mob{position:absolute!important;z-index:35!important;left:0!important;bottom:10px!important;width:100%!important;padding:0 12px!important;margin:0!important;display:flex!important;align-items:flex-end!important;justify-content:space-between!important;pointer-events:none!important;}
#pad,#fire{pointer-events:auto!important;}
#pad{display:grid!important;grid-template-columns:76px 76px 76px!important;grid-template-rows:62px 62px!important;gap:6px!important;filter:drop-shadow(0 5px 8px rgba(0,0,0,.45));}
.ctrl{min-width:76px!important;min-height:62px!important;font-size:31px!important;border:2px solid rgba(231,189,99,.9)!important;border-radius:16px!important;background:rgba(31,25,20,.86)!important;box-shadow:0 4px 0 rgba(0,0,0,.55)!important;}
#fire{width:150px!important;height:126px!important;border-radius:28px!important;font-size:19px!important;border:3px solid #d8a540!important;background:linear-gradient(180deg,rgba(154,55,42,.94),rgba(91,27,21,.96))!important;box-shadow:0 6px 0 rgba(0,0,0,.55),0 0 20px rgba(216,165,64,.15)!important;}
#hint{display:none!important;}#start{border-radius:0!important;}.card{border-radius:18px!important;max-width:min(88vw,560px)!important;}
@media(max-width:650px){#box{width:100vw!important;aspect-ratio:15/11!important;}#hud{top:4px!important;width:98vw!important;font-size:9.5px!important;padding:4px!important;}#mob{bottom:7px!important;padding:0 8px!important;}#pad{grid-template-columns:70px 70px 70px!important;grid-template-rows:58px 58px!important;gap:5px!important;}.ctrl{min-width:70px!important;min-height:58px!important;font-size:29px!important;}#fire{width:132px!important;height:116px!important;font-size:17px!important;}}
@media(max-width:390px){#pad{grid-template-columns:64px 64px 64px!important;grid-template-rows:54px 54px!important;}.ctrl{min-width:64px!important;min-height:54px!important;}#fire{width:118px!important;height:108px!important;}}
</style>
"""

gameplay_patch = r"""
<script>
(() => {
  let longanizaUnlocked=false,ristras=0,longPick=null,tutorialPaused=false,chargeStart=0,charging=false,thrownRistras=[];
  const tileIn=(cells,entity)=>!!entity&&!!cells&&cells.some(c=>c.x===entity.x&&c.y===entity.y);
  const oldHud=hud,oldLevel=level,oldTouch=touch,oldUpdate=update,oldDrawWorld=drawWorld,oldBlast=blast,baseFire=fire,baseDamageCells=damageCells;

  const hudNode=document.getElementById('hud'),ammoBadge=document.createElement('span');
  ammoBadge.className='b';ammoBadge.id='ristras';hudNode.insertBefore(ammoBadge,document.getElementById('sc'));
  function updateRistraHud(){ammoBadge.textContent=longanizaUnlocked?`🌭 ${ristras}`:'🌭 —';ammoBadge.title='Ristras de Longaniza de Fuentes';}
  hud=function(){oldHud();updateRistraHud();};

  const tutorial=document.createElement('div');tutorial.id='longTutorial';tutorial.style.cssText='display:none;position:absolute;inset:0;z-index:80;background:rgba(8,6,4,.92);align-items:center;justify-content:center;padding:18px;text-align:center;';
  tutorial.innerHTML=`<div style="max-width:560px;background:#25170e;border:3px solid #d8a540;border-radius:18px;padding:22px;box-shadow:0 10px 35px #000;color:#fff0c2"><div style="font-size:44px">🌭</div><h2 style="color:#ffd95c;margin:4px 0 10px">¡LONGANIZA DE FUENTES!</h2><p><b>ARMA ARROJADIZA DESBLOQUEADA</b></p><p>Mantén pulsado <b>PEPINAZO durante 1 segundo</b> y suelta.</p><p>La ristra vuela hasta <b>4 casillas</b> en la dirección del rey y explota con alcance de <b>2 casillas a cada lado</b>.</p><p>Cada enemigo eliminado después de conseguirla añade <b>+1 ristra</b>. La munición se conserva entre fases.</p><p>Empiezas con <b>2 ristras</b>.</p><button id="longOk" style="margin-top:8px;padding:12px 22px;font:900 18px monospace;border:2px solid #d8a540;border-radius:12px;background:#7d2b22;color:#fff0c2">¡ENTENDIDO!</button></div>`;
  document.getElementById('box').appendChild(tutorial);document.getElementById('longOk').onclick=()=>{tutorialPaused=false;tutorial.style.display='none';};
  function unlockLonganiza(){if(longanizaUnlocked)return;longanizaUnlocked=true;ristras+=2;tutorialPaused=true;tutorial.style.display='flex';updateRistraHud();}
  function chooseLongPick(){if(longanizaUnlocked){longPick=null;return;}const candidates=[];for(let y=1;y<R-1;y++)for(let x=1;x<C-1;x++)if(g[y][x]===2&&!picks.some(pk=>pk.x===x&&pk.y===y))candidates.push({x,y});if(candidates.length){const q=candidates[Math.floor(Math.random()*candidates.length)];longPick={x:q.x,y:q.y,hidden:true,taken:false,t:0};}}
  level=function(){oldLevel();chooseLongPick();updateRistraHud();};
  function awardKill(n=1){if(!longanizaUnlocked||n<=0)return;ristras+=n;updateRistraHud();}

  damageCells=function(cells,allowBreak=true){const before=enemies.filter(e=>e.alive).length+(elite&&elite.alive?1:0)+sappers.filter(s=>s.alive).length;baseDamageCells(cells,allowBreak);const after=enemies.filter(e=>e.alive).length+(elite&&elite.alive?1:0)+sappers.filter(s=>s.alive).length;awardKill(before-after);if(longPick&&longPick.hidden)for(const c of cells)if(c.x===longPick.x&&c.y===longPick.y&&g[c.y][c.x]===0){longPick.hidden=false;say('¡ALGO HUELE A FUENTES!','#ffd95c',700);break;}};
  touch=function(){if(longPick&&!longPick.hidden&&!longPick.taken&&p.x===longPick.x&&p.y===longPick.y){longPick.taken=true;unlockLonganiza();}oldTouch();};

  function dirVec(){const d=p.dir||p.lastDir||'down';if(d==='left')return[-1,0];if(d==='right')return[1,0];if(d==='up')return[0,-1];return[0,1];}
  function throwLonganiza(){if(!longanizaUnlocked||ristras<=0||tutorialPaused||over||trans)return false;ristras--;updateRistraHud();const[dx,dy]=dirVec();let tx=p.x,ty=p.y;for(let i=0;i<4;i++){const nx=tx+dx,ny=ty+dy;if(nx<=0||ny<=0||nx>=C-1||ny>=R-1||g[ny][nx]===1||g[ny][nx]===3)break;tx=nx;ty=ny;}const now=performance.now();thrownRistras.push({sx:p.x,sy:p.y,x:tx,y:ty,px:p.px,py:p.py,start:now,land:now+420,boomUntil:0,cells:null});say('¡LONGANIZA VOLADORA!','#ffcf61',420);return true;}
  function explodeLonganiza(r,now){r.cells=traceBlast({x:r.x,y:r.y,range:2});r.boomUntil=now+520;damageCells(r.cells,true);}
  function beginCharge(){if(tutorialPaused||over||trans||charging)return;charging=true;chargeStart=performance.now();document.getElementById('fire').textContent=longanizaUnlocked&&ristras>0?'🌭 CARGANDO…':'💥 PEPINAZO';}
  function releaseCharge(){if(!charging)return;const held=performance.now()-chargeStart;charging=false;document.getElementById('fire').innerHTML='💥<br>PEPINAZO';if(held>=950&&longanizaUnlocked&&ristras>0)throwLonganiza();else baseFire();}
  fire=beginCharge;window.addEventListener('keyup',e=>{if(e.key===' ')releaseCharge();});
  const fireBtn=document.getElementById('fire');fireBtn.onclick=null;fireBtn.addEventListener('pointerdown',e=>{e.preventDefault();beginCharge();});fireBtn.addEventListener('pointerup',e=>{e.preventDefault();releaseCharge();});fireBtn.addEventListener('pointercancel',()=>releaseCharge());fireBtn.addEventListener('pointerleave',()=>{if(charging)releaseCharge();});

  function lingeringFire(now){const active=bombs.filter(b=>b.ex&&now<b.until);for(const b of active){const cells=b.sacredCells?b.cells.concat(b.sacredCells):b.cells;let kills=0;for(const e of enemies)if(e.alive&&tileIn(cells,e)){e.alive=false;score+=200;kills++;}if(elite&&elite.alive&&tileIn(cells,elite)){elite.alive=false;score+=500;kills++;say('¡ÉLITE ABRASADO!','#75e3ff',520);}for(const s of sappers)if(s.alive&&tileIn(cells,s)){s.alive=false;score+=120;leaveBlood(s.x,s.y);kills++;}if(p&&tileIn(cells,p))hurt();if(boss.alive&&duel&&!b._bossHazardHit&&tileIn(cells,boss)){b._bossHazardHit=true;boss.hp--;score+=350;if(boss.hp<=0){boss.alive=false;score+=1000;say('¡'+BOSSES[L-1].name+' REVENTADO!','#ff8c42',700);setTimeout(win,720);}else say(`¡PEPINAZO! ${boss.hp} ♥`,'#ff8c42',580);}awardKill(kills);}if(active.length){hud();checkDuel();}}
  blast=function(b){const initialCells=traceBlast(b);const bossHitInitially=boss&&boss.alive&&duel&&tileIn(initialCells,boss);oldBlast(b);b._bossHazardHit=bossHitInitially;};

  update=function(dt,now){if(tutorialPaused)return;oldUpdate(dt,now);lingeringFire(now);for(const r of thrownRistras){if(!r.cells){const t=Math.min(1,(now-r.start)/(r.land-r.start));r.px=tcx(r.sx)+(tcx(r.x)-tcx(r.sx))*t;r.py=tcy(r.sy)+(tcy(r.y)-tcy(r.sy))*t-Math.sin(Math.PI*t)*TH*.7;if(t>=1)explodeLonganiza(r,now);}}thrownRistras=thrownRistras.filter(r=>!r.cells||now<r.boomUntil);if(longPick&&!longPick.hidden&&!longPick.taken)longPick.t+=dt*.004;};

  function drawLonganiza(cx,cy,scale=1,angle=0){ctx.save();ctx.translate(cx,cy);ctx.rotate(angle);ctx.fillStyle='#6b331d';ctx.fillRect(-30*scale,-8*scale,60*scale,16*scale);ctx.fillStyle='#c96635';for(let i=-2;i<=2;i++){ctx.beginPath();ctx.ellipse(i*13*scale,0,10*scale,7*scale,0,0,7);ctx.fill();}ctx.strokeStyle='#e1c891';ctx.lineWidth=3*scale;ctx.beginPath();ctx.moveTo(-35*scale,0);ctx.lineTo(35*scale,0);ctx.stroke();ctx.restore();}
  drawWorld=function(now){oldDrawWorld(now);if(longPick&&!longPick.hidden&&!longPick.taken){const bob=Math.sin(longPick.t)*4;ctx.save();ctx.fillStyle='#ffd95c33';ctx.beginPath();ctx.arc(tcx(longPick.x),tcy(longPick.y)+bob,44,0,7);ctx.fill();ctx.restore();drawLonganiza(tcx(longPick.x),tcy(longPick.y)+bob,1,0);}for(const r of thrownRistras){if(!r.cells)drawLonganiza(r.px,r.py,.9,(now-r.start)/90);else for(const c of r.cells){const a=c.x*TW,d=c.y*TH;ctx.fillStyle='#fff0a7';ctx.fillRect(a+7,d+7,TW-14,TH-14);ctx.fillStyle='#ff7b32';ctx.fillRect(a+TW*.22,d+TH*.22,TW*.56,TH*.56);}}};

  lantern=function(side=1){const flicker=1+Math.sin(performance.now()/70)*.08;ctx.save();ctx.translate(35*side,3);ctx.scale(side,1);ctx.strokeStyle='#8a5a28';ctx.lineWidth=4;ctx.beginPath();ctx.arc(0,-13,11,Math.PI,0);ctx.stroke();ctx.fillStyle='#5c371a';ctx.fillRect(-4,-14,8,22);ctx.fillStyle='#9b682c';ctx.fillRect(-12,5,24,6);ctx.fillRect(-13,29,26,6);ctx.fillStyle='#e5b75b';ctx.fillRect(-10,10,20,19);ctx.fillStyle='rgba(255,233,155,.72)';ctx.fillRect(-6,12,12,15);ctx.fillStyle='#ffca4c';ctx.beginPath();ctx.ellipse(0,19,5*flicker,8*flicker,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff5bd';ctx.beginPath();ctx.ellipse(0,18,2.5*flicker,4.5*flicker,0,0,Math.PI*2);ctx.fill();ctx.restore();};
  drawLightOverlay=function(){if(!(darkMode||L===2))return;const outerRadius=TW*6.15;ctx.save();ctx.fillStyle='rgba(0,0,0,0.90)';ctx.fillRect(0,0,cv.width,cv.height);ctx.globalCompositeOperation='destination-out';const cut=ctx.createRadialGradient(p.px,p.py,0,p.px,p.py,outerRadius);cut.addColorStop(0,'rgba(0,0,0,0.78)');cut.addColorStop(.80,'rgba(0,0,0,0.78)');cut.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=cut;ctx.beginPath();ctx.arc(p.px,p.py,outerRadius,0,Math.PI*2);ctx.fill();ctx.restore();ctx.save();ctx.globalCompositeOperation='screen';const glow=ctx.createRadialGradient(p.px,p.py,TH*.15,p.px,p.py,TW*2.7);glow.addColorStop(0,'rgba(255,207,92,.24)');glow.addColorStop(.55,'rgba(255,174,58,.09)');glow.addColorStop(1,'rgba(255,160,40,0)');ctx.fillStyle=glow;ctx.beginPath();ctx.arc(p.px,p.py,TW*2.7,0,Math.PI*2);ctx.fill();ctx.restore();};

  updateRistraHud();
})();
</script>
"""

html = html.replace("</head>", responsive_ui + "\n</head>")
html = html.replace("</body>", gameplay_patch + "\n</body>")
st.components.v1.html(html, height=590, scrolling=False)
