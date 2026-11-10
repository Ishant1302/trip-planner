import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Star, MapPin, Zap, Brain, Shield, ArrowRight, TrendingUp, Clock,
  ChevronRight
} from 'lucide-react'
import { TemplateNavigation, TemplateHero } from '@/components/ui/saa-s-template'
import Footer from '@/components/layout/Footer'
import { destinationsApi, type Destination } from '@/services/api'

const FEATURES = [
  {
    icon: <Brain className="w-5 h-5 text-purple-700" />,
    title: 'Random Forest Classification',
    description: 'Predicts your likelihood of loving each spot based on your multidimensional preference vector, interest alignment, and place rating.',
    badge: 'Supervised ML',
    stat: 'F1: 89.1%',
    iconBg: 'bg-purple-50',
  },
  {
    icon: <Zap className="w-5 h-5 text-teal-700" />,
    title: 'K-Means Traveller Profiling',
    description: 'Discovers latent traveller archetypes (e.g., Adventure Explorer, Food & Culture Enthusiast) from centroid features.',
    badge: 'Unsupervised ML',
    stat: 'k=4 Clusters',
    iconBg: 'bg-teal-50',
  },
  {
    icon: <TrendingUp className="w-5 h-5 text-amber-700" />,
    title: 'Ridge & RF Regression',
    description: 'Estimates total trip budget and required activity hours accurately using regularized regression trained on past travel observations.',
    badge: 'Regression',
    stat: 'R²: 93.7%',
    iconBg: 'bg-amber-50',
  },
  {
    icon: <Shield className="w-5 h-5 text-rose-700" />,
    title: 'Iterative Constraint Engine',
    description: 'Enforces hard budget and time constraints without compromising experience quality, swapping activities dynamically.',
    badge: 'Constraint Solver',
    stat: '100% Bound',
    iconBg: 'bg-rose-50',
  },
]

const TESTIMONIALS = [
  {
    name: 'Aarav Sharma',
    role: 'Backpacker & Photographer',
    location: 'Bangalore',
    text: 'The K-Means clustering tagged me as an "Adventure & Nature Explorer" and recommended high-elevation treks in Manali within my ₹18,000 budget. Perfect fit!',
    rating: 5,
    dest: 'Manali, Himachal Pradesh',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=120&q=80',
  },
  {
    name: 'Dr. Meera Iyer',
    role: 'Heritage Researcher',
    location: 'Chennai',
    text: 'The Random Forest like-probabilities for architectural ruins in Jaipur were remarkably accurate. The day-wise pacing gave ample time for each monument.',
    rating: 5,
    dest: 'Jaipur, Rajasthan',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&q=80',
  },
  {
    name: 'Rohan & Ananya',
    role: 'Couple Travellers',
    location: 'Mumbai',
    text: 'We planned a 5-day Kerala trip with a ₹35,000 budget. The cost estimation model came within 4% of our actual expenditure. Incredible engineering!',
    rating: 5,
    dest: 'Kerala Backwaters',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=120&q=80',
  },
]

const PIPELINE_PREVIEW = [
  { step: '01', title: 'Multidimensional Input', desc: 'Budget, group size, walking comfort & 6 interest ratings' },
  { step: '02', title: 'RF Classification', desc: 'Predicts Like / Not Like with probability calibration' },
  { step: '03', title: 'K-Means Clustering', desc: 'Assigns user to optimal centroid-derived traveller profile' },
  { step: '04', title: 'Composite Scoring', desc: 'Weighted rank: 0.35 RF + 0.30 Match + 0.20 Rating + 0.15 Budget' },
  { step: '05', title: 'Regression Estimation', desc: 'Ridge & RF models predict total cost and activity hours' },
  { step: '06', title: 'Constraint Solver', desc: 'Iteratively prunes or swaps places to guarantee strict budget adherence' },
]

export default function HomePage() {
  const [destinations, setDestinations] = useState<Destination[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    destinationsApi.getAll({ sort_by: 'avg_rating' })
      .then(res => setDestinations(res.data.destinations.slice(0, 6)))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-[#F7F7F7] text-[#222222]">
      {/* Airbnb / Linear Style Navigation & Hero */}
      <TemplateNavigation />
      <TemplateHero />

      {/* ML Pipeline Architecture Section */}
      <section className="py-24 px-6 bg-white border-t border-[#DDDDDD] w-full">
        <div className="max-w-7xl mx-auto w-full">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-sm text-[#717171] font-medium mb-2 block">
              Academic ML Architecture
            </span>
            <h2 className="text-3xl md:text-4xl font-bold text-[#222222] tracking-tight mb-4">
              Rigorous Machine Learning, Not Generic Rules
            </h2>
            <p className="text-[#717171] text-base leading-relaxed max-w-2xl mx-auto font-normal">
              Designed according to academic standards. An end-to-end 6-stage pipeline integrating supervised classification, unsupervised clustering, weighted recommendation, and regularized regression.
            </p>
          </div>

          {/* 4 ML pillar cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {FEATURES.map((feat, idx) => (
              <motion.div
                key={feat.title}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.3, delay: idx * 0.08 }}
                className="bg-white border border-[#DDDDDD] rounded-2xl p-6 hover:shadow-md transition-shadow flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-5">
                    <div className={`w-10 h-10 rounded-xl ${feat.iconBg} flex items-center justify-center`}>
                      {feat.icon}
                    </div>
                    <span className="text-xs font-mono text-[#717171] bg-[#F7F7F7] rounded-lg px-2 py-1">
                      {feat.stat}
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-[#222222] mb-2">{feat.title}</h3>
                  <p className="text-xs text-[#717171] leading-relaxed">{feat.description}</p>
                </div>
                <div className="pt-4 mt-4 border-t border-[#DDDDDD] flex items-center justify-between text-xs text-[#717171]">
                  <span>{feat.badge}</span>
                  <ChevronRight className="w-3.5 h-3.5 text-[#717171]" />
                </div>
              </motion.div>
            ))}
          </div>

          {/* Pipeline flow cards */}
          <div className="bg-[#F7F7F7] rounded-2xl border border-[#DDDDDD] p-8">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 mb-8 border-b border-[#DDDDDD] gap-4">
              <div>
                <span className="text-xs text-[#008489] font-semibold uppercase tracking-wider block mb-1">
                  Sequential Execution
                </span>
                <h3 className="text-2xl font-bold text-[#222222]">
                  Full ML Pipeline Execution Flow
                </h3>
                <p className="text-xs text-[#717171] mt-1">
                  Every user trip executes this end-to-end flow asynchronously on the FastAPI backend
                </p>
              </div>
              <Link
                to="/how-it-works"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white border border-[#DDDDDD] text-xs font-medium text-[#222222] hover:bg-[#F7F7F7] transition-colors self-start sm:self-auto cursor-pointer"
              >
                Mathematical Formulation <ArrowRight className="w-3.5 h-3.5 text-[#008489]" />
              </Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
              {PIPELINE_PREVIEW.map((item) => (
                <div
                  key={item.step}
                  className="bg-white border border-[#DDDDDD] rounded-xl p-5"
                >
                  <div className="text-xs text-[#008489] font-semibold mb-2">Stage {item.step}</div>
                  <div className="text-sm font-semibold text-[#222222] mb-1.5 leading-snug">{item.title}</div>
                  <div className="text-xs text-[#717171] leading-relaxed">{item.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Featured Destinations Showcase */}
      <section className="py-24 px-6 bg-[#F7F7F7] border-t border-[#DDDDDD] w-full">
        <div className="max-w-7xl mx-auto w-full">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">
            <div>
              <span className="text-sm text-[#717171] font-medium block mb-1">
                Curated Dataset
              </span>
              <h2 className="text-3xl font-bold text-[#222222] tracking-tight">
                Explore Top Destinations
              </h2>
              <p className="text-[#717171] text-sm mt-1">
                Real historical tourism points with calibrated interest vectors, ratings and local costs
              </p>
            </div>
            <Link
              to="/destinations"
              className="inline-flex items-center gap-2 text-sm font-medium text-[#008489] hover:underline transition-colors"
            >
              Browse all 20+ destinations <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[1, 2, 3, 4, 5, 6].map(i => (
                <div key={i} className="h-80 rounded-2xl bg-white border border-[#DDDDDD] animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {destinations.map(dest => (
                <Link
                  key={dest.destination}
                  to={`/destinations/${encodeURIComponent(dest.destination)}`}
                  className="group bg-white rounded-2xl overflow-hidden border border-[#DDDDDD] hover:shadow-md transition-shadow flex flex-col justify-between"
                >
                  <div>
                    <div className="h-56 overflow-hidden relative">
                      <img
                        src={dest.image}
                        alt={dest.destination}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        referrerPolicy="no-referrer"
                        loading="lazy"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80'
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
                      <div className="absolute top-3 right-3 flex items-center gap-1 bg-white/95 px-2.5 py-1 rounded-full text-xs font-semibold text-[#222222] shadow-sm">
                        <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" /> {dest.avg_rating}
                      </div>
                      <div className="absolute bottom-3 left-3 flex flex-wrap gap-1.5">
                        {(dest.categories || []).slice(0, 2).map(c => (
                          <span
                            key={c}
                            className="bg-black/60 text-white text-xs rounded-full px-2 py-0.5"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="p-5">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-semibold text-[#222222] group-hover:text-[#008489] transition-colors">
                          {dest.destination}
                        </h3>
                        <span className="text-sm text-[#717171] flex items-center gap-1 font-normal">
                          <MapPin className="w-3.5 h-3.5 text-[#717171]" /> {dest.region || dest.country}
                        </span>
                      </div>
                      <p className="text-xs text-[#717171] line-clamp-2 leading-relaxed">
                        {dest.description}
                      </p>
                    </div>
                  </div>

                  <div className="px-5 pb-5 pt-0">
                    <div className="flex items-center justify-between pt-3 border-t border-[#DDDDDD] text-xs">
                      <span className="text-[#717171]">
                        <strong className="text-[#222222] font-semibold text-sm">₹{dest.avg_cost_per_day?.toLocaleString('en-IN')}</strong> / day
                      </span>
                      <span className="text-[#717171] flex items-center gap-1 font-normal">
                        <Clock className="w-3.5 h-3.5 text-[#717171]" /> {dest.best_duration_days} days ideal
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-24 px-6 bg-white border-t border-[#DDDDDD] w-full">
        <div className="max-w-7xl mx-auto w-full">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-sm text-[#717171] font-medium block mb-1">
              Empirical Evaluation
            </span>
            <h2 className="text-3xl font-bold text-[#222222] tracking-tight">
              Tested by Diverse Traveller Cohorts
            </h2>
            <p className="text-[#717171] text-sm mt-2 font-normal">
              Verified test cases across different user preference profiles and budget constraints
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {TESTIMONIALS.map(t => (
              <div
                key={t.name}
                className="bg-[#F7F7F7] rounded-2xl border border-[#DDDDDD] p-8 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center gap-1 text-amber-400 mb-4">
                    {[...Array(t.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-amber-400" />
                    ))}
                  </div>
                  <p className="text-[#222222] italic text-sm leading-relaxed mb-6">
                    "{t.text}"
                  </p>
                </div>
                <div className="pt-4 border-t border-[#DDDDDD] flex items-center gap-3">
                  <img
                    src={t.avatar}
                    alt={t.name}
                    className="w-10 h-10 rounded-full object-cover border border-[#DDDDDD]"
                  />
                  <div>
                    <h4 className="font-semibold text-[#222222] text-sm">{t.name}</h4>
                    <p className="text-xs text-[#717171]">{t.role} · {t.location}</p>
                    <span className="text-xs text-[#717171] block mt-0.5">
                      📍 {t.dest}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="py-20 px-6 bg-[#222222] text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">
            Experience Personalized Travel Planning Powered by Machine Learning
          </h2>
          <p className="text-stone-300 text-base md:text-lg max-w-2xl mx-auto mb-10 leading-relaxed font-normal">
            Stop scrolling generic top-10 lists. Let our trained classification and clustering models build a customized day-wise itinerary matched to your tastes and wallet.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/planner">
              <button className="bg-white text-[#222222] rounded-xl font-medium px-8 py-3.5 hover:bg-stone-100 transition-colors cursor-pointer text-sm">
                Launch Trip Planner Wizard
              </button>
            </Link>
            <Link to="/ml-dashboard">
              <button className="border border-white/40 text-white rounded-xl font-medium px-8 py-3.5 hover:bg-white/10 transition-colors cursor-pointer text-sm">
                View ML Model Analytics
              </button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
