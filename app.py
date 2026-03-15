import streamlit as st
from supabase import create_client
import qrcode
from io import BytesIO

# --- 1. CONFIGURAÇÕES INICIAIS ---
st.set_page_config(page_title="Portugal Vision", layout="wide")

URL = "https://hhrmbrcaujfsqfanxqqq.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhocm1icmNhdWpmc3FmYW54cXFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNTA0NDIsImV4cCI6MjA4ODcyNjQ0Mn0.pPkvwcb4h8SjYyvAFt1dnJE6Xn8KDQ4TVcy-QiamLpk"

supabase = create_client(URL, KEY)

# --- 2. NAVEGAÇÃO LATERAL ---
st.sidebar.title("🇵🇹 Portugal Vision")
area = st.sidebar.selectbox("Ir para:", ["🛍️ Catálogo Público", "⚙️ Painel do Lojista", "📝 Criar Conta de Loja", "🖥️ Digital Box", "👑 Master Admin"])

# --- 3. CATÁLOGO PÚBLICO ---
if area == "🛍️ Catálogo Público":
    loja_slug = st.query_params.get("loja", None)
    if loja_slug:
        loja_res = supabase.table("lojas").select("*").eq("slug", loja_slug).execute()
        if loja_res.data:
            loja = loja_res.data[0]
            if loja.get("status_catalogo"):
                st.header(f"Bem-vindo à {loja['nome_loja']}")
                st.info("Catálogo em carregamento...")
            else:
                st.warning("Montra temporariamente indisponível.")
        else:
            st.error("Loja não encontrada.")
    else:
        st.header("Portugal Vision")
        st.write("Leia um QR Code para ver o catálogo.")

# --- 4. CRIAR CONTA ---
elif area == "📝 Criar Conta de Loja":
    st.header("📝 Registe a sua Loja")
    with st.form("registo"):
        nome = st.text_input("Nome da Loja")
        email = st.text_input("E-mail")
        nif = st.text_input("NIF")
        senha = st.text_input("Password", type="password")
        if st.form_submit_button("Criar Conta"):
            slug = nome.lower().replace(" ", "-")
            data = {"nome_loja": nome, "email": email, "nif": nif, "password": senha, "slug": slug}
            supabase.table("lojas").insert(data).execute()
            st.success("Conta criada! Aguarde ativação do Master.")

# --- 5. PAINEL DO LOJISTA ---
elif area == "⚙️ Painel do Lojista":
    st.header("⚙️ Gestão")
    email_l = st.text_input("E-mail")
    pass_l = st.text_input("Password", type="password")
    if st.button("Entrar"):
        res = supabase.table("lojas").select("*").eq("email", email_l).eq("password", pass_l).execute()
        if res.data:
            loja = res.data[0]
            st.success(f"Ligado: {loja['nome_loja']}")
            if loja.get("status_catalogo"):
                link = f"https://portugal-vision.streamlit.app/?loja={loja['slug']}"
                qr = qrcode.make(link)
                buf = BytesIO()
                qr.save(buf, format="PNG")
                st.image(buf.getvalue(), width=200)
        else:
            st.error("Login inválido.")

# --- 6. MASTER ADMIN ---
elif area == "👑 Master Admin":
    st.header("👑 Controlo Master")
    m_pass = st.text_input("Chave Master", type="password")
    if m_pass == "PORTUGAL2026":
        lojas = supabase.table("lojas").select("*").execute()
        for l in lojas.data:
            with st.expander(f"Loja: {l['nome_loja']}"):
                cat = st.toggle("Ativar Catálogo", value=l.get("status_catalogo", False), key=f"c_{l['id']}")
                if st.button("Guardar", key=f"s_{l['id']}"):
                    supabase.table("lojas").update({"status_catalogo": cat}).eq("id", l['id']).execute()
                    st.rerun()

# --- 7. DIGITAL BOX ---
elif area == "🖥️ Digital Box":
    st.header("🖥️ Digital Box Ativa")
