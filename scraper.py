import requests
import re
import json
import pandas as pd
import concurrent.futures

def analiza_domeniu(url,reguli_tehnologii):

    headere_browser={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    if not url.startswith("http"):
        url = "https://" + url

    tehnologii_gasite = {}

    try:
        raspuns=requests.get(url,headers=headere_browser,timeout=10)
        html_brut=raspuns.text
        headere_lowercase={cheie.lower():valoare.lower() for cheie,valoare in raspuns.headers.items()}
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

        return url,{"succes": True, "tehnologii": tehnologii_gasite, "eroare": None}

    except requests.exceptions.Timeout:
        return url, {"succes": False, "tehnologii": {}, "eroare": "Timeout"}
    except Exception as e:
        return url,{"succes": False, "tehnologii": {}, "eroare": str(e)}

with open('reguli.json','r',encoding='utf-8') as fisier:
    reguli_incarcate=json.load(fisier)

tabel_date = pd.read_parquet('domenii.parquet')
lista_domenii = tabel_date['root_domain'].tolist()

lista_domenii=list(set(lista_domenii))
rezultate_finale={}

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:

    joburi=[executor.submit(analiza_domeniu,domeniu,reguli_incarcate) for domeniu in lista_domenii]

    for job in concurrent.futures.as_completed(joburi):
        url_domeniu,rezultat=job.result()
        rezultate_finale[url_domeniu]=rezultat

with open('rezultate_scanare.json','w',encoding='utf-8') as f:
    json.dump(rezultate_finale,f,indent=4,ensure_ascii=False)
