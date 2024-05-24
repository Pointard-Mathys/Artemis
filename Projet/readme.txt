                                                        ARTEMIS

Ce dépôt contient une application Flask qui permet de créé des agent, des véhicules et des intervention dans le cadre de projet du cours de python avancer.




Fonctionnalités:

Gestion des Agents : De nouveaux agents peuvent être créés en requetant /new_agent. Les agents ont un statut de disponibilité (True pour disponible, False pour non disponible).

Gestion des Véhicules : Le système gère deux types de véhicules : VSAV (Véhicule de Secours et d'Assistance aux Victimes) et CCR (Camion Citerne Rural). c'est véhicules peuvent être créer une seul fois en requetant /vehicule.

Gestion des Interventions : De nouvelles interventions peuvent être créées en requetant /new_intervention. Le système sélectionne le véhicule approprié en fonction du type d'intervention (par exemple, "feu de maison" ou "malaise") et attribue les agents disponibles à l'intervention. Si le nombre requis d'agents n'est pas disponible, ou si aucun agent n'est disponible pour le véhicule sélectionné, un message d'erreur approprié est renvoyé.
(une fois les agent sur une intervention il devient indispo)



Configuration:

--> Installation des Dépendances : Installez les dépendances requises en exécutant pip install -r requirements.txt.

--> Exécution de l'Application :le serveur Flask s'exécute sur http://localhost:5000.




Points d'Accès:

/new_agent : Point d'accès GET pour créer un nouvel agent avec un statut de disponibilité aléatoire.
/vehicule : Point d'accès GET pour créer les véhicules VSAV et CCR.
/new_intervention : Point d'accès GET pour créer une nouvelle intervention, en attribuant les agents disponibles à l'intervention en fonction du type et du nombre requis d'agents pour le véhicule sélectionné.
Remarque : Cette application est un prototype de base et peut nécessiter des fonctionnalités supplémentaires, une gestion des erreurs et des améliorations de sécurité pour une utilisation en production.





