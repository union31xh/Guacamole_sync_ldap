#######################################################
# tout ce qui est en relation avec des recherches ldap
#######################################################


####################
# télécharger le module :
# pip install ldap3

import ldap3
import ssl
import time

from classe_gen.utilisateur import *
from classe_gen.liste_utilisateur import *


class Rech_Ldap:

    # dictionnaire contennant les paramètres
    ParamLDAP = {
        'host'   : '',
        'user'   : '',
        'passwd' : '',
        'use_ssl': True
    }


    """ constructeur"""
    def __init__ (self,ParamLDAP):
        self.ParamLDAP = ParamLDAP


    def Get_liste_utilisateurs(self,requete_ldap,base_recherche):


        attributs_retour = ['uid','givenName','sn','title']
        #attributs_retour = ldap3.ALL_ATTRIBUTES


        # Instance serveur
        serveur_ldap = ldap3.Server(self.ParamLDAP['host'],
                               use_ssl=self.ParamLDAP['use_ssl'],
                               get_info=ldap3.ALL)

        # Connexion au serveur
        conn = ldap3.Connection(serveur_ldap)

        # Authentification serveur
        res_connexion = conn.bind() # le bind peut être long ...

        #print ("etat connexion :",res_connexion)
        #print ("Connexion :\n", conn)

        if (res_connexion) :

            # Recherche ldap
            res_recherche = conn.search(base_recherche,requete_ldap,attributes=attributs_retour)


            liste_util = Liste_Utilisateurs()

            #print ("DEBUG : liste_util", len(liste_util.Liste_util))

            # Parcours du resultat
            cpt = 0
            cpt_info = 0
            temps_deb = time.time()
            for element in conn.entries :
                # Affiche tous les champs ldap retournés ...
                #print (" {} --> {}".format(i,element))

                #Creer un utilisateur avec cet uid
                compte_uid = element.uid
                un_utilisateur = Utilisateur(compte_uid)
                un_utilisateur.Prenom_Ldap = element.givenName
                un_utilisateur.Nom_Ldap = element.sn
                un_utilisateur.Title_Ldap = element.title
                            
                #Construire liste utilisateur
                liste_util.Ajouter(un_utilisateur)

                cpt+=1
                #print("DEBUG --> cpt : ",cpt)

                # affichage info traitement
                cpt_info += 1
                if (cpt_info>500):
                    cpt_info =0
                    duree = time.time() - temps_deb
                    #print ("                500 comptes récupérés ... ({} s)".format(duree))

                    temps_deb = time.time()

            #deconnexion
            conn.unbind()

        # retour resultat
        return liste_util





    
