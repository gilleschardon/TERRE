# TERRE
Ton Écran Ratp (Rer, Etc.)

Nécessite flask et zeep et, (surtout !) l'accès à l'[API temps réel RATP](https://data.ratp.fr/explore/dataset/horaires-temps-reel/information/).


[Exemple](https://gilleschardon.fr/TERRE.html)

Pour tester (en local) :

* ajouter le fichier `wsiv.wsdl` (fourni par la RATP) dans le répertoire instance
* puis dans le répertoire racine :

```bash
export FLASK_APP=TERRE/TERRE_flask.py
export FLASK_ENV=development
flask run
```

Le fichier de configuration `TERRE.conf` se structure commme
```
ligne	station	direction	nbmax	T
```
séparés par des tabs où `nbmax` est le nombre maximal de trains/tram/bus à afficher (0 si infini) et `T` le temps nécessaire pour arriver à la gare/station.

Pour le RER, on peut faire suivre par des stations pour lesquelles l'arrêt sera indiqué.
