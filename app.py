import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Buscador de Pasillos - Depósito", page_icon="👟")

st.title("👟 Buscador de Pasillos")
st.markdown("Ingresá el modelo para saber en qué pasillo se encuentra.")

@st.cache_data
def load_data():
    file_name = 'estanterias_shop.csv'
    
    if not os.path.exists(file_name):
        return None, None

    try:
        # Forzamos el separador de coma y saltamos líneas con errores si las hubiera
        df = pd.read_csv(file_name, sep=',', on_bad_lines='skip')
        
        # El nombre de la columna de pasillos en el nuevo CSV es 'PASILLO'
        pasillo_col = 'PASILLO'
        model_cols = [col for col in df.columns if 'MODELO' in col]
        
        lista_modelos = []
        mapping = {} 
        
        for _, row in df.iterrows():
            pasillo = str(row[pasillo_col]).strip()
            if pd.isna(row[pasillo_col]) or pasillo.lower() == 'nan' or pasillo == "":
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
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None, None

try:
    modelos, ubicaciones = load_data()

    if modelos is None:
        st.error("⚠️ Error crítico al cargar los datos.")
    else:
        seleccion = st.selectbox(
            "Seleccioná o escribí el nombre del modelo:",
            options=[""] + modelos,
            format_func=lambda x: "🔎 Empezá a escribir..." if x == "" else x
        )

        if seleccion:
            pasillos = ubicaciones[seleccion]
            st.subheader(f"📍 Ubicación para: {seleccion}")
            
            if len(pasillos) > 1:
                st.warning(f"Este modelo está en {len(pasillos)} pasillos.")
            
            for p in pasillos:
                st.success(f"✅ **{p}**")
                
except Exception as e:
    st.error(f"Error inesperado: {e}")
