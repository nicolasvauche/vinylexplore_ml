# app/train_model.py
import pandas as pd
from model import AlbumRecommender


def prepare_data():
    # Exemple de données basé sur ce que l'application Symfony envoie
    data = {
        'dayOfWeek': ['lundi'] * 10 + ['mardi'] * 10 + ['mercredi'] * 10 + ['jeudi'] * 10 + ['vendredi'] * 10,
        'timeOfDay': ['matin'] * 10 + ['midi'] * 10 + ['après-midi'] * 10 + ['soir'] * 10 + ['nuit'] * 10,
        'season': ['printemps'] * 10 + ['été'] * 10 + ['automne'] * 10 + ['hiver'] * 20,
        'mood': ['mélancolique'] * 10 + ['motivé'] * 10 + ['paisible'] * 10 + ['concentré'] * 10 + ['amoureux'] * 10,
        'location': ['maison'] * 30 + ['chérie'] * 10 + ['travail'] * 10,
        'genre': ['Rock'] * 10 + ['Électro'] * 10 + ['Métal'] * 10 + ['Jazz'] * 10 + ['Classique'] * 10,
        'style': ['Hard'] * 10 + ['Alternatif'] * 10 + ['Blues'] * 10 + ['Indie'] * 10 + ['Progressif'] * 10,
        'status': ['écouté'] * 25 + ['ignoré'] * 25,
        'playCount': [1] * 10 + [2] * 10 + [3] * 10 + [4] * 10 + [5] * 10,
        'ignoredCount': [1] * 10 + [2] * 10 + [3] * 10 + [4] * 10 + [5] * 10,
        'listenedCount': [1] * 10 + [2] * 10 + [3] * 10 + [4] * 10 + [5] * 10,
    }
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    data = prepare_data()
    recommender = AlbumRecommender()
    recommender.train(data)
    recommender.save_model()
    print("Model trained and saved successfully!")
