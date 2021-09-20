# -*-coding:UTF8 ISO-8859-1 -*
import os
import xml.etree.cElementTree as xml
import json
import codecs

#def json_fusion (json1, json2) :
    
def recherche_dossier (chemin_dossier) :
    '''
        fonction qui pour chaque dossier va chercher les différents formats de fichier,
        va renvoyer un json comportant ces informations avec le nom du dossier.
        Ceci fonctionne pour un dossier spécifique.
    '''
    for root, dirs, files in os.walk(chemin_dossier, topdown=False):
        # par défaut, le nom sera bat, mais il faudrait analyser les mots
        # dans les fichiers pour interpréter
        categories = [{"nom" : "bat"}]
        if files != '' : # y a t-il des fichiers dans le dossier ?
            liste_de_categories = {}
            for name in files:
                file_extension = os.path.splitext(name)[1] # extension du nom
                # on compte le nombre d'extensions
                if (file_extension in liste_de_categories.keys()):
                    liste_de_categories[file_extension] += 1
                else :
                    liste_de_categories[file_extension] = 1
            # on formate le retour en json
            for cat in liste_de_categories.items() :
                categories += [{"format": cat[0], "nombre":cat[1]}]
    return (categories)
        

def structure_generale (nom_dossier) :
    '''
        Fonction donnant la structure générale du json de base.
    '''
    data = {"dossier":nom_dossier, "categories" : []}
    return (data)

def main () :
    # sélection du dossier.
    os.chdir("./bat_wolf_Alex_3")
    data = structure_generale("test")
    print (data)
    print (data["categories"])

    data["categories"] = recherche_dossier ("./../test/dossierA")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if (__name__ == "__main__"):
    '''
        On force sur l'appel main() pour que ce soit déterministe.
        Possibilité de retirer cela pour appeler dans un autre ordre les fonctions.
    '''
    main()
