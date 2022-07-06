# led_matrix_control_high
Code source de l'applicatif des matrices led. HTTP/API, Python, sous Linux

# Explication

Tout d'abord, pour automatiser l'allumage des scripts au démarrage, il faut effectuer les commandes suivantes (en tant que root) :
```
crontab -e
ADD: @reboot sudo python3 /path/to/panel.py >> /var/log/panel-py.log 2>&1
ADD: @reboot sudo python3 /path/to/web/run.py >> /var/log/panel-web.log 2>&1
```

La partie web se présente ainsi :
- `run.py` est le code récupérant les POST venant de l'interface web
- `index.html` est l'interface graphique par laquelle 
- `set.html` est la page de retour, que ce soit avec une commande `curl`, mais aussi avec l'interface web.

Exemple de ligne de commande, sans passer par l'interface graphique, qui affiche 'LIBRE' en vert :
```
curl -X POST http://localhost/set -H 'Content-Type: application/x-www-form-urlencoded' -d 'couleur=#00ff00&texte=LIBRE&posX=0&posY=0
```

panel.py se décomposse de la manière suivante :
- Les imports, la définition de variables mais aussi de lecture de la configuration
- `Handler` : va observer le contenu du dossier "messages" et lorsqu'un fichier y est créé, va le déplacer dans lastmessage et en ensuite le traiter.
- `main; start` : on y ouvre le sous processus de [ce projet](https://github.com/ArrayIndexOutOfBound/led_matrix_control_low), on initialise le watchdog et si le fichier lastmessage existe (100% des cas en utilisation normal), on le traite
- `main; while True:` : On vérifie si on alterne entre deux texte, si oui on les affiche l'un puis l'autre, sinon on reste en état "figé". Cette routine tourne de manière infini et en parallèle avec le watchdog. C'est cette zone du programme qui communique avec [ce projet](https://github.com/ArrayIndexOutOfBound/led_matrix_control_low) après l'avoir ouvert plus tôt


# Installation
Il faut créer un dossier nommé "messages", vide, sinon le script plantera. Je n'arrive pas à upload un dossier vide.

Il existe deux manières de bien installer ce projet :
- soit mettre le contenu de ce projet dans le dossier `/opt/panel/`, tout est déjà prêt pour. 
- sinon, modifier les fichiers suivant car les chemins sont codé en dur :
```
- `config.txt`
- le début de `panel.py`
```

# Exemple de message transmis
- Depuis la création de "commande.txt" dans le dossier "messages" par run.py (partie web)
- Déplacement de ce fichier vers lastmessage, pour reprnedre si la Raspberry crash ou n'est plus alimenté.
- Copie envoyé par une pipe vers [ce projet](https://github.com/ArrayIndexOutOfBound/led_matrix_control_low) qui le traitera pour enfin afficher sur les panneaux de LEDs
```
C:0,255,0;B:0,0,0;X:0;Y:0;T:LIBRE
C:255,0,0;B:0,0,0;X:0;Y:0;T:OCCUPE
10
```
Ca affichera uniquement "LIBRE", en vert, puis "OCCUPE" en rouge. Les deux mots seront alternés toutes les 10 secondes.

# Dépendances

- pip, pour télécharger des modules Python additionnels : ```sudo apt install python3-pip```
- Module watchdog utilisé dans `panel.py` : ```python -m pip install -U watchdog```

# Améliorations possible
- Script d'installation
- Installation automatique de dépendance
- Chemins relatif à la place de chemins absolu

