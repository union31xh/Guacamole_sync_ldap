################################
#  Classe definissant un profil
################################

class Profil:
    """Définition profil pour mise à jour Guacamole"""


    Libelle_profil = ""
    Liste_id_connection = []
    Liste_id_group_connection = []
    Interrogation_Ldap = ""
    Base_recherche_ldap = ""

    
    def __init__ (self,Libelle_profil="",Liste_id_connection=[],Liste_id_group_connection=[],Interrogation_Ldap="",Base_recherche_ldap=""):
        """ constructeur"""

        self.Libelle_profil = Libelle_profil
        self.Liste_id_connection = Liste_id_connection
        self.Liste_id_group_connection = Liste_id_group_connection
        self.Interrogation_Ldap=Interrogation_Ldap
        self.Base_recherche_ldap = Base_recherche_ldap

    def Ajouter_id_connection(self,id_connection):
        """ Ajoute une in_connection dans la liste interne"""
        self.Liste_id_connection.append(id_connection)


    def Ajouter_id_group_connection(self,id_group_connection):
        """ Ajoute une id Group connection """
        Self.Liste_id_group_connection.append(id_group_connection)

    
    def __str__(self):
        """ """

        texte = ""
        texte += "Libellé : {} \r\n".format(self.Libelle_profil)
        texte += "Liste_id_connectioné : {} \r\n".format(self.Liste_id_connection)
        texte += "Liste_id_group_connectioné : {} \r\n".format(self.Liste_id_group_connection)
        texte += "Interrogation_Ldap : {} \r\n".format(self.Interrogation_Ldap)
        texte += "BAse recherche ldap : {} \r\n".format(self.Base_recherche_ldap)
        
        return texte
        


    
