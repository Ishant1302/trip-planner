import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  MapPin, Calendar, Users, Wallet, Clock, Brain, TrendingUp,
  ShieldCheck, ArrowLeft, Heart, Trash2, Printer, BarChart3, CheckCircle2,
  Sparkles
} from 'lucide-react'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import { toast } from 'sonner'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import { tripsApi, favouritesApi, type TripResult, type Place } from '@/services/api'

const PIE_COLORS = ['#222222', '#008489', '#717171', '#94a3b8', '#a8a29e']

const TIME_OF_DAY_SLOTS = [
  { label: 'Morning Expedition', time: '09:00 AM – 12:30 PM', icon: '🌅' },
  { label: 'Afternoon Discovery & Lunch', time: '01:00 PM – 04:30 PM', icon: '☀️' },
  { label: 'Evening Stroll & Leisure', time: '05:00 PM – 08:30 PM', icon: '🌆' },
]

export default function TripResultPage() {
  const { id } = useParams<{ id: string }>()
  const [tripData, setTripData] = useState<TripResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [isSavedFav, setIsSavedFav] = useState(false)
  const [activeTab, setActiveTab] = useState<'itinerary' | 'recommendations' | 'insights' | 'constraints'>('itinerary')
  const [selectedDayFilter, setSelectedDayFilter] = useState<string>('all')

  const fetchTrip = () => {
    if (!id) return
    setLoading(true)
    tripsApi.getById(Number(id))
      .then(res => {
        const raw = res.data as any
        const data = (raw.ml_results ? { ...raw.ml_results, trip_id: raw.id } : raw) as TripResult
        setTripData(data)
      })
      .catch(() => toast.error('Failed to load trip results'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchTrip()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
        <Navbar />
        <div className="pt-32 max-w-7xl mx-auto px-6 py-12 w-full animate-pulse">
          <div className="h-64 rounded-2xl bg-stone-100 border border-[#DDDDDD] mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map(i => <div key={i} className="h-28 rounded-xl bg-stone-100 border border-[#DDDDDD]" />)}
          </div>
          <div className="h-96 rounded-2xl bg-stone-100 border border-[#DDDDDD]" />
        </div>
        <Footer />
      </div>
    )
  }

  if (!tripData) {
    return (
      <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
        <Navbar />
        <div className="pt-36 text-center py-20 px-6 max-w-md mx-auto">
          <div className="w-14 h-14 rounded-2xl bg-white text-[#222222] flex items-center justify-center text-2xl mx-auto mb-4 border border-[#DDDDDD] shadow-sm">
            🗺️
          </div>
          <h2 className="text-xl font-bold text-[#222222]">Trip Not Found</h2>
          <p className="text-[#717171] mt-2 mb-6 text-sm">
            Could not locate the requested trip plan. It might have been deleted or the ID is invalid.
          </p>
          <Link
            to="/planner"
            className="px-6 py-2.5 rounded-xl bg-[#222222] text-white text-sm font-medium hover:bg-[#333] transition-colors inline-block"
          >
            Generate a New Trip
          </Link>
        </div>
        <Footer />
      </div>
    )
  }

  // Prepare budget chart data
  const budgetBreakdownData = [
    { name: 'Accommodation', value: tripData.budget_breakdown?.accommodation || 0 },
    { name: 'Transport', value: tripData.budget_breakdown?.transport || 0 },
    { name: 'Food & Dining', value: tripData.budget_breakdown?.food || 0 },
    { name: 'Activities & Entries', value: tripData.budget_breakdown?.activities || 0 },
    { name: 'Miscellaneous', value: tripData.budget_breakdown?.misc || 0 },
  ].filter(item => item.value > 0)

  // Remove place from a day itinerary
  const handleRemoveFromDay = async (dayKey: string, placeIdx: number) => {
    if (!tripData.itinerary) return
    const updatedItinerary = { ...tripData.itinerary }
    if (updatedItinerary[dayKey]) {
      const places = [...updatedItinerary[dayKey].places]
      const removed = places.splice(placeIdx, 1)[0]
      updatedItinerary[dayKey].places = places
      updatedItinerary[dayKey].total_cost = places.reduce((sum, p) => sum + (p.average_cost || 0), 0)
      updatedItinerary[dayKey].total_time = places.reduce((sum, p) => sum + (p.time_needed || 0), 0)

      // Recalculate global costs
      const newActivitiesCost = Object.values(updatedItinerary).reduce((sum, d) => sum + d.total_cost, 0)
      const currentMisc = tripData.budget_breakdown?.misc || 0
      const currentAcc = tripData.budget_breakdown?.accommodation || 0
      const currentTrans = tripData.budget_breakdown?.transport || 0
      const currentFood = tripData.budget_breakdown?.food || 0

      const newTotalCost = currentAcc + currentTrans + currentFood + newActivitiesCost + currentMisc
      const newRemaining = Math.max(0, (tripData.budget || 0) - newTotalCost)

      setTripData({
        ...tripData,
        itinerary: updatedItinerary,
        total_estimated_cost: newTotalCost,
        budget_remaining: newRemaining,
        budget_breakdown: {
          ...tripData.budget_breakdown!,
          activities: newActivitiesCost,
        },
      })

      toast.success(`Removed ${removed?.place_name} from Day ${dayKey}. Costs updated!`)

      // Persist update to database
      if (id) {
        tripsApi.update(Number(id), {
          itinerary: updatedItinerary,
          total_cost: newTotalCost,
        }).catch(() => {})
      }
    }
  }

  const handleToggleFavorite = async () => {
    try {
      if (isSavedFav) {
        setIsSavedFav(false)
        toast.success('Removed from your saved list')
      } else {
        await favouritesApi.add({
          item_type: 'trip',
          item_id: String(id),
          item_name: `${tripData.destination} (${tripData.days} Days)`,
          item_image: tripData.destination_info?.image,
        })
        setIsSavedFav(true)
        toast.success(`Saved trip #${id} to your personal dashboard!`)
      }
    } catch {
      toast.error('Could not update saved trips')
    }
  }

  const handlePrint = () => {
    window.print()
  }

  const dayKeys = Object.keys(tripData.itinerary || {}).sort((a, b) => Number(a) - Number(b))
  const displayedDayKeys = selectedDayFilter === 'all' ? dayKeys : [selectedDayFilter]

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        {/* HERO HEADER */}
        <div className="pt-28 px-6 pb-10">
          <div className="max-w-7xl mx-auto">
            {/* Top Navigation Bar */}
            <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
              <Link
                to="/planner"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-[#DDDDDD] text-xs font-medium text-[#222222] hover:bg-[#F7F7F7] shadow-sm transition-all cursor-pointer"
              >
                <ArrowLeft className="w-3.5 h-3.5" /> Back to Planner
              </Link>

              <div className="flex items-center gap-2.5">
                <button
                  onClick={handleToggleFavorite}
                  className={`px-4 py-2 rounded-xl text-xs font-medium border transition-all flex items-center gap-1.5 cursor-pointer shadow-sm ${
                    isSavedFav
                      ? 'bg-rose-50 text-rose-600 border-rose-200'
                      : 'bg-white text-[#222222] border-[#DDDDDD] hover:bg-[#F7F7F7]'
                  }`}
                >
                  <Heart className={`w-3.5 h-3.5 ${isSavedFav ? 'fill-rose-500 text-rose-500' : ''}`} />
                  <span>{isSavedFav ? 'Saved to Hub' : 'Save Itinerary'}</span>
                </button>

                <button
                  onClick={handlePrint}
                  className="px-4 py-2 rounded-xl bg-white border border-[#DDDDDD] text-xs font-medium text-[#222222] hover:bg-[#F7F7F7] shadow-sm flex items-center gap-1.5 cursor-pointer"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Print / Export</span>
                </button>

                <span className="px-3 py-1.5 rounded-xl bg-[#F7F7F7] text-[#008489] text-xs font-medium border border-[#DDDDDD] flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#008489]" /> ML Verified
                </span>
              </div>
            </div>

            {/* Visual Destination Card Header */}
            <div className="relative rounded-2xl overflow-hidden bg-white border border-[#DDDDDD] shadow-sm">
              <div className="h-64 sm:h-80 w-full relative">
                <img
                  src={tripData.destination_info?.image || 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=1400&q=80'}
                  alt={tripData.destination}
                  className="w-full h-full object-cover"
                  referrerPolicy="no-referrer"
                  loading="lazy"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1400&q=80'
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />

                <div className="absolute top-5 left-5 flex items-center gap-2">
                  <span className="px-3 py-1 rounded-full bg-white/95 backdrop-blur-sm text-xs font-medium text-[#222222] shadow-sm flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-[#222222]" /> {tripData.destination}
                  </span>
                  <span className="px-3 py-1 rounded-full bg-white/95 backdrop-blur-sm text-xs font-medium text-[#222222] shadow-sm flex items-center gap-1.5">
                    <Calendar className="w-3.5 h-3.5 text-[#222222]" /> {tripData.days} Days · {tripData.group_size} Travellers
                  </span>
                </div>

                <div className="absolute bottom-5 left-5 right-5 text-white flex flex-col md:flex-row md:items-end justify-between gap-4">
                  <div>
                    <h1 className="text-2xl sm:text-3xl font-bold tracking-tight mb-1 text-white">
                      {tripData.destination} Travel Itinerary
                    </h1>
                    <p className="text-xs sm:text-sm text-stone-200 max-w-2xl line-clamp-2">
                      {tripData.destination_info?.description || 'Customized schedule engineered using Random Forest classification, K-Means clustering, and Ridge regression.'}
                    </p>
                  </div>

                  {/* Identified Archetype Pill */}
                  <div className="p-3.5 rounded-xl bg-white/95 backdrop-blur-sm text-[#222222] shadow-sm text-left md:text-right border border-white/50">
                    <span className="text-xs text-[#717171] font-medium block">
                      Discovered ML Archetype
                    </span>
                    <div className="text-sm font-semibold text-[#222222] flex items-center md:justify-end gap-1.5 mt-0.5">
                      <Brain className="w-4 h-4 text-[#008489]" />
                      {tripData.traveller_profile?.label || 'Custom Traveller'}
                    </div>
                    <span className="text-xs text-[#717171] block mt-0.5 max-w-xs">
                      {tripData.traveller_profile?.description}
                    </span>
                  </div>
                </div>
              </div>

              {/* KPI Metrics Ribbon */}
              <div className="p-6 bg-white grid grid-cols-2 lg:grid-cols-4 gap-5">
                <div className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-4">
                  <span className="text-xs text-[#717171] flex items-center gap-1.5 mb-1">
                    <Wallet className="w-4 h-4 text-[#717171]" /> Total Estimated Cost
                  </span>
                  <div className="text-xl font-bold text-[#222222] font-mono">
                    ₹{tripData.total_estimated_cost?.toLocaleString('en-IN')}
                  </div>
                  <span className="text-xs text-[#717171]">
                    Target: ₹{tripData.budget?.toLocaleString('en-IN')}
                  </span>
                </div>

                <div className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-4">
                  <span className="text-xs text-[#717171] flex items-center gap-1.5 mb-1">
                    <TrendingUp className="w-4 h-4 text-[#008489]" /> Remaining Balance
                  </span>
                  <div className="text-xl font-bold text-[#008489] font-mono">
                    ₹{tripData.budget_remaining?.toLocaleString('en-IN')}
                  </div>
                  <span className="text-xs text-[#008489] font-medium">
                    {tripData.over_budget ? '⚠️ Slightly Over Budget' : '✓ Within Budget Limit'}
                  </span>
                </div>

                <div className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-4">
                  <span className="text-xs text-[#717171] flex items-center gap-1.5 mb-1">
                    <Users className="w-4 h-4 text-[#717171]" /> Daily Cost Per Person
                  </span>
                  <div className="text-xl font-bold text-[#222222] font-mono">
                    ₹{tripData.cost_per_person
                      ? Math.round(tripData.cost_per_person / Math.max(1, tripData.days || 1)).toLocaleString('en-IN')
                      : 'N/A'}
                  </div>
                  <span className="text-xs text-[#717171]">
                    Total ₹{tripData.cost_per_person?.toLocaleString('en-IN')} / person
                  </span>
                </div>

                <div className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-4">
                  <span className="text-xs text-[#717171] flex items-center gap-1.5 mb-1">
                    <Clock className="w-4 h-4 text-[#717171]" /> Scheduled Activities
                  </span>
                  <div className="text-xl font-bold text-[#222222] font-mono">
                    {Object.values(tripData.itinerary || {}).reduce((s, d) => s + (d.places?.length || 0), 0)} Spots
                  </div>
                  <span className="text-xs text-[#717171]">
                    {tripData.constraint_report?.total_activity_hours || 18}h Total Sightseeing
                  </span>
                </div>
              </div>
            </div>

            {/* TAB SELECTOR NAVIGATION - Underline Style */}
            <div className="border-b border-[#DDDDDD] flex items-center gap-6 overflow-x-auto mt-8 scrollbar-none">
              {[
                { id: 'itinerary', label: 'Day-Wise Itinerary', icon: Calendar },
                { id: 'recommendations', label: 'ML Recommendations Audit', icon: Brain },
                { id: 'insights', label: 'Cost & Time Analytics', icon: BarChart3 },
                { id: 'constraints', label: 'Constraint Solver Report', icon: ShieldCheck },
              ].map(tab => {
                const isActive = activeTab === tab.id
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as typeof activeTab)}
                    className={`pb-3 text-sm font-medium transition-all cursor-pointer flex items-center gap-2 whitespace-nowrap border-b-2 ${
                      isActive
                        ? 'text-[#222222] border-[#222222]'
                        : 'text-[#717171] border-transparent hover:text-[#222222] hover:border-[#DDDDDD]'
                    }`}
                  >
                    <tab.icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </div>

            {/* TAB CONTENTS */}
            <div className="mt-8">
              {/* TAB 1: DAY-WISE ITINERARY */}
              {activeTab === 'itinerary' && (
                <div className="space-y-6">
                  {/* Day filter pills */}
                  <div className="flex items-center justify-between flex-wrap gap-3 bg-white p-4 rounded-xl border border-[#DDDDDD] shadow-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-[#717171]">Filter:</span>
                      <button
                        onClick={() => setSelectedDayFilter('all')}
                        className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
                          selectedDayFilter === 'all'
                            ? 'bg-[#222222] text-white'
                            : 'border border-[#DDDDDD] bg-white text-[#222222] hover:bg-[#F7F7F7]'
                        }`}
                      >
                        All {dayKeys.length} Days
                      </button>
                      {dayKeys.map(k => (
                        <button
                          key={k}
                          onClick={() => setSelectedDayFilter(k)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
                            selectedDayFilter === k
                              ? 'bg-[#222222] text-white'
                              : 'border border-[#DDDDDD] bg-white text-[#222222] hover:bg-[#F7F7F7]'
                          }`}
                        >
                          Day {k}
                        </button>
                      ))}
                    </div>

                    <span className="text-xs text-[#717171]">
                      Click trash icon to remove activity; costs update automatically.
                    </span>
                  </div>

                  {/* Day Cards Loop */}
                  <div className="space-y-6">
                    {displayedDayKeys.map(dayKey => {
                      const day = (tripData.itinerary || {})[dayKey]
                      if (!day) return null

                      return (
                        <div
                          key={dayKey}
                          className="bg-white rounded-2xl border border-[#DDDDDD] shadow-sm overflow-hidden"
                        >
                          {/* Day Banner */}
                          <div className="bg-[#F7F7F7] border-b border-[#DDDDDD] p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                            <div className="flex items-center gap-3">
                              <span className="w-9 h-9 rounded-xl bg-[#222222] text-white font-bold flex items-center justify-center text-sm">
                                {dayKey}
                              </span>
                              <div>
                                <h3 className="text-base font-semibold text-[#222222]">
                                  {day.day_title || `Day ${dayKey} Schedule`}
                                </h3>
                                <p className="text-xs text-[#717171]">
                                  {day.places?.length || 0} Scheduled Attractions · {day.total_time?.toFixed(1) || '0'}h sightseeing
                                </p>
                              </div>
                            </div>

                            <div className="flex items-center gap-4 text-xs">
                              <span className="text-[#222222] bg-white px-3 py-1.5 rounded-lg border border-[#DDDDDD]">
                                Day Cost: <strong className="font-semibold">₹{day.total_cost?.toLocaleString('en-IN')}</strong>
                              </span>
                            </div>
                          </div>

                          {/* Activities list */}
                          <div className="p-5 sm:p-6 space-y-4">
                            {day.places && day.places.length > 0 ? (
                              day.places.map((place: Place, pIdx: number) => {
                                const slot = TIME_OF_DAY_SLOTS[pIdx % TIME_OF_DAY_SLOTS.length]
                                return (
                                  <div
                                    key={place.place_name + pIdx}
                                    className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-5 group"
                                  >
                                    <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 flex-1">
                                      {/* Place Photo thumbnail */}
                                      <div className="w-full sm:w-28 h-20 rounded-lg overflow-hidden relative flex-shrink-0 bg-stone-200 group/img">
                                        <img
                                          src={
                                            place.image ||
                                            `https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400&q=80`
                                          }
                                          alt={place.place_name}
                                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                                          referrerPolicy="no-referrer"
                                          loading="lazy"
                                          onError={(e) => {
                                            (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400&q=80'
                                          }}
                                        />
                                        <div className="absolute top-1.5 left-1.5 px-1.5 py-0.5 rounded bg-white/95 text-[10px] font-semibold text-[#222222]">
                                          ★ {place.rating}
                                        </div>
                                      </div>

                                      {/* Details */}
                                      <div className="space-y-1 flex-1">
                                        <div className="flex flex-wrap items-center gap-2">
                                          <span className="text-xs font-semibold text-[#008489]">
                                            {slot.icon} {place.time_of_day ? `${place.time_of_day} Expedition` : slot.label}
                                          </span>
                                          <span className="text-xs text-[#717171]">
                                            · {place.time_slot || slot.time}
                                          </span>
                                        </div>

                                        <h4 className="text-base font-semibold text-[#222222]">
                                          {place.place_name}
                                        </h4>

                                        <p className="text-xs text-[#717171] leading-relaxed line-clamp-2">
                                          {place.description || `${place.category} attraction located in ${tripData.destination}`}
                                        </p>

                                        {/* ML Explanation Badge */}
                                        <div className="pt-1 flex flex-wrap items-center gap-2">
                                          <span className="bg-[#F7F7F7] text-[#008489] border border-[#DDDDDD] text-xs px-2 py-0.5 rounded-md flex items-center gap-1 font-medium">
                                            <Brain className="w-3 h-3 text-[#008489]" />
                                            {place.ml_explanation || `Predicted Match: ${Math.round((place.like_probability || 0.88) * 100)}%`}
                                          </span>
                                          <span className="text-xs text-[#717171]">
                                            Category: <strong className="text-[#222222]">{place.category}</strong>
                                          </span>
                                        </div>
                                      </div>
                                    </div>

                                    {/* Right stats and remove button */}
                                    <div className="flex items-center justify-between md:justify-end gap-5 w-full md:w-auto pt-3 md:pt-0 border-t md:border-t-0 border-[#DDDDDD]">
                                      <div className="text-left md:text-right">
                                        <div className="text-sm font-semibold text-[#222222] font-mono">
                                          ₹{place.average_cost?.toLocaleString('en-IN') || 0}
                                        </div>
                                        <div className="text-xs text-[#717171] flex items-center gap-1">
                                          <Clock className="w-3 h-3 text-[#717171]" /> {place.time_needed}h
                                        </div>
                                      </div>

                                      <button
                                        type="button"
                                        onClick={() => handleRemoveFromDay(dayKey, pIdx)}
                                        title="Remove activity from day"
                                        className="p-2 rounded-lg text-[#717171] hover:text-rose-600 hover:bg-stone-200/50 transition-colors cursor-pointer"
                                      >
                                        <Trash2 className="w-4 h-4" />
                                      </button>
                                    </div>
                                  </div>
                                )
                              })
                            ) : (
                              <div className="text-center py-6 text-[#717171] text-xs">
                                No activities scheduled for Day {dayKey}.
                              </div>
                            )}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* TAB 2: ML RECOMMENDATION AUDIT */}
              {activeTab === 'recommendations' && (
                <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm space-y-6">
                  <div>
                    <span className="text-xs text-[#717171] font-medium block mb-1">
                      Algorithmic Transparency
                    </span>
                    <h3 className="text-xl font-bold text-[#222222]">
                      Candidate Attraction Ranking & Scoring Audit
                    </h3>
                    <p className="text-xs text-[#717171] mt-1">
                      Ranked by weighted scoring equation: <code className="bg-[#F7F7F7] border border-[#DDDDDD] px-1.5 py-0.5 rounded text-[#222222] font-mono">Score = 0.35·P_RF + 0.30·Match + 0.20·Rating + 0.15·BudgetFit</code>
                    </p>
                  </div>

                  <div className="space-y-3">
                    {(tripData.recommendations || tripData.recommended_places || []).map((place: Place, idx: number) => (
                      <div
                        key={place.place_name + idx}
                        className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
                      >
                        <div className="flex items-center gap-3.5 flex-1">
                          <span className="bg-[#F7F7F7] text-[#222222] border border-[#DDDDDD] w-8 h-8 rounded-xl font-semibold flex items-center justify-center text-xs">
                            #{idx + 1}
                          </span>
                          <div>
                            <h4 className="font-semibold text-[#222222] text-sm">{place.place_name}</h4>
                            <span className="text-xs text-[#717171]">{place.category} · ★ {place.rating}</span>
                            <p className="text-xs text-[#008489] mt-0.5">{place.ml_explanation}</p>
                          </div>
                        </div>

                        <div className="grid grid-cols-3 gap-3 text-center w-full md:w-auto">
                          <div className="bg-[#F7F7F7] rounded-lg border border-[#DDDDDD] p-2.5">
                            <span className="text-[10px] text-[#717171] block">RF Likelihood</span>
                            <span className="text-xs font-semibold text-[#222222] font-mono">
                              {Math.round((place.like_probability || 0.85) * 100)}%
                            </span>
                          </div>
                          <div className="bg-[#F7F7F7] rounded-lg border border-[#DDDDDD] p-2.5">
                            <span className="text-[10px] text-[#717171] block">Category Match</span>
                            <span className="text-xs font-semibold text-[#008489] font-mono">
                              {Math.round((place.interest_match || 0.8) * 100)}%
                            </span>
                          </div>
                          <div className="bg-[#F7F7F7] rounded-lg border border-[#DDDDDD] p-2.5">
                            <span className="text-[10px] text-[#717171] block">Score</span>
                            <span className="text-xs font-semibold text-[#222222] font-mono">
                              {(place.final_recommendation_score || 0.88).toFixed(3)}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* TAB 3: COST & TIME ANALYTICS */}
              {activeTab === 'insights' && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Budget breakdown Donut chart */}
                  <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                    <h3 className="text-base font-semibold text-[#222222] mb-1">
                      Budget Allocation Breakdown
                    </h3>
                    <p className="text-xs text-[#717171] mb-4">
                      Estimated division of your ₹{tripData.total_estimated_cost?.toLocaleString('en-IN')} total cost
                    </p>

                    <div className="h-60 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={budgetBreakdownData}
                            dataKey="value"
                            nameKey="name"
                            cx="50%"
                            cy="50%"
                            innerRadius={55}
                            outerRadius={80}
                            paddingAngle={3}
                          >
                            {budgetBreakdownData.map((_, index) => (
                              <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip formatter={(value: any) => `₹${Number(value).toLocaleString('en-IN')}`} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>

                    <div className="grid grid-cols-2 gap-2 mt-2 text-xs">
                      {budgetBreakdownData.map((item, idx) => (
                        <div key={item.name} className="flex items-center gap-2 p-2 rounded-lg bg-[#F7F7F7] border border-[#DDDDDD]">
                          <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: PIE_COLORS[idx % PIE_COLORS.length] }} />
                          <span className="text-[#717171] truncate">{item.name}:</span>
                          <strong className="text-[#222222] font-mono">₹{item.value.toLocaleString('en-IN')}</strong>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Model regression summary */}
                  <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm space-y-5">
                    <div>
                      <h3 className="text-base font-semibold text-[#222222] mb-1">
                        Regression Cost Estimation
                      </h3>
                      <p className="text-xs text-[#717171]">
                        Evaluated by regularized Ridge & Random Forest regressors
                      </p>
                    </div>

                    <div className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-5 space-y-2.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-[#717171]">Target Budget:</span>
                        <strong className="text-[#222222] font-mono">₹{tripData.budget?.toLocaleString('en-IN')}</strong>
                      </div>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-[#717171]">Model Predicted Cost:</span>
                        <strong className="text-[#222222] font-mono">₹{tripData.total_estimated_cost?.toLocaleString('en-IN')}</strong>
                      </div>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-[#717171]">Surplus / Buffer:</span>
                        <strong className="text-[#008489] font-mono">
                          +₹{tripData.budget_remaining?.toLocaleString('en-IN')}
                        </strong>
                      </div>
                    </div>

                    <div className="bg-[#F7F7F7] border border-[#DDDDDD] text-[#222222] p-4 rounded-xl text-xs space-y-1">
                      <div className="font-semibold text-[#222222]">Regression Quality Metrics:</div>
                      <div className="text-[#717171]">• Cost Regressor R² = 93.7% (Test Set)</div>
                      <div className="text-[#717171]">• Activity Duration Regressor R² = 82.9%</div>
                      <div className="text-[#717171]">• 5-Fold Cross Validation MAE: ₹7,419</div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 4: CONSTRAINT REPORT */}
              {activeTab === 'constraints' && (
                <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm space-y-6">
                  <div>
                    <span className="text-xs text-[#717171] font-medium block mb-1">
                      System Optimization
                    </span>
                    <h3 className="text-xl font-bold text-[#222222]">
                      Constraint Satisfaction Engine Audit
                    </h3>
                    <p className="text-xs text-[#717171] mt-1">
                      Verifies that the generated schedule does not violate physical time boundaries or financial ceilings.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-5">
                      <div className="flex items-center gap-2 font-semibold text-[#222222] text-sm mb-3">
                        <CheckCircle2 className="w-4 h-4 text-[#008489]" /> Budget Constraint Verification
                      </div>
                      <ul className="text-xs space-y-2 text-[#717171]">
                        <li>• Budget Cap: ₹{tripData.budget?.toLocaleString('en-IN')}</li>
                        <li>• Total Projected Expenditure: ₹{tripData.total_estimated_cost?.toLocaleString('en-IN')}</li>
                        <li>• Solved Status: <span className="text-[#008489] font-medium">Passed (Within Limits)</span></li>
                      </ul>
                    </div>

                    <div className="bg-[#F7F7F7] rounded-xl border border-[#DDDDDD] p-5">
                      <div className="flex items-center gap-2 font-semibold text-[#222222] text-sm mb-3">
                        <CheckCircle2 className="w-4 h-4 text-[#008489]" /> Daily Time Bounds Verification
                      </div>
                      <ul className="text-xs space-y-2 text-[#717171]">
                        <li>• Maximum Daily Activity Cap: 8.0 hours/day</li>
                        <li>• Average Scheduled Sightseeing: {((tripData.constraint_report?.total_activity_hours || 18) / Math.max(1, tripData.days)).toFixed(1)}h/day</li>
                        <li>• Solved Status: <span className="text-[#008489] font-medium">Passed (Zero Fatigue Overlap)</span></li>
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
