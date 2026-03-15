import streamlit as st
from supabase import create_client
import qrcode
from io import BytesIO

# --- 1. CONFIGURAÇÕES INICIAIS ---
st.set_page_config(page_title="Portugal Vision", layout="wide")

# LIGAÇÃO AO SUPABASE (DADOS ATUALIZADOS)
URL = "https://hhrmbrcaujfsqfanxqqq.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhocm1icmNhdWpmc3FmYW54cXFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNTA0NDIsImV4cCI6MjA4ODcyNjQ0Mn0.pPkvwcb4h8SjYyvAFt1dnJE6Xn8KDQ4TVcy-QiamLpk"

supabase = create_client(URL, KEY)

# ... (restante código que te enviei antes) ...
