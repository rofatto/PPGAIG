
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
    "a) Sensoriamento Remoto de Sistemas Agrícolas",
    "b) Mapeamento móvel e ARP na Fitotecnia",
    "c) Sistemas computacionais inteligentes",
    "d) GNSS, modelagem, controle de qualidade",
    "e) Sensores na Agricultura de Precisão"
]

subareas_l2 = [
    "a) Biotecnologia na agricultura",
    "b) Recursos florestais",
    "c) Hortaliças e plantas medicinais",
    "d) Patologia florestal e sensoriamento",
    "e) Nutrição mineral e metabolismo",
    "f) Manejo de plantas daninhas e herbicidas",
    "g) Microbiologia agrícola",
    "h) Controle biológico e sensoriamento",
    "i) Mecanização e aplicação de precisão",
    "j) Manejo da água em sistemas irrigados",
    "k) Melhoramento e fenotipagem de hortaliças",
    "l) Entomologia agrícola",
    "m) Tecnologias na cafeicultura"
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
