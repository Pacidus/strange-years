import re
import sys
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed

match sys.argv:
    case ["download_data.py", folder]:
        pass
    case ["download_data.py"]:
        folder = "./"

api = "https://www.data.gouv.fr/api/2/datasets"
idata = "5de8f397634f4164071119c5"
apir = "resources"

b = "█"
w = " "
L = 70

def write(file, text):
    with open(file, "w") as fwt:
        fwt.write(text)

def download(year, url):
    file = f"{folder}/{year}.txt"
    get = requests.get(url)
    write(file, get.text)
    return int(year)

print(f"Les fichiers seronts stockées dans '{folder}'.")

# On récupère le nombre de resources
Nres = requests.get(f"{api}/{idata}").json()["resources"]["total"]
query = {"page": 1, "page_size": Nres}

print(f"Première requete réussie, nombre de ressources sur la base: {Nres}.")

# On récupère les adresses de toutes les données
rdata = requests.get(f"{api}/{idata}/{apir}/", params=query).json()["data"]

print("Récupération des adresses pour toutes les données effectuées.")

nres = 0
to_download = []
for i, data in enumerate(rdata):
    match re.split(r"-|\.", data["title"]):
        case ["deces", year, "txt"]:
            nres += 1
            to_download += [(year, data["latest"])]

print(f"Nombre d'années complètes: {nres}.")

to_download = sorted(to_download)
years = [i for i,j in to_download]
y0 = int(years[0])
where = ["0"] * nres
done = 0
Mth = 8
with ThreadPoolExecutor(max_workers=Mth) as executor:
    future = {executor.submit(download, *arg) for arg in to_download}
    for exc in as_completed(future):
        where[exc.result() - y0] = "1"
        y = years["".join(where).find("0")]
        done += 1
        l = int(L * done / nres)
        string = f"|{b*l}{w*(L-l)}|{done/nres:6.1%} {done}/{nres} {y}" 
        print(string, end="\r")

print(f"|{b*L}|{1:6.1%}")
print("Données récupérées")
