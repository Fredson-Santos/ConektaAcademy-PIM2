import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os
import json
from io import BytesIO

# Tentar importar reportlab (opcional)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_DISPONIVEL = True
except ImportError:
    REPORTLAB_DISPONIVEL = False

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sistema.funcoes import verificar_login
from sistema.database import criar_tabelas
from interface.telas.login import tela_login, fazer_logout, salvar_sessao, carregar_sessao, limpar_sessao
from interface.telas.area_aluno import area_aluno
from interface.telas.area_professor import area_professor
from interface.telas.area_secretaria import area_secretaria

# Configurar página
st.set_page_config(
    page_title="ConektaAcademy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar banco de dados
criar_tabelas()

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin-bottom: 10px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
    }
    .chat-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 8px;
        max-width: 80%;
    }
    .chat-user {
        background-color: #667eea;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .chat-bot {
        background-color: #e9ecef;
        color: #212529;
    }
</style>
""", unsafe_allow_html=True)


# Inicializar session state
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'sessao_carregada' not in st.session_state:
    st.session_state.sessao_carregada = False
if 'mensagens_chat' not in st.session_state:
    st.session_state.mensagens_chat = []

# Tentar carregar sessão salva na primeira execução
if not st.session_state.sessao_carregada and not st.session_state.autenticado:
    login_salvo, senha_salva = carregar_sessao()
    if login_salvo and senha_salva:
        usuario = verificar_login(login_salvo, senha_salva)
        if usuario:
            st.session_state.usuario = usuario
            st.session_state.autenticado = True
    st.session_state.sessao_carregada = True

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200?text=Sistema+Acadêmico", use_container_width=True)
    
    if st.session_state.autenticado:
        usuario = st.session_state.usuario
        st.markdown(f"""
        <div class="user-card">
            <h4>{usuario[1]}</h4>
            <p>Tipo: {usuario[5].capitalize()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            fazer_logout()
    
    st.divider()
    st.info("💡 ConektaAcademy v1.0 - Gerencimento completo de educação")
    
    st.divider()
    st.markdown("""
    <div style="text-align: center; padding: 10px; font-size: 0.8em; color: #6c757d;">
        <p style="margin: 0;">© Conekta - Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

# Render main content
if not st.session_state.autenticado:
    tela_login()
else:
    usuario = st.session_state.usuario
    
    if usuario[5] == "professor":
        area_professor(usuario)
    elif usuario[5] == "secretaria":
        area_secretaria(usuario)
    else:
        area_aluno(usuario)

