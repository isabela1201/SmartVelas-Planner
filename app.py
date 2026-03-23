import streamlit as st
import pandas as pd
import time
from geopy.geocoders import Nominatim
from brain import calcular_distribuicao_velas

# --- (PEAK VERSION) ---
st.set_page_config(page_title="SmartVelas-Planner", layout="wide", page_icon="𓆝 𓆟 𓆞")

# CSS Inteligente: Verde UA nos botões e Borda Verde nos Cartões das Velas
st.markdown("""
    <style>
    :root { 
        --ua-green: #007D69;        /* Verde Escuro Oficial (para botões) */
        --ua-green-light: #A8DADC;  /* NOVO: Verde Clarinho (para bordas) */
    }
    
    /* Botões Principais com a cor da UA */
    .stButton>button {
        background-color: var(--ua-green) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    /* Hover dos botões */
    .stButton>button:hover {
        background-color: #005a4b !important;
    }

    /* Estilo para os cartões de velas na Aba 2 (Containers com BORDA VERDE CLARA) */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stExpander"] {
        /* MUDANÇA AQUI: Trocámos --ua-green por --ua-green-light e suavizámos a borda para 1px */
        border: 1px solid var(--ua-green-light) !important; 
        border-radius: 8px !important;
        padding: 10px !important;
        /* Opcional: Adiciona um fundo muito suave para destacar */
        background-color: #f0fdf9 !important;
    }
    
    /* Ajuste de cartões da Aba 1 para serem visíveis mas mais discretos */
    div[data-testid="stTabs"] div[data-testid="stHorizontalBlock"] div[data-testid="stExpander"] {
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

geolocator = Nominatim(user_agent="velastack_ua_vFinal")

# Inicialização segura do Session State
if 'entidades' not in st.session_state: st.session_state.entidades = []
if 'edit_index' not in st.session_state: st.session_state.edit_index = -1
if 'velas_layout' not in st.session_state: st.session_state.velas_layout = {}

st.title("°‧ 𓆝 SmartVelas 𓆟 Planner 𓆞·｡")
st.caption("Benção das pastas | Organizador de Velas")

# --- SIDEBAR ---
st.sidebar.header("Configurações")
min_p = st.sidebar.slider("Mínimo por vela", 1, 5, 3)
max_p = st.sidebar.slider("Máximo por vela", 2, 10, 5)

st.sidebar.divider()
st.sidebar.header("Dados")
uploaded_file = st.sidebar.file_uploader("Importar CSV", type="csv")

if uploaded_file:
    df_temp = pd.read_csv(uploaded_file)
    dados_importados = []
    for _, row in df_temp.iterrows():
        dados_importados.append({
            'nome': str(row.get('nome', 'Sem Nome')),
            'morada': str(row.get('morada', 'Aveiro')),
            'grupo_id': str(row.get('grupo_id', 'geral')),
            'num': int(row.get('num', 1)),
            'tipo': str(row.get('tipo', 'pessoa')).lower(),
            'locked': bool(row.get('locked', False))
        })
    st.session_state.entidades = dados_importados
    st.sidebar.success("Dados carregados.")

# --- ABAS PRINCIPAIS ---
tab_input, tab_viz = st.tabs(["Gestão de Entidades", "Quadro de Organização"])

# --- ABA 1: INPUT ---
with tab_input:
    is_editing = st.session_state.edit_index != -1
    curr = st.session_state.entidades[st.session_state.edit_index] if is_editing else {'nome': '', 'morada': 'Aveiro', 'grupo_id': '', 'num': 1, 'locked': False, 'tipo': 'pessoa'}

    with st.container():
        st.markdown(f"#### {'Editar' if is_editing else 'Novo'} Item")
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1:
            n_nome = st.text_input("Identificação", value=curr.get('nome', ''))
            n_morada = st.text_input("Localização", value=curr.get('morada', 'Aveiro'))
        with c2:
            n_grupo = st.text_input("Afiliação", value=curr.get('grupo_id', ''))
            tipo_idx = 0 if str(curr.get('tipo', 'pessoa')).lower() == 'pessoa' else 1
            tipo = st.radio("Categoria", ["Pessoa", "Grupo"], index=tipo_idx, horizontal=True)
        with c3:
            n_num = st.number_input("Qtd", min_value=1, value=int(curr.get('num', 1)))
        with c4:
            n_locked = st.checkbox("Fixo", value=bool(curr.get('locked', False)))
            
        if is_editing:
            cb1, cb2 = st.columns(2)
            if cb1.button("Guardar Alterações", key="save_btn"):
                st.session_state.entidades[st.session_state.edit_index] = {
                    'nome': n_nome, 'morada': n_morada, 'grupo_id': n_grupo,
                    'num': n_num, 'tipo': tipo.lower(), 'locked': n_locked
                }
                st.session_state.edit_index = -1
                st.rerun()
            if cb2.button("Cancelar", key="cancel_btn"):
                st.session_state.edit_index = -1
                st.rerun()
        else:
            if st.button("Adicionar ao Plano"):
                if n_nome:
                    st.session_state.entidades.append({
                        'nome': n_nome, 'morada': n_morada, 'grupo_id': n_grupo,
                        'num': n_num, 'tipo': tipo.lower(), 'locked': n_locked
                    })
                    st.rerun()

    st.divider()
    
    if st.session_state.entidades:
        cols = st.columns(4)
        for i, ent in enumerate(st.session_state.entidades):
            with cols[i % 4]:
                with st.container(border=True):
                    st.markdown(f"**{ent.get('nome', 'N/A')}**")
                    st.caption(f"{ent.get('grupo_id', '-')} | Pax: {ent.get('num', 1)}")
                    if ent.get('locked'): st.caption("🔒")
                    
                    eb1, eb2 = st.columns(2)
                    if eb1.button("Editar", key=f"e_{i}"):
                        st.session_state.edit_index = i
                        st.rerun()
                    if eb2.button("Remover", key=f"r_{i}"):
                        st.session_state.entidades.pop(i)
                        st.rerun()

        st.divider()
        if st.button("Gerar Distribuição Inicial", use_container_width=True, type="primary"):
            with st.spinner("O teu tempo de brainrot... aka vai demorar (ᵕ—ᴗ—) "):
                flat_rows = []
                for ent in st.session_state.entidades:
                    qtd = int(ent.get('num', 1))
                    for j in range(qtd):
                        tag = ent['nome'] if qtd == 1 else f"{ent['nome']} ({j+1})"
                        flat_rows.append({
                            'nome': tag, 'morada': ent.get('morada', 'Aveiro'), 
                            'grupo_id': ent.get('grupo_id', 'geral'), 'locked': ent.get('locked', False),
                            'morada_id': str(ent.get('morada', 'Aveiro')).lower().strip()
                        })
                
                df_f = pd.DataFrame(flat_rows)
                lats, lons = [], []
                for m in df_f['morada']:
                    try:
                        loc = geolocator.geocode(m, timeout=2)
                        lats.append(loc.latitude if loc else 40.644)
                        lons.append(loc.longitude if loc else -8.645)
                    except:
                        lats.append(40.644); lons.append(-8.645)
                df_f['lat'], df_f['lon'] = lats, lons
                
                velas_list = calcular_distribuicao_velas(df_f, min_p, max_p)
                st.session_state.velas_layout = {idx + 1: v for idx, v in enumerate(velas_list)}
                st.success("Processamento concluído! Clica agora na aba 'Quadro de Organização' no topo para veres e ajustares o resultado :).");
                st.rerun()

# --- ABA 2: QUADRO DE ORGANIZAÇÃO (COM BORDAS VERDES UA) ---
with tab_viz:
    if not st.session_state.velas_layout:
        st.info("Configura os dados na aba 1 e gera a distribuição.")
    else:
        st.markdown("#### Ajuste Manual (Layout Final)")
        v_keys = sorted(st.session_state.velas_layout.keys())
        cols_viz = st.columns(3)
        for v_id in v_keys:
            with cols_viz[(v_id-1) % 3]:
                # Este container (Expander) terá a borda verde UA via CSS
                with st.expander(f"Vela {v_id}", expanded=True):
                    st.caption("Usa o menu para mover pessoas.")
                    pessoas = st.session_state.velas_layout[v_id]
                    for idx_p, p in enumerate(pessoas):
                        p_name = p['nome']
                        target_v = st.selectbox(
                            f"👤 {p_name}", options=v_keys, index=v_id-1, key=f"mv_{p_name}_{v_id}_{idx_p}"
                        )
                        if target_v != v_id:
                            item = st.session_state.velas_layout[v_id].pop(idx_p)
                            st.session_state.velas_layout[target_v].append(item)
                            st.rerun()
        
        st.divider()
        c_exp1, c_exp2 = st.columns(2)
        csv_input = pd.DataFrame(st.session_state.entidades).to_csv(index=False).encode('utf-8')
        c_exp1.download_button("💾 Backup Dados Entrada", csv_input, "velastack_input.csv", "text/csv")
        
        final_data = []
        for vid, plist in st.session_state.velas_layout.items():
            for p in plist:
                final_data.append({'Vela': vid, 'Nome': p['nome'], 'Grupo': p['grupo_id'], 'Morada': p['morada']})
        csv_final = pd.DataFrame(final_data).to_csv(index=False).encode('utf-8')
        c_exp2.download_button("💾 Exportar Organização Final", csv_final, "velastack_final.csv", "text/csv")