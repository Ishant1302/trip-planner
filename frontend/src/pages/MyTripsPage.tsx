import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Trash2, MapPin, Sparkles, ArrowRight } from 'lucide-react'
import { toast } from 'sonner'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import { tripsApi, favouritesApi, type SavedTrip } from '@/services/api'

export default function MyTripsPage() {
  const [trips, setTrips] = useState<SavedTrip[]>([])
  const [favourites, setFavourites] = useState<Array<{ id: number; item_name: string; item_image?: string; item_type: string }>>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'trips' | 'favourites'>('trips')
  const [deletingId, setDeletingId] = useState<number | null>(null)

  const loadData = async () => {
    setLoading(true)
    try {
      const [tripsRes, favsRes] = await Promise.all([tripsApi.getAll(), favouritesApi.getAll()])
      setTrips(tripsRes.data.trips)
      setFavourites(favsRes.data.favourites)
    } catch {
      toast.error('Failed to load trips from database')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleDelete = async (id: number, name: string) => {
    if (!confirm(`Are you sure you want to delete "${name}"?`)) return
    setDeletingId(id)
    try {
      await tripsApi.delete(id)
      setTrips(prev => prev.filter(t => t.id !== id))
      toast.success('Trip plan deleted')
    } catch {
      toast.error('Could not delete trip')
    } finally {
      setDeletingId(null)
    }
  }

  const handleRemoveFav = async (id: number, name: string) => {
    try {
      await favouritesApi.remove(id)
      setFavourites(prev => prev.filter(f => f.id !== id))
      toast.success(`Removed ${name} from favourites`)
    } catch {
      toast.error('Could not remove favourite')
    }
  }

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        <div className="max-w-7xl mx-auto px-6 pt-32 pb-16">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
            <div>
              <h1 className="text-3xl sm:text-4xl font-bold text-[#222222] tracking-tight">
                My Trips & Saved Destinations
              </h1>
              <p className="text-[#717171] text-sm mt-1">
                Access your previously computed itineraries and favorite spots persisted in SQLite.
              </p>
            </div>

            <Link
              to="/planner"
              className="px-5 py-2.5 rounded-xl bg-[#222222] hover:bg-[#333333] text-white text-xs font-medium transition-all shadow-sm flex items-center gap-1.5 self-start sm:self-auto cursor-pointer"
            >
              <Sparkles className="w-3.5 h-3.5" /> Plan New Trip
            </Link>
          </div>

          {/* Tab Selector - Underline style */}
          <div className="flex gap-6 mb-8 border-b border-[#DDDDDD] pb-3">
            <button
              onClick={() => setActiveTab('trips')}
              className={`text-sm font-medium transition-all cursor-pointer pb-1 border-b-2 ${
                activeTab === 'trips'
                  ? 'text-[#222222] border-[#222222]'
                  : 'text-[#717171] border-transparent hover:text-[#222222]'
              }`}
            >
              Generated Itineraries ({trips.length})
            </button>
            <button
              onClick={() => setActiveTab('favourites')}
              className={`text-sm font-medium transition-all cursor-pointer pb-1 border-b-2 ${
                activeTab === 'favourites'
                  ? 'text-[#222222] border-[#222222]'
                  : 'text-[#717171] border-transparent hover:text-[#222222]'
              }`}
            >
              Saved Wishlist ({favourites.length})
            </button>
          </div>

          {/* Content */}
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-64 rounded-2xl bg-stone-100 animate-pulse border border-[#DDDDDD]" />
              ))}
            </div>
          ) : activeTab === 'trips' ? (
            trips.length === 0 ? (
              <div className="text-center py-16 bg-white rounded-2xl border border-[#DDDDDD] p-8 max-w-lg mx-auto shadow-sm">
                <div className="w-14 h-14 rounded-2xl bg-[#F7F7F7] text-[#222222] flex items-center justify-center text-2xl mx-auto mb-4 border border-[#DDDDDD]">
                  🗺️
                </div>
                <h3 className="text-lg font-semibold text-[#222222]">No Trips Generated Yet</h3>
                <p className="text-xs text-[#717171] mt-1 mb-6 leading-relaxed">
                  You haven't run the ML itinerary generator yet. Create your first customized plan in less than 60 seconds!
                </p>
                <Link
                  to="/planner"
                  className="px-5 py-2.5 rounded-xl bg-[#222222] text-white text-xs font-medium hover:bg-[#333] transition-colors inline-block"
                >
                  Start Trip Planner Wizard →
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {trips.map(trip => (
                  <div
                    key={trip.id}
                    className="group bg-white rounded-2xl overflow-hidden border border-[#DDDDDD] shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between"
                  >
                    <div>
                      <div className="h-48 relative overflow-hidden bg-stone-100">
                        <img
                          src={
                            trip.destination_info?.image ||
                            'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80'
                          }
                          alt={trip.destination}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                          referrerPolicy="no-referrer"
                          loading="lazy"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
                        <span className="absolute top-3 left-3 px-2.5 py-1 rounded-full bg-white/95 text-xs font-medium text-[#222222] shadow-sm flex items-center gap-1">
                          <MapPin className="w-3 h-3 text-[#222222]" /> {trip.destination}
                        </span>
                        <span className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-black/60 text-white text-[11px] font-mono">
                          Trip #{trip.id}
                        </span>
                        <div className="absolute bottom-3 left-3 text-white">
                          <span className="text-xs text-stone-200 block">
                            {trip.days} Days · {trip.group_size} Travellers
                          </span>
                        </div>
                      </div>

                      <div className="p-5">
                        <h3 className="font-semibold text-[#222222] text-base mb-1">
                          {trip.destination} Expedition
                        </h3>
                        <p className="text-xs text-[#717171] line-clamp-1 mb-4">
                          Created {new Date(trip.created_at || Date.now()).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })}
                        </p>

                        <div className="p-3.5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] space-y-1.5 text-xs">
                          <div className="flex justify-between">
                            <span className="text-[#717171]">Total Cost:</span>
                            <strong className="text-[#222222] font-mono font-semibold">₹{trip.total_cost?.toLocaleString('en-IN')}</strong>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-[#717171]">Budget Target:</span>
                            <span className="text-[#008489] font-mono font-medium">₹{trip.budget?.toLocaleString('en-IN')}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="p-5 pt-0 flex gap-2">
                      <Link
                        to={`/trips/${trip.id}`}
                        className="flex-1 py-2 rounded-xl bg-[#222222] hover:bg-[#333333] text-white text-xs font-medium text-center transition-colors flex items-center justify-center gap-1.5"
                      >
                        <span>View Itinerary</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                      <button
                        onClick={() => handleDelete(trip.id, trip.destination)}
                        disabled={deletingId === trip.id}
                        className="p-2 rounded-xl border border-[#DDDDDD] text-[#717171] hover:text-rose-600 hover:bg-stone-100 transition-colors cursor-pointer"
                        title="Delete Trip"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )
          ) : (
            favourites.length === 0 ? (
              <div className="text-center py-16 bg-white rounded-2xl border border-[#DDDDDD] p-8 max-w-lg mx-auto shadow-sm">
                <div className="text-3xl mb-3">❤️</div>
                <h3 className="text-lg font-semibold text-[#222222]">No Wishlist Items Yet</h3>
                <p className="text-xs text-[#717171] mt-1 mb-6 leading-relaxed">
                  Browse through destinations and click the heart icon on any card to save it here.
                </p>
                <Link
                  to="/destinations"
                  className="px-5 py-2.5 rounded-xl bg-[#222222] text-white text-xs font-medium hover:bg-[#333] transition-colors inline-block"
                >
                  Browse Destinations →
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
                {favourites.map(fav => (
                  <div
                    key={fav.id}
                    className="p-4 rounded-2xl bg-white border border-[#DDDDDD] shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between"
                  >
                    <div className="h-36 rounded-xl overflow-hidden mb-3 relative bg-stone-100">
                      <img
                        src={fav.item_image || 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=400&q=80'}
                        alt={fav.item_name}
                        className="w-full h-full object-cover"
                        referrerPolicy="no-referrer"
                        loading="lazy"
                      />
                    </div>
                    <div>
                      <h4 className="font-semibold text-[#222222] text-sm mb-0.5">{fav.item_name}</h4>
                      <span className="text-[10px] text-[#717171] font-medium uppercase tracking-wider block mb-3">
                        {fav.item_type}
                      </span>
                    </div>
                    <div className="flex gap-2">
                      <Link
                        to={`/destinations/${encodeURIComponent(fav.item_name)}`}
                        className="flex-1 py-2 text-center rounded-xl border border-[#DDDDDD] bg-white hover:bg-[#F7F7F7] text-[#222222] text-xs font-medium"
                      >
                        View
                      </Link>
                      <button
                        onClick={() => handleRemoveFav(fav.id, fav.item_name)}
                        className="p-2 rounded-xl text-[#717171] hover:text-rose-600 hover:bg-stone-100 transition-colors cursor-pointer"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )
          )}
        </div>
      </div>

      <Footer />
    </div>
  )
}
