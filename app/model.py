import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
from sklearn.model_selection import train_test_split


class AlbumRecommender:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, data):
        # Feature Engineering
        data['dayOfWeek'] = data['dayOfWeek'].map(
            {'lundi': 0, 'mardi': 1, 'mercredi': 2, 'jeudi': 3, 'vendredi': 4, 'samedi': 5, 'dimanche': 6})
        data['timeOfDay'] = data['timeOfDay'].map({'matin': 0, 'midi': 1, 'après-midi': 2, 'soir': 3, 'nuit': 4})
        data['season'] = data['season'].map({'printemps': 0, 'été': 1, 'automne': 2, 'hiver': 3})
        data['mood'] = data['mood'].map(
            {'motivé': 0, 'paisible': 1, 'amoureux': 2, 'en soirée': 3, 'mélancolique': 4, 'concentré': 5})
        data['location'] = data['location'].map({'maison': 0, 'travail': 1, 'chez ma compagne': 2})
        data['genre'] = data['genre'].map({'Rock': 0, 'Électro': 1, 'Métal': 2, 'Jazz': 3, 'Classique': 4})
        data['style'] = data['style'].map({'Hard': 0, 'Alternatif': 1, 'Blues': 2, 'Indie': 3, 'Progressif': 4})

        # Ajouter des caractéristiques supplémentaires
        data['playCount'] = data['playCount'].fillna(0)
        data['ignoredCount'] = data['ignoredCount'].fillna(0)
        data['listenedCount'] = data['listenedCount'].fillna(0)

        # Séparation des caractéristiques et de la cible
        X = data.drop(columns=['status'])
        y = data['status']

        # Division des données en ensembles d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entraînement du modèle
        self.model.fit(X_train, y_train)

        # Prédiction et évaluation
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')

    def save_model(self, path='model.joblib'):
        joblib.dump(self.model, os.path.join(os.path.dirname(__file__), '..', path))

    def load_model(self, path='model.joblib'):
        self.model = joblib.load(os.path.join(os.path.dirname(__file__), '..', path))

    def predict(self, data):
        # Convertir les données catégorielles en valeurs numériques
        data['dayOfWeek'] = data['dayOfWeek'].map(
            {'lundi': 0, 'mardi': 1, 'mercredi': 2, 'jeudi': 3, 'vendredi': 4, 'samedi': 5, 'dimanche': 6})
        data['timeOfDay'] = data['timeOfDay'].map({'matin': 0, 'midi': 1, 'après-midi': 2, 'soir': 3, 'nuit': 4})
        data['season'] = data['season'].map({'printemps': 0, 'été': 1, 'automne': 2, 'hiver': 3})
        data['mood'] = data['mood'].map(
            {'motivé': 0, 'paisible': 1, 'amoureux': 2, 'en soirée': 3, 'mélancolique': 4, 'concentré': 5})
        data['location'] = data['location'].map({'maison': 0, 'travail': 1, 'chérie': 2})
        data['genre'] = data['genre'].map({'Rock': 0, 'Électro': 1, 'Métal': 2, 'Jazz': 3, 'Classique': 4})
        data['style'] = data['style'].map({'Hard': 0, 'Alternatif': 1, 'Blues': 2, 'Indie': 3, 'Progressif': 4})

        return self.model.predict(data)
