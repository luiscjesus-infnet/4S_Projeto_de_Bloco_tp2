import requests
from bs4 import BeautifulSoup
from pathlib import Path

def realizar_coleta():
    # Caminho onde os dados serão salvos (separação de camadas)
    caminho_dados = Path("../data")
    caminho_dados.mkdir(parents=True, exist_ok=True)
    
    url = "https://agenciabrasil.ebc.com.br/meio-ambiente" 
    
    # 1. Fazendo a requisição e salvando o snapshot (boa prática para evitar bloqueios)[cite: 5, 6]
    resposta = requests.get(url)
    arquivo_html = caminho_dados / "snapshot_meio_ambiente.html"
    
    with open(arquivo_html, "w", encoding="utf-8") as f:
        f.write(resposta.text)
        
    # 2. Lendo o arquivo local com Beautiful Soup para extrair os dados[cite: 5]
    with open(arquivo_html, "r", encoding="utf-8") as f:
        sopa = BeautifulSoup(f, "html.parser")
        
    # Extraindo as manchetes (buscando links em cabeçalhos, por exemplo)[cite: 5, 6]
    manchetes = sopa.find_all("h3") 
    
    # 3. Salvando os dados estruturados em um arquivo TXT[cite: 6]
    arquivo_txt = caminho_dados / "noticias.txt"
    with open(arquivo_txt, "w", encoding="utf-8") as txt:
        for manchete in manchetes:
            texto = manchete.get_text(strip=True)
            txt.write(f"{texto}\n")

if __name__ == "__main__":
    realizar_coleta()