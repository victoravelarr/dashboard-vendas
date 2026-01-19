# 1. importar bibliotecas
# 2. carregar base
# 3. tratar dados (data, mes, ano)
# 4. criar filtros
# 5. criar métricas
# 6. criar gráficos


import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_excel("dados_vendas_grande.xlsx")

df["faturamento"] = df["valor"] * df["quantidade"]

st.title("Resumo de Vendas")
st.caption("Visão geral do faturamento e desempenho por produto e período")
st.subheader("Filtros")

df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month

col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

with col_filtro1:
    meses = st.multiselect("Mês", sorted(df["mes"].unique()))

with col_filtro2:
    anos = st.multiselect("Ano", sorted(df["ano"].unique()))

with col_filtro3:
    produtos = st.multiselect("Produto(s)", sorted(df["produto"].unique()))


if anos:
    df = df[df["ano"].isin(anos)]

if meses:
    df = df[df["mes"].isin(meses)]

if produtos:
    df = df[df["produto"].isin(produtos)]





st.divider()

# 3 metricas
    # Faturamento total(centralizado)
col_esq, col_centro, col_dir = st.columns([1, 2, 1])

with col_centro:
    st.metric("Faturamento total",f"R$ {df['faturamento'].sum():,.2f}")

    # qntd vendida e ticket medio(um do lado do outro)
col1, col2 = st.columns(2)

with col1:
    st.metric("Quantidade vendida", f"{df['quantidade'].sum():,}")

with col2:
    ticket_medio = df["faturamento"].sum() / df["quantidade"].sum()
    st.metric("Ticket médio", f"R$ {ticket_medio:,.2f}")

# graficos
    #linha
st.subheader("Evolução das Vendas")
st.bar_chart(df.groupby("data")["faturamento"].sum())

# pizza
st.subheader("Distribuição por Produto")

faturamento_produto = (df.groupby("produto", as_index=False)["faturamento"].sum())

fig = px.pie(faturamento_produto, names="produto", values="faturamento", title="Participação no Faturamento por Produto")

# 🔹 ajustes visuais
fig.update_traces(textinfo="percent+label", textfont_size=17, textposition="inside")

fig.update_traces(pull=[0.05 if i == faturamento_produto["faturamento"].idxmax() else 0 for i in range(len(faturamento_produto))])

st.plotly_chart(fig, use_container_width=True)
