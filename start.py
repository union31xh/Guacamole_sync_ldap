# -*- coding: latin-1 -*-

############################################
# MAJ Guacamole : Programme principal
############################################

########################
# Description générale #
###########################################################################
# Intègre tous les comptes Ldap dans la base de données guacamole
#  et associe à chaque comptes un groupe de connexions et les connexions
#  liés à un utilisateur (ou groupe)
###########################################################################


from controleur.controleur_general import *


#######################
#  Paramètres globaux #
#######################

##################################
# --> Paramètres accès serveurs

# Les paramètres de connexions au serveurs se trouvent dans les fichiers .ini
#  sous le répertoire ./conf
# C'est le controleur qui charge automatiquement ces valeurs


##################################
# --> Paramètres profils

# Les profils sont définis dans le fichier Profils.ini
#  Ce fichier est automatiquement chargé par le controleur.



##########################
# Main
##########################


print ("###################")
print ("# Début");
print ("###################")
print ("")

main = Controleur_General()
main.Maj_Bdd_Guacamole()

#main.Maj_Bdd_Guacamole_test()

print ("")
print ("###################")
print ("#Fin");
print ("###################")



