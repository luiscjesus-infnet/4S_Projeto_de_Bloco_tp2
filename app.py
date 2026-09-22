import streamlit as st
import pandas as pd
from collections import Counter

# 1. Configuração Inicial
st.set_page_config(page_title="Dashboard ODS 6", layout="wide")
st.title("💧 Painel Dinâmico: Saneamento e Meio Ambiente")

# ==========================================
# 2. CACHE DATA (Performance)
# ==========================================
# Lendo o arquivo TXT que o nosso script de web scraping gerou[cite: 3]
@st.cache_data
def carregar_noticias():
    try:
        with open("data/noticias.txt", "r", encoding="utf-8") as f:
            # Retorna uma lista limpando os espaços em branco de cada linha
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    except FileNotFoundError:
        return []

lista_noticias = carregar_noticias()

# ==========================================
# 3. SESSION STATE (Memória do Usuário)
# ==========================================
if 'termos_buscados' not in st.session_state:
    st.session_state['termos_buscados'] = []

# ==========================================
# 4. FILTROS INTERATIVOS COM FORMULÁRIO
# ==========================================
st.sidebar.header("Filtros de Notícias")

# O st.form evita que a página recarregue a cada caractere digitado[cite: 12]
with st.sidebar.form("filtros_form"):
    st.write("Filtre o conteúdo raspado da web:")
    
    # Substituímos o multiselect pelo text_input para buscar palavras nas frases do TXT[cite: 12]
    termo_busca = st.text_input("Buscar palavra-chave (ex: água, clima):", "")
    
    aplicar_filtros = st.form_submit_button("Aplicar Filtros")

# Salvando histórico de buscas na sessão
if aplicar_filtros and termo_busca and termo_busca not in st.session_state['termos_buscados']:
    st.session_state['termos_buscados'].append(termo_busca)

if st.session_state['termos_buscados']:
    st.sidebar.write("**Últimas buscas:**", st.session_state['termos_buscados'])
    if st.sidebar.button("Limpar Histórico"):
        st.session_state['termos_buscados'] = []

# ==========================================
# 5. APLICAÇÃO DOS FILTROS E EXIBIÇÃO
# ==========================================
st.subheader("📰 Radar da Mídia: Impactos Ambientais")

# Filtrando a lista de textos baseada no que o usuário digitou
noticias_filtradas = lista_noticias
if aplicar_filtros and termo_busca:
    noticias_filtradas = [noticia for noticia in lista_noticias if termo_busca.lower() in noticia.lower()]

# ==========================================
# 6. GRÁFICO / NUVEM DE PALAVRAS E TABELA
# ==========================================
if noticias_filtradas:
    st.write(f"**Exibindo {len(noticias_filtradas)} manchete(s) encontrada(s).**")
    
    # Exibe as notícias em formato de tabela simples
    df_exibicao = pd.DataFrame(noticias_filtradas, columns=["Manchetes Extraídas"])
    st.dataframe(df_exibicao, use_container_width=True)
    
    st.markdown("### 📊 Frequência de Termos (Nuvem de Palavras)")
    
    # Contando palavras da lista filtrada
    texto_completo = " ".join(noticias_filtradas).lower()
    palavras = [p for p in texto_completo.split() if len(p) > 3]
    contagem = Counter(palavras).most_common(10)
    
    # Plotando o gráfico
    if contagem:
        df_palavras = pd.DataFrame(contagem, columns=["Palavra", "Frequência"])
        st.bar_chart(df_palavras.set_index("Palavra"))
else:
    st.warning("Nenhuma notícia encontrada com o termo buscado ou o arquivo TXT está vazio.")

# ==========================================
# 7. UPLOAD E DOWNLOAD DE ARQUIVOS
# ==========================================
st.markdown("---")
st.subheader("📂 Envio e Exportação de Dados Complementares")
st.write("Insira uma base própria para análise ou baixe a nossa amostra.")

arquivo_enviado = st.file_uploader("Faça upload de uma base (CSV)", type=["csv"])

if arquivo_enviado is not None:
    df_upload = pd.read_csv(arquivo_enviado)
    st.write("Pré-visualização dos dados enviados:")
    st.dataframe(df_upload.head())
    
    csv_baixar = df_upload.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Baixar Base Processada",
        data=csv_baixar,
        file_name="dados_processados.csv",
        mime="text/csv"
    )