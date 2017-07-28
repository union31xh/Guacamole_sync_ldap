############################################################
# Tout ce qui est en relation avec la gestion des fichiers
############################################################

import pickle
import os
import json
from collections import namedtuple
from classe_gen.profil import *


class Util_fichiers:
    """classe utilitaire pour le chergement de fichiers de paramètres"""

    _slash = "/"
    chemin_conf = ""


    def __init__(self):
        """ Constructeur"""

        print("os.name : {}" .format(os.name))
        print("Répertoire de travail : {}" .format(os.getcwd()))

        # séparateur de fichier en fonction de l'OS
        if (os.name=="nt"):
            self._slash = "\\"
        # chemin fichier conf
        self.chemin_conf = os.getcwd() + self._slash + "conf"+self._slash
        

    def charger_parametres(self,nom_fichier):
        """ méthode générale de chargement de fichier de paramètres"""
        
        #print("chemin_conf : {}" .format(self.chemin_conf))    
        chemin_complet = self.chemin_conf + nom_fichier
        print ("PARAM --> ", chemin_complet)

        with open(chemin_complet) as fichier:
            texte_json_fichier = fichier.read()
            # --> texte json to DICT
            obj = json.loads(texte_json_fichier)
            return obj


    def charger_profils(self,nom_fichier):
        """ méthode générale de chargement de fichier d'une liste de paramètres"""
        """ Retourne une liste de profil"""
        chemin_complet = self.chemin_conf + nom_fichier
        print ("PARAM liste --> ", chemin_complet)

        liste_profil=[]
        
        with open(chemin_complet) as fichier:
            texte_json_fichier = fichier.read()
            # --> texte json to DICT
            objects_json = json.loads(texte_json_fichier)

            for obj in objects_json :

                un_profil_tmp = Profil()
                un_profil_tmp.Libelle_profil            = obj["Libelle_profil"]
                un_profil_tmp.Liste_id_connection       = obj["Liste_id_connection"]
                un_profil_tmp.Liste_id_group_connection = obj["Liste_id_group_connection"]
                un_profil_tmp.Interrogation_Ldap        = obj["Interrogation_Ldap"]
                un_profil_tmp.Base_recherche_ldap       = obj["Base_recherche_ldap"]

                liste_profil.append(un_profil_tmp)
                        
        return liste_profil




