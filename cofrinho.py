import streamlit as st
import plotly.graph_objects as go
import json
import datetime

# Função para formatar valores em reais
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Simulador Cofrinho Itaú", layout="centered")
st.title("💰 Simulador Cofrinho Itaú - Aporte Mensal")

st.markdown("""
Simule a evolução do seu investimento como no Cofrinho do Itaú.

- **Rendimento usado**: 100% do CDI (~10,65% a.a.)
- **Rendimento diário aproximado**: 0,028% ao dia
- **Aportes aplicados a cada 30 dias**
""")

# Entradas
valor_inicial = st.number_input("Valor inicial (R$)", min_value=0.0, value=10000.0, step=100.0, format="%.2f")
aporte_mensal = st.number_input("Aporte mensal (R$)", min_value=0.0, value=0.0, step=50.0, format="%.2f")
dias = st.slider("Número de dias para simulação", min_value=30, max_value=365, value=180)

# Simulação
rendimento_dia = 0.1065 / 365
saldos = []
datas = []
saldo = valor_inicial
data_atual = datetime.date.today()

for dia in range(1, dias + 1):
    saldo += saldo * rendimento_dia
    if dia % 30 == 0:
        saldo += aporte_mensal
    saldos.append(round(saldo, 2))
    datas.append(data_atual + datetime.timedelta(days=dia))

# Gráfico com tooltip formatado
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=datas,
    y=saldos,
    mode='lines+markers',
    name='Saldo',
    line=dict(color='green', width=3),
    marker=dict(size=5),
    hovertemplate='<b>Data:</b> %{x|%d/%m/%Y}<br><b>Saldo:</b> R$ %{y:,.2f}<extra></extra>',
))
fig.update_layout(
    title="📈 Evolução do Saldo",
    xaxis_title="Data",
    yaxis_title="Saldo (R$)",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# Texto formatado com R$
st.success(f"Saldo final após {dias} dias: **{formatar_brl(saldos[-1])}**")

# Exportar dados
data_export = {
    "valor_inicial": valor_inicial,
    "aporte_mensal": aporte_mensal,
    "dias": dias,
    "resultados": saldos,
    "datas": [str(d) for d in datas]
}
json_str = json.dumps(data_export, indent=2)
st.download_button("📥 Exportar dados", data=json_str, file_name="simulacao_cofrinho.json")

# Importar dados
st.markdown("### 📤 Importar dados salvos")
arquivo_json = st.file_uploader("Escolha o arquivo `.json` exportado anteriormente", type=["json"])
if arquivo_json:
    dados_importados = json.load(arquivo_json)
    st.write("Dados importados com sucesso!")
    st.json(dados_importados)
