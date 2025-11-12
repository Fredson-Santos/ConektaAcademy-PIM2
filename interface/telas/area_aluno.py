"""
Módulo da Área do Aluno
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Imports das funções do sistema
from sistema.funcoes import *
from sistema import database as db
from sistema.relatorios import gerar_relatorio_pdf
from interface.telas.login import chat_aba

# Tentar importar reportlab (opcional)
try:
    from reportlab.lib.pagesizes import letter, A4
    REPORTLAB_DISPONIVEL = True
except ImportError:
    REPORTLAB_DISPONIVEL = False

def area_aluno(aluno):
    """Área do Aluno"""
    # Buscar informações da turma e curso do aluno
    matricula = aluno[3]
    turma_nome = "N/A"
    curso_nome = "N/A"
    
    try:
        conn = db.conectar()
        cursor = conn.cursor()
        
        # Buscar turma_id e curso diretamente da tabela usuarios
        # (o curso é atualizado automaticamente quando o aluno é vinculado à turma)
        cursor.execute("SELECT turma_id, curso FROM usuarios WHERE matricula = ? AND tipo_usuario = 'aluno'", (matricula,))
        resultado = cursor.fetchone()
        
        if resultado:
            if resultado[0]:  # turma_id
                turma_nome = resultado[0]
            if resultado[1]:  # curso
                curso_nome = resultado[1]
        
        conn.close()
    except Exception as e:
        # Em caso de erro, manter valores padrão
        pass
    
    st.markdown(f"""
    <div class="user-card">
        <h3>🎓 Bem-vindo, {aluno[1]}!</h3>
        <div style="display: flex; gap: 30px; flex-wrap: wrap; margin-top: 10px;">
            <p style="margin: 0;"><strong>Matrícula:</strong> {matricula}</p>
            <p style="margin: 0;"><strong>Curso:</strong> {curso_nome}</p>
            <p style="margin: 0;"><strong>Turma:</strong> {turma_nome}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📘 Notas", "📅 Presenças", "📖 Cronograma", "📔 Bloco do Aluno", "📄 Relatórios", "💬 Chat de Ajuda"])
    
    with tab1:
        st.subheader("Minhas Notas")
        
        # Buscar disciplinas vinculadas ao aluno
        disciplinas_aluno = buscar_disciplinas_por_aluno(aluno[3])
        
        if not disciplinas_aluno:
            st.warning("⚠️ Você não está vinculado a nenhuma disciplina. Entre em contato com a secretaria.")
        else:
            # Preparar dados para a tabela
            dados_tabela_notas = []
            for disc in disciplinas_aluno:
                disciplina_id = disc[0]
                disciplina_nome = disc[1]
                curso_nome = disc[3]
                disciplina_completa = f"{disciplina_nome} - {curso_nome}"
                
                # Buscar notas do aluno nesta disciplina
                notas = consultar_notas_por_disciplina(disciplina_id, aluno[3])
                
                np1 = notas[0] if notas and notas[0] is not None else None
                np2 = notas[1] if notas and notas[1] is not None else None
                pim = notas[2] if notas and notas[2] is not None else None
                
                # Calcular média
                media = None
                if np1 is not None and np2 is not None and pim is not None:
                    media = (np1 + np2 + pim) / 3
                elif notas:
                    notas_validas = [n for n in [np1, np2, pim] if n is not None]
                    if notas_validas:
                        media = sum(notas_validas) / len(notas_validas)
                
                # Formatar notas
                np1_str = f"{np1:.1f}" if np1 is not None else "-"
                np2_str = f"{np2:.1f}" if np2 is not None else "-"
                pim_str = f"{pim:.1f}" if pim is not None else "-"
                media_str = f"{media:.1f}" if media is not None else "-"
                
                dados_tabela_notas.append({
                    'Disciplina': disciplina_completa,
                    'NP1': np1_str,
                    'NP2': np2_str,
                    'PIM': pim_str,
                    'Média': media_str,
                    'media_valor': media  # Para uso na formatação de cores
                })
            
            # Exibir tabela
            if dados_tabela_notas:
                df_notas_aluno = pd.DataFrame(dados_tabela_notas)
                
                # Criar estilos CSS para cores condicionais
                st.markdown("""
                <style>
                    .nota-baixa {
                        background-color: #ffebee;
                        color: #c62828;
                    }
                    .nota-alta {
                        background-color: #e8f5e9;
                        color: #2e7d32;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                # Exibir tabela com formatação condicional
                for idx, row in df_notas_aluno.iterrows():
                    media_valor = row['media_valor']
                    
                    if media_valor is not None:
                        if media_valor < 7:
                            cor_fundo = "#ffebee"
                            cor_texto = "#c62828"
                        else:
                            cor_fundo = "#e8f5e9"
                            cor_texto = "#2e7d32"
                        
                        st.markdown(f"""
                        <div style="background-color: {cor_fundo}; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {cor_texto};">
                            <h4 style="color: {cor_texto}; margin-top: 0;">{row['Disciplina']}</h4>
                            <div style="display: flex; gap: 20px;">
                                <div><strong>NP1:</strong> {row['NP1']}</div>
                                <div><strong>NP2:</strong> {row['NP2']}</div>
                                <div><strong>PIM:</strong> {row['PIM']}</div>
                                <div><strong>Média:</strong> <span style="font-size: 1.2em; font-weight: bold; color: {cor_texto};">{row['Média']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                            <h4 style="margin-top: 0;">{row['Disciplina']}</h4>
                            <div style="display: flex; gap: 20px;">
                                <div><strong>NP1:</strong> {row['NP1']}</div>
                                <div><strong>NP2:</strong> {row['NP2']}</div>
                                <div><strong>PIM:</strong> {row['PIM']}</div>
                                <div><strong>Média:</strong> {row['Média']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Nenhuma nota registrada ainda.")
    
    with tab2:
        st.subheader("Minhas Presenças")
        presencas = consultar_presenca(aluno[3])
        
        if presencas:
            df = pd.DataFrame(presencas, columns=["Data", "Presente"])
            df["Status"] = df["Presente"].apply(lambda x: "✅ Presente" if x else "❌ Faltou")
            
            # Contar presenças
            total_dias = len(presencas)
            dias_presentes = sum(1 for _, p in presencas if p)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Dias", total_dias)
            with col2:
                st.metric("Dias Presentes", dias_presentes)
            with col3:
                percentual = (dias_presentes / total_dias * 100) if total_dias > 0 else 0
                st.metric("Taxa de Presença", f"{percentual:.1f}%")
            
            st.dataframe(df[["Data", "Status"]], use_container_width=True)
        else:
            st.info("ℹ️ Nenhum registro de presença ainda.")
    
    with tab3:
        st.subheader("Cronograma de Aulas")
        cronogramas = consultar_cronograma()
        
        if cronogramas:
            df = pd.DataFrame(cronogramas, columns=["Sala", "Data", "Dia da Semana", "Conteúdo"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("ℹ️ Nenhuma aula agendada no cronograma.")
    
    with tab4:
        st.subheader("📔 Bloco do Aluno")
        st.write("Use este espaço para fazer suas anotações pessoais.")
        
        arquivo = f"bloco_{aluno[3]}.txt"
        
        # Ler anotações existentes
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                anotacoes_existentes = f.read()
        except:
            anotacoes_existentes = ""
        
        # Textarea para novas anotações
        nova_anotacao = st.text_area(
            "Digite suas anotações:",
            value=anotacoes_existentes,
            height=300,
            placeholder="Digite suas anotações aqui..."
        )
        
        if st.button("💾 Salvar Anotações", use_container_width=True, type="primary", key="btn_salvar_anotacoes_aluno"):
            try:
                with open(arquivo, "w", encoding="utf-8") as f:
                    f.write(nova_anotacao)
                st.success("✅ Anotações salvas com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")
    
    with tab5:
        st.subheader("📄 Meus Relatórios")
        
        # Buscar dados completos do aluno
        dados_completos = buscar_dados_completos_aluno(matricula)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Relatório Completo**")
            
            if dados_completos and dados_completos['aluno']:
                aluno_info = dados_completos['aluno']
                
                # Informações do aluno
                st.markdown("### 👤 Informações do Aluno")
                st.write(f"**Nome:** {aluno_info[1]}")
                st.write(f"**Email:** {aluno_info[2] or 'N/A'}")
                st.write(f"**Matrícula:** {matricula}")
                st.write(f"**Curso:** {curso_nome}")
                st.write(f"**Turma:** {turma_nome}")
                
                st.divider()
                
                # Relatório de Notas
                st.markdown("### 📘 Relatório de Notas")
                disciplinas_aluno_rel = buscar_disciplinas_por_aluno(matricula)
                
                if disciplinas_aluno_rel:
                    dados_notas_rel = []
                    for disc in disciplinas_aluno_rel:
                        disciplina_id = disc[0]
                        disciplina_nome = disc[1]
                        curso_nome_disc = disc[3]
                        disciplina_completa = f"{disciplina_nome} - {curso_nome_disc}"
                        
                        notas = consultar_notas_por_disciplina(disciplina_id, matricula)
                        
                        np1 = notas[0] if notas and notas[0] is not None else None
                        np2 = notas[1] if notas and notas[1] is not None else None
                        pim = notas[2] if notas and notas[2] is not None else None
                        
                        # Calcular média
                        media = None
                        if np1 is not None and np2 is not None and pim is not None:
                            media = (np1 + np2 + pim) / 3
                        elif notas:
                            notas_validas = [n for n in [np1, np2, pim] if n is not None]
                            if notas_validas:
                                media = sum(notas_validas) / len(notas_validas)
                        
                        dados_notas_rel.append({
                            'Disciplina': disciplina_completa,
                            'NP1': f"{np1:.1f}" if np1 is not None else "-",
                            'NP2': f"{np2:.1f}" if np2 is not None else "-",
                            'PIM': f"{pim:.1f}" if pim is not None else "-",
                            'Média': f"{media:.1f}" if media is not None else "-"
                        })
                    
                    df_notas_rel = pd.DataFrame(dados_notas_rel)
                    st.dataframe(df_notas_rel, use_container_width=True, hide_index=True)
                else:
                    st.info("ℹ️ Nenhuma disciplina vinculada.")
                
                st.divider()
                
                # Relatório de Faltas
                st.markdown("### 📅 Relatório de Faltas")
                presencas_rel = consultar_presenca(matricula)
                
                if presencas_rel:
                    total_dias_rel = len(presencas_rel)
                    dias_presentes_rel = sum(1 for _, p in presencas_rel if p)
                    dias_faltas_rel = total_dias_rel - dias_presentes_rel
                    percentual_rel = (dias_presentes_rel / total_dias_rel * 100) if total_dias_rel > 0 else 0
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total de Dias", total_dias_rel)
                    with col2:
                        st.metric("Dias Presentes", dias_presentes_rel)
                    with col3:
                        st.metric("Dias de Faltas", dias_faltas_rel)
                    with col4:
                        st.metric("Taxa de Presença", f"{percentual_rel:.1f}%")
                    
                    # Tabela de presenças
                    df_pres_rel = pd.DataFrame(presencas_rel, columns=["Data", "Presente"])
                    df_pres_rel["Status"] = df_pres_rel["Presente"].apply(lambda x: "✅ Presente" if x else "❌ Faltou")
                    st.dataframe(df_pres_rel[["Data", "Status"]], use_container_width=True, hide_index=True)
                else:
                    st.info("ℹ️ Nenhum registro de presença ainda.")
            else:
                st.warning("⚠️ Não foi possível carregar os dados do aluno.")
        
        with col2:
            st.write("**Download de Boletim**")
            
            if not REPORTLAB_DISPONIVEL:
                st.warning("⚠️ Biblioteca reportlab não instalada. Instale com: pip install reportlab")
            else:
                if st.button("📥 Baixar Boletim PDF", use_container_width=True, type="primary", key="btn_download_boletim_aluno"):
                    try:
                        pdf_bytes = gerar_relatorio_pdf(matricula)
                        if pdf_bytes:
                            nome_arquivo = f"boletim_{matricula}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                            st.download_button(
                                label="⬇️ Baixar Boletim PDF",
                                data=pdf_bytes,
                                file_name=nome_arquivo,
                                mime="application/pdf",
                                use_container_width=True,
                                key="btn_download_pdf_aluno"
                            )
                            st.success("✅ Boletim gerado com sucesso! Clique no botão acima para baixar.")
                        else:
                            st.error("❌ Erro ao gerar boletim. Verifique se há dados disponíveis.")
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar boletim: {str(e)}")
    
    with tab6:
        chat_aba(contexto="aluno")

