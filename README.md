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
- ``

Exemple de ligne de commande, sans passer par l'interface graphique, qui affiche 'LIBRE' en vert :
```
curl -X POST http://localhost/set -H 'Content-Type: application/x-www-form-urlencoded' -d 'couleur=#00ff00&texte=LIBRE&posX=0&posY=0
```

panel.py se décomposse de la manière suivante :
- ``
- ``
- ``
- ``

# Dépendances

! S'il y a un manque de dépandance !
