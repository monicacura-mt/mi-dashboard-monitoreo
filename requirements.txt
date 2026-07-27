import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página con tema ancho
st.set_page_config(page_title="Centro de Monitoreo", layout="wide")

# CSS personalizado para la estética Dark / Neon exacta
st.markdown("""
    <style>
    .stApp { background-color: #0b111e; color: #ffffff; }
    .kpi-card {
        background-color: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .kpi-title { color: #94a3b8; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }
    .kpi-value { color: #ffffff; font-size: 2rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("📡 CENTRO DE MONITOREO")
st.caption("Panel Dinámico de Control Operativo y GPS")

# Carga interactiva del archivo de Excel
st.sidebar.header("⚙️ Panel de Control")
uploaded_file = st.sidebar.file_uploader("Cargar VIAJES_MENSUALES.xlsx", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Lectura de datos
    df = pd.read_excel(uploaded_file)
    
    # 1. Tarjetas KPI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Viajes</div><div class="kpi-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    with col2:
        clientes_unicos = df['CLIENTE'].nunique() if 'CLIENTE' in df.columns else 0
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Clientes Activos</div><div class="kpi-value">{clientes_unicos}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi-card"><div class="kpi-title">Estatus Operación</div><div class="kpi-value" style="color: #22c55e;">Sincronizado</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="kpi-card"><div class="kpi-title">Sistema</div><div class="kpi-value" style="color: #38bdf8;">En Línea</div></div>', unsafe_allow_html=True)

    st.write("---")

    # 2. Secciones del Dashboard
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📊 Distribución de Viajes")
        if 'CLIENTE' in df.columns:
            top_clientes = df['CLIENTE'].value_counts().head(10).reset_index()
            top_clientes.columns = ['CLIENTE', 'VIAJES']
            
            fig = px.bar(
                top_clientes, x='CLIENTE', y='VIAJES',
                color_discrete_sequence=['#ff6b00']
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="#ffffff"
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("📋 Matriz de Control")
        st.dataframe(df.head(15), use_container_width=True)

else:
    st.info("👈 Por favor, arrastra tu archivo Excel en la barra lateral para desplegar los gráficos.")