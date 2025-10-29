import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title="League of Legends - Análises", layout="wide")
st.title("🎮 League of Legends - Painel Analítico")

# ---------------- CARREGAR DADOS ----------------
csv_path = "League of Legends Ranked Match Data  Season 15 (EUN).csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

try:
    df = load_data(csv_path)
    st.success("✅ Base de dados carregada com sucesso!")
except FileNotFoundError:
    st.error(f"❌ Arquivo '{csv_path}' não encontrado. Coloque-o na mesma pasta do app.py.")
    st.stop()

# ---------------- MENU LATERAL ----------------
st.sidebar.header("📊 Escolha a análise")
opcao = st.sidebar.radio(
    "Selecione uma das opções abaixo:",
    (
        "1️⃣ Taxa de Vitória vs Nível de Maestria",
        "2️⃣ Elo vs Duração da Partida"
    )
)

# 1️⃣ TAXA DE VITÓRIA VS MAESTRIA (DINÂMI
if opcao == "1️⃣ Taxa de Vitória vs Nível de Maestria":
    st.header("1️⃣ Taxa de Vitória por Faixa de Nível de Maestria")

    # Conversão da coluna win (True/False → 1/0)
    df['win_numeric'] = df['win'].astype(int)

    # Cria faixas de maestria
    bins_mastery = [0, 11, 21, 31, 41, 51, df['mastery_level'].max() + 1]
    labels_mastery = ['0-10', '11-20', '21-30', '31-40', '41-50', '51+']
    df['mastery_bin'] = pd.cut(df['mastery_level'], bins=bins_mastery, labels=labels_mastery, right=False)

    win_rate_by_mastery = df.groupby('mastery_bin')['win_numeric'].mean().reset_index()
    win_rate_by_mastery['Taxa de Vitória (%)'] = win_rate_by_mastery['win_numeric'] * 100


    selected_bin = st.sidebar.selectbox("🎯 Selecione a faixa de maestria:", labels_mastery)
    filtered_data = df[df['mastery_bin'] == selected_bin]
    win_rate = filtered_data['win_numeric'].mean() * 100 if not filtered_data.empty else 0

    st.metric(label=f"Taxa de Vitória ({selected_bin})", value=f"{win_rate:.2f}%")

    # Gráfico geral
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='mastery_bin', y='Taxa de Vitória (%)', data=win_rate_by_mastery, palette='mako', ax=ax)
    plt.title('Taxa de Vitória por Faixa de Nível de Maestria', fontsize=16)
    plt.xlabel('Faixa de Nível de Maestria')
    plt.ylabel('Taxa de Vitória (%)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# 2️⃣ ELO VS DURAÇÃO DA PARTIDA (DINÂMICO)
elif opcao == "2️⃣ Elo vs Duração da Partida":
    st.header("2️⃣ Duração Média das Partidas por Tier")

    df["duration_minutes"] = df["duration"] / 60

    # Define ordem dos tiers
    tier_order = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD',
                  'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    df['solo_tier'] = pd.Categorical(df['solo_tier'], categories=tier_order, ordered=True)

    tier_avg = df.groupby("solo_tier")["duration_minutes"].mean().reset_index()

    selected_tier = st.sidebar.selectbox("🏅 Selecione o Tier:", tier_order)
    tier_filtered = df[df["solo_tier"] == selected_tier]
    avg_duration = tier_filtered["duration_minutes"].mean() if not tier_filtered.empty else 0

    st.metric(label=f"Duração Média ({selected_tier})", value=f"{avg_duration:.2f} min")

    # Gráfico geral
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="solo_tier", y="duration_minutes", data=tier_avg, palette="crest", ax=ax)
    plt.title("Duração Média das Partidas por Tier", fontsize=16)
    plt.ylabel("Duração Média (minutos)")
    plt.xlabel("Tier Ranqueado")
    plt.xticks(rotation=45)
    plt.ylim(20, tier_avg["duration_minutes"].max() + 2)
    for i, value in enumerate(tier_avg["duration_minutes"].values):
        ax.text(i, value + 0.3, f"{value:.1f}", ha='center', va='bottom', fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)
