# coding: utf-8
# the interface chosen for the script
# "T" = TERMINAL
# "J" = JSON file
# "JM" = JSON JMeterFarm
__INTERFACE__ = "JM"

import sys
import os
import datetime
import platform
from string import Template
import xml.dom.minidom as minidom
import re
import argparse
import logging
import json

overwrite_security = True # DO NOT OVERWRITE IT IF YOU WANT TO PREVENT DATA LOSS
SI = "JMeter"
LTN_prefix = datetime.date.today().isoformat() +"_"+ str(datetime.datetime.today().hour) +"-"+ str(datetime.datetime.today().minute)
LTN_corpse = "Load_test"
LTN = LTN_prefix + "_" + LTN_corpse
VU = "${__threadNum}"
LSN = "${__threadGroupName}"
LGL = platform.node()

header_values_to_add = Template("SI=$SI;LTN=$LTN;VU=$VU;LSN=$LSN;TSN=$TSN;LGL=$LGL;RG=;")

def populate_header_global_variables():
    global SI, LTN_prefix, LTN_corpse, LTN, VU, LSN, LGL
    SI = "JMeter"
    LTN_prefix = datetime.date.today().isoformat() +"_"+ str(datetime.datetime.today().hour) +"-"+ str(datetime.datetime.today().minute)
    LTN_corpse = "Load_test"
    LTN = LTN_prefix + "_" + LTN_corpse
    VU = "${__threadNum}"
    LSN = "${__threadGroupName}"
    LGL = platform.node()

def clean_file(string_f_source):
    #Thanks to Clemens Hermann for this workaround initially proposed in 2007 for the library BeautifulSoup
    #pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE) #create a pattern
    #string_f_source = re.sub(pat, '', string_f_source)       # remove leading and trailing whitespaces
    #string_f_source = re.sub('\n', '', string_f_source)# convert newlines to nothing
    string_f_source = re.sub('[\s]+<', '<', string_f_source) # remove whitespaces before opening tags
    string_f_source = re.sub('>[\s]+', '>', string_f_source) # remove whitespaces after closing tags
    return string_f_source


def extract_json_values(file_path):
    global overwrite_security, SI, LTN, LGL
    try:
        #on ouvre le fichier
        with open(file_path, "r", encoding="utf-8") as f_json:
            json_object = json.load(f_json)
            #Si un élément qui est extrait n'existe pas dasn le fichier json, on lève une exception 'KeyError'
            try:
                integration_object = json_object["integration_object"]
                #Si L'INTERFACE est "J", on regarde pour extraire des variables supplémentaire du json
                #sinon on passe
                # Si les types de variables du JSON sont celles espérées,
                #alors on extrait des variables supplémentaires du fichier JSON
                # sion, on lève une exepction
                if __INTERFACE__ == "J":
                    if isinstance(integration_object["overwrite_security"],bool) and\
                    isinstance(integration_object["source_file_path"],str) and isinstance(integration_object["target_file_path"],str):
                        overwrite_security = integration_object["overwrite_security"]
                        source_file_path = integration_object["source_file_path"]
                        target_file_path = integration_object["target_file_path"]
                    else:
                        raise TypeError()
                #Si les types de variables du JSON sont celles espérées, on continue
                #sinon, on lève une exception et le 'except' la catch pour afficher un message dans le terminal
                if isinstance(integration_object["variables"]["SI"],str) and isinstance(integration_object["variables"]["LTN"],str) \
                and isinstance(integration_object["variables"]["LGL"],str):
                    SI = integration_object["variables"]["SI"]
                    LTN = integration_object["variables"]["LTN"]
                    LGL = integration_object["variables"]["LGL"]
                else:
                    raise TypeError()

            except KeyError as e:
                logging.error("Wrong format of the json file. Please be sure to follow the best practice for the json file creation and try again.")
                exit(1)
            except TypeError as e:
                logging.error("JSON variables type mismatch the required ones. Please be sure to follow the best practice for the json file creation and try again.")
                exit(1)
    except FileNotFoundError as e:
        logging.error("JSON file or directory does not exist. Please check the given path.")
        exit(1)
    except json.decoder.JSONDecodeError as e:
        logging.error("JSON file seems to NOT be a JSON file. Please check the given path.")
        exit(1)
    if __INTERFACE__ == "J":
        return source_file_path,target_file_path

def extract_source_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f_source_jmx:
            liste_lignes_f_source = f_source_jmx.readlines()
            string_f_source = clean_file("".join(liste_lignes_f_source))
            f_source_jmx.close()
            return string_f_source
    except FileNotFoundError as e:
        logging.error("Source file or directory does not exist. Please check the given path.")
        exit(1)


def validate_target_file_path(target_file_path):
    tfp = "./target.jmx"
    continuer = False
    #si le target_file_path est renseigné
    if target_file_path != None:
        dir_path, file_name = os.path.split(target_file_path)
        #si le dossier cible existe
        if os.path.isdir(os.path.dirname(target_file_path)):
            #si aucun fichier n'est renseigné, on renseigne celui par défaut
            if file_name == "":
                target_file_path = os.path.join(dir_path,"target.jmx")
                logging.warning("The target file path given does not contain any file name. The file name was set to 'target.jmx'. Press Ctrl+C to abort.")
            #affectation du path donné en paramètre au pth par défaut
            tfp = target_file_path
        else:
            logging.error("Target directory does not exist. Please check the given path.")
            exit(1)
    else:
        logging.info("No target file path given. The target default path is ./target.jmx")
    #verification de l'existence du fichier cible
    if os.path.exists(tfp) and overwrite_security:
        logging.warning("The target file given already exists. If you continue, it will be overwritten. \nDo you want to continue ? [y/n]")
        continuer = True if input() == "y" else False
        if continuer:
            logging.info("Your current target file will be OVERWRITTEN. Press Ctrl+C to abort.")
        else:
            logging.info("Please verify your target file path. Then try again")
            exit(0)
    return tfp

def menu():
    global SI, LTN_prefix, LTN_corpse, LTN, LGL
    print("SI (Solution Information) [JMeter] : ")
    iSI = input()
    SI = iSI if iSI != "" else SI
    print("LTN (Load Test Name) PREFIX ["+LTN_prefix+"] : ")
    iLTN_prefix = input()
    LTN_prefix = iLTN_prefix if iLTN_prefix != "" else LTN_prefix
    print("LTN (Load Test Name) CORPSE ["+LTN_corpse+"] : ")
    iLTN_corpse = input()
    LTN_corpse = iLTN_corpse if iLTN_corpse != "" else LTN_corpse
    LTN = LTN_prefix +"_"+ LTN_corpse
    print("The LTN variable is set to : "+ LTN)
    print("LGL (Load Generator Location) ["+LGL+"] : ")
    iLGL = input()
    LGL = iLGL if iLGL != "" else LGL

def validate_input():
    global SI, LTN, LGL, header_values_to_add
    print("Do you confirm those inputs ? [y/n]")
    print("SI= "+SI)
    print("LTN= "+LTN)
    print("LGL= "+LGL)
    confirmed = input()
    if confirmed == "y":
        #on applique les modification header à ajouter et on renvoie vrai
        header_values_to_add = Template(header_values_to_add.safe_substitute(SI=SI,LTN=LTN,VU=VU,LSN=LSN,LGL=LGL))
        return True
    populate_header_global_variables()
    return False

def create_header_element(dom_f_source, local_header_values_to_add):
    global header_values_to_add
    #1 Creation du conteneur "header"
    header_element = dom_f_source.createElement("elementProp")
    header_element.setAttribute("name", "apm-integration-jmeterfarm")
    header_element.setAttribute("elementType", "Header")

    #2 Creation du conteneur "nom du header"
    header_name_element = dom_f_source.createElement("stringProp")
    header_name_element.setAttribute("name", "Header.name")
    #insertion de la valeur de l'element (ici, on insère la valeur que prendra le nom du header )
    header_name_element.appendChild(dom_f_source.createTextNode("apm-integration-jmeterfarm"))

    #3 Creation du conteneur "valeur du header"
    header_value_element = dom_f_source.createElement("stringProp")
    header_value_element.setAttribute("name", "Header.value")
    #insertion de la valeur de l'element (ici, on insère la valeur que prendra la valeur du header )
    header_value_element.appendChild(dom_f_source.createTextNode(local_header_values_to_add))

    #4 On ajoute les deux "stringProp" a l'élément "header" (elementProp)
    header_element.appendChild(header_name_element)
    header_element.appendChild(header_value_element)

    return header_element

def create_headerManager_element(dom_f_source, local_header_values_to_add):
    #1 Creation du conteneur "HeaderManager"
    headerManager_element = dom_f_source.createElement("HeaderManager")
    headerManager_element.setAttribute("guiclass", "HeaderPanel")
    headerManager_element.setAttribute("testclass", "HeaderManager")
    headerManager_element.setAttribute("testname", "HTTP Header Manager")
    headerManager_element.setAttribute("enabled", "true")
    #2 Creation du conteneur "collectionProp" qui va contenir tous les headers du HeaderManager
    collectionProp_element = dom_f_source.createElement("collectionProp")
    collectionProp_element.setAttribute("name", "HeaderManager.headers")
    #3 Creation du conteneur "hashTree"
    hashTree_element = dom_f_source.createElement("hashTree")
    #4 Creation et ajout du header dans le collectionProp
    collectionProp_element.appendChild(create_header_element(dom_f_source,local_header_values_to_add))
    #5 Ajout du collectionProp dans le headerManager
    headerManager_element.appendChild(collectionProp_element)

    return headerManager_element


#---------------------------INTEGRATION WITH DYNATRACE------------------------

def integrate_with_dynatrace(string_f_source, target_file_path):
    global header_values_to_add
    #on parse le "fichier" source en xml dom pour faire des recherches plus simplement
    dom_f_source = minidom.parseString(string_f_source)

    # pour tous les éléments "TransactionController" du dom
    for tc in dom_f_source.getElementsByTagName("TransactionController"):
        #on récupère le nom de la transaction
        transaction_name = tc.getAttribute("testname")

        #on transforme le template de la valeur de header à ajouté ("SI=$SI;LTN=$LTN;VU=$VU;LSN=$LSN;TSN=$TSN;LGL=$LGL;RG=;") en string avec les valeurs correctes
        #on n'en remplace qu'un car les autres l'ont déjà été dans la fonction validate input
        local_header_values_to_add = header_values_to_add.safe_substitute(TSN=transaction_name)


        #on va au niveau du node qui contient tous les éléments de la transaction (c'est un hashTree)
        tc_children_container = tc.nextSibling
        #nombre de headerManager directement enfants d'un TransactionController
        nb_headerManager = 0
        #le headerManager (directement enfant d'un TransactionController) à modifié s'il existe
        headerManager_to_modify = None
        # pour tous les headerManager que l'on a trouvé pour un TransactionController
        for hm in tc_children_container.getElementsByTagName("HeaderManager"):
            #on verifie que son père direct est bien le TransactionController
            #(on s'assure ici que l'on ne compte que les HeaderManagers qui sont les fils direct du TransactionController)
            #ET on sauvegarde le headerManager à modifier pour l'utiliser dasn les else de la condition suivante
            if hm.parentNode.previousSibling.localName == "TransactionController":
                headerManager_to_modify = hm
                nb_headerManager+=1
        # S'il n'y a pas de HeaderManager dans le TransactionController courant : On cré un HeaderManager
        # OU s'il y en plus d'un seul : On lève une exception
        # sinon : on ajoute un header dans le HeaderManager existant
        if nb_headerManager == 0:
            #Si le TransactionController contient des requêtes, alors on ajoute le header_element
            # sinon on n'ajoute pas car cela ne sert à rien
            if len(tc.nextSibling.getElementsByTagName("HTTPSamplerProxy")) != 0:
                #Creation du 'xml element node' headerManager
                headerManager_element = create_headerManager_element(dom_f_source, local_header_values_to_add)
                #on ajoute un HeaderManager
                tc.nextSibling.appendChild(headerManager_element)
        elif nb_headerManager > 1:
            #on lève une exception
            logging.error("Many HeaderManagers found at least in one TransactionController. Please be sure to only have one HeaderManager by TransactionController. Then retry.")
            exit(1)
        else:
            try:
                #Pour tous les headers contenu dans le headerManager
                headers_to_delete = []
                for header in headerManager_to_modify.getElementsByTagName("collectionProp")[0].getElementsByTagName("elementProp"):
                    #EN GROS : Si un header avec le même nom existe déjà, alors on l'ajoute à la suppression avant d'ajouter le nouveau
                    #(en gros on overwrite le header)
                    #Pour tous les enfants du header (tous ceux appelé stringProp, c'est à dire tous les éléments actuellement)
                    #(c'est à dire son nom et sa valeur)
                    for child in header.childNodes:
                        #Si l'enfant courant possède le nom du header
                        if child.getAttributeNode("name").value == "Header.name":
                            #Si le nom de ce header vaut 'apm-integration-jmeterfarm'
                            if child.firstChild.data == "apm-integration-jmeterfarm":
                                #on ajoute ce header à la liste des headers à supprimer
                                headers_to_delete.append(header)
                #on supprime tous les headers contenu dans headers_to_delete
                #(normalement il n'y en a qu'un seul, si on n'en a pas rajouté ensuite à la main avec le même nom)
                for header in headers_to_delete:
                    headerManager_to_modify.getElementsByTagName("collectionProp")[0].removeChild(header)
                #Creation du 'xml element node' header
                header_element = create_header_element(dom_f_source, local_header_values_to_add)
                #on ajoute un header dans le HeaderManager existant dans l'élément collectionProp.
                #(Il n'y en a forcément qu'un seul dans cette version de JMeter, donc on peut mettre [0] en dur)
                headerManager_to_modify.getElementsByTagName("collectionProp")[0].appendChild(header_element)
            except AttributeError as e:
                logging.critical("A variable may be null. This error is not intended to happen.\nPlease retry. If this error persists, please contact the developers and give them this stack trace :\n",exc_info=True)
                exit(1)


    #on exporte le dom en xml lisible
    #l'encodage/décodage est ici pour mettre explicitement l'encodage utf-8 dans l'en-tête xml
    # Cela permet d'éviter des erreurs sous Microdoft Windows
    file_content_string = dom_f_source.toprettyxml(encoding="utf-8").decode("utf-8")
    #file_content_string = dom_f_source.toprettyxml()
    #print(file_content_string)
    #On écrit ce xml dans un fichier cible
    f_target_jmx = open(target_file_path,"w", encoding="utf-8")
    f_target_jmx.write(file_content_string)
    f_target_jmx.close()


#-----------------------------MAIN--------------------------

def main():
    logging.basicConfig(format='%(levelname)s - %(message)s',level=logging.INFO)
    #Mise en place des arguments de lancement
    parser = argparse.ArgumentParser()
    if __INTERFACE__ == "T":
        parser.add_argument("source", help="the path of the jmx source file to integrate")
        parser.add_argument("-t","--target", help="the path of the jmx target file. \n By default, the jmx target file is named target.jmx and it is stored in the root folder of the launched script.\n Ex: ./folder1/file.jmx")
    elif __INTERFACE__ == "J":
        parser.add_argument("jsonFile", help="the json file path containing the necessary information for the integration")
    elif __INTERFACE__ == "JM":
        # pour la jmeterfarm, on désactive la sécurité pour éviter les bloquages
        global overwrite_security
        overwrite_security = False
        parser.add_argument("source", help="the path of the jmx source file to integrate")
        parser.add_argument("-t","--target", help="the path of the jmx target file. \n By default, the jmx target file is named target.jmx and it is stored in the root folder of the launched script.\n Ex: ./folder1/file.jmx")
        parser.add_argument("jsonFile", help="the json file path containing the necessary information for the integration")
    else:
        logging.error("Wrong __INTERFACE__ value. Please verify it inside the script.")

    #récupération des arguments de lancement
    args = parser.parse_args()

    #récupération des chemins des fichiers source et cible
    if __INTERFACE__ == "T" or __INTERFACE__ == "JM":
        source_file_path = args.source
        target_file_path = args.target
        extract_json_values(args.jsonFile)
    elif __INTERFACE__ == "J":
        source_file_path, target_file_path = extract_json_values(args.jsonFile)

    #extraction du fichier source
    string_f_source = extract_source_file(source_file_path)

    #validation du fichier cible
    target_file_path = validate_target_file_path(target_file_path)

    print("-------JMeter-Dynatrace Integration Script-------")
    print("Created by Julien Revaud for Leanovia Consulting")
    #si l'interface est le terminal, on affiche le menu et on réalise les actions nécessaires
    #sinon, on modifie directement le header à ajouter aux requêtes avec les variables globales (déjà modifié avec les valeurs du JSON)
    if __INTERFACE__ == "T":
        print("You will have to choose the values of the different variables sent to Dynatrace")
        continuer = False
        while not continuer:
            menu()
            continuer = validate_input()
    elif __INTERFACE__ == "J" or __INTERFACE__ == "JM":
        global header_values_to_add
        header_values_to_add = Template(header_values_to_add.safe_substitute(SI=SI,LTN=LTN,VU=VU,LSN=LSN,LGL=LGL))
    print("Creation of the Dynatrace integrated file...")
    integrate_with_dynatrace(string_f_source, target_file_path)
    print("Creation sucessful.")

if __name__ == '__main__':
    main()
