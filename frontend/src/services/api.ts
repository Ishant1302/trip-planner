import axios from 'axios'

const API_BASE = '/api'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

// ─── Types ───────────────────────────────────────────────────────────────────

export interface Destination {
  destination_id?: number
  destination: string
  country: string
  region?: string
  image?: string
  description?: string
  avg_rating: number
  avg_cost_per_day: number
  best_duration_days: number
  categories?: string[]
  best_season?: string
  latitude?: number
  longitude?: number
}

export interface Place {
  place_id: number
  place_name: string
  destination: string
  category: string
  nature_score: number
  adventure_score: number
  food_score: number
  history_score: number
  shopping_score: number
  culture_score: number
  average_cost: number
  time_needed: number
  rating: number
  location: string
  distance_from_city_centre: number
  image?: string
  description?: string
  time_of_day?: string
  time_slot?: string
  rf_probability?: number
  like_probability?: number
  like_probability_pct?: string
  composite_score?: number
  final_recommendation_score?: number
  interest_match?: number
  budget_fit?: number
  reasons?: string[]
  ml_explanation?: string
}

export interface TripGenerateRequest {
  destination: string
  budget: number
  days: number
  group_size: number
  food_preference: string
  nature_interest: number
  adventure_interest: number
  food_interest: number
  history_interest: number
  shopping_interest: number
  culture_interest: number
  walking_comfort: string
  accommodation_type: string
  transport_preference: string
  trip_pace: string
  group_type: string
  additional_notes?: string
}

export interface TripResult {
  trip_id: number
  destination: string
  destination_info: { image: string; description: string; avg_cost_per_day: number }
  days: number
  group_size: number
  budget: number
  traveller_profile: { label: string; description: string; cluster_id: number }
  total_estimated_cost: number
  cost_per_person: number
  daily_cost: number
  budget_remaining: number
  over_budget: boolean
  regression_cost_estimate?: number
  regression_time_estimate?: number
  budget_breakdown: {
    accommodation: number
    transport: number
    food: number
    activities: number
    misc: number
    total: number
  }
  recommendations: Place[]
  recommended_places?: Place[]
  itinerary: Record<string, {
    day: number
    title: string
    day_title?: string
    places: (Place & { time_of_day: string })[]
    total_cost: number
    total_time: number
  }>
  constraint_report: {
    violations: string[]
    adjustments: string[]
    total_activity_hours: number
    total_activity_time_hours?: number
    available_time_hours: number
  }
  ml_insights: {
    traveller_profile: string
    cluster_description: string
    avg_rf_probability: number
    avg_recommendation_score: number
    top_place_probability: number
    models_used: string[]
  }
}

export interface SavedTrip {
  id: number
  name: string
  destination: string
  days: number
  group_size: number
  budget: number
  status: string
  created_at?: string
  total_cost?: number
  traveller_profile?: string
  destination_info?: { image?: string; description?: string }
}

// ─── API Functions ────────────────────────────────────────────────────────────

export const destinationsApi = {
  getAll: (params?: { search?: string; category?: string; min_rating?: number; max_budget?: number; sort_by?: string }) =>
    api.get<{ destinations: Destination[]; total: number }>('/destinations', { params }),

  getByName: (name: string) =>
    api.get<{ destination: Destination; places: Place[] }>(`/destinations/${encodeURIComponent(name)}`),

  getNames: () =>
    api.get<{ names: string[] }>('/destinations/names'),
}

export const tripsApi = {
  generate: (data: TripGenerateRequest) =>
    api.post<TripResult>('/trips/generate', data),

  getAll: (session: string = 'demo') =>
    api.get<{ trips: SavedTrip[] }>('/trips', { params: { user_session: session } }),

  getById: (id: number) =>
    api.get<TripResult & { id: number }>(`/trips/${id}`),

  update: (id: number, data: { itinerary?: Record<string, unknown>; name?: string; status?: string; total_cost?: number }) =>
    api.put(`/trips/${id}`, data),

  delete: (id: number) =>
    api.delete(`/trips/${id}`),
}

export const favouritesApi = {
  add: (data: { item_type: string; item_id: string; item_name: string; item_image?: string }) =>
    api.post('/favourites', { ...data, user_session: 'demo' }),

  getAll: () =>
    api.get<{ favourites: Array<{ id: number; item_type: string; item_id: string; item_name: string; item_image?: string }> }>('/favourites', {
      params: { user_session: 'demo' }
    }),

  remove: (id: number) =>
    api.delete(`/favourites/${id}`),
}

export const mlApi = {
  getMetrics: () => api.get('/ml/metrics'),
  getClassification: () => api.get('/ml/classification'),
  getClustering: () => api.get('/ml/clustering'),
  getRegression: () => api.get('/ml/regression'),
  getFeatureImportance: () => api.get('/ml/feature-importance'),
  train: () => api.post('/ml/train'),
  getDatasetStats: () => api.get('/ml/dataset-stats'),
}

export const healthApi = {
  check: () => api.get('/health'),
}

export const updatePlaceImage = async (data: { place_name: string; destination?: string; image_url: string }) => {
  const res = await api.put('/places/image', data)
  return res.data
}

export const updateDestinationImage = async (data: { destination: string; image_url: string }) => {
  const res = await api.put('/destinations/image', data)
  return res.data
}

export interface ImageUploadResponse {
  success: boolean
  image_url: string
  filename: string
  trips_updated?: number
  place_name?: string
  destination?: string
  message: string
}

export const uploadImageFromLaptop = async (data: {
  filename: string
  data_base64: string
  place_name?: string
  destination?: string
  item_type?: 'place' | 'destination'
}) => {
  const res = await api.post<ImageUploadResponse>('/upload-image', data)
  return res.data
}

export const getAllPlaces = async (destination?: string, search?: string) => {
  const res = await api.get<{ places: Place[]; total: number }>('/places', {
    params: { destination, search }
  })
  return res.data
}
