import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Painel Analítico - Obesidade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================
# Reutilizando estilos do app_PT_melhorado.py para manter a consistência
st.markdown("""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Aplicar fonte em toda a aplicação */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header personalizado */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Cards de insights (Métricas) */
    [data-testid="stMetric"] {
        background-color: #1a1a2e;
        padding: 15px 15px 15px 15px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: #ffffff;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #e0e0e0;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1a1a2e;
        color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES DE PRÉ-PROCESSAMENTO E CARREGAMENTO
# ============================================================================

# Função para carregar e pré-processar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('Obesity.csv')
    
    # Renomear colunas para facilitar a manipulação e visualização
    df.columns = ['Gender', 'Age', 'Height', 'Weight', 'Family_History_with_Overweight',
                  'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SNC', 'FAF',
                  'TUE', 'CALC', 'MTRANS', 'NObeyesdad']
    
    # Mapear e traduzir NObeyesdad para português e padronizar
    obesity_map = {
        'Insufficient_Weight': 'Baixo Peso',
        'Normal_Weight': 'Peso Normal',
        'Overweight_Level_I': 'Sobrepeso I',
        'Overweight_Level_II': 'Sobrepeso II',
        'Obesity_Type_I': 'Obesidade I',
        'Obesity_Type_II': 'Obesidade II',
        'Obesity_Type_III': 'Obesidade III'
    }
    df['NObeyesdad_PT'] = df['NObeyesdad'].replace(obesity_map)
    
    # Criar coluna de IMC
    df['IMC'] = df['Weight'] / (df['Height'] ** 2)
    
    # Traduzir outras colunas categóricas
    df['Gender_PT'] = df['Gender'].replace({'Male': 'Masculino', 'Female': 'Feminino'})
    df['Family_History_with_Overweight_PT'] = df['Family_History_with_Overweight'].replace({'yes': 'Sim', 'no': 'Não'})
    df['SMOKE_PT'] = df['SMOKE'].replace({'yes': 'Sim', 'no': 'Não'})
    df['CAEC_PT'] = df['CAEC'].replace({'Sometimes': 'Às vezes', 'Frequently': 'Frequentemente', 'Always': 'Sempre', 'no': 'Não'})
    df['CALC_PT'] = df['CALC'].replace({'Sometimes': 'Às vezes', 'Frequently': 'Frequentemente', 'Always': 'Sempre', 'no': 'Não'})
    
    return df

df = load_data()

# ============================================================================
# FUNÇÃO PARA GERAR O PAINEL
# ============================================================================

def formatar_categoria(categoria):
    """Aplica a formatação correta para os algarismos romanos"""
    return categoria.replace('I', 'I').replace('II', 'II').replace('III', 'III')

def create_dashboard():
    
    # Título Principal
    st.markdown(f"""
    <div class='main-header'>
        <h1>📊 Painel Analítico: Fatores de Obesidade</h1>
        <p>Insights Estratégicos Baseados em Dados para Equipes Médicas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================================
    # SIDEBAR - FILTROS
    # ============================================================================
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; font-size: 5rem;'>🏥</h1>", unsafe_allow_html=True)
        st.title("⚙️ Filtros de Análise")
        
        # Filtro de Gênero
        genero_filtro = st.multiselect(
            "Gênero",
            options=df['Gender_PT'].unique(),
            default=df['Gender_PT'].unique()
        )
        
        # Filtro de Idade
        min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
        idade_range = st.slider(
            "Faixa Etária",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
        )
        
        # Filtro de Histórico Familiar
        hist_familiar_filtro = st.multiselect(
            "Histórico Familiar de Obesidade",
            options=df['Family_History_with_Overweight_PT'].unique(),
            default=df['Family_History_with_Overweight_PT'].unique()
        )
        
        # Aplicar filtros
        df_filtered = df[
            (df['Gender_PT'].isin(genero_filtro)) &
            (df['Age'] >= idade_range[0]) &
            (df['Age'] <= idade_range[1]) &
            (df['Family_History_with_Overweight_PT'].isin(hist_familiar_filtro))
        ]
        
        st.info(f"Dados Filtrados: {len(df_filtered)} registros")

    # Se não houver dados, exibir mensagem
    if df_filtered.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
        return

    # ============================================================================
    # LINHA 1: MÉTRICAS CHAVE (KPIs)
    # ============================================================================
    st.markdown("### 🔑 Métricas Chave")
    
    total_pacientes = len(df_filtered)
    perc_obesidade = df_filtered[df_filtered['NObeyesdad'].str.contains('Obesity')].shape[0] / total_pacientes
    media_imc = df_filtered['IMC'].mean()
    media_idade = df_filtered['Age'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total de Pacientes", value=total_pacientes)
    with col2:
        st.metric(label="Média de Idade", value=f"{media_idade:.1f} anos")
    with col3:
        st.metric(label="Média de IMC", value=f"{media_imc:.2f}")
    with col4:
        st.metric(label="% Obesidade (Tipo I, II, III)", value=f"{perc_obesidade*100:.1f}%", delta=f"{perc_obesidade*100:.1f}%")

    st.markdown("---")

    # ============================================================================
    # LINHA 2: DISTRIBUIÇÃO E FATORES DE RISCO
    # ============================================================================
    col_dist, col_risco = st.columns([1.5, 1])
    
    # Gráfico 1: Distribuição dos Níveis de Obesidade
    with col_dist:
        st.markdown("### 📊 Distribuição dos Níveis de Peso")
        
        df_dist = df_filtered['NObeyesdad_PT'].value_counts().reset_index()
        df_dist.columns = ['Nível de Peso', 'Contagem']
        
        # Definir uma ordem lógica para o eixo Y
        order = ['Baixo Peso', 'Peso Normal', 'Sobrepeso I', 'Sobrepeso II', 'Obesidade I', 'Obesidade II', 'Obesidade III']
        df_dist['Nível de Peso'] = pd.Categorical(df_dist['Nível de Peso'], categories=order, ordered=True)
        df_dist = df_dist.sort_values('Nível de Peso')
        
        fig_dist = px.bar(
            df_dist, 
            y='Nível de Peso', 
            x='Contagem', 
            orientation='h',
            color='Nível de Peso',
            color_discrete_map={
                'Baixo Peso': '#2196f3',
                'Peso Normal': '#4caf50',
                'Sobrepeso I': '#ffc107',
                'Sobrepeso II': '#ff9800',
                'Obesidade I': '#ff5722',
                'Obesidade II': '#f44336',
                'Obesidade III': '#b71c1c'
            },
            template="plotly_dark",
            title="Contagem de Pacientes por Nível de Peso"
        )
        fig_dist.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Número de Pacientes")
        st.plotly_chart(fig_dist, use_container_width=True)

    # Gráfico 2: Fatores de Risco (Histórico Familiar)
    with col_risco:
        st.markdown("### 🧬 Relação: Histórico Familiar")
        
        df_hist = df_filtered.groupby('Family_History_with_Overweight_PT')['NObeyesdad'].value_counts(normalize=True).mul(100).rename('Percentual').reset_index()
        
        # Filtrar apenas Obesidade
        df_hist_obesity = df_hist[df_hist['NObeyesdad'].str.contains('Obesity')]
        
        # Agrupar por Histórico Familiar
        df_hist_sum = df_hist_obesity.groupby('Family_History_with_Overweight_PT')['Percentual'].sum().reset_index()
        
        fig_hist = px.pie(
            df_hist_sum,
            values='Percentual',
            names='Family_History_with_Overweight_PT',
            title='Proporção de Obesidade (I, II, III) por Histórico Familiar',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_hist.update_traces(textinfo='percent+label')
        fig_hist.update_layout(showlegend=False, template="plotly_dark")
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # ============================================================================
    # LINHA 3: HÁBITOS ALIMENTARES E ESTILO DE VIDA
    # ============================================================================
    st.markdown("### 🥗 Hábitos e Estilo de Vida")
    
    col_habito1, col_habito2 = st.columns(2)
    
    # Gráfico 3: Consumo de Água (CH2O) vs Obesidade
    with col_habito1:
        st.markdown("#### Média de Consumo de Água (CH2O)")
        
        df_ch2o = df_filtered.groupby('NObeyesdad_PT')['CH2O'].mean().reset_index()
        df_ch2o.columns = ['Nível de Peso', 'Média de CH2O']
        
        # Definir ordem
        df_ch2o['Nível de Peso'] = pd.Categorical(df_ch2o['Nível de Peso'], categories=order, ordered=True)
        df_ch2o = df_ch2o.sort_values('Nível de Peso')
        
        fig_ch2o = px.bar(
            df_ch2o,
            x='Nível de Peso',
            y='Média de CH2O',
            color='Média de CH2O',
            template="plotly_dark",
            title="Média de Consumo de Água (Escala 1-3) por Nível de Peso"
        )
        fig_ch2o.update_layout(xaxis_title=None, yaxis_title="Média de Consumo", showlegend=False)
        st.plotly_chart(fig_ch2o, use_container_width=True)

    # Gráfico 4: Frequência de Atividade Física (FAF) vs Obesidade
    with col_habito2:
        st.markdown("#### Média de Atividade Física (FAF)")
        
        df_faf = df_filtered.groupby('NObeyesdad_PT')['FAF'].mean().reset_index()
        df_faf.columns = ['Nível de Peso', 'Média de FAF']
        
        # Definir ordem
        df_faf['Nível de Peso'] = pd.Categorical(df_faf['Nível de Peso'], categories=order, ordered=True)
        df_faf = df_faf.sort_values('Nível de Peso')
        
        fig_faf = px.bar(
            df_faf,
            x='Nível de Peso',
            y='Média de FAF',
            color='Média de FAF',
            template="plotly_dark",
            title="Média de Atividade Física (Escala 0-3) por Nível de Peso"
        )
        fig_faf.update_layout(xaxis_title=None, yaxis_title="Média de FAF", showlegend=False)
        st.plotly_chart(fig_faf, use_container_width=True)
        
    st.markdown("---")
    
    # ============================================================================
    # LINHA 4: INFORMAÇÕES ADICIONAIS
    # ============================================================================
    st.markdown("### 💡 Insights para a Equipe Médica")
    
    with st.expander("Análise Detalhada dos Fatores"):
        st.markdown("""
        O painel acima demonstra correlações importantes que podem guiar a intervenção médica:
        
        - **Histórico Familiar (Risco Genético):** O gráfico de pizza mostra que a vasta maioria dos pacientes com Obesidade (I, II, III) possui histórico familiar. Isso reforça a necessidade de **rastreamento precoce** e **intervenção preventiva** em famílias de risco.
        
        - **Consumo de Água (CH2O):** Observa-se que os níveis de Obesidade I e III apresentam a maior média de consumo de água. Isso pode ser um **fator de confusão** ou indicar que o consumo de água, isoladamente, não é suficiente para mitigar os efeitos de outros hábitos.
        
        - **Atividade Física (FAF):** A média de FAF é claramente **inversamente proporcional** ao nível de peso. Pacientes com 'Peso Normal' e 'Baixo Peso' apresentam as maiores médias de FAF, enquanto os níveis de 'Obesidade' têm as menores. **Focar na FAF** é uma estratégia de intervenção primária.
        
        - **Distribuição:** A distribuição é razoavelmente uniforme entre as categorias, indicando que o modelo de Machine Learning tem dados balanceados para todas as classes.
        """)

# Executar o painel
create_dashboard()
