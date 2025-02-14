# VinyleXplore - Moteur de Recommandation de Vinyles 🎶

VinyleXplore est un moteur de recommandation de vinyles intelligent basé sur l'humeur et le contexte d'écoute de
l'utilisateur. Il utilise **FastAPI** pour exposer une API REST et **scikit-learn** pour entraîner un modèle de Machine
Learning qui améliore la pertinence des suggestions.

## Fonctionnalités

- Recommandation d'albums en fonction :
    - De l'**humeur** de l'utilisateur (motivé, paisible, amoureux, etc.).
    - Du **moment de la journée** (matin, midi, soir...).
    - De la **saison** actuelle.
    - Du **lieu** où se trouve l'utilisateur.
    - Du **nombre d'écoutes** passées.
    - Du **genre et du style musical** des albums.
- **Sélection aléatoire** d’un album si aucune humeur n'est définie.
- **Moteur basé sur un modèle de Machine Learning** entraîné avec `RandomForestClassifier`.
- **Exposition via une API REST** avec FastAPI.

---

## Installation

### 1. Cloner le projet

```bash
git clone [url_du_referentiel]
cd vinylexplore_ml
```

### 2. Créer un environnement virtuel et installer les dépendances

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3. Lancer l'API FastAPI

```bash
uvicorn app.main:app --reload
```

L'API sera disponible à l'adresse http://127.0.0.1:8000.

---

## Endpoints de l'API

Route : `POST /recommend`

Corps de la requête (JSON) :

```json
{
  "context": {
    "dayOfWeek": "vendredi",
    "timeOfDay": "soir",
    "season": "hiver",
    "mood": "motivé",
    "location": "maison"
  },
  "albums": [
    {
      "id": 1,
      "moods": [
        "motivé",
        "en soirée"
      ],
      "playCount": 3,
      "lastPlayedAt": 1700000000,
      "listeningHistory": [],
      "ignoredCount": 1,
      "listenedCount": 2,
      "genre": "Rock",
      "style": "Alternative Rock"
    },
    {
      "id": 2,
      "moods": [
        "paisible"
      ],
      "playCount": 10,
      "lastPlayedAt": 1700000000,
      "listeningHistory": [],
      "ignoredCount": 3,
      "listenedCount": 7,
      "genre": "Jazz",
      "style": "Smooth Jazz"
    }
  ]
}
```

Réponse attendue :

```json
{
  "id": 1,
  "moods": [
    "motivé",
    "en soirée"
  ],
  "playCount": 3,
  "lastPlayedAt": 1700000000,
  "listeningHistory": [],
  "ignoredCount": 1,
  "listenedCount": 2,
  "genre": "Rock",
  "style": "Alternative Rock"
}
```

---

## Algorithme de Recommandation

### 1. Prétraitement des Données :

Transformation des catégories (dayOfWeek, mood, etc.) en valeurs numériques.
Gestion des valeurs None (remplacement par 0 si nécessaire).
Création d'un DataFrame pour la prédiction.

### 2. Prédiction via Machine Learning :

Utilisation d'un RandomForestClassifier entraîné sur des écoutes réelles.
Le modèle classe les albums comme "écouté" ou "ignoré".

### 3. Calcul du Score des Albums :

- Diversité : Moins un album a été écouté, plus il est recommandé.
- Match Humeur-Genre : Si le genre ou le style correspond à l'humeur, bonus de score.
- Correspondance avec l’historique d’écoute : Les albums déjà appréciés sont favorisés.
- Mélange des albums de score égal pour éviter la répétition.

### 4. Sélection de l'album final :

- Si mood est null → Sélection totalement aléatoire.
- Sinon → Album avec le meilleur score et mélange des résultats.

---

## Entraînement du Modèle

Le modèle est entraîné avec des données simulées dans `train_model.py` :

```bash
python app/train_model.py
```

---

## Améliorations Futures

- Ajout du filtrage temporel pour éviter de recommander un album écouté récemment.
- Prise en compte des albums jamais écoutés dans la recommandation.
- Affinage du modèle avec de véritables données d’écoute utilisateurs.

---

## Licence

Ce projet est sous licence MIT.