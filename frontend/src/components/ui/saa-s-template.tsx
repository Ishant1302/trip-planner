import React from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Compass, MapPin, ArrowRight, Star, Calendar, CheckCircle2, Menu, X
} from "lucide-react";

// Button Component matching template interface with clean minimal styling
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "ghost" | "gradient" | "teal" | "accent";
  size?: "default" | "sm" | "lg";
  children: React.ReactNode;
}

export const TemplateButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "default", size = "default", className = "", children, ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center justify-center gap-2 whitespace-nowrap font-medium transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 cursor-pointer select-none active:scale-[0.99]";

    const variants = {
      default:
        "bg-[#222222] text-white hover:bg-[#333333] rounded-xl",
      secondary:
        "bg-white text-[#222222] border border-[#DDDDDD] hover:bg-[#F7F7F7] rounded-xl",
      ghost:
        "text-[#717171] hover:text-[#222222] hover:bg-[#F7F7F7] rounded-xl",
      accent:
        "bg-[#008489] text-white hover:bg-[#006c70] rounded-xl",
      gradient:
        "bg-[#222222] text-white hover:bg-[#333333] rounded-xl",
      teal:
        "bg-[#008489] text-white hover:bg-[#006c70] rounded-xl",
    };

    const sizes = {
      default: "h-10 px-5 text-sm",
      sm: "h-9 px-4 text-xs font-medium",
      lg: "h-12 px-6 text-sm font-semibold",
    };

    return (
      <button
        ref={ref}
        className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);
TemplateButton.displayName = "TemplateButton";

// Navigation Component
export const TemplateNavigation = React.memo(() => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const [scrolled, setScrolled] = React.useState(false);

  React.useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 15);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-200 ${
        scrolled
          ? "bg-white/95 backdrop-blur-md border-b border-[#DDDDDD] shadow-sm py-3.5"
          : "bg-white/80 backdrop-blur-sm py-4"
      }`}
    >
      <nav className="max-w-7xl mx-auto px-6 w-full">
        <div className="flex items-center justify-between">
          {/* Brand Identity */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[#222222] flex items-center justify-center text-white">
              <Compass className="w-4 h-4" />
            </div>
            <span className="text-lg font-bold text-[#222222] tracking-tight">
              VoyageML
            </span>
          </Link>

          {/* Actual Application Navigation Links */}
          <div className="hidden lg:flex items-center gap-8">
            <Link
              to="/destinations"
              className="text-sm font-medium text-[#222222] hover:text-[#008489] transition-colors"
            >
              Explore Destinations
            </Link>
            <Link
              to="/planner"
              className="text-sm font-medium text-[#222222] hover:text-[#008489] transition-colors"
            >
              Plan a Trip
            </Link>
            <Link
              to="/my-trips"
              className="text-sm font-medium text-[#222222] hover:text-[#008489] transition-colors"
            >
              My Trips
            </Link>
            <Link
              to="/how-it-works"
              className="text-sm font-medium text-[#222222] hover:text-[#008489] transition-colors"
            >
              How It Works
            </Link>
            <Link
              to="/ml-dashboard"
              className="text-sm font-medium text-[#222222] hover:text-[#008489] transition-colors"
            >
              ML Insights
            </Link>
          </div>

          {/* Action CTAs */}
          <div className="hidden sm:flex items-center gap-3">
            <Link to="/about">
              <TemplateButton variant="ghost" size="sm">
                About Project
              </TemplateButton>
            </Link>
            <Link to="/planner">
              <TemplateButton variant="default" size="sm">
                Start Planning
              </TemplateButton>
            </Link>
          </div>

          {/* Mobile hamburger */}
          <button
            type="button"
            className="lg:hidden p-2 text-[#222222] hover:bg-[#F7F7F7] rounded-xl transition-colors cursor-pointer"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-white mt-3 border-t border-[#DDDDDD] px-6 py-6 shadow-lg">
          <div className="flex flex-col gap-4">
            <Link
              to="/destinations"
              className="text-base font-medium text-[#222222] hover:text-[#008489] py-1"
              onClick={() => setMobileMenuOpen(false)}
            >
              Explore Destinations
            </Link>
            <Link
              to="/planner"
              className="text-base font-medium text-[#222222] hover:text-[#008489] py-1"
              onClick={() => setMobileMenuOpen(false)}
            >
              Plan a Trip
            </Link>
            <Link
              to="/my-trips"
              className="text-base font-medium text-[#222222] hover:text-[#008489] py-1"
              onClick={() => setMobileMenuOpen(false)}
            >
              My Saved Trips
            </Link>
            <Link
              to="/how-it-works"
              className="text-base font-medium text-[#222222] hover:text-[#008489] py-1"
              onClick={() => setMobileMenuOpen(false)}
            >
              How the ML Pipeline Works
            </Link>
            <Link
              to="/ml-dashboard"
              className="text-base font-medium text-[#008489] font-semibold py-1"
              onClick={() => setMobileMenuOpen(false)}
            >
              ML Model Analytics
            </Link>
            <Link
              to="/about"
              className="text-base font-medium text-[#717171] hover:text-[#222222] py-1"
              onClick={() => setMobileMenuOpen(false)}
            >
              About Project
            </Link>
            <div className="pt-4 border-t border-[#DDDDDD] flex flex-col gap-2">
              <Link to="/planner" onClick={() => setMobileMenuOpen(false)}>
                <TemplateButton variant="default" className="w-full">
                  Start Planning
                </TemplateButton>
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  );
});
TemplateNavigation.displayName = "TemplateNavigation";

// Hero Component with Travel Visuals, Spacious Layout, and Live Showcase
export const TemplateHero = React.memo(() => {
  const navigate = useNavigate();
  const [quickDest, setQuickDest] = React.useState("Goa");
  const [quickDays, setQuickDays] = React.useState("3");

  const handleQuickPlan = (e: React.FormEvent) => {
    e.preventDefault();
    navigate(`/planner?destination=${encodeURIComponent(quickDest)}`);
  };

  return (
    <section className="relative pt-28 pb-16 lg:pt-36 lg:pb-24 bg-white border-b border-[#DDDDDD] w-full">
      <div className="max-w-7xl mx-auto px-6 w-full flex flex-col items-center">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto mb-10 w-full">
          {/* Subtle Tagline */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#F7F7F7] border border-[#DDDDDD] text-xs font-medium text-[#717171] mb-6">
            <span>Academic ML Project · Group 6</span>
            <span className="text-[#DDDDDD]">|</span>
            <Link
              to="/how-it-works"
              className="text-[#008489] hover:underline flex items-center gap-1 font-medium"
            >
              Explore ML Pipeline <ArrowRight size={12} />
            </Link>
          </div>

          {/* Hero Headline */}
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-bold text-[#222222] tracking-tight leading-tight max-w-3xl mx-auto mb-5 text-center">
            Your Journey. Your Interests.{" "}
            <span className="text-[#008489]">Your Perfect Trip.</span>
          </h1>

          {/* Hero Subtitle */}
          <p className="text-base sm:text-lg text-[#717171] font-normal leading-relaxed max-w-2xl mx-auto mb-8 text-center">
            Discover destinations, forecast travel budgets, and generate intelligent itineraries powered by Random Forest classification, K-Means clustering, and Ridge regression.
          </p>

          {/* Quick interactive planning strip */}
          <form
            onSubmit={handleQuickPlan}
            className="w-full max-w-2xl mx-auto bg-white border border-[#DDDDDD] rounded-2xl shadow-sm hover:shadow-md transition-shadow p-2 flex flex-col sm:flex-row items-center gap-2 mb-8"
          >
            <div className="flex-1 w-full flex items-center gap-3 px-4 py-2 border-b sm:border-b-0 sm:border-r border-[#DDDDDD]">
              <MapPin className="w-4 h-4 text-[#717171] shrink-0" />
              <div className="text-left w-full">
                <label className="text-[10px] font-semibold uppercase tracking-wider text-[#717171] block">
                  Destination
                </label>
                <select
                  value={quickDest}
                  onChange={(e) => setQuickDest(e.target.value)}
                  className="w-full bg-transparent text-sm font-semibold text-[#222222] focus:outline-none cursor-pointer"
                >
                  <option value="Goa">Goa (Beaches & Heritage)</option>
                  <option value="Jaipur">Jaipur (Pink City Forts)</option>
                  <option value="Kerala Backwaters">Kerala Backwaters (Lagoons)</option>
                  <option value="Manali">Manali (Himalayan Adventure)</option>
                  <option value="Leh Ladakh">Leh Ladakh (High Passes)</option>
                  <option value="Udaipur">Udaipur (City of Lakes)</option>
                  <option value="Varanasi">Varanasi (Sacred Ghats)</option>
                </select>
              </div>
            </div>

            <div className="w-full sm:w-36 flex items-center gap-3 px-4 py-2">
              <Calendar className="w-4 h-4 text-[#717171] shrink-0" />
              <div className="text-left w-full">
                <label className="text-[10px] font-semibold uppercase tracking-wider text-[#717171] block">
                  Duration
                </label>
                <select
                  value={quickDays}
                  onChange={(e) => setQuickDays(e.target.value)}
                  className="w-full bg-transparent text-sm font-semibold text-[#222222] focus:outline-none cursor-pointer"
                >
                  <option value="2">2 Days</option>
                  <option value="3">3 Days</option>
                  <option value="4">4 Days</option>
                  <option value="5">5 Days</option>
                  <option value="7">7 Days</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              className="w-full sm:w-auto bg-[#008489] hover:bg-[#006c70] text-white px-6 py-2.5 rounded-xl font-medium text-sm transition-colors flex items-center justify-center gap-1.5 cursor-pointer shrink-0"
            >
              Generate Plan <ArrowRight size={15} />
            </button>
          </form>

          {/* Social Proof Tags */}
          <div className="flex flex-wrap items-center justify-center gap-6 text-xs sm:text-sm text-[#717171]">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#008489]" /> 111 Verified Attractions
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#008489]" /> 89.1% Test F1 Accuracy
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#008489]" /> Strict Budget Solver
            </span>
          </div>
        </div>

        {/* Travel Showcase Preview Card */}
        <div className="relative w-full max-w-5xl mx-auto mt-6">
          <div className="bg-white rounded-2xl border border-[#DDDDDD] shadow-lg p-6 lg:p-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              {/* Visual Trip Showcase Card */}
              <div className="lg:col-span-7 space-y-5">
                <div className="relative h-72 sm:h-80 rounded-xl overflow-hidden group">
                  <img
                    src="https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=1000&q=80"
                    alt="Goa Beach and Architecture"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                  <div className="absolute top-4 left-4 flex gap-2">
                    <span className="px-3 py-1 rounded-full bg-white text-xs font-semibold text-[#222222] shadow-sm">
                      Beach & Culture
                    </span>
                    <span className="px-3 py-1 rounded-full bg-[#008489] text-white text-xs font-semibold shadow-sm">
                      92% Match Score
                    </span>
                  </div>
                  <div className="absolute bottom-5 left-5 right-5 text-white">
                    <h3 className="text-xl sm:text-2xl font-bold mb-1">
                      Goa Coastal & Heritage Expedition
                    </h3>
                    <div className="flex flex-wrap items-center gap-3 text-xs text-stone-200">
                      <span className="flex items-center gap-1 font-medium text-amber-300">
                        <Star className="w-3.5 h-3.5 fill-amber-300 text-amber-300" /> 4.6 Stars
                      </span>
                      <span>•</span>
                      <span>4 Days · 2 Travellers</span>
                      <span>•</span>
                      <span className="font-semibold text-white">₹23,635 Est. Cost (Within Budget)</span>
                    </div>
                  </div>
                </div>

                {/* Micro timeline sample */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="p-3.5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                    <span className="text-[10px] font-semibold text-[#008489] uppercase tracking-wider block mb-1">
                      Morning · 09:30 AM
                    </span>
                    <h4 className="font-bold text-[#222222] text-xs">Fort Aguada Lighthouse</h4>
                    <p className="text-[11px] text-[#717171] mt-0.5">Historical visit · 2.0h</p>
                  </div>
                  <div className="p-3.5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                    <span className="text-[10px] font-semibold text-[#008489] uppercase tracking-wider block mb-1">
                      Afternoon · 01:00 PM
                    </span>
                    <h4 className="font-bold text-[#222222] text-xs">Spice Plantation Tour</h4>
                    <p className="text-[11px] text-[#717171] mt-0.5">Goan lunch · 3.0h</p>
                  </div>
                  <div className="p-3.5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                    <span className="text-[10px] font-semibold text-[#008489] uppercase tracking-wider block mb-1">
                      Evening · 05:30 PM
                    </span>
                    <h4 className="font-bold text-[#222222] text-xs">Palolem Sunset Cruise</h4>
                    <p className="text-[11px] text-[#717171] mt-0.5">Nature & leisure · 2.5h</p>
                  </div>
                </div>
              </div>

              {/* Right Analytics Box */}
              <div className="lg:col-span-5 bg-[#F7F7F7] rounded-xl p-6 border border-[#DDDDDD] space-y-6">
                <div>
                  <span className="text-xs font-semibold text-[#008489] uppercase tracking-wider block mb-1">
                    K-Means Traveller Profile
                  </span>
                  <h4 className="text-lg font-bold text-[#222222]">Relaxed Leisure Traveller</h4>
                  <p className="text-xs text-[#717171] mt-1">
                    High preference for scenic landscapes and coastal leisure with comfortable pacing.
                  </p>
                </div>

                {/* Signal bars */}
                <div className="space-y-3 pt-3 border-t border-[#DDDDDD]">
                  <div>
                    <div className="flex justify-between text-xs font-medium mb-1">
                      <span className="text-[#717171]">Random Forest Confidence</span>
                      <span className="text-[#222222] font-semibold">92.4%</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-[#DDDDDD] overflow-hidden">
                      <div className="h-full bg-[#222222] rounded-full w-[92%]" />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-medium mb-1">
                      <span className="text-[#717171]">Ridge Cost Regression Fit</span>
                      <span className="text-[#008489] font-semibold">R² = 0.9367</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-[#DDDDDD] overflow-hidden">
                      <div className="h-full bg-[#008489] rounded-full w-[94%]" />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-medium mb-1">
                      <span className="text-[#717171]">Constraint Adherence</span>
                      <span className="text-[#222222] font-semibold">100% Guaranteed</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-[#DDDDDD] overflow-hidden">
                      <div className="h-full bg-[#222222] rounded-full w-full" />
                    </div>
                  </div>
                </div>

                {/* Call to action within preview */}
                <div className="pt-4 border-t border-[#DDDDDD] flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-[#717171] block">Try with your preferences</span>
                    <strong className="text-xs text-[#222222]">Ready in 2 seconds</strong>
                  </div>
                  <Link to="/planner">
                    <TemplateButton variant="default" size="sm">
                      Create Your Trip →
                    </TemplateButton>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
});
TemplateHero.displayName = "TemplateHero";

// Main Component Default Export
export default function Component() {
  return (
    <main className="min-h-screen bg-[#F7F7F7] text-[#222222]">
      <TemplateNavigation />
      <TemplateHero />
    </main>
  );
}
