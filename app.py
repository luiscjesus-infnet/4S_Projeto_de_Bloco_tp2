import streamlit as st
import pandas as pd
from collections import Counter # Biblioteca padrão do Python para contar palavras (Nuvem de palavras)
import io

st.set_page_config(page_title="Dashboard ESG - TP2", layout="wide")
st.title("💧 Painel Dinâmico de Saneamento e Sustentabilidade")

# ==========================================
# 1. CACHE DATA (Trabalho Caro)
# ==========================================
# Utilizamos @st.cache_data para ler o arquivo do scraping apenas uma vez, 
# compartilhando o resultado com todos os usuários e melhorando a performance.
@st.cache_data
def carregar_noticias():
    try:
        with open("data/noticias.txt", "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return [] # Fallback caso o web scraping ainda não tenha sido rodado

noticias = carregar_noticias()

# ==========================================
# 2. STATE SESSION (Memória do Usuário)
# ==========================================
# Inicializa uma memória para o usuário não perder os estados favoritados a cada atualização da página.
if 'favoritos' not in st.session_state:
    st.session_state['favoritos'] = []

st.sidebar.header("Filtros Interativos")
novo_favorito = st.sidebar.selectbox("Adicionar Estado aos Favoritos:", ["SP", "RJ", "MG", "BA", "RO"])

if st.sidebar.button("Favoritar"):
    if novo_favorito not in st.session_state['favoritos']:
        st.session_state['favoritos'].append(novo_favorito) # Acumulando dados na sessão

if st.sidebar.button("Limpar Favoritos"):
    st.session_state['favoritos'] = [] # Resetando a memória

st.sidebar.write("Estados Favoritados:", st.session_state['favoritos'])

# ==========================================
# 3. ESTATÍSTICAS E CONTAGEM (Nuvem de Palavras)
# ==========================================
st.subheader("📰 Análise de Notícias (Web Scraping)")
if noticias:
    st.write(f"**Total de notícias extraídas:** {len(noticias)}")
    
    # Fazer nuvem de palavras é basicamente contar palavras, 
    # o que pode ser feito com a biblioteca padrão do Python.
    texto_completo = " ".join(noticias).lower()
    palavras = [p for p in texto_completo.split() if len(p) > 3] # Filtro simples
    contagem = Counter(palavras).most_common(5) # Pegando as 5 palavras mais comuns
    
    df_palavras = pd.DataFrame(contagem, columns=["Palavra", "Frequência"])
    st.bar_chart(df_palavras.set_index("Palavra")) # Exibindo a estatística
else:
    st.warning("Nenhuma notícia encontrada. Rode o script de coleta web primeiro.")

# ==========================================
# 4. UPLOAD E DOWNLOAD DE ARQUIVOS
# ==========================================
st.subheader("📂 Envio e Exportação de Dados")

# O file_uploader cria um botão para o usuário subir arquivos, e a tag 'type' restringe apenas a CSV.
arquivo_enviado = st.file_uploader("Faça upload de uma base complementar (CSV)", type=["csv"])

if arquivo_enviado is not None:
    # Lendo o arquivo se ele existir
    df_upload = pd.read_csv(arquivo_enviado)
    st.write("Pré-visualização dos dados enviados:")
    st.dataframe(df_upload.head(3))
    
    # Preparando o dado enviado pelo usuário para download
    csv_baixar = df_upload.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Baixar Base Processada",
        data=csv_baixar,
        file_name="dados_processados.csv",
        mime="text/csv"
    )