import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

const STAGES = [
  {
    step: '1',
    name: 'Input Vectorization & Normalization',
    algo: 'StandardScaler & Vector Mapping',
    icon: '📊',
    badge: 'Feature Engineering',
    desc: 'The user enters budget in INR, days (1-14), group size, walking comfort tier (Low/Medium/High), and evaluates 6 interest dimensions (Nature, Adventure, Food, History, Shopping, Culture) on a 1-5 discrete scale. These are scaled to zero-mean unit-variance to eliminate dimensional bias.',
    input: 'Budget, Days, Group Size, 6 Interest Ratings, Walking Comfort',
    output: 'Normalized continuous user feature vector X_user',
    equation: 'z = (x - μ) / σ',
  },
  {
    step: '2',
    name: 'Classification: Like Likelihood Prediction',
    algo: 'RandomForestClassifier',
    icon: '🌲',
    badge: 'Supervised ML',
    desc: 'Trained on 2,928 user-place interactions with 5-fold cross-validation. Outperformed Logistic Regression and Decision Tree on test F1-score (89.1%). Uses predict_proba to estimate the exact probability P(Like=1 | user, place) for every candidate spot.',
    input: 'Concatenated (User Vector + Place Vector + Cosine Interest Match)',
    output: 'P(Like) probability ∈ [0.0, 1.0] for every place',
    equation: 'P(y=1|x) = (1/B) Σ_b f_b(x)',
  },
  {
    step: '3',
    name: 'Clustering: Latent Traveller Archetypes',
    algo: 'K-Means Clustering (k=4)',
    icon: '🎯',
    badge: 'Unsupervised ML',
    desc: 'Groups travellers based on interest patterns without ground-truth labels. The optimal cluster count (k=4) was verified via the Elbow Method (identifying the inflection point in within-cluster inertia) and Silhouette scoring. Discovered archetypes: Adventure & Nature, Food & Culture, History & Heritage, Relaxed Leisure.',
    input: '6D Interest Coordinates + Normalized Budget & Pace',
    output: 'Cluster ID & centroid-derived archetype description',
    equation: 'arg min_S Σ_i Σ_{x ∈ S_i} ||x - μ_i||²',
  },
  {
    step: '4',
    name: 'Weighted Composite Recommendation Engine',
    algo: 'Multi-Criteria Utility Scoring',
    icon: '⭐',
    badge: 'Hybrid Recommendation',
    desc: 'Combines the machine learning predicted preference, category affinity, visitor star rating, and budget compatibility using transparent mathematical weights.',
    input: 'RF Prob (0.35), Cosine Match (0.30), Rating (0.20), Budget Fit (0.15)',
    output: 'Ranked list of top destination attractions with audit reasons',
    equation: 'Score = 0.35·P_{RF} + 0.30·Match + 0.20·(Rating/5) + 0.15·BudgetFit',
  },
  {
    step: '5',
    name: 'Regression: Expense & Schedule Estimation',
    algo: 'Ridge Regression & Random Forest Regressor',
    icon: '💰',
    badge: 'Regression Analysis',
    desc: 'Estimates total trip expenditure and required visit hours from past trip logs. Random Forest achieved R² = 0.9367 (MAE ₹7,419) on cost estimation by capturing non-linear group stay scaling, while Ridge Regression (L2 α=10.0) predicts duration with R² = 0.8293.',
    input: 'Days, Group Size, Base Cost/Day, Hotel Tier, Transport Mode',
    output: 'Estimated Cost (₹) & Estimated Activity Hours (h)',
    equation: 'ŷ_{cost} = f_{RF}(X),  ŷ_{time} = Xβ_{Ridge}',
  },
  {
    step: '6',
    name: 'System Constraint Checker & Day-Wise Scheduler',
    algo: 'Greedy Iterative Constraint Solver',
    icon: '⚖️',
    badge: 'Optimization',
    desc: 'Validates that total activities + accommodation + transport do not exceed the declared user budget, and that daily hours match the selected pace (Relaxed: 5h, Balanced: 7h, Packed: 9h). If violated, the lowest composite-scoring place is iteratively swapped until all constraints pass.',
    input: 'Ranked Candidate Activities, Hard Budget Ceiling, Max Hours',
    output: 'Final valid day-by-day itinerary (Morning/Afternoon/Evening)',
    equation: 'Σ Cost_i ≤ Budget  ∧  Σ Time_{i,day} ≤ MaxHours_{pace}',
  },
]

export default function HowItWorksPage() {
  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        {/* Hero */}
        <div className="pt-32 pb-12 px-6">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-3xl sm:text-4xl font-bold text-[#222222] tracking-tight mb-3">
              How the Machine Learning Pipeline Works
            </h1>
            <p className="text-[#717171] text-sm sm:text-base leading-relaxed max-w-2xl mx-auto">
              A comprehensive walkthrough of our multi-stage pipeline, linking feature scaling, supervised classification, unsupervised clustering, composite utility scoring, and constraint satisfaction.
            </p>
          </div>
        </div>

        {/* Stages Timeline */}
        <div className="max-w-4xl mx-auto px-6 pb-20 space-y-6">
          {STAGES.map((s, idx) => (
            <motion.div
              key={s.step}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.05 }}
              className="p-6 sm:p-8 rounded-2xl bg-white border border-[#DDDDDD] shadow-sm relative overflow-hidden"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-[#DDDDDD] gap-2">
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-lg bg-[#222222] text-white flex items-center justify-center text-xs font-semibold">
                    {s.step}
                  </span>
                  <div>
                    <span className="text-[11px] text-[#717171] block">
                      Stage {s.step} · {s.algo}
                    </span>
                    <h3 className="text-lg font-bold text-[#222222]">{s.name}</h3>
                  </div>
                </div>

                <span className="text-xs text-[#717171] bg-[#F7F7F7] border border-[#DDDDDD] px-3 py-1 rounded-full self-start sm:self-auto font-medium">
                  {s.badge}
                </span>
              </div>

              <p className="text-xs text-[#717171] leading-relaxed mb-5">
                {s.desc}
              </p>

              {/* Equation Box */}
              <div className="p-3.5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] font-mono text-xs text-[#222222] flex items-center justify-between mb-4">
                <span className="text-[#717171] font-sans text-xs">Formulation:</span>
                <span className="text-[#008489] font-semibold">{s.equation}</span>
              </div>

              {/* Inputs / Outputs */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-lg bg-[#F7F7F7] border border-[#DDDDDD]">
                  <span className="text-[#717171] block text-[10px] uppercase font-medium mb-0.5">Input Vector</span>
                  <span className="text-[#222222] font-medium">{s.input}</span>
                </div>
                <div className="p-3 rounded-lg bg-[#F7F7F7] border border-[#DDDDDD]">
                  <span className="text-[#717171] block text-[10px] uppercase font-medium mb-0.5">Output Vector</span>
                  <span className="text-[#222222] font-medium">{s.output}</span>
                </div>
              </div>
            </motion.div>
          ))}

          {/* CTA Link */}
          <div className="p-8 rounded-2xl bg-white border border-[#DDDDDD] text-center shadow-sm">
            <h3 className="text-xl font-bold text-[#222222] mb-2">Want to see the models in action?</h3>
            <p className="text-xs text-[#717171] max-w-md mx-auto mb-6">
              Launch the Trip Planner Wizard to execute the full pipeline on your personal travel preferences.
            </p>
            <div className="flex items-center justify-center gap-3">
              <Link to="/planner">
                <button className="px-6 py-2.5 rounded-xl bg-[#222222] hover:bg-[#333333] text-white font-medium text-xs shadow-sm transition-all cursor-pointer flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" /> Launch Trip Planner Wizard
                </button>
              </Link>
              <Link to="/ml-dashboard">
                <button className="px-6 py-2.5 rounded-xl border border-[#DDDDDD] bg-white hover:bg-[#F7F7F7] text-[#222222] font-medium text-xs transition-all cursor-pointer">
                  View Live ML Metrics
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
