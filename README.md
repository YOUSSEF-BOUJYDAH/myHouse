# MyHouse – Gestion Immobilière (API REST)

Petit projet personnel de gestion immobilière développé avec **Flask**, **PostgreSQL**, **JWT** et **Docker**.

**Objectif** : démontrer les compétences backend Python  (authentification, CRUD, contrôle d’accès, conteneurisation, tests, CI/CD, déploiement Kubernetes simple).

---

## Fonctionnalités principales

* Inscription et connexion utilisateurs (JWT)
* Création, modification et consultation de biens immobiliers
* Ajout de pièces à un bien immobilier
* Seul le **propriétaire** peut modifier ou supprimer un bien
* Filtrage des biens par ville

---

## Stack technique

* **Backend** : Python 3 + Flask
* **Base de données** : PostgreSQL + SQLAlchemy
* **Authentification** : Flask-JWT-Extended
* **Conteneurisation** : Docker + docker-compose
* **Tests** : pytest
* **Déploiement** : Kubernetes (Deployment, Service, HPA CPU)
* **CI/CD** : GitHub Actions (tests + build + push image)

---

## Prérequis

* Docker + Docker Compose (développement local)
* kubectl + un cluster Kubernetes (Minikube, Kind, ou cloud)
* Compte Docker Hub (ou GitHub Container Registry)

---

## Installation & lancement rapide (local)

### 1. Cloner le dépôt

```bash
git clone https://github.com/YOUSSEF-BOUJYDAH/myHouse.git
cd myHouse
```

### 2. Créer le fichier d’environnement

```bash
cp .env.example .env
```

Remplir les valeurs sensibles dans `.env` :

```env
# Exemple minimal – MODIFIER OBLIGATOIREMENT
POSTGRES_USER=myhouseuser
POSTGRES_PASSWORD=ChangeMeWithAVeryStrongPassword2026!!
POSTGRES_DB=myHouse

DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}

JWT_SECRET_KEY=generate_a_very_long_random_string_here_min_64_chars
```

Générer une bonne clé JWT :

```bash
openssl rand -hex 32
# ou
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Lancer l’application

```bash
docker compose up --build
```

➡️ L’API est disponible sur : **[http://localhost:5000](http://localhost:5000)**

---

## Tester l’API (exemples `curl`)

### Créer un utilisateur

```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "date_of_birth": "1990-01-01"
      }'
```

### Se connecter

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
        "email": "john.doe@example.com",
        "password": "password123"
      }'
```

### Ajouter un bien immobilier

```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
        "name": "Appartement Lyon",
        "description": "T3 lumineux centre-ville",
        "type": "Appartement",
        "city": "Lyon"
      }'
```

### Modifier un bien (test propriétaire)

```bash
curl -X PUT http://localhost:5000/update/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
        "name": "Appartement Lyon – Modifié"
      }'
```

### Lister les biens par ville

```bash
curl http://localhost:5000/getByCity/Lyon
```

### Ajouter une pièce

```bash
curl -X POST http://localhost:5000/addRoom/1/rooms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
        "name": "Chambre parentale",
        "size": 18
      }'
```

---

## Tests

```bash
# Dans le conteneur (recommandé)
docker compose exec web pytest tests/ -v

# Ou localement
pytest tests/ -v
```

---

## Déploiement Kubernetes (simple)

Le dossier `k8s/` contient :

* `deployment.yaml` → 2 replicas
* `service.yaml` → ClusterIP
* `hpa.yaml` → autoscaling CPU (> 65 %)

### Étapes rapides

```bash
# Créer le secret (une seule fois)
kubectl create secret generic myhouse-secrets \
  --from-literal=DATABASE_URL="postgresql://myhouseuser:TON_MDP@db-service:5432/myHouse" \
  --from-literal=JWT_SECRET_KEY="TA_CLE_TRES_LONGUE"

# Déployer
kubectl apply -f k8s/

# Vérifier
kubectl get pods,svc,deploy,hpa -l app=myhouse
```

---

## CI/CD – GitHub Actions

Workflow situé dans `.github/workflows/ci-cd.yml` :

* Lance les tests `pytest`
* Construit l’image Docker
* Pousse l’image sur Docker Hub (ou GHCR)

### Secrets à configurer dans GitHub

* `DOCKER_USERNAME`
* `DOCKER_PASSWORD` (Personal Access Token Docker Hub)

---

## Sécurité & bonnes pratiques

* Secrets uniquement via `.env` ou Kubernetes Secrets
* Pas de credentials en clair dans le dépôt
* Contrôle d’accès propriétaire
* Tests automatisés dans la CI
* Autoscaling CPU dans Kubernetes

---

## Améliorations futures possibles

* Hashage des mots de passe (bcrypt / argon2)
* Validation des données (Pydantic)
* Ingress + HTTPS
* Monitoring basique
* Tests d’intégration PostgreSQL

---

## Auteur

**Youssef BOUJYDAH**
Projet réalisé pour consolider les compétences backend & déploiement.

Bonne exploration 🚀
