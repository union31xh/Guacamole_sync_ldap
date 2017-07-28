# Guacamole_sync_ldap

**English :**

Python (V3) script to synchonize database of guacamole with an LDAP.

It's also possible to associate connections or groups of connections to users.

**Français :**

Script en python (V3) permettant de remplir la base de données guacamole à partir d'un annuaire LDAP.

Il permet également d'associer des connexions et groupes de connexions à un ensemble d'utilisateurs (représenté par une requête Ldap)

Avant de lancer le script il faut modifier les fichiers ini dans le répertoire /conf :
```
	-  ParamLDAP.ini 	--> pour la connexion au serveur LDAP	
	-  ParamMail.ini 	--> pour l'envoi de mail une fois les opérations de synchronisations finies
	-  ParamMySql.ini 	--> pour la connexion à la base de données de Guacamole_sync_ldap

	-  Profils.ini		--> permet de définir les ensembles ldap que l'on souhaite intégrer dans la base de données
```
	
Ci-dessous un exemple du fichier "Profils.ini" :

Exemple :
```
[
	{
		"Libelle_profil"   			: "Group with connections",
		"Liste_id_connection"   	: [6,7,8],
		"Liste_id_group_connection" : [3,4,5,6],
		"Interrogation_Ldap"     	: "(&(|(eduPersonPrimaryAffiliation=employee)(eduPersonPrimaryAffiliation=faculty))(mipSitePrincipal=UT1))",
		"Base_recherche_ldap"		: "OU=organisation_unit,DC=compagny,DC=fr"
	},
	{
		"Libelle_profil"   			: "All users without connections",
		"Liste_id_connection"   	: [],
		"Liste_id_group_connection" : [],
		"Interrogation_Ldap"     	: "(eduPersonPrimaryAffiliation=*)",
		"Base_recherche_ldap"		: "OU=organisation_unit,DC=compagny,DC=fr"
	}
	
]
```

Dans cet exemple, 2 profils de mise à jour sont définis :
* le premier, nommé "Group with connections" permet :
	* d'ajouter tous les utilisateurs contenu dans la requête ldap "(&(|(eduPersonPrimaryAffiliation=employee)(eduPersonPrimaryAffiliation=faculty))(mipSitePrincipal=UT1))",
	* d'y associer des connexions [6,7,8] et groupes de connexion [3,4,5,6].

* le deuxième exemple n'ajoute que les utilisateurs contenus dans "(eduPersonPrimaryAffiliation=*)" sans associer de connexions.
	
Pour connaitre les numéros des connexions et groupes de connexions il faut lancer le script "info_connection_guacamole.py".

Exemple d'un résultat obtenu :

```
###################
# Début
###################

os.name : nt
Répertoire de travail : D:\python\Guacamole V2 [git]
PARAM -->  D:\python\Guacamole V2 [git]\conf\ParamMySql.ini
PARAM -->  D:\python\Guacamole V2 [git]\conf\ParamLDAP.ini
PARAM -->  D:\python\Guacamole V2 [git]\conf\ParamMail.ini
PARAM liste -->  D:\python\Guacamole V2 [git]\conf\Profils.ini
Liste des 'connections' dans guacamole :
  id: 1 	 --> PC Jacques
  id: 2 	 --> PC Marcel
  id: 3 	 --> Serveur web
  id: 4 	 --> PCA Applications RH
  id: 5 	 --> SSH_guacamole
  id: 6 	 --> Poste témoin pour master
  id: 7 	 --> Proxy 1
  id: 8 	 --> Proxy 2
  id: 9 	 --> PC recette 1
Liste des GROUPES de 'connections' dans guacamole :
  id_group : 1 	 + Test xavier
  id_group : 2 	 + Serveur
  id_group : 7 	   + Proxy(s)
  id_group : 3 	 + Salles
  id_group : 4 	   + Réunion
  id_group : 5 	   + Accueil
  id_group : 6 	   + DSI

###################
#Fin
###################
```

Aini grace à cette liste il sera possible de construire ses profils et de remplir les champs suivants du fichier Profils.ini :
* "Liste_id_connection"  
* "Liste_id_group_connection"
		
		
		
Ce script fonctionne avec la version 0.9.12 incubating de guacamole.

		
		
