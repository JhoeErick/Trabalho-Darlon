import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="League of Legends - Dashboard Dinâmico", layout="wide")
st.title("🎮 Painel Analítico - League of Legends (Season 15)")


csv_path = "League of Legends Ranked Match Data  Season 15 (EUN).csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(csv_path)
    st.success("✅ Base de dados carregada com sucesso!")
except FileNotFoundError:
    st.error(f"❌ Arquivo '{csv_path}' não encontrado. Coloque-o na mesma pasta do app.py.")
    st.stop()

# Pré-processamento inicial
df['win_numeric'] = df['win'].astype(int)
df["duration_minutes"] = df["duration"] / 60

tier_order = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD',
              'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
df['solo_tier'] = pd.Categorical(df['solo_tier'], categories=tier_order, ordered=True)

--
st.sidebar.header("📊 Escolha a análise")

analise = st.sidebar.selectbox(
    "Selecione uma análise:",
    [
        "Taxa de Vitória vs Nível de Maestria",
        "Elo vs Duração da Partida",
        "Taxa de Vitória por Elo e Maestria"
    ]
)

<<<<<<< HEAD
st.sidebar.markdown("---")
st.sidebar.caption("")
=======
# 1️⃣ TAXA DE VITÓRIA VS MAESTRIA (DINÂMI
if opcao == "1️⃣ Taxa de Vitória vs Nível de Maestria":
    st.header("1️⃣ Taxa de Vitória por Faixa de Nível de Maestria")
>>>>>>> 22bcbddf95420370513a074efacfdcefc6fe3d9a

#  ANÁLISE 1 
if analise == "Taxa de Vitória vs Nível de Maestria":
    st.header("🏆 Taxa de Vitória por Nível de Maestria")

    # Sliders para faixa de maestria
    min_mastery = int(df['mastery_level'].min())
    max_mastery = int(df['mastery_level'].max())

    faixa = st.slider(
        "Selecione o intervalo de maestria:",
        min_value=min_mastery,
        max_value=max_mastery,
        value=(min_mastery, max_mastery)
    )

<<<<<<< HEAD
    filtered = df[(df['mastery_level'] >= faixa[0]) & (df['mastery_level'] <= faixa[1])]
=======

    selected_bin = st.sidebar.selectbox("🎯 Selecione a faixa de maestria:", labels_mastery)
    filtered_data = df[df['mastery_bin'] == selected_bin]
    win_rate = filtered_data['win_numeric'].mean() * 100 if not filtered_data.empty else 0
>>>>>>> 22bcbddf95420370513a074efacfdcefc6fe3d9a

    win_rate = filtered.groupby('mastery_level')['win_numeric'].mean().reset_index()
    win_rate['Taxa de Vitória (%)'] = win_rate['win_numeric'] * 100

    fig = px.line(
        win_rate,
        x='mastery_level',
        y='Taxa de Vitória (%)',
        markers=True,
        title=f"Taxa de Vitória por Nível de Maestria ({faixa[0]}–{faixa[1]})"
    )
    st.plotly_chart(fig, use_container_width=True)

<<<<<<< HEAD
# ANÁLISE 2 
elif analise == "Elo vs Duração da Partida":
    st.header("⏱️ Duração Média das Partidas por Tier")
=======
# 2️⃣ ELO VS DURAÇÃO DA PARTIDA (DINÂMICO)
elif opcao == "2️⃣ Elo vs Duração da Partida":
    st.header("2️⃣ Duração Média das Partidas por Tier")
>>>>>>> 22bcbddf95420370513a074efacfdcefc6fe3d9a

    selected_tiers = st.multiselect("Selecione os Tiers:", tier_order, default=tier_order)
    filtered = df[df['solo_tier'].isin(selected_tiers)]

    tier_avg = filtered.groupby('solo_tier')['duration_minutes'].mean().reset_index()

    fig = px.bar(
        tier_avg,
        x='solo_tier',
        y='duration_minutes',
        color='duration_minutes',
        text='duration_minutes',
        color_continuous_scale='blues',
        title="Duração Média das Partidas por Tier (Dinâmico)"
    )
    fig.update_traces(texttemplate='%{text:.1f} min', textposition='outside')
    fig.update_layout(yaxis_title="Duração Média (min)", xaxis_title="Tier")
    st.plotly_chart(fig, use_container_width=True)

<<<<<<< HEAD
#  ANÁLISE 3 
elif analise == "Taxa de Vitória por Elo e Maestria":
    st.header("⚔️ Taxa de Vitória por Tier e Faixa de Maestria")
=======
    selected_tier = st.sidebar.selectbox("🏅 Selecione o Tier:", tier_order)
    tier_filtered = df[df["solo_tier"] == selected_tier]
    avg_duration = tier_filtered["duration_minutes"].mean() if not tier_filtered.empty else 0
>>>>>>> 22bcbddf95420370513a074efacfdcefc6fe3d9a

    # Sliders dinâmicos para maestria
    min_mastery = int(df['mastery_level'].min())
    max_mastery = int(df['mastery_level'].max())

    faixa_maestria = st.slider(
        "Selecione o intervalo de maestria:",
        min_value=min_mastery,
        max_value=max_mastery,
        value=(min_mastery, max_mastery)
    )

    selected_tiers = st.multiselect("Selecione os Tiers:", tier_order, default=['GOLD', 'PLATINUM', 'DIAMOND'])

    filtered = df[
        (df['solo_tier'].isin(selected_tiers)) &
        (df['mastery_level'] >= faixa_maestria[0]) &
        (df['mastery_level'] <= faixa_maestria[1])
    ]

    result = filtered.groupby('solo_tier')['win_numeric'].mean().reset_index()
    result['Taxa de Vitória (%)'] = result['win_numeric'] * 100

    fig = px.bar(
        result,
        x='solo_tier',
        y='Taxa de Vitória (%)',
        color='solo_tier',
        title=f"Taxa de Vitória por Tier ({faixa_maestria[0]}–{faixa_maestria[1]} de Maestria)"
    )
    fig.update_layout(xaxis_title="Tier", yaxis_title="Taxa de Vitória (%)")
    st.plotly_chart(fig, use_container_width=True)
