################################
#  classe : Utilisateur_Ldap
################################


class Utilisateur:
    """ classe définissant un utilisateur """

    # Attribut de classe
    Compte_Ldap = ""
    Nom_Ldap = ""           # A titre info seulement
    Prenom_Ldap = ""        # A titre info seulement
    Title_Ldap  = ""        # A titre info seulement
    Guac_Id_User = -1
    Guac_connection_group_permission = ""  # A transformer ...
    Guac_connection_permission = ""   # A transformer ...

    """Constructeur"""
    def __init__(self,Compte_Ldap):
        self.Compte_Ldap = Compte_Ldap
         
