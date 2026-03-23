import pandas as pd
import numpy as np
from geopy.distance import geodesic

def calcular_distribuicao_velas(df, min_pess=3, max_pess=5):
    # 1. Limpeza e Normalização
    df = df.copy()
    df['grupo_id'] = df['grupo_id'].fillna('geral')
    # morada_id serve para identificar a mesma casa
    df['morada_id'] = df['morada'].fillna('desconhecido').str.lower().str.strip()
    
    velas_finais = []
    sobras = []

    # --- FASE 1: Prioridade por GRUPO_ID ---
    # Agrupamos por afiliação primeiro para garantir que amigos/família ficam juntos
    grupos = df.groupby('grupo_id')
    
    for _, group_df in grupos:
        lista_pessoas = group_df.to_dict('records')
        n = len(lista_pessoas)
        
        if n >= min_pess:
            # Calculamos quantas velas este grupo precisa
            # k = número de velas
            k = n // max_pess + (1 if n % max_pess != 0 else 0)
            
            # Ajuste: se n/k for menor que o mínimo, reduzimos o número de velas
            if k > 1 and n / k < min_pess:
                k = n // min_pess
            
            if k < 1: k = 1
            
            # Dividir o grupo em k velas o mais iguais possível
            # Ex: 6 pessoas viram 3+3 em vez de 5+1
            base_size = n // k
            extras = n % k
            
            idx = 0
            for i in range(k):
                tamanho_atual = base_size + (1 if i < extras else 0)
                if tamanho_atual > 0:
                    velas_finais.append(lista_pessoas[idx : idx + tamanho_atual])
                    idx += tamanho_atual
        else:
            # Grupos demasiado pequenos vão para as sobras para serem unidos por geografia
            sobras.extend(lista_pessoas)

    # --- FASE 2: Unir Sobras por Proximidade (Geografia + Morada) ---
    while len(sobras) > 0:
        ponto_ancora = sobras.pop(0)
        vela_atual = [ponto_ancora]
        
        while len(vela_atual) < max_pess and len(sobras) > 0:
            def calcular_afinidade(p1, p2):
                dist = geodesic((p1['lat'], p1['lon']), (p2['lat'], p2['lon'])).meters
                # Se for a MESMA morada (mesma casa), a distância é virtualmente zero
                if p1['morada_id'] == p2['morada_id'] and p1['morada_id'] != 'aveiro':
                    return dist * 0.01
                # Se for o mesmo grupo (embora pequeno), também tem prioridade
                if p1['grupo_id'] == p2['grupo_id']:
                    return dist * 0.1
                return dist

            distancias = [calcular_afinidade(ponto_ancora, s) for s in sobras]
            idx_proximo = np.argmin(distancias)
            vela_atual.append(sobras.pop(idx_proximo))
            
        # Validação de última vela
        if len(vela_atual) < min_pess and len(velas_finais) > 0:
            velas_finais[-1].extend(vela_atual)
        else:
            velas_finais.append(vela_atual)
            
    return velas_finais