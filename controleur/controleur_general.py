#########################################
#  Controleur général
#########################################

from classe_gen.utilisateur import *
from classe_gen.liste_utilisateur import *
from classe_gen.profil import *
from metier.traitement_bdd import *
from metier.rech_ldap import *
from metier.mail import *
from metier.fichiers import *

class Controleur_General:
    """ class générale qui va piloter toutes les actions"""

    #Paramètres MYSQL (Structure)
    ParamMysql = {
        'host'   : 'localhost',
        'user'   : 'root',
        'passwd' : '',
        'db'     : 'guacamole_db'
    }

    # Paramètres LDAP (structure)
    ParamLDAP = {
        'host'   : '',
        'user'   : '',
        'passwd' : '',
        'use_ssl' : True
    }

    # param mail (structure)
    ParamMail = {
        'serveur'   : '',
        'emmetteur' : '',
        'destinataire' : ''
    }

    # Va contenir tous les profils à mettre à jour dans Guacamole
    Liste_profil =[]
    

    


    def __init__(self):
        """Constructeur"""

        # charge les paramètres globaux
        util_fichiers = Util_fichiers()
        self.ParamMysql = util_fichiers.charger_parametres ("ParamMySql.ini")
        self.ParamLDAP  = util_fichiers.charger_parametres ("ParamLDAP.ini")
        self.ParamMail  = util_fichiers.charger_parametres ("ParamMail.ini")

        self.Liste_profil = util_fichiers.charger_profils("Profils.ini")

        
                

    def Maj_Bdd_Guacamole(self):
        """met à jour la base de données guacamole"""

        ParamLDAP = self.ParamLDAP
        ParamMysql = self.ParamMysql
        ParamMail = self.ParamMail
        
        
        Une_recherche_ldap = Rech_Ldap(ParamLDAP)

        nb_utilisateurs = 0
        cpt_profil = 0

        texte_parcours_mail = ""
        
        for elt_profil in self.Liste_profil:

            cpt_profil += 1

            print ("Traitement du profil n°",cpt_profil)
            print ("  Requete Ldap : ", elt_profil.Interrogation_Ldap )
            ## Récupération des comptes utilisateurs
            print ("    --> Recherche comptes LDAP en cours ...")
            
            liste_utilisateurs = Une_recherche_ldap.Get_liste_utilisateurs(elt_profil.Interrogation_Ldap, elt_profil.Base_recherche_ldap)

            ## nb utilisateurs
            nb_utilisateurs = len(liste_utilisateurs.Liste_util)

            ## prepare texte mail
            texte_parcours_mail += " - Profil n°{} : {} compte(s)  --> {} \r\n".format(cpt_profil,nb_utilisateurs,elt_profil.Libelle_profil)

            ## MAJ dans base de données
            print ("    --> MAJ BDD en cours pour {} utilisateurs".format (nb_utilisateurs))
            traitement_guacamole = Traitement_bdd(ParamMysql,elt_profil.Liste_id_connection,elt_profil.Liste_id_group_connection)
            traitement_guacamole.Ajoute_Profil_Utilisateur_BDD_Guacamole(liste_utilisateurs)

            #traitement_guacamole.Enleve_Profil_Utilisateur_BDD_Guacamole(liste_utilisateurs)


        ## mail
        un_mail = Envoi_mail(ParamMail)
        texte_mail  = "Ce mail pour indiquer que la mise à jour de la base de données guacamole a été lancée\r\n"
        texte_mail  += "\r\n"
        texte_mail  += "Cela concerne : "
        texte_mail  += "\r\n"
        texte_mail  += texte_parcours_mail
        texte_mail  += "\r\n"
        texte_mail  += "Merci de ne pas répondre\r\n"
        texte_mail  += "DSI-Support \r\n"

        sujet       = "Synchronisation utilisateurs LDAP / Groupe de connexion RDP PU-PEDA"
        mail_a      = ParamMail["destinataire"]

        un_mail.Envoyer_mail(sujet,texte_mail,mail_a)


    def Afficher_connection_guacamole(self):
        """Affiche la liste des connexions créées dans guacamole"""

        traitement_guacamole = Traitement_bdd(self.ParamMysql)
        traitement_guacamole.Afficher_connexions()
        
        
    # pour tests ...
    def Maj_Bdd_Guacamole_test(self):
        """met à jour la base de données guacamole avec des utilisateurs fictifs"""

        ParamLDAP = self.ParamLDAP
        ParamMysql = self.ParamMysql
        ParamMail = self.ParamMail
        


        liste_utilisateurs = Liste_Utilisateurs()

        i = 0

        print ("Remplit tableau utilisateur tests :")
        while i<60000 :
            i+=1
            compte_uid = "Util{}".format(i)
            un_utilisateur = Utilisateur(compte_uid)
            un_utilisateur.Prenom_Ldap = ""
            un_utilisateur.Nom_Ldap = ""
            un_utilisateur.Title_Ldap = ""
            liste_utilisateurs.Ajouter(un_utilisateur)

        print ("Remplit base de données :")
        traitement_guacamole = Traitement_bdd(ParamMysql,[],[])
        traitement_guacamole.Ajoute_Profil_Utilisateur_BDD_Guacamole(liste_utilisateurs)

        
        
    
