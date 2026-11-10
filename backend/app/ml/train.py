"""
Training Script - Trip Planner ML Pipeline
Runs the complete ML pipeline:
1. Data Preprocessing
2. Classification (Random Forest)
3. Clustering (K-Means)
4. Regression (Cost & Time)
Saves all models and evaluation results to saved_models/.
"""

import sys
import json
import time
import traceback
from pathlib import Path

# Add the project root to path so imports resolve correctly
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir.parent))

from app.ml.preprocessing import DataPreprocessor
from app.ml.classification import TripClassifier
from app.ml.clustering import TravelerClusterer
from app.ml.regression import TripRegressor

import joblib

MODELS_DIR = backend_dir / "saved_models"
MODELS_DIR.mkdir(exist_ok=True)


def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def train_pipeline() -> dict:
    """
    Full end-to-end ML training pipeline.
    Returns a summary dict of all training results.
    """
    start_time = time.time()
    results = {}

    # ------------------------------------------------------------------ #
    # STEP 1: Data Preprocessing
    # ------------------------------------------------------------------ #
    print_section("STEP 1: Data Preprocessing")
    try:
        preprocessor = DataPreprocessor()
        data = preprocessor.prepare_all()

        clf_data = data["classification"]
        cluster_data = data["clustering"]
        reg_data = data["regression"]

        print(f"  Classification samples: {len(clf_data['X_train'])} train, {len(clf_data['X_test'])} test")
        print(f"  Clustering samples: {len(cluster_data['X'])}")
        print(f"  Regression samples: {len(reg_data['X_train'])} train, {len(reg_data['X_test'])} test")
        print(f"  Feature names: {clf_data['feature_names']}")

        results["preprocessing"] = {
            "status": "success",
            "classification_train_size": len(clf_data["X_train"]),
            "classification_test_size": len(clf_data["X_test"]),
            "clustering_size": len(cluster_data["X"]),
            "regression_train_size": len(reg_data["X_train"]),
            "feature_count": len(clf_data["feature_names"]),
            "feature_names": clf_data["feature_names"],
        }
    except Exception as e:
        print(f"  ERROR in preprocessing: {e}")
        traceback.print_exc()
        results["preprocessing"] = {"status": "error", "error": str(e)}
        return results

    # ------------------------------------------------------------------ #
    # STEP 2: Classification
    # ------------------------------------------------------------------ #
    print_section("STEP 2: Classification - Random Forest")
    try:
        classifier = TripClassifier()
        classifier.train_all_models(
            clf_data["X_train"],
            clf_data["y_train"],
            clf_data["feature_names"],
        )
        clf_eval = classifier.evaluate(clf_data["X_test"], clf_data["y_test"])

        print("\n  === Model Comparison ===")
        for model_name, metrics in clf_eval["model_comparison"].items():
            print(f"  {model_name}:")
            print(f"    Accuracy : {metrics['accuracy']:.4f}")
            print(f"    Precision: {metrics['precision']:.4f}")
            print(f"    Recall   : {metrics['recall']:.4f}")
            print(f"    F1 Score : {metrics['f1_score']:.4f}")
            print(f"    ROC-AUC  : {metrics['roc_auc']:.4f}")

        print(f"\n  Best Model (by F1): {clf_eval['best_model']}")
        print(f"  Final Model: {clf_eval['final_model']}")
        print(f"  CV F1: {clf_eval['cv_f1_mean']:.4f} +/- {clf_eval['cv_f1_std']:.4f}")

        print("\n  Top 5 Feature Importances:")
        for fi in clf_eval["feature_importance"][:5]:
            print(f"    {fi['feature']}: {fi['importance']:.4f}")

        results["classification"] = {
            "status": "success",
            **clf_eval,
        }
    except Exception as e:
        print(f"  ERROR in classification: {e}")
        traceback.print_exc()
        results["classification"] = {"status": "error", "error": str(e)}
        classifier = TripClassifier()

    # ------------------------------------------------------------------ #
    # STEP 3: Clustering
    # ------------------------------------------------------------------ #
    print_section("STEP 3: Clustering - K-Means")
    try:
        clusterer = TravelerClusterer()
        optimal_k = clusterer.find_optimal_k(cluster_data["X"])
        print(f"  Optimal k determined: {optimal_k}")

        clusterer.fit(cluster_data["X"], n_clusters=optimal_k)
        cluster_eval = clusterer.evaluation_results

        print(f"\n  Clustering Results:")
        print(f"    n_clusters     : {cluster_eval['n_clusters']}")
        print(f"    Inertia        : {cluster_eval['inertia']:.2f}")
        print(f"    Silhouette     : {cluster_eval['silhouette_score']:.4f}")

        print("\n  Cluster Distribution:")
        for c in cluster_eval["cluster_distribution"]:
            lbl = str(c['label']).encode('ascii', 'ignore').decode('ascii')
            print(f"    Cluster {c['cluster_id']}: {lbl} ({c['count']} users)")

        results["clustering"] = {
            "status": "success",
            **cluster_eval,
        }
    except Exception as e:
        print(f"  ERROR in clustering: {e}")
        traceback.print_exc()
        results["clustering"] = {"status": "error", "error": str(e)}
        clusterer = TravelerClusterer()

    # ------------------------------------------------------------------ #
    # STEP 4: Regression
    # ------------------------------------------------------------------ #
    print_section("STEP 4: Regression - Cost & Time Estimation")
    try:
        regressor = TripRegressor()
        regressor.train(
            reg_data["X_train"], reg_data["X_test"],
            reg_data["y_cost_train"], reg_data["y_cost_test"],
            reg_data["y_time_train"], reg_data["y_time_test"],
        )
        reg_eval = regressor.evaluation_results

        print("\n  Cost Estimation:")
        print(f"    Best Model: {reg_eval['cost_estimation']['best_model']}")
        for model_type in ["ridge_regression", "random_forest"]:
            m = reg_eval["cost_estimation"][model_type]
            print(f"    {model_type}: MAE={m['mae']:.2f}, RMSE={m['rmse']:.2f}, R2={m['r2']:.4f}")

        print("\n  Time Estimation:")
        print(f"    Best Model: {reg_eval['time_estimation']['best_model']}")
        for model_type in ["ridge_regression", "random_forest"]:
            m = reg_eval["time_estimation"][model_type]
            print(f"    {model_type}: MAE={m['mae']:.2f}, RMSE={m['rmse']:.2f}, R2={m['r2']:.4f}")

        results["regression"] = {
            "status": "success",
            **reg_eval,
        }
    except Exception as e:
        print(f"  ERROR in regression: {e}")
        traceback.print_exc()
        results["regression"] = {"status": "error", "error": str(e)}
        regressor = TripRegressor()

    # ------------------------------------------------------------------ #
    # STEP 5: Save Combined Pipeline State
    # ------------------------------------------------------------------ #
    print_section("STEP 5: Saving Pipeline State")
    try:
        pipeline_state = {
            "preprocessor": preprocessor,
            "classifier": classifier,
            "clusterer": clusterer,
            "regressor": regressor,
            "feature_names": clf_data.get("feature_names", []),
        }
        joblib.dump(pipeline_state, MODELS_DIR / "pipeline.pkl")

        # Save evaluation summary as JSON
        summary = {
            "preprocessing": results.get("preprocessing", {}),
            "classification": {
                k: v for k, v in results.get("classification", {}).items()
                if k != "feature_importance"  # exclude large objects for JSON
            },
            "clustering": {
                k: v for k, v in results.get("clustering", {}).items()
                if k not in ("elbow_data", "silhouette_data")
            },
            "regression": results.get("regression", {}),
        }

        with open(MODELS_DIR / "training_summary.json", "w") as f:
            json.dump(summary, f, indent=2, default=str)

        import datetime
        status = {
            "trained": True,
            "trained_at": datetime.datetime.now().isoformat(),
            "models": ["Random Forest Classifier", "K-Means Clusterer", "Cost Regressor", "Time Regressor"],
            "classification_f1": results.get("classification", {}).get("model_comparison", {}).get("Random Forest", {}).get("f1_score", 0),
            "clustering_silhouette": results.get("clustering", {}).get("silhouette_score", 0),
        }
        with open(MODELS_DIR / "training_status.json", "w") as f:
            json.dump(status, f, indent=2)

        elapsed = round(time.time() - start_time, 2)
        print(f"  Pipeline state saved to {MODELS_DIR}")
        print(f"  Total training time: {elapsed}s")
        results["total_time_seconds"] = elapsed
        results["status"] = "success"

    except Exception as e:
        print(f"  ERROR saving pipeline: {e}")
        traceback.print_exc()
        results["save_error"] = str(e)

    print_section("TRAINING COMPLETE")
    return results


def load_pipeline():
    """Load the saved full pipeline from disk."""
    path = MODELS_DIR / "pipeline.pkl"
    if path.exists():
        return joblib.load(path)
    raise FileNotFoundError(
        f"No saved pipeline found at {path}. Run train_pipeline() first."
    )


train_all = train_pipeline


if __name__ == "__main__":
    results = train_pipeline()
    print("\nFinal Results Summary:")
    for key, val in results.items():
        if isinstance(val, dict):
            print(f"  {key}: {val.get('status', 'unknown')}")
        else:
            print(f"  {key}: {val}")
