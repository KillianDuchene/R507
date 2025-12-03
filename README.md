# Projet R507

3 application : 
- main.py : elle permet de lancer l'api et gerer la base de donné (model.py).
- requet.py : elle vas envoyer le fichier agent.py via ssh (class : SSHConnection) et l'executer en arriere plan.
- agent.py : elle vas s'executer sur l'ordinateur a superviser et envoyer tout les 60 seconde les informations (ram, disque, os, etc) a l'api defini dans man.py

## Lancement de l'application api et base de donnée : 

```bash
uvicorn main:app --reload
```

## Lancement de la supervision sur un hote distant  : 
```bash
python3 requet.py
```