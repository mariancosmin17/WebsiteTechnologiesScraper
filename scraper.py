import requests
from bs4 import BeautifulSoup
import re

url_de_test="https://kyliecosmetics.com"

headere_browser={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

reguli_tehnologii={
    "Cloudflare":{
        "headers":{"server":"cloudflare"}
    },
    "Shopify": {
        "html": "cdn\\.shopify\\.com",
        "cookies": "_shopify_y"
    },
    "WordPress": {
        "html": "wp-content/themes"
    },
    "Google Analytics": {
        "html": "google-analytics\\.com/analytics\\.js"
    }
}

try:
    raspuns=requests.get(url_de_test,headers=headere_browser,timeout=10)
    html_brut=raspuns.text
    headere_lowercase={cheie.lower():valoare.lower() for cheie,valoare in raspuns.headers.items()}
    tehnologii_gasite={}
    cookies=raspuns.cookies.get_dict()

    for teh,reguli in reguli_tehnologii.items():
        if "html" in reguli:
            tipar_cautat=reguli["html"]
            potrivire=re.search(tipar_cautat,html_brut,re.IGNORECASE)
            if potrivire:
                tehnologii_gasite[teh]=f"s a gasit tiparul {tipar_cautat} in codul html"
                continue

        if "headers" in reguli:
            for header_cautat,valoare_cautata in reguli["headers"].items():
                if header_cautat in headere_lowercase and re.search(valoare_cautata,headere_lowercase[header_cautat],re.IGNORECASE):
                    tehnologii_gasite[teh]=f"s a gasit {valoare_cautata} in header-ul {header_cautat}"
                    continue

        if "cookies" in reguli:
            nume_cookie=reguli["cookies"]
            if nume_cookie in cookies:
                tehnologii_gasite[teh]=f"s a gasit {nume_cookie} in cookies"
                continue

    if tehnologii_gasite:
        for tehnologie,dovada in tehnologii_gasite.items():
            print(f"{tehnologie}")
            print(f" : {dovada}")
    else:
        print("nu am detectat nimic")

except Exception as e:
    print(f"A aparut o eroare: {e}")