# 🏥 Sistema Inteligente de Predição de Obesidade

## 🎯 Visão Geral do Projeto

Este projeto, desenvolvido para o Tech Challenge de Data Analytics, apresenta uma solução completa para auxiliar equipes médicas na triagem e intervenção precoce da obesidade. A solução é composta por:

1. **Aplicação de Predição (app.py):** Uma interface intuitiva para prever o nível de obesidade de um paciente em tempo real, com foco em usabilidade e feedback imediato.
2. **Painel Analítico (app_dashboard.py):** Um dashboard estratégico com insights baseados em dados para a equipe médica, apoiando a tomada de decisão clínica e a definição de estratégias de saúde.

---

## ✨ 1. Aplicação de Predição (app.py)

A aplicação utiliza um modelo de Machine Learning (Gradient Boosting Classifier) para classificar o paciente em 7 níveis de peso.

### 🎨 Diferenciais de UX/UI

- **Design Profissional e Coeso:** Interface moderna com tema escuro, sidebar informativa e paleta de cores consistente.
- **Organização por Abas:** Inputs organizados em "Dados Pessoais", "Hábitos Alimentares" e "Estilo de Vida" para reduzir a sobrecarga cognitiva.
- **Visualização de Resultados Aprimorada:**
    - **Card de Predição:** Resultado principal destacado com cores contextuais.
    - **Card de Peso Ideal (DIFERENCIAL):** Cálculo e faixa de peso saudável para o paciente, transformando o resultado em uma **meta clara e acionável**.
    - **Gráfico de Probabilidades:** Distribuição da confiança do modelo entre todas as classes.
- **Recomendações Personalizadas:** Orientações específicas baseadas no resultado da predição.

---

## 📊 2. Painel Analítico (app_dashboard.py)

O painel foi desenvolvido para transformar o dataset em inteligência estratégica, suportando a tomada de decisão clínica e a definição de políticas de saúde.

### 🔑 Principais Insights para a Equipe Médica

| Insight | Visualização | Estratégia de Intervenção |
|---|---|---|
| **Risco Genético Elevado** | Gráfico de Pizza (Histórico Familiar) | Reforça a necessidade de **rastreamento precoce** e intervenção preventiva em famílias de risco. |
| **Atividade Física (FAF)** | Gráfico de Barras (Média de FAF) | Demonstra que a FAF é **inversamente proporcional** ao nível de peso, validando o foco na promoção de exercícios. |
| **Distribuição de Risco** | Gráfico de Barras (Níveis de Peso) | Fornece uma visão epidemiológica da base de pacientes. |

---

## 🚀 3. Deploy e Execução

O projeto está configurado para **Deploy Contínuo (CI/CD)** no Streamlit Community Cloud, garantindo acessibilidade 24/7.

### 🛠️ Pré-requisitos

- Python 3.x
- `pip install -r requirements.txt`

### 🖥️ Como Executar Localmente

Para rodar as aplicações localmente, certifique-se de que o `Obesity.csv` esteja no mesmo diretório:

```bash
# Executar a Aplicação de Predição
streamlit run app.py

# Executar o Painel Analítico
streamlit run app_dashboard.py
```

### 🌐 Links do Deploy (Exemplo)

| Aplicação | URL Pública |
|---|---|
| **Predição** | `https://[seu-nome]-predicao.streamlit.app` |
| **Painel Analítico** | `https://[seu-nome]-painel.streamlit.app` |

---

## ⚙️ Estrutura do Repositório

```
/
├── app.py         # Aplicação de Predição (Melhorada)
├── app_dashboard.py            # Painel Analítico (Novo)
├── ml_pipeline_obesity.py   # Script de Treinamento do Modelo
├── Obesity.csv                 # Dataset Original
├── requirements.txt            # Dependências do Projeto
├── .streamlit/                 # Configurações de Tema e Servidor
└── README.md                   # Este arquivo
```


**Tech Challenge - Fase 04 | POSTECH Data Analytics**

