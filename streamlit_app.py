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

html = html.replace("</head>", responsive_ui + "\n</head>")
st.components.v1.html(html, height=590, scrolling=False)
