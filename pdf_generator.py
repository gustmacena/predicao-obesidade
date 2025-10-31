"""
Módulo para geração de relatórios PDF de predição de obesidade
"""

from fpdf import FPDF
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os

class ObesityReportPDF(FPDF):
    """Classe personalizada para geração de relatórios de obesidade"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Cabeçalho do PDF"""
        # Logo/Título
        self.set_font('Arial', 'B', 16)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, 'Sistema de Predição de Obesidade', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Relatório Individual de Avaliação', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        """Rodapé do PDF"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
    def add_section_title(self, title, icon=''):
        """Adiciona título de seção"""
        self.set_font('Arial', 'B', 14)
        self.set_text_color(102, 126, 234)
        self.ln(5)
        # Remover emojis para compatibilidade com latin-1
        title_clean = title
        self.cell(0, 8, f'{title_clean}', 0, 1, 'L')
        self.set_draw_color(102, 126, 234)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        
    def add_field(self, label, value):
        """Adiciona campo com label e valor"""
        self.set_font('Arial', 'B', 10)
        self.set_text_color(50, 50, 50)
        self.cell(60, 6, f'{label}:', 0, 0, 'L')
        self.set_font('Arial', '', 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 6, str(value), 0, 1, 'L')
        
    def add_result_box(self, prediction, confidence, color_rgb):
        """Adiciona caixa de resultado destacada"""
        self.ln(5)
        self.set_fill_color(*color_rgb)
        self.set_draw_color(*color_rgb)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 12)
        
        # Caixa colorida
        self.rect(10, self.get_y(), 190, 25, 'F')
        
        # Texto dentro da caixa
        y_pos = self.get_y()
        self.set_xy(10, y_pos + 5)
        self.cell(190, 7, 'RESULTADO DA PREDIÇÃO', 0, 1, 'C')
        self.set_font('Arial', 'B', 14)
        self.set_xy(10, y_pos + 12)
        self.cell(190, 8, f'{prediction}', 0, 1, 'C')
        
        self.ln(5)
        
    def add_bullet_list(self, items):
        """Adiciona lista com bullets"""
        self.set_font('Arial', '', 10)
        self.set_text_color(60, 60, 60)
        for item in items:
            self.cell(5, 6, '', 0, 0)
            self.multi_cell(0, 6, f'- {item}')
            
    def add_warning_box(self, text):
        """Adiciona caixa de aviso"""
        self.ln(5)
        self.set_fill_color(255, 243, 224)
        self.set_draw_color(255, 152, 0)
        self.set_line_width(0.5)
        
        # Calcular altura necessária
        self.set_font('Arial', 'I', 9)
        self.set_text_color(230, 81, 0)
        
        # Desenhar caixa
        y_start = self.get_y()
        self.rect(10, y_start, 190, 20, 'FD')
        
        # Adicionar texto
        self.set_xy(15, y_start + 5)
        self.multi_cell(180, 5, text)
        self.ln(5)


def generate_obesity_report(patient_data, prediction_result, output_path='relatorio_obesidade.pdf'):
    """
    Gera relatório PDF completo de predição de obesidade
    
    Args:
        patient_data: Dicionário com dados do paciente
        prediction_result: Dicionário com resultados da predição
        output_path: Caminho para salvar o PDF
        
    Returns:
        Caminho do arquivo PDF gerado
    """
    
    pdf = ObesityReportPDF()
    pdf.add_page()
    
    # ========================================================================
    # INFORMAÇÕES DO RELATÓRIO
    # ========================================================================
    pdf.add_section_title('Informacoes do Relatorio', '')
    pdf.add_field('Data de Geracao', datetime.now().strftime('%d/%m/%Y %H:%M'))
    pdf.add_field('Modelo Utilizado', 'Gradient Boosting Classifier')
    pdf.ln(3)
    
    # ========================================================================
    # DADOS DO PACIENTE
    # ========================================================================
    pdf.add_section_title('Dados do Paciente', '')
    
    # Dados demográficos
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 7, 'Dados Demograficos', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    pdf.add_field('Genero', patient_data.get('Gênero', 'N/A'))
    pdf.add_field('Idade', f"{patient_data.get('Idade', 'N/A')} anos")
    pdf.add_field('Altura', f"{patient_data.get('Altura', 'N/A')} m")
    pdf.add_field('Peso', f"{patient_data.get('Peso', 'N/A')} kg")
    pdf.add_field('IMC Calculado', f"{patient_data.get('IMC', 'N/A'):.2f}")
    pdf.add_field('Historico Familiar de Obesidade', patient_data.get('Histórico Familiar', 'N/A'))
    pdf.ln(3)
    
    # Hábitos alimentares
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 7, 'Hábitos Alimentares', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    pdf.add_field('Consumo de Alimentos Calóricos', patient_data.get('FAVC', 'N/A'))
    pdf.add_field('Consumo de Vegetais (escala 1-3)', patient_data.get('FCVC', 'N/A'))
    pdf.add_field('Numero de Refeicoes por Dia', patient_data.get('NCP', 'N/A'))
    pdf.add_field('Consumo de Agua (litros/dia)', patient_data.get('Água por dia', 'N/A'))
    pdf.add_field('Alimentos entre Refeicoes', patient_data.get('CAEC', 'N/A'))
    pdf.add_field('Monitora Calorias', patient_data.get('Conta Calorias', 'N/A'))
    pdf.add_field('Consumo de Alcool', patient_data.get('Álcool', 'N/A'))
    pdf.ln(3)
    
    # Estilo de vida
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 7, 'Estilo de Vida', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    pdf.add_field('Atividade Fisica (escala 0-3)', patient_data.get('Atividade Física', 'N/A'))
    pdf.add_field('Tempo em Telas (horas/dia)', patient_data.get('Tempo em Telas', 'N/A'))
    pdf.add_field('Fumante', patient_data.get('Fuma', 'N/A'))
    pdf.add_field('Principal Meio de Transporte', patient_data.get('Transporte', 'N/A'))
    
    # ========================================================================
    # RESULTADO DA PREDIÇÃO
    # ========================================================================
    pdf.add_page()
    pdf.add_section_title('Resultado da Predicao', '')
    
    # Determinar cor baseada na predição
    pred = prediction_result['prediction']
    if 'Baixo' in pred or 'Normal' in pred:
        color = (76, 175, 80)  # Verde
    elif 'Sobrepeso' in pred:
        color = (255, 152, 0)  # Laranja
    else:
        color = (244, 67, 54)  # Vermelho
    
    pdf.add_result_box(pred, prediction_result['confidence'], color)
    
    # Confiança
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 7, 'Confianca do Modelo', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(80, 80, 80)
    
    confidence = prediction_result['confidence']
    pdf.cell(0, 6, f'Nivel de confianca: {confidence:.1f}%', 0, 1, 'L')
    
    if confidence >= 80:
        pdf.cell(0, 6, 'Interpretacao: Alta confianca - O modelo esta muito seguro desta predicao.', 0, 1, 'L')
    elif confidence >= 60:
        pdf.cell(0, 6, 'Interpretacao: Confianca moderada - Considere avaliacao clinica adicional.', 0, 1, 'L')
    else:
        pdf.cell(0, 6, 'Interpretacao: Baixa confianca - Recomenda-se avaliacao medica detalhada.', 0, 1, 'L')
    
    pdf.ln(5)
    
    # Probabilidades
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 7, 'Distribuicao de Probabilidades', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(80, 80, 80)
    
    # Tabela de probabilidades
    probabilities = prediction_result.get('probabilities', {})
    for category, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
        pdf.cell(100, 5, f'{category}', 0, 0, 'L')
        pdf.cell(0, 5, f'{prob:.2f}%', 0, 1, 'R')
    
    # ========================================================================
    # RECOMENDAÇÕES
    # ========================================================================
    pdf.add_page()
    pdf.add_section_title('Recomendacoes e Orientacoes', '')
    
    # Ações recomendadas baseadas na predição
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 7, 'Acoes Recomendadas', 0, 1, 'L')
    
    recommendations = get_recommendations(pred)
    pdf.add_bullet_list(recommendations)
    
    pdf.ln(5)
    
    # Fatores de risco
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 7, 'Fatores de Risco Identificados', 0, 1, 'L')
    
    risk_factors = identify_risk_factors(patient_data)
    if risk_factors:
        pdf.add_bullet_list(risk_factors)
    else:
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(76, 175, 80)
        pdf.cell(0, 6, 'Nenhum fator de risco significativo identificado!', 0, 1, 'L')
    
    # ========================================================================
    # AVISO LEGAL
    # ========================================================================
    pdf.ln(10)
    pdf.add_warning_box(
        'AVISO LEGAL: Este relatório é gerado por um sistema de apoio à decisão clínica '
        'e não substitui a avaliação de um profissional de saúde qualificado. '
        'Os resultados devem ser interpretados por um médico no contexto clínico completo do paciente.'
    )
    
    # ========================================================================
    # FOOTER FINAL
    # ========================================================================
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, 'POSTECH - Data Analytics | Tech Challenge - Fase 04', 0, 1, 'C')
    pdf.cell(0, 5, 'Sistema Inteligente de Predição de Obesidade', 0, 1, 'C')
    
    # Salvar PDF
    pdf.output(output_path)
    
    return output_path


def get_recommendations(prediction):
    """Retorna recomendações baseadas na predição"""
    
    if "Baixo" in prediction:
        return [
            "Consultar nutricionista para plano alimentar adequado",
            "Avaliar necessidade de suplementação nutricional",
            "Investigar possíveis causas médicas",
            "Monitorar ganho de peso saudável"
        ]
    elif "Normal" in prediction:
        return [
            "Manter hábitos alimentares saudáveis",
            "Continuar prática regular de atividade física",
            "Manter hidratação adequada",
            "Realizar check-ups preventivos regulares"
        ]
    elif "Sobrepeso" in prediction:
        return [
            "Adotar dieta balanceada com déficit calórico moderado",
            "Aumentar frequência de atividade física (150min/semana)",
            "Aumentar consumo de água",
            "Monitorar peso e medidas regularmente",
            "Considerar acompanhamento nutricional"
        ]
    else:  # Obesidade
        return [
            "CONSULTA MÉDICA PRIORITÁRIA para avaliação completa",
            "Acompanhamento multidisciplinar (médico, nutricionista, educador físico)",
            "Plano alimentar individualizado e supervisionado",
            "Programa de exercícios adaptado e progressivo",
            "Avaliar necessidade de tratamento medicamentoso",
            "Considerar suporte psicológico",
            "Monitoramento frequente de saúde metabólica"
        ]


def identify_risk_factors(patient_data):
    """Identifica fatores de risco baseado nos dados do paciente"""
    
    risk_factors = []
    
    # IMC
    imc = patient_data.get('IMC', 0)
    if imc >= 30:
        risk_factors.append("IMC elevado (≥30)")
    
    # Histórico familiar
    if patient_data.get('Histórico Familiar') == 'Sim':
        risk_factors.append("Histórico familiar de obesidade")
    
    # Alimentos calóricos
    if patient_data.get('FAVC') == 'Sim':
        risk_factors.append("Consumo frequente de alimentos hipercalóricos")
    
    # Vegetais
    fcvc = float(patient_data.get('FCVC', 3))
    if fcvc < 2:
        risk_factors.append("Baixo consumo de vegetais")
    
    # Atividade física
    faf = float(patient_data.get('Atividade Física', 3))
    if faf < 1:
        risk_factors.append("Sedentarismo (atividade física insuficiente)")
    
    # Água
    ch2o = float(patient_data.get('Água por dia', 3))
    if ch2o < 2:
        risk_factors.append("Hidratação inadequada")
    
    # Tempo em telas
    tue = float(patient_data.get('Tempo em Telas', 0))
    if tue >= 1.5:
        risk_factors.append("Tempo excessivo em telas")
    
    # Tabagismo
    if patient_data.get('Fuma') == 'Sim':
        risk_factors.append("Tabagismo")
    
    # Álcool
    if patient_data.get('Álcool') in ['Frequentemente', 'Sempre']:
        risk_factors.append("Consumo frequente de álcool")
    
    # Transporte
    if patient_data.get('Transporte') == 'Automóvel':
        risk_factors.append("Baixa atividade física no transporte")
    
    return risk_factors
