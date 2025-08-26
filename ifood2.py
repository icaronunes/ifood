import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL que você quer fazer o scraping
url =  "https://www.ifood.com.br/delivery/sao-paulo-sp/boi-gaucho---unidade-penha-penha/c25cfc08-348f-4a44-ada2-b69e9e55f58f"

# Criar pasta para salvar as imagens
os.makedirs("imagens", exist_ok=True)

# Requisição da página
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar todas as tags <img>
for img in soup.find_all("img"):
    src = img.get("src")
    if not src:
        continue
    
    # Resolver URL absoluta (caso seja relativa)
    img_url = urljoin(url, src)

    # Nome do arquivo
    filename = os.path.join("imagens", os.path.basename(img_url.split("?")[0]))

    try:
        # Baixar imagem
        img_data = requests.get(img_url).content
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"✅ Baixada: {filename}")
    except Exception as e:
        print(f"⚠️ Erro ao baixar {img_url}: {e}")
