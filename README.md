# Projet R507

3 applications :
- **main.py** : lance l'API et gère la base de données (model.py).
- **requet.py** : envoie le fichier agent.py via SSH (classe : SSHConnection) et l'exécute en arrière-plan.
- **agent.py** : s'exécute sur l'ordinateur à superviser et envoie toutes les 60 secondes les informations (RAM, disque, OS, etc.) à l'API définie dans main.py.

## Lancement de l'application API et base de données

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Lancement de la supervision sur un hôte distant

```bash
python3 requet.py
```

## Utilisation dans un contexte d'infrastructure

Pour simuler une infrastructure à superviser, j'ai utilisé docker-compose pour simuler 3 PC-client et 2 routeurs :

### Les 3 PC

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

Les PC clients ont comme adresses IP : 172.25.0.11, 172.25.0.12, 172.25.0.13. Le port SSH est mappé avec l'hôte sur les ports 2221, 2222, 2223 pour pouvoir les joindre depuis docker-compose et de l'extérieur.

### Les 2 routeurs

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

### 2 applications Docker pour la supervision

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

Cette application crée l'API et gère la base de données.

Chemins disponibles de l'API :
- `GET /routeurs` : liste les routeurs
- `POST /routeur` : ajoute un routeur
- `DELETE /routeur/id` : supprime un routeur
- `GET /pcs` : liste les PC
- `POST /pc` : ajoute un PC
- `DELETE /pc/id` : supprime un PC
- `GET /name/pc_hostname` : liste les PC par hostname

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

Cette application fait le lien entre les éléments à superviser et l'API. Elle envoie le fichier agent.py via SSH aux PC pour qu'ils envoient automatiquement leurs informations à l'API toutes les 60 secondes.

Pour les éléments sensibles comme les routeurs, cette application envoie une requête SSH pour récupérer leurs informations et les transmet via l'API.

## Lancement de l'infrastructure

```bash
cd docker
docker compose up
```
Une fois l'infrastructure déployée, le port 8000 de l'hôte est mappé avec celui de l'API Docker.

## fichier python
### main.py

**main.py** dispose de plusieurs dépendances et permet le lancement de l'API.

### /request_api/requet.py

**/request_api/requet.py** déploie **agent.py** sur les PC via SSH, ce qui permet à ces derniers de renvoyer leurs informations via l'API.

### Routeurs

Pour les routeurs, une connexion SSH est établie pour récupérer les informations et effectuer un appel à l'API.



Des tests Bruno sont disponibles dans le dossier `/Bruno`.


