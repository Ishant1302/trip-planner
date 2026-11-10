import { Link } from 'react-router-dom'
import { CheckCircle2 } from 'lucide-react'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

export default function AboutPage() {
  const stack = [
    {
      category: 'Frontend Engineering',
      techs: ['React 19 + TypeScript', 'Vite 8', 'Tailwind CSS v4', 'Framer Motion', 'Recharts Analytics', 'Lucide Icons'],
      desc: 'Modern, fully responsive client interface inspired by clean Airbnb and Linear aesthetics with custom travel design system.',
    },
    {
      category: 'Backend & REST APIs',
      techs: ['FastAPI (Python 3.13)', 'Uvicorn ASGI', 'Pydantic v2 Validation', 'SQLAlchemy ORM', 'SQLite (PostgreSQL ready)'],
      desc: 'Modular REST service with asynchronous endpoints, parameter validation, and SQLite persistence for trips and bookmarks.',
    },
    {
      category: 'Machine Learning Core',
      techs: ['Scikit-Learn 1.5', 'Pandas & NumPy', 'RandomForestClassifier', 'K-Means Clustering', 'Ridge & RF Regressors'],
      desc: 'Supervised classification, unsupervised archetype profiling, multi-criteria recommendation, and constraint enforcement.',
    },
  ]

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        <div className="pt-32 pb-12 px-6">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-3xl sm:text-4xl font-bold text-[#222222] tracking-tight mb-3">
              About the Trip Planner System
            </h1>
            <p className="text-[#717171] text-sm sm:text-base leading-relaxed max-w-2xl mx-auto">
              Built as a comprehensive Machine Learning capstone project demonstrating practical implementations of ML algorithms in modern travel technology.
            </p>
          </div>
        </div>

        <div className="max-w-5xl mx-auto px-6 pb-20 space-y-10">
          {/* Project Goals */}
          <div className="bg-white rounded-2xl border border-[#DDDDDD] p-8 shadow-sm">
            <h2 className="text-xl font-bold text-[#222222] mb-3">Project Objectives & Motivation</h2>
            <p className="text-xs sm:text-sm text-[#717171] leading-relaxed mb-6">
              Traditional travel planning tools offer one-size-fits-all itineraries that fail to account for a traveller's unique interest weighting, physical walking comfort, food restrictions, and strict budget ceilings. This project designs and deploys an intelligent end-to-end Machine Learning pipeline that maps user preferences into an optimized, constraint-checked travel itinerary.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-[#008489] flex-shrink-0 mt-0.5" />
                <span className="text-[#717171]">
                  <strong className="text-[#222222]">Supervised Classification:</strong> Predicts Like/Not-Like with 89.1% F1-score via Random Forest with 5-fold CV.
                </span>
              </div>
              <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-[#008489] flex-shrink-0 mt-0.5" />
                <span className="text-[#717171]">
                  <strong className="text-[#222222]">Unsupervised Clustering:</strong> Discovers latent traveller archetypes from 6-dimensional interest space using K-Means.
                </span>
              </div>
              <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-[#008489] flex-shrink-0 mt-0.5" />
                <span className="text-[#717171]">
                  <strong className="text-[#222222]">Regularized Regression:</strong> Accurately forecasts total trip expenses (R² = 0.9367) and activity hours using Ridge & RF.
                </span>
              </div>
              <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-[#008489] flex-shrink-0 mt-0.5" />
                <span className="text-[#717171]">
                  <strong className="text-[#222222]">Constraint Enforcement:</strong> Guaranteed adherence to financial and daily time constraints via iterative optimization.
                </span>
              </div>
            </div>
          </div>

          {/* Technology Architecture */}
          <div>
            <h2 className="text-xl font-bold text-[#222222] mb-6 text-center">Full-Stack Architecture</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {stack.map(s => (
                <div key={s.category} className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
                  <div>
                    <h3 className="font-bold text-[#222222] text-base mb-2">{s.category}</h3>
                    <p className="text-xs text-[#717171] leading-relaxed mb-6">{s.desc}</p>
                  </div>
                  <div className="pt-4 border-t border-[#DDDDDD]">
                    <ul className="space-y-1.5 text-xs text-[#717171] font-mono">
                      {s.techs.map(t => (
                        <li key={t} className="flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-[#222222]" /> {t}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Academic Attribution Card */}
          <div className="p-8 rounded-2xl bg-white border border-[#DDDDDD] text-center shadow-sm">
            <span className="text-xs font-mono uppercase text-[#717171] tracking-wider block mb-1">
              University Capstone Project
            </span>
            <h3 className="text-xl font-bold text-[#222222] mb-2">
              Trip Planner System · Group 6 Machine Learning Project
            </h3>
            <p className="text-xs text-[#717171] max-w-lg mx-auto mb-6">
              Based on the academic report <code className="bg-[#F7F7F7] border border-[#DDDDDD] px-1.5 py-0.5 rounded text-[#222222]">Trip_Planner_Report_Ml.pdf</code> and custom design system.
            </p>
            <Link to="/planner">
              <button className="px-6 py-2.5 rounded-xl bg-[#222222] hover:bg-[#333333] text-white font-medium text-xs shadow-sm transition-all cursor-pointer">
                Launch Trip Planner System →
              </button>
            </Link>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
