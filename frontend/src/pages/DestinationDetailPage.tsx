import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Star, MapPin, Clock, Heart, ArrowLeft, Calendar, ShieldCheck, Sparkles, Compass, Wallet } from 'lucide-react'
import { toast } from 'sonner'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import { destinationsApi, favouritesApi, type Destination, type Place } from '@/services/api'

const CATEGORY_ICONS: Record<string, string> = {
  Nature: '🌿', Adventure: '🏔️', History: '🏛️', Food: '🍜',
  Shopping: '🛍️', Culture: '🎭', Relaxation: '🌅',
}

export default function DestinationDetailPage() {
  const { name } = useParams<{ name: string }>()
  const [destination, setDestination] = useState<Destination | null>(null)
  const [places, setPlaces] = useState<Place[]>([])
  const [loading, setLoading] = useState(true)
  const [isFav, setIsFav] = useState(false)
  const [selectedCat, setSelectedCat] = useState('All')

  useEffect(() => {
    if (!name) return
    setLoading(true)
    const destName = decodeURIComponent(name)
    destinationsApi.getByName(destName)
      .then(res => {
        setDestination(res.data.destination)
        setPlaces(res.data.places)
      })
      .catch(() => toast.error('Could not load destination details'))
      .finally(() => setLoading(false))

    favouritesApi.getAll()
      .then(res => {
        setIsFav(res.data.favourites.some(f => f.item_name.toLowerCase() === destName.toLowerCase()))
      })
      .catch(() => {})
  }, [name])

  const handleFavourite = async () => {
    if (!destination) return
    try {
      if (isFav) {
        const res = await favouritesApi.getAll()
        const fav = res.data.favourites.find(f => f.item_name.toLowerCase() === destination.destination.toLowerCase())
        if (fav) {
          await favouritesApi.remove(fav.id)
          setIsFav(false)
          toast.success('Removed from favourites')
        }
      } else {
        await favouritesApi.add({
          item_type: 'destination',
          item_id: String(destination.destination_id || destination.destination),
          item_name: destination.destination,
          item_image: destination.image,
        })
        setIsFav(true)
        toast.success(`Saved ${destination.destination} to favourites`)
      }
    } catch {
      toast.error('Could not update favourites')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
        <Navbar />
        <div className="pt-32 max-w-7xl mx-auto px-6 py-12 w-full animate-pulse">
          <div className="h-96 rounded-2xl bg-stone-100 border border-[#DDDDDD] mb-8" />
          <div className="h-8 w-1/3 bg-stone-100 rounded-lg mb-4" />
          <div className="h-4 w-2/3 bg-stone-100 rounded-lg" />
        </div>
        <Footer />
      </div>
    )
  }

  if (!destination) {
    return (
      <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
        <Navbar />
        <div className="pt-36 text-center py-20 px-6 max-w-md mx-auto">
          <div className="text-4xl mb-3">📍</div>
          <h2 className="text-xl font-bold text-[#222222]">Destination Not Found</h2>
          <p className="text-[#717171] mt-2 mb-6 text-sm">
            The destination you requested does not exist in our dataset.
          </p>
          <Link
            to="/destinations"
            className="px-6 py-2.5 rounded-xl bg-[#222222] text-white text-xs font-medium hover:bg-[#333] transition-colors inline-block"
          >
            Back to Destinations
          </Link>
        </div>
        <Footer />
      </div>
    )
  }

  const allCategories = ['All', ...Array.from(new Set(places.map(p => p.category).filter(Boolean)))]
  const filteredPlaces = selectedCat === 'All' ? places : places.filter(p => p.category === selectedCat)

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        {/* HERO BANNER */}
        <div className="pt-28 px-6 pb-12">
          <div className="max-w-7xl mx-auto">
            {/* Breadcrumb & Actions */}
            <div className="flex items-center justify-between gap-4 mb-6">
              <Link
                to="/destinations"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-[#DDDDDD] text-xs font-medium text-[#222222] hover:bg-[#F7F7F7] shadow-sm transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" /> All Destinations
              </Link>

              <div className="flex items-center gap-2.5">
                <button
                  onClick={handleFavourite}
                  className={`px-4 py-2 rounded-xl text-xs font-medium border transition-all flex items-center gap-1.5 cursor-pointer shadow-sm ${
                    isFav
                      ? 'bg-rose-50 text-rose-600 border-rose-200'
                      : 'bg-white text-[#222222] border-[#DDDDDD] hover:bg-[#F7F7F7]'
                  }`}
                >
                  <Heart className={`w-3.5 h-3.5 ${isFav ? 'fill-rose-500 text-rose-500' : ''}`} />
                  <span>{isFav ? 'Saved' : 'Wishlist'}</span>
                </button>

                <Link to={`/planner?destination=${encodeURIComponent(destination.destination)}`}>
                  <button className="px-5 py-2 rounded-xl bg-[#222222] hover:bg-[#333333] text-white text-xs font-medium transition-all shadow-sm flex items-center gap-1.5 cursor-pointer">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Plan Trip Here</span>
                  </button>
                </Link>
              </div>
            </div>

            {/* Visual Hero Card */}
            <div className="relative rounded-2xl overflow-hidden bg-white border border-[#DDDDDD] shadow-sm mb-10">
              <div className="h-80 sm:h-96 w-full relative">
                <img
                  src={destination.image}
                  alt={destination.destination}
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
                    <MapPin className="w-3.5 h-3.5 text-[#222222]" /> {destination.region || destination.country}
                  </span>
                  <span className="px-3 py-1 rounded-full bg-white/95 backdrop-blur-sm text-xs font-medium text-[#222222] shadow-sm flex items-center gap-1">
                    <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-500" /> {destination.avg_rating} Stars
                  </span>
                </div>

                <div className="absolute bottom-5 left-5 right-5 text-white">
                  <h1 className="text-3xl sm:text-4xl font-bold tracking-tight mb-2 text-white">
                    {destination.destination}
                  </h1>
                  <p className="text-sm text-stone-200 max-w-2xl leading-relaxed">
                    {destination.description}
                  </p>
                </div>
              </div>

              {/* Stats Ribbon */}
              <div className="p-6 bg-white grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                  <span className="text-xs text-[#717171] flex items-center gap-1 mb-1">
                    <Wallet className="w-3.5 h-3.5 text-[#717171]" /> Average Daily Cost
                  </span>
                  <div className="text-xl font-bold text-[#222222] font-mono">
                    ₹{destination.avg_cost_per_day?.toLocaleString('en-IN')}
                  </div>
                  <span className="text-[11px] text-[#717171]">per person / day</span>
                </div>

                <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                  <span className="text-xs text-[#717171] flex items-center gap-1 mb-1">
                    <Calendar className="w-3.5 h-3.5 text-[#717171]" /> Ideal Duration
                  </span>
                  <div className="text-xl font-bold text-[#222222] font-mono">
                    {destination.best_duration_days} Days
                  </div>
                  <span className="text-[11px] text-[#717171]">recommended pace</span>
                </div>

                <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                  <span className="text-xs text-[#717171] flex items-center gap-1 mb-1">
                    <Compass className="w-3.5 h-3.5 text-[#717171]" /> Verified Attractions
                  </span>
                  <div className="text-xl font-bold text-[#222222] font-mono">
                    {places.length} Places
                  </div>
                  <span className="text-[11px] text-[#717171]">calibrated in dataset</span>
                </div>

                <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                  <span className="text-xs text-[#717171] flex items-center gap-1 mb-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-[#008489]" /> ML Calibrated
                  </span>
                  <div className="text-xl font-bold text-[#008489] font-mono">
                    100% Ready
                  </div>
                  <span className="text-[11px] text-[#717171]">full pipeline support</span>
                </div>
              </div>
            </div>

            {/* Attractions Section */}
            <div className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h3 className="text-2xl font-bold text-[#222222]">
                    Attractions in {destination.destination}
                  </h3>
                  <p className="text-xs text-[#717171] mt-1">
                    Historical points of interest, viewpoints, culinary centers, and adventure activities.
                  </p>
                </div>

                {/* Filter Pills */}
                <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
                  {allCategories.map(cat => {
                    const isActive = selectedCat === cat
                    return (
                      <button
                        key={cat}
                        onClick={() => setSelectedCat(cat || 'All')}
                        className={`px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
                          isActive
                            ? 'bg-[#222222] text-white'
                            : 'bg-white border border-[#DDDDDD] text-[#222222] hover:bg-[#F7F7F7]'
                        }`}
                      >
                        {cat}
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Grid of Places */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredPlaces.map(place => (
                  <div
                    key={place.place_name}
                    className="p-5 rounded-2xl bg-white border border-[#DDDDDD] shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="relative h-44 rounded-xl overflow-hidden mb-4 bg-stone-100">
                        <img
                          src={place.image || 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=500&q=80'}
                          alt={place.place_name}
                          className="w-full h-full object-cover"
                          referrerPolicy="no-referrer"
                          loading="lazy"
                          onError={(e) => {
                            (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=500&q=80'
                          }}
                        />
                        <div className="absolute top-2.5 right-2.5 bg-white/95 backdrop-blur-sm px-2.5 py-0.5 rounded-md text-xs font-semibold text-[#222222] flex items-center gap-1">
                          ★ {place.rating}
                        </div>
                        <div className="absolute bottom-2.5 left-2.5">
                          <span className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-black/60 text-white backdrop-blur-sm">
                            {CATEGORY_ICONS[place.category || ''] || '📍'} {place.category}
                          </span>
                        </div>
                      </div>

                      <h4 className="font-semibold text-[#222222] text-base mb-1">
                        {place.place_name}
                      </h4>
                      <p className="text-xs text-[#717171] line-clamp-2 leading-relaxed mb-4">
                        {place.description || `Famous ${place.category} attraction located in ${destination.destination}`}
                      </p>
                    </div>

                    <div className="pt-3 border-t border-[#DDDDDD] flex items-center justify-between text-xs">
                      <span className="text-[#717171]">
                        Entry: <strong className="text-[#222222] font-semibold">₹{place.average_cost?.toLocaleString('en-IN') || 0}</strong>
                      </span>
                      <span className="text-[#717171] flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-[#717171]" /> {place.time_needed}h needed
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Bottom Call to Action */}
            <div className="mt-16 p-8 sm:p-10 rounded-2xl bg-white border border-[#DDDDDD] flex flex-col sm:flex-row items-center justify-between gap-6 shadow-sm">
              <div>
                <h3 className="text-xl font-bold text-[#222222] mb-1">
                  Ready to visit {destination.destination}?
                </h3>
                <p className="text-xs text-[#717171] max-w-lg">
                  Let our machine learning pipeline build a day-wise itinerary optimized for your budget and specific interests.
                </p>
              </div>
              <Link to={`/planner?destination=${encodeURIComponent(destination.destination)}`}>
                <button className="px-6 py-3 rounded-xl bg-[#222222] hover:bg-[#333333] text-white font-medium text-xs shadow-sm transition-all cursor-pointer whitespace-nowrap">
                  Plan Itinerary with AI →
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
