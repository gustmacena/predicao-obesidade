import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# FUNÇÃO AUXILIAR PARA FORMATAÇÃO
# ============================================================================
def formatar_nome_categoria(nome):
    """Formata o nome da categoria mantendo algarismos romanos (I, II, III) em maiúsculas"""
    nome = nome.replace('_', ' ')
    # Substituir padrões específicos mantendo algarismos romanos em maiúsculas
    nome = nome.replace('Baixo peso', 'Baixo Peso')
    nome = nome.replace('Peso normal', 'Peso Normal')
    nome = nome.replace('Sobrepeso i', 'Sobrepeso I')
    nome = nome.replace('Sobrepeso ii', 'Sobrepeso II')
    nome = nome.replace('Obesidade i', 'Obesidade I')
    nome = nome.replace('Obesidade ii', 'Obesidade II')
    nome = nome.replace('Obesidade iii', 'Obesidade III')
    return nome

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Sistema de Predição de Obesidade",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================
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
    
    /* Cards de seção */
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    /* Botão de predição customizado */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Alertas personalizados */
    .custom-alert {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-info {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #1565c0;
    }
    
    .alert-success {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        color: #2e7d32;
    }
    
    .alert-warning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        color: #e65100;
    }
    
    /* Métricas personalizadas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Texto da sidebar */
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    /* Títulos na sidebar */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Links e texto forte na sidebar */
    [data-testid="stSidebar"] strong {
        color: #ffffff !important;
    }
    
    /* Divisores na sidebar */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Tooltips */
    .tooltip-text {
        font-size: 0.85rem;
        color: #6c757d;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER PRINCIPAL
# ============================================================================
st.markdown("""
<div class="main-header">
    <h1>🏥 Sistema Inteligente de Predição de Obesidade</h1>
    <p>Ferramenta de apoio à decisão médica baseada em Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - INFORMAÇÕES E CONTEXTO
# ============================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 5rem;'>🏥</h1>", unsafe_allow_html=True)
    st.title("ℹ️ Sobre o Sistema")
    
    st.markdown("""
    ### O que é este sistema?
    
    Este é um sistema de apoio à decisão médica que utiliza **Machine Learning** 
    para prever o nível de obesidade de um paciente com base em dados demográficos, 
    hábitos alimentares e estilo de vida.
    
    ### Como funciona?
    
    1. **Preencha** os dados do paciente nos campos ao lado
    2. **Clique** no botão "Realizar Predição"
    3. **Analise** os resultados e probabilidades
    4. **Interprete** as recomendações fornecidas
    
    ### Categorias de Obesidade
    
    - 🟢 **Baixo Peso**: IMC < 18.5
    - 🟢 **Peso Normal**: IMC 18.5-24.9
    - 🟡 **Sobrepeso I**: IMC 25-27.4
    - 🟡 **Sobrepeso II**: IMC 27.5-29.9
    - 🟠 **Obesidade I**: IMC 30-34.9
    - 🔴 **Obesidade II**: IMC 35-39.9
    - 🔴 **Obesidade III**: IMC ≥ 40
    
    ### ⚠️ Aviso Importante
    
    Este sistema é uma **ferramenta de apoio** e não substitui 
    a avaliação clínica de um profissional de saúde qualificado.
    """)
    
    st.divider()
    
    st.markdown("""
    <div style='text-align: center; color: #6c757d; font-size: 0.85rem;'>
        <p><strong>Tech Challenge - Fase 04</strong></p>
        <p>POSTECH - Data Analytics</p>
        <p>Modelo: Gradient Boosting Classifier</p>
        <p>Acurácia: 95%</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CARREGAR MODELO
# ============================================================================
@st.cache_resource
def load_model():
    try:
        return joblib.load("obesity_pipeline.pkl")
    except FileNotFoundError:
        st.error("⚠️ Modelo não encontrado! Certifique-se de que o arquivo 'obesity_pipeline.pkl' está no diretório correto.")
        st.stop()

model = load_model()

# ============================================================================
# INTRODUÇÃO E CONTEXTO
# ============================================================================
with st.expander("📋 Entenda a Obesidade e seus Fatores de Risco", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### O que é Obesidade?
        
        A **obesidade** é uma condição médica caracterizada pelo acúmulo excessivo de gordura corporal, 
        a ponto de prejudicar a saúde. É uma doença multifatorial que envolve uma combinação de 
        fatores genéticos, ambientais e comportamentais.
        
        ### Por que é importante?
        
        A obesidade está associada a diversos problemas de saúde graves:
        - Doenças cardiovasculares
        - Diabetes tipo 2
        - Hipertensão arterial
        - Apneia do sono
        - Problemas articulares
        - Alguns tipos de câncer
        """)
    
    with col2:
        st.markdown("""
        ### Fatores que Influenciam
        
        Este sistema analisa diversos fatores para fazer a predição:
        
        **Dados Demográficos:**
        - Idade, gênero, altura e peso
        
        **Hábitos Alimentares:**
        - Consumo de alimentos calóricos
        - Ingestão de vegetais e água
        - Frequência de refeições
        
        **Estilo de Vida:**
        - Atividade física
        - Tempo em dispositivos eletrônicos
        - Consumo de álcool e tabaco
        - Meio de transporte utilizado
        """)

st.divider()

# ============================================================================
# FORMULÁRIO DE ENTRADA DE DADOS
# ============================================================================
st.markdown("## 📝 Dados do Paciente")

# Criar abas para organizar melhor os inputs
tab1, tab2, tab3 = st.tabs(["👤 Dados Pessoais", "🍽️ Hábitos Alimentares", "🏃 Estilo de Vida"])

with tab1:
    st.markdown("### Informações Demográficas")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        genero = st.selectbox(
            "Gênero",
            ["Masculino", "Feminino"],
            help="Selecione o gênero biológico do paciente"
        )
    
    with col2:
        idade = st.number_input(
            "Idade (anos)",
            min_value=0.0,
            max_value=120.0,
            value=23.0,
            step=1.0,
            help="Idade do paciente em anos completos"
        )
    
    with col3:
        altura = st.number_input(
            "Altura (m)",
            min_value=1.0,
            max_value=2.3,
            value=1.70,
            step=0.01,
            format="%.2f",
            help="Altura do paciente em metros"
        )
    
    with col4:
        peso = st.number_input(
            "Peso (kg)",
            min_value=20.0,
            max_value=300.0,
            value=80.0,
            step=0.1,
            help="Peso atual do paciente em quilogramas"
        )
    
    # Calcular e exibir IMC
    if altura > 0:
        imc = peso / (altura ** 2)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="📊 IMC Calculado",
                value=f"{imc:.2f}",
                help="Índice de Massa Corporal = Peso / Altura²"
            )
        
        with col2:
            if imc < 18.5:
                categoria_imc = "Baixo Peso"
                cor_imc = "🟢"
            elif imc < 25:
                categoria_imc = "Peso Normal"
                cor_imc = "🟢"
            elif imc < 30:
                categoria_imc = "Sobrepeso"
                cor_imc = "🟡"
            elif imc < 35:
                categoria_imc = "Obesidade I"
                cor_imc = "🟠"
            elif imc < 40:
                categoria_imc = "Obesidade II"
                cor_imc = "🔴"
            else:
                categoria_imc = "Obesidade III"
                cor_imc = "🔴"
            
            st.metric(
                label="Categoria IMC",
                value=f"{cor_imc} {categoria_imc}"
            )
        
        with col3:
            historico_familiar = st.selectbox(
                "Histórico Familiar de Obesidade?",
                ["Sim", "Não"],
                help="Algum familiar direto possui histórico de obesidade?"
            )

with tab2:
    st.markdown("### Padrões Alimentares")
    
    col1, col2 = st.columns(2)
    
    with col1:
        favc = st.selectbox(
            "🍔 Consome alimentos hipercalóricos com frequência?",
            ["Sim", "Não"],
            help="Alimentos como fast food, doces, frituras, etc."
        )
        
        fcvc = st.slider(
            "🥗 Frequência de consumo de vegetais (0-3)",
            0.0, 3.0, 2.0, 0.5,
            help="0 = Nunca, 1 = Às vezes, 2 = Frequentemente, 3 = Sempre"
        )
        
        ncp = st.slider(
            "🍽️ Número de refeições principais por dia (1-4)",
            1.0, 4.0, 3.0, 1.0,
            help="Quantas refeições principais você faz por dia?"
        )
        
        ch2o = st.slider(
            "💧 Litros de água consumidos por dia (1-3)",
            1.0, 3.0, 2.0, 0.5,
            help="Quantidade diária de água em litros"
        )
    
    with col2:
        caec = st.selectbox(
            "🍿 Consome alimentos entre as refeições?",
            ["Não", "Às vezes", "Frequentemente", "Sempre"],
            help="Com que frequência belisca entre as refeições?"
        )
        
        scc = st.selectbox(
            "📊 Monitora as calorias consumidas?",
            ["Sim", "Não"],
            help="Você conta ou monitora as calorias que consome?"
        )
        
        alcool = st.selectbox(
            "🍷 Frequência de consumo de álcool",
            ["Não", "Às vezes", "Frequentemente", "Sempre"],
            help="Com que frequência consome bebidas alcoólicas?"
        )

with tab3:
    st.markdown("### Atividades e Hábitos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        faf = st.slider(
            "🏃 Frequência de atividade física (0-3)",
            0.0, 3.0, 1.0, 0.5,
            help="0 = Sedentário, 1 = 1-2 dias/semana, 2 = 3-4 dias/semana, 3 = 5+ dias/semana"
        )
        
        tue = st.slider(
            "📱 Tempo diário em dispositivos eletrônicos (0-3)",
            0.0, 3.0, 1.0, 0.5,
            help="Horas por dia em celular, TV, computador, videogame, etc."
        )
    
    with col2:
        fuma = st.selectbox(
            "🚬 É fumante?",
            ["Não", "Sim"],
            help="Fuma cigarros regularmente?"
        )
        
        transp = st.selectbox(
            "🚌 Principal meio de transporte",
            ["Transporte público", "Caminhada", "Automóvel", "Motocicleta", "Bicicleta"],
            help="Qual o meio de transporte mais utilizado no dia a dia?"
        )

st.divider()

# ============================================================================
# BOTÃO DE PREDIÇÃO E RESULTADOS
# ============================================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("🔮 Realizar Predição", use_container_width=True)

if predict_button:
    # Criar dataframe com os dados de entrada
    row = pd.DataFrame([{
        "Gênero": genero,
        "Idade": idade,
        "Altura": altura,
        "Peso": peso,
        "Histórico Familiar": historico_familiar,
        "FAVC": favc,
        "FCVC": fcvc,
        "NCP": ncp,
        "CAEC": caec,
        "Fuma": fuma,
        "Água por dia": ch2o,
        "Conta Calorias": scc,
        "Atividade Física": faf,
        "Tempo em Telas": tue,
        "Álcool": alcool,
        "Transporte": transp
    }])
    
    # Mostrar animação de processamento
    with st.spinner("🔄 Analisando dados e gerando predição..."):
        import time
        time.sleep(1)  # Simular processamento
        
        # Fazer predição
        pred = model.predict(row)[0]
        proba = model.predict_proba(row)[0]
        classes = model.named_steps["clf"].classes_
    
    st.divider()
    
    # ============================================================================
    # EXIBIR RESULTADOS
    # ============================================================================
    st.markdown("## 🎯 Resultados da Predição")
    
    # Resultado principal - 2 cards lado a lado
    col_card1, col_card2 = st.columns(2)
    
    # Card 1: Predição do Modelo
    with col_card1:
        # Determinar cor e emoji baseado na predição
        if "Baixo_peso" in pred or "Peso_normal" in pred:
            cor_resultado = "#4caf50"
            emoji_resultado = "🟢"
        elif "Sobrepeso" in pred:
            cor_resultado = "#ff9800"
            emoji_resultado = "🟡"
        else:
            cor_resultado = "#f44336"
            emoji_resultado = "🔴"
        
        st.markdown(f"""
        <div style='background: {cor_resultado}; padding: 2rem; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 200px; display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0; font-size: 1.3rem;'>Predição do Modelo</h2>
            <h1 style='color: white; margin: 0.5rem 0; font-size: 2rem;'>{emoji_resultado} {formatar_nome_categoria(pred)}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Card 2: Peso Ideal
    with col_card2:
        # Calcular peso ideal baseado em IMC saudável (18.5 - 24.9)
        peso_ideal_min = 18.5 * (altura ** 2)
        peso_ideal_max = 24.9 * (altura ** 2)
        peso_ideal_medio = (peso_ideal_min + peso_ideal_max) / 2
        
        # Determinar cor baseado na diferença do peso atual
        diferenca_peso = peso - peso_ideal_medio
        
        if abs(diferenca_peso) <= 5:
            cor_peso = "#4caf50"  # Verde - próximo do ideal
            emoji_peso = "✅"
            status_peso = "Próximo do Ideal"
        elif diferenca_peso > 5:
            cor_peso = "#ff9800"  # Laranja - acima do ideal
            emoji_peso = "⚠️"
            status_peso = "Acima do Ideal"
        else:
            cor_peso = "#2196f3"  # Azul - abaixo do ideal
            emoji_peso = "📊"
            status_peso = "Abaixo do Ideal"
        
        st.markdown(f"""
        <div style='background: {cor_peso}; padding: 2rem; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 200px; display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0; font-size: 1.3rem;'>Peso Ideal</h2>
            <h1 style='color: white; margin: 0.5rem 0; font-size: 2rem;'>{emoji_peso} {peso_ideal_min:.1f} - {peso_ideal_max:.1f} kg</h1>
            <p style='color: white; margin: 0.5rem 0; font-size: 1rem;'>{status_peso}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de probabilidades
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Distribuição de Probabilidades")
        
        # Criar dataframe para o gráfico
        df_proba = pd.DataFrame({
            "Categoria": [formatar_nome_categoria(c) for c in classes],
            "Probabilidade": proba * 100
        }).sort_values("Probabilidade", ascending=True)
        
        # Gráfico de barras horizontal
        fig = px.bar(
            df_proba,
            x="Probabilidade",
            y="Categoria",
            orientation='h',
            text=df_proba["Probabilidade"].apply(lambda x: f"{x:.1f}%"),
            color="Probabilidade",
            color_continuous_scale="RdYlGn_r",
            labels={"Probabilidade": "Probabilidade (%)"}
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Probabilidade (%)",
            yaxis_title="",
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Confiança da Predição")
        
        # Probabilidade máxima (confiança)
        max_proba = max(proba) * 100
        
        # Gauge chart para confiança
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=max_proba,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Confiança do Modelo", 'font': {'size': 20}},
            number={'suffix': "%", 'font': {'size': 40}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': cor_resultado},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#ffebee'},
                    {'range': [50, 75], 'color': '#fff3e0'},
                    {'range': [75, 100], 'color': '#e8f5e9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Interpretação da confiança
        if max_proba >= 80:
            st.success("✅ **Alta confiança** - O modelo está muito seguro desta predição.")
        elif max_proba >= 60:
            st.warning("⚠️ **Confiança moderada** - Considere avaliação clínica adicional.")
        else:
            st.error("❌ **Baixa confiança** - Recomenda-se avaliação médica detalhada.")
    
    st.divider()
    
    # ============================================================================
    # RECOMENDAÇÕES BASEADAS NO RESULTADO
    # ============================================================================
    st.markdown("## 💡 Recomendações e Orientações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Ações Recomendadas")
        
        if "Baixo_peso" in pred:
            st.markdown("""
            - 🍽️ Consultar nutricionista para plano alimentar adequado
            - 💪 Avaliar necessidade de suplementação nutricional
            - 🏥 Investigar possíveis causas médicas
            - 📊 Monitorar ganho de peso saudável
            """)
        elif "Peso_normal" in pred:
            st.markdown("""
            - ✅ Manter hábitos alimentares saudáveis
            - 🏃 Continuar prática regular de atividade física
            - 💧 Manter hidratação adequada
            - 📊 Realizar check-ups preventivos regulares
            """)
        elif "Sobrepeso" in pred:
            st.markdown("""
            - 🥗 Adotar dieta balanceada com déficit calórico moderado
            - 🏃 Aumentar frequência de atividade física (150min/semana)
            - 💧 Aumentar consumo de água
            - 📊 Monitorar peso e medidas regularmente
            - 👨‍⚕️ Considerar acompanhamento nutricional
            """)
        else:  # Obesidade
            st.markdown("""
            - 🏥 **Consulta médica prioritária** para avaliação completa
            - 👨‍⚕️ Acompanhamento multidisciplinar (médico, nutricionista, educador físico)
            - 🥗 Plano alimentar individualizado e supervisionado
            - 🏃 Programa de exercícios adaptado e progressivo
            - 💊 Avaliar necessidade de tratamento medicamentoso
            - 🧠 Considerar suporte psicológico
            - 📊 Monitoramento frequente de saúde metabólica
            """)
    
    with col2:
        st.markdown("### ⚠️ Fatores de Risco Identificados")
        
        fatores_risco = []
        
        if imc >= 30:
            fatores_risco.append("🔴 IMC elevado (≥30)")
        if historico_familiar == "Sim":
            fatores_risco.append("🟡 Histórico familiar de obesidade")
        if favc == "Sim":
            fatores_risco.append("🟡 Consumo frequente de alimentos hipercalóricos")
        if fcvc < 2:
            fatores_risco.append("🟡 Baixo consumo de vegetais")
        if faf < 1:
            fatores_risco.append("🔴 Sedentarismo (atividade física insuficiente)")
        if ch2o < 2:
            fatores_risco.append("🟡 Hidratação inadequada")
        if tue >= 1.5:
            fatores_risco.append("🟡 Tempo excessivo em telas")
        if fuma == "Sim":
            fatores_risco.append("🔴 Tabagismo")
        if alcool in ["Frequentemente", "Sempre"]:
            fatores_risco.append("🟠 Consumo frequente de álcool")
        if transp == "Automóvel":
            fatores_risco.append("🟡 Baixa atividade física no transporte")
        
        if fatores_risco:
            for fator in fatores_risco:
                st.markdown(f"- {fator}")
        else:
            st.success("✅ Nenhum fator de risco significativo identificado!")
    
    st.divider()
    
    # ============================================================================
    # TABELA DETALHADA DE PROBABILIDADES
    # ============================================================================
    with st.expander("📈 Ver Tabela Detalhada de Probabilidades"):
        df_detailed = pd.DataFrame({
            "Categoria": [formatar_nome_categoria(c) for c in classes],
            "Probabilidade (%)": [f"{p*100:.2f}%" for p in proba],
            "Valor Numérico": proba
        }).sort_values("Valor Numérico", ascending=False).reset_index(drop=True)
        
        df_detailed.index = df_detailed.index + 1
        df_detailed = df_detailed.drop(columns=["Valor Numérico"])
        
        st.dataframe(
            df_detailed,
            use_container_width=True,
            hide_index=False
        )

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 2rem;'>
    <p style='font-size: 0.9rem;'>
        <strong>⚠️ Aviso Legal:</strong> Este sistema é uma ferramenta de apoio à decisão clínica 
        e não substitui a avaliação de um profissional de saúde qualificado. 
        Os resultados devem ser interpretados por um médico no contexto clínico completo do paciente.
    </p>
</div>
""", unsafe_allow_html=True)

