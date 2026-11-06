# API Météo

Petite API de démonstration avec **FastAPI** et **SQLAlchemy**. Elle gère des villes (nom, latitude, longitude) avec un CRUD complet.

## Lancer le projet

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

La documentation interactive est disponible sur http://127.0.0.1:8000/docs

## Architecture

```
app/
├── main.py                  # Point d'entrée : crée l'application
├── core/
│   ├── config.py            # Configuration (lit le fichier .env)
│   └── database.py          # Connexion à la base de données
├── models/
│   └── ville.py             # Modèle ORM : la table "villes"
├── repositories/
│   └── ville_repository.py  # Requêtes vers la base de données
├── services/
│   └── ville_service.py     # Logique métier
└── api/
    ├── deps.py              # Dépendances partagées (session BDD)
    └── v1/
        ├── router.py        # Regroupe toutes les routes de la v1
        ├── schemas/
        │   └── ville.py     # DTO : formats d'entrée et de sortie
        └── routes/
            └── villes.py    # Endpoints HTTP
```

### Le trajet d'une requête

```
Client ──> Route ──> Service ──> Repository ──> Base de données
              ▲                                       │
              └──────────── DTO (schemas) ◄───────────┘
```

Chaque couche a **une seule responsabilité** :

| Couche | Rôle | Elle ne doit pas... |
|---|---|---|
| **Routes** | Recevoir la requête HTTP et renvoyer la réponse | contenir de logique métier ni de requêtes SQL |
| **Schemas (DTO)** | Définir et valider les données échangées avec le client | connaître la base de données |
| **Services** | Appliquer les règles métier (ex : 404 si la ville n'existe pas) | écrire de requêtes SQL directement |
| **Repositories** | Lire et écrire en base de données | contenir de règles métier |
| **Models** | Décrire les tables de la base (ORM) | être renvoyés tels quels au client |

### Les composants en détail

- **`core/`** : la configuration technique. `config.py` lit l'URL de la base dans `.env`, et `database.py` crée le moteur SQLAlchemy et la classe `Base` dont héritent les modèles.
- **`models/`** : les classes Python qui représentent les tables. `Ville` correspond à la table `villes`.
- **`api/v1/schemas/`** : les **DTO** (Data Transfer Objects) Pydantic.
  - `VilleCreate` : ce que le client envoie pour créer ou remplacer une ville (nom, latitude, longitude obligatoires).
  - `VilleUpdate` : ce que le client envoie pour une modification partielle (tous les champs optionnels).
  - `VilleRead` : ce que l'API renvoie (avec l'`id` en plus).
- **`repositories/`** : les fonctions d'accès à la base (`get_all`, `get_by_id`, `save`, `delete`).
- **`services/`** : les fonctions métier appelées par les routes (`lister`, `recuperer`, `creer`, `modifier`, `modifier_partiellement`, `supprimer`).
- **`api/v1/routes/`** : les endpoints FastAPI.
- **`api/deps.py`** : `get_db()` ouvre une session de base de données pour chaque requête et la ferme ensuite.

### Pourquoi un dossier `v1` ?

Les schemas et les routes forment le **contrat** de l'API avec ses clients. Si ce contrat doit changer, on crée un dossier `v2` sans casser les clients qui utilisent encore la `v1`. Les models, repositories et services restent partagés entre les versions.

### Pourquoi séparer Model et DTO ?

- Le **model** décrit la façon dont les données sont **stockées**.
- Le **DTO** décrit la façon dont elles sont **exposées**.

Grâce à cette séparation, on peut changer la base sans changer l'API, et inversement. On peut aussi cacher certains champs : par exemple, on ne renverrait jamais le mot de passe d'un utilisateur.

## Endpoints

Tous les endpoints commencent par `/api/v1/villes`.

| Méthode | URL | Action |
|---|---|---|
| GET | `/` | Lister les villes |
| GET | `/{id}` | Récupérer une ville |
| POST | `/` | Créer une ville |
| PUT | `/{id}` | Remplacer une ville (tous les champs) |
| PATCH | `/{id}` | Modifier une partie d'une ville |
| DELETE | `/{id}` | Supprimer une ville |

Exemple de corps pour `POST` ou `PUT` :

```json
{
  "nom": "Lille",
  "latitude": 50.63,
  "longitude": 3.06
}
```

Exemple de corps pour `PATCH` (on n'envoie que ce qui change) :

```json
{
  "nom": "Lille Métropole"
}
```

### PUT ou PATCH ?

| | PUT | PATCH |
|---|---|---|
| Principe | Remplace **toute** la ressource | Modifie **seulement** les champs envoyés |
| DTO utilisé | `VilleCreate` (tous les champs obligatoires) | `VilleUpdate` (tous les champs optionnels) |
| Champ oublié | Erreur 422 | Valeur actuelle conservée |

Côté service, le PATCH utilise `model_dump(exclude_unset=True)` pour ne récupérer que les champs réellement envoyés par le client.
