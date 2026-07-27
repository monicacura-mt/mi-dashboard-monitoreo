import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Monitoreo Logístico",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Dashboard de Monitoreo y Control Operativo")
st.markdown("Carga tus archivos de **Registro de Viajes** y/o **Matriz de Control** para visualizar la radiografía completa de la operación.")

# Sidebar para cargar archivos
st.sidebar.header("📁 Cargar Archivos de Excel")
uploaded_file = st.sidebar.file_loc = st.sidebar.file_uploader(
    "Sube la Matriz de Operaciones / Control", 
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        
        # Filtro de hoja en la barra lateral
        selected_sheet = st.sidebar.selectbox("Selecciona la pestaña a analizar:", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        # Limpieza rápida de columnas
        df.columns = [str(c).strip() for c in df.columns]
        
        # --- CASO 1: Pestañas de Registro de Viajes ---
        if 'CLIENTE' in df.columns and ('FECHA_INICIO' in df.columns or 'ORIGEN' in df.columns):
            st.success(f"Analizando la hoja: **{selected_sheet}** ({len(df):,} registros encotrados)")
            
            # Filtros en Sidebar
            st.sidebar.subheader("🎯 Filtros Operativos")
            
            # Filtro por Cliente
            clientes = ['Todos'] + sorted(list(df['CLIENTE'].dropna().unique()))
            cliente_sel = st.sidebar.selectbox("Filtrar por Cliente:", clientes)
            
            df_filtered = df.copy()
            if cliente_sel != 'Todos':
                df_filtered = df_filtered[df_filtered['CLIENTE'] == cliente_sel]
                
            # Métricas Principales (KPIs)
            st.markdown("### 📈 KPIs Operativos")
            col1, col2, col3, col4 = st.columns(4)
            
            col1.metric("Total de Viajes", f"{len(df_filtered):,}")
            
            if 'HORAS MONITOREADAS' in df_filtered.columns:
                col2.metric("Pestaña Seleccionada", selected_sheet)
            if 'UNIDAD' in df_filtered.columns:
                col3.metric("Unidades Activas", df_filtered['UNIDAD'].nunique())
            if 'OPERADOR' in df_filtered.columns:
                col4.metric("Operadores Registrados", df_filtered['OPERADOR'].nunique())
                
            st.divider()
            
            # Gráficas Principales
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🏆 Top 10 Clientes con Más Viajes")
                top_clientes = df_filtered['CLIENTE'].value_counts().head(10).reset_index()
                top_clientes.columns = ['Cliente', 'Viajes']
                fig_clientes = px.bar(top_clientes, x='Viajes', y='Cliente', orientation='h', 
                                      color='Viajes', color_continuous_scale='Blues')
                fig_clientes.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_clientes, use_container_width=True)
                
            with c2:
                if 'ORIGEN' in df_filtered.columns:
                    st.subheader("📍 Top 10 Rutas de Origen")
                    top_origen = df_filtered['ORIGEN'].value_counts().head(10).reset_index()
                    top_origen.columns = ['Origen', 'Cantidad']
                    fig_origen = px.pie(top_origen, names='Origen', values='Cantidad', hole=0.4)
                    st.plotly_chart(fig_origen, use_container_width=True)

            # Detalle de la tabla
            with st.expander("📄 Ver detalle de los datos filtrados"):
                st.dataframe(df_filtered)

        # --- CASO 2: Comparativa de Facturación ---
        elif 'CLIENTE' in df.columns or 'CLIENTE' in [c.strip() for c in df.columns] and 'VIAJES REALES' in str(df.columns):
            st.success("Análisis de Comparativa y Facturación Detectado")
            st.dataframe(df)

        else:
            st.info(f"Pestaña cargada: **{selected_sheet}**")
            st.dataframe(df.head(50))
            
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
else:
    st.info("👆 Por favor sube tu archivo `.xlsx` desde el menú lateral para comenzar a generar los reportes.")
