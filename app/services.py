from .model import AlbumRecommender
import pandas as pd
import random

# Charger le modèle
recommender = AlbumRecommender()
recommender.load_model()

# Correspondance humeur - genres et styles musicaux
MOOD_GENRE_MAP = {
    "motivé": ["Rock", "Métal", "Punk", "Hip-Hop", "Électro", "Industriel", "Hard", "Alternatif", "Fusion"],
    "paisible": ["Jazz", "Ambient", "Classique", "Folk", "Blues", "Soft", "Indie"],
    "amoureux": ["Soul", "R&B", "Pop", "Chanson", "Soft"],
    "mélancolique": ["Blues", "Indie", "Post-Rock", "Shoegaze", "Stoner"],
    "concentré": ["Classique", "Ambient", "Instrumental", "Lo-Fi", "Expérimental", "Trip-Hop", "Psychédélique",
                  "Progressif"],
    "en soirée": ["Rock", "Électro", "House", "Techno", "Disco", "Rap", "Fusion"]
}


def recommend_album(request):
    # Si l'humeur n'est pas définie, retourner un album aléatoire
    if not request.context.mood:
        return random.choice(request.albums)

    # Créer une liste d'entrées, une par album
    data_list = [{
        'dayOfWeek': request.context.dayOfWeek,
        'timeOfDay': request.context.timeOfDay,
        'season': request.context.season,
        'mood': request.context.mood,
        'location': request.context.location,
        'genre': album.genre,
        'style': album.style or 0,
        'playCount': album.playCount or 0,
        'ignoredCount': album.ignoredCount or 0,
        'listenedCount': album.listenedCount or 0
    } for album in request.albums]

    # Convertir en DataFrame
    data = pd.DataFrame(data_list)

    # Faire une prédiction
    predictions = recommender.predict(data)

    # Sélectionner les albums prédits comme "écouté"
    recommended_albums = [album for album, prediction in zip(request.albums, predictions) if prediction == 'écouté']

    # Si aucun album n'est recommandé, choisir aléatoirement
    if not recommended_albums:
        return random.choice(request.albums)

    # Créer une liste temporaire pour stocker les albums avec leurs scores
    scored_albums = []

    for album in recommended_albums:
        # Score basé sur la fréquence d'écoute (moins écouté = plus recommandé)
        diversity_score = 1 / ((album.playCount or 0) + 1)

        # Score basé sur la correspondance avec l'humeur actuelle
        match_score = 2 if request.context.mood in (album.moods or []) else 1

        # Score basé sur la correspondance entre humeur et genre musical
        genre_match_score = 2 if album.genre in MOOD_GENRE_MAP.get(request.context.mood, []) else 1

        # Score basé sur la correspondance entre humeur et style musical
        style_match_score = 2 if album.style in MOOD_GENRE_MAP.get(request.context.mood, []) else 1

        # Score total = pondération de chaque critère
        total_score = match_score + genre_match_score + style_match_score + diversity_score

        # Ajouter l'album et son score dans une liste temporaire
        scored_albums.append((album, total_score))

    # Trier les albums par score total
    scored_albums.sort(key=lambda x: x[1], reverse=True)

    # Mélanger les albums ayant le même score pour éviter toujours le même résultat
    top_albums = [album for album, _ in scored_albums]
    random.shuffle(top_albums)

    # Retourner le premier album après tri et mélange
    return top_albums[0]
