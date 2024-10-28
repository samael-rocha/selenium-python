from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from email_smtp import enviar_email
from time import sleep

# elementos
link = 'https://www.mercadolivre.com.br/'
SEARCH_BOX = 'nav-search-input' # classe
OFERTAS_BUTTON = '/html/body/header/div/div[5]/div/ul/li[2]/a' #xpath
PRODUTOS_LOC = 'andes-card poly-card poly-card--grid-card andes-card--flat andes-card--padding-0 andes-card--animated' #classe
TITULO_LOC = 'poly-component__title' #classe
EMPRESA_LOC = 'poly-component__seller'  #classe
PRECO_INTEIRO = 'andes-money-amount__fraction' #classe
PRECO_CENTAVOS = 'andes-money-amount__cents andes-money-amount__cents--superscript-24' #classe
FIGURA_LOC = 'poly-component__picture' #figura

# setup driver
chrome_service = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument("--headless") # rodar sem interface gráfica
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")

# instancia do navegador
driver = webdriver.Chrome(service=chrome_service, options=chrome_options) 


driver.get(link)

# clicl no botão de ofertas do dia
ofertas = WebDriverWait(driver,15).until(
    EC.element_to_be_clickable((By.XPATH, OFERTAS_BUTTON))
)
ofertas.click()

sleep(10)

try: # coleta dos titulos
    titulos_web = driver.find_elements(By.CLASS_NAME, TITULO_LOC)
except Exception as e:
    print(e)

try: # coleta dos nome das empresas
    empresas_web = driver.find_elements(By.CLASS_NAME, EMPRESA_LOC)
except Exception as e:
    print(e)

try: # coleta dos links
    link_web = driver.find_elements(By.CLASS_NAME, TITULO_LOC)
except Exception as e:
    print(e)

# transformando em listas
titulos = [titulo.text for titulo in titulos_web[:20]]
empresas = [empresa.text for empresa in empresas_web[:20]]
links = [link.get_attribute('href') for link in link_web[:20]]

# encerrando o navegador
driver.quit()

tabela_html = """

<p>Produtos em Oferta hoje no Mercado Livre</p>
<p>Corra logo e venha aproveitar</p>

<table >
    <thead>
        <tr>
            <th>Titulo Produto</th>
            <th>Empresa</th>
        </tr>
    </thead>
    <tbody>
"""
# construção das listas para criar as linhas da tabela
for i in range(len(titulos)):
    tabela_html += f"""
        <tr>
            <td><a href="{link[i]}">{titulos[i]}</a></td>
            <td>{empresas[i]}</td>
        </tr>
    """

# Fechando a tabela
tabela_html += """
    </tbody>
</table>
"""
# parametros para envio de email
assunto = 'Ofertas Mercado Livre'
email_origem = 'email_origem@gmail.com'
email_destino = 'email_destino@gmail.com'
corpo = tabela_html

# puchando a função criada em email_smtp.py para o envio do email
enviar_email(assunto, email_origem, email_destino, corpo)