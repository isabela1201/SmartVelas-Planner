# SmartVelas-Planner
**Organizador Inteligente e Interativo para a Bênção das Pastas**

**Já podes usar a app online aqui:** 
> https://smartvelas-planner-isabela1201.streamlit.app/

Como possível finalista, basicamente quis complicar a minha vida e fazer um 'planner' interativo e inteligente para a escolha do número de velas que comprar para a Benção das pastas.

## O que é o SmartVelas?
O **SmartVelas-Planner** é uma ferramenta de suporte à decisão que utiliza algoritmos de agrupamento (*clustering*) para sugerir a distribuição ideal de pessoas por velas através da morada e da afiliação. 

O sistema não 'olha' apenas para a proximidade das moradas (via Geocoding), mas prioriza a **afinidade de grupo** PRINCIPALMENTE. Se marcaste várias pessoas com o mesmo ID de grupo, o algoritmo fará de tudo para que fiquem na mesma vela!

## Funcionalidades Principais
- **Entrada de Dados Híbrida:** Suporta a criação manual de cartões ou o import de ficheiros CSV (compatível com listas de contactos simples).
- **Gestão de Grupos e Famílias:** Define grupos inteiros num só cartão ou isola pessoas individualmente.
- **Algoritmo de Otimização:** Calcula a distribuição baseada em limites (mínimo/máximo por vela) e proximidade geográfica.
- **Quadro de Organização Interativo:** Uma interface visual com bordas suaves (Verde UA 🌿) onde podes arrastar (mover) pessoas entre velas para o ajuste final.
- **Exportação Total:** Exporta tanto o rascunho de trabalho como a lista final organizada para partilha.

## Tecnologias Utilizadas
- **Python**: A base de toda a lógica.
- **Streamlit**: Para uma interface web rápida e reativa.
- **Pandas**: Gestão e manipulação de bases de dados CSV.
- **Geopy**: Para converter moradas em coordenadas reais.

## Estética Minimalista
A interface foi desenhada com um tema minimalista que respeita o **Dark Mode** e utiliza a paleta de cores aesthetic da **Universidade de Aveiro**.

## Como instalar e usar
1. Clone o repositório
2. Instale as dependências:
pip install -r requirements.txt
3. Corre a aplicação:
streamlit run app.py

Feito com 💚, cafezinho e brownies de chocolate (props para a Bia :)).
