#! env/bin/python3

from pathlib import Path
import shutil

from requests import get
from bs4 import BeautifulSoup

import categorie
import article


path = Path("./extractions")
pathImg = Path(f"{path.resolve()}/Images")

page = get("http://books.toscrape.com/")
if page.status_code == 200:

    # Suppression du dossier de sortie
    try:
        if path.exists():
            shutil.rmtree(path.resolve())
    except:
        print(f"Impossible de supprimer le dossier {path.resolve()}")     # Arrêt --
    else:
        path.mkdir()        # Création des dossiers
        pathImg.mkdir()

        try:
            # -- Recherche des catégories et lancement des lectures
            soup = BeautifulSoup(page.content, "html.parser")
            liste = soup.find("ul", class_="nav nav-list").find("ul").find_all("a")
            liste.sort(key=lambda elem : elem.string)       # Affichage plus agréable
            print("Traitement en cours")

            # -- Création d'une barre de progression envoyée au module article pour l'affichage
            progression = str()
            for i, c in enumerate(liste):
                progression = "["
                for j in range(14):
                    if j <= int(i * 14 / len(liste)):
                        progression +="X"
                    else:
                        progression +="–"

                progression += "]"

                # --
                categorie.lectureCategorie("http://books.toscrape.com/" + c["href"], path.resolve(), progression)

            print("\nExtraction terminée")

        except AttributeError:
            print("\nErreur lors de la recherche d'une balise - Extraction impossible")     # Site modifié, revoir les soup.find

        finally:
            print(f"\n{categorie.compteurCategorie} catégories et {article.compteurArticle} articles traités")

