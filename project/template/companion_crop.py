# models.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class CompanionCropModel:
    def __init__(self):
        # Load companion planting data
        self.companion_data = pd.read_csv('companion_planting_data.csv')

        # Split data into features and target
        X = self.companion_data.drop('companion_crop', axis=1)
        y = self.companion_data['companion_crop']

        # Initialize and train the Random Forest classifier
        self.rf_classifier = RandomForestClassifier()
        self.rf_classifier.fit(X, y)

    def predict_companion_crop(self, crop_name):
        # Predict companion crop for a given crop
        return self.rf_classifier.predict([crop_name])[0]
