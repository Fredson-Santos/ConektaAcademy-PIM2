"""
Módulo da Área do Professor
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Imports das funções do sistema
from sistema.funcoes import *
from interface.telas.login import chat_aba
from sistema.relatorios import gerar_relatorio_pdf

# Tentar importar reportlab (opcional)
try:
    from reportlab.lib.pagesizes import letter, A4
    REPORTLAB_DISPONIVEL = True
except ImportError:
    REPORTLAB_DISPONIVEL = False

def area_professor(professor):
    """Área do Professor"""
    professor_id = professor[0]
    
    # Buscar disciplinas do professor
    disciplinas_prof = buscar_disciplinas_por_professor(professor_id)
    # Formatar: "Nome da Disciplina - Nome do Curso"
    disciplinas_nomes = [f"{disc[1]} - {disc[3]}" for disc in disciplinas_prof] if disciplinas_prof else []
    
    st.markdown(f"""
    <div class="user-card">
        <h3>👨‍🏫 Bem-vindo, Professor {professor[1]}!</h3>
        <p>Email: {professor[2]} | Disciplinas: {len(disciplinas_nomes)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Minhas Disciplinas",
        "📄 Relatórios",
        "📖 Cronograma",
        "🗒️ Bloco do Professor",
        "💬 Chat de Ajuda"
    ])
    
    with tab1:
        st.subheader("Minhas Disciplinas")
        
        if not disciplinas_prof:
            st.warning("⚠️ Você não possui disciplinas vinculadas. Entre em contato com a secretaria.")
        else:
            sub_tab1, sub_tab2 = st.tabs(["📘 Lançar Notas", "📅 Presença"])
            
            with sub_tab1:
                st.write("**Lançamento de Notas**")
                
                col1, col2 = st.columns(2)
                with col1:
                    disciplina_selec = st.selectbox("Disciplina", disciplinas_nomes, key="disc_lancar")
                    
                    # Encontrar ID da disciplina (comparar com o formato "Nome - Curso")
                    disciplina_id_lancar = None
                    for disc in disciplinas_prof:
                        disc_formatada = f"{disc[1]} - {disc[3]}"
                        if disc_formatada == disciplina_selec:
                            disciplina_id_lancar = disc[0]
                            break
                    
                    # Buscar alunos da disciplina selecionada
                    alunos_disciplina = []
                    if disciplina_id_lancar:
                        alunos_disciplina = buscar_alunos_por_disciplina(disciplina_id_lancar)
                    
                    if alunos_disciplina:
                        opcoes_alunos_disc = [f"(Matrícula: {aluno[1] or 'N/A'}) - {aluno[0]}" for aluno in alunos_disciplina]
                        aluno_selec = st.selectbox("Selecione o Aluno", opcoes_alunos_disc, key="aluno_selec_nota")
                        
                        # Extrair matrícula do aluno selecionado
                        matricula_aluno = None
                        for aluno in alunos_disciplina:
                            if f"(Matrícula: {aluno[1] or 'N/A'}) - {aluno[0]}" == aluno_selec:
                                matricula_aluno = aluno[1]
                                break
                    else:
                        st.info("ℹ️ Nenhum aluno vinculado a esta disciplina. Verifique se a disciplina está vinculada a uma turma e se há alunos nessa turma.")
                        matricula_aluno = None
                
                with col2:
                    tipo_nota = st.selectbox("Tipo de Nota", ["NP1", "NP2", "PIM"], key="tipo_nota")
                    nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1, key="nota_valor")
                
                if st.button("✅ Lançar Nota", use_container_width=True, type="primary", key="btn_lancar_nota"):
                    if not matricula_aluno:
                        st.error("❌ Por favor, selecione um aluno!")
                    elif not disciplina_id_lancar:
                        st.error("❌ Erro ao selecionar disciplina!")
                    else:
                        try:
                            # Preparar valores para cada tipo de nota
                            np1 = nota if tipo_nota == "NP1" else None
                            np2 = nota if tipo_nota == "NP2" else None
                            pim = nota if tipo_nota == "PIM" else None
                            
                            cadastrar_nota_por_disciplina(disciplina_id_lancar, matricula_aluno, np1, np2, pim)
                            st.success(f"✅ Nota {nota} lançada com sucesso para {tipo_nota} em {disciplina_selec}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao lançar nota: {str(e)}")
                
                # Lista de alunos e notas
                st.divider()
                st.subheader("📊 Lista de Alunos e Notas")
                
                if disciplina_id_lancar:
                    notas_alunos = listar_notas_disciplina(disciplina_id_lancar)
                    
                    if notas_alunos:
                        # Preparar dados para a tabela
                        dados_tabela = []
                        for aluno_nota in notas_alunos:
                            np1_str = f"{aluno_nota['np1']:.1f}" if aluno_nota['np1'] is not None else "-"
                            np2_str = f"{aluno_nota['np2']:.1f}" if aluno_nota['np2'] is not None else "-"
                            pim_str = f"{aluno_nota['pim']:.1f}" if aluno_nota['pim'] is not None else "-"
                            media_str = f"{aluno_nota['media']:.1f}" if aluno_nota['media'] is not None else "-"
                            
                            aluno_formatado = f"(Matrícula: {aluno_nota['matricula'] or 'N/A'}) - {aluno_nota['nome']}"
                            dados_tabela.append({
                                'Aluno': aluno_formatado,
                                'NP1': np1_str,
                                'NP2': np2_str,
                                'PIM': pim_str,
                                'Média': media_str
                            })
                        
                        # Exibir tabela
                        df_notas = pd.DataFrame(dados_tabela)
                        st.dataframe(df_notas, use_container_width=True, hide_index=True)
                    else:
                        st.info("ℹ️ Nenhum aluno encontrado nesta disciplina.")
                else:
                    st.info("ℹ️ Selecione uma disciplina para ver as notas dos alunos.")
            
            with sub_tab2:
                st.write("**Atualizar Presença**")
                
                # Selecionar disciplina
                disciplina_pres = st.selectbox("Disciplina", disciplinas_nomes, key="disc_pres")
                
                # Encontrar ID da disciplina (comparar com o formato "Nome - Curso")
                disciplina_id_pres = None
                for disc in disciplinas_prof:
                    disc_formatada = f"{disc[1]} - {disc[3]}"
                    if disc_formatada == disciplina_pres:
                        disciplina_id_pres = disc[0]
                        break
                
                # Buscar alunos da disciplina selecionada
                alunos_disciplina_pres = []
                if disciplina_id_pres:
                    alunos_disciplina_pres = buscar_alunos_por_disciplina(disciplina_id_pres)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if alunos_disciplina_pres:
                        opcoes_alunos_pres = [f"(Matrícula: {aluno[1] or 'N/A'}) - {aluno[0]}" for aluno in alunos_disciplina_pres]
                        aluno_selec_pres = st.selectbox("Selecione o Aluno", opcoes_alunos_pres, key="aluno_selec_pres")
                        
                        # Extrair matrícula do aluno selecionado
                        matricula_pres = None
                        for aluno in alunos_disciplina_pres:
                            if f"(Matrícula: {aluno[1] or 'N/A'}) - {aluno[0]}" == aluno_selec_pres:
                                matricula_pres = aluno[1]
                                break
                    else:
                        st.info("ℹ️ Nenhum aluno vinculado a esta disciplina.")
                        matricula_pres = None
                with col2:
                    data_pres = st.date_input("Data", value=datetime.now(), key="data_pres_prof")
                with col3:
                    presente = st.selectbox("Status", ["Presente", "Faltou"], key="status_pres")
                
                if st.button("✅ Atualizar Presença", use_container_width=True, type="primary", key="btn_atualizar_presenca"):
                    if not matricula_pres:
                        st.error("❌ Por favor, selecione um aluno!")
                    else:
                        try:
                            presente_bool = 1 if presente == "Presente" else 0
                            atualizar_presenca(matricula_pres, str(data_pres), presente_bool)
                            st.success(f"✅ Presença atualizada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao atualizar: {str(e)}")
                
                # Lista de presenças dos alunos
                st.divider()
                st.subheader("📊 Lista de Presenças")
                
                if disciplina_id_pres:
                    presencas_alunos = listar_presencas_disciplina(disciplina_id_pres)
                    
                    if presencas_alunos:
                        # Preparar dados para a tabela
                        dados_tabela_pres = []
                        for aluno_pres in presencas_alunos:
                            percentual_str = f"{aluno_pres['percentual']:.1f}%" if aluno_pres['total_aulas'] > 0 else "-"
                            
                            aluno_formatado_pres = f"(Matrícula: {aluno_pres['matricula'] or 'N/A'}) - {aluno_pres['nome']}"
                            dados_tabela_pres.append({
                                'Aluno': aluno_formatado_pres,
                                'Presentes': aluno_pres['presentes'],
                                'Faltas': aluno_pres['faltas'],
                                'Percentual de Presença': percentual_str
                            })
                        
                        # Exibir tabela
                        df_presencas = pd.DataFrame(dados_tabela_pres)
                        st.dataframe(df_presencas, use_container_width=True, hide_index=True)
                    else:
                        st.info("ℹ️ Nenhum aluno encontrado nesta disciplina.")
                else:
                    st.info("ℹ️ Selecione uma disciplina para ver as presenças dos alunos.")
    
    with tab2:
        st.subheader("Gerar Relatório")
        
        if not disciplinas_prof:
            st.warning("⚠️ Você não possui disciplinas vinculadas.")
        else:
            matricula_rel = st.text_input("Matrícula do Aluno", placeholder="Digite a matrícula", key="matric_rel")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📄 Gerar Relatório", use_container_width=True, key="btn_gerar_rel_prof"):
                    if not matricula_rel:
                        st.error("❌ Por favor, digite a matrícula!")
                    else:
                        try:
                            st.info(f"📋 Relatório do Aluno - Matrícula: {matricula_rel}")
                            
                            # Buscar dados completos
                            dados = buscar_dados_completos_aluno(matricula_rel)
                            
                            if dados and dados['aluno']:
                                aluno = dados['aluno']
                                st.write(f"**Nome:** {aluno[1]}")
                                st.write(f"**Email:** {aluno[2] or 'N/A'}")
                                
                                # Mostrar notas de todas as disciplinas do professor
                                st.subheader("📘 Notas por Disciplina")
                                for disc in disciplinas_prof:
                                    disciplina_id = disc[0]
                                    disciplina_nome = disc[1]
                                    curso_nome = disc[3]
                                    disciplina_completa = f"{disciplina_nome} - {curso_nome}"
                                    notas = consultar_notas_por_disciplina(disciplina_id, matricula_rel)
                                    if notas and any(notas):
                                        st.write(f"**{disciplina_completa}:**")
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("NP1", notas[0] if notas[0] else "-")
                                        with col2:
                                            st.metric("NP2", notas[1] if notas[1] else "-")
                                        with col3:
                                            st.metric("PIM", notas[2] if notas[2] else "-")
                                        st.divider()
                                
                                # Presenças
                                presencas = consultar_presenca(matricula_rel)
                                if presencas:
                                    st.subheader("📅 Presenças")
                                    df_pres = pd.DataFrame(presencas, columns=["Data", "Presente"])
                                    df_pres["Status"] = df_pres["Presente"].apply(lambda x: "✅ Presente" if x else "❌ Faltou")
                                    
                                    # Estatísticas
                                    total_dias = len(presencas)
                                    dias_presentes = sum(1 for _, p in presencas if p)
                                    percentual = (dias_presentes / total_dias * 100) if total_dias > 0 else 0
                                    
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Total de Dias", total_dias)
                                    with col2:
                                        st.metric("Dias Presentes", dias_presentes)
                                    with col3:
                                        st.metric("Taxa de Presença", f"{percentual:.1f}%")
                                    
                                    st.dataframe(df_pres[["Data", "Status"]], use_container_width=True)
                                else:
                                    st.info("ℹ️ Sem registros de presença.")
                            else:
                                st.error("❌ Aluno não encontrado!")
                        except Exception as e:
                            st.error(f"❌ Erro ao gerar relatório: {str(e)}")
            
            with col2:
                if not REPORTLAB_DISPONIVEL:
                    st.warning("⚠️ Biblioteca reportlab não instalada. Instale com: pip install reportlab")
                else:
                    if st.button("📥 Download PDF", use_container_width=True, type="primary", key="btn_download_pdf_prof"):
                        if not matricula_rel:
                            st.error("❌ Por favor, digite a matrícula primeiro!")
                        else:
                            try:
                                pdf_bytes = gerar_relatorio_pdf(matricula_rel)
                                if pdf_bytes:
                                    nome_arquivo = f"relatorio_{matricula_rel}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                                    st.download_button(
                                        label="⬇️ Baixar Relatório PDF",
                                        data=pdf_bytes,
                                        file_name=nome_arquivo,
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                    st.success("✅ PDF gerado com sucesso! Clique no botão acima para baixar.")
                                else:
                                    st.error("❌ Erro ao gerar PDF. Verifique se o aluno existe.")
                            except Exception as e:
                                st.error(f"❌ Erro ao gerar PDF: {str(e)}")
    
    with tab3:
        st.subheader("Gerenciar Cronograma")
        
        sub_tab1, sub_tab2 = st.tabs(["Ver Cronograma", "Adicionar Aula"])
        
        with sub_tab1:
            cronogramas = consultar_cronograma()
            if cronogramas:
                df = pd.DataFrame(cronogramas, columns=["Sala", "Data", "Dia da Semana", "Conteúdo"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ Nenhuma aula agendada.")
        
        with sub_tab2:
            col1, col2 = st.columns(2)
            with col1:
                sala = st.text_input("Sala", placeholder="Ex: 101")
                data_aula = st.date_input("Data da Aula", value=datetime.now(), key="data_aula_prof")
            with col2:
                dia_semana = st.selectbox("Dia da Semana", 
                    ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], key="dia_semana_prof")
                conteudo = st.text_area("Conteúdo da Aula", placeholder="Digite o conteúdo da aula")
            
            if st.button("➕ Adicionar Aula", use_container_width=True, type="primary", key="btn_adicionar_aula"):
                if not sala or not conteudo:
                    st.error("❌ Por favor, preencha todos os campos!")
                else:
                    try:
                        adicionar_aula_cronograma(sala, str(data_aula), dia_semana, conteudo)
                        st.success("✅ Aula adicionada com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar: {str(e)}")
    
    with tab4:
        st.subheader("🗒️ Bloco do Professor")
        st.write("Use este espaço para anotações sobre suas aulas e alunos.")
        
        arquivo_prof = "bloco_professor.txt"
        
        try:
            with open(arquivo_prof, "r", encoding="utf-8") as f:
                anotacoes_prof = f.read()
        except:
            anotacoes_prof = ""
        
        nova_anotacao_prof = st.text_area(
            "Suas anotações:",
            value=anotacoes_prof,
            height=300,
            placeholder="Digite suas anotações aqui..."
        )
        
        if st.button("💾 Salvar Anotações", use_container_width=True, type="primary", key="save_prof"):
            try:
                with open(arquivo_prof, "w", encoding="utf-8") as f:
                    f.write(nova_anotacao_prof)
                st.success("✅ Anotações salvas com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")
    
    with tab5:
        chat_aba(contexto="professor")

