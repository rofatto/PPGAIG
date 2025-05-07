import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Formulário de Seleção", layout="centered")

st.title("Formulário de Seleção de Linha de Pesquisa")
st.markdown("Por favor, preencha as informações abaixo:")

# Entrada do nome
nome = st.text_input("Nome completo")

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
    "Nutrição. Manejo e cultura de tecidos em hortaliças e plantas medicinais",
    "Micologia Aplicada. Patologia Florestal. Patologia de Sementes. Sensoriamento remoto aplicado à Patologia Florestal",
    "Nutrição mineral e metabolismo de plantas",
    "Manejo integrado de plantas daninhas. Uso de herbicidas na Agricultura. Sistemas de informação para controle de plantas",
    "Microbiologia agrícola",
    "Controle biológico de doenças de plantas. Controle biológico de plantas daninhas. Sensoriamento remoto aplicado à Fitopatologia",
    "Mecanização agrícola. Tecnologia de aplicação de precisão",
    "Manejo da água em sistemas agrícolas irrigados",
    "Melhoramento genético de hortaliças e fenotipagem de alto desempenho",
    "Entomologia agrícola: manejo integrado. controle biológico. controle microbiano",
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

# Função para gerar PDF com reportlab
def gerar_pdf(nome, linha, subarea_df):
    caminho_pdf = f"resposta_{nome.replace(' ', '_')}.pdf"
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 50, "Relatório de Escolha de Linha de Pesquisa")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Nome: {nome}")
    c.drawString(50, height - 120, f"Linha de Pesquisa Selecionada: {linha}")
    c.drawString(50, height - 150, "Subáreas por ordem de preferência:")

    y = height - 170
    subarea_df_sorted = subarea_df.sort_values(by="Ordem de preferência")
    for idx, row in subarea_df_sorted.iterrows():
        texto = f"{row['Ordem de preferência']}. {row['Subárea']}"
        c.drawString(60, y, texto)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    return caminho_pdf

# Botão de envio
if st.button("Enviar"):
    if not nome.strip():
        st.warning("Por favor, preencha o nome.")
    elif subarea_df["Ordem de preferência"].duplicated().any():
        st.error("Cada subárea deve ter uma ordem de preferência única. Verifique os valores duplicados.")
    else:
        subarea_df.insert(0, "Linha de Pesquisa", linha)
        subarea_df.insert(0, "Nome", nome.strip())
        st.success("Respostas registradas com sucesso!")
        st.dataframe(subarea_df)

        # Gerar CSV
        csv = subarea_df.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar respostas em CSV", csv, file_name=f"resposta_{nome.replace(' ', '_')}.csv")

        # Gerar PDF com reportlab
        pdf_path = gerar_pdf(nome.strip(), linha, subarea_df)
        with open(pdf_path, "rb") as f:
            st.download_button("Baixar relatório em PDF", f.read(), file_name=pdf_path, mime="application/pdf")
