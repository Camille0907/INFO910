# INFO910: TP Docker - Kubernetes

_TP réalisé individuellement : Camille MORAND_

L'objectif du TP est de réaliser une application, et de la faire tourner d'une part avec Docker, et d'autre part avec Kubernetes. 
Il n'y a pas de contrainte sur le langage; il faut que l'application aie besoin d'au moins deux conteneurs Docker pour tourner, dont au moins un faisant tourner une image que l'on construit avec un Dockerfile. Les conteneurs doivent être coordonnés par par un fichier docker-compose.

Dans le cadre de mon TP, j'ai réalisé une application Flask, utilisant Nginx en serveur web. L'application a pour but de renvoyer une image de chat pour chaque code HTTP possible. Pour cela elle fait des appels à l'API https://http.cat/ .

## Fonctionnement avec Docker

Dans le dossier Docker, l'application se divise en deux dossiers, pour les deux images à faire tourner.
Le dossier flask contient l'application en elle-même : 
- Le dossier app contient la plupart du code et des pages HTML
- run.py est le fichier appelé au lancement de l'application
- Le fichier app.ini paramètre l'application pour qu'elle communique sur une socket, avec uwsgi
- Le fichier requirement.txt regroupe les paquets python à installer pour que l'application fonctionne
- Le fichier .dockerignore est utilisé pour préciser qu'il ne faut pas copier certains éléments (en particulier ceux liés à l'IDE) dans l'image Docker
- Enfin, le fichier Dockerfile crée l'image de l'application : on part d'une image permettant d'exécuter python3, on crée un répertoire de travail dans lequel on ajoute le code de l'application, on installe les dépendances nécessaires et enfin on lance uwsgi, qui s'occupera de lancer l'application et de la faire communiquer.


Le dossier nginx gère le serveur Nginx : quasiment aucune modification n'est réalisée par rapport à l'image Nginx originale, il faut cependant modifier la configuration pour indiquer au server Nginx comment communiquer avec l'application Flask (fichier nginx.conf). Par conséquent, le Dockerfile sert uniquement à récupérer l'image nginx et à remplacer son nginx.conf par le nôtre.


Enfin, à la racine du dossier Docker, on trouve un fichier compose.yaml pour coordonner les deux images. Il permet de récupérer les images existantes, ou de les construire si elles n'existent pas, et de jouer sur les ports exposés à l'intérieur et à l'extérieur des services pour que les images communique entre elles, et soient accessible depuis l'extérieur.


### Pour lancer l'application : 
Il suffit de se placer à la racine du dossier Docker, et de taper `docker-compose up`. L'application est ensuite accessible à l'adresse http://127.0.0.1:80


## Fonctionnement avec Kubernetes

Le dossier K8s contient un service et un deployment pour chacune des deux images. Les deployments permettent de spécifier une image à récupérer pour le deployment, la stratégie de redémarrage, les ressources mémoire et processeurs allouées, les ports à exposer, les variables d'environnement auxquelles doit avoir accès le conteneur, ...
Les services permettent d'exposer les deployements ayant les mêmes labels qu'eux en tant que services : le service flask est exposé "en interne" pour être accessible par nginx, le service nginx est exposé de façon à être accessible à l'extérieur, en l'occurence sur le port 3000.


### Pour lancer l'application (avec Minikube): 
Il faut évidemment que Minikube soit lancé : commande `minkube start`.
Ensuite on se place à la racine du dossier K8s, et on applique les 4 fichiers : `kubectl apply -f flask-dep.yaml,flask-svc.yaml,nginx-dep.yaml,nginx-svc.yaml`
L'application est ensuite accessible sur le navigateur : dans le cadre de mes tests, l'adresse était toujours http://192.148.49.2:3000 
Si cela ne semble pas être la bonne adresse on peut la retrouver en tapant la commande `minikube service list`, et en cherchant l'URL liée à "nginx".
Le port 3000 est fixé par la ligne nodePort à la fin du fichier nginx-svc.yaml : il peut être modifié ici si le port 3000 est déjà occupé. 
