"""
🤖 Página de Previsões com Machine Learning
"""

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Previsões ML", page_icon="🤖", layout="wide")

st.title("🤖 Previsões com Machine Learning")
st.markdown("### Simulador de Previsões de Vendas")

st.markdown("---")

# Tentar carregar modelos
try:
    modelo_reg = joblib.load('./Modelos/modelo_regressao.pkl')
    scaler_reg = joblib.load('./Modelos/scaler_regressao.pkl')
    modelo_clf = joblib.load('./Modelos/modelo_classificacao.pkl')
    scaler_clf = joblib.load('./Modelos/scaler_classificacao.pkl')
    
    modelos_carregados = True
    st.success("✅ Modelos de ML carregados com sucesso!")
    
except Exception as e:
    modelos_carregados = False
    st.warning("⚠️ Modelos de ML não encontrados. Execute os notebooks de ML primeiro.")
    st.info("📝 Execute: notebooks/ml_clustering.ipynb e ml_supervisionado.ipynb")

st.markdown("---")

# Formulário de entrada
st.header("📝 Dados do Cliente e Veículo")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Informações do Cliente")
    
    idade = st.slider("Idade", 18, 80, 45)
    genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
    renda_anual = st.number_input(
        "Renda Anual (R$)",
        min_value=100000,
        max_value=5000000,
        value=800000,
        step=50000,
        format="%d"
    )

with col2:
    st.subheader("🚗 Informações do Veículo")
    
    marca = st.selectbox("Marca", [
        "Porsche", "Ferrari", "Lamborghini", "McLaren", 
        "Mercedes-AMG", "BMW M", "Audi Sport", "Aston Martin"
    ])
    
    potencia = st.slider("Potência (CV)", 300, 1000, 600)
    cilindradas = st.slider("Cilindradas (L)", 2.0, 8.0, 4.0, 0.5)
    
    categoria = st.selectbox("Categoria", [
        "Superesportivo", "Esportivo", "Gran Turismo", "Roadster"
    ])
    
    preco_base = st.number_input(
        "Preço Base (R$)",
        min_value=200000,
        max_value=5000000,
        value=1200000,
        step=100000,
        format="%d"
    )

st.markdown("---")

# Informações de Test Drive (para classificação)
st.header("🏎️ Informações do Test Drive")

col1, col2, col3 = st.columns(3)

with col1:
    avaliacao = st.slider("Avaliação do Test Drive (1-5)", 1, 5, 5)

with col2:
    dia_semana = st.selectbox("Dia da Semana", [
        "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"
    ])
    dia_semana_num = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"].index(dia_semana)

with col3:
    hora = st.slider("Hora do Test Drive", 8, 20, 14)

st.markdown("---")

# Botão de previsão
if st.button("🔮 Fazer Previsão", type="primary", use_container_width=True):
    
    if not modelos_carregados:
        st.error("❌ Modelos não carregados. Execute os notebooks de ML primeiro.")
    else:
        # Preparar dados
        genero_encoded = 0 if genero == "Masculino" else 1
        categoria_encoded = ["Superesportivo", "Esportivo", "Gran Turismo", "Roadster"].index(categoria)
        marca_encoded = ["Porsche", "Ferrari", "Lamborghini", "McLaren", 
                        "Mercedes-AMG", "BMW M", "Audi Sport", "Aston Martin"].index(marca)
        
        idade_veiculo = 2024 - 2023  # Assumir carro novo
        poder_compra = renda_anual / 1_000_000
        ratio_preco_renda = preco_base / renda_anual
        
        # Features para regressão
        X_reg = pd.DataFrame({
            'idade_cliente': [idade],
            'genero_encoded': [genero_encoded],
            'renda_anual': [renda_anual],
            'potencia_cv': [potencia],
            'cilindradas': [cilindradas],
            'idade_veiculo': [idade_veiculo],
            'categoria_encoded': [categoria_encoded],
            'marca_encoded': [marca_encoded],
            'preco_base': [preco_base],
            'pagamento_encoded': [0],  # Financiamento
            'numero_parcelas': [60],
            'desconto_percentual': [5],
            'poder_compra': [poder_compra],
            'ratio_preco_renda': [ratio_preco_renda]
        })
        
        # Features para classificação
        final_semana = 1 if dia_semana_num >= 5 else 0
        horario_comercial = 1 if 9 <= hora <= 18 else 0
        
        X_clf = pd.DataFrame({
            'idade_cliente': [idade],
            'genero_encoded': [genero_encoded],
            'renda_anual': [renda_anual],
            'potencia_cv': [potencia],
            'cilindradas': [cilindradas],
            'idade_veiculo': [idade_veiculo],
            'categoria_encoded': [categoria_encoded],
            'marca_encoded': [marca_encoded],
            'preco_base': [preco_base],
            'avaliacao': [avaliacao],
            'dia_semana': [dia_semana_num],
            'hora': [hora],
            'poder_compra': [poder_compra],
            'ratio_preco_renda': [ratio_preco_renda],
            'final_semana': [final_semana],
            'horario_comercial': [horario_comercial]
        })
        
        try:
            # Fazer previsões
            X_reg_scaled = scaler_reg.transform(X_reg)
            valor_previsto = modelo_reg.predict(X_reg_scaled)[0]
            
            X_clf_scaled = scaler_clf.transform(X_clf)
            prob_conversao = modelo_clf.predict_proba(X_clf_scaled)[0][1]
            
            st.markdown("---")
            st.header("🎯 Resultados da Previsão")
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="💰 Valor Previsto de Venda",
                    value=f"R$ {valor_previsto:,.2f}",
                    delta=f"{((valor_previsto/preco_base-1)*100):+.1f}% vs preço base"
                )
            
            with col2:
                st.metric(
                    label="📊 Probabilidade de Conversão",
                    value=f"{prob_conversao*100:.1f}%",
                    delta="Alta" if prob_conversao > 0.6 else "Média" if prob_conversao > 0.3 else "Baixa"
                )
            
            with col3:
                ticket_medio = 876000  # Valor médio do dataset
                st.metric(
                    label="🎯 Comparação com Ticket Médio",
                    value=f"{(valor_previsto/ticket_medio):.2f}x",
                    delta=f"{((valor_previsto/ticket_medio-1)*100):+.1f}%"
                )
            
            # Gauge de probabilidade
            st.subheader("📈 Probabilidade de Conversão")
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prob_conversao * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Chance de Venda (%)"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 60], 'color': "gray"},
                        {'range': [60, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Recomendações
            st.markdown("---")
            st.subheader("💡 Recomendações")
            
            if prob_conversao > 0.6:
                st.success("""
                ✅ **Alta Probabilidade de Conversão!**
                - Cliente tem perfil ideal para este veículo
                - Priorize o atendimento
                - Ofereça test drive premium
                - Prepare proposta comercial
                """)
            elif prob_conversao > 0.3:
                st.warning("""
                ⚠️ **Probabilidade Média de Conversão**
                - Cliente demonstra interesse
                - Destaque diferenciais do veículo
                - Ofereça condições especiais de financiamento
                - Agende follow-up próximo
                """)
            else:
                st.info("""
                ℹ️ **Baixa Probabilidade de Conversão**
                - Cliente pode não estar no perfil ideal
                - Avalie veículos alternativos
                - Foque em construir relacionamento
                - Considere remarketing futuro
                """)
            
            # Fatores de influência
            st.markdown("---")
            st.subheader("🔍 Análise dos Fatores")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💰 Fatores Financeiros:**")
                if ratio_preco_renda < 1.5:
                    st.success("✅ Preço compatível com renda")
                elif ratio_preco_renda < 3:
                    st.warning("⚠️ Preço no limite da capacidade")
                else:
                    st.error("❌ Preço acima da capacidade recomendada")
                
                st.markdown(f"- Renda Anual: R$ {renda_anual:,.2f}")
                st.markdown(f"- Preço/Renda: {ratio_preco_renda:.2f}x")
                st.markdown(f"- Poder de Compra: R$ {poder_compra:.2f}M")
            
            with col2:
                st.markdown("**🏎️ Fatores do Veículo:**")
                if avaliacao >= 4:
                    st.success("✅ Alta satisfação no test drive")
                elif avaliacao >= 3:
                    st.warning("⚠️ Satisfação média")
                else:
                    st.error("❌ Baixa satisfação no test drive")
                
                st.markdown(f"- Avaliação: {avaliacao}/5 ⭐")
                st.markdown(f"- Potência: {potencia} CV")
                st.markdown(f"- Categoria: {categoria}")
        
        except Exception as e:
            st.error(f"❌ Erro ao fazer previsão: {e}")
            st.info("💡 Verifique se os modelos foram treinados corretamente")

else:
    st.info("👆 Preencha os dados acima e clique em 'Fazer Previsão'")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🤖 Previsões baseadas em modelos de Machine Learning treinados com dados históricos</p>
</div>
""", unsafe_allow_html=True)
