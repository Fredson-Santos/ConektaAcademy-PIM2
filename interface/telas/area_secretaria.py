"""
Módulo da Área da Secretaria
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Imports das funções do sistema
from sistema.funcoes import *
from interface.telas.login import chat_aba
from sistema.relatorios import gerar_relatorio_pdf, gerar_dados_relatorio_turmas, gerar_dados_relatorio_disciplinas, gerar_dados_relatorio_cursos
from sistema import database as db

# Tentar importar reportlab (opcional)
try:
    from reportlab.lib.pagesizes import letter, A4
    REPORTLAB_DISPONIVEL = True
except ImportError:
    REPORTLAB_DISPONIVEL = False

def area_secretaria(secretaria):
    """Área da Secretaria"""
    st.markdown(f"""
    <div class="user-card">
        <h3>🗂️ Bem-vindo(a), {secretaria[1]}!</h3>
        <p>Acesso: Secretaria | Email: {secretaria[2]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["👥 Gerenciar Usuários", "📚 Turmas", "📖 Disciplinas", "🎓 Cursos", "📄 Relatórios", "💬 Chat de Ajuda"])
    
    with tab1:
        st.subheader("Gerenciamento de Usuários")
        
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "Listar",
            "Cadastrar",
            "Excluir",
            "Resetar Senha"
        ])
        
        with sub_tab1:
            st.write("**Todos os Usuários**")
            try:
                usuarios = listar("usuarios", "nome", "email", "matricula", "tipo_usuario")
                if usuarios:
                    df = pd.DataFrame(usuarios, columns=["Nome", "Email", "Matrícula", "Tipo"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("ℹ️ Nenhum usuário cadastrado.")
            except Exception as e:
                st.error(f"❌ Erro ao listar: {str(e)}")
        
        with sub_tab2:
            st.write("**Cadastrar Novo Usuário**")
            
            col1, col2 = st.columns(2)
            with col1:
                tipo_novo = st.selectbox("Tipo de Usuário", ["aluno", "professor", "secretaria"], key="tipo_novo_user")
                nome_novo = st.text_input("Nome Completo", placeholder="Digite o nome")
            with col2:
                email_novo = st.text_input("Email", placeholder="user@email.com")
                matricula_nova = st.text_input("Matrícula", placeholder="Deixe em branco se for professor")
            
            senha_nova = st.text_input("Senha", type="password", placeholder="Digite a senha", key="senha_nova_cad")
            
            if st.button("✅ Cadastrar Usuário", use_container_width=True, type="primary", key="btn_cadastrar_user_sec"):
                if not nome_novo or not senha_nova:
                    st.error("❌ Nome e Senha são obrigatórios!")
                else:
                    try:
                        # Professores não têm matéria no cadastro, será vinculado depois via disciplinas
                        adicionar_usuario(nome_novo, email_novo, matricula_nova, senha_nova, tipo_novo, None)
                        st.success("✅ Usuário cadastrado com sucesso!")
                        st.info("💡 Professores devem ser vinculados a disciplinas pela secretaria.")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
        
        with sub_tab3:
            st.write("**Excluir Usuário**")
            matricula_exc = st.text_input("Matrícula do usuário a excluir", placeholder="Digite a matrícula", key="mat_exc_user")
            
            if st.button("🗑️ Excluir", use_container_width=True, type="secondary", key="btn_excluir_user"):
                if not matricula_exc:
                    st.error("❌ Digite uma matrícula!")
                else:
                    try:
                        excluir_usuario(matricula_exc)
                        st.success("✅ Usuário excluído com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
        
        with sub_tab4:
            st.write("**Redefinir Senha**")
            matricula_reset = st.text_input("Matrícula do usuário", placeholder="Digite a matrícula", key="mat_reset_senha")
            nova_senha_reset = st.text_input("Nova Senha", type="password", placeholder="Digite a nova senha", key="nova_senha_reset")
            
            if st.button("🔑 Redefinir Senha", use_container_width=True, type="primary", key="btn_redefinir_senha"):
                if not matricula_reset or not nova_senha_reset:
                    st.error("❌ Preencha todos os campos!")
                else:
                    try:
                        if consultar_usuario(matricula_reset):
                            redefinir_senha(matricula_reset, nova_senha_reset)
                            st.success("✅ Senha redefinida com sucesso!")
                        else:
                            st.error("❌ Usuário não encontrado!")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
    
    with tab2:
        st.subheader("Gerenciamento de Turmas")
        
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "Listar",
            "Criar",
            "Excluir",
            "Vincular"
        ])
        
        with sub_tab1:
            st.write("**Todas as Turmas**")
            try:
                # Buscar turmas com ID
                conn = db.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, ano, professor_id, curso_id FROM turmas")
                turmas = cursor.fetchall()
                conn.close()
                
                if turmas:
                    # Buscar alunos de cada turma
                    dados_turmas = []
                    for turma in turmas:
                        turma_id = turma[0]
                        nome_turma = turma[1]
                        ano_turma = turma[2] if turma[2] is not None else "N/A"
                        professor_id = turma[3] if turma[3] is not None else None
                        curso_id = turma[4] if turma[4] is not None else None
                        
                        # Buscar nome do curso se houver
                        curso_nome = "N/A"
                        if curso_id:
                            conn = db.conectar()
                            cursor = conn.cursor()
                            cursor.execute("SELECT nome FROM cursos WHERE id = ?", (curso_id,))
                            curso = cursor.fetchone()
                            conn.close()
                            if curso:
                                curso_nome = curso[0]
                        
                        # Buscar email do professor se houver
                        professor_email = "N/A"
                        if professor_id:
                            conn = db.conectar()
                            cursor = conn.cursor()
                            cursor.execute("SELECT email FROM usuarios WHERE id = ? AND tipo_usuario = 'professor'", (professor_id,))
                            prof = cursor.fetchone()
                            conn.close()
                            if prof and prof[0]:
                                professor_email = prof[0]
                        
                        # Buscar alunos desta turma
                        conn = db.conectar()
                        cursor = conn.cursor()
                        cursor.execute("SELECT nome, matricula FROM usuarios WHERE turma_id = ? AND tipo_usuario = 'aluno'", (nome_turma,))
                        alunos_turma = cursor.fetchall()
                        conn.close()
                        
                        num_alunos = len(alunos_turma)
                        
                        dados_turmas.append({
                            "ID": turma_id,
                            "Turma": nome_turma,
                            "Ano": ano_turma,
                            "Curso": curso_nome,
                            "Professor Email": professor_email,
                            "Alunos": f"{num_alunos} aluno(s)" if num_alunos > 0 else "Nenhum aluno"
                        })
                    
                    df = pd.DataFrame(dados_turmas)
                    st.dataframe(df, use_container_width=True)
                    
                    # Expander para ver detalhes
                    with st.expander("📋 Ver alunos por turma"):
                        for turma in turmas:
                            nome_turma = turma[1]
                            st.write(f"**Turma: {nome_turma}**")
                            
                            conn = db.conectar()
                            cursor = conn.cursor()
                            cursor.execute("SELECT nome, matricula FROM usuarios WHERE turma_id = ? AND tipo_usuario = 'aluno'", (nome_turma,))
                            alunos_turma = cursor.fetchall()
                            conn.close()
                            
                            if alunos_turma:
                                for aluno in alunos_turma:
                                    st.write(f"- (Matrícula: {aluno[1]}) - {aluno[0]}")
                            else:
                                st.write("Nenhum aluno vinculado.")
                            st.divider()
                else:
                    st.info("ℹ️ Nenhuma turma cadastrada.")
            except Exception as e:
                st.error(f"❌ Erro ao listar: {str(e)}")
        
        with sub_tab2:
            st.write("**Criar Nova Turma**")
            
            # Listar cursos para selectbox
            try:
                cursos = listar("cursos", "id", "nome")
                cursos_list = []
                if cursos:
                    cursos_list = [(str(curso[0]), curso[1]) for curso in cursos]  # (id, nome)
            except:
                cursos_list = []
            
            col1, col2 = st.columns(2)
            with col1:
                nome_turma = st.text_input("Nome da Turma", placeholder="Ex: 1º Ano A", key="nome_turma_new")
                ano_turma = st.text_input("Ano", placeholder="Ex: 2024", key="ano_turma_new")
            with col2:
                if cursos_list:
                    opcoes_cursos_turma = [f"{nome} (ID: {id_curso})" for id_curso, nome in cursos_list]
                    curso_selec_turma = st.selectbox("Selecione o Curso*", opcoes_cursos_turma, key="curso_selec_turma")
                    
                    # Extrair ID do curso selecionado
                    curso_id_turma = None
                    if curso_selec_turma:
                        curso_id_turma = int(curso_selec_turma.split("(ID: ")[1].replace(")", ""))
                else:
                    st.error("❌ Nenhum curso cadastrado. É necessário cadastrar um curso antes de criar uma turma.")
                    curso_id_turma = None
            
            # Campo para vincular professor
            professores_criar = buscar_professores()
            matricula_professor_turma = None
            if professores_criar:
                opcoes_prof_turma = ["Nenhum"] + [f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}" for prof in professores_criar]
                prof_selec_turma = st.selectbox("Vincular Professor (opcional)", opcoes_prof_turma, key="prof_selec_turma_criar")
                
                # Extrair matrícula do professor selecionado
                if prof_selec_turma != "Nenhum":
                    for prof in professores_criar:
                        prof_formatado = f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}"
                        if prof_formatado == prof_selec_turma:
                            matricula_professor_turma = prof[3]
                            break
            else:
                st.info("ℹ️ Nenhum professor cadastrado. Você pode criar uma turma sem professor.")
            
            if st.button("➕ Criar Turma", use_container_width=True, type="primary", key="btn_criar_turma"):
                if not nome_turma or not ano_turma:
                    st.error("❌ Preencha nome e ano da turma!")
                elif not curso_id_turma:
                    st.error("❌ Selecione um curso! O curso é obrigatório.")
                else:
                    try:
                        resultado = criar_turma(nome_turma.lower(), ano_turma, curso_id_turma, matricula_professor_turma)
                        if resultado:
                            st.success("✅ Turma criada com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao criar turma.")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
        
        with sub_tab3:
            st.write("**Excluir Turma**")
            
            # Buscar todas as turmas para o selectbox
            try:
                conn = db.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, ano, curso_id FROM turmas ORDER BY nome")
                turmas_excluir = cursor.fetchall()
                conn.close()
                
                if turmas_excluir:
                    # Buscar nomes dos cursos
                    turmas_com_curso = []
                    for turma in turmas_excluir:
                        turma_id = turma[0]
                        nome_turma = turma[1]
                        ano_turma = turma[2] if turma[2] else "N/A"
                        curso_id = turma[3] if turma[3] else None
                        
                        curso_nome = "Sem curso"
                        if curso_id:
                            conn = db.conectar()
                            cursor = conn.cursor()
                            cursor.execute("SELECT nome FROM cursos WHERE id = ?", (curso_id,))
                            curso = cursor.fetchone()
                            conn.close()
                            if curso:
                                curso_nome = curso[0]
                        
                        turmas_com_curso.append({
                            "id": turma_id,
                            "nome": nome_turma,
                            "ano": ano_turma,
                            "curso": curso_nome
                        })
                    
                    # Criar lista de opções para o selectbox
                    opcoes_turmas = [f"{t['nome']} - {t['curso']} (Ano: {t['ano']})" for t in turmas_com_curso]
                    turma_selec_excluir = st.selectbox("Selecione a Turma a excluir", opcoes_turmas, key="turma_selec_excluir")
                    
                    if st.button("🗑️ Excluir Turma", use_container_width=True, type="secondary", key="btn_excluir_turma"):
                        try:
                            # Extrair nome da turma selecionada
                            nome_turma_exc = None
                            for t in turmas_com_curso:
                                turma_formatada = f"{t['nome']} - {t['curso']} (Ano: {t['ano']})"
                                if turma_formatada == turma_selec_excluir:
                                    nome_turma_exc = t['nome']
                                    break
                            
                            if nome_turma_exc:
                                excluir_turma(nome_turma_exc)
                                st.success("✅ Turma excluída com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao identificar a turma selecionada.")
                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")
                else:
                    st.info("ℹ️ Nenhuma turma cadastrada para excluir.")
            except Exception as e:
                st.error(f"❌ Erro ao carregar turmas: {str(e)}")
        
        with sub_tab4:
            st.write("**Vincular Turmas**")
            
            sub_sub_tab1, sub_sub_tab2 = st.tabs(["Vincular Professor", "Vincular Aluno"])
            
            with sub_sub_tab1:
                st.write("**Vincular Professor a Turma**")
                
                # Listar turmas
                turmas_vinc = listar("turmas", "nome", "ano")
                if turmas_vinc:
                    nomes_turmas_vinc = [t[0] for t in turmas_vinc]
                    turma_selec_vinc = st.selectbox("Selecione a Turma", nomes_turmas_vinc, key="turma_vinc_prof")
                    
                    # Listar professores
                    professores_vinc = buscar_professores()
                    if professores_vinc:
                        nomes_prof_vinc = [f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}" for prof in professores_vinc]
                        prof_selec_vinc = st.selectbox("Selecione o Professor", nomes_prof_vinc, key="prof_vinc_turma")
                        
                        if st.button("🔗 Vincular Professor", use_container_width=True, type="primary", key="btn_vinc_prof_turma"):
                            try:
                                # Extrair matrícula do professor
                                prof_matricula_vinc = None
                                for prof in professores_vinc:
                                    prof_formatado = f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}"
                                    if prof_formatado == prof_selec_vinc:
                                        prof_matricula_vinc = prof[3]
                                        break
                                
                                resultado = vincular_professor_turma(prof_matricula_vinc, turma_selec_vinc)
                                if resultado:
                                    st.success("✅ Professor vinculado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao vincular professor. Verifique se os dados estão corretos.")
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")
                    else:
                        st.warning("⚠️ Nenhum professor cadastrado.")
                else:
                    st.warning("⚠️ Nenhuma turma cadastrada.")
            
            with sub_sub_tab2:
                st.write("**Vincular Aluno a Turma**")
                
                # Listar turmas
                turmas_vinc_aluno = listar("turmas", "nome", "ano")
                if turmas_vinc_aluno:
                    nomes_turmas_aluno = [t[0] for t in turmas_vinc_aluno]
                    turma_selec_aluno = st.selectbox("Selecione a Turma", nomes_turmas_aluno, key="turma_vinc_aluno_tab")
                    
                    # Buscar lista de alunos
                    try:
                        usuarios = listar("usuarios", "nome", "email", "matricula", "tipo_usuario")
                        alunos = []
                        if usuarios:
                            for u in usuarios:
                                if u and len(u) > 3 and u[3] == "aluno":
                                    alunos.append((u[2], u[0]))  # (matricula, nome)
                        
                        if alunos:
                            # Selectbox para escolher aluno
                            opcoes_alunos = [f"(Matrícula: {matricula or 'N/A'}) - {nome}" for matricula, nome in alunos]
                            aluno_selecionado = st.selectbox("Selecione o Aluno", opcoes_alunos, key="aluno_vinc_turma_tab")
                            
                            # Extrair matrícula
                            matricula_aluno_vinc = None
                            for matricula, nome in alunos:
                                if f"(Matrícula: {matricula or 'N/A'}) - {nome}" == aluno_selecionado:
                                    matricula_aluno_vinc = matricula
                                    break
                            
                            if st.button("🔗 Vincular Aluno", use_container_width=True, type="primary", key="btn_vinc_aluno_turma"):
                                if matricula_aluno_vinc and turma_selec_aluno:
                                    try:
                                        resultado = vincular_aluno_turma(matricula_aluno_vinc, turma_selec_aluno)
                                        if resultado:
                                            st.success(f"✅ Aluno vinculado à turma '{turma_selec_aluno}' com sucesso!")
                                            st.rerun()
                                        else:
                                            st.error("❌ Erro ao vincular aluno. Verifique se o aluno e a turma existem.")
                                    except Exception as e:
                                        error_msg = str(e)
                                        st.error(f"❌ Erro: {error_msg}")
                                else:
                                    st.error("❌ Selecione aluno e turma!")
                        else:
                            st.warning("⚠️ Nenhum aluno cadastrado no sistema.")
                    except Exception as e:
                        st.error(f"❌ Erro ao buscar dados: {str(e)}")
                else:
                    st.warning("⚠️ Nenhuma turma cadastrada. Crie uma turma primeiro.")
    
    with tab3:
        st.subheader("Gerenciamento de Disciplinas")
        
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "Listar",
            "Criar",
            "Excluir",
            "Vincular"
        ])
        
        with sub_tab1:
            st.write("**Todas as Disciplinas**")
            try:
                disciplinas_raw = listar("disciplinas", "id", "nome", "professor_id", "carga_horaria", "curso_id", "turma_id")
                if disciplinas_raw:
                    # Processar dados para exibir nomes ao invés de IDs
                    disciplinas_processadas = []
                    for disc in disciplinas_raw:
                        disc_id = disc[0]
                        disc_nome = disc[1]
                        prof_id = disc[2]
                        carga_hor = disc[3]
                        curso_id_disc = disc[4] if len(disc) > 4 else None
                        turma_id_disc = disc[5] if len(disc) > 5 else None
                        
                        # Buscar nome do professor
                        prof_nome = "N/A"
                        if prof_id:
                            conn = db.conectar()
                            cursor = conn.cursor()
                            cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (prof_id,))
                            prof = cursor.fetchone()
                            conn.close()
                            if prof:
                                prof_nome = prof[0]
                        
                        # Buscar nome do curso
                        curso_nome_disc = "N/A"
                        if curso_id_disc:
                            conn = db.conectar()
                            cursor = conn.cursor()
                            cursor.execute("SELECT nome FROM cursos WHERE id = ?", (curso_id_disc,))
                            curso = cursor.fetchone()
                            conn.close()
                            if curso:
                                curso_nome_disc = curso[0]
                        
                        disciplinas_processadas.append({
                            "ID": disc_id,
                            "Nome": disc_nome,
                            "Professor": prof_nome,
                            "Carga Horária": carga_hor,
                            "Curso": curso_nome_disc,
                            "Turma": turma_id_disc or "N/A"
                        })
                    
                    df = pd.DataFrame(disciplinas_processadas)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("ℹ️ Nenhuma disciplina cadastrada.")
            except Exception as e:
                st.error(f"❌ Erro ao listar: {str(e)}")
        
        with sub_tab2:
            st.write("**Criar Nova Disciplina**")
            
            # Listar cursos e turmas para selectboxes
            try:
                cursos = listar("cursos", "id", "nome")
                cursos_list = []
                if cursos:
                    cursos_list = [(str(curso[0]), curso[1]) for curso in cursos]  # (id, nome)
                
                turmas = listar("turmas", "nome", "ano")
                turmas_list = []
                if turmas:
                    turmas_list = [turma[0] for turma in turmas]  # nome da turma
            except:
                cursos_list = []
                turmas_list = []
            
            col1, col2 = st.columns(2)
            with col1:
                nome_disc = st.text_input("Nome da Disciplina", placeholder="Ex: Matemática", key="nome_disc_new")
                carga_horaria_disc = st.number_input("Carga Horária (horas)", min_value=1, value=60, key="carga_disc_new")
                
                # Listar professores para selectbox
                professores_disc = buscar_professores()
                if professores_disc:
                    opcoes_prof_disc = ["Nenhum"] + [f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}" for prof in professores_disc]
                    prof_selec_disc = st.selectbox("Selecione o Professor (opcional)", opcoes_prof_disc, key="prof_selec_disc_new")
                    
                    # Extrair matrícula do professor selecionado
                    matricula_prof_disc = None
                    if prof_selec_disc != "Nenhum":
                        for prof in professores_disc:
                            if f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}" == prof_selec_disc:
                                matricula_prof_disc = prof[3]
                                break
                else:
                    st.info("ℹ️ Nenhum professor cadastrado.")
                    matricula_prof_disc = None
            
            with col2:
                if cursos_list:
                    opcoes_cursos_disc = ["Nenhum"] + [f"{nome} (ID: {id_curso})" for id_curso, nome in cursos_list]
                    curso_selec_disc = st.selectbox("Selecione o Curso (opcional)", opcoes_cursos_disc, key="curso_selec_disc_new")
                    
                    # Extrair ID do curso selecionado
                    curso_id_disc = None
                    if curso_selec_disc != "Nenhum":
                        curso_id_disc = int(curso_selec_disc.split("(ID: ")[1].replace(")", ""))
                else:
                    st.info("ℹ️ Nenhum curso cadastrado.")
                    curso_id_disc = None
                
                if turmas_list:
                    opcoes_turmas_disc = ["Nenhuma"] + turmas_list
                    turma_selec_disc = st.selectbox("Selecione a Turma (opcional)", opcoes_turmas_disc, key="turma_selec_disc_new")
                    
                    # Extrair nome da turma selecionada
                    turma_id_disc = None
                    if turma_selec_disc != "Nenhuma":
                        turma_id_disc = turma_selec_disc.lower()
                else:
                    st.info("ℹ️ Nenhuma turma cadastrada.")
                    turma_id_disc = None
            
            if st.button("➕ Criar Disciplina", use_container_width=True, type="primary", key="btn_criar_disc"):
                if not nome_disc:
                    st.error("❌ Digite o nome da disciplina!")
                else:
                    try:
                        resultado = criar_disciplina(
                            nome_disc.lower(), 
                            matricula_prof_disc if matricula_prof_disc else None, 
                            carga_horaria_disc,
                            curso_id=curso_id_disc if curso_id_disc else None,
                            turma_id=turma_id_disc if turma_id_disc else None
                        )
                        if resultado:
                            st.success("✅ Disciplina criada com sucesso!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Disciplina não foi criada. Verifique os dados.")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
        
        with sub_tab3:
            st.write("**Excluir Disciplina**")
            id_disc_exc = st.text_input("ID da Disciplina a excluir", placeholder="Digite o ID", key="id_disc_exc")
            
            if st.button("🗑️ Excluir Disciplina", use_container_width=True, type="secondary", key="btn_excluir_disc"):
                if not id_disc_exc:
                    st.error("❌ Digite um ID!")
                else:
                    try:
                        excluir_disciplina(id_disc_exc)
                        st.success("✅ Disciplina excluída com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
        
        with sub_tab4:
            st.write("**Vincular Disciplinas**")
            
            sub_sub_tab1, sub_sub_tab2, sub_sub_tab3 = st.tabs(["Vincular Professor", "Vincular Curso", "Vincular Turma"])
            
            with sub_sub_tab1:
                st.write("**Vincular Professor a Disciplina**")
                
                # Listar disciplinas
                disciplinas_vinc = buscar_disciplinas()
                if disciplinas_vinc:
                    nomes_disc_vinc = [f"{disc[0]} - {disc[1]}" for disc in disciplinas_vinc]
                    disc_selec_vinc = st.selectbox("Selecione a Disciplina", nomes_disc_vinc, key="disc_vinc_prof")
                    
                    # Listar professores
                    professores_vinc = buscar_professores()
                    if professores_vinc:
                        nomes_prof_vinc = [f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}" for prof in professores_vinc]
                        prof_selec_vinc = st.selectbox("Selecione o Professor", nomes_prof_vinc, key="prof_vinc_disc")
                        
                        if st.button("🔗 Vincular Professor", use_container_width=True, type="primary", key="btn_vinc_prof_disc"):
                            try:
                                # Extrair IDs
                                disc_id_vinc = int(disc_selec_vinc.split(" - ")[0])
                                prof_id_vinc = None
                                for prof in professores_vinc:
                                    prof_formatado = f"(Matrícula: {prof[3] or 'N/A'}) - {prof[1]}"
                                    if prof_formatado == prof_selec_vinc:
                                        prof_id_vinc = prof[0]
                                        break
                                
                                vincular_disciplina_professor(disc_id_vinc, prof_id_vinc)
                                st.success("✅ Professor vinculado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")
                    else:
                        st.warning("⚠️ Nenhum professor cadastrado.")
                else:
                    st.warning("⚠️ Nenhuma disciplina cadastrada.")
            
            with sub_sub_tab2:
                st.write("**Vincular Disciplina a Curso**")
                
                disciplinas_vinc_curso = buscar_disciplinas()
                if disciplinas_vinc_curso:
                    nomes_disc_curso = [f"{disc[0]} - {disc[1]}" for disc in disciplinas_vinc_curso]
                    disc_selec_curso = st.selectbox("Selecione a Disciplina", nomes_disc_curso, key="disc_vinc_curso")
                    
                    # Listar cursos
                    cursos_vinc = listar("cursos", "id", "nome")
                    if cursos_vinc:
                        nomes_cursos = [f"{curso[0]} - {curso[1]}" for curso in cursos_vinc]
                        curso_selec = st.selectbox("Selecione o Curso", nomes_cursos, key="curso_vinc_disc")
                        
                        if st.button("🔗 Vincular Curso", use_container_width=True, type="primary", key="btn_vinc_curso_disc"):
                            try:
                                disc_id_curso = int(disc_selec_curso.split(" - ")[0])
                                curso_id_curso = int(curso_selec.split(" - ")[0])
                                
                                vincular_disciplina_curso(disc_id_curso, curso_id_curso)
                                st.success("✅ Curso vinculado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")
                    else:
                        st.warning("⚠️ Nenhum curso cadastrado.")
                else:
                    st.warning("⚠️ Nenhuma disciplina cadastrada.")
            
            with sub_sub_tab3:
                st.write("**Vincular Disciplina a Turma**")
                st.info("ℹ️ Ao vincular uma disciplina a uma turma, todos os alunos dessa turma ficam automaticamente vinculados à disciplina.")
                
                # Listar disciplinas
                disciplinas_vinc_turma = buscar_disciplinas()
                if disciplinas_vinc_turma:
                    nomes_disc_turma = [f"{disc[0]} - {disc[1]}" for disc in disciplinas_vinc_turma]
                    disc_selec_turma = st.selectbox("Selecione a Disciplina", nomes_disc_turma, key="disc_vinc_turma")
                    
                    # Listar turmas
                    turmas_vinc_disc = listar("turmas", "nome", "ano")
                    if turmas_vinc_disc:
                        nomes_turmas_vinc_disc = [t[0] for t in turmas_vinc_disc]
                        turma_selec_disc = st.selectbox("Selecione a Turma", nomes_turmas_vinc_disc, key="turma_vinc_disc")
                        
                        if st.button("🔗 Vincular Turma", use_container_width=True, type="primary", key="btn_vinc_turma_disc"):
                            try:
                                disc_id_turma = int(disc_selec_turma.split(" - ")[0])
                                
                                resultado = vincular_disciplina_turma(disc_id_turma, turma_selec_disc)
                                if resultado:
                                    st.success(f"✅ Disciplina vinculada à turma '{turma_selec_disc}' com sucesso! Todos os alunos da turma estão automaticamente vinculados à disciplina.")
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao vincular turma. Verifique se os dados estão corretos.")
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")
                    else:
                        st.warning("⚠️ Nenhuma turma cadastrada.")
                else:
                    st.warning("⚠️ Nenhuma disciplina cadastrada.")
    
    with tab4:
        st.subheader("Gerenciamento de Cursos")
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "Listar",
            "Criar",
            "Excluir"
        ])
        
        with sub_tab1:
            st.write("**Todos os Cursos**")
            try:
                cursos = listar("cursos", "id", "nome", "inicio", "duracao")
                if cursos:
                    df = pd.DataFrame(cursos, columns=["ID", "Nome", "Início", "Duração (semestres)"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("ℹ️ Nenhum curso cadastrado.")
            except Exception as e:
                st.error(f"❌ Erro ao listar: {str(e)}")
        
        with sub_tab2:
            st.write("**Criar Novo Curso**")
            
            col1, col2 = st.columns(2)
            with col1:
                nome_curso = st.text_input("Nome do Curso", placeholder="Ex: Engenharia de Software", key="nome_curso_new")
                inicio_curso = st.text_input("Data de Início", placeholder="Ex: 01/02/2024", key="inicio_curso_new")
            with col2:
                duracao_curso = st.number_input("Duração (semestres)", min_value=1, value=8, key="duracao_curso_new")
            
            if st.button("➕ Criar Curso", use_container_width=True, type="primary", key="btn_criar_curso"):
                if not nome_curso:
                    st.error("❌ Digite o nome do curso!")
                else:
                    try:
                        criar_curso(nome_curso, inicio_curso, duracao_curso)
                        st.success("✅ Curso criado com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
        
        with sub_tab3:
            st.write("**Excluir Curso**")
            id_curso_exc = st.text_input("ID do Curso a excluir", placeholder="Digite o ID", key="id_curso_exc")
            
            if st.button("🗑️ Excluir Curso", use_container_width=True, type="secondary", key="btn_excluir_curso"):
                if not id_curso_exc:
                    st.error("❌ Digite um ID!")
                else:
                    try:
                        excluir_curso(id_curso_exc)
                        st.success("✅ Curso excluído com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
    
    with tab5:
        st.subheader("Gerar Relatórios")
        
        sub_rel_tab1, sub_rel_tab2, sub_rel_tab3, sub_rel_tab4 = st.tabs([
            "👤 Relatório de Alunos",
            "🏫 Relatório de Turmas",
            "📖 Relatório de Disciplinas",
            "🎓 Relatório de Cursos"
        ])
        
        with sub_rel_tab1:
            st.write("**Gerar Relatório Completo do Aluno**")
            
            # Buscar lista de alunos
            try:
                usuarios = listar("usuarios", "nome", "email", "matricula", "tipo_usuario")
                alunos = []
                if usuarios:
                    for u in usuarios:
                        if u and len(u) > 3 and u[3] == "aluno":
                            alunos.append((u[2], u[0], u[1]))  # (matricula, nome, email)
                
                if alunos:
                    # Selectbox para escolher aluno
                    opcoes_alunos = [f"(Matrícula: {matricula or 'N/A'}) - {nome}" for matricula, nome, email in alunos]
                    aluno_selecionado = st.selectbox("Selecione o Aluno", opcoes_alunos, key="aluno_rel_secretaria")
                    
                    # Extrair matrícula do aluno selecionado
                    matricula_secretaria = None
                    for matricula, nome, email in alunos:
                        if f"(Matrícula: {matricula or 'N/A'}) - {nome}" == aluno_selecionado:
                            matricula_secretaria = matricula
                            break
                    
                    if matricula_secretaria:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("📄 Gerar Relatório", use_container_width=True, key="btn_gerar_rel_sec"):
                                try:
                                    dados = buscar_dados_completos_aluno(matricula_secretaria)
                                    
                                    if dados and dados['aluno']:
                                        aluno = dados['aluno']
                                        st.info(f"📋 Relatório do Aluno - {aluno[1]}")
                                        st.write(f"**Matrícula:** {matricula_secretaria}")
                                        st.write(f"**Email:** {aluno[2] or 'N/A'}")
                                        
                                        # Notas
                                        if dados['notas']:
                                            st.subheader("📘 Notas por Disciplina")
                                            for nota_disc in dados['notas']:
                                                st.write(f"**{nota_disc['disciplina']}:**")
                                                col1, col2, col3 = st.columns(3)
                                                with col1:
                                                    st.metric("NP1", nota_disc['np1'] if nota_disc['np1'] else "-")
                                                with col2:
                                                    st.metric("NP2", nota_disc['np2'] if nota_disc['np2'] else "-")
                                                with col3:
                                                    st.metric("PIM", nota_disc['pim'] if nota_disc['pim'] else "-")
                                                st.divider()
                                        
                                        # Presenças
                                        if dados['presencas']:
                                            st.subheader("📅 Presenças")
                                            total_dias = len(dados['presencas'])
                                            dias_presentes = sum(1 for _, p in dados['presencas'] if p)
                                            percentual = (dias_presentes / total_dias * 100) if total_dias > 0 else 0
                                            
                                            col1, col2, col3 = st.columns(3)
                                            with col1:
                                                st.metric("Total de Dias", total_dias)
                                            with col2:
                                                st.metric("Dias Presentes", dias_presentes)
                                            with col3:
                                                st.metric("Taxa de Presença", f"{percentual:.1f}%")
                                            
                                            df_pres = pd.DataFrame(dados['presencas'], columns=["Data", "Presente"])
                                            df_pres["Status"] = df_pres["Presente"].apply(lambda x: "✅ Presente" if x else "❌ Faltou")
                                            st.dataframe(df_pres[["Data", "Status"]], use_container_width=True)
                                    else:
                                        st.error("❌ Aluno não encontrado!")
                                except Exception as e:
                                    st.error(f"❌ Erro ao gerar relatório: {str(e)}")
                        
                        with col2:
                            if not REPORTLAB_DISPONIVEL:
                                st.warning("⚠️ Biblioteca reportlab não instalada. Instale com: pip install reportlab")
                            else:
                                if st.button("📥 Download PDF", use_container_width=True, type="primary", key="btn_download_pdf_sec"):
                                    try:
                                        pdf_bytes = gerar_relatorio_pdf(matricula_secretaria)
                                        if pdf_bytes:
                                            nome_arquivo = f"relatorio_aluno_{matricula_secretaria}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                                            st.download_button(
                                                label="⬇️ Baixar Relatório PDF",
                                                data=pdf_bytes,
                                                file_name=nome_arquivo,
                                                mime="application/pdf",
                                                use_container_width=True
                                            )
                                            st.success("✅ PDF gerado com sucesso! Clique no botão acima para baixar.")
                                        else:
                                            st.error("❌ Erro ao gerar PDF.")
                                    except Exception as e:
                                        st.error(f"❌ Erro ao gerar PDF: {str(e)}")
                else:
                    st.warning("⚠️ Nenhum aluno cadastrado no sistema.")
            except Exception as e:
                st.error(f"❌ Erro ao buscar alunos: {str(e)}")
        
        with sub_rel_tab2:
            st.write("**Relatório de Turmas**")
            
            try:
                dados_relatorio_turmas, total_turmas, total_alunos_geral, media_alunos = gerar_dados_relatorio_turmas()
                
                if dados_relatorio_turmas is not None:
                    # Exibir estatísticas gerais
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Turmas", total_turmas)
                    with col2:
                        st.metric("Total de Alunos", total_alunos_geral)
                    with col3:
                        st.metric("Média de Alunos por Turma", f"{media_alunos:.1f}")
                    
                    st.divider()
                    
                    # Exibir tabela de turmas
                    df_turmas = pd.DataFrame(dados_relatorio_turmas)
                    st.dataframe(df_turmas, use_container_width=True, hide_index=True)
                    
                    # Botão para exportar
                    if st.button("📥 Exportar Relatório (CSV)", use_container_width=True, key="btn_exportar_turmas"):
                        csv = df_turmas.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Baixar CSV",
                            data=csv,
                            file_name=f"relatorio_turmas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                else:
                    st.info("ℹ️ Nenhuma turma cadastrada no sistema.")
            except Exception as e:
                st.error(f"❌ Erro ao gerar relatório: {str(e)}")
        
        with sub_rel_tab3:
            st.write("**Relatório de Disciplinas**")
            
            try:
                dados_relatorio_disc, total_disciplinas, total_carga_horaria, media_carga = gerar_dados_relatorio_disciplinas()
                
                if dados_relatorio_disc is not None:
                    # Exibir estatísticas gerais
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Disciplinas", total_disciplinas)
                    with col2:
                        st.metric("Total de Carga Horária", f"{total_carga_horaria}h")
                    with col3:
                        st.metric("Média de Carga Horária", f"{media_carga:.1f}h")
                    
                    st.divider()
                    
                    # Exibir tabela de disciplinas
                    df_disc = pd.DataFrame(dados_relatorio_disc)
                    st.dataframe(df_disc, use_container_width=True, hide_index=True)
                    
                    # Botão para exportar
                    if st.button("📥 Exportar Relatório (CSV)", use_container_width=True, key="btn_exportar_disc"):
                        csv = df_disc.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Baixar CSV",
                            data=csv,
                            file_name=f"relatorio_disciplinas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                else:
                    st.info("ℹ️ Nenhuma disciplina cadastrada no sistema.")
            except Exception as e:
                st.error(f"❌ Erro ao gerar relatório: {str(e)}")
        
        with sub_rel_tab4:
            st.write("**Relatório de Cursos**")
            
            try:
                dados_relatorio_cursos, total_cursos, total_turmas_curso = gerar_dados_relatorio_cursos()
                
                if dados_relatorio_cursos is not None:
                    # Exibir estatísticas gerais
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total de Cursos", total_cursos)
                    with col2:
                        st.metric("Total de Turmas", total_turmas_curso)
                    
                    st.divider()
                    
                    # Exibir tabela de cursos
                    df_cursos = pd.DataFrame(dados_relatorio_cursos)
                    st.dataframe(df_cursos, use_container_width=True, hide_index=True)
                    
                    # Botão para exportar
                    if st.button("📥 Exportar Relatório (CSV)", use_container_width=True, key="btn_exportar_cursos"):
                        csv = df_cursos.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Baixar CSV",
                            data=csv,
                            file_name=f"relatorio_cursos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                else:
                    st.info("ℹ️ Nenhum curso cadastrado no sistema.")
            except Exception as e:
                st.error(f"❌ Erro ao gerar relatório: {str(e)}")
    
    with tab6:
        chat_aba(contexto="secretaria")
