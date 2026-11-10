import { useState, useEffect } from 'react'
import { Search, Star, MapPin, Clock, Heart } from 'lucide-react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import { destinationsApi, favouritesApi, type Destination } from '@/services/api'

const CATEGORIES = [
  { label: 'All', icon: '✨' },
  { label: 'Nature', icon: '🌿' },
  { label: 'Adventure', icon: '🏔️' },
  { label: 'History', icon: '🏛️' },
  { label: 'Food', icon: '🍜' },
  { label: 'Shopping', icon: '🛍️' },
  { label: 'Culture', icon: '🎭' },
  { label: 'Relaxation', icon: '🌅' },
]

const SORT_OPTIONS = [
  { value: 'avg_rating', label: 'Highest Rated' },
  { value: 'avg_cost_per_day', label: 'Lowest Budget First' },
  { value: 'best_duration_days', label: 'Ideal Trip Duration' },
]

const BUDGET_OPTIONS = [
  { label: 'Any Budget', value: undefined },
  { label: 'Under ₹2,500 / day', value: 2500 },
  { label: 'Under ₹4,000 / day', value: 4000 },
  { label: 'Under ₹6,000 / day', value: 6000 },
]

function DestinationCard({
  dest,
  onFavourite,
  isFav,
}: {
  dest: Destination
  onFavourite: (d: Destination) => void
  isFav: boolean
}) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.98 }}
      className="group bg-white rounded-2xl overflow-hidden border border-[#DDDDDD] hover:shadow-lg transition-all duration-200 flex flex-col justify-between"
    >
      <div>
        <div className="relative h-56 overflow-hidden bg-stone-100">
          <img
            src={dest.image || 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=700&q=80'}
            alt={dest.destination}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            referrerPolicy="no-referrer"
            loading="lazy"
            onError={(e) => {
              (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=700&q=80'
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />

          {/* Favourite button */}
          <button
            onClick={(e) => {
              e.preventDefault()
              e.stopPropagation()
              onFavourite(dest)
            }}
            className={`absolute top-3 right-3 w-9 h-9 rounded-full flex items-center justify-center transition-all shadow-sm cursor-pointer ${
              isFav
                ? 'bg-rose-500 text-white'
                : 'bg-white/90 backdrop-blur-md text-[#222222] hover:bg-white hover:text-rose-500'
            }`}
            aria-label="Save to favourites"
          >
            <Heart className={`w-4 h-4 ${isFav ? 'fill-white' : ''}`} />
          </button>

          {/* Rating pill top-left */}
          <div className="absolute top-3 left-3 bg-white/90 backdrop-blur-md px-2.5 py-1 rounded-full text-xs font-semibold text-[#222222] flex items-center gap-1 shadow-sm">
            <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
            <span>{dest.avg_rating}</span>
          </div>

          {/* Category badges */}
          <div className="absolute bottom-3 left-3 right-3 flex flex-wrap gap-1.5">
            {(dest.categories || []).slice(0, 3).map(cat => (
              <span
                key={cat}
                className="bg-black/50 text-white text-xs rounded-full px-2 py-0.5 backdrop-blur-sm"
              >
                {cat}
              </span>
            ))}
          </div>
        </div>

        <div className="p-5">
          <div className="flex items-start justify-between gap-2 mb-1">
            <div>
              <h3 className="text-base font-semibold text-[#222222]">
                {dest.destination}
              </h3>
              <p className="text-sm text-[#717171] flex items-center gap-1 mt-0.5">
                <MapPin className="w-3.5 h-3.5 text-[#717171]" /> {dest.region || dest.country}
              </p>
            </div>
          </div>
          <p className="text-sm text-[#717171] line-clamp-2 mt-2">
            {dest.description}
          </p>
        </div>
      </div>

      <div className="p-5 pt-0">
        <div className="flex items-center justify-between pt-4 mt-4 border-t border-[#DDDDDD] text-xs mb-4">
          <div>
            <span className="text-[#717171]">Est. Daily Cost:</span>{' '}
            <strong className="font-semibold text-[#222222] text-sm ml-1">
              ₹{dest.avg_cost_per_day?.toLocaleString('en-IN')}
            </strong>
          </div>
          <div className="text-sm text-[#717171] flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-[#717171]" /> {dest.best_duration_days} days ideal
          </div>
        </div>

        <div className="flex gap-2">
          <Link
            to={`/destinations/${encodeURIComponent(dest.destination)}`}
            className="flex-1 py-2 text-center rounded-xl border border-[#DDDDDD] text-[#222222] text-sm font-medium hover:bg-[#F7F7F7] transition-colors cursor-pointer"
          >
            Explore Places
          </Link>
          <Link
            to={`/planner?destination=${encodeURIComponent(dest.destination)}`}
            className="flex-1 py-2 text-center rounded-xl bg-[#222222] hover:bg-[#333333] text-white text-sm font-medium transition-colors cursor-pointer flex items-center justify-center gap-1"
          >
            Plan Trip
          </Link>
        </div>
      </div>
    </motion.div>
  )
}

export default function DestinationsPage() {
  const [destinations, setDestinations] = useState<Destination[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('All')
  const [sortBy, setSortBy] = useState('avg_rating')
  const [maxBudget, setMaxBudget] = useState<number | undefined>()
  const [favourites, setFavourites] = useState<Set<string>>(new Set())

  useEffect(() => {
    setLoading(true)
    destinationsApi.getAll({
      search: search || undefined,
      category: category !== 'All' ? category : undefined,
      max_budget: maxBudget,
      sort_by: sortBy,
    })
      .then(res => setDestinations(res.data.destinations))
      .catch(() => toast.error('Failed to load destinations. Ensure backend is running.'))
      .finally(() => setLoading(false))
  }, [search, category, sortBy, maxBudget])

  useEffect(() => {
    favouritesApi.getAll()
      .then(res => setFavourites(new Set(res.data.favourites.map(f => f.item_name))))
      .catch(() => {})
  }, [])

  const handleFavourite = async (dest: Destination) => {
    try {
      if (favourites.has(dest.destination)) {
        const favs = await favouritesApi.getAll()
        const fav = favs.data.favourites.find(f => f.item_name === dest.destination)
        if (fav) {
          await favouritesApi.remove(fav.id)
          setFavourites(prev => {
            const next = new Set(prev)
            next.delete(dest.destination)
            return next
          })
          toast.success(`Removed ${dest.destination} from favourites`)
        }
      } else {
        await favouritesApi.add({
          item_type: 'destination',
          item_id: String(dest.destination_id || dest.destination),
          item_name: dest.destination,
          item_image: dest.image,
        })
        setFavourites(prev => new Set([...prev, dest.destination]))
        toast.success(`Saved ${dest.destination} to favourites`)
      }
    } catch {
      toast.error('Could not update favourites')
    }
  }

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        {/* Hero Section */}
        <div className="pt-32 pb-10 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="text-center max-w-3xl mx-auto mb-10">
              <h1 className="text-3xl sm:text-4xl font-bold text-[#222222] tracking-tight mb-3">
                Explore Premier Destinations
              </h1>
              <p className="text-base text-[#717171] leading-relaxed">
                Browse hand-curated Indian destinations with calibrated interest vectors, daily cost benchmarks, and direct ML pipeline planning.
              </p>
            </div>

            {/* Filter & Search Bar */}
            <div className="bg-white rounded-2xl border border-[#DDDDDD] shadow-sm p-4 max-w-4xl mx-auto mb-10 space-y-4">
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#717171]" />
                  <input
                    type="text"
                    placeholder="Search by destination name, region, or keyword..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    className="w-full border border-[#DDDDDD] rounded-xl pl-10 pr-4 py-2.5 text-sm bg-white text-[#222222] placeholder:text-[#717171] focus:outline-none focus:ring-2 focus:ring-[#222222]/10 focus:border-[#222222]"
                  />
                </div>

                <div className="flex gap-2">
                  <select
                    value={sortBy}
                    onChange={e => setSortBy(e.target.value)}
                    className="border border-[#DDDDDD] rounded-xl px-3 py-2.5 text-sm bg-white text-[#222222] focus:outline-none focus:border-[#222222] cursor-pointer"
                  >
                    {SORT_OPTIONS.map(opt => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>

                  <select
                    value={maxBudget || ''}
                    onChange={e => setMaxBudget(e.target.value ? Number(e.target.value) : undefined)}
                    className="border border-[#DDDDDD] rounded-xl px-3 py-2.5 text-sm bg-white text-[#222222] focus:outline-none focus:border-[#222222] cursor-pointer"
                  >
                    {BUDGET_OPTIONS.map(opt => (
                      <option key={opt.label} value={opt.value || ''}>{opt.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Category Pills */}
              <div className="flex items-center gap-2 overflow-x-auto pb-1 pt-1 scrollbar-none">
                {CATEGORIES.map(cat => {
                  const isActive = category === cat.label
                  return (
                    <button
                      key={cat.label}
                      onClick={() => setCategory(cat.label)}
                      className={`text-sm py-1.5 px-4 rounded-full whitespace-nowrap transition-all cursor-pointer flex items-center gap-1.5 ${
                        isActive
                          ? 'bg-[#222222] text-white border border-[#222222]'
                          : 'border border-[#DDDDDD] text-[#222222] bg-white hover:bg-[#F7F7F7]'
                      }`}
                    >
                      <span>{cat.icon}</span>
                      <span>{cat.label}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Destination Grid */}
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {[1, 2, 3, 4, 5, 6].map(i => (
                  <div key={i} className="h-96 rounded-2xl bg-stone-100 animate-pulse border border-[#DDDDDD]" />
                ))}
              </div>
            ) : destinations.length === 0 ? (
              <div className="text-center py-16 bg-white rounded-2xl border border-[#DDDDDD] p-8 max-w-md mx-auto">
                <div className="text-4xl mb-3">🔍</div>
                <h3 className="text-base font-semibold text-[#222222]">No destinations matched your filters</h3>
                <p className="text-sm text-[#717171] mt-1 mb-5">Try clearing the search query or selecting "All" categories.</p>
                <button
                  onClick={() => { setSearch(''); setCategory('All'); setMaxBudget(undefined) }}
                  className="px-5 py-2.5 rounded-xl bg-[#222222] text-white text-sm font-medium hover:bg-[#333] transition-colors cursor-pointer"
                >
                  Reset All Filters
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {destinations.map(dest => (
                  <DestinationCard
                    key={dest.destination}
                    dest={dest}
                    onFavourite={handleFavourite}
                    isFav={favourites.has(dest.destination)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
