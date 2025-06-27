import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import numpy as np
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Ames Housing Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado com tema preto, vermelho e azul
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #000000;
    color: #ffffff;
}

[data-testid="stHeader"] {
    background-color: #000000;
    border-bottom: 1px solid #ff0000;
}

[data-testid="stSidebar"] {
    background-color: #000000;
    color: white;
    border-right: 1px solid #1e3a8a;
}

.custom-container {
    background-color: #0a0a0a;
    border-radius: 8px;
    padding: 25px;
    margin: 10px 0;
    border: 1px solid #1e3a8a;
    box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
}

.info-panel {
    background-color: #0a0a0a;
    border-left: 4px solid #ff0000;
    padding: 15px;
    margin: 15px 0;
    border-radius: 0 8px 8px 0;
}

/* Estilos para métricas */
[data-testid="metric-container"] {
    background-color: #0a0a0a !important;
    border: 1px solid #1e3a8a !important;
    border-radius: 5px !important;
    padding: 10px !important;
    margin: 10px 0 !important;
}

[data-testid="metric-container"] label {
    color: #ffffff !important;
    font-size: 1rem !important;
}

[data-testid="metric-container"] div {
    color: #1e90ff !important;
    font-weight: bold !important;
    font-size: 1.5rem !important;
}

/* Títulos */
h1 {
    color: #ff0000 !important;
    border-bottom: 1px solid #1e3a8a;
    padding-bottom: 10px;
}

h2 {
    color: #1e3a8a !important;
}

h3 {
    color: #ffffff !important;
}

/* Rodapé */
footer {
    color: #ffffff !important;
    background-color: #000000 !important;
    border-top: 1px solid #1e3a8a !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Carregar dados
df = pd.read_csv('AmesHousing.csv')

# Renomear colunas para formato mais legível
df = df.rename(columns={
    'PoolQC': 'Pool QC',
    'GrLivArea': 'Gr Liv Area',
    'TotalBsmtSF': 'Total Bsmt SF',
    'OverallQual': 'Overall Qual',
    'BedroomAbvGr': 'Bedroom Abv Gr',
    'FullBath': 'Full Bath'
})

# Barra lateral com filtros
with st.sidebar:
    st.title("📊 Ames Housing Predictor")
    selected = option_menu(
        menu_title="Menu Principal",
        options=["Visão Geral", "Análise de Dados", "Modelo Preditivo", "Conclusões"],
        icons=["house", "database", "robot", "lightbulb"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#000000", "border": "1px solid #1e3a8a"},
            "icon": {"color": "#ff0000", "font-size": "18px"}, 
            "nav-link": {"color": "#ffffff", "font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#1e3a8a", "color": "#ffffff"},
        }
    )

    st.markdown("---")
    st.markdown("### Filtros de Análise")
    
    # Filtro de preço
    price_min, price_max = int(df['SalePrice'].min()), int(df['SalePrice'].max())
    price_range = st.slider(
        "Faixa de Preço (USD)", 
        min_value=price_min,
        max_value=price_max,
        value=(price_min, price_max)
    )
    
    # Filtro de qualidade
    qual_min, qual_max = int(df['Overall Qual'].min()), int(df['Overall Qual'].max())
    quality_range = st.slider(
        "Qualidade Geral", 
        min_value=qual_min,
        max_value=qual_max,
        value=(qual_min, qual_max))
    
    # Aplicar filtros
    filtered_df = df[
        (df['SalePrice'] >= price_range[0]) & 
        (df['SalePrice'] <= price_range[1]) & 
        (df['Overall Qual'] >= quality_range[0]) & 
        (df['Overall Qual'] <= quality_range[1])
    ]
    
    st.markdown("---")
    st.markdown(f"🔍 Imóveis filtrados: {len(filtered_df):,} de {len(df):,}")

# Página principal
if selected == "Visão Geral":
    st.title("🏠 Modelo Preditivo de Preços de Imóveis - Ames, Iowa")
    
    # Seção "Sobre o Projeto"
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h3 style="color: #ff0000;">Sobre o Projeto</h3>
        <p style="color: #ffffff;">Desenvolvemos um modelo de machine learning para prever preços de imóveis 
        usando o dataset Ames Housing, com 2.930 propriedades e 81 características cada. Nosso objetivo é criar 
        uma alternativa transparente aos algoritmos monopolizados que inflacionam os preços.</p>
        
        <h4 style="color: #ff0000; margin-top: 20px;">Contexto do Mercado</h4>
        <p style="color: #ffffff;">Algoritmos de precificação monopolizados como o YieldStar têm contribuído para:</p>
        <ul style="color: #ffffff;">
            <li>Aumento médio de <b>US$ 181/mês</b> nos aluguéis</li>
            <li><b>US$ 3.8 bilhões</b> em custos adicionais para inquilinos em 2024</li>
        </ul>
        
        <h3 style="color: #ff0000; margin-top: 20px;">Nossa Solução</h3>
        <p style="color: #ffffff;">Desenvolvemos este projeto em <b>1 semana</b> com apenas <b>1 cientista de dados</b>. 
        Com uma equipe ampliada, poderemos:</p>
        <ul style="color: #ffffff;">
            <li>Reduzir o erro médio do nosso modelo atual</li>
            <li>Desenvolver modelos para outras cidades</li>
            <li>Criar um sistema preditivo mais justo e transparente</li>
            <li>Gerar soluções com <b>alto retorno financeiro</b> para a equipe</li>
        </ul>
        
        <h3 style="color: #ff0000; margin-top: 20px;">Explore um pouco nossa feature alvo:</h3>
        """, unsafe_allow_html=True)
    
    # Métricas com dados filtrados
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.subheader("Principais Estatísticas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Preço Médio", f"${filtered_df['SalePrice'].mean():,.0f}")
        with col2:
            st.metric("Área Média", f"{filtered_df['Gr Liv Area'].mean():,.0f} sqft")
        with col3:
            st.metric("Qualidade Média", f"{filtered_df['Overall Qual'].mean():.1f}/10")
    
    # Gráfico de distribuição de preços
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.subheader("Distribuição de Preços (Filtrados)")
        fig = px.histogram(filtered_df, x='SalePrice', nbins=50, 
                          title="Distribuição dos Preços de Venda",
                          color_discrete_sequence=['#ff0000'])
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font': {'color': 'white'},
            'xaxis': {'title': 'Preço de Venda (USD)'},
            'yaxis': {'title': 'Número de Imóveis'}
        })
        st.plotly_chart(fig, use_container_width=True)

elif selected == "Análise de Dados":
    st.title("🔍 Análise do Dataset Ames Housing")
    
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.subheader("Tratamento de Dados")
        st.markdown("""
         <h4 style="color: #ff0000;">Processamento realizado:</h4>
        <ul style="color: #ffffff;">
            <li><b>Valores ausentes:</b> 15 variáveis categóricas utilizavam NA como uma categoria, que foi convertido para 'None'</li>
            <li><b>Inconsistências:</b> Remoção de registros logicamente inconsistentes</li>
            <li><b>Imputação:</b> Mediana para numéricos, moda para categóricos</li>
            <li><b>Seleção:</b> Redução de 81 para 36 variáveis mais relevantes (via feature importance e eliminação de variáveis muito correlacionadas entre si)</li>
        </ul>
        """, unsafe_allow_html=True)
    
    # Seção unificada de visualizações
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.subheader("Relação Entre Variáveis")
        
        # Tabs para as visualizações principais
        tab1, tab2, tab3, tab4 = st.tabs(["Área vs Preço", "Qualidade vs Preço", "Distribuição por Bairros", "Interações Adicionais"])
        
        with tab1:
            fig = px.scatter(filtered_df, x='Gr Liv Area', y='SalePrice', 
                            color='Overall Qual',
                            title="Área Habitável vs Preço de Venda",
                            labels={'Gr Liv Area': 'Área Habitável (sqft)', 
                                   'SalePrice': 'Preço de Venda (USD)'})
            fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {'color': 'white'}
            })
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = px.box(filtered_df, x='Overall Qual', y='SalePrice',
                        title="Preço por Nível de Qualidade",
                        color_discrete_sequence=['#1e3a8a'])
            fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {'color': 'white'},
                'xaxis': {'title': 'Qualidade Geral (1-10)'},
                'yaxis': {'title': 'Preço de Venda (USD)'}
            })
            st.plotly_chart(fig, use_container_width=True)
            
        with tab3:
            fig = px.box(filtered_df, x='Neighborhood', y='SalePrice',
                        title="Distribuição de Preços por Bairro",
                        color_discrete_sequence=['#ff0000'])
            fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {'color': 'white'},
                'xaxis': {'title': 'Bairro'},
                'yaxis': {'title': 'Preço de Venda (USD)'}
            })
            st.plotly_chart(fig, use_container_width=True)
            
        with tab4:
            # Nova aba com visualizações adicionais interativas
            st.subheader("Exploração Interativa das Variáveis-Chave")
            
            # Gráfico de dispersão 3D interativo
            st.markdown("**Visualização 3D Interativa:**")
            x_axis = st.selectbox("Eixo X", options=['Gr Liv Area', 'Total Bsmt SF', 'Year Built'], index=0)
            y_axis = st.selectbox("Eixo Y", options=['Total Bsmt SF', 'Year Built', 'Gr Liv Area'], index=1)
            z_axis = st.selectbox("Eixo Z", options=['SalePrice', 'Overall Qual', 'Full Bath'], index=0)
            color_by = st.selectbox("Colorir por", options=['Overall Qual', 'Full Bath', 'Year Built'], index=0)
                
            fig = px.scatter_3d(filtered_df,
                              x=x_axis,
                              y=y_axis,
                              z=z_axis,
                              color=color_by,
                              title=f"Relação 3D: {x_axis} × {y_axis} × {z_axis}",
                              height=600)
            fig.update_layout({
                'scene': {
                    'xaxis': {'title': x_axis},
                    'yaxis': {'title': y_axis},
                    'zaxis': {'title': z_axis},
                    'bgcolor': 'rgba(0,0,0,0)'
                },
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {'color': 'white'}
            })
            st.plotly_chart(fig, use_container_width=True)
    
    # Seção de correlações
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.subheader("Importância das Variáveis")
        importance_data = pd.DataFrame({
            'Feature': ['Overall Qual', 'Gr Liv Area', 'Total Bsmt SF', 'Year Built', 'Full Bath'],
            'Importance': [0.35, 0.25, 0.15, 0.10, 0.05]
        })
        
        fig = px.bar(importance_data.sort_values('Importance', ascending=True), 
             x='Importance', 
             y='Feature', 
             orientation='h',
             color_discrete_sequence=['#1e3a8a'])

        # Configuração separada do título usando update_layout
        fig.update_layout(
            title={
                'text': "<b>Importância das Variáveis no Modelo</b><br><span style='font-size:12px;color:gray'>Para restringirmos o número de features, aplicamos um modelo prévio que nos fornece as features mais relevantes</span>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        # Mantenha suas outras configurações de layout
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font': {'color': 'white'},
            'xaxis': {'title': 'Importância Relativa'},
            'yaxis': {'title': ''}
        })
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
            ## Principais Variáveis Explicativas
            - **Overall Qual**: Avaliação geral (1-10) de materiais e acabamentos da casa (35% importância)
            - **Gr Liv Area**: Área habitável acima do solo em sqft (25% importância)  
            - **Total Bsmt SF**: Área total do porão, incluindo espaços acabados (15% importância)
            - **Year Built**: Ano original de construção da propriedade (10% importância)
            - **Full Bath**: Número de banheiros completos acima do solo (5% importância)
        """)



        st.subheader("Análise de Correlações")
        
        # Texto explicativo
        st.markdown("""
        <div style="color: #ffffff; margin-bottom: 20px;">
            <h4 style="color: #ff0000;">Métodos de Análise:</h4>
            <ul>
                <li><b>Correlação de Spearman:</b> Para variáveis numéricas (mede relações monotônicas)</li>
                <li><b>V de Cramer:</b> Para variáveis categóricas (mede associação entre categorias)</li>
            </ul>
            <h4 style="color: #ff0000; margin-top: 15px;">Principais Observações:</h4>
            <ul>
                <li>Em ambos os gráficos, a última linha representa nossa variável-alvo (preço de venda)</li>
                <li>Para análise com variáveis categóricas, o preço foi dividido em quartis</li>
                <li>Algumas variáveis mostraram alta correlação entre si, indicando possível redundância</li>
                <li>As correlações mais fortes ajudaram na seleção de features para o modelo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Colunas para as imagens de correlação
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("correlacao_spearman.png", caption="Correlação de Spearman - Variáveis Numéricas", use_container_width=True)
        
        with col2:
            st.image("v_de_cramer.png", caption="V de Cramer - Variáveis Categóricas", use_container_width=True)


elif selected == "Modelo Preditivo":
    st.title("🤖 Nosso Modelo Preditivo")
    
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        
        # Seção de Método Escolhido
        st.markdown("""
        ### ⚙️ Método: XGBoost Regressor
        **Por que esta escolha?**
        - Excelente desempenho com dados estruturados (como tabelas de imóveis)
        - Resistente a overfitting com os parâmetros adequados
        - Capacidade de capturar relações não-lineares entre features
        - Importância automática de variáveis integrada
        
        **Parâmetros utilizados:**
        - Learning Rate: 0.05
        - Profundidade Máxima: 5
        - Número de Estimadores: 1000
        - Subamostragem: 0.8
        """)
        
        # Seção de Performance
        st.markdown("---")
        st.subheader("📈 Performance do Modelo")
        
        # Métricas de Treino
        st.markdown("#### 🔧 Métricas no Conjunto de TREINO (1460 primeiros dados)")
        col_train1, col_train2, col_train3 = st.columns(3)
        with col_train1:
            st.metric("R² Score", "0.9726")
        with col_train2:
            st.metric("Erro Médio Absoluto (MAE)", "$8,341.26")
        with col_train3:
            st.metric("RMSE", "$12,981.83")
        
        # Métricas de Teste
        st.markdown("#### 🧪 Métricas no Conjunto de TESTE")
        col_test1, col_test2, col_test3 = st.columns(3)
        with col_test1:
            st.metric("R² Score", "0.830")
        with col_test2:
            st.metric("Erro Médio Absoluto (MAE)", "$16,972")
        with col_test3:
            st.metric("RMSE", "$33,193")
        
        # Gráfico de distribuição de erros
        st.markdown("---")
        st.subheader("📉 Distribuição dos Erros")
        st.image("distribuicao_erros.png", use_container_width=True,
                caption="Distribuição dos resíduos (erros) nos conjuntos de treino e teste")

        # Nova seção de Análise de Erros (adicionada aqui)
        st.markdown("---")
        st.subheader("🔍 Análise dos Resultados")
        st.markdown("""
        <div style="background-color: #0a0a0a; padding: 15px; border-radius: 8px; border-left: 4px solid #1e3a8a;">
        <h4 style="color: #1e90ff; margin-top: 0;">Principais Observações:</h4>
        <ol style="color: #ffffff;">
            <li><b>Erros centrados em zero</b> - Médias de -$125,56 (treino) e $1,442,91 (teste) indicam baixo viés global</li>
            <li><b>Padrão quase-normal com subestimação</b> - Cauda direita alongada revela dificuldade com imóveis premium</li>
            <li><b>Bom ajuste com overfitting moderado</b> - R² de 0.97 (treino) vs 0.83 (teste)</li>
            <li><b>Sensibilidade a outliers</b> - Disparidade entre MAE ($8k/$17k) e RMSE ($13k/$33k)</li>
            <li><b>Oportunidades de melhoria</b> - Foco em regularização para propriedades de alto valor</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        # Seção de Chamada para Ação
        st.markdown("""
        <div style="background-color: #0a0a0a; padding: 20px; border-radius: 8px; border: 1px solid #ff0000; margin-top: 20px;">
        <h3 style="color: #ff0000; text-align: center;">🚀 <b>Vamos Juntos Melhorar Esses Resultados!</b></h3>
        <p style="color: #ffffff; text-align: center;">
        Com <b>83% de acurácia</b> já comprovada, imagine o que podemos alcançar com seu talento!<br>
        Estamos construindo um modelo <b>mais justo e transparente</b> para o mercado imobiliário.<br>
        <b>Sua expertise</b> pode ser a peça que falta para:
        </p>
        <ul style="color: #ffffff; columns: 2; column-gap: 20px;">
            <li>Reduzir o overfitting</li>
            <li>Otimizar a precificação de imóveis premium</li>
            <li>Melhorar a generalização</li>
            <li>Desenvolver novas features</li>
        </ul>
        <p style="color: #1e90ff; text-align: center; font-weight: bold;">
        ✨ Junte-se ao nosso time e deixe sua marca na próxima geração de modelos preditivos! ✨
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
elif selected == "Conclusões":
    st.title("🚀 Insights Transformadores e Oportunidades")
    
    with st.container():
        st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background-color: #0a0a0a;
                border-radius: 8px;
                padding: 25px;
                margin: 10px 0;
                border: 1px solid #1e3a8a;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border-left: 4px solid #ff0000; padding-left: 15px; margin-bottom: 30px;">
        <h3 style="color: #1e90ff;">O QUE APRENDEMOS: REVELAÇÕES CHAVE</h3>
        <p style="color: #ffffff; font-size: 1.1em;">Nosso mergulho nos dados desvendou padrões cruciais que desafiam intuições convencionais:</p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px;">
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 8px; border-top: 3px solid #1e3a8a;">
                <h4 style="color: #ff0000; margin-top: 0;">📈 Fatores de Impacto</h4>
                <p style="color: #ffffff;">A qualidade geral explica <b>35% da variação</b> nos preços - mais que o dobro da área habitável. Acabamentos premium (Overall Qual) agregam mais valor que metros extras: qualidade construtiva impacta 40% mais no preço que a área habitável.</p>
            </div>
            <div style="background-color: #1e1e1e; padding: 15px; border-radius: 8px; border-top: 3px solid #ff0000;">
                <h4 style="color: #1e90ff; margin-top: 0;">🤖 Performance do Modelo</h4>
                <p style="color: #ffffff;">Nosso XGBoost acerta <b>83% das variações</b> de preço, mas revela fragilidade em imóveis premium - nossa próxima fronteira a conquistar.</p>
            </div>
        </div>
        
        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 8px; border: 1px solid #1e3a8a; margin-bottom: 30px;">
        <h3 style="color: #ff0000;">🔭 VISÃO DO FUTURO: ONDE ESTAMOS INDO</h3>
        <p style="color: #ffffff;">Estamos construindo mais que um modelo - uma plataforma que pode redefinir padrões do mercado:</p>
        <ul style="color: #ffffff; columns: 2; column-gap: 30px;">
            <li><b>Precisão Cirúrgica:</b> Meta de reduzir o erro para <b>US$ 12.000</b> com técnicas avançadas de ensemble</li>
            <li><b>Expansão Estratégica:</b> Levar o modelo para 5 novas cidades em 12 meses</li>
            <li><b>Transparência Radical:</b> Dashboard explicativo para cada previsão gerada</li>
            <li><b>Monetização Inteligente:</b> Modelo SaaS para corretores com ROI estimado de 3x</li>
        </ul>
        </div>
        
        <div style="background-color: #0a0a0a; padding: 20px; border-radius: 8px; border: 1px solid #ff0000;">
        <h3 style="color: #1e90ff; text-align: center;">💡 OPORTUNIDADE ÚNICA</h3>
        <p style="color: #ffffff; text-align: center; font-size: 1.1em;">
        <b>Este projeto comprovou que algoritmos abertos podem competir com soluções proprietárias.</b><br>
        Com recursos adicionais, podemos não apenas igualar, mas <b>superar</b> os modelos atuais, criando um padrão mais justo para o mercado.
        </p>
        <p style="text-align: center; margin-top: 20px;">
        <span style="color: #ff0000; font-weight: bold;">Próxima Parada:</span> 
        <span style="color: #1e90ff;">Redução de 20% no erro preditivo e expansão para novos mercados</span>
        </p>
        </div>
        """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #ffffff; font-size: 0.9em; background-color: #000000; padding: 10px; border-top: 1px solid #1e3a8a;">
    <p>© 2023 Ames Housing Predictor | Desenvolvido para criar alternativas justas no mercado imobiliário</p>
</div>
""", unsafe_allow_html=True)