import streamlit as st
import plotly.graph_objects as go
import json
import datetime
import locale

# Define o locale com base no sistema operacional
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Linux/mac
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')  # Windows

st.set_page_config(page_title="Simulador Cofrinho Itaú", layout="centered")
st.title("💰 Simulador Cofrinho Itaú - Aporte Mensal")

st.markdown("""
Simule a evolução do seu investimento como no Cofrinho do Itaú.

- **Rendimento usado**: 100% do CDI (~10,65% a.a.)
- **Rendimento diário aproximado**: 0,028% ao dia
- **Aportes aplicados a cada 30 dias**
""")

# Entradas com valores padrão ajustados
valor_inicial = st.number_input("Valor inicial (R$)", min_value=0.0, value=10000.0, step=100.0, format="%.2f")
aporte_mensal = st.number_input("Aporte mensal (R$)", min_value=0.0, value=0.0, step=50.0, format="%.2f")
dias = st.slider("Número de dias para simulação", min_value=30, max_value=365, value=180)

# Rendimento diário baseado em 100% do CDI (10,65% a.a.)
rendimento_dia = 0.1065 / 365

# Simulação
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
    template="plotly_white",
    yaxis_tickformat=".2f"
)
st.plotly_chart(fig, use_container_width=True)

# Exibir saldo final formatado
st.success(f"Saldo final após {dias} dias: **{locale.currency(saldos[-1], grouping=True)}**")

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
