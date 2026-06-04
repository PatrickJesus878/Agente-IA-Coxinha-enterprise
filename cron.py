from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

urls = [
    "https://agente-ia-coxinha-enterprise.streamlit.app/"
]

def wake_up_apps():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Estas duas linhas abaixo são necessárias para o robô funcionar dentro do GitHub Actions:
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    for url in urls:
        try:
            print(f"--- Verificando: {url} ---")
            driver.get(url)
            
            # Espera 15 segundos para dar tempo à página de carregar o botão
            time.sleep(15)
            
            try:
                # Procura o botão azul pelo texto exato que o Streamlit usa
                button = driver.find_element(By.XPATH, "//button[contains(., 'Yes, get this app back up!')]")
                if button:
                    print(f"Botão de despertar encontrado em {url}. A clicar...")
                    button.click()
                    
                    print("Aguardando 35 segundos para a inicialização...")
                    time.sleep(35)
                    
                    driver.refresh()
                    time.sleep(10)
                    print(f"Aplicação {url} deve estar agora disponível.")
            except:
                print(f"A aplicação {url} já parece estar acordada ou o botão não foi necessário.")
                
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

    driver.quit()
    print("--- Processo finalizado ---")

if __name__ == "__main__":
    wake_up_apps()
