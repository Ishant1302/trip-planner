import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Compass } from 'lucide-react'
import { cn } from '@/lib/utils'

const NAV_LINKS = [
  { label: 'Explore Destinations', href: '/destinations' },
  { label: 'Plan a Trip', href: '/planner' },
  { label: 'My Saved Trips', href: '/my-trips' },
  { label: 'How It Works', href: '/how-it-works' },
  { label: 'ML Insights', href: '/ml-dashboard' },
]

export default function Navbar({ dark = false }: { dark?: boolean }) {
  // Keep dark prop signature intact for compatibility, but render clean light theme
  const [mobileOpen, setMobileOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 15)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  const isActive = (href: string) => location.pathname === href

  return (
    <header
      className={cn(
        'fixed top-0 left-0 right-0 z-50 bg-white border-b border-[#DDDDDD] transition-all duration-200',
        scrolled ? 'shadow-sm py-3.5' : 'py-4'
      )}
    >
      <nav className="max-w-7xl mx-auto px-6 w-full">
        <div className="flex items-center justify-between">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[#222222] flex items-center justify-center text-white">
              <Compass className="w-4 h-4" />
            </div>
            <span className="text-lg font-bold text-[#222222] tracking-tight">
              VoyageML
            </span>
          </Link>

          {/* Desktop Nav Items */}
          <div className="hidden lg:flex items-center gap-7">
            {NAV_LINKS.map(link => {
              const active = isActive(link.href)
              return (
                <Link
                  key={link.href}
                  to={link.href}
                  className={cn(
                    'text-sm transition-colors cursor-pointer py-1',
                    active
                      ? 'text-[#222222] font-semibold border-b-2 border-[#222222]'
                      : 'text-[#717171] font-medium hover:text-[#222222]'
                  )}
                >
                  {link.label}
                </Link>
              )
            })}
          </div>

          {/* Action CTAs */}
          <div className="hidden sm:flex items-center gap-4">
            <Link
              to="/about"
              className="text-sm font-medium text-[#717171] hover:text-[#222222] transition-colors"
            >
              About Project
            </Link>
            <Link to="/planner">
              <button className="bg-[#222222] text-white px-5 py-2 rounded-xl text-sm font-medium hover:bg-[#333333] transition-colors cursor-pointer">
                Start Planning
              </button>
            </Link>
          </div>

          {/* Mobile hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="lg:hidden p-2 rounded-xl text-[#222222] hover:bg-[#F7F7F7] transition-colors cursor-pointer"
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </nav>

      {/* Mobile Drawer */}
      {mobileOpen && (
        <div className="lg:hidden bg-white border-t border-[#DDDDDD] px-6 py-6 shadow-lg">
          <div className="flex flex-col gap-3">
            {NAV_LINKS.map(link => {
              const active = isActive(link.href)
              return (
                <Link
                  key={link.href}
                  to={link.href}
                  onClick={() => setMobileOpen(false)}
                  className={cn(
                    'text-base font-medium py-1.5 transition-colors',
                    active
                      ? 'text-[#008489] font-semibold'
                      : 'text-[#222222] hover:text-[#008489]'
                  )}
                >
                  {link.label}
                </Link>
              )
            })}
            <Link
              to="/about"
              onClick={() => setMobileOpen(false)}
              className="text-base font-medium text-[#717171] hover:text-[#222222] py-1.5"
            >
              About Project
            </Link>
            <div className="pt-4 mt-1 border-t border-[#DDDDDD]">
              <Link to="/planner" onClick={() => setMobileOpen(false)}>
                <button className="w-full bg-[#222222] text-white py-3 rounded-xl text-sm font-medium hover:bg-[#333333] transition-colors">
                  Start Planning
                </button>
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}
