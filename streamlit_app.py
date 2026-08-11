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

# Capa responsive: mantiene el tablero proporcionado y convierte los controles
# en una interfaz móvil flotante, sin alargar el canvas verticalmente.
responsive_ui = r"""
<style>
html,body{
  width:100%;height:100%;margin:0!important;overflow:hidden!important;
  background:#0b0907!important;
}
#w{
  width:100%!important;height:100vh!important;max-width:none!important;
  padding:0!important;position:relative!important;overflow:hidden!important;
  display:flex!important;align-items:center!important;justify-content:center!important;
}
#box{
  width:min(100vw,860px)!important;
  height:auto!important;
  aspect-ratio:15/11!important;
  margin:0 auto!important;
  border:0!important;
  box-shadow:none!important;
  position:relative!important;
}
canvas{width:100%!important;height:100%!important;object-fit:contain!important;}
#hud{
  position:absolute!important;z-index:30!important;top:8px!important;left:50%!important;
  transform:translateX(-50%)!important;width:min(96vw,820px)!important;
  padding:5px 7px!important;border:1px solid rgba(222,181,95,.65)!important;
  border-radius:12px!important;background:rgba(24,18,13,.78)!important;
  backdrop-filter:blur(6px)!important;box-shadow:0 4px 16px rgba(0,0,0,.35)!important;
  font-size:11px!important;gap:4px!important;
}
#hud .b{
  border:0!important;border-radius:8px!important;background:rgba(76,57,37,.72)!important;
  padding:4px 6px!important;
}
#mob{
  position:absolute!important;z-index:35!important;left:0!important;bottom:10px!important;
  width:100%!important;padding:0 12px!important;margin:0!important;
  display:flex!important;align-items:flex-end!important;justify-content:space-between!important;
  pointer-events:none!important;
}
#pad,#fire{pointer-events:auto!important;}
#pad{
  display:grid!important;grid-template-columns:76px 76px 76px!important;
  grid-template-rows:62px 62px!important;gap:6px!important;
  filter:drop-shadow(0 5px 8px rgba(0,0,0,.45));
}
.ctrl{
  min-width:76px!important;min-height:62px!important;font-size:31px!important;
  border:2px solid rgba(231,189,99,.9)!important;border-radius:16px!important;
  background:rgba(31,25,20,.86)!important;box-shadow:0 4px 0 rgba(0,0,0,.55)!important;
}
#fire{
  width:150px!important;height:126px!important;border-radius:28px!important;
  font-size:19px!important;border:3px solid #d8a540!important;
  background:linear-gradient(180deg,rgba(154,55,42,.94),rgba(91,27,21,.96))!important;
  box-shadow:0 6px 0 rgba(0,0,0,.55),0 0 20px rgba(216,165,64,.15)!important;
}
#hint{display:none!important;}
#start{border-radius:0!important;}
.card{border-radius:18px!important;max-width:min(88vw,560px)!important;}
@media(max-width:650px){
  #box{width:100vw!important;aspect-ratio:15/11!important;}
  #hud{top:4px!important;width:98vw!important;font-size:9.5px!important;padding:4px!important;}
  #mob{bottom:7px!important;padding:0 8px!important;}
  #pad{grid-template-columns:70px 70px 70px!important;grid-template-rows:58px 58px!important;gap:5px!important;}
  .ctrl{min-width:70px!important;min-height:58px!important;font-size:29px!important;}
  #fire{width:132px!important;height:116px!important;font-size:17px!important;}
}
@media(max-width:390px){
  #pad{grid-template-columns:64px 64px 64px!important;grid-template-rows:54px 54px!important;}
  .ctrl{min-width:64px!important;min-height:54px!important;}
  #fire{width:118px!important;height:108px!important;}
}
</style>
"""

# Correcciones de gameplay/iluminación sobre la V5 sin rehacer toda la lógica.
gameplay_patch = r"""
<script>
(() => {
  const tileIn = (cells, entity) => !!entity && !!cells && cells.some(c => c.x === entity.x && c.y === entity.y);
  const visibleFireCells = (b) => (b.sacredCells ? b.cells.concat(b.sacredCells) : b.cells);

  // Marca si el boss ya recibió el golpe inicial de ESTA explosión,
  // para que la llama persistente no le quite varios corazones por el mismo pepinazo.
  const originalBlast = blast;
  blast = function(b){
    const initialCells = traceBlast(b);
    const bossHitInitially = boss && boss.alive && duel && tileIn(initialCells, boss);
    originalBlast(b);
    b._bossHazardHit = bossHitInitially;
  };

  // Mientras el fogonazo sea visible sigue siendo una zona peligrosa.
  // Cualquier enemigo que entre después también recibe el impacto.
  const originalUpdate = update;
  update = function(dt, now){
    originalUpdate(dt, now);
    let changed = false;

    for(const b of bombs){
      if(!b.ex || now >= b.until) continue;
      const cells = visibleFireCells(b);

      for(const e of enemies){
        if(e.alive && tileIn(cells, e)){
          e.alive = false;
          score += 200;
          changed = true;
        }
      }

      if(elite && elite.alive && tileIn(cells, elite)){
        elite.alive = false;
        score += 500;
        say('¡ÉLITE ABRASADO!','#75e3ff',520);
        changed = true;
      }

      for(const s of sappers){
        if(s.alive && tileIn(cells, s)){
          s.alive = false;
          score += 120;
          leaveBlood(s.x, s.y);
          changed = true;
        }
      }

      if(boss && boss.alive && duel && !b._bossHazardHit && tileIn(cells, boss)){
        b._bossHazardHit = true;
        boss.hp--;
        score += 350;
        changed = true;
        if(boss.hp <= 0){
          boss.alive = false;
          score += 1000;
          say('¡'+BOSSES[L-1].name+' REVENTADO!','#ff8c42',700);
          setTimeout(win,720);
        } else {
          say(`¡PEPINAZO! ${boss.hp} ♥`,'#ff8c42',580);
        }
      }

      if(p && tileIn(cells, p)) hurt();
    }

    if(changed){
      hud();
      checkDuel();
    }
  };

  // Candil mucho más reconocible: asa, cuerpo, cristal y llama animada.
  lantern = function(side=1){
    const flicker = 1 + Math.sin(performance.now()/70)*0.08;
    ctx.save();
    ctx.translate(35*side, 3);
    ctx.scale(side, 1);
    ctx.strokeStyle='#8a5a28';
    ctx.lineWidth=4;
    ctx.beginPath();
    ctx.arc(0,-13,11,Math.PI,0);
    ctx.stroke();
    ctx.fillStyle='#5c371a';
    ctx.fillRect(-4,-14,8,22);
    ctx.fillStyle='#9b682c';
    ctx.fillRect(-12,5,24,6);
    ctx.fillRect(-13,29,26,6);
    ctx.fillStyle='#e5b75b';
    ctx.fillRect(-10,10,20,19);
    ctx.fillStyle='rgba(255,233,155,.72)';
    ctx.fillRect(-6,12,12,15);
    ctx.fillStyle='#ffca4c';
    ctx.beginPath();
    ctx.ellipse(0,19,5*flicker,8*flicker,0,0,Math.PI*2);
    ctx.fill();
    ctx.fillStyle='#fff5bd';
    ctx.beginPath();
    ctx.ellipse(0,18,2.5*flicker,4.5*flicker,0,0,Math.PI*2);
    ctx.fill();
    ctx.restore();
  };

  // Visibilidad pedida:
  // - resto del mapa ≈10% visible
  // - círculo de unas 6 casillas ≈80% visible
  // - borde suavizado para que el candil resulte natural.
  drawLightOverlay = function(){
    if(!(darkMode || L===2)) return;

    const outerRadius = TW * 6.15;
    ctx.save();
    ctx.fillStyle='rgba(0,0,0,0.90)';
    ctx.fillRect(0,0,cv.width,cv.height);

    ctx.globalCompositeOperation='destination-out';
    const cut = ctx.createRadialGradient(p.px,p.py,0,p.px,p.py,outerRadius);
    cut.addColorStop(0,'rgba(0,0,0,0.78)');
    cut.addColorStop(0.80,'rgba(0,0,0,0.78)');
    cut.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=cut;
    ctx.beginPath();
    ctx.arc(p.px,p.py,outerRadius,0,Math.PI*2);
    ctx.fill();
    ctx.restore();

    // Tono cálido del candil sin lavar el escenario.
    ctx.save();
    ctx.globalCompositeOperation='screen';
    const glow = ctx.createRadialGradient(p.px,p.py,TH*.15,p.px,p.py,TW*2.7);
    glow.addColorStop(0,'rgba(255,207,92,.24)');
    glow.addColorStop(.55,'rgba(255,174,58,.09)');
    glow.addColorStop(1,'rgba(255,160,40,0)');
    ctx.fillStyle=glow;
    ctx.beginPath();
    ctx.arc(p.px,p.py,TW*2.7,0,Math.PI*2);
    ctx.fill();
    ctx.restore();
  };
})();
</script>
"""

html = html.replace("</head>", responsive_ui + "\n</head>")
html = html.replace("</body>", gameplay_patch + "\n</body>")
st.components.v1.html(html, height=590, scrolling=False)
