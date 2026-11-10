import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'sonner'
import HomePage from '@/pages/HomePage'
import DestinationsPage from '@/pages/DestinationsPage'
import DestinationDetailPage from '@/pages/DestinationDetailPage'
import PlannerPage from '@/pages/PlannerPage'
import TripResultPage from '@/pages/TripResultPage'
import MyTripsPage from '@/pages/MyTripsPage'
import MLDashboardPage from '@/pages/MLDashboardPage'
import HowItWorksPage from '@/pages/HowItWorksPage'
import AboutPage from '@/pages/AboutPage'

export default function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" richColors expand toastOptions={{ duration: 4000 }} />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/destinations" element={<DestinationsPage />} />
        <Route path="/destinations/:name" element={<DestinationDetailPage />} />
        <Route path="/planner" element={<PlannerPage />} />
        <Route path="/trips/:id" element={<TripResultPage />} />
        <Route path="/my-trips" element={<MyTripsPage />} />
        <Route path="/ml-dashboard" element={<MLDashboardPage />} />
        <Route path="/how-it-works" element={<HowItWorksPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </BrowserRouter>
  )
}
