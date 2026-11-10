import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  MapPin, Wallet, Calendar, Users, ArrowRight, ArrowLeft,
  Check, Compass, Shield, Clock, Utensils, Hotel, Car,
  Footprints, Info, Star
} from 'lucide-react'
import { toast } from 'sonner'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import { destinationsApi, tripsApi, type Destination, type TripGenerateRequest } from '@/services/api'

const INTEREST_FIELDS = [
  { id: 'nature_interest', label: 'Nature & Scenery', icon: '🌿', desc: 'Mountains, lakes, forests & waterfalls', tag: 'Landscape' },
  { id: 'adventure_interest', label: 'Outdoor Adventure', icon: '🏔️', desc: 'Trekking, sports, rafting & expeditions', tag: 'Adrenaline' },
  { id: 'food_interest', label: 'Culinary & Dining', icon: '🍜', desc: 'Local delicacies, street food & fine dining', tag: 'Gastronomy' },
  { id: 'history_interest', label: 'History & Heritage', icon: '🏛️', desc: 'Palaces, forts, monuments & archaeology', tag: 'Architecture' },
  { id: 'shopping_interest', label: 'Markets & Shopping', icon: '🛍️', desc: 'Bazaars, handicrafts, textiles & souvenirs', tag: 'Local Crafts' },
  { id: 'culture_interest', label: 'Culture & Arts', icon: '🎭', desc: 'Festivals, performances, spiritual & temples', tag: 'Tradition' },
]

const RATING_LABELS: Record<number, string> = {
  1: 'Low Interest',
  2: 'Slight Preference',
  3: 'Moderate Interest',
  4: 'High Priority',
  5: 'Must-Have / Essential',
}

const LOADING_STAGES = [
  { title: 'Feature Vectorization', desc: 'Normalizing 6 interest coordinates and user budget to zero-mean standard scale...' },
  { title: 'K-Means Clustering', desc: 'Computing euclidean distances to 4 cluster centroids to identify your traveller archetype...' },
  { title: 'Random Forest Inference', desc: 'Evaluating 111 candidate attractions with calibrated like-probabilities P(Like=1)...' },
  { title: 'Composite Scoring', desc: 'Calculating weighted scores: 0.35 RF + 0.30 Match + 0.20 Rating + 0.15 Budget Fit...' },
  { title: 'Regression Estimation', desc: 'Running trained Ridge & Random Forest regressors to estimate hotel, food & transport costs...' },
  { title: 'Constraint Solver', desc: 'Iteratively validating budget ceilings and daily 8-hour activity limits...' },
  { title: 'Structuring Day-Wise Schedule', desc: 'Assembling optimal morning, afternoon, and evening itinerary...' },
]

export default function PlannerPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const preselectedDest = searchParams.get('destination')

  const [step, setStep] = useState(1)
  const [destinations, setDestinations] = useState<Destination[]>([])
  const [destSearch, setDestSearch] = useState('')
  const [selectedRegionFilter, setSelectedRegionFilter] = useState('All')
  const [loadingDestinations, setLoadingDestinations] = useState(true)

  // Form state
  const [formData, setFormData] = useState<TripGenerateRequest>({
    destination: preselectedDest || '',
    budget: 25000,
    days: 4,
    group_size: 2,
    food_preference: 'No Preference',
    nature_interest: 4,
    adventure_interest: 3,
    food_interest: 4,
    history_interest: 3,
    shopping_interest: 2,
    culture_interest: 3,
    walking_comfort: 'Medium',
    accommodation_type: 'Standard',
    transport_preference: 'Mixed',
    trip_pace: 'Balanced',
    group_type: 'Friends',
    additional_notes: '',
  })

  // ML Execution loading state
  const [isGenerating, setIsGenerating] = useState(false)
  const [currentStageIdx, setCurrentStageIdx] = useState(0)

  useEffect(() => {
    destinationsApi.getAll()
      .then(res => {
        setDestinations(res.data.destinations)
        if (preselectedDest) {
          const match = res.data.destinations.find(
            d => d.destination.toLowerCase() === preselectedDest.toLowerCase()
          )
          if (match) {
            setFormData(prev => ({ ...prev, destination: match.destination }))
          }
        }
      })
      .catch(() => toast.error('Could not load destinations list'))
      .finally(() => setLoadingDestinations(false))
  }, [preselectedDest])

  const filteredDestinations = destinations.filter(d => {
    const matchesSearch =
      d.destination.toLowerCase().includes(destSearch.toLowerCase()) ||
      d.country.toLowerCase().includes(destSearch.toLowerCase()) ||
      (d.region && d.region.toLowerCase().includes(destSearch.toLowerCase()))

    if (selectedRegionFilter === 'All') return matchesSearch
    return matchesSearch && d.categories?.includes(selectedRegionFilter)
  })

  const handleNext = () => {
    if (step === 1 && !formData.destination) {
      toast.error('Please select a destination to continue')
      return
    }
    if (step === 2) {
      if (formData.budget < 3000) {
        toast.error('Please enter a realistic total budget (minimum ₹3,000)')
        return
      }
      if (formData.days < 1 || formData.days > 14) {
        toast.error('Trip duration must be between 1 and 14 days')
        return
      }
      if (formData.group_size < 1) {
        toast.error('Group size must be at least 1 person')
        return
      }
    }
    setStep(prev => Math.min(prev + 1, 6))
    window.scrollTo({ top: 100, behavior: 'smooth' })
  }

  const handleBack = () => {
    setStep(prev => Math.max(prev - 1, 1))
    window.scrollTo({ top: 100, behavior: 'smooth' })
  }

  const handleGenerate = async () => {
    setIsGenerating(true)
    setCurrentStageIdx(0)

    const interval = setInterval(() => {
      setCurrentStageIdx(prev => {
        if (prev < LOADING_STAGES.length - 1) {
          return prev + 1
        }
        return prev
      })
    }, 600)

    try {
      const response = await tripsApi.generate(formData)
      clearInterval(interval)
      toast.success('Itinerary generated successfully by ML Pipeline!')
      if (response.data.trip_id) {
        navigate(`/trips/${response.data.trip_id}`)
      } else {
        toast.error('Trip ID missing from response')
      }
    } catch (err: unknown) {
      clearInterval(interval)
      setIsGenerating(false)
      const errMessage =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        'ML execution failed. Please verify that the backend server is running.'
      toast.error(errMessage)
    }
  }

  const costPerPersonPerDay = Math.round(
    formData.budget / Math.max(1, formData.days) / Math.max(1, formData.group_size)
  )

  const stepsConfig = [
    { s: 1, label: 'Destination' },
    { s: 2, label: 'Budget & Days' },
    { s: 3, label: 'Interests' },
    { s: 4, label: 'Travel Style' },
    { s: 5, label: 'Group & Pace' },
    { s: 6, label: 'Review & Run' },
  ]

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        {/* Hero Section */}
        <div className="pt-32 pb-8 px-6 text-center max-w-4xl mx-auto">
          <h1 className="text-3xl sm:text-4xl font-bold text-[#222222] tracking-tight mb-3">
            Design Your Personalized Journey
          </h1>
          <p className="text-base text-[#717171] max-w-2xl mx-auto leading-relaxed">
            Specify your destination, budget, and 6-factor interest ratings. Our machine learning pipeline will infer your preferences and calculate an optimal day-wise itinerary.
          </p>
        </div>

        {/* Stepper Progress Bar */}
        <div className="max-w-4xl mx-auto px-6 mb-10">
          <div className="bg-white p-4 rounded-2xl border border-[#DDDDDD] shadow-sm">
            <div className="grid grid-cols-6 gap-2 mb-3 text-center text-xs">
              {stepsConfig.map(item => {
                const isActive = step === item.s
                const isCompleted = step > item.s
                return (
                  <button
                    key={item.s}
                    onClick={() => item.s < step && setStep(item.s)}
                    disabled={item.s > step}
                    className={`flex flex-col items-center gap-1.5 transition-colors cursor-pointer ${
                      isActive
                        ? 'text-[#222222] font-semibold'
                        : isCompleted
                        ? 'text-[#008489]'
                        : 'text-[#717171]'
                    }`}
                  >
                    <span
                      className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium transition-all ${
                        isActive
                          ? 'bg-[#222222] text-white'
                          : isCompleted
                          ? 'bg-[#008489] text-white'
                          : 'bg-[#F7F7F7] text-[#717171] border border-[#DDDDDD]'
                      }`}
                    >
                      {isCompleted ? '✓' : item.s}
                    </span>
                    <span className="hidden sm:inline text-[11px] truncate w-full">
                      {item.label}
                    </span>
                  </button>
                )
              })}
            </div>
            <div className="w-full h-1.5 rounded-full bg-stone-100 overflow-hidden">
              <motion.div
                className="h-full bg-[#222222]"
                initial={{ width: '16%' }}
                animate={{ width: `${(step / 6) * 100}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
        </div>

        {/* Wizard Main Card */}
        <div className="max-w-4xl mx-auto px-6 pb-20">
          <div className="bg-white rounded-2xl border border-[#DDDDDD] p-8 sm:p-10 shadow-sm relative overflow-hidden">
            <AnimatePresence mode="wait">
              {/* STEP 1: DESTINATION SELECTION */}
              {step === 1 && (
                <motion.div
                  key="step1"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="space-y-6"
                >
                  <div className="border-b border-[#DDDDDD] pb-5">
                    <span className="text-xs text-[#717171] font-medium mb-1 block">
                      Step 1 of 6
                    </span>
                    <h2 className="text-2xl font-bold text-[#222222]">
                      Where would you like to travel?
                    </h2>
                    <p className="text-sm text-[#717171] mt-1">
                      Select a destination from our curated, ML-calibrated dataset of 20+ premier Indian locations.
                    </p>
                  </div>

                  {/* Search and Category Filter Strip */}
                  <div className="flex flex-col sm:flex-row gap-3">
                    <div className="relative flex-1">
                      <input
                        type="text"
                        placeholder="Search by city, state, or keywords (e.g., Goa, Manali, Kerala)..."
                        value={destSearch}
                        onChange={e => setDestSearch(e.target.value)}
                        className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-[#DDDDDD] text-sm text-[#222222] placeholder:text-[#717171] focus:outline-none focus:border-[#222222] bg-white"
                      />
                      <MapPin className="w-4 h-4 text-[#717171] absolute left-3.5 top-1/2 -translate-y-1/2" />
                    </div>

                    <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
                      {['All', 'Nature', 'Adventure', 'History', 'Culture'].map(cat => {
                        const isActive = selectedRegionFilter === cat
                        return (
                          <button
                            key={cat}
                            type="button"
                            onClick={() => setSelectedRegionFilter(cat)}
                            className={`px-3.5 py-2 rounded-xl text-xs font-medium whitespace-nowrap transition-all cursor-pointer ${
                              isActive
                                ? 'bg-[#222222] text-white'
                                : 'border border-[#DDDDDD] bg-white text-[#222222] hover:bg-[#F7F7F7]'
                            }`}
                          >
                            {cat}
                          </button>
                        )
                      })}
                    </div>
                  </div>

                  {/* Destination Grid */}
                  {loadingDestinations ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                      {[1, 2, 3, 4, 5, 6].map(i => (
                        <div key={i} className="h-44 rounded-xl bg-stone-100 animate-pulse border border-[#DDDDDD]" />
                      ))}
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 max-h-[460px] overflow-y-auto p-1 pr-2">
                      {filteredDestinations.map(d => {
                        const isSelected = formData.destination.toLowerCase() === d.destination.toLowerCase()
                        return (
                          <div
                            key={d.destination}
                            onClick={() => setFormData({ ...formData, destination: d.destination })}
                            className={`group relative rounded-xl overflow-hidden cursor-pointer transition-all duration-200 text-left p-3.5 flex flex-col justify-between ${
                              isSelected
                                ? 'border-2 border-[#222222] bg-[#F7F7F7]'
                                : 'border border-[#DDDDDD] bg-white hover:border-[#222222]/30'
                            }`}
                          >
                            <div className="relative h-28 rounded-lg overflow-hidden mb-3 bg-stone-100">
                              <img
                                src={d.image}
                                alt={d.destination}
                                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                referrerPolicy="no-referrer"
                                loading="lazy"
                                onError={(e) => {
                                  (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=500&q=80'
                                }}
                              />
                              <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
                              <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-md px-2 py-0.5 rounded-md text-[10px] font-semibold text-[#222222] flex items-center gap-1 shadow-xs">
                                <Star className="w-3 h-3 fill-amber-400 text-amber-400" /> {d.avg_rating}
                              </div>
                              {isSelected && (
                                <div className="absolute top-2 left-2 bg-[#222222] text-white p-1 rounded-full shadow-sm">
                                  <Check className="w-3.5 h-3.5" />
                                </div>
                              )}
                              <div className="absolute bottom-2 left-2 text-white">
                                <span className="text-[10px] text-stone-200 block">
                                  {d.region || d.country}
                                </span>
                              </div>
                            </div>

                            <div>
                              <h4 className="font-semibold text-[#222222] text-sm">
                                {d.destination}
                              </h4>
                              <p className="text-xs text-[#717171] line-clamp-1 mt-0.5">
                                {d.description}
                              </p>
                              <div className="flex items-center justify-between pt-2.5 mt-2 border-t border-[#DDDDDD] text-xs">
                                <span className="font-medium text-[#222222]">
                                  ₹{d.avg_cost_per_day?.toLocaleString('en-IN')} / day
                                </span>
                                <span className="text-[#717171]">
                                  {d.best_duration_days}d ideal
                                </span>
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  )}

                  {formData.destination && (
                    <div className="bg-[#F7F7F7] border border-[#DDDDDD] rounded-xl p-4 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-[#222222] text-white flex items-center justify-center font-semibold text-sm">
                          ✓
                        </div>
                        <div>
                          <span className="text-[#717171] text-xs block">Selected Destination</span>
                          <span className="font-semibold text-[#222222] text-base">{formData.destination}</span>
                        </div>
                      </div>
                      <span className="text-[#717171] text-xs bg-white border border-[#DDDDDD] px-3 py-1.5 rounded-lg">
                        Ready for Step 2
                      </span>
                    </div>
                  )}
                </motion.div>
              )}

              {/* STEP 2: BUDGET & DURATION */}
              {step === 2 && (
                <motion.div
                  key="step2"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="space-y-6"
                >
                  <div className="border-b border-[#DDDDDD] pb-5">
                    <span className="text-xs text-[#717171] font-medium mb-1 block">
                      Step 2 of 6
                    </span>
                    <h2 className="text-2xl font-bold text-[#222222]">
                      Budget, Duration & Travellers
                    </h2>
                    <p className="text-sm text-[#717171] mt-1">
                      Our regression and constraint engine uses these numbers to bound place recommendations.
                    </p>
                  </div>

                  {/* Real-time calculated budget insight card - clean white/off-white */}
                  <div className="bg-[#F7F7F7] border border-[#DDDDDD] rounded-xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div>
                      <span className="text-xs text-[#717171] font-medium block mb-1">
                        Live Calculated Allowance
                      </span>
                      <div className="text-2xl sm:text-3xl font-bold text-[#222222] font-mono">
                        ₹{costPerPersonPerDay.toLocaleString('en-IN')}{' '}
                        <span className="text-sm font-normal text-[#717171]">/ person / day</span>
                      </div>
                      <p className="text-xs text-[#717171] mt-1">
                        Covers accommodation, local transport, dining, and attraction entries.
                      </p>
                    </div>
                    <div className="text-xs text-[#717171] bg-white border border-[#DDDDDD] rounded-lg px-3 py-1 font-medium">
                      {costPerPersonPerDay < 2000
                        ? '🎒 Budget Backpacker Tier'
                        : costPerPersonPerDay < 5000
                        ? '🌟 Balanced Comfort Tier'
                        : '💎 Premium Luxury Tier'}
                    </div>
                  </div>

                  {/* Budget Input & Slider */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2">
                        <Wallet className="w-4 h-4 text-[#717171]" /> Total Trip Budget (INR)
                      </label>
                      <span className="text-xl font-bold text-[#222222] font-mono">
                        ₹{formData.budget.toLocaleString('en-IN')}
                      </span>
                    </div>

                    <input
                      type="range"
                      min={5000}
                      max={200000}
                      step={2500}
                      value={formData.budget}
                      onChange={e => setFormData({ ...formData, budget: Number(e.target.value) })}
                      className="w-full accent-[#222222] h-2 bg-stone-200 rounded-lg cursor-pointer"
                    />

                    {/* Quick Budget Presets */}
                    <div className="flex flex-wrap gap-2 pt-1">
                      {[
                        { label: '₹15,000 (Budget)', val: 15000 },
                        { label: '₹30,000 (Comfort)', val: 30000 },
                        { label: '₹60,000 (Premium)', val: 60000 },
                        { label: '₹1,20,000 (Luxury)', val: 120000 },
                      ].map(preset => {
                        const isActive = formData.budget === preset.val
                        return (
                          <button
                            key={preset.val}
                            type="button"
                            onClick={() => setFormData({ ...formData, budget: preset.val })}
                            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer ${
                              isActive
                                ? 'bg-[#222222] text-white'
                                : 'bg-white border border-[#DDDDDD] text-[#222222] hover:bg-[#F7F7F7]'
                            }`}
                          >
                            {preset.label}
                          </button>
                        )
                      })}
                    </div>
                  </div>

                  {/* Days & Group Size Dual Grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-4 border-t border-[#DDDDDD]">
                    {/* Duration in Days */}
                    <div className="space-y-3">
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-[#717171]" /> Travel Duration
                      </label>
                      <div className="flex items-center gap-3">
                        <button
                          type="button"
                          onClick={() => setFormData(prev => ({ ...prev, days: Math.max(1, prev.days - 1) }))}
                          className="w-11 h-11 bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] rounded-xl hover:bg-stone-100 font-semibold text-lg flex items-center justify-center transition-colors cursor-pointer"
                        >
                          -
                        </button>
                        <div className="flex-1 py-2.5 px-4 rounded-xl border border-[#DDDDDD] bg-white text-center font-semibold text-base text-[#222222]">
                          {formData.days} {formData.days === 1 ? 'Day' : 'Days'}
                        </div>
                        <button
                          type="button"
                          onClick={() => setFormData(prev => ({ ...prev, days: Math.min(14, prev.days + 1) }))}
                          className="w-11 h-11 bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] rounded-xl hover:bg-stone-100 font-semibold text-lg flex items-center justify-center transition-colors cursor-pointer"
                        >
                          +
                        </button>
                      </div>
                      <div className="flex gap-2">
                        {[2, 3, 5, 7].map(d => (
                          <button
                            key={d}
                            type="button"
                            onClick={() => setFormData({ ...formData, days: d })}
                            className={`flex-1 py-1 rounded-lg text-xs font-medium cursor-pointer transition-colors ${
                              formData.days === d
                                ? 'bg-[#222222] text-white'
                                : 'bg-white border border-[#DDDDDD] text-[#717171] hover:bg-[#F7F7F7]'
                            }`}
                          >
                            {d}d
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Group Size */}
                    <div className="space-y-3">
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2">
                        <Users className="w-4 h-4 text-[#717171]" /> Number of Travellers
                      </label>
                      <div className="flex items-center gap-3">
                        <button
                          type="button"
                          onClick={() => setFormData(prev => ({ ...prev, group_size: Math.max(1, prev.group_size - 1) }))}
                          className="w-11 h-11 bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] rounded-xl hover:bg-stone-100 font-semibold text-lg flex items-center justify-center transition-colors cursor-pointer"
                        >
                          -
                        </button>
                        <div className="flex-1 py-2.5 px-4 rounded-xl border border-[#DDDDDD] bg-white text-center font-semibold text-base text-[#222222]">
                          {formData.group_size} {formData.group_size === 1 ? 'Person' : 'People'}
                        </div>
                        <button
                          type="button"
                          onClick={() => setFormData(prev => ({ ...prev, group_size: Math.min(12, prev.group_size + 1) }))}
                          className="w-11 h-11 bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] rounded-xl hover:bg-stone-100 font-semibold text-lg flex items-center justify-center transition-colors cursor-pointer"
                        >
                          +
                        </button>
                      </div>
                      <div className="flex gap-2">
                        {[1, 2, 4, 6].map(g => (
                          <button
                            key={g}
                            type="button"
                            onClick={() => setFormData({ ...formData, group_size: g })}
                            className={`flex-1 py-1 rounded-lg text-xs font-medium cursor-pointer transition-colors ${
                              formData.group_size === g
                                ? 'bg-[#222222] text-white'
                                : 'bg-white border border-[#DDDDDD] text-[#717171] hover:bg-[#F7F7F7]'
                            }`}
                          >
                            {g === 1 ? 'Solo' : `${g}p`}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* STEP 3: 6 INTERESTS RATINGS */}
              {step === 3 && (
                <motion.div
                  key="step3"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="space-y-6"
                >
                  <div className="border-b border-[#DDDDDD] pb-5">
                    <span className="text-xs text-[#717171] font-medium mb-1 block">
                      Step 3 of 6
                    </span>
                    <h2 className="text-2xl font-bold text-[#222222]">
                      Rate Your Travel Interests (1 to 5)
                    </h2>
                    <p className="text-sm text-[#717171] mt-1">
                      These 6 dimensions feed directly into our K-Means archetype clusterer and Random Forest classifier.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {INTEREST_FIELDS.map(field => {
                      const currentVal = (formData as any)[field.id] as number
                      return (
                        <div
                          key={field.id}
                          className="bg-[#F7F7F7] border border-[#DDDDDD] rounded-xl p-5 hover:border-[#222222]/30 transition-all flex flex-col justify-between"
                        >
                          <div>
                            <div className="flex items-center justify-between mb-1.5">
                              <div className="flex items-center gap-2">
                                <span className="text-xl">{field.icon}</span>
                                <h4 className="font-semibold text-[#222222] text-sm">{field.label}</h4>
                              </div>
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-white border border-[#DDDDDD] text-[#717171]">
                                {field.tag}
                              </span>
                            </div>
                            <p className="text-xs text-[#717171] mb-3">{field.desc}</p>
                          </div>

                          <div>
                            <div className="flex items-center justify-between mb-2 text-xs">
                              <span className="text-[#717171]">Rating:</span>
                              <span className="text-[#008489] font-medium">
                                {currentVal} / 5 · {RATING_LABELS[currentVal]}
                              </span>
                            </div>

                            <div className="grid grid-cols-5 gap-1.5">
                              {[1, 2, 3, 4, 5].map(star => {
                                const isSelected = currentVal >= star
                                return (
                                  <button
                                    key={star}
                                    type="button"
                                    onClick={() => setFormData({ ...formData, [field.id]: star })}
                                    className={`py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer flex items-center justify-center gap-1 ${
                                      isSelected
                                        ? 'bg-[#222222] text-white'
                                        : 'bg-white border border-[#DDDDDD] text-[#717171] hover:border-[#222222]/30'
                                    }`}
                                  >
                                    <Star className={`w-3 h-3 ${isSelected ? 'fill-white' : ''}`} />
                                    <span>{star}</span>
                                  </button>
                                )
                              })}
                            </div>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </motion.div>
              )}

              {/* STEP 4: PREFERENCES & TRAVEL STYLE */}
              {step === 4 && (
                <motion.div
                  key="step4"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="space-y-6"
                >
                  <div className="border-b border-[#DDDDDD] pb-5">
                    <span className="text-xs text-[#717171] font-medium mb-1 block">
                      Step 4 of 6
                    </span>
                    <h2 className="text-2xl font-bold text-[#222222]">
                      Travel Style & Comfort Preferences
                    </h2>
                    <p className="text-sm text-[#717171] mt-1">
                      Calibrates accommodation cost models, walking intensity, and dining recommendations.
                    </p>
                  </div>

                  <div className="space-y-5">
                    {/* Food Preference */}
                    <div>
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2 mb-2.5">
                        <Utensils className="w-4 h-4 text-[#717171]" /> Dining & Dietary Preference
                      </label>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        {['Vegetarian', 'Non-Vegetarian', 'Vegan', 'No Preference'].map(opt => {
                          const isActive = formData.food_preference === opt
                          return (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => setFormData({ ...formData, food_preference: opt })}
                              className={`p-3.5 rounded-xl text-xs font-medium transition-all text-center cursor-pointer ${
                                isActive
                                  ? 'border-2 border-[#222222] bg-[#F7F7F7] text-[#222222]'
                                  : 'border border-[#DDDDDD] bg-white text-[#717171] hover:border-[#222222]/30'
                              }`}
                            >
                              {opt}
                            </button>
                          )
                        })}
                      </div>
                    </div>

                    {/* Walking Comfort */}
                    <div>
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2 mb-2.5">
                        <Footprints className="w-4 h-4 text-[#717171]" /> Walking & Mobility Comfort
                      </label>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {[
                          { val: 'Low', title: 'Leisurely / Minimal', sub: 'Cabs preferred, light walking only' },
                          { val: 'Medium', title: 'Moderate Stroller', sub: 'Standard walking tours & bazaars' },
                          { val: 'High', title: 'Active Explorer', sub: 'Hikes, long treks & continuous walks' },
                        ].map(opt => {
                          const isActive = formData.walking_comfort === opt.val
                          return (
                            <button
                              key={opt.val}
                              type="button"
                              onClick={() => setFormData({ ...formData, walking_comfort: opt.val })}
                              className={`p-4 rounded-xl text-left transition-all cursor-pointer ${
                                isActive
                                  ? 'border-2 border-[#222222] bg-[#F7F7F7] text-[#222222]'
                                  : 'border border-[#DDDDDD] bg-white text-[#717171] hover:border-[#222222]/30'
                              }`}
                            >
                              <div className="font-semibold text-xs text-[#222222] mb-0.5">{opt.title}</div>
                              <div className="text-[11px] text-[#717171]">{opt.sub}</div>
                            </button>
                          )
                        })}
                      </div>
                    </div>

                    {/* Accommodation Type */}
                    <div>
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2 mb-2.5">
                        <Hotel className="w-4 h-4 text-[#717171]" /> Accommodation Preference
                      </label>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {[
                          { val: 'Budget', title: 'Budget & Hostels', sub: '₹800 - ₹1,800/night' },
                          { val: 'Standard', title: 'Standard 3-4★', sub: '₹2,500 - ₹5,000/night' },
                          { val: 'Luxury', title: 'Luxury 5★ Resort', sub: '₹7,500+/night' },
                        ].map(opt => {
                          const isActive = formData.accommodation_type === opt.val
                          return (
                            <button
                              key={opt.val}
                              type="button"
                              onClick={() => setFormData({ ...formData, accommodation_type: opt.val })}
                              className={`p-4 rounded-xl text-left transition-all cursor-pointer ${
                                isActive
                                  ? 'border-2 border-[#222222] bg-[#F7F7F7] text-[#222222]'
                                  : 'border border-[#DDDDDD] bg-white text-[#717171] hover:border-[#222222]/30'
                              }`}
                            >
                              <div className="font-semibold text-xs text-[#222222] mb-0.5">{opt.title}</div>
                              <div className="text-[11px] text-[#717171]">{opt.sub}</div>
                            </button>
                          )
                        })}
                      </div>
                    </div>

                    {/* Transport Preference */}
                    <div>
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2 mb-2.5">
                        <Car className="w-4 h-4 text-[#717171]" /> Local Transportation Mode
                      </label>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        {['Public Transport', 'Cab', 'Rental', 'Mixed'].map(opt => {
                          const isActive = formData.transport_preference === opt
                          return (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => setFormData({ ...formData, transport_preference: opt })}
                              className={`p-3 rounded-xl text-xs font-medium transition-all text-center cursor-pointer ${
                                isActive
                                  ? 'border-2 border-[#222222] bg-[#F7F7F7] text-[#222222]'
                                  : 'border border-[#DDDDDD] bg-white text-[#717171] hover:border-[#222222]/30'
                              }`}
                            >
                              {opt}
                            </button>
                          )
                        })}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* STEP 5: GROUP TYPE & PACE */}
              {step === 5 && (
                <motion.div
                  key="step5"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="space-y-6"
                >
                  <div className="border-b border-[#DDDDDD] pb-5">
                    <span className="text-xs text-[#717171] font-medium mb-1 block">
                      Step 5 of 6
                    </span>
                    <h2 className="text-2xl font-bold text-[#222222]">
                      Trip Pace & Group Composition
                    </h2>
                    <p className="text-sm text-[#717171] mt-1">
                      Controls the density of activities scheduled per day.
                    </p>
                  </div>

                  <div className="space-y-5">
                    {/* Trip Pace */}
                    <div>
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2 mb-2.5">
                        <Clock className="w-4 h-4 text-[#717171]" /> Daily Itinerary Pace
                      </label>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        {[
                          { val: 'Relaxed', title: 'Relaxed Pace', desc: '1-2 key places/day with leisurely lunches and free evenings' },
                          { val: 'Balanced', title: 'Balanced Pace', desc: '3-4 attractions/day balancing exploration with relaxation' },
                          { val: 'Packed', title: 'Action-Packed', desc: '5+ places/day maximizing sightseeing and photo-ops' },
                        ].map(opt => {
                          const isActive = formData.trip_pace === opt.val
                          return (
                            <button
                              key={opt.val}
                              type="button"
                              onClick={() => setFormData({ ...formData, trip_pace: opt.val })}
                              className={`p-4 rounded-xl text-left transition-all cursor-pointer ${
                                isActive
                                  ? 'border-2 border-[#222222] bg-[#F7F7F7] text-[#222222]'
                                  : 'border border-[#DDDDDD] bg-white text-[#717171] hover:border-[#222222]/30'
                              }`}
                            >
                              <div className="font-semibold text-xs text-[#222222] mb-0.5">{opt.title}</div>
                              <div className="text-xs text-[#717171] leading-relaxed">{opt.desc}</div>
                            </button>
                          )
                        })}
                      </div>
                    </div>

                    {/* Group Type */}
                    <div>
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2 mb-2.5">
                        <Users className="w-4 h-4 text-[#717171]" /> Travel Companion Type
                      </label>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        {['Solo', 'Couple', 'Friends', 'Family'].map(opt => {
                          const isActive = formData.group_type === opt
                          return (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => setFormData({ ...formData, group_type: opt })}
                              className={`p-3.5 rounded-xl text-xs font-medium transition-all text-center cursor-pointer ${
                                isActive
                                  ? 'border-2 border-[#222222] bg-[#F7F7F7] text-[#222222]'
                                  : 'border border-[#DDDDDD] bg-white text-[#717171] hover:border-[#222222]/30'
                              }`}
                            >
                              {opt}
                            </button>
                          )
                        })}
                      </div>
                    </div>

                    {/* Additional Notes */}
                    <div>
                      <label className="text-sm font-semibold text-[#222222] flex items-center gap-2 mb-2">
                        <Info className="w-4 h-4 text-[#717171]" /> Special Requests or Travel Notes (Optional)
                      </label>
                      <textarea
                        rows={3}
                        placeholder="E.g., We love sunset spots, prefer photography viewpoints, celebrating an anniversary..."
                        value={formData.additional_notes || ''}
                        onChange={e => setFormData({ ...formData, additional_notes: e.target.value })}
                        className="w-full px-4 py-2.5 rounded-xl border border-[#DDDDDD] text-sm text-[#222222] placeholder:text-[#717171] focus:outline-none focus:border-[#222222] bg-white"
                      />
                    </div>
                  </div>
                </motion.div>
              )}

              {/* STEP 6: FINAL REVIEW */}
              {step === 6 && (
                <motion.div
                  key="step6"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="space-y-6"
                >
                  <div className="border-b border-[#DDDDDD] pb-5">
                    <span className="text-xs text-[#717171] font-medium mb-1 block">
                      Step 6 of 6 · Final Review
                    </span>
                    <h2 className="text-2xl font-bold text-[#222222]">
                      Ready to Execute the ML Pipeline
                    </h2>
                    <p className="text-sm text-[#717171] mt-1">
                      Review your travel configuration before triggering the backend algorithms.
                    </p>
                  </div>

                  <div className="bg-[#F7F7F7] border border-[#DDDDDD] rounded-xl p-6 sm:p-8 space-y-6">
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pb-6 border-b border-[#DDDDDD]">
                      <div>
                        <span className="text-xs text-[#717171] block mb-1">Destination</span>
                        <div className="text-base font-semibold text-[#222222]">{formData.destination}</div>
                      </div>
                      <div>
                        <span className="text-xs text-[#717171] block mb-1">Duration</span>
                        <div className="text-base font-semibold text-[#222222]">{formData.days} Days</div>
                      </div>
                      <div>
                        <span className="text-xs text-[#717171] block mb-1">Travellers</span>
                        <div className="text-base font-semibold text-[#222222]">{formData.group_size} People ({formData.group_type})</div>
                      </div>
                      <div>
                        <span className="text-xs text-[#717171] block mb-1">Budget Ceiling</span>
                        <div className="text-base font-bold text-[#222222] font-mono">₹{formData.budget.toLocaleString('en-IN')}</div>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-xs font-semibold text-[#717171] mb-3">
                        Configured 6D Interest Profile
                      </h4>
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                        {INTEREST_FIELDS.map(f => (
                          <div key={f.id} className="p-3 rounded-lg bg-white border border-[#DDDDDD] text-xs flex items-center justify-between">
                            <span className="text-[#222222] font-medium">{f.icon} {f.label}</span>
                            <span className="font-semibold text-[#008489]">{(formData as any)[f.id]}/5</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-[#DDDDDD] text-xs">
                      <div>
                        <span className="text-[#717171] block">Food:</span>
                        <strong className="text-[#222222]">{formData.food_preference}</strong>
                      </div>
                      <div>
                        <span className="text-[#717171] block">Walking:</span>
                        <strong className="text-[#222222]">{formData.walking_comfort} Comfort</strong>
                      </div>
                      <div>
                        <span className="text-[#717171] block">Hotel:</span>
                        <strong className="text-[#222222]">{formData.accommodation_type}</strong>
                      </div>
                      <div>
                        <span className="text-[#717171] block">Pace:</span>
                        <strong className="text-[#222222]">{formData.trip_pace}</strong>
                      </div>
                    </div>
                  </div>

                  <div className="bg-[#F7F7F7] border border-[#DDDDDD] rounded-xl p-4 flex items-center gap-3">
                    <Shield className="w-5 h-5 text-[#717171] flex-shrink-0" />
                    <p className="text-xs text-[#717171]">
                      <strong className="text-[#222222]">Academic Model Guarantee:</strong> The generated plan will strictly respect your budget of ₹{formData.budget.toLocaleString('en-IN')} and adhere to maximum 8 daily activity hours using our iterative constraint solver.
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Bottom Navigation Buttons */}
            <div className="flex items-center justify-between pt-6 mt-8 border-t border-[#DDDDDD]">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={handleBack}
                  className="border border-[#DDDDDD] text-[#222222] rounded-xl px-6 py-2.5 text-sm font-medium hover:bg-[#F7F7F7] transition-all flex items-center gap-2 cursor-pointer"
                >
                  <ArrowLeft className="w-4 h-4" /> Back
                </button>
              ) : (
                <div />
              )}

              {step < 6 ? (
                <button
                  type="button"
                  onClick={handleNext}
                  className="bg-[#222222] text-white rounded-xl px-6 py-2.5 text-sm font-medium hover:bg-[#333333] transition-all flex items-center gap-2 cursor-pointer"
                >
                  Continue to Step {step + 1} <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleGenerate}
                  className="bg-[#222222] text-white px-8 py-3.5 rounded-xl text-sm font-semibold hover:bg-[#333333] transition-colors flex items-center justify-center gap-2 cursor-pointer"
                >
                  Generate Intelligent Itinerary →
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* CLEAN ML LOADING MODAL */}
      <AnimatePresence>
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-white/95 backdrop-blur-sm flex items-center justify-center p-6"
          >
            <div className="max-w-md w-full bg-white border border-[#DDDDDD] rounded-2xl p-8 text-center shadow-lg">
              {/* Spinner with Compass */}
              <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center">
                <Compass className="w-10 h-10 text-[#222222] animate-spin" style={{ animationDuration: '3s' }} />
              </div>

              <span className="inline-block text-xs text-[#717171] bg-[#F7F7F7] border border-[#DDDDDD] rounded-full px-3 py-1 mb-3">
                Stage {currentStageIdx + 1} of {LOADING_STAGES.length}
              </span>

              <h3 className="text-lg font-bold text-[#222222] mb-2">
                {LOADING_STAGES[currentStageIdx].title}
              </h3>
              <p className="text-xs text-[#717171] leading-relaxed min-h-[44px] mb-6">
                {LOADING_STAGES[currentStageIdx].desc}
              </p>

              {/* Progress bar */}
              <div className="w-full h-1.5 rounded-full bg-stone-100 overflow-hidden mb-3">
                <motion.div
                  className="h-full bg-[#222222]"
                  initial={{ width: '10%' }}
                  animate={{ width: `${((currentStageIdx + 1) / LOADING_STAGES.length) * 100}%` }}
                  transition={{ duration: 0.4 }}
                />
              </div>

              <div className="flex items-center justify-between text-[11px] font-mono text-[#717171]">
                <span>FastAPI Pipeline Execution</span>
                <span>{Math.round(((currentStageIdx + 1) / LOADING_STAGES.length) * 100)}%</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <Footer />
    </div>
  )
}
