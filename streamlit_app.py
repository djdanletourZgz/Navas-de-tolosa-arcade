import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Navas de Tolosa Arcade", page_icon="⚔️", layout="wide")
st.markdown("""
<style>
html, body, [data-testid='stAppViewContainer'] { background:#111; }
.block-container { padding:0 !important; max-width:100% !important; }
header, footer { visibility:hidden; height:0; }
iframe { border:0 !important; }
</style>
""", unsafe_allow_html=True)

html = Path("game/index.html").read_text(encoding="utf-8")
st.components.v1.html(html, height=940, scrolling=False)
