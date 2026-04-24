import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Buscador de Pasillos - Depósito", page_icon="👟")

st.title("👟 Buscador de Pasillos")
st.markdown("Ingresá el modelo para saber en qué pasillo se encuentra.")

@st.cache_data
def load_data():
    # Buscamos el archivo en la misma carpeta donde corre el script
    file_name = 'estanterias_shop.csv'
    
    # Verificación de existencia del archivo
    if not os.path.exists(file_name):
        return None, None

    # Carga de datos
    df = pd.read_csv(file_name)
    
    # Identificar columnas de modelos (asumimos que contienen la palabra 'MODELO')
    model_cols = [col for col in df.columns if 'MODELO' in col]
    
    lista_modelos = []
    mapping = {} 
    
    for _, row in df.iterrows():
        # La primera columna es el Pasillo (Unnamed: 0 o similar)
        pasillo = str(row.iloc[0]).strip()
        if pd.isna(row.iloc[0]) or pasillo.lower() == 'nan' or pasillo == "":
            continue
            
        for col in model_cols:
            modelo = str(row[col]).strip()
            if pd.notna(row[col]) and modelo != "" and modelo.lower() != 'nan':
                if modelo not in mapping:
                    mapping[modelo] = []
                if pasillo not in mapping[modelo]:
                    mapping[modelo].append(pasillo)
                if modelo not in lista_modelos:
                    lista_modelos.append(modelo)
    
    return sorted(lista_modelos), mapping

# Ejecución de la lógica
try:
    modelos, ubicaciones = load_data()

    if modelos is None:
        st.error("⚠️ Error: No se encontró el archivo 'estanterias_shop.csv' en el repositorio.")
        st.info("Asegurate de que el archivo esté subido a GitHub con ese nombre exacto (todo en minúsculas).")
    else:
        # Buscador con autocompletado
        seleccion = st.selectbox(
            "Seleccioná o escribí el nombre del modelo:",
            options=[""] + modelos,
            format_func=lambda x: "🔎 Empezá a escribir..." if x == "" else x
        )

        if seleccion:
            pasillos = ubicaciones[seleccion]
            st.subheader(f"📍 Ubicación para: {seleccion}")
            
            # Si el modelo está en más de un pasillo, avisamos
            if len(pasillos) > 1:
                st.warning(f"Atención: Este modelo está en {len(pasillos)} pasillos.")
            
            for p in pasillos:
                st.success(f"✅ **{p}**")
                
except Exception as e:
    st.error(f"Ocurrió un error inesperado: {e}")
