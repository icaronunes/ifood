import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import urljoin

# URL alvo
url =  "https://www.ifood.com.br/delivery/sao-paulo-sp/boi-gaucho---unidade-penha-penha/c25cfc08-348f-4a44-ada2-b69e9e55f58f"

# Configurar Selenium (headless = sem abrir janela do navegador)
chrome_options = Options()
# chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

time.sleep(3)
# Espera um pouco para a página renderizar (ajuste se precisar)
last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(0, last_height, 200):  # Rola a página 5 vezes
    driver.execute_script(f"window.scrollTo(0, {i});")
    time.sleep(0.4)

# Criar pasta para salvar
os.makedirs("imagens", exist_ok=True)

# Pega todas as tags <img>
imgs = driver.find_elements("css selector", "img.dish-card__image")

for i, img in enumerate(imgs, start=1):
    src = img.get_attribute("src")
    if not src:
        continue

    # Resolver URL
    img_url = urljoin(url, src)

    try:
        # Nome do arquivo
        filename = os.path.join("imagens", f"img_{i}.jpg")
        # Baixar imagem
        img_data = requests.get(img_url).content
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"✅ Baixada: {filename}")
    except Exception as e:
        print(f"⚠️ Erro ao baixar {img_url}: {e}")

driver.quit()

