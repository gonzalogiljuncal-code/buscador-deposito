
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Pasillos", page_icon="👟")

st.title("👟 Buscador de Pasillos")
st.markdown("Busca el modelo para saber su ubicación en el depósito.")

@st.cache_data
def load_data():
    # Buscamos el archivo en el repositorio
    file_path = 'estanterias_shop.csv' 
    df = pd.read_csv(file_path)
    model_cols = [col for col in df.columns if 'MODELO' in col]
    
    lista_modelos = []
    mapping = {}
    
    for _, row in df.iterrows():
        pasillo = str(row.iloc[0]).strip() # Usamos la primera columna
        if pd.isna(row.iloc[0]) or pasillo.lower() == 'nan':
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

try:
    modelos, ubicaciones = load_data()
    seleccion = st.selectbox("Seleccioná o escribí el modelo:", [""] + modelos)

    if seleccion:
        pasillos = ubicaciones[seleccion]
        st.subheader(f"📍 Ubicación: {seleccion}")
        for p in pasillos:
            st.success(f"✅ **{p}**")
except Exception as e:
    st.error("Error: Asegurate de que el archivo 'estanterias_shop.csv' esté en el repositorio.")
