# MyHouse - Application de Gestion Immobilière

MyHouse est une application web de gestion immobilière qui permet aux utilisateurs de gérer des biens immobiliers, d'ajouter des pièces, et de consulter les biens disponibles. L'application est construite avec Flask, SQLAlchemy, et Docker.

## Fonctionnalités

- **Authentification** :
    - Les utilisateurs peuvent se connecter et obtenir un token JWT.

- **Gestion des utilisateurs** :
    - Créer un utilisateur.
    - Modifier les informations d'un utilisateur.

- **Gestion des biens immobiliers** :
    - Ajouter un bien immobilier.
    - Modifier un bien immobilier.
    - Lister les biens d'une ville.

- **Gestion des pièces** :
    - Ajouter une pièce à un bien.

- **Fonctionnalité bonus** :
    - Seul le propriétaire d'un bien peut le modifier.

## Prérequis

- Docker
- Docker Compose

## Lancer l'application

### Cloner le dépôt

```bash
git clone git@github.com:YOUSSEF-BOUJYDAH/myHouse.git
cd myHouse
```

### Construire et lancer les conteneurs

```bash
docker-compose up --build
```

### Accéder à l'application

L'API sera disponible à l'adresse :
```
http://localhost:5000
```

## Étapes de migration

Les migrations sont automatiquement appliquées au démarrage de l'application grâce au fichier `run.py`. Si tu souhaites appliquer manuellement les migrations :

### Accéder au conteneur web

```bash
docker-compose exec web bash
```

### Initialiser les migrations (si ce n'est pas déjà fait)

```bash
flask db init
```

### Créer une migration

```bash
flask db migrate -m "Initial migration"
```

### Appliquer la migration

```bash
flask db upgrade
```

## Tester les fonctionnalités

### 1. Créer un utilisateur

```bash
curl -X POST http://localhost:5000/api/users/add \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "John",
           "last_name": "Doe",
           "email": "john.doe@example.com",
           "password": "password123",
           "date_of_birth": "1990-01-01"
         }'
```

### 2. Se connecter (obtenir un token JWT)

```bash
curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{
           "email": "john.doe@example.com",
           "password": "password123"
         }'
```

### 3. Ajouter un bien immobilier

```bash
curl -X POST http://localhost:5000/api/properties/add \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <JWT>" \
     -d '{
           "name": "Maison à Paris",
           "description": "Une belle maison en plein cœur de Paris.",
           "type": "Maison",
           "city": "Paris"
         }'
```

### 4. Modifier un bien immobilier

```bash
curl -X PUT http://localhost:5000/api/properties/update/1 \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <JWT>" \
     -d '{
           "name": "Maison à Paris (modifiée)",
           "description": "Une très belle maison en plein cœur de Paris."
         }'
```

### 5. Lister les biens d'une ville

```bash
curl -X GET http://localhost:5000/api/properties/getByCity/Paris
```

### 6. Ajouter une pièce à un bien

```bash
curl -X POST http://localhost:5000/api/properties/addRoom/1/rooms \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <JWT>" \
     -d '{
           "name": "Salon",
           "size": 20
         }'
```

### 7. Fonctionnalité bonus : Seul le propriétaire peut modifier un bien

#### Test 1 : Modifier un bien avec un autre utilisateur

```bash
curl -X PUT http://localhost:5000/api/properties/update/1 \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <JWT_Jane>" \
     -d '{
           "name": "Maison à Paris (modifiée par Jane)"
         }'
```

#### Réponse attendue

```json
{
  "msg": "You are not the owner of this property"
}
```

#### Test 2 : Modifier un bien avec le propriétaire

```bash
curl -X PUT http://localhost:5000/api/properties/update/1 \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <JWT_John>" \
     -d '{
           "name": "Maison à Paris (modifiée par John)"
         }'
```

#### Réponse attendue

```json
{
  "message": "Property updated successfully",
  "property": {
    "id": 1,
    "name": "Maison à Paris (modifiée par John)",
    "description": "Une très belle maison en plein cœur de Paris.",
    "type": "Maison",
    "city": "Paris"
  }
}
}
```