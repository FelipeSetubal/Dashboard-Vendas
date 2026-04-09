import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title("Dashboard de Vendas Profissional")

# Upload ou dados padrão

arquivo = st.file_uploader("Envie um CSV", type=["csv"])

if arquivo:
    df = pd.read_csv(arquivo)
else:
    st.info("Usando dados de exemplo...")
    df = pd.DataFrame({
        "data": ["2024-01-01", "2024-01-02", "2024-02-01"],
        "produto": ["Notebook", "Mouse", "Teclado"],
        "quantidade": [2, 5, 3],
        "preco": [3500, 80, 150]
    })


# Tratamento

df["data"] = pd.to_datetime(df["data"])
df["total"] = df["quantidade"] * df["preco"]

# Sidebar filtros

st.sidebar.header("Filtros")

produtos = st.sidebar.multiselect(
    "Produtos",
    df["produto"].unique(),
    default=df["produto"].unique()
)

data_inicio = st.sidebar.date_input("Data inicial", df["data"].min())
data_fim = st.sidebar.date_input("Data final", df["data"].max())

df = df[
    (df["produto"].isin(produtos)) &
    (df["data"] >= pd.to_datetime(data_inicio)) &
    (df["data"] <= pd.to_datetime(data_fim))
]

# Métricas

faturamento = df["total"].sum()
qtd = df["quantidade"].sum()
ticket = faturamento / qtd if qtd > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Faturamento", f"R$ {faturamento:,.2f}")
col2.metric("Quantidade", qtd)
col3.metric("Ticket Médio", f"R$ {ticket:,.2f}")

st.divider()

# Gráfico Produto

st.subheader("Vendas por Produto")

vendas_produto = df.groupby("produto")["total"].sum().reset_index()

fig1 = px.bar(vendas_produto, x="produto", y="total", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico tempo

st.subheader("Evolução das Vendas")

df["mes"] = df["data"].dt.to_period("M").astype(str)
vendas_mes = df.groupby("mes")["total"].sum().reset_index()

fig2 = px.line(vendas_mes, x="mes", y="total", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Insights automáticos

st.subheader("Insights")

if not df.empty:
    top_produto = vendas_produto.sort_values(by="total", ascending=False).iloc[0]
    st.success(f"Produto mais vendido: {top_produto['produto']}")

# Download

st.subheader("⬇Download")

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Baixar dados filtrados",
    data=csv,
    file_name="dados_filtrados.csv",
    mime="text/csv"
)

# Tabela

st.subheader("Dados")
st.dataframe(df)
