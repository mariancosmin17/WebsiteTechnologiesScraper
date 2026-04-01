import json
from collections import Counter

try:
    with open('rezultate_scanare.json', 'r', encoding='utf-8') as f:
        date_scanare = json.load(f)
except FileNotFoundError:
    print("eroare:nu am gasit fișierul rezultate_scanare.json")
    exit()

tehnologii_distincte = set()

clasament = Counter()

for domeniu, info in date_scanare.items():
    if info["succes"]:

        if info["tehnologii"]:
            for nume_teh in info["tehnologii"].keys():
                tehnologii_distincte.add(nume_teh)
                clasament[nume_teh] += 1

print(f"{len(tehnologii_distincte)} tehnologii unice în total")

print("topul tehnologiilor gasite:")
for teh, numar in clasament.most_common():
    print(f"{teh}: prezent pe {numar} site-uri")
