import requests
from bs4 import BeautifulSoup

url_de_test="https://kyliecosmetics.com"

headere_browser={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

raspuns=requests.get(url_de_test,headers=headere_browser,timeout=10)

print("cod primit: ",raspuns.status_code)

tehnologii_gasite={}

headere_lowercase={cheie.lower():valoare.lower() for cheie,valoare in raspuns.headers.items()}

if 'server' in headere_lowercase and 'cloudfare' in headere_lowercase['server']:
    tehnologii_gasite['Cloudfare']="cuvantul cloudfare gasit in headerul http"

navigate=BeautifulSoup(raspuns.text,'html.parser')

toate_scripturile=navigate.find_all('script')

for script in toate_scripturile:
    sursa_script=script.get('src')
    if sursa_script and 'cdn.shopify.com' in sursa_script:
        tehnologii_gasite['Shopify']=f"am gasit un fisier js care incarca de la {sursa_script}"
        break

if len(tehnologii_gasite) > 0:
    for tehnologie,dovada in tehnologii_gasite.items():
        print(f"{tehnologie}")
        print(f" : {dovada}")
else:
    print("nu am detectat nimic")