# Trip Planner System — AI/ML-Powered Personalized Travel Planning Platform

An academic capstone Machine Learning web application combining Supervised Learning, Unsupervised Clustering, Multi-Criteria Recommendation, and Regularized Regression into an end-to-end travel itinerary and budget planning platform.

---

## 📌 Executive Summary

Traditional travel planning tools offer generic, one-size-fits-all itineraries that ignore individual budget ceilings, time limits, physical walking comfort, food preferences, and multidimensional interest weighting. 

This project implements the complete Machine Learning methodology described in the project report:
```
USER INPUT
    ↓
CLASSIFICATION (Random Forest Classifier)
    ↓
CLUSTERING (K-Means Clustering, k=4)
    ↓
RECOMMENDATION (Weighted Composite Utility Scoring)
    ↓
REGRESSION (Cost & Time Estimation: Ridge + Random Forest Regressor)
    ↓
CONSTRAINT CHECKING (Iterative Pruning & Budget Compliance Solver)
    ↓
FINAL PERSONALIZED TRIP PLAN (Day-wise Itinerary & Analytics)
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, TypeScript, Vite 8, Tailwind CSS v4, Framer Motion, Recharts, Lucide React, Sonner Toasts |
| **UI Foundation** | 21st.dev `saa-s-template.tsx` adapted for travel technology startup aesthetics |
| **Backend** | Python 3.13, FastAPI, Pydantic v2, Uvicorn ASGI, SQLite (PostgreSQL migration ready) |
| **Machine Learning** | Scikit-Learn 1.5, Pandas, NumPy, Joblib |
| **Database** | SQLite with SQLAlchemy ORM (`trips`, `destinations`, `favourites` tables) |

---

## 🧠 Machine Learning Methodology

### 1. Classification — Random Forest Classifier
- **Objective:** Predict whether a user will Like ($1$) or Not Like ($0$) a specific attraction based on preference vectors.
- **Model Comparison:** 
  - **Logistic Regression (Baseline):** Acc: 81.4%, Precision: 82.7%, Recall: 97.5%, F1: 89.5%, ROC-AUC: 0.704
  - **Decision Tree Classifier:** Acc: 78.2%, Precision: 82.9%, Recall: 92.0%, F1: 87.2%, ROC-AUC: 0.641
  - **Random Forest Classifier (Selected Final Model):** Acc: 80.4%, Precision: 81.1%, Recall: 98.7%, F1: 89.1%, ROC-AUC: 0.711
- **Cross-Validation:** 5-fold cross-validation with GridSearchCV parameter search (`n_estimators=200`, `min_samples_leaf=5`, `max_depth=None`), yielding CV F1: $0.8966 \pm 0.0015$.
- **Feature Importance (Top Signals):**
  1. `interest_match`: 15.98%
  2. `cost_to_budget_ratio`: 12.81%
  3. `average_cost`: 7.22%
  4. `avg_interest`: 6.66%
  5. `distance_from_city_centre`: 5.94%

### 2. Clustering — K-Means
- **Objective:** Group travellers into latent travel archetypes without predefined class labels.
- **Cluster Selection:** Optimal $k=4$ validated through:
  - **Elbow Method:** Clear inflection point in within-cluster sum of squares (inertia: 3976.8).
  - **Silhouette Score:** Evaluated across $k \in [2, 8]$ ($0.0824$).
- **Discovered Archetypes & Centroids:**
  1. **Budget Explorer** (138 users): High adventure and food affinity with constrained budget.
  2. **Urban Culture Explorer** (73 users): Balanced city arts, shopping, and food.
  3. **History & Heritage Traveller** (138 users): Dominant historical & cultural preference ($4.6/5$).
  4. **Relaxed Leisure Traveller** (151 users): Dominant nature, wellness, and scenic interest ($4.5/5$).

### 3. Multi-Criteria Recommendation Engine
- **Formula:**
  $$\text{Score} = 0.35 \cdot P_{\text{RF}}(\text{Like}) + 0.30 \cdot \text{InterestMatch} + 0.20 \cdot \frac{\text{Rating}}{5} + 0.15 \cdot \text{BudgetFit}$$
- All components normalized to $[0.0, 1.0]$.
- Every recommended attraction includes automated natural-language explanations (e.g., *"Strong match for your history interest (rated 5/5)"*, *"92% predicted likelihood"*).

### 4. Regression — Cost & Time Estimation
- **Objective:** Predict total monetary expense and required activity hours from past trip logs.
- **Cost Estimation:**
  - **Ridge Regression (L2 Penalty $\alpha=10.0$):** MAE: ₹15,252, RMSE: ₹23,474, $R^2 = 0.7840$
  - **Random Forest Regressor (Selected):** MAE: ₹7,419, RMSE: ₹12,706, $R^2 = 0.9367$
- **Time Estimation:**
  - **Ridge Regression (Selected):** MAE: 6.12h, RMSE: 7.50h, $R^2 = 0.8293$
  - **Random Forest Regressor:** MAE: 6.36h, RMSE: 7.90h, $R^2 = 0.8104$

### 5. Constraint Checking Solver
- Real system-level iterative optimization step.
- Checks:
  1. $\sum \text{Cost} \le \text{Budget}$
  2. $\sum \text{Hours}_{\text{day}} \le \text{MaxHours}_{\text{pace}}$ (Relaxed: 5h, Balanced: 7h, Packed: 9h)
  3. Walking comfort radius enforcement ($\text{Low} \le 15\text{km}$, $\text{Medium} \le 40\text{km}$)
  4. Dietary preferences consideration
- Pruning strategy: If constraints are violated, iteratively removes the lowest composite-scoring place, logs an audit message, and recalculates until all constraints are met.

---

## 📊 Datasets

Located in `backend/datasets/`:
1. `destinations.csv`: 20 authentic Indian destinations (Goa, Jaipur, Kerala Backwaters, Manali, Leh Ladakh, Varanasi, Udaipur, Agra, Mumbai, etc.) with coordinates, average daily cost, ratings, and category tags.
2. `places.csv`: 111 detailed attractions and landmarks with 6-dimensional category scores (1-5), admission costs, average visit durations, and distance from city centre.
3. `users.csv`: 500 simulated user profiles with budgets, duration, group size, and 6-dimensional interest preferences.
4. `interactions.csv`: 2,928 user-place interaction observations (Like, Saved, Skipped) for supervised training.
5. `past_trips.csv`: 800 historical trip records with actual recorded costs and activity durations for regression training.

*Academic note: Interaction and past trip datasets are synthetically generated with fixed random seed (42) for reproducible academic demonstration.*

---

## 🚀 How to Run the Application

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Node.js 18+ (Tested on Node.js v24)
- npm or pnpm

---

### Step 1: Start the Backend (FastAPI)

```bash
# Navigate to the backend directory
cd backend

# (Optional) Activate your Python virtual environment
# python -m venv venv && .\venv\Scripts\activate

# Run the FastAPI server via Uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API will be accessible at: `http://localhost:8000`
- Interactive Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

---

### Step 2: Start the Frontend (Vite + React)

Open a second terminal:

```bash
# Navigate to the frontend directory
cd frontend

# Start the Vite development server
npm run dev
```
- Web Application will be accessible at: `http://localhost:5173`

---

### Step 3: Retraining the Machine Learning Models (Optional)

All models are pre-trained and saved in `backend/saved_models/`. To retrain models from scratch:

```bash
# Run the training script directly
python backend/app/ml/train.py
```
Or click the **"Retrain Pipeline"** button on the live **ML Insights & Model Analytics** dashboard (`/ml-dashboard`).

---

## 🌐 Application Pages & User Journey

1. **Landing Page (`/`):** Built on the exact 21st.dev SaaS template foundation (`saa-s-template.tsx`), featuring a dark-themed travel startup visual design, animated dashboard preview, core features, and top destinations.
2. **Explore Destinations (`/destinations`):** Filter by category, budget tier, and minimum rating. Search by name and bookmark favorites.
3. **Destination Detail (`/destinations/:name`):** High-resolution destination overview, benchmark statistics, category-grouped attractions, and 1-click transition to the planner wizard.
4. **Trip Planner Wizard (`/planner`):** 6-step interactive questionnaire covering Destination, Budget & Days, 6D Interest Ratings (1-5), Travel Style, Pace & Group Dynamic, and a Final Review Screen.
5. **Trip Result Dashboard (`/trips/:id`):** 
   - Assigned K-Means traveller profile.
   - Total estimated cost vs. remaining budget.
   - Random Forest predicted like-probability.
   - Interactive day-by-day itinerary (morning/afternoon/evening slots) with real-time activity deletion and cost recalculation.
   - Recharts visual expenditure pie chart breakdown.
   - Constraint solver audit log.
6. **My Trips Hub (`/my-trips`):** Saved trip itineraries and bookmarked destinations stored in the SQLite database.
7. **ML Insights & Model Analytics (`/ml-dashboard`):** Real academic dashboard displaying:
   - Logistic Regression vs. Decision Tree vs. Random Forest metrics (Accuracy, Precision, Recall, F1, ROC-AUC).
   - 2x2 Confusion Matrix for Random Forest.
   - Gini Feature Importance bar chart.
   - K-Means Elbow Curve (Inertia vs $k$) and Silhouette Score chart.
   - Cluster centroid dimension tables.
   - Actual vs. Predicted Cost scatter plot ($R^2 = 0.9367$).
   - Live Retrain button triggering backend pipeline.
8. **How It Works (`/how-it-works`):** Comprehensive step-by-step mathematical breakdown for academic project evaluation.
9. **About Page (`/about`):** Architecture breakdown, tech stack summary, and dataset disclosure.

---

## 🧪 Verification & Testing

To test the ML pipeline and services directly:

```bash
python backend/datasets/generate_datasets.py   # Generates raw CSVs
python backend/app/ml/train.py                 # Trains all models
python -c "import app.main; print('Import OK')" # Verifies backend imports
```

---

## 📄 License & Attribution

Academic Machine Learning Capstone Project.
Template component adapted from 21st.dev React Component Library.
Tourist attraction benchmarks modeled after authentic locations across India.

