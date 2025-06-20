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

---

## Qualité du code & SonarQube

### SonarQube

La qualité du code est analysée par **SonarQube** (linting, tests, sécurité, duplications…) à chaque push sur la branche `main` et à chaque pull request.

- Rapport accessible sur le serveur SonarQube : [SonarQube Server](http://sonarqube.ensiie.fr/)
- Projet : `mediathèque-api`
- Nécessite un compte utilisateur sur le serveur

### Installation locale de SonarQube

Pour les développeurs souhaitant une instance locale de SonarQube :

1. **Docker** : Assurez-vous que Docker est installé et en cours d'exécution.
2. **Lancer SonarQube** : 
   ```bash
   docker run -d --name sonarqube -p 9000:9000 -e SONAR_JDBC_URL=jdbc:postgresql://host.docker.internal:5432/sonar -e SONAR_JDBC_USERNAME=sonar -e SONAR_JDBC_PASSWORD=sonarpassword sonarqube
   ```
3. **Accéder à SonarQube** : Ouvrez votre navigateur et allez à l'adresse [http://localhost:9000](http://localhost:9000).

### Analyse locale

Pour effectuer une analyse locale avant de pousser vos changements :

```bash
# 1. Installer les dépendances requises
pip install bandit black isort flake8 mypy pytest pytest-cov

# 2. Exécuter les outils de qualité
bandit -r app/  # Analyse de sécurité
black --check app/  # Formatage
isort --check-only app/  # Ordre des imports
flake8 app/  # Linting
mypy app/  # Vérification des types
pytest --cov=app tests/  # Tests et couverture
```

---

## Intégration continue : Qualité & Sécurité

### Pipeline SonarQube (GitHub Actions)

Un pipeline CI est configuré pour analyser la qualité du code à chaque pull request, exécution manuelle ou chaque nuit (minuit UTC) via [GitHub Actions](https://github.com/features/actions) :

- **Analyse SonarQube** :
  - Linting, détection de bugs, vulnérabilités, duplications, couverture de tests…
  - Génération automatique du rapport de couverture (`coverage.xml`) avec `pytest`.
  - Nécessite les secrets `SONAR_HOST_URL` et `SONAR_TOKEN` dans les paramètres du repo.

Extrait du workflow :

```yaml
name: SonarQube Analysis
on:
  workflow_dispatch:
  pull_request:
  schedule:
    - cron: "0 0 * * *"
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Install Node.js dependencies
        run: |
          cd src
          npm ci
      - name: run unit tests
        run: |
          pytest --cov=App --cov-report=xml Tests/
        continue-on-error: true
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v5
        env:
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Mises à jour automatiques des dépendances (Dependabot)

Le projet utilise [Dependabot](https://docs.github.com/fr/code-security/dependabot) pour surveiller et proposer automatiquement des pull requests de mise à jour des dépendances Python (`requirements.txt`) et Node.js (`src/package.json`).

- **Fréquence** : quotidienne (`daily`)
- **Sécurité** : chaque PR est testée par le pipeline CI
- **Configuration** : `.github/dependabot.yml`

---

## Respect du cahier des charges

- [x] API REST complète (CRUD, filtres, tri, pagination)
- [x] Authentification JWT
- [x] Documentation Swagger
- [x] Tests unitaires et d'intégration
- [x] Gestion des erreurs
- [x] Logging
- [x] Dockerisation
- [x] CI/CD avec GitHub Actions
- [x] Analyse de code avec SonarQube
- [x] Mise à jour automatique des dépendances avec Dependabot

---