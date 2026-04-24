import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Buscador de Pasillos John Foos", page_icon="👟")

st.title("👟 Buscador de Pasillos JF")
st.markdown("Ingresá el modelo para saber su ubicación.")

@st.cache_data
def load_data():
    file_name = 'estanterias_shop.csv'
    if not os.path.exists(file_name):
        return None, None

    try:
        # Leemos el CSV sin importar los nombres de las columnas
        df = pd.read_csv(file_name, sep=',', on_bad_lines='skip')
        
        lista_modelos = []
        mapping = {} 
        
        for _, row in df.iterrows():
            # Usamos iloc[0] para la primera columna (Pasillo)
            pasillo = str(row.iloc[0]).strip()
            if pd.isna(row.iloc[0]) or pasillo.lower() == 'nan' or pasillo == "":
                continue
            
            # Usamos el resto de las columnas para los modelos
            modelos_en_fila = row.iloc[1:]
            for val in modelos_en_fila:
                modelo = str(val).strip()
                if pd.notna(val) and modelo != "" and modelo.lower() != 'nan':
                    if modelo not in mapping:
                        mapping[modelo] = []
                    if pasillo not in mapping[modelo]:
                        mapping[modelo].append(pasillo)
                    if modelo not in lista_modelos:
                        lista_modelos.append(modelo)
        
        return sorted(lista_modelos), mapping
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return None, None

try:
    modelos, ubicaciones = load_data()

    if modelos is None:
        st.error("⚠️ No se pudo cargar el archivo 'estanterias_shop.csv'.")
    else:
        seleccion = st.selectbox(
            "Seleccioná o escribí el modelo:",
            options=[""] + modelos,
            format_func=lambda x: "🔎 Buscar modelo..." if x == "" else x
        )

        if seleccion:
            pasillos = ubicaciones[seleccion]
            st.subheader(f"📍 Ubicación: {seleccion}")
            for p in pasillos:
                st.success(f"✅ **{p}**")
                
except Exception as e:
    st.error(f"Error inesperado: {e}")
