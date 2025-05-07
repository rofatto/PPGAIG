
import streamlit as st
import pandas as pd

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
    "Desenvolvimento de sistemas de mapeamento móvel; Utilização de aeronaves remotamente pilotadas na Fitotecnia",
    "Sistemas computacionais inteligentes na agricultura e informações geoespaciais",
    "Posicionamento por GNSS; Modelagem e análise de dados geoespaciais; Controle de qualidade de informações geoespaciais",
    "Sensores Aplicados a Agricultura de Precisão"
]

subareas_l2 = [
    "Biotecnologia na agricultura",
    "Recursos florestais",
    "Nutrição, manejo e cultura de tecidos em hortaliças e plantas medicinais",
    "Micologia Aplicada; Patologia Florestal; Patologia de Sementes; Sensoriamento remoto aplicado à Patologia Florestal",
    "Nutrição mineral e metabolismo de plantas",
    "Manejo integrado de plantas daninhas. Uso de herbicidas na Agricultura. Sistemas de informação para controle de plantas",
    "Microbiologia agrícola",
    "Controle biológico de doenças de plantas; Controle biológico de plantas daninhas; Sensoriamento remoto aplicado à Fitopatologia",
    "Mecanização agrícola; Tecnologia de aplicação de precisão",
    "Manejo da água em sistemas agrícolas irrigados",
    "Melhoramento genético de hortaliças e fenotipagem de alto desempenho",
    "Entomologia agrícola: manejo integrado, controle biológico, controle microbiano",
    "Tecnologias aplicadas à cafeicultura"
]

st.markdown("---")

# Classificação das subáreas
st.subheader("Classifique as subáreas por ordem de preferência")
if "Linha 1" in linha:
    selected_order = [st.number_input(sub, min_value=1, max_value=5, step=1, key=sub) for sub in subareas_l1]
    subarea_df = pd.DataFrame({"Subárea": subareas_l1, "Ordem de preferência": selected_order})
elif "Linha 2" in linha:
    selected_order = [st.number_input(sub, min_value=1, max_value=13, step=1, key=sub) for sub in subareas_l2]
    subarea_df = pd.DataFrame({"Subárea": subareas_l2, "Ordem de preferência": selected_order})

# Botão de envio
if st.button("Enviar"):
    if not nome.strip():
        st.warning("Por favor, preencha o nome.")
    else:
        subarea_df.insert(0, "Linha de Pesquisa", linha)
        subarea_df.insert(0, "Nome", nome.strip())
        st.success("Respostas registradas com sucesso!")
        st.dataframe(subarea_df)
        csv = subarea_df.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar respostas em CSV", csv, file_name=f"resposta_{nome.replace(' ', '_')}.csv")
