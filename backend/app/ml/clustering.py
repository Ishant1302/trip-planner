"""
Clustering Module - K-Means
Groups travellers into meaningful profiles based on their preferences.
Uses Elbow Method and Silhouette Score to determine optimal k.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "saved_models"


CLUSTER_LABEL_RULES = [
    {"label": "Adventure & Nature Explorer", "icon": "🏔️",
     "description": "Loves outdoor adventures, trekking and natural landscapes",
     "top_features": ["adventure_interest", "nature_interest"]},
    {"label": "Food & Culture Enthusiast", "icon": "🍜",
     "description": "Passionate about local cuisine, art and cultural experiences",
     "top_features": ["food_interest", "culture_interest"]},
    {"label": "History & Heritage Traveller", "icon": "🏛️",
     "description": "Fascinated by historical sites, monuments and ancient civilizations",
     "top_features": ["history_interest", "culture_interest"]},
    {"label": "Relaxed Leisure Traveller", "icon": "🌅",
     "description": "Prefers laid-back itineraries, beaches and wellness retreats",
     "top_features": ["nature_interest", "shopping_interest"]},
    {"label": "Budget Backpacker", "icon": "🎒",
     "description": "Maximizes experiences on a minimal budget with smart planning",
     "top_features": ["adventure_interest", "food_interest"]},
    {"label": "Luxury Wanderer", "icon": "✨",
     "description": "Seeks premium experiences, fine dining and upscale accommodations",
     "top_features": ["shopping_interest", "food_interest"]},
]


class TravelerClusterer:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.kmeans = None
        self.scaler = StandardScaler()
        self.cluster_labels = {}
        self.cluster_descriptions = {}
        self.elbow_data = []
        self.silhouette_data = []
        self.optimal_k = 5
        self.evaluation_results = {}

    def find_optimal_k(self, X, k_range=range(2, 10)):
        """Elbow method + silhouette to find optimal number of clusters."""
        X_scaled = self.scaler.fit_transform(X)
        inertias = []
        silhouettes = []

        for k in k_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias.append(float(km.inertia_))
            if k >= 2:
                score = silhouette_score(X_scaled, km.labels_)
                silhouettes.append(float(score))
            else:
                silhouettes.append(0)

        self.elbow_data = [{"k": k, "inertia": round(i, 2)}
                           for k, i in zip(k_range, inertias)]
        self.silhouette_data = [{"k": k, "silhouette": round(s, 4)}
                                 for k, s in zip(k_range, silhouettes)]

        # Find elbow
        if len(inertias) > 2:
            diffs = np.diff(inertias)
            diffs2 = np.diff(diffs)
            elbow_idx = np.argmax(diffs2) + 1
            self.optimal_k = list(k_range)[elbow_idx]
        else:
            self.optimal_k = 5

        # Also consider silhouette
        best_sil_idx = np.argmax(silhouettes)
        best_sil_k = list(k_range)[best_sil_idx]

        # Balance between elbow and silhouette
        self.optimal_k = min(max(self.optimal_k, 4), 6)
        print(f"Optimal k (elbow): {self.optimal_k}, Best silhouette k: {best_sil_k}")
        return self.optimal_k

    def fit(self, X, n_clusters=None):
        """Fit K-Means and assign cluster labels."""
        if n_clusters is None:
            n_clusters = self.optimal_k
        self.n_clusters = n_clusters

        X_scaled = self.scaler.fit_transform(X)
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.kmeans.fit(X_scaled)

        # Assign meaningful labels based on centroids
        centroids = pd.DataFrame(
            self.scaler.inverse_transform(self.kmeans.cluster_centers_),
            columns=X.columns
        )

        feature_cols = ["nature_interest","adventure_interest","food_interest",
                        "history_interest","shopping_interest","culture_interest"]

        for cluster_id in range(n_clusters):
            centroid = centroids.iloc[cluster_id]
            # Find the two highest interest features
            interests = {col: centroid.get(col, 0) for col in feature_cols if col in centroid}
            top_two = sorted(interests, key=interests.get, reverse=True)[:2]

            # Map to predefined labels
            label_map = {
                frozenset(["adventure_interest","nature_interest"]): ("Adventure & Nature Explorer", "🏔️",
                    "Loves outdoor adventures, trekking and natural landscapes"),
                frozenset(["food_interest","culture_interest"]): ("Food & Culture Enthusiast", "🍜",
                    "Passionate about local cuisine, art and cultural experiences"),
                frozenset(["history_interest","culture_interest"]): ("History & Heritage Traveller", "🏛️",
                    "Fascinated by historical sites, monuments and ancient civilizations"),
                frozenset(["nature_interest","shopping_interest"]): ("Relaxed Leisure Traveller", "🌅",
                    "Prefers laid-back itineraries, beaches and wellness retreats"),
                frozenset(["adventure_interest","food_interest"]): ("Budget Explorer", "🎒",
                    "Maximizes diverse experiences with energetic exploration"),
                frozenset(["shopping_interest","food_interest"]): ("Urban Luxury Wanderer", "✨",
                    "Seeks premium shopping, fine dining and upscale experiences"),
                frozenset(["history_interest","nature_interest"]): ("Cultural Nature Seeker", "🌿",
                    "Blends natural exploration with cultural and historical discovery"),
                frozenset(["adventure_interest","history_interest"]): ("Thrill-Seeking Historian", "⚔️",
                    "Combines adventure sports with deep historical exploration"),
            }

            key = frozenset(top_two)
            default = (f"Traveller Type {cluster_id+1}", "✈️", "Diverse travel preferences")
            lbl, icon, desc = label_map.get(key, default)

            self.cluster_labels[cluster_id] = lbl
            if not hasattr(self, 'cluster_icons'):
                self.cluster_icons = {}
            self.cluster_icons[cluster_id] = icon
            self.cluster_descriptions[cluster_id] = desc

        # Compute silhouette for fitted model
        sil_score = silhouette_score(X_scaled, self.kmeans.labels_)
        cluster_counts = np.bincount(self.kmeans.labels_)

        self.evaluation_results = {
            "n_clusters": n_clusters,
            "inertia": round(float(self.kmeans.inertia_), 2),
            "silhouette_score": round(float(sil_score), 4),
            "elbow_data": self.elbow_data,
            "silhouette_data": self.silhouette_data,
            "optimal_k": self.optimal_k,
            "cluster_distribution": [
                {
                    "cluster_id": int(i),
                    "label": self.cluster_labels.get(i, f"Cluster {i}"),
                    "icon": getattr(self, 'cluster_icons', {}).get(i, "✈️"),
                    "description": self.cluster_descriptions.get(i, ""),
                    "count": int(c),
                    "centroid": {
                        col: round(float(centroids.iloc[i][col]), 2)
                        for col in feature_cols if col in centroids.columns
                    }
                }
                for i, c in enumerate(cluster_counts)
            ],
        }

        joblib.dump(self, MODELS_DIR / "clusterer.pkl")
        joblib.dump(self.evaluation_results, MODELS_DIR / "clustering_results.pkl")
        print(f"Clustering complete: {n_clusters} clusters, Silhouette={sil_score:.4f}")
        return self

    def predict_cluster(self, user_features: dict, feature_cols: list) -> dict:
        """Predict cluster for a new user."""
        if self.kmeans is None:
            return {"cluster_id": 0, "label": "Adventure Traveller", "description": "Loves exploring"}

        X = pd.DataFrame([user_features])[feature_cols]
        X_scaled = self.scaler.transform(X)
        cluster_id = int(self.kmeans.predict(X_scaled)[0])
        return {
            "cluster_id": cluster_id,
            "label": self.cluster_labels.get(cluster_id, f"Traveller Type {cluster_id+1}"),
            "description": self.cluster_descriptions.get(cluster_id, "Diverse travel preferences"),
        }

    @classmethod
    def load(cls):
        path = MODELS_DIR / "clusterer.pkl"
        if path.exists():
            return joblib.load(path)
        return cls()
