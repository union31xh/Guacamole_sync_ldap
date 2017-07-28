# -*- coding: latin-1 -*-

############################################
# MAJ Guacamole : Programme principal
############################################

########################
# Description g�n�rale #
###########################################################################
# Int�gre tous les comptes Ldap dans la base de donn�es guacamole
#  et associe � chaque comptes un groupe de connexions et les connexions
#  li�s � un utilisateur (ou groupe)
###########################################################################


from controleur.controleur_general import *


#######################
#  Param�tres globaux #
#######################

##################################
# --> Param�tres acc�s serveurs

# Les param�tres de connexions au serveurs se trouvent dans les fichiers .ini
#  sous le r�pertoire ./conf
# C'est le controleur qui charge automatiquement ces valeurs


##################################
# --> Param�tres profils

# Les profils sont d�finis dans le fichier Profils.ini
#  Ce fichier est automatiquement charg� par le controleur.



##########################
# Main
##########################


print ("###################")
print ("# D�but");
print ("###################")
print ("")

main = Controleur_General()
main.Maj_Bdd_Guacamole()

#main.Maj_Bdd_Guacamole_test()

print ("")
print ("###################")
print ("#Fin");
print ("###################")



