"""
Dataset Generator for Trip Planner System
Generates realistic synthetic datasets for ML training.
All data is simulated/synthetic and clearly documented as such.
"""

import pandas as pd
import numpy as np
import os
import json
from pathlib import Path

# Set seed for reproducibility
np.random.seed(42)

DATASETS_DIR = Path(__file__).parent
DATASETS_DIR.mkdir(exist_ok=True)


# ─── Destination & Place Data ───────────────────────────────────────────────

DESTINATIONS_DATA = [
    # Indian destinations
    {"destination": "Goa", "country": "India", "region": "South India",
     "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80",
     "description": "Sun-kissed beaches, vibrant nightlife and Portuguese heritage make Goa India's most beloved coastal destination.",
     "avg_rating": 4.4, "avg_cost_per_day": 3500, "best_duration_days": 4,
     "categories": ["Relaxation", "Adventure", "Food"], "best_season": "Nov-Feb",
     "latitude": 15.2993, "longitude": 74.1240},
    {"destination": "Jaipur", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800&q=80",
     "description": "The Pink City dazzles with magnificent forts, opulent palaces and vibrant bazaars steeped in Rajput glory.",
     "avg_rating": 4.5, "avg_cost_per_day": 2800, "best_duration_days": 3,
     "categories": ["History", "Culture", "Shopping"], "best_season": "Oct-Mar",
     "latitude": 26.9124, "longitude": 75.7873},
    {"destination": "Kerala Backwaters", "country": "India", "region": "South India",
     "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&q=80",
     "description": "Tranquil houseboat cruises through emerald lagoons and lush tropical landscapes in God's Own Country.",
     "avg_rating": 4.7, "avg_cost_per_day": 4200, "best_duration_days": 5,
     "categories": ["Nature", "Relaxation", "Culture"], "best_season": "Sep-Mar",
     "latitude": 9.4981, "longitude": 76.3388},
    {"destination": "Manali", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&q=80",
     "description": "Adventure capital of India with dramatic Himalayan peaks, snow-covered passes and thrilling outdoor sports.",
     "avg_rating": 4.5, "avg_cost_per_day": 3200, "best_duration_days": 5,
     "categories": ["Adventure", "Nature"], "best_season": "Apr-Jun, Oct-Nov",
     "latitude": 32.2396, "longitude": 77.1887},
    {"destination": "Agra", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80",
     "description": "Home to the iconic Taj Mahal — the world's greatest monument to love — and other Mughal architectural marvels.",
     "avg_rating": 4.3, "avg_cost_per_day": 2500, "best_duration_days": 2,
     "categories": ["History", "Culture"], "best_season": "Oct-Mar",
     "latitude": 27.1767, "longitude": 78.0081},
    {"destination": "Mumbai", "country": "India", "region": "West India",
     "image": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=800&q=80",
     "description": "India's maximum city — a mesmerizing blend of colonial architecture, street food, Bollywood glamour and coastal beauty.",
     "avg_rating": 4.2, "avg_cost_per_day": 4500, "best_duration_days": 3,
     "categories": ["Food", "Shopping", "Culture"], "best_season": "Nov-Feb",
     "latitude": 19.0760, "longitude": 72.8777},
    {"destination": "Leh Ladakh", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&q=80",
     "description": "Stark lunar landscapes, ancient Buddhist monasteries and world's highest motorable roads in the Himalayas.",
     "avg_rating": 4.8, "avg_cost_per_day": 5000, "best_duration_days": 7,
     "categories": ["Adventure", "Nature", "Culture"], "best_season": "Jun-Sep",
     "latitude": 34.1526, "longitude": 77.5771},
    {"destination": "Rishikesh", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?w=800&q=80",
     "description": "Yoga capital of the world with sacred ghats, white-water rafting and serene Himalayan foothills.",
     "avg_rating": 4.4, "avg_cost_per_day": 2200, "best_duration_days": 3,
     "categories": ["Adventure", "Culture", "Nature"], "best_season": "Sep-Jun",
     "latitude": 30.0869, "longitude": 78.2676},
    {"destination": "Udaipur", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=800&q=80",
     "description": "City of Lakes where shimmering water palaces, romantic sunsets and Rajasthani grandeur create pure magic.",
     "avg_rating": 4.6, "avg_cost_per_day": 3000, "best_duration_days": 3,
     "categories": ["History", "Relaxation", "Culture"], "best_season": "Sep-Mar",
     "latitude": 24.5854, "longitude": 73.7125},
    {"destination": "Varanasi", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1561361058-c24cecae35ca?w=800&q=80",
     "description": "One of world's oldest living cities — sacred ghats, ancient temples and mesmerizing Ganga Aarti ceremonies.",
     "avg_rating": 4.3, "avg_cost_per_day": 2000, "best_duration_days": 2,
     "categories": ["History", "Culture"], "best_season": "Oct-Mar",
     "latitude": 25.3176, "longitude": 82.9739},
    {"destination": "Coorg", "country": "India", "region": "South India",
     "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&q=80",
     "description": "Scotland of India — misty coffee and spice plantations, lush forests and serene waterfalls.",
     "avg_rating": 4.4, "avg_cost_per_day": 3800, "best_duration_days": 3,
     "categories": ["Nature", "Relaxation"], "best_season": "Oct-Jun",
     "latitude": 12.3375, "longitude": 75.8069},
    {"destination": "Darjeeling", "country": "India", "region": "East India",
     "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80",
     "description": "Queen of Hills with world-famous tea gardens, the Toy Train and stunning Himalayan panoramas.",
     "avg_rating": 4.3, "avg_cost_per_day": 2800, "best_duration_days": 3,
     "categories": ["Nature", "Culture"], "best_season": "Mar-May, Sep-Nov",
     "latitude": 27.0360, "longitude": 88.2627},
    {"destination": "Hampi", "country": "India", "region": "South India",
     "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&q=80",
     "description": "UNESCO World Heritage Site — dramatic boulder landscapes dotted with magnificent ruins of the Vijayanagara Empire.",
     "avg_rating": 4.5, "avg_cost_per_day": 1800, "best_duration_days": 2,
     "categories": ["History", "Adventure"], "best_season": "Nov-Feb",
     "latitude": 15.3350, "longitude": 76.4600},
    {"destination": "Andaman Islands", "country": "India", "region": "Islands",
     "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
     "description": "Pristine tropical islands with crystal-clear waters, vibrant coral reefs and powder-white beaches.",
     "avg_rating": 4.7, "avg_cost_per_day": 5500, "best_duration_days": 6,
     "categories": ["Adventure", "Relaxation", "Nature"], "best_season": "Nov-May",
     "latitude": 11.7401, "longitude": 92.6586},
    {"destination": "Kolkata", "country": "India", "region": "East India",
     "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",
     "description": "City of Joy — rich literary heritage, colonial architecture, legendary street food and vibrant cultural scene.",
     "avg_rating": 4.1, "avg_cost_per_day": 2500, "best_duration_days": 3,
     "categories": ["Culture", "Food", "History"], "best_season": "Oct-Feb",
     "latitude": 22.5726, "longitude": 88.3639},
    {"destination": "Mysore", "country": "India", "region": "South India",
     "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&q=80",
     "description": "City of Palaces with magnificent royal heritage, fragrant sandalwood, silk sarees and grand Dasara festivities.",
     "avg_rating": 4.3, "avg_cost_per_day": 2200, "best_duration_days": 2,
     "categories": ["History", "Culture", "Shopping"], "best_season": "Oct-Mar",
     "latitude": 12.2958, "longitude": 76.6394},
    {"destination": "Spiti Valley", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&q=80",
     "description": "Cold desert mountain valley in Himachal Pradesh with ancient monasteries, starry skies and raw Himalayan beauty.",
     "avg_rating": 4.8, "avg_cost_per_day": 4000, "best_duration_days": 7,
     "categories": ["Adventure", "Nature", "Culture"], "best_season": "Jun-Sep",
     "latitude": 32.2461, "longitude": 78.0338},
    {"destination": "Ooty", "country": "India", "region": "South India",
     "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80",
     "description": "Queen of Hill Stations with rolling Nilgiri tea estates, scenic mountain railways and pleasant cool climate.",
     "avg_rating": 4.1, "avg_cost_per_day": 2600, "best_duration_days": 3,
     "categories": ["Nature", "Relaxation"], "best_season": "Apr-Jun, Sep-Nov",
     "latitude": 11.4102, "longitude": 76.6950},
    {"destination": "Jaisalmer", "country": "India", "region": "North India",
     "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800&q=80",
     "description": "Golden City rising from the Thar Desert — sandstone haveli architecture, camel safaris and starlit desert camps.",
     "avg_rating": 4.5, "avg_cost_per_day": 3000, "best_duration_days": 3,
     "categories": ["Adventure", "History", "Culture"], "best_season": "Oct-Mar",
     "latitude": 26.9157, "longitude": 70.9083},
    {"destination": "Munnar", "country": "India", "region": "South India",
     "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&q=80",
     "description": "Breathtaking tea country with emerald hillsides, misty valleys, exotic wildlife and romantic mountain retreats.",
     "avg_rating": 4.5, "avg_cost_per_day": 3500, "best_duration_days": 3,
     "categories": ["Nature", "Relaxation"], "best_season": "Sep-May",
     "latitude": 10.0889, "longitude": 77.0595},
]

# ─── Places per Destination ──────────────────────────────────────────────────

PLACES_TEMPLATES = {
    "Goa": [
        {"place_name": "Baga Beach", "category": "Relaxation",
         "nature_score": 3, "adventure_score": 4, "food_score": 4,
         "history_score": 1, "shopping_score": 3, "culture_score": 2,
         "average_cost": 500, "time_needed": 3, "rating": 4.4,
         "location": "North Goa", "distance_from_city_centre": 12,
         "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80"},
        {"place_name": "Fort Aguada", "category": "History",
         "nature_score": 2, "adventure_score": 2, "food_score": 1,
         "history_score": 5, "shopping_score": 2, "culture_score": 4,
         "average_cost": 300, "time_needed": 2, "rating": 4.2,
         "location": "Sinquerim", "distance_from_city_centre": 15,
         "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80"},
        {"place_name": "Dudhsagar Waterfalls", "category": "Nature",
         "nature_score": 5, "adventure_score": 4, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 2,
         "average_cost": 800, "time_needed": 5, "rating": 4.6,
         "location": "Eastern Goa", "distance_from_city_centre": 60,
         "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80"},
        {"place_name": "Anjuna Flea Market", "category": "Shopping",
         "nature_score": 1, "adventure_score": 2, "food_score": 3,
         "history_score": 2, "shopping_score": 5, "culture_score": 3,
         "average_cost": 1500, "time_needed": 3, "rating": 4.0,
         "location": "North Goa", "distance_from_city_centre": 18,
         "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80"},
        {"place_name": "Palolem Beach", "category": "Relaxation",
         "nature_score": 5, "adventure_score": 3, "food_score": 3,
         "history_score": 1, "shopping_score": 2, "culture_score": 2,
         "average_cost": 400, "time_needed": 4, "rating": 4.7,
         "location": "South Goa", "distance_from_city_centre": 65,
         "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80"},
        {"place_name": "Spice Plantation Tour", "category": "Culture",
         "nature_score": 4, "adventure_score": 2, "food_score": 5,
         "history_score": 3, "shopping_score": 3, "culture_score": 5,
         "average_cost": 600, "time_needed": 3, "rating": 4.3,
         "location": "Ponda", "distance_from_city_centre": 30,
         "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80"},
    ],
    "Jaipur": [
        {"place_name": "Amber Fort", "category": "History",
         "nature_score": 2, "adventure_score": 3, "food_score": 1,
         "history_score": 5, "shopping_score": 2, "culture_score": 5,
         "average_cost": 500, "time_needed": 3, "rating": 4.7,
         "location": "Amer", "distance_from_city_centre": 11,
         "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&q=80"},
        {"place_name": "City Palace", "category": "History",
         "nature_score": 1, "adventure_score": 1, "food_score": 1,
         "history_score": 5, "shopping_score": 2, "culture_score": 5,
         "average_cost": 400, "time_needed": 2, "rating": 4.5,
         "location": "Central Jaipur", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&q=80"},
        {"place_name": "Hawa Mahal", "category": "History",
         "nature_score": 1, "adventure_score": 1, "food_score": 1,
         "history_score": 4, "shopping_score": 1, "culture_score": 4,
         "average_cost": 200, "time_needed": 1, "rating": 4.3,
         "location": "Central Jaipur", "distance_from_city_centre": 2,
         "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&q=80"},
        {"place_name": "Johari Bazaar", "category": "Shopping",
         "nature_score": 1, "adventure_score": 1, "food_score": 3,
         "history_score": 3, "shopping_score": 5, "culture_score": 4,
         "average_cost": 2000, "time_needed": 2, "rating": 4.2,
         "location": "Central Jaipur", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&q=80"},
        {"place_name": "Nahargarh Fort", "category": "Adventure",
         "nature_score": 4, "adventure_score": 4, "food_score": 1,
         "history_score": 4, "shopping_score": 1, "culture_score": 3,
         "average_cost": 300, "time_needed": 2, "rating": 4.4,
         "location": "North Jaipur", "distance_from_city_centre": 6,
         "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&q=80"},
        {"place_name": "Chokhi Dhani", "category": "Culture",
         "nature_score": 2, "adventure_score": 3, "food_score": 5,
         "history_score": 3, "shopping_score": 3, "culture_score": 5,
         "average_cost": 800, "time_needed": 4, "rating": 4.5,
         "location": "South Jaipur", "distance_from_city_centre": 20,
         "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&q=80"},
    ],
    "Kerala Backwaters": [
        {"place_name": "Alleppey Houseboat Cruise", "category": "Relaxation",
         "nature_score": 5, "adventure_score": 2, "food_score": 4,
         "history_score": 2, "shopping_score": 1, "culture_score": 4,
         "average_cost": 5000, "time_needed": 8, "rating": 4.8,
         "location": "Alleppey", "distance_from_city_centre": 0,
         "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80"},
        {"place_name": "Kumarakom Bird Sanctuary", "category": "Nature",
         "nature_score": 5, "adventure_score": 2, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 2,
         "average_cost": 400, "time_needed": 3, "rating": 4.5,
         "location": "Kumarakom", "distance_from_city_centre": 14,
         "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80"},
        {"place_name": "Kathakali Performance", "category": "Culture",
         "nature_score": 1, "adventure_score": 1, "food_score": 1,
         "history_score": 3, "shopping_score": 1, "culture_score": 5,
         "average_cost": 500, "time_needed": 2, "rating": 4.6,
         "location": "Kochi", "distance_from_city_centre": 25,
         "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80"},
        {"place_name": "Kochi Fort Area", "category": "History",
         "nature_score": 2, "adventure_score": 1, "food_score": 4,
         "history_score": 5, "shopping_score": 3, "culture_score": 4,
         "average_cost": 600, "time_needed": 3, "rating": 4.4,
         "location": "Fort Kochi", "distance_from_city_centre": 25,
         "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80"},
        {"place_name": "Munroe Island Canoe Tour", "category": "Adventure",
         "nature_score": 5, "adventure_score": 4, "food_score": 2,
         "history_score": 1, "shopping_score": 1, "culture_score": 3,
         "average_cost": 800, "time_needed": 4, "rating": 4.6,
         "location": "Kollam", "distance_from_city_centre": 40,
         "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80"},
        {"place_name": "Kerala Ayurveda Spa", "category": "Relaxation",
         "nature_score": 3, "adventure_score": 1, "food_score": 2,
         "history_score": 2, "shopping_score": 1, "culture_score": 4,
         "average_cost": 2500, "time_needed": 3, "rating": 4.7,
         "location": "Alleppey", "distance_from_city_centre": 5,
         "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80"},
    ],
    "Manali": [
        {"place_name": "Rohtang Pass", "category": "Adventure",
         "nature_score": 5, "adventure_score": 5, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 2,
         "average_cost": 1500, "time_needed": 6, "rating": 4.6,
         "location": "Kullu District", "distance_from_city_centre": 51,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Solang Valley Skiing", "category": "Adventure",
         "nature_score": 4, "adventure_score": 5, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 1,
         "average_cost": 2000, "time_needed": 5, "rating": 4.5,
         "location": "Solang Nala", "distance_from_city_centre": 14,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Hadimba Temple", "category": "Culture",
         "nature_score": 3, "adventure_score": 1, "food_score": 1,
         "history_score": 4, "shopping_score": 2, "culture_score": 5,
         "average_cost": 100, "time_needed": 1, "rating": 4.4,
         "location": "Old Manali", "distance_from_city_centre": 3,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Beas River Rafting", "category": "Adventure",
         "nature_score": 4, "adventure_score": 5, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 1,
         "average_cost": 1200, "time_needed": 3, "rating": 4.5,
         "location": "Kullu", "distance_from_city_centre": 40,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Naggar Castle", "category": "History",
         "nature_score": 3, "adventure_score": 2, "food_score": 1,
         "history_score": 5, "shopping_score": 1, "culture_score": 4,
         "average_cost": 200, "time_needed": 2, "rating": 4.2,
         "location": "Naggar", "distance_from_city_centre": 22,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Great Himalayan National Park", "category": "Nature",
         "nature_score": 5, "adventure_score": 4, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 2,
         "average_cost": 1000, "time_needed": 6, "rating": 4.7,
         "location": "Kullu", "distance_from_city_centre": 60,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
    ],
    "Agra": [
        {"place_name": "Taj Mahal", "category": "History",
         "nature_score": 2, "adventure_score": 1, "food_score": 1,
         "history_score": 5, "shopping_score": 2, "culture_score": 5,
         "average_cost": 1300, "time_needed": 3, "rating": 4.9,
         "location": "Taj Ganj", "distance_from_city_centre": 3,
         "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=600&q=80"},
        {"place_name": "Agra Fort", "category": "History",
         "nature_score": 2, "adventure_score": 1, "food_score": 1,
         "history_score": 5, "shopping_score": 1, "culture_score": 5,
         "average_cost": 650, "time_needed": 2, "rating": 4.5,
         "location": "Central Agra", "distance_from_city_centre": 2,
         "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=600&q=80"},
        {"place_name": "Fatehpur Sikri", "category": "History",
         "nature_score": 2, "adventure_score": 1, "food_score": 1,
         "history_score": 5, "shopping_score": 1, "culture_score": 4,
         "average_cost": 500, "time_needed": 3, "rating": 4.4,
         "location": "Fatehpur Sikri", "distance_from_city_centre": 40,
         "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=600&q=80"},
        {"place_name": "Kinari Bazaar", "category": "Shopping",
         "nature_score": 1, "adventure_score": 1, "food_score": 3,
         "history_score": 2, "shopping_score": 5, "culture_score": 3,
         "average_cost": 1500, "time_needed": 2, "rating": 4.0,
         "location": "Central Agra", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=600&q=80"},
    ],
    "Mumbai": [
        {"place_name": "Gateway of India", "category": "History",
         "nature_score": 2, "adventure_score": 1, "food_score": 2,
         "history_score": 5, "shopping_score": 2, "culture_score": 4,
         "average_cost": 300, "time_needed": 1, "rating": 4.4,
         "location": "Colaba", "distance_from_city_centre": 3,
         "image": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=600&q=80"},
        {"place_name": "Marine Drive", "category": "Relaxation",
         "nature_score": 3, "adventure_score": 1, "food_score": 3,
         "history_score": 2, "shopping_score": 2, "culture_score": 3,
         "average_cost": 200, "time_needed": 2, "rating": 4.5,
         "location": "Nariman Point", "distance_from_city_centre": 2,
         "image": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=600&q=80"},
        {"place_name": "Dharavi Tour", "category": "Culture",
         "nature_score": 1, "adventure_score": 2, "food_score": 4,
         "history_score": 3, "shopping_score": 3, "culture_score": 5,
         "average_cost": 500, "time_needed": 3, "rating": 4.3,
         "location": "Dharavi", "distance_from_city_centre": 8,
         "image": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=600&q=80"},
        {"place_name": "Colaba Causeway", "category": "Shopping",
         "nature_score": 1, "adventure_score": 1, "food_score": 3,
         "history_score": 2, "shopping_score": 5, "culture_score": 3,
         "average_cost": 2000, "time_needed": 2, "rating": 4.1,
         "location": "Colaba", "distance_from_city_centre": 3,
         "image": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=600&q=80"},
        {"place_name": "Elephanta Caves", "category": "History",
         "nature_score": 3, "adventure_score": 2, "food_score": 1,
         "history_score": 5, "shopping_score": 1, "culture_score": 4,
         "average_cost": 700, "time_needed": 4, "rating": 4.4,
         "location": "Elephanta Island", "distance_from_city_centre": 10,
         "image": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=600&q=80"},
        {"place_name": "Juhu Beach Street Food", "category": "Food",
         "nature_score": 2, "adventure_score": 1, "food_score": 5,
         "history_score": 1, "shopping_score": 3, "culture_score": 4,
         "average_cost": 400, "time_needed": 2, "rating": 4.3,
         "location": "Juhu", "distance_from_city_centre": 25,
         "image": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=600&q=80"},
    ],
    "Leh Ladakh": [
        {"place_name": "Pangong Lake", "category": "Nature",
         "nature_score": 5, "adventure_score": 4, "food_score": 1,
         "history_score": 2, "shopping_score": 1, "culture_score": 3,
         "average_cost": 2000, "time_needed": 8, "rating": 4.9,
         "location": "Eastern Ladakh", "distance_from_city_centre": 150,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Thiksey Monastery", "category": "Culture",
         "nature_score": 3, "adventure_score": 2, "food_score": 1,
         "history_score": 4, "shopping_score": 2, "culture_score": 5,
         "average_cost": 200, "time_needed": 2, "rating": 4.6,
         "location": "Thiksey", "distance_from_city_centre": 19,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Khardung La Pass", "category": "Adventure",
         "nature_score": 5, "adventure_score": 5, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 2,
         "average_cost": 1500, "time_needed": 5, "rating": 4.7,
         "location": "North Leh", "distance_from_city_centre": 39,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Nubra Valley", "category": "Nature",
         "nature_score": 5, "adventure_score": 4, "food_score": 2,
         "history_score": 2, "shopping_score": 1, "culture_score": 3,
         "average_cost": 2500, "time_needed": 8, "rating": 4.8,
         "location": "North Ladakh", "distance_from_city_centre": 120,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
        {"place_name": "Leh Palace", "category": "History",
         "nature_score": 3, "adventure_score": 2, "food_score": 1,
         "history_score": 5, "shopping_score": 2, "culture_score": 5,
         "average_cost": 200, "time_needed": 2, "rating": 4.4,
         "location": "Central Leh", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80"},
    ],
    "Rishikesh": [
        {"place_name": "Ganga Rafting", "category": "Adventure",
         "nature_score": 4, "adventure_score": 5, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 2,
         "average_cost": 1200, "time_needed": 3, "rating": 4.6,
         "location": "Rishikesh", "distance_from_city_centre": 5,
         "image": "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?w=600&q=80"},
        {"place_name": "Laxman Jhula", "category": "Culture",
         "nature_score": 3, "adventure_score": 2, "food_score": 2,
         "history_score": 4, "shopping_score": 3, "culture_score": 5,
         "average_cost": 200, "time_needed": 2, "rating": 4.4,
         "location": "Central Rishikesh", "distance_from_city_centre": 3,
         "image": "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?w=600&q=80"},
        {"place_name": "Yoga Retreat", "category": "Relaxation",
         "nature_score": 3, "adventure_score": 2, "food_score": 3,
         "history_score": 2, "shopping_score": 1, "culture_score": 5,
         "average_cost": 2000, "time_needed": 4, "rating": 4.7,
         "location": "Tapovan", "distance_from_city_centre": 6,
         "image": "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?w=600&q=80"},
        {"place_name": "Neer Garh Waterfall Trek", "category": "Adventure",
         "nature_score": 5, "adventure_score": 4, "food_score": 1,
         "history_score": 1, "shopping_score": 1, "culture_score": 1,
         "average_cost": 500, "time_needed": 4, "rating": 4.5,
         "location": "Rishikesh", "distance_from_city_centre": 7,
         "image": "https://images.unsplash.com/photo-1593693411515-c20261bcad6e?w=600&q=80"},
    ],
    "Udaipur": [
        {"place_name": "City Palace Museum", "category": "History",
         "nature_score": 1, "adventure_score": 1, "food_score": 1,
         "history_score": 5, "shopping_score": 2, "culture_score": 5,
         "average_cost": 500, "time_needed": 3, "rating": 4.6,
         "location": "Central Udaipur", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&q=80"},
        {"place_name": "Lake Pichola Boat Ride", "category": "Relaxation",
         "nature_score": 4, "adventure_score": 2, "food_score": 1,
         "history_score": 3, "shopping_score": 1, "culture_score": 3,
         "average_cost": 400, "time_needed": 2, "rating": 4.7,
         "location": "Central Udaipur", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&q=80"},
        {"place_name": "Sajjangarh Monsoon Palace", "category": "History",
         "nature_score": 4, "adventure_score": 2, "food_score": 1,
         "history_score": 4, "shopping_score": 1, "culture_score": 3,
         "average_cost": 300, "time_needed": 2, "rating": 4.4,
         "location": "Udaipur Hills", "distance_from_city_centre": 5,
         "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&q=80"},
        {"place_name": "Shilpgram Crafts Village", "category": "Culture",
         "nature_score": 2, "adventure_score": 1, "food_score": 3,
         "history_score": 3, "shopping_score": 4, "culture_score": 5,
         "average_cost": 300, "time_needed": 2, "rating": 4.3,
         "location": "West Udaipur", "distance_from_city_centre": 3,
         "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&q=80"},
    ],
    "Varanasi": [
        {"place_name": "Ganga Aarti Ceremony", "category": "Culture",
         "nature_score": 2, "adventure_score": 1, "food_score": 1,
         "history_score": 4, "shopping_score": 1, "culture_score": 5,
         "average_cost": 200, "time_needed": 2, "rating": 4.8,
         "location": "Dashashwamedh Ghat", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1561361058-c24cecae35ca?w=600&q=80"},
        {"place_name": "Boat Ride on the Ganges", "category": "Culture",
         "nature_score": 3, "adventure_score": 2, "food_score": 1,
         "history_score": 4, "shopping_score": 1, "culture_score": 5,
         "average_cost": 500, "time_needed": 2, "rating": 4.6,
         "location": "Ghats", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1561361058-c24cecae35ca?w=600&q=80"},
        {"place_name": "Kashi Vishwanath Temple", "category": "Culture",
         "nature_score": 1, "adventure_score": 1, "food_score": 1,
         "history_score": 5, "shopping_score": 2, "culture_score": 5,
         "average_cost": 300, "time_needed": 2, "rating": 4.7,
         "location": "Central Varanasi", "distance_from_city_centre": 1,
         "image": "https://images.unsplash.com/photo-1561361058-c24cecae35ca?w=600&q=80"},
        {"place_name": "Sarnath", "category": "History",
         "nature_score": 2, "adventure_score": 1, "food_score": 1,
         "history_score": 5, "shopping_score": 1, "culture_score": 4,
         "average_cost": 400, "time_needed": 3, "rating": 4.4,
         "location": "Sarnath", "distance_from_city_centre": 10,
         "image": "https://images.unsplash.com/photo-1561361058-c24cecae35ca?w=600&q=80"},
    ],
}

# Fill remaining destinations with generic places
for dest_data in DESTINATIONS_DATA:
    dest = dest_data["destination"]
    if dest not in PLACES_TEMPLATES:
        cats = dest_data.get("categories", ["Nature"])
        PLACES_TEMPLATES[dest] = []
        generic_places = [
            f"{dest} City Tour", f"{dest} Heritage Walk",
            f"Local Food Tour {dest}", f"{dest} Viewpoint",
            f"{dest} Market", f"{dest} Nature Trail"
        ]
        for i, pname in enumerate(generic_places):
            cat = cats[i % len(cats)]
            PLACES_TEMPLATES[dest].append({
                "place_name": pname,
                "category": cat,
                "nature_score": np.random.randint(2, 5),
                "adventure_score": np.random.randint(1, 5),
                "food_score": np.random.randint(2, 5),
                "history_score": np.random.randint(2, 5),
                "shopping_score": np.random.randint(1, 4),
                "culture_score": np.random.randint(2, 5),
                "average_cost": int(np.random.randint(300, 2000)),
                "time_needed": int(np.random.randint(2, 6)),
                "rating": round(float(np.random.uniform(3.8, 4.8)), 1),
                "location": dest,
                "distance_from_city_centre": int(np.random.randint(1, 30)),
                "image": dest_data["image"],
            })


def generate_places_dataset():
    """Generate the main places dataset."""
    rows = []
    place_id = 1
    for dest_data in DESTINATIONS_DATA:
        dest = dest_data["destination"]
        for place in PLACES_TEMPLATES.get(dest, []):
            rows.append({
                "place_id": place_id,
                "place_name": place["place_name"],
                "destination": dest,
                "country": dest_data["country"],
                "region": dest_data.get("region", "India"),
                "category": place["category"],
                "nature_score": int(place["nature_score"]),
                "adventure_score": int(place["adventure_score"]),
                "food_score": int(place["food_score"]),
                "history_score": int(place["history_score"]),
                "shopping_score": int(place["shopping_score"]),
                "culture_score": int(place["culture_score"]),
                "average_cost": int(place["average_cost"]),
                "time_needed": float(place["time_needed"]),
                "rating": float(place["rating"]),
                "location": place["location"],
                "distance_from_city_centre": float(place["distance_from_city_centre"]),
                "image": place.get("image", dest_data["image"]),
            })
            place_id += 1
    df = pd.DataFrame(rows)
    df.to_csv(DATASETS_DIR / "places.csv", index=False)
    print(f"Places dataset: {len(df)} records")
    return df


def generate_destinations_dataset():
    """Generate destinations dataset."""
    rows = []
    for dest_data in DESTINATIONS_DATA:
        rows.append({
            "destination_id": len(rows) + 1,
            "destination": dest_data["destination"],
            "country": dest_data["country"],
            "region": dest_data.get("region", "India"),
            "image": dest_data["image"],
            "description": dest_data["description"],
            "avg_rating": dest_data["avg_rating"],
            "avg_cost_per_day": dest_data["avg_cost_per_day"],
            "best_duration_days": dest_data["best_duration_days"],
            "categories": json.dumps(dest_data["categories"]),
            "best_season": dest_data.get("best_season", "Oct-Mar"),
            "latitude": dest_data.get("latitude", 20.0),
            "longitude": dest_data.get("longitude", 78.0),
        })
    df = pd.DataFrame(rows)
    df.to_csv(DATASETS_DIR / "destinations.csv", index=False)
    print(f"Destinations dataset: {len(df)} records")
    return df


def generate_users_dataset(n=500):
    """Generate synthetic user profiles."""
    food_prefs = ["Vegetarian", "Non-Vegetarian", "Vegan", "No Preference"]
    group_types = ["Solo", "Couple", "Friends", "Family"]
    hotel_types = ["Budget", "Standard", "Luxury"]

    rows = []
    for i in range(1, n + 1):
        budget = int(np.random.choice([
            np.random.randint(5000, 15000),   # budget traveller
            np.random.randint(15000, 40000),  # moderate
            np.random.randint(40000, 150000), # luxury
        ], p=[0.35, 0.45, 0.20]))

        days = int(np.random.randint(2, 10))
        group_size = int(np.random.randint(1, 8))

        rows.append({
            "user_id": i,
            "budget": budget,
            "days": days,
            "group_size": group_size,
            "group_type": np.random.choice(group_types),
            "food_preference": np.random.choice(food_prefs),
            "nature_interest": int(np.random.randint(1, 6)),
            "adventure_interest": int(np.random.randint(1, 6)),
            "food_interest": int(np.random.randint(1, 6)),
            "history_interest": int(np.random.randint(1, 6)),
            "shopping_interest": int(np.random.randint(1, 6)),
            "culture_interest": int(np.random.randint(1, 6)),
            "walking_comfort": np.random.choice(["Low", "Medium", "High"]),
            "accommodation_type": np.random.choice(hotel_types),
            "transport_preference": np.random.choice(["Public Transport", "Cab", "Rental", "Mixed"]),
            "trip_pace": np.random.choice(["Relaxed", "Balanced", "Packed"]),
        })

    df = pd.DataFrame(rows)
    df.to_csv(DATASETS_DIR / "users.csv", index=False)
    print(f"Users dataset: {len(df)} records")
    return df


def generate_interactions_dataset(users_df, places_df, n_interactions=3000):
    """Generate user-place interaction dataset."""
    interaction_types = ["Like", "Saved", "Skipped"]
    rows = []
    seen = set()

    for _ in range(n_interactions):
        user_id = int(np.random.choice(users_df["user_id"]))
        place_id = int(np.random.choice(places_df["place_id"]))
        key = (user_id, place_id)
        if key in seen:
            continue
        seen.add(key)

        user = users_df[users_df["user_id"] == user_id].iloc[0]
        place = places_df[places_df["place_id"] == place_id].iloc[0]

        # Compute interest match
        interest_map = {
            "Nature": "nature_interest",
            "Adventure": "adventure_interest",
            "Food": "food_interest",
            "History": "history_interest",
            "Shopping": "shopping_interest",
            "Culture": "culture_interest",
        }
        score_map = {
            "Nature": "nature_score",
            "Adventure": "adventure_score",
            "Food": "food_score",
            "History": "history_score",
            "Shopping": "shopping_score",
            "Culture": "culture_score",
        }
        cat = place["category"]
        interest_col = interest_map.get(cat, "nature_interest")
        score_col = score_map.get(cat, "nature_score")
        interest = user.get(interest_col, 3)
        place_score = place.get(score_col, 3)

        cost_per_person = place["average_cost"] * user["days"]
        budget_per_person = user["budget"] / max(user["group_size"], 1)
        budget_ok = cost_per_person <= budget_per_person * 0.3

        # Probabilistic like based on interest + match + budget
        base_prob = 0.3 + 0.1 * interest + 0.05 * place_score + (0.2 if budget_ok else 0)
        base_prob = min(base_prob, 0.95)
        liked = int(np.random.random() < base_prob)
        interaction = "Like" if liked else np.random.choice(["Saved", "Skipped"], p=[0.4, 0.6])

        rows.append({
            "user_id": user_id,
            "place_id": place_id,
            "interaction": interaction,
            "liked": liked,
        })

    df = pd.DataFrame(rows)
    df.to_csv(DATASETS_DIR / "interactions.csv", index=False)
    print(f"Interactions dataset: {len(df)} records")
    return df


def generate_past_trips_dataset(n=800):
    """Generate past trips dataset for regression training."""
    hotel_types = ["Budget", "Standard", "Luxury"]
    transports = ["Public Transport", "Cab", "Rental", "Mixed"]
    destinations = [d["destination"] for d in DESTINATIONS_DATA]

    cost_multipliers = {"Budget": 0.7, "Standard": 1.0, "Luxury": 1.8}
    transport_costs = {"Public Transport": 500, "Cab": 1500, "Rental": 2000, "Mixed": 1000}

    rows = []
    for i in range(1, n + 1):
        dest_data = np.random.choice(DESTINATIONS_DATA)
        days = int(np.random.randint(2, 10))
        group_size = int(np.random.randint(1, 8))
        hotel_type = np.random.choice(hotel_types)
        transport = np.random.choice(transports)

        base_cost_per_day = dest_data["avg_cost_per_day"]
        hotel_mult = cost_multipliers[hotel_type]
        transport_per_day = transport_costs[transport]
        food_cost = int(np.random.randint(400, 1200)) * days

        # Actual cost with noise
        actual_cost = int(
            base_cost_per_day * hotel_mult * days * group_size * 0.6
            + transport_per_day * days
            + food_cost
            + np.random.normal(0, base_cost_per_day * 0.1)
        )
        actual_cost = max(actual_cost, 1000)

        # Actual time (hours) - 6-10 hours per day
        actual_time = round(days * np.random.uniform(5, 9), 1)

        rows.append({
            "trip_id": i,
            "destination": dest_data["destination"],
            "days": days,
            "group_size": group_size,
            "hotel_type": hotel_type,
            "transport": transport,
            "actual_cost": actual_cost,
            "actual_time": actual_time,
            "base_cost_per_day": dest_data["avg_cost_per_day"],
            "cost_multiplier": hotel_mult,
        })

    df = pd.DataFrame(rows)
    df.to_csv(DATASETS_DIR / "past_trips.csv", index=False)
    print(f"Past trips dataset: {len(df)} records")
    return df


def generate_all():
    """Generate all datasets."""
    print("=" * 50)
    print("TRIP PLANNER - DATASET GENERATION")
    print("NOTE: All data is synthetic/simulated")
    print("=" * 50)

    places_df = generate_places_dataset()
    dest_df = generate_destinations_dataset()
    users_df = generate_users_dataset(500)
    interactions_df = generate_interactions_dataset(users_df, places_df, 3000)
    past_trips_df = generate_past_trips_dataset(800)

    # Save metadata
    metadata = {
        "data_note": "All datasets are synthetic/simulated for academic ML demonstration",
        "seed": 42,
        "records": {
            "places": len(places_df),
            "destinations": len(dest_df),
            "users": len(users_df),
            "interactions": len(interactions_df),
            "past_trips": len(past_trips_df),
        }
    }
    with open(DATASETS_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n[OK] All datasets generated successfully!")
    print(f"  Saved to: {DATASETS_DIR}")
    return places_df, dest_df, users_df, interactions_df, past_trips_df


if __name__ == "__main__":
    generate_all()

