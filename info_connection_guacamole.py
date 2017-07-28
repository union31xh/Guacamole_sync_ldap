# -*- coding: latin-1 -*-

############################################
# Info Guacamole : Programme principal
############################################

########################
# Description générale #
###########################################################################
# Permet de lister les connexion et groupe de 'connections'
#  aide pour construire un profil particulier
###########################################################################


from controleur.controleur_general import *

# param connexion serveur mysql
ParamMysql = {
    'host'   : 'localhost',
    'user'   : 'root',
    'passwd' : '',
    'db'     : 'guacamole_db'
}

print ("###################")
print ("# Début");
print ("###################")
print ("")

main = Controleur_General()
main.Afficher_connection_guacamole()

print ("")
print ("###################")
print ("#Fin");
print ("###################")
