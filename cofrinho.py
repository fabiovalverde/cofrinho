import streamlit as st
import plotly.graph_objects as go
import json
import datetime

st.set_page_config(page_title="Simulador Cofrinho Itaú", layout="centered")
st.title("💰 Simulador Cofrinho Itaú - Aporte Mensal")

st.markdown("""
Simule a evolução do seu investimento como no Cofrinho do Itaú.

- **Rendimento usado**: 100% do CDI (~10,65% a.a.)
- **Rendimento diário aproximado**: 0,028% ao dia
- **Aportes aplicados a cada 30 dias**
""")

# Entrada de dados
valor_inicial = st.number_input("Valor inicial (R$)", min_value=0.0, value=100.0, step=10.0)
aporte_mensal = st.number_input("Aporte mensal (R$)", min_value=0.0, value=200.0, step=10.0)
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

# Gráfico com Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=datas, y=saldos, mode='lines+markers', name='Saldo',
    line=dict(color='green', width=3),
    marker=dict(size=5)
))
fig.update_layout(
    title="📈 Evolução do Saldo",
    xaxis_title="Data",
    yaxis_title="Saldo (R$)",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# Exibir saldo final
st.success(f"Saldo final após {dias} dias: **R$ {saldos[-1]:,.2f}**")

# Exportar dados como JSON
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
