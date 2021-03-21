# TERRE
Ton Écran Ratp (Rer, Etc.)

Nécessite flask et zeep

Pour tester (en local) :

* ajouter le fichier `wsiv.wsdl` dans le répertoire instance
* puis dans le répertoire racine :

```bash
export FLASK_APP=TERRE/TERRE_flask.py
export FLASK_ENV=development
flask run
```
