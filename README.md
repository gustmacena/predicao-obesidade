# 🏥 Sistema Inteligente de Predição de Obesidade - Versão Melhorada

## Visão Geral

Este projeto apresenta uma aplicação web interativa desenvolvida em **Streamlit** para predição de níveis de obesidade utilizando técnicas de **Machine Learning**. A ferramenta foi projetada como um sistema de apoio à decisão médica, auxiliando profissionais de saúde na avaliação de risco de obesidade em pacientes.

A versão melhorada oferece uma experiência visual profissional, educacional e envolvente, com interface moderna, visualizações interativas e sistema completo de recomendações personalizadas.

---

## 🎯 Objetivos do Projeto

Este projeto foi desenvolvido como parte do **Tech Challenge - Fase 04** do curso de **Data Analytics da POSTECH**, com os seguintes objetivos:

- Desenvolver um modelo de Machine Learning para predição de obesidade com acurácia superior a 75%
- Implementar pipeline completo de feature engineering e treinamento
- Realizar deploy do modelo em aplicação preditiva utilizando Streamlit
- Construir visão analítica com principais insights sobre obesidade
- Criar interface profissional e envolvente para usuários finais

---

## 📊 Sobre o Dataset

O projeto utiliza o dataset **Obesity Levels** que contém informações sobre:

### Dados Demográficos
- Gênero (masculino/feminino)
- Idade (anos)
- Altura (metros)
- Peso (quilogramas)

### Hábitos Alimentares
- Consumo de alimentos hipercalóricos (FAVC)
- Frequência de consumo de vegetais (FCVC)
- Número de refeições principais por dia (NCP)
- Consumo de alimentos entre refeições (CAEC)
- Consumo diário de água (CH2O)
- Monitoramento de calorias (SCC)

### Estilo de Vida
- Atividade física (FAF)
- Tempo em dispositivos eletrônicos (TUE)
- Consumo de álcool (CALC)
- Tabagismo (SMOKE)
- Meio de transporte (MTRANS)

### Variável Alvo
- **Obesity_level**: Nível de obesidade classificado em 7 categorias
  - Baixo Peso (Insufficient Weight)
  - Peso Normal (Normal Weight)
  - Sobrepeso I (Overweight Level I)
  - Sobrepeso II (Overweight Level II)
  - Obesidade I (Obesity Type I)
  - Obesidade II (Obesity Type II)
  - Obesidade III (Obesity Type III)

---

## 🤖 Modelo de Machine Learning

### Algoritmo
**Gradient Boosting Classifier** - Modelo ensemble baseado em árvores de decisão que constrói sequencialmente múltiplos modelos fracos para criar um modelo forte.

### Pipeline
O modelo utiliza um pipeline completo do scikit-learn que inclui:

1. **Pré-processamento de Dados**
   - StandardScaler para variáveis numéricas
   - OneHotEncoder para variáveis categóricas

2. **Treinamento**
   - Validação cruzada estratificada (5-fold)
   - Split de treino/teste (80/20)
   - Random state fixo para reprodutibilidade

3. **Avaliação**
   - Acurácia superior a 75%
   - Classification report completo
   - Matriz de confusão

### Arquivo do Modelo
`obesity_pipeline_pt.pkl` - Pipeline completo serializado com joblib, incluindo pré-processamento e modelo treinado.

---

## 🎨 Características da Interface Melhorada

### Design Visual Profissional
- **Paleta de cores** baseada em psicologia das cores para aplicações de saúde
- **Gradientes modernos** no header e botões
- **Tipografia Inter** importada do Google Fonts
- **Sombras e profundidade** para hierarquia visual
- **Layout responsivo** que se adapta a diferentes tamanhos de tela

### Organização Intuitiva
- **Abas temáticas** para organizar inputs (Dados Pessoais, Hábitos Alimentares, Estilo de Vida)
- **Sidebar informativa** com contexto completo sobre o sistema
- **Expanders** para conteúdo adicional sem poluir a interface
- **Tooltips explicativos** em todos os campos de entrada

### Visualizações Interativas
- **Cálculo automático de IMC** com exibição da categoria
- **Gráfico de barras** (Plotly) mostrando probabilidades de todas as categorias
- **Gauge chart** semicircular indicando confiança do modelo
- **Card destacado** com resultado principal em cores contextuais
- **Métricas visuais** para informações importantes

### Sistema de Recomendações
- **Ações personalizadas** baseadas na categoria predita
- **Identificação automática** de fatores de risco presentes
- **Orientações específicas** para cada nível de obesidade
- **Disclaimers médicos** claros e visíveis

### Conteúdo Educacional
- **Explicação sobre obesidade** e suas complicações
- **Descrição dos fatores** analisados pelo modelo
- **Referência rápida** das categorias e faixas de IMC
- **Interpretação de resultados** com linguagem acessível

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Verificar Arquivos Necessários

Certifique-se de que os seguintes arquivos estão no diretório:
- `app_PT_melhorado.py` - Aplicação Streamlit melhorada
- `obesity_pipeline_pt.pkl` - Modelo treinado
- `requirements.txt` - Dependências Python

### Passo 3: Executar a Aplicação

```bash
streamlit run app_PT_melhorado.py
```

### Passo 4: Acessar no Navegador

A aplicação abrirá automaticamente em `http://localhost:8501`

Se não abrir automaticamente, acesse manualmente o endereço acima no seu navegador.

---

## 📦 Estrutura de Arquivos

```
projeto-obesidade/
│
├── app_PT.py                          # Versão original da aplicação
├── app_PT_melhorado.py                # Versão melhorada da aplicação ⭐
├── ml_pipeline_obesity_PT.py          # Script de treinamento do modelo
├── obesity_pipeline_pt.pkl            # Modelo treinado serializado
├── Obesity.csv                        # Dataset original
│
├── requirements.txt                   # Dependências Python
├── README.md                          # Este arquivo
├── GUIA_DE_MELHORIAS.md              # Documentação detalhada das melhorias
├── COMPARATIVO_ANTES_DEPOIS.md       # Análise comparativa
│
└── POSTECH-TechChallenge-Fase4-DataAnalytics.pdf  # Especificação do projeto
```

---

## 🛠️ Tecnologias Utilizadas

### Backend e Machine Learning
- **Python 3.11** - Linguagem de programação
- **scikit-learn 1.3+** - Framework de Machine Learning
- **pandas 2.0+** - Manipulação de dados
- **numpy 1.24+** - Computação numérica
- **joblib 1.3+** - Serialização de modelos

### Frontend e Visualização
- **Streamlit 1.28+** - Framework para aplicações web de dados
- **Plotly 5.17+** - Biblioteca de visualização interativa
- **HTML/CSS** - Customização de estilos

---

## 📊 Dependências Detalhadas

```
streamlit>=1.28.0      # Framework web para aplicações de dados
pandas>=2.0.0          # Manipulação e análise de dados
joblib>=1.3.0          # Serialização de modelos
scikit-learn>=1.3.0    # Machine Learning
plotly>=5.17.0         # Visualizações interativas
numpy>=1.24.0          # Computação numérica
```

---

## 💡 Como Usar a Aplicação

### 1. Preencher Dados do Paciente

#### Aba "Dados Pessoais"
- Selecione o gênero
- Informe idade, altura e peso
- O IMC será calculado automaticamente
- Indique se há histórico familiar de obesidade

#### Aba "Hábitos Alimentares"
- Responda sobre consumo de alimentos calóricos
- Indique frequência de consumo de vegetais
- Informe número de refeições por dia
- Responda sobre consumo de água
- Indique hábito de beliscar entre refeições
- Informe se monitora calorias
- Indique frequência de consumo de álcool

#### Aba "Estilo de Vida"
- Informe frequência de atividade física
- Indique tempo diário em dispositivos eletrônicos
- Responda sobre tabagismo
- Selecione principal meio de transporte

### 2. Realizar Predição

Clique no botão **"🔮 Realizar Predição"** centralizado na tela.

### 3. Analisar Resultados

#### Resultado Principal
Card colorido destacado mostrando a categoria predita.

#### Distribuição de Probabilidades
Gráfico de barras interativo mostrando probabilidade de cada categoria.

#### Confiança do Modelo
Gauge semicircular indicando nível de certeza da predição:
- **Verde (75-100%)**: Alta confiança
- **Amarelo (50-75%)**: Confiança moderada
- **Vermelho (0-50%)**: Baixa confiança

#### Recomendações
Ações específicas baseadas na categoria predita.

#### Fatores de Risco
Lista de fatores de risco identificados nos dados fornecidos.

---

## 🎓 Interpretação dos Resultados

### Categorias de Obesidade

#### 🟢 Baixo Peso (IMC < 18.5)
- **Risco**: Desnutrição, deficiências nutricionais
- **Ação**: Consulta nutricional, investigação médica

#### 🟢 Peso Normal (IMC 18.5-24.9)
- **Risco**: Baixo
- **Ação**: Manutenção de hábitos saudáveis

#### 🟡 Sobrepeso I (IMC 25-27.4)
- **Risco**: Moderado
- **Ação**: Ajustes na dieta e aumento de atividade física

#### 🟡 Sobrepeso II (IMC 27.5-29.9)
- **Risco**: Moderado a alto
- **Ação**: Acompanhamento nutricional, programa de exercícios

#### 🟠 Obesidade I (IMC 30-34.9)
- **Risco**: Alto
- **Ação**: Acompanhamento multidisciplinar

#### 🔴 Obesidade II (IMC 35-39.9)
- **Risco**: Muito alto
- **Ação**: Tratamento médico intensivo

#### 🔴 Obesidade III (IMC ≥ 40)
- **Risco**: Extremamente alto
- **Ação**: Intervenção médica urgente, considerar cirurgia bariátrica

---

## ⚠️ Avisos Importantes

### Limitações da Ferramenta

Este sistema é uma **ferramenta de apoio à decisão** e possui as seguintes limitações:

1. **Não substitui avaliação médica**: A predição deve ser interpretada por profissional de saúde qualificado
2. **Baseado em dados limitados**: O modelo considera apenas as variáveis fornecidas
3. **Não considera histórico médico completo**: Condições pré-existentes não são analisadas
4. **Não é diagnóstico definitivo**: Serve como triagem e orientação inicial

### Uso Apropriado

A ferramenta deve ser utilizada:
- ✅ Como apoio à decisão clínica
- ✅ Para triagem inicial de pacientes
- ✅ Para educação sobre fatores de risco
- ✅ Para monitoramento de tendências

A ferramenta NÃO deve ser utilizada:
- ❌ Como único critério diagnóstico
- ❌ Para auto-diagnóstico sem supervisão médica
- ❌ Em substituição a exames clínicos
- ❌ Para decisões de tratamento sem avaliação completa

---

## 🔒 Privacidade e Segurança

### Dados do Paciente
- Nenhum dado é armazenado permanentemente
- Processamento ocorre localmente no navegador
- Não há envio de informações para servidores externos
- Cada sessão é isolada e independente

### Recomendações para Uso em Produção
Se você planeja usar esta aplicação em ambiente de produção:

1. **Implementar autenticação** de usuários
2. **Adicionar logging** de predições (com consentimento)
3. **Criptografar dados sensíveis**
4. **Implementar HTTPS**
5. **Adicionar termos de uso e política de privacidade**
6. **Conformidade com LGPD/GDPR**
7. **Auditorias de segurança regulares**

---

## 📈 Melhorias Futuras

### Funcionalidades Planejadas

#### Curto Prazo
- Exportação de relatórios em PDF
- Histórico de predições por paciente
- Gráficos de evolução temporal
- Modo comparativo entre pacientes

#### Médio Prazo
- Integração com prontuário eletrônico
- API REST para integração com outros sistemas
- Dashboard administrativo com estatísticas
- Suporte a múltiplos idiomas

#### Longo Prazo
- Modelos especializados por faixa etária
- Incorporação de dados genéticos
- Predição de comorbidades associadas
- Sistema de recomendações com IA generativa

---

## 🤝 Contribuições

Este projeto foi desenvolvido como trabalho acadêmico, mas sugestões e melhorias são bem-vindas.

### Como Contribuir
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📚 Documentação Adicional

- **GUIA_DE_MELHORIAS.md**: Documentação detalhada de todas as melhorias implementadas
- **COMPARATIVO_ANTES_DEPOIS.md**: Análise comparativa entre versão original e melhorada
- **ml_pipeline_obesity_PT.py**: Código comentado do pipeline de treinamento

---

## 📞 Suporte e Recursos

### Documentação de Tecnologias
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Comunidades
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Stack Overflow - Streamlit](https://stackoverflow.com/questions/tagged/streamlit)
- [Stack Overflow - Scikit-learn](https://stackoverflow.com/questions/tagged/scikit-learn)

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge - Fase 04 da POSTECH.

---

## 👥 Autores

**Tech Challenge - Fase 04**  
**POSTECH - Data Analytics**  
**Outubro 2025**

---

## 🙏 Agradecimentos

- POSTECH pela proposta desafiadora do Tech Challenge
- Comunidade Streamlit pelos recursos e documentação
- Comunidade científica pelos datasets e pesquisas sobre obesidade
- Profissionais de saúde que inspiraram as funcionalidades educacionais

---

## 📊 Status do Projeto

✅ **Concluído** - Versão 2.0 (Melhorada)

### Checklist de Requisitos do Tech Challenge

- [x] Pipeline de Machine Learning completo
- [x] Modelo com acurácia > 75%
- [x] Deploy em aplicação Streamlit
- [x] Visão analítica com insights
- [x] Interface profissional e envolvente
- [x] Documentação completa
- [x] Código versionado

---

## 🎉 Conclusão

Este projeto demonstra a aplicação prática de técnicas de Machine Learning em um contexto de saúde pública relevante. A transformação da interface de uma versão básica para uma experiência profissional e educacional ilustra a importância do design centrado no usuário em aplicações de dados.

A ferramenta resultante não apenas faz predições precisas, mas também educa usuários sobre obesidade, identifica fatores de risco modificáveis e fornece orientações personalizadas, maximizando seu valor como instrumento de apoio à decisão médica.

---

**Para mais informações, consulte os documentos complementares:**
- 📘 GUIA_DE_MELHORIAS.md
- 📊 COMPARATIVO_ANTES_DEPOIS.md

**Desenvolvido com ❤️ para o Tech Challenge - POSTECH Data Analytics**

