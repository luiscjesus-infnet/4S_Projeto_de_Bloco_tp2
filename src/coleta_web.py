import requests
from bs4 import BeautifulSoup
from pathlib import Path

def realizar_coleta():
    # 1. Criando o "caminho robusto" ensinado nas aulas[cite: 5, 6]
    # Path(__file__).resolve() acha o local exato deste script (pasta src).
    # .parent.parent volta para a raiz do projeto, para então acessar a pasta data com segurança.
    caminho_base = Path(__file__).resolve().parent.parent
    caminho_dados = caminho_base / "data"
    caminho_dados.mkdir(parents=True, exist_ok=True)
    
    url = "https://agenciabrasil.ebc.com.br/meio-ambiente" 
    
    # 2. Fazendo a requisição
    resposta = requests.get(url)
    
    # 3. Verificando se o site nos bloqueou antes de tentar salvar arquivo vazio[cite: 3]
    if resposta.status_code != 200:
        print(f"Erro! O site recusou o acesso. Código: {resposta.status_code}")
        return
        
    print("Acesso liberado! Salvando o HTML...")
    arquivo_html = caminho_dados / "snapshot_meio_ambiente.html"
    
    with open(arquivo_html, "w", encoding="utf-8") as f:
        f.write(resposta.text)
        
    # 4. Lendo o arquivo local com Beautiful Soup
    with open(arquivo_html, "r", encoding="utf-8") as f:
        sopa = BeautifulSoup(f, "html.parser")
        
    # Busca todas as tags de link ('a') da página inteira[cite: 3]
    todos_os_links = sopa.find_all("a") 
    
    noticias_salvas = 0
    arquivo_txt = caminho_dados / "noticias.txt"
    
    with open(arquivo_txt, "w", encoding="utf-8") as txt:
        for link in todos_os_links:
            # Puxa o endereço (href) de dentro da tag
            href = link.get("href", "")
            
            # Filtra apenas os links que contêm a palavra "noticia"[cite: 3]
            if "noticia" in href: 
                # Pega o texto da chamada da reportagem[cite: 3]
                texto = link.get_text(strip=True)
                
                # Garante que não vai salvar textos vazios
                if texto: 
                    txt.write(f"{texto}\n")
                    noticias_salvas += 1
            
    print(f"Sucesso! Foram salvas {noticias_salvas} notícias na pasta data.")

if __name__ == "__main__":
    realizar_coleta()