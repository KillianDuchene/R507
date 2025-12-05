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

## Utilisation dans un context d'infrastructure 

pour simuler une infrastrusture a superviser j'ai utiliser docker-compose pour simuler 3 pc-client et 2 routeur :

### Les 3 pc :

```docker

services:
  pc-1:
    build: dockerclient/.
    container_name: pc-1
    hostname: pc-1
    ports:
      - "2221:22"
    networks:
      reseau_prive:
        ipv4_address: 172.25.0.11
    restart: always

  pc-2:
    build: dockerclient/.
    container_name: pc-2
    hostname: pc-2
    ports:
      - "2222:22"
    networks:
      reseau_prive:
        ipv4_address: 172.25.0.12
    restart: always

  pc-3:
    build: dockerclient/.
    container_name: pc-3
    hostname: pc-3
    ports:
      - "2223:22"
    networks:
      reseau_prive:
        ipv4_address: 172.25.0.13
    restart: always
```
Mes pc client on comme address ip : 172.25.0.11,172.25.0.12,172.25.0.13
le port ssh est macther avec l'hote sur les port 2222,2223,2224 pour pouvoir les joindre depuis le docker-compose et egalement depuis l'exterieur

### Les 2 routeur :

```docker
  router:
    image: aguacero7/frr-router:latest
    container_name: router
    hostname: router-1
    privileged: true
    ports:
      - "2224:22"
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
      - NET_RAW
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv6.conf.all.forwarding=0
    volumes:
      - ./vtysh.conf:/etc/frr/vtysh.conf
    networks:
      reseau_prive:
        ipv4_address: 172.25.0.250
    restart: always

  router-2:
    image: aguacero7/frr-router:latest
    container_name: router-2
    hostname: router-2
    privileged: true
    ports:
      - "2225:22"
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
      - NET_RAW
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv6.conf.all.forwarding=0
    volumes:
      - ./vtysh.conf:/etc/frr/vtysh.conf
    networks:
      reseau_prive:
        ipv4_address: 172.25.0.251
    restart: always
```

### J'ai également 2 application docker utilie pour la supervisation

#### api_serveur

```docker
  api_serveur:
    build: ../.
    container_name: api_serveur
    hostname: api_serveur
    ports:
      - "8000:8000"
    networks:
      reseau_prive:
        ipv4_address: 172.25.0.100
    volumes:
      - ../base_equipement.db:/app/base_equipement.db
    restart: always

```
Cette application vas permetre de cree l'api et de gerer la base de donné

Les chemin de l'api sont : 
* get /routeurs : permet de lister les routeurs
* post /routeur : permet d'ajouter les specification d'un routeur
* delete /routeur/id : permet de supprimé un routeur


* get /pcs : permet de lister les PCs
* post /pc : permet d'ajouter les specification d'un pc
* delete /pc/id : permet de supprimé un pc
* get /name/pc_hostname : permet de lister tout les pcs en fonction du hostname

il y a egalement d'autre chemin comme les switch et les put mais je ne les utilise pas dans l'outil de supervisation


#### requet_api

```docker
  requet_api:
    build: ../request_api/.
    container_name: requet_api
    hostname: requet_api
    networks:
      reseau_prive:
        ipv4_address: 172.25.0.150
    restart: always

```

Cette application fait le lien entre les element a superviser et l'api, elle vas envoyer le fichier python "agent.py" en ssh aux PCs afin qu'il envoit tout seul leur information a l'api sans aucun contact de celle-ci.

Pour les element plus sensible comme les routeur ces l'application qui vas leur envoyer une requete ssh afin de recuperer leur information et de les transmettre grace a l'api