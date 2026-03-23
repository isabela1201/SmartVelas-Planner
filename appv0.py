import streamlit as st
import pandas as pd
import time
from geopy.geocoders import Nominatim
from brain import calcular_distribuicao_velas 

geolocator = Nominatim(user_agent="bencao_aveiro_final_v4")

st.set_page_config(page_title="Velas UA", layout="wide")
st.title("🎓 Gestor de Velas UA")

# --- SIDEBAR: Configurações e Import ---
st.sidebar.header("📂 Gestão de Dados")
uploaded_file = st.sidebar.file_uploader("Importar CSV", type="csv")

st.sidebar.header("⚙️ Configurações")
min_p = st.sidebar.slider("Mínimo por vela", 1, 5, 3)
max_p = st.sidebar.slider("Máximo por vela", 2, 10, 5)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['nome', 'morada', 'grupo_id'])

if uploaded_file:
    st.session_state.data = pd.read_csv(uploaded_file)

# --- CRIAÇÃO DAS ABAS ---
tab1, tab2 = st.tabs(["🤖 Gerador Automático", "✍️ Ajuste Manual"])

with tab1:
    st.subheader("1. Lista de Pessoas")
    # O editor reflete sempre o que está no session_state
    edited_df = st.data_editor(st.session_state.data, num_rows="dynamic", use_container_width=True, key="editor_v4")

    if st.button("🚀 Gerar Distribuição Automática"):
        if len(edited_df) < min_p:
            st.error(f"Precisas de pelo menos {min_p} pessoas!")
        else:
            with st.spinner("A calcular..."):
                # CRIAR df_proc AQUI (resolve o NameError)
                df_proc = edited_df.copy()
                df_proc['morada_id'] = df_proc['morada'].fillna('aveiro').str.lower().str.strip()
                df_proc['grupo_id'] = df_proc['grupo_id'].fillna('geral')
                
                # Geocodificação
                lats, lons = [], []
                for m in df_proc['morada']:
                    try:
                        loc = geolocator.geocode(m if m else "Aveiro", timeout=5)
                        lats.append(loc.latitude if loc else 40.644)
                        lons.append(loc.longitude if loc else -8.645)
                        time.sleep(0.5)
                    except:
                        lats.append(40.644); lons.append(-8.645)
                
                df_proc['lat'], df_proc['lon'] = lats, lons
                
                # Calcular e guardar no session_state para a Aba 2 ver
                velas_geradas = calcular_distribuicao_velas(df_proc, min_p, max_p)
                
                # Transformar o resultado (lista de listas) num DataFrame plano para edição
                flat_list = []
                for i, vela in enumerate(velas_geradas):
                    for p in vela:
                        p['vela_n'] = i + 1
                        flat_list.append(p)
                
                st.session_state.df_final = pd.DataFrame(flat_list)
                st.success("Velas geradas! Vai à aba 'Ajuste Manual' para conferir.")

with tab2:
    if 'df_final' in st.session_state:
        st.subheader("✍️ Ajuste Fino")
        st.info("Altera o número na coluna 'vela_n' para mover pessoas entre folhas.")
        
        # Editor para a tabela final
        df_editado_final = st.data_editor(
            st.session_state.df_final[['nome', 'grupo_id', 'morada', 'vela_n']], 
            use_container_width=True,
            key="ajuste_manual"
        )
        
        # Resumo Visual Dinâmico
        st.write("### 🕯️ Layout das Velas")
        if not df_editado_final.empty:
            # Agrupar pelo número da vela definido pelo utilizador
            velas_agrupadas = df_editado_final.groupby('vela_n')
            cols = st.columns(3)
            for i, (n_vela, grupo) in enumerate(velas_agrupadas):
                with cols[i % 3]:
                    st.success(f"Vela {int(n_vela)}")
                    for n in grupo['nome']:
                        st.write(f"• {n}")
        
        # Download do resultado final ajustado
        csv_final = df_editado_final.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Baixar Plano de Velas Final", csv_final, "plano_velas_final.csv", "text/csv")
    else:
        st.warning("Clica primeiro no botão da aba anterior para gerar os dados.")