# CleanCode

# Médiathèque API – EPSI Quality Code

API REST complète pour la gestion d'une médiathèque (utilisateurs, ressources, emprunts), réalisée en **Python FastAPI** + **PostgreSQL**.

## Sommaire

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Structure du projet](#structure-du-projet)
- [Guide de démarrage rapide](#guide-de-démarrage-rapide)
- [Données de démonstration (Fixtures)](#données-de-démonstration-fixtures)
- [Qualité du code & SonarQube](#qualité-du-code--sonarqube)
- [Respect du cahier des charges](#respect-du-cahier-des-charges)
- [Auteurs](#auteurs)

---

## Description

Cette API permet de :
- Gérer les utilisateurs de la médiathèque
- Gérer les ressources (livres, films, jeux vidéo, etc.)
- Permettre l'emprunt et la restitution des ressources

Toutes les entités sont identifiées par un UUID (jamais d’ID auto-incrément SQL exposé).

---

## Fonctionnalités

### 1. Gestion des utilisateurs
- Création, consultation, modification, suppression
- Champs : id (UUID), nom, prénom, mail (unique), téléphone (tous formats), nationalité

### 2. Gestion des ressources
- Création, consultation (filtrage par type/disponibilité), modification, suppression
- Champs : id (UUID), titre, type (`Livre`, `Film`, `Jeu`, `Autre`), auteur/créateur, disponible

### 3. Système d’emprunt
- Un utilisateur peut emprunter une ou plusieurs ressources disponibles
- Mise à jour de l’état de disponibilité de la ressource
- Enregistrement des dates d’emprunt et de restitution (format : **JJ-MM-AAAA**)
- Restitution (remettre à disposition et supprimer/clore l’emprunt)

### 4. Documentation interactive
- **Swagger UI** disponible sur `/docs` ([localhost:8000/docs](http://localhost:8000/docs))

---

## Structure du projet

.
├── app/  
│   ├── api/  
│   │   ├── main.py  
│   │   ├── dependencies.py  
│   │   └── routers/  
│   │       ├── user.py  
│   │       ├── ressource.py  
│   │       └── emprunt.py  
│   │  
│   ├── db/ #initialisation base de données  
│   │   ├── base.py  
│   │   └── init_db.py  
│   │  
│   ├── models/ # models base de données  
│   │   ├── user.py  
│   │   ├── ressource.py  
│   │   ├── emprunt.py  
│   │   └── utils.py  
│   │  
│   ├── schemas/ #schemas pydantic  
│   │   ├── user.py  
│   │   ├── ressource.py  
│   │   └── emprunt.py  
│   │  
│   ├── repositories/ # opérations CRUD basiques  
│   │   ├── user.py  
│   │   ├── ressource.py  
│   │   └── emprunt.py  
│   │
│   └── services/ # logique métier & validation  
│       ├── user.py  
│       ├── ressource.py  
│       └── emprunt.py  
│  
├── scripts/ # scripts d’administration  
│   └── load_fixtures.py # chargement de données d’exemple  
│
├── tests/ # tests pytest   
│   └── test_app.py # fichiers de tests  
│  
├── requirements.txt  
├── README.md  
└── sonar-project.properties  


---

## Guide de démarrage rapide

### Prérequis

- Python 3.10+
- PostgreSQL (ou autre DB compatible)
- [Docker](https://www.docker.com/) (pour SonarQube)

### Installation
## API

```bash
# 1. Cloner
git clone https://github.com/ton-repo/mediathèque-api.git
cd mediathèque-api

# 2. Environnement virtuel + dépendances
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurer la DB
cp env.example .env
# éditer .env pour renseigner POSTGRES_USER, PASSWORD, HOST, DB, PORT

# 4. Créer les tables
python -m app.db.init

# 5. Charger les fixtures
python -m scripts.load_fixtures

# 6. Lancer l’API
uvicorn app.api.main:app --reload
```

# Accéder à l'API
[http://localhost:8000/docs] #(Swagger)

## Front

```bash
    # 1. Installer les dépendances
    npm install

    # 2. Lancer le serveur
    npm run dev

```