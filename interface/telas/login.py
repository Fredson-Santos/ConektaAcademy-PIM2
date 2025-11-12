"""
Módulo de Telas e Navegação
Contém todas as funções responsáveis pelas interfaces do sistema
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# Imports das funções do sistema
from sistema.funcoes import *
from sistema.chat import enviar_mensagens

# Tentar importar reportlab (opcional) - verificação para interface
try:
    from reportlab.lib.pagesizes import letter, A4
    REPORTLAB_DISPONIVEL = True
except ImportError:
    REPORTLAB_DISPONIVEL = False

# Arquivo para salvar sessão
SESSAO_ARQUIVO = "sessao_salva.json"

# Funções para gerenciar sessão
def salvar_sessao(login, senha):
    """Salva as informações de login em arquivo"""
    try:
        dados = {
            "login": login,
            "senha": senha,
            "timestamp": datetime.now().isoformat()
        }
        with open(SESSAO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados, f)
        return True
    except Exception as e:
        return False

def carregar_sessao():
    """Carrega as informações de sessão salvas"""
    try:
        if os.path.exists(SESSAO_ARQUIVO):
            with open(SESSAO_ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados.get("login"), dados.get("senha")
    except:
        pass
    return None, None

def limpar_sessao():
    """Remove o arquivo de sessão"""
    try:
        if os.path.exists(SESSAO_ARQUIVO):
            os.remove(SESSAO_ARQUIVO)
    except:
        pass

def fazer_logout():
    """Realiza logout do usuário"""
    st.session_state.usuario = None
    st.session_state.autenticado = False
    st.session_state.mensagens_chat = []
    limpar_sessao()
    st.success("Logout realizado com sucesso!")
    st.rerun()

def chat_aba(contexto="geral"):
    """Aba de chat de ajuda"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 8px; margin-bottom: 20px; color: white;">
        <h3 style="color: white; margin: 0;">💬 Chat de Ajuda</h3>
        <p style="color: white; margin: 5px 0 0 0;">Entre em contato conosco para tirar suas dúvidas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Obter identificação do usuário
    if st.session_state.autenticado:
        usuario = st.session_state.usuario
        identificacao = usuario[3] if usuario[3] else usuario[2] if usuario[2] else "visitante"
        nome_usuario = usuario[1] if usuario[1] else "Usuário"
        st.info(f"👤 Conectado como: **{nome_usuario}** ({identificacao})")
    else:
        identificacao = "visitante"
        st.info("ℹ️ Você pode usar o chat mesmo sem estar autenticado. Se precisar de ajuda com login ou cadastro, estamos aqui!")
    
    # Container principal do chat
    st.markdown("---")
    
    # Área de mensagens com scroll automático
    chat_container = st.container()
    with chat_container:
        # Mostrar mensagens anteriores
        if not st.session_state.mensagens_chat:
            st.markdown("""
            <div style="background-color: #e9ecef; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 15px;">
                <p style="margin: 0; color: #495057;"><strong>🤖 Assistente:</strong> Olá! Como posso ajudá-lo hoje? Digite sua pergunta abaixo.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Exibir todas as mensagens
            for msg in st.session_state.mensagens_chat:
                if msg['tipo'] == 'usuario':
                    st.markdown(f"""
                    <div style="background-color: #667eea; color: white; padding: 12px; border-radius: 10px; margin-bottom: 10px; margin-left: 20%; text-align: right;">
                        <p style="margin: 0;"><strong>Você:</strong> {msg['texto']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; color: #212529; padding: 12px; border-radius: 10px; margin-bottom: 10px; margin-right: 20%; border-left: 4px solid #667eea;">
                        <p style="margin: 0;"><strong>🤖 Assistente:</strong> {msg['texto']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Área de input para nova mensagem - usar contexto para keys únicas
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        nova_mensagem = st.text_input(
            "Digite sua mensagem:",
            key=f"input_chat_aba_{contexto}",
            placeholder="Digite sua pergunta ou mensagem...",
            label_visibility="collapsed"
        )
    with col2:
        enviar_btn = st.button("📤 Enviar", use_container_width=True, type="primary", key=f"btn_enviar_chat_aba_{contexto}")
    with col3:
        limpar_btn = st.button("🗑️ Limpar", use_container_width=True, key=f"btn_limpar_chat_aba_{contexto}")
    
    # Processar envio de mensagem
    if enviar_btn and nova_mensagem.strip():
        # Adicionar mensagem do usuário
        st.session_state.mensagens_chat.append({
            'tipo': 'usuario',
            'texto': nova_mensagem
        })
        
        # Mostrar indicador de carregamento
        with st.spinner("⏳ Enviando mensagem..."):
            # Enviar para API e obter resposta
            try:
                resposta_bot = enviar_mensagens(nova_mensagem, identificacao)
                st.session_state.mensagens_chat.append({
                    'tipo': 'bot',
                    'texto': resposta_bot
                })
            except Exception as e:
                st.session_state.mensagens_chat.append({
                    'tipo': 'bot',
                    'texto': f"❌ Erro ao conectar com o chat. Tente novamente mais tarde. Erro: {str(e)}"
                })
        
        st.rerun()
    
    # Processar limpeza de chat
    if limpar_btn:
        st.session_state.mensagens_chat = []
        st.success("✅ Chat limpo com sucesso!")
        st.rerun()
    
    # Informações adicionais
    st.markdown("---")
    if not st.session_state.autenticado:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; font-size: 0.9em; color: #6c757d;">
            <p style="margin: 0;">💡 <strong>Dica:</strong> Você pode fazer perguntas sobre como fazer login, como se cadastrar, ou qualquer outra dúvida sobre o sistema acadêmico.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; font-size: 0.9em; color: #6c757d;">
            <p style="margin: 0;">💡 <strong>Dica:</strong> Você pode fazer perguntas sobre o sistema, suas notas, presenças, ou qualquer outra dúvida relacionada ao sistema acadêmico.</p>
        </div>
        """, unsafe_allow_html=True)

def tela_login():
    """Tela de Login"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🎓 ConektaAcademy</h1>
            <p>Bem-vindo ao Sistema de Gerenciamento Acadêmico</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Login", "Cadastro", "💬 Chat de Ajuda"])
        
        with tab1:
            st.subheader("Faça Login")
            
            # Tentar preencher com sessão salva
            login_salvo, senha_salva = carregar_sessao()
            valor_login = login_salvo if login_salvo else ""
            valor_senha = senha_salva if senha_salva else ""
            
            login_input = st.text_input("Email ou Matrícula", value=valor_login, placeholder="seu_email@email.com ou sua_matricula")
            senha_input = st.text_input("Senha", type="password", value=valor_senha, placeholder="Digite sua senha")
            
            # Checkbox para salvar sessão
            lembrar_me = st.checkbox("💾 Lembrar-me (manter logado)", value=bool(login_salvo))
            
            if st.button("🔓 Entrar", use_container_width=True, type="primary", key="btn_entrar_login"):
                if not login_input or not senha_input:
                    st.error("❌ Por favor, preencha todos os campos!")
                else:
                    usuario = verificar_login(login_input, senha_input)
                    if usuario:
                        st.session_state.usuario = usuario
                        st.session_state.autenticado = True
                        
                        # Salvar sessão se marcado "Lembrar-me"
                        if lembrar_me:
                            salvar_sessao(login_input, senha_input)
                        else:
                            limpar_sessao()
                        
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Email/Matrícula ou senha incorretos!")
                        limpar_sessao()
        
        with tab2:
            st.subheader("Criar Nova Conta")
            
            nome = st.text_input("Nome Completo", placeholder="Digite seu nome completo")
            email = st.text_input("Email", placeholder="seu_email@email.com)")
            matricula = st.text_input("Matrícula", placeholder="Sua matrícula")
            senha = st.text_input("Senha", type="password", placeholder="Digite uma senha")
            confirmar_senha = st.text_input("Confirmar Senha", type="password", placeholder="Confirme a senha")
            
            if st.button("✅ Cadastrar", use_container_width=True, type="primary", key="btn_cadastrar_login"):
                if not nome or not senha:
                    st.error("❌ Nome e Senha são obrigatórios!")
                elif senha != confirmar_senha:
                    st.error("❌ As senhas não conferem!")
                else:
                    try:
                        # Determinar tipo de usuário
                        if "@prof" in email:
                            tipo_usuario = "professor"
                            materia = None  # Matéria será vinculada pela secretaria através de disciplinas
                        elif "@sec" in email:
                            tipo_usuario = "secretaria"
                            materia = None
                        else:
                            tipo_usuario = "aluno"
                            materia = None
                        
                        adicionar_usuario(nome, email, matricula, senha, tipo_usuario, materia)
                        st.success("✅ Usuário cadastrado com sucesso! Faça login para continuar.")
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar: {str(e)}")
        
        with tab3:
            chat_aba(contexto="login")

