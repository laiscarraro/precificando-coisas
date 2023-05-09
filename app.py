import streamlit as st
import plotly.express as px
from google_shopping import *

st.set_page_config(layout="wide")

st.title('Precificação de qualquer coisa!')

query = st.text_input('O que você quer precificar?')
df = get_products(search(query))

st.markdown('## Preço sugerido')
preco_sugerido = st.slider(
    label = 'Estratégia de cálculo: mediana',
    min_value = float(df.preco.min()),
    max_value = float(df.preco.max()),
    value = float(df.preco.median()),
    step = 0.1
)

histograma = px.histogram(df.preco)
histograma.add_vline(preco_sugerido)

c1, c2 = st.columns(2)
st.dataframe(df)
st.plotly_chart(
    histograma,
    use_container_width=True
)