import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import config 

st.set_page_config(
    page_title="LoL meta analytics",
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl="1h") 
def carregar_dados():
    try:
        conexao_str = f"mysql+pymysql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}"
        engine = create_engine(conexao_str)
        
        df_campeoes = pd.read_sql("SELECT * FROM vw_meta_campeoes", con=engine)
        df_rotas = pd.read_sql("SELECT * FROM vw_impacto_rotas", con=engine)
        
        # NOVA CONSULTA: Pega apenas o total de partidas únicas para o subtítulo
        query_total = "SELECT COUNT(DISTINCT match_id) as total FROM estatisticas_partidas"
        total_partidas = pd.read_sql(query_total, con=engine).iloc[0]['total']
        
        return df_campeoes, df_rotas, total_partidas
    except Exception as e:
        st.error(f"Erro ao conectar no banco de dados: {e}")
        return pd.DataFrame(), pd.DataFrame(), 0

df_meta, df_rotas, total_partidas_bd = carregar_dados()

if not df_meta.empty:
    df_meta['kda'] = (df_meta['media_abates'] + df_meta['media_assistencias']) / df_meta['media_mortes'].clip(lower=1)

total_formatado = f"{total_partidas_bd:,}".replace(",", ".")
st.title("League of Legends: Challenger meta analytics")

st.markdown(f"Análise tática de **{total_formatado} partidas** da fila solo/duo para descobrir o verdadeiro impacto de campeões e rotas no meta atual.")

with st.sidebar:
    st.header("Parâmetros de análise")
    filtro_min_partidas = st.slider("Mínimo de partidas (campeões):", 1, 100, 15, 5)
    
    if not df_meta.empty:
        df_meta_filtrado = df_meta[df_meta['total_partidas'] >= filtro_min_partidas]

st.subheader("Visão geral do servidor")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

if not df_meta.empty and not df_rotas.empty:
    with kpi1:
        st.metric(label="Total de campeões analisados", value=len(df_meta_filtrado))
    with kpi2:
        campeao_mais_jogado = df_meta_filtrado.loc[df_meta_filtrado['total_partidas'].idxmax()]
        st.metric(label="Campeão mais jogado", value=campeao_mais_jogado['campeao'], delta=f"{campeao_mais_jogado['total_partidas']} partidas")
    with kpi3:
        campeao_maior_wr = df_meta_filtrado.loc[df_meta_filtrado['win_rate'].idxmax()]
        st.metric(label="Maior win rate", value=campeao_maior_wr['campeao'], delta=f"{campeao_maior_wr['win_rate']}%")
    with kpi4:
        rota_maior_dano = df_rotas.loc[df_rotas['media_dano_causado'].idxmax()]
        st.metric(label="Rota mais letal", value=rota_maior_dano['rota'])

st.divider()

tab1, tab2, tab3 = st.tabs(["Visão geral dos campeões", "Análise de impacto das rotas", "Ficha técnica do campeão"])

# ABA 1
with tab1:
    st.header("Performance do meta")
    
    col_grafico1, col_grafico2 = st.columns([2, 1])
    
    with col_grafico1:
        st.subheader("Quadrante do meta: win rate vs pick rate")
        st.markdown("*Dica: Utilize o filtro 'Mínimo de partidas' na barra lateral esquerda para reduzir a sobreposição de nomes e focar nos campeões mais consolidados.*")
        
        if not df_meta_filtrado.empty:
            lista_destaque = ["Nenhum"] + sorted(df_meta_filtrado['campeao'].unique())
            campeao_destaque = st.selectbox("🔍 Pesquisar e destacar campeão:", lista_destaque)
            
            df_meta_filtrado['cor_destaque'] = df_meta_filtrado['campeao'].apply(
                lambda x: "#DF1B1B" if x == campeao_destaque else '#4C72B0'
            )
            
            fig_quadrante = px.scatter(
                df_meta_filtrado,
                x='total_partidas',
                y='win_rate',
                text='campeao',
                size='media_dano_causado', 
                color='cor_destaque', 
                color_discrete_map="identity", 
                labels={'total_partidas': 'Total de partidas (pick rate)', 'win_rate': 'Taxa de vitória (%)'},
                height=500
            )
            
            fig_quadrante.update_traces(textposition='top center')
            fig_quadrante.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="50% WR")
            fig_quadrante.add_vline(x=df_meta_filtrado['total_partidas'].mean(), line_dash="dash", line_color="gray", annotation_text="Média de partidas")
            
            st.plotly_chart(fig_quadrante, use_container_width=True)
            
    with col_grafico2:
        st.subheader("Top 10 por métrica")
        
        if not df_meta_filtrado.empty:
            tab_dano, tab_ouro, tab_abates, tab_assist, tab_mortes = st.tabs(["Dano", "Ouro", "Abates", "Assistências", "Mortes"])
            
            with tab_dano:
                df_top_dano = df_meta_filtrado.nlargest(10, 'media_dano_causado').sort_values('media_dano_causado', ascending=True)
                fig_dano = px.bar(
                    df_top_dano, x='media_dano_causado', y='campeao', orientation='h',
                    text=df_top_dano['media_dano_causado'].apply(lambda x: f"{x/1000:.1f}k"),
                    hover_data={'media_dano_causado': True, 'win_rate': False}, color_discrete_sequence=['#4C72B0'],
                    labels={'media_dano_causado': 'Dano médio', 'campeao': ''}, height=420
                )
                fig_dano.update_traces(textposition='inside', textfont_color='white')
                fig_dano.update_layout(xaxis=dict(showgrid=False, visible=False), margin=dict(t=10, b=10, l=10, r=10), dragmode=False)
                st.plotly_chart(fig_dano, use_container_width=True, config={'displayModeBar': False})
            
            with tab_ouro:
                df_top_ouro = df_meta_filtrado.nlargest(10, 'media_ouro_coletado').sort_values('media_ouro_coletado', ascending=True)
                fig_ouro = px.bar(
                    df_top_ouro, x='media_ouro_coletado', y='campeao', orientation='h',
                    text=df_top_ouro['media_ouro_coletado'].apply(lambda x: f"{x/1000:.1f}k"),
                    hover_data={'media_ouro_coletado': True, 'win_rate': False}, color_discrete_sequence=['#E8A838'],
                    labels={'media_ouro_coletado': 'Ouro médio', 'campeao': ''}, height=420
                )
                fig_ouro.update_traces(textposition='inside', textfont_color='white')
                fig_ouro.update_layout(xaxis=dict(showgrid=False, visible=False), margin=dict(t=10, b=10, l=10, r=10), dragmode=False)
                st.plotly_chart(fig_ouro, use_container_width=True, config={'displayModeBar': False})

            with tab_abates:
                df_top_abates = df_meta_filtrado.nlargest(10, 'media_abates').sort_values('media_abates', ascending=True)
                fig_abates = px.bar(
                    df_top_abates, x='media_abates', y='campeao', orientation='h',
                    text=df_top_abates['media_abates'].apply(lambda x: f"{x:.1f}"),
                    hover_data={'media_abates': True, 'win_rate': False}, color_discrete_sequence=['#C44E52'],
                    labels={'media_abates': 'Abates médios', 'campeao': ''}, height=420
                )
                fig_abates.update_traces(textposition='inside', textfont_color='white')
                fig_abates.update_layout(xaxis=dict(showgrid=False, visible=False), margin=dict(t=10, b=10, l=10, r=10), dragmode=False)
                st.plotly_chart(fig_abates, use_container_width=True, config={'displayModeBar': False})

            with tab_assist:
                df_top_assist = df_meta_filtrado.nlargest(10, 'media_assistencias').sort_values('media_assistencias', ascending=True)
                fig_assist = px.bar(
                    df_top_assist, x='media_assistencias', y='campeao', orientation='h',
                    text=df_top_assist['media_assistencias'].apply(lambda x: f"{x:.1f}"),
                    hover_data={'media_assistencias': True, 'win_rate': False}, color_discrete_sequence=['#55A868'],
                    labels={'media_assistencias': 'Assistências médias', 'campeao': ''}, height=420
                )
                fig_assist.update_traces(textposition='inside', textfont_color='white')
                fig_assist.update_layout(xaxis=dict(showgrid=False, visible=False), margin=dict(t=10, b=10, l=10, r=10), dragmode=False)
                st.plotly_chart(fig_assist, use_container_width=True, config={'displayModeBar': False})
                
            with tab_mortes:
                df_top_mortes = df_meta_filtrado.nlargest(10, 'media_mortes').sort_values('media_mortes', ascending=True)
                fig_mortes = px.bar(
                    df_top_mortes, x='media_mortes', y='campeao', orientation='h',
                    text=df_top_mortes['media_mortes'].apply(lambda x: f"{x:.1f}"),
                    hover_data={'media_mortes': True, 'win_rate': False}, color_discrete_sequence=['#5E5E5E'], 
                    labels={'media_mortes': 'Mortes médias', 'campeao': ''}, height=420
                )
                fig_mortes.update_traces(textposition='inside', textfont_color='white')
                fig_mortes.update_layout(xaxis=dict(showgrid=False, visible=False), margin=dict(t=10, b=10, l=10, r=10), dragmode=False)
                st.plotly_chart(fig_mortes, use_container_width=True, config={'displayModeBar': False})

# ABA 2
with tab2:
    st.header("Eficiência por posição")
    
    col_grafico3, col_grafico4 = st.columns(2)
    
    with col_grafico3:
        st.subheader("Radar de impacto por rota")
        st.markdown("*Nota: O gráfico utiliza o maior valor do servidor como teto (100%). Por exemplo, se a rota BOTTOM marca 100% em Ouro, significa que ela tem a maior média de acúmulo absoluto entre todas as 5 rotas.*")
        
        if not df_rotas.empty:
            df_radar = df_rotas.copy()
            metricas = ['media_dano_causado', 'media_ouro_coletado', 'media_abates', 'media_assistencias']
            
            for col in metricas:
                max_val = df_radar[col].max()
                df_radar[f'{col}_norm'] = (df_radar[col] / max_val) * 100
            
            rotas_unicas = df_radar['rota'].unique()
            tabs_radar = st.tabs(list(rotas_unicas))
            
            for i, rota in enumerate(rotas_unicas):
                with tabs_radar[i]:
                    row = df_radar[df_radar['rota'] == rota].iloc[0]
                    
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=[row['media_dano_causado_norm'], row['media_ouro_coletado_norm'], row['media_abates_norm'], row['media_assistencias_norm']],
                        theta=['Dano', 'Ouro', 'Abates', 'Assistências'],
                        fill='toself',
                        name=rota,
                        line_color='#4C72B0'
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False, height=400, margin=dict(t=30, b=30, l=30, r=30), dragmode=False
                    )
                    st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
            
    with col_grafico4:
        st.subheader("Distribuição de abates por rota")
        
        if not df_rotas.empty:
            fig_donut = px.pie(
                df_rotas, values='media_abates', names='rota', hole=0.4, 
                color_discrete_sequence=px.colors.sequential.Blues_r 
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            fig_donut.update_layout(height=450, showlegend=False, dragmode=False) 
            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

# ABA 3
with tab3:
    st.header("Ficha técnica do campeão")
    st.markdown("Busque um campeão específico para visualizar suas métricas detalhadas baseadas no meta Challenger.")
    
    if not df_meta.empty:
        lista_campeoes = sorted(df_meta['campeao'].unique())
        campeao_selecionado = st.selectbox("Selecione um Campeão:", lista_campeoes)
        
        if campeao_selecionado:
            dados_camp = df_meta[df_meta['campeao'] == campeao_selecionado].iloc[0]
            
            st.markdown(f"### Estatísticas de **{campeao_selecionado}**")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Win Rate", f"{dados_camp['win_rate']}%")
            c2.metric("Total de Partidas", dados_camp['total_partidas'])
            c3.metric("KDA Médio", f"{dados_camp['kda']:.2f}")
            c4.metric("Dano Médio", f"{dados_camp['media_dano_causado']/1000:.1f}k")
            
            st.markdown("<br>", unsafe_allow_html=True) 
            
            c5, c6, c7, c8 = st.columns(4)
            c5.metric("Abates / Jogo", dados_camp['media_abates'])
            c6.metric("Mortes / Jogo", dados_camp['media_mortes'])
            c7.metric("Assistências / Jogo", dados_camp['media_assistencias'])
            c8.metric("Ouro Médio", f"{dados_camp['media_ouro_coletado']/1000:.1f}k")