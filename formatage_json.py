# -*-coding:UTF8 ISO-8859-1 -*
import os
import xml.etree.cElementTree as xml
import json
import codecs
import re

def dossier_json (chemin_dossier) :
    '''
        fonction qui pour chaque dossier va chercher les différents formats de fichier,
        va renvoyer un json comportant ces informations avec le nom du dossier.
        Ceci fonctionne pour un dossier spécifique.
    '''
    for root, dirs, files in os.walk(chemin_dossier, topdown=False):
        categories = []
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

def fusion_json (chemin_dossier):
    '''
        fonction qui pour chaque dossier va chercher les différents formats de fichier,
        va rassembler tous les corps de json dans un répertoire donné.
    '''
    liste_de_corps_json = []
    for root, dirs, files in os.walk(chemin_dossier, topdown=False):
        categories = []
        if files != '' : # y a t-il des fichiers dans le dossier ?
            for name in files:
                file_extension = os.path.splitext(name)[1] # extension du nom
                if (file_extension.upper() == ".JSON"):
                    print (os.path.join(root, name))
                    with open(os.path.join(root, name), 'r', encoding='utf-8') as f:
                        liste_de_corps_json += [json.load(f)]
    return (liste_de_corps_json)
    
        
def decomposition_type (nom) :
    '''
        fonction servant à décomposer le nom en plusieurs parties.
        Elle vérifie si ces parties appartiennent à une liste de types pré-définis.
    '''
    types_pre_definis = ['bat', 'vampire', 'wolf']
    nom_decompose = nom.split("_")
    nom_type = []
    for word in nom_decompose :
        if word in types_pre_definis :
            nom_type.append(word)
    return (nom_type)
        
def decomposition_lieu (nom) :
    '''
        fonction servant à décomposer le nom en plusieurs parties.
        Elle vérifie si ces parties appartiennent à une liste de lieu pré-définis.
    '''
    types_pre_definis = ['CVM', 'Alex']
    nom_decompose = nom.split("_")
    nom_type = []
    for word in nom_decompose :
        if word in types_pre_definis :
            nom_type.append(word)
    return (nom_type)

def structure_generale (nom_dossier) :
    '''
        Fonction donnant la structure générale du json de base.
        Les types doivent être déterminés à partir de l'analyse du nom du dossier.
        On peut se baser sur une liste existante codée en dur dans un fichier pour vérifier la correspondace des types.
    '''
    data = {"chemin_du_dossier": str(os.getcwd()) + "\\" + nom_dossier, \
            "type" : decomposition_type(nom_dossier),\
            "lieu" : decomposition_lieu(nom_dossier),\
            "categories" : []}
    return (data)

def main () :
    for root, dirs, files in os.walk("."):
        for name in dirs:
            data = structure_generale(name)
            data["categories"] = dossier_json (os.path.join(root, name))
            with open(os.path.join(root, name,"data.json"), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    print (fusion_json("."))
            

if (__name__ == "__main__"):
    '''
        On force sur l'appel main() pour que ce soit déterministe.
        Possibilité de retirer cela pour appeler dans un autre ordre les fonctions.
    '''
    main()
