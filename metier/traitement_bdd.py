#######################################################
# tout ce qui est en relation avec les bdd MYSQL
#######################################################



import MySQLdb
import sys

from classe_gen.utilisateur import *
from classe_gen.liste_utilisateur import *


class Traitement_bdd() :


    #dictionnaire contenant les paramètres
    ParamMysql = {
        'host'   : 'localhost',
        'user'   : 'root',
        'passwd' : '',
        'db'     : 'guacamole_db'
    }

    # Liste des connexions à associer
    Liste_id_connection = ()

    # Liste des groupes de connexions à associer
    Liste_id_groupe_connection = ()
    
    
    

    def __init__ (self, ParamMysql,Liste_id_connection=list(),Liste_id_groupe_connection=list()):
        """ Constructeur """
        self.ParamMysql = ParamMysql
        self.Liste_id_connection = Liste_id_connection
        self.Liste_id_groupe_connection = Liste_id_groupe_connection

    def Ajoute_Profil_Utilisateur_BDD_Guacamole(self,Liste_utilisateurs):
        """ Méthode principale d'ajout de profil d'utilisateur dans la bdd"""
        #print("--> Liste utilisateur :" ,Liste_utilisateurs)
        #print("--> Liste utilisateur (nb):" ,len(Liste_utilisateurs.Liste_util))


        try:
            ## création d'une connection
            conn = MySQLdb.connect(**self.ParamMysql)

            cpt = 0

            ## parcours de la liste des utilisateurs
            for un_util in Liste_utilisateurs.Liste_util :
                cpt +=1
                #print ("-->", un_util.Compte_Ldap)

                id_user = self._Verifier_compte_existant(conn,un_util.Compte_Ldap)
                # 1 : compte inexistant --> création
                if (id_user==-1):
                   #print ("    --> Création compte connexion", id_user)
                   id_user = self._Creer_compte(conn,un_util.Compte_Ldap)
                   self._Definir_droit_compte(conn,id_user)
                # 2 : création des droits sur les "connexions rdp"
                #print ("    --> AJOUTE association droit connexion", id_user)
                self._Creer_connexion_pour_utilisateur(conn,id_user)
                
                # 3 : création des droits sur les "groupes de connexions rdp"
                #print ("    --> AJOUTE association droit connexion groupe", id_user)
                self._Creer_groupe_connexion_pour_utilisateur(conn,id_user)
                #print(cpt)
     
        except MySQLdb.Error as e:
            # En cas d'anomalie
            print ("Error %d: %s" % (e.args[0],e.args[1]))
            sys.exit(1)

        finally:
            # On ferme la connexion
            if conn:
                conn.close()
        



    def Enleve_Profil_Utilisateur_BDD_Guacamole(self,Liste_utilisateurs):
        """ Méthode principale de retrait de profil d'utilisateur dans la bdd"""
        print("--> Liste utilisateur :" ,Liste_utilisateurs)
        print("--> Liste utilisateur (nb):" ,len(Liste_utilisateurs.Liste_util))


        try:
            ## création d'une connection
            conn = MySQLdb.connect(**self.ParamMysql)

            ## parcours de la liste des utilisateurs
            for un_util in Liste_utilisateurs.Liste_util :
                print ("-->", un_util.Compte_Ldap)
                id_user = self._Verifier_compte_existant(conn,un_util.Compte_Ldap)
                # 1 : compte inexistant --> création
                if (id_user==-1):
                   print ("    --> Création compte connexion", id_user)
                   id_user = self._Creer_compte(conn,un_util.Compte_Ldap) 
                # 2 : suppression des droits sur les "connexions rdp"
                print ("    --> ENLEVE association droit connexion", id_user)
                self._Enlever_connexion_pour_utilisateur(conn,id_user)
                
                # 3 : suppression des droits sur les "groupes de connexions rdp"
                print ("    --> ENLEVE association droit connexion groupe", id_user)
                self._Enlever_groupe_connexion_pour_utilisateur(conn,id_user)
     
        except MySQLdb.Error as e:
            # En cas d'anomalie
            print ("Error %d: %s" % (e.args[0],e.args[1]))
            sys.exit(1)

        finally:
            # On ferme la connexion
            if conn:
                conn.close()



    def Afficher_connexions(self):
        """ Affiche les id_connexions existantes de la BDD"""

        
        try:

            ## création d'une connexion
            ConnexionBDD = MySQLdb.connect(**self.ParamMysql)

            ## Liste des connections guacamole
            requete_sql = "select * from guacamole_connection"
            cur = ConnexionBDD.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(requete_sql)
            rows = cur.fetchall()
            print ("Liste des 'connections' dans guacamole :")
            for row in rows:
                # Récupère val champs
                connection_id = row['connection_id']
                connection_name = row['connection_name']

                print ("  id: {} \t --> {}".format(connection_id,connection_name))

            ## liste des groupes de connections
            requete_sql = "select * from guacamole_connection_group"
            cur = ConnexionBDD.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(requete_sql)
            rows = cur.fetchall()
            print ("Liste des GROUPES de 'connections' dans guacamole :")

            liste_noeuds = list()

            ## Récupération des valeurs et stockage dans liste
            for row in rows:
                # Récupère val champs
                connection_group_id = row['connection_group_id']
                parent_id           = row['parent_id']
                connection_group_name = row['connection_group_name']

                un_noeud = (connection_group_id,parent_id,connection_group_name)
                liste_noeuds.append(un_noeud)

                #print ("  id: {} \t --> {}".format(connection_group_id,connection_group_name))            

            ## Affiche liste sous forme d'arbre

            self._afficher_arbre(liste_noeuds,None,0)



        except MySQLdb.Error as e:
            # En cas d'anomalie
            print ("Error %d: %s" % (e.args[0],e.args[1]))
            sys.exit(1)

        finally:
            # On ferme la connexion
            if ConnexionBDD:
                ConnexionBDD.close()


    # Fonction recursive utilisé par Afficher_connexions
    def _afficher_arbre(self, liste_noeuds,id_parent_select, niveau):
        """ Affiche arbre de noeuds"""

        for un_noeud in liste_noeuds :
            id_group    = un_noeud[0]
            id_parent   = un_noeud[1]
            text_group  = un_noeud[2]
            if (id_parent == id_parent_select) :
                #print("{} \t {}--> {}".format(id_group,id_parent,text_group))

                texte_blanc = ""
                i=0
                while i<niveau :
                    texte_blanc += "  "
                    i+=1
                
                print("  id_group : {} \t {}+ {}".format(id_group,texte_blanc,text_group))

                self._afficher_arbre(liste_noeuds,id_group, niveau+1)

        
        
    def _Verifier_compte_existant(self,ConnexionBDD,Id_compte):
        """Vérifier si un compte est dans la base de données """

        resultat = -1
        requete_sql = "select * from guacamole_user where username= '{}'".format(Id_compte)
    
        # On créé un curseur MySQL
        cur = ConnexionBDD.cursor(MySQLdb.cursors.DictCursor)
        # On exécute la requête SQL
        cur.execute(requete_sql)
        # On récupère toutes les lignes du résultat de la requête
        rows = cur.fetchall()

        #print(requete_sql)

        # On parcourt toutes les lignes
        for row in rows:
            # Pour récupérer les différentes valeurs des différents champs
            user_id = row['user_id']
            user_name = row['username']

            if (user_name==Id_compte):
                resultat=user_id

        return resultat


    """ Créer un compte dans la table user et renvoie le ID_user"""
    def _Creer_compte(self,ConnexionBDD,Nom_compte):

        resultat = -1
        # On créé un curseur MySQL
        cur = ConnexionBDD.cursor(MySQLdb.cursors.DictCursor)

        ## Insertion du compte
        mdp = "cc2eed5549865ab7f7f069f54a77121069743cf79a9c2e57442791d136f8002d"
        sel = "9f673804316b21f9d8e2de283782bfb59a96a6df67f6eeb14011f9cf7f772bdc"
        date_mdp = "2017-04-24 15:11:19"
        requete_sql =" insert into guacamole_user set username = '{}', password_hash = UNHEX('{}'), password_salt = UNHEX('{}') , password_date = '{}'".format(Nom_compte,mdp,sel,date_mdp)
        self._Execute_sql_insert_delete_update(ConnexionBDD, requete_sql) 

        ## Cherche id de ce nouveau compte
        requete_sql = "select * from guacamole_user where username= '{}'".format(Nom_compte)
        cur = ConnexionBDD.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(requete_sql)
        rows = cur.fetchall()        
        for row in rows:
            # Récupère id_user du nouveau compte créé
            resultat = row['user_id']

        return resultat


    def _Definir_droit_compte(self,ConnexionBDD, id_utilisateur) :
        ## Definition des droits du nouvel utilisateur

        requete_sql ="insert into guacamole_user_permission set user_id = '{}', affected_user_id='{}', permission = '{}'";

        # indique que l'admin a ajouté l'utilisateur
        requete_sql_read        = requete_sql.format("1",id_utilisateur,"READ")
        requete_sql_update      = requete_sql.format("1",id_utilisateur,"UPDATE")
        requete_sql_administer  = requete_sql.format("1",id_utilisateur,"ADMINISTER")
        requete_sql_delete      = requete_sql.format("1",id_utilisateur,"DELETE")

        # positionne juste les droits de READ à l'utilisateur
        requete_sql_read2        = requete_sql.format(id_utilisateur,id_utilisateur,"READ")

        ## execute les requetes sql
        self._Execute_sql_insert_delete_update(ConnexionBDD,requete_sql_read)
        self._Execute_sql_insert_delete_update(ConnexionBDD,requete_sql_update)
        self._Execute_sql_insert_delete_update(ConnexionBDD,requete_sql_administer)
        self._Execute_sql_insert_delete_update(ConnexionBDD,requete_sql_delete)

        self._Execute_sql_insert_delete_update(ConnexionBDD,requete_sql_read2)



    def _Creer_connexion_pour_utilisateur(self,ConnexionBDD,ID_compte):
        """ Associer les connexions à un utilisateur"""

        for id_connection in self.Liste_id_connection :
            requete_sql = "insert into guacamole_connection_permission set user_id = {}, connection_id= {}, permission='READ' ".format(ID_compte,id_connection)
            self._Execute_sql_insert_delete_update(ConnexionBDD, requete_sql) 


    def _Creer_groupe_connexion_pour_utilisateur(self,ConnexionBDD,ID_compte):
        """ Associer les Groupes de connexions à un utilisateur"""

        for id_groupe_connection in self.Liste_id_groupe_connection :
            requete_sql = "insert into guacamole_connection_group_permission set user_id = {}, connection_group_id= {}, permission='READ' ".format(ID_compte,id_groupe_connection)
            self._Execute_sql_insert_delete_update(ConnexionBDD, requete_sql) 


    def _Enlever_connexion_pour_utilisateur(self,ConnexionBDD,ID_compte):
        """ Enlève association connexion pour un utilisateur"""

        for id_connection in self.Liste_id_connection :
            requete_sql = "delete from guacamole_connection_permission where user_id = {} and  connection_id= {} ".format(ID_compte,id_connection)
            self._Execute_sql_insert_delete_update(ConnexionBDD, requete_sql) 


    def _Enlever_groupe_connexion_pour_utilisateur(self,ConnexionBDD,ID_compte):
        """ Associer les Groupes de connexions à un utilisateur"""

        for id_groupe_connection in self.Liste_id_groupe_connection :
            requete_sql = "delete from guacamole_connection_group_permission where user_id = {} and  connection_group_id= {} ".format(ID_compte,id_groupe_connection)
            self._Execute_sql_insert_delete_update(ConnexionBDD, requete_sql)



    def _Execute_sql_insert_delete_update(self,ConnexionBDD,requete_sql):
        """ Executer requete sql """

        # execution de la requête
        cur = ConnexionBDD.cursor(MySQLdb.cursors.DictCursor)
        try:
            # On exécute la requête SQL
            cur.execute(requete_sql)
            # On committe
            ConnexionBDD.commit()
        except MySQLdb.Error as e:

            continuer = True

            # ignore l'affichage de l'erreur de type "duplicate key"
            if (e.args[0]==1062):
                continuer=False

            # Affichage de l'erreur
            if (continuer):
                print ("    Error %d: %s" % (e.args[0],e.args[1]))
                print ("    requete sql : ", requete_sql)
            # en cas d'erreur : collback
            ConnexionBDD.rollback()  
        






    
