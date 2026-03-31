import requests

url_de_test="https://www.shopify.com"

headere_browser={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

raspuns=requests.get(url_de_test,headers=headere_browser,timeout=10)

print("cod primit: ",raspuns.status_code)

print("\n Headerele http trimise de server:")
for cheie,valoare in raspuns.headers.items():
    print(f"{cheie}: {valoare}")

print("\n Primele 500 de carac din codul html:")
html_extras=raspuns.text[0:500]
print(html_extras)
