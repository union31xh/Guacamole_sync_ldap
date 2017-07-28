################################
#  classe : Liste_utilisateurs
################################



class Liste_Utilisateurs:


    # Attribut de classe   
    Liste_util = list()


    """ Contructeur """
    def __init__(self):
        self.Liste_util = list()


    """ Ajouter un objet de type utilisateur à la liste"""
    def Ajouter(self, Utilisateur) :
        
        # verifie si compte déjà existant
        continuer = True

        #for un_util in self.Liste_util :
        #    if un_util.Compte_Ldap == Utilisateur.Compte_Ldap :
        #        continuer = False
        #        print("déjà existant :",un_util.Compte_Ldap)


        # compte non trouvé --> insertion liste
        if continuer == True :
            self.Liste_util.append(Utilisateur)
            
        return continuer
       


    """ Affiche tous les objets stockés dans la liste """
    def Afficher_utilisateurs(self):
        print ("-> Contenu de la liste utilisateur :")
        i=0
        for element in self.Liste_util:
            print ("\t" ,
                   i,
                   "\t",
                   element.Compte_Ldap,
                   "\t\t(",
                   element.Nom_Ldap,
                   " ",
                   element.Prenom_Ldap,
                   " ",
                   element.Title_Ldap,
                   ")")
            i+=1
        
            
        
