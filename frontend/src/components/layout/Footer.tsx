import { Link } from 'react-router-dom'
import { Compass, Heart } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-[#F7F7F7] text-[#717171] border-t border-[#DDDDDD] w-full">
      <div className="max-w-7xl mx-auto px-6 pt-16 pb-12 w-full">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-10 pb-12 border-b border-[#DDDDDD]">
          {/* Brand info */}
          <div className="md:col-span-2 space-y-4">
            <Link to="/" className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#222222] flex items-center justify-center text-white">
                <Compass className="w-4 h-4" />
              </div>
              <span className="text-lg font-bold text-[#222222] tracking-tight">
                VoyageML
              </span>
            </Link>
            <p className="text-sm text-[#717171] leading-relaxed max-w-sm">
              An intelligent, machine-learning-powered travel itinerary engine designed for academic evaluation. Demonstrates full-pipeline integration of classification, clustering, weighted utility scoring, and regularized regression.
            </p>
          </div>

          {/* Nav links */}
          <div>
            <h4 className="text-xs font-semibold text-[#222222] uppercase tracking-wider mb-3">
              Explore & Plan
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link to="/destinations" className="text-[#717171] hover:text-[#222222] transition-colors">
                  Top Destinations
                </Link>
              </li>
              <li>
                <Link to="/planner" className="text-[#717171] hover:text-[#222222] transition-colors">
                  Trip Planner Wizard
                </Link>
              </li>
              <li>
                <Link to="/my-trips" className="text-[#717171] hover:text-[#222222] transition-colors">
                  Saved Itineraries
                </Link>
              </li>
              <li>
                <Link to="/destinations?category=Nature" className="text-[#717171] hover:text-[#222222] transition-colors">
                  Nature & Scenic Spots
                </Link>
              </li>
            </ul>
          </div>

          {/* ML & Methodology */}
          <div>
            <h4 className="text-xs font-semibold text-[#222222] uppercase tracking-wider mb-3">
              ML Methodology
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link to="/how-it-works" className="text-[#717171] hover:text-[#222222] transition-colors">
                  6-Stage Pipeline
                </Link>
              </li>
              <li>
                <Link to="/ml-dashboard" className="text-[#717171] hover:text-[#222222] transition-colors">
                  Live Model Metrics
                </Link>
              </li>
              <li>
                <Link to="/ml-dashboard" className="text-[#717171] hover:text-[#222222] transition-colors">
                  Random Forest (F1: 89.1%)
                </Link>
              </li>
              <li>
                <Link to="/ml-dashboard" className="text-[#717171] hover:text-[#222222] transition-colors">
                  K-Means (k=4 Silhouette)
                </Link>
              </li>
            </ul>
          </div>

          {/* Capstone Info */}
          <div>
            <h4 className="text-xs font-semibold text-[#222222] uppercase tracking-wider mb-3">
              Project Credential
            </h4>
            <div className="space-y-2 text-sm text-[#717171]">
              <p className="font-medium text-[#222222]">Group 6 Capstone Project</p>
              <p className="text-xs leading-relaxed">Machine Learning Academic Report Reference Implementation</p>
              <div className="pt-2">
                <Link
                  to="/about"
                  className="inline-flex items-center gap-1 text-sm text-[#008489] hover:underline font-medium"
                >
                  Read Architecture Spec →
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[#717171]">
          <p>© 2026 VoyageML — Machine Learning Academic Capstone Platform.</p>
          <p className="flex items-center gap-1">
            Engineered with <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500 inline" /> using React 19, Vite, Tailwind CSS & FastAPI
          </p>
        </div>
      </div>
    </footer>
  )
}
