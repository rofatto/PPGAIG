import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Formulário de Seleção", layout="centered")

st.title("Formulário de Seleção de Linha de Pesquisa")
st.markdown("Por favor, preencha as informações abaixo:")

# Entradas do formulário
nome = st.text_input("Nome completo")
email = st.text_input("Email")
cpf = st.text_input("CPF")
data_nascimento = st.date_input("Data de Nascimento")
ano_conclusao = st.number_input("Ano de Conclusão do Curso de Graduação", min_value=1950, max_value=2100, step=1)

# Seleção da linha de pesquisa
linha = st.radio("Selecione apenas 1 (uma) linha de pesquisa:", [
    "Linha 1: Desenvolvimento e aplicações de métodos em informações geoespaciais",
    "Linha 2: Sistemas integrados de produção vegetal"
])

# Subáreas por linha
subareas_l1 = [
    "Sensoriamento Remoto de Sistemas Agrícolas",
    "Desenvolvimento de sistemas de mapeamento móvel. Utilização de aeronaves remotamente pilotadas na Fitotecnia",
    "Sistemas computacionais inteligentes na agricultura e informações geoespaciais",
    "Posicionamento por GNSS. Modelagem e análise de dados geoespaciais. Controle de qualidade de informações geoespaciais",
    "Sensores Aplicados a Agricultura de Precisão"
]

subareas_l2 = [
    "Biotecnologia na agricultura",
    "Recursos florestais",
    "Nutrição, Manejo e cultura de tecidos em hortaliças e plantas medicinais",
    "Micologia Aplicada. Patologia Florestal. Patologia de Sementes. Sensoriamento remoto aplicado à Patologia Florestal",
    "Nutrição mineral e metabolismo de plantas",
    "Manejo integrado de plantas daninhas. Uso de herbicidas na Agricultura. Sistemas de informação para controle de plantas",
    "Microbiologia agrícola",
    "Controle biológico de doenças de plantas. Controle biológico de plantas daninhas. Sensoriamento remoto aplicado à Fitopatologia",
    "Mecanização agrícola. Tecnologia de aplicação de precisão",
    "Manejo da água em sistemas agrícolas irrigados",
    "Melhoramento genético de hortaliças e fenotipagem de alto desempenho",
    "Entomologia agrícola: manejo integrado, controle biológico, controle microbiano",
    "Tecnologias aplicadas à cafeicultura"
]

st.markdown("---")

# Classificação das subáreas
st.subheader("Classifique as subáreas por ordem de preferência")
subarea_df = pd.DataFrame()

if "Linha 1" in linha:
    selected_order = [st.number_input(sub, min_value=1, max_value=5, step=1, key=sub) for sub in subareas_l1]
    subarea_df = pd.DataFrame({"Subárea": subareas_l1, "Ordem de preferência": selected_order})
elif "Linha 2" in linha:
    selected_order = [st.number_input(sub, min_value=1, max_value=13, step=1, key=sub) for sub in subareas_l2]
    subarea_df = pd.DataFrame({"Subárea": subareas_l2, "Ordem de preferência": selected_order})

# Função para gerar PDF
def gerar_pdf(nome, email, cpf, data_nascimento, ano_conclusao, linha, subarea_df):
    nome_arquivo = "formulario_selecao_linha_pesquisa_subarea.pdf"
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Relatório de Escolha de Linha de Pesquisa", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Nome:</b> {nome}", styles['Normal']))
    elements.append(Paragraph(f"<b>Email:</b> {email}", styles['Normal']))
    elements.append(Paragraph(f"<b>CPF:</b> {cpf}", styles['Normal']))
    elements.append(Paragraph(f"<b>Data de Nascimento:</b> {data_nascimento.strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Paragraph(f"<b>Ano de Conclusão do Curso de Graduação:</b> {ano_conclusao}", styles['Normal']))
    elements.append(Paragraph(f"<b>Linha de Pesquisa Selecionada:</b> {linha}", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Subáreas por ordem de preferência:</b>", styles['Heading4']))

    subarea_df_sorted = subarea_df.sort_values(by="Ordem de preferência")
    for _, row in subarea_df_sorted.iterrows():
        texto = f"{int(row['Ordem de preferência'])}. {row['Subárea']}"
        elements.append(Paragraph(texto, styles['Normal']))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    return nome_arquivo

# Botão de envio
if st.button("Enviar"):
    if not nome.strip() or not email.strip() or not cpf.strip():
        st.warning("Por favor, preencha todos os campos obrigatórios (Nome, Email, CPF).")
    elif subarea_df["Ordem de preferência"].duplicated().any():
        st.error("Cada subárea deve ter uma ordem de preferência única. Verifique os valores duplicados.")
    else:
        subarea_df.insert(0, "Linha de Pesquisa", linha)
        subarea_df.insert(0, "Ano de Conclusão", ano_conclusao)
        subarea_df.insert(0, "Data de Nascimento", data_nascimento)
        subarea_df.insert(0, "CPF", cpf.strip())
        subarea_df.insert(0, "Email", email.strip())
        subarea_df.insert(0, "Nome", nome.strip())
        st.success("Respostas registradas com sucesso!")
        st.dataframe(subarea_df)

        # Gerar PDF
        pdf_path = gerar_pdf(nome.strip(), email.strip(), cpf.strip(), data_nascimento, ano_conclusao, linha, subarea_df)
        with open(pdf_path, "rb") as f:
            st.download_button("Baixar relatório em PDF", f.read(), file_name=pdf_path, mime="application/pdf")
