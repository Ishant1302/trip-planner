"""
Script to generate an enriched, comprehensive places dataset with rich descriptions
and 8-12 authentic attractions per destination.
"""

import pandas as pd

PLACES_DATA = [
    # ─── 1. JAIPUR (10 Places) ────────────────────────────────────────────────
    {
        "place_name": "Amber Fort & Palace",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 3, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 500, "time_needed": 3.0, "rating": 4.7,
        "location": "Amer, Jaipur", "distance_from_city_centre": 11.0,
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=700&q=80",
        "description": "Majestic 16th-century hilltop fortress renowned for its grand courtyards, Maota Lake reflections, and the glittering Sheesh Mahal mirror palace."
    },
    {
        "place_name": "Hawa Mahal (Palace of Winds)",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 1, "adventure_score": 2, "food_score": 3, "history_score": 5, "shopping_score": 4, "culture_score": 5,
        "average_cost": 200, "time_needed": 1.5, "rating": 4.4,
        "location": "Badi Choupad, Old City", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1603258849062-103328407886?w=700&q=80",
        "description": "Iconic five-story pink sandstone facade with 953 intricately carved jharokha casements, built in 1799 for royal women to witness street processions."
    },
    {
        "place_name": "City Palace & Maharaja Museum",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 400, "time_needed": 2.5, "rating": 4.5,
        "location": "Jaleb Chowk, Old City", "distance_from_city_centre": 3.5,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "Grand royal residence blending Rajput and Mughal architecture, housing courtyards, arms galleries, royal costumes, and the Peacock Gate."
    },
    {
        "place_name": "Jantar Mantar Observatory",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 2, "adventure_score": 2, "food_score": 1, "history_score": 5, "shopping_score": 2, "culture_score": 4,
        "average_cost": 200, "time_needed": 1.5, "rating": 4.5,
        "location": "Gangori Bazaar, Jaipur", "distance_from_city_centre": 3.8,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "UNESCO World Heritage collection of nineteen architectural astronomical instruments, including the world's largest stone sundial."
    },
    {
        "place_name": "Nahargarh Fort Sunset Viewpoint",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 4, "adventure_score": 4, "food_score": 3, "history_score": 4, "shopping_score": 1, "culture_score": 4,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.6,
        "location": "Aravalli Hills", "distance_from_city_centre": 15.0,
        "image": "https://images.unsplash.com/photo-1617854818583-09e7f077a156?w=700&q=80",
        "description": "Perched on the rugged ridge of the Aravallis, offering sweeping panoramic sunset views of the illuminated Pink City below."
    },
    {
        "place_name": "Jal Mahal (Water Palace)",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 2, "food_score": 3, "history_score": 4, "shopping_score": 3, "culture_score": 4,
        "average_cost": 100, "time_needed": 1.5, "rating": 4.3,
        "location": "Amer Road, Man Sagar Lake", "distance_from_city_centre": 7.0,
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=700&q=80",
        "description": "Photogenic 18th-century palace floating serenely in the center of Man Sagar Lake, surrounded by the picturesque Nahargarh hills."
    },
    {
        "place_name": "Johari Bazaar & Bapu Bazaar Walk",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "Shopping",
        "nature_score": 1, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 5,
        "average_cost": 800, "time_needed": 2.5, "rating": 4.4,
        "location": "Pink City Bazaars", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=700&q=80",
        "description": "Bustling cultural shopping lanes celebrated for Kundan gemstone jewelry, handcrafted Rajasthani juttis, Jaipuri quilts, and block-print textiles."
    },
    {
        "place_name": "Chokhi Dhani Ethnic Village",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "Food",
        "nature_score": 2, "adventure_score": 3, "food_score": 5, "history_score": 3, "shopping_score": 4, "culture_score": 5,
        "average_cost": 1100, "time_needed": 3.5, "rating": 4.6,
        "location": "Tonk Road, Jaipur", "distance_from_city_centre": 19.0,
        "image": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=700&q=80",
        "description": "Immersive Rajasthani village carnival featuring Kalbeliya folk dances, puppet shows, acrobatics, and an authentic multi-course royal thali feast."
    },
    {
        "place_name": "Albert Hall Museum",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 300, "time_needed": 2.0, "rating": 4.5,
        "location": "Ram Niwas Garden", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1620766182966-c6eb5ed2b788?w=700&q=80",
        "description": "The oldest museum in Rajasthan, showcasing Indo-Saracenic architecture, rare metal sculptures, miniature paintings, and an ancient Egyptian mummy."
    },
    {
        "place_name": "Patrika Gate at Jawahar Circle",
        "destination": "Jaipur", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 3, "history_score": 3, "shopping_score": 2, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.6,
        "location": "Jawahar Circle, Malviya Nagar", "distance_from_city_centre": 10.0,
        "image": "https://images.unsplash.com/photo-1598890777032-bde835ba27c2?w=700&q=80",
        "description": "Spectacular vibrant archway adorned with colorful hand-painted murals portraying Rajasthani traditions, forts, and royal weddings."
    },

    # ─── 2. GOA (10 Places) ───────────────────────────────────────────────────
    {
        "place_name": "Baga Beach & Watersports",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 4, "adventure_score": 5, "food_score": 4, "history_score": 1, "shopping_score": 3, "culture_score": 2,
        "average_cost": 800, "time_needed": 3.0, "rating": 4.4,
        "location": "North Goa", "distance_from_city_centre": 14.0,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=700&q=80",
        "description": "Energetic beach hub famous for parasailing, jet-skiing, lively beach shacks, and vibrant seaside evening music."
    },
    {
        "place_name": "Fort Aguada & Lighthouse",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 4,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.5,
        "location": "Sinquerim, Candolim", "distance_from_city_centre": 15.0,
        "image": "https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=700&q=80",
        "description": "Well-preserved 17th-century Portuguese fortress overlooking the Mandovi River and Arabian Sea, featuring an iconic stone lighthouse."
    },
    {
        "place_name": "Basilica of Bom Jesus",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.6,
        "location": "Old Goa", "distance_from_city_centre": 10.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "UNESCO World Heritage baroque cathedral housing the mortal remains of St. Francis Xavier, adorned with gilded altars and marble floors."
    },
    {
        "place_name": "Dudhsagar Waterfalls Expedition",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 1500, "time_needed": 5.0, "rating": 4.7,
        "location": "Bhagwan Mahaveer Sanctuary", "distance_from_city_centre": 60.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Four-tiered roaring white cataract cascading 310 meters down the Western Ghats, reachable via an exhilarating forest jeep safari."
    },
    {
        "place_name": "Palolem Beach & Canoe Cruise",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 3, "food_score": 4, "history_score": 1, "shopping_score": 2, "culture_score": 2,
        "average_cost": 400, "time_needed": 3.0, "rating": 4.7,
        "location": "Canacona, South Goa", "distance_from_city_centre": 65.0,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Crescent-shaped tropical paradise fringed with coconut palms, calm turquoise waters ideal for kayaking, and silent noise parties."
    },
    {
        "place_name": "Fontainhas Latin Quarter Heritage Walk",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 2, "food_score": 5, "history_score": 4, "shopping_score": 3, "culture_score": 5,
        "average_cost": 250, "time_needed": 2.0, "rating": 4.6,
        "location": "Panaji City Center", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=700&q=80",
        "description": "Charming colonial neighborhood characterized by pastel-hued Portuguese villas, terracotta roofs, ornate balconies, and artisanal bakeries."
    },
    {
        "place_name": "Chapora Fort & Sunset Trail",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 4, "adventure_score": 3, "food_score": 3, "history_score": 4, "shopping_score": 2, "culture_score": 3,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.4,
        "location": "Vagator, North Goa", "distance_from_city_centre": 18.0,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=700&q=80",
        "description": "Famed hilltop red-laterite fort overlooking Vagator Beach and the Chapora River, popular for atmospheric sunset photography."
    },
    {
        "place_name": "Sahakari Spice Plantation Tour & Lunch",
        "destination": "Goa", "country": "India", "region": "South India",
        "category": "Food",
        "nature_score": 5, "adventure_score": 2, "food_score": 5, "history_score": 2, "shopping_score": 3, "culture_score": 4,
        "average_cost": 600, "time_needed": 2.5, "rating": 4.5,
        "location": "Curti, Ponda", "distance_from_city_centre": 28.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Guided aromatic tour through vanilla, cardamom, and cinnamon groves, complete with a traditional Goan buffet served on banana leaves."
    },

    # ─── 3. KERALA BACKWATERS (8 Places) ──────────────────────────────────────
    {
        "place_name": "Alleppey Houseboat Lagoon Cruise",
        "destination": "Kerala Backwaters", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 5, "history_score": 2, "shopping_score": 2, "culture_score": 4,
        "average_cost": 3000, "time_needed": 5.0, "rating": 4.8,
        "location": "Vembanad Lake, Alappuzha", "distance_from_city_centre": 4.0,
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=700&q=80",
        "description": "Signature Kettuvallam luxury boat voyage meandering through tranquil palm-fringed canals, paddy fields, and floating village life."
    },
    {
        "place_name": "Kumarakom Bird Sanctuary",
        "destination": "Kerala Backwaters", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 3,
        "average_cost": 250, "time_needed": 2.5, "rating": 4.4,
        "location": "Kavanattinkara, Kumarakom", "distance_from_city_centre": 32.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Fourteen-acre lush wetland sanctuary hosting migratory water birds including Siberian storks, egrets, herons, and kingfishers."
    },
    {
        "place_name": "Marari Serene White Sand Beach",
        "destination": "Kerala Backwaters", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 4, "history_score": 1, "shopping_score": 2, "culture_score": 3,
        "average_cost": 100, "time_needed": 3.0, "rating": 4.6,
        "location": "Mararikulam, Alappuzha", "distance_from_city_centre": 14.0,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Secluded, uncommercialized coastal haven with swaying coconut palms, gentle surf, and fresh seafood shacks serving Karimeen Pollichathu."
    },
    {
        "place_name": "Alappuzha Lighthouse & Marine Promenade",
        "destination": "Kerala Backwaters", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 4, "adventure_score": 2, "food_score": 3, "history_score": 4, "shopping_score": 2, "culture_score": 3,
        "average_cost": 100, "time_needed": 1.5, "rating": 4.3,
        "location": "Alappuzha Beach", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=700&q=80",
        "description": "Historic striped beacon built in 1862, offering 360-degree aerial views over the Arabian Sea and historic pier ruins."
    },
    {
        "place_name": "Krishnapuram Palace & Mural Gallery",
        "destination": "Kerala Backwaters", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 150, "time_needed": 2.0, "rating": 4.4,
        "location": "Kayamkulam", "distance_from_city_centre": 45.0,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "18th-century Travancore royal palace displaying Kerala-style gabled roofs and the famous Gajendra Moksham mural, the largest in Kerala."
    },
    {
        "place_name": "Vembanad Kayaking & Village Canals",
        "destination": "Kerala Backwaters", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 3, "history_score": 1, "shopping_score": 1, "culture_score": 4,
        "average_cost": 900, "time_needed": 2.5, "rating": 4.7,
        "location": "Kuttanad Canals", "distance_from_city_centre": 8.0,
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=700&q=80",
        "description": "Quiet guided small-craft kayak excursion paddling through narrow canals inaccessible to larger houseboats, observing coir-making."
    },

    # ─── 4. MANALI (8 Places) ─────────────────────────────────────────────────
    {
        "place_name": "Solang Valley Adventures",
        "destination": "Manali", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 3, "history_score": 1, "shopping_score": 2, "culture_score": 2,
        "average_cost": 1200, "time_needed": 4.0, "rating": 4.6,
        "location": "Solang, Manali", "distance_from_city_centre": 14.0,
        "image": "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=700&q=80",
        "description": "High-altitude alpine playground offering paragliding, zorbing, ATV quad biking, and quad lifts against snow-draped Himalayan peaks."
    },
    {
        "place_name": "Hadimba Devi Cedar Temple",
        "destination": "Manali", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 100, "time_needed": 1.5, "rating": 4.5,
        "location": "Dhungri Forest, Manali", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Four-tiered pagoda-style wooden temple constructed in 1553, nested within a mystical grove of towering deodar cedar trees."
    },
    {
        "place_name": "Rohtang Pass Snow Crest",
        "destination": "Manali", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 2000, "time_needed": 6.0, "rating": 4.7,
        "location": "Pir Panjal Range", "distance_from_city_centre": 51.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Dramatic 3,978m mountain pass connecting Kullu to Lahaul & Spiti, offering year-round snow landscapes and views of twin glaciers."
    },
    {
        "place_name": "Jogini Waterfall Pine Forest Trek",
        "destination": "Manali", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 3,
        "average_cost": 150, "time_needed": 3.0, "rating": 4.6,
        "location": "Vashisht Village", "distance_from_city_centre": 4.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Invigorating forest trail passing through apple orchards and pine woods to a spectacular multi-stage cascade tumbling into sacred pools."
    },
    {
        "place_name": "Old Manali Cafes & Music Street",
        "destination": "Manali", "country": "India", "region": "North India",
        "category": "Food",
        "nature_score": 3, "adventure_score": 2, "food_score": 5, "history_score": 2, "shopping_score": 4, "culture_score": 4,
        "average_cost": 650, "time_needed": 2.5, "rating": 4.5,
        "location": "Old Manali Village", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=700&q=80",
        "description": "Bohemian cobblestone streets lined with artisan bakeries, trout grills, wood-fired pizzerias, and live acoustic music sessions."
    },
    {
        "place_name": "Vashisht Natural Hot Springs",
        "destination": "Manali", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 4, "shopping_score": 3, "culture_score": 4,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.3,
        "location": "Vashisht Temple", "distance_from_city_centre": 3.5,
        "image": "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=700&q=80",
        "description": "Ancient sulfur-rich thermal spring baths adjacent to stone-carved temples, renowned for their therapeutic rejuvenation."
    },

    # ─── 5. AGRA (8 Places) ───────────────────────────────────────────────────
    {
        "place_name": "Taj Mahal Sunrise Monument",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 3, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 250, "time_needed": 3.0, "rating": 4.9,
        "location": "Dharmapuri, Forest Colony", "distance_from_city_centre": 4.0,
        "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=700&q=80",
        "description": "UNESCO World Wonder and marble mausoleum built by Emperor Shah Jahan, glowing ethereal shades of peach and gold at sunrise."
    },
    {
        "place_name": "Agra Fort & Diwan-i-Khas",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 2, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 350, "time_needed": 2.5, "rating": 4.6,
        "location": "Agra Fort Road", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "Massive 16th-century Mughal red sandstone citadel housing royal audience halls, the marble Pearl Mosque, and Jahangiri Mahal."
    },
    {
        "place_name": "Fatehpur Sikri Royal Complex",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 2, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 300, "time_needed": 3.5, "rating": 4.6,
        "location": "Fatehpur Sikri", "distance_from_city_centre": 36.0,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "Preserved Mughal imperial capital founded by Akbar in 1571, featuring the monumental 54m Buland Darwaza and Salim Chishti tomb."
    },
    {
        "place_name": "Mehtab Bagh Moonlight Garden",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 1, "food_score": 2, "history_score": 4, "shopping_score": 1, "culture_score": 4,
        "average_cost": 200, "time_needed": 2.0, "rating": 4.5,
        "location": "Opposite Taj Mahal, Yamuna Bank", "distance_from_city_centre": 7.0,
        "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=700&q=80",
        "description": "Charbagh-style riverside garden situated directly across the Yamuna, delivering unobstructed sunset reflections of the Taj Mahal."
    },
    {
        "place_name": "Itmad-ud-Daulah (Baby Taj)",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 1, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 200, "time_needed": 1.5, "rating": 4.4,
        "location": "Moti Bagh, Agra", "distance_from_city_centre": 5.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "Exquisite white marble jewel box mausoleum preceding the Taj, famed for introducing intricate pietra dura floral inlay craftsmanship."
    },
    {
        "place_name": "Kinari Bazaar & Petha Food Walk",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Food",
        "nature_score": 1, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 4,
        "average_cost": 400, "time_needed": 2.0, "rating": 4.3,
        "location": "Old Agra Market Lanes", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=700&q=80",
        "description": "Vibrant medieval market lanes tasting authentic Agra petha sweet varieties, dalmoth snacks, and shopping for brass artifacts."
    },

    # ─── 6. VARANASI (8 Places) ───────────────────────────────────────────────
    {
        "place_name": "Dashashwamedh Ghat Evening Ganga Aarti",
        "destination": "Varanasi", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 150, "time_needed": 2.0, "rating": 4.9,
        "location": "Dashashwamedh Ghat", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "Grand spiritual ceremony illuminated by multi-tiered brass oil lamps, rhythmic Vedic chants, conch horns, and floating river diyas."
    },
    {
        "place_name": "Assi Ghat Sunrise Boat Cruise",
        "destination": "Varanasi", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 3, "food_score": 4, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 400, "time_needed": 2.5, "rating": 4.8,
        "location": "Assi Ghat Riverfront", "distance_from_city_centre": 4.0,
        "image": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?w=700&q=80",
        "description": "Tranquil wooden oared rowboat ride drifting past ancient palace facades while the rising sun paints the sacred Ganges in crimson."
    },
    {
        "place_name": "Kashi Vishwanath Golden Temple",
        "destination": "Varanasi", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 2, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 200, "time_needed": 2.0, "rating": 4.8,
        "location": "Vishwanath Gali, Varanasi", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "One of twelve revered Jyotirlingas, capped with one ton of gold spire plating, connected to the river via a grand corridor."
    },
    {
        "place_name": "Sarnath Buddhist Monasteries & Dhamek Stupa",
        "destination": "Varanasi", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 4, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 300, "time_needed": 3.0, "rating": 4.7,
        "location": "Sarnath", "distance_from_city_centre": 10.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "Hallowed Deer Park where Lord Buddha delivered his first sermon; contains the 43m stone Dhamek Stupa and Ashoka Lion Capital museum."
    },
    {
        "place_name": "Manikarnika Sacred Ghat Walk",
        "destination": "Varanasi", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 2, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.5,
        "location": "Manikarnika Ghat", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?w=700&q=80",
        "description": "The primary cremation ghat of Kashi where sacred funeral fires have burned continuously for millennia, representing the cycle of Moksha."
    },
    {
        "place_name": "Godowlia Market Street Food & Banarasi Silk",
        "destination": "Varanasi", "country": "India", "region": "North India",
        "category": "Shopping",
        "nature_score": 1, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 5,
        "average_cost": 750, "time_needed": 2.5, "rating": 4.5,
        "location": "Godowlia Crossing", "distance_from_city_centre": 2.2,
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=700&q=80",
        "description": "Sensory labyrinth of woven brocade silk sari ateliers, artisanal malaiyyo foam sweets, kachori breakfasts, and creamy clay-cup lassi."
    },

    # ─── 7. UDAIPUR (8 Places) ────────────────────────────────────────────────
    {
        "place_name": "City Palace Complex & Museum",
        "destination": "Udaipur", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 4, "adventure_score": 2, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 500, "time_needed": 3.0, "rating": 4.8,
        "location": "Old City, Lake Pichola", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "Rajasthan's largest royal palace complex with marble cupolas, mosaic peacock courtyards, and museum galleries overlooking Lake Pichola."
    },
    {
        "place_name": "Lake Pichola & Jag Mandir Island Cruise",
        "destination": "Udaipur", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 4, "history_score": 4, "shopping_score": 2, "culture_score": 4,
        "average_cost": 600, "time_needed": 2.0, "rating": 4.7,
        "location": "Rameshwar Ghat", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Enchanting boat cruise past the floating Taj Lake Palace to the 17th-century island garden palace guarded by stone elephants."
    },
    {
        "place_name": "Saheliyon-ki-Bari (Garden of Maids)",
        "destination": "Udaipur", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 1, "food_score": 1, "history_score": 4, "shopping_score": 1, "culture_score": 4,
        "average_cost": 150, "time_needed": 1.5, "rating": 4.4,
        "location": "Saheli Marg", "distance_from_city_centre": 4.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Tranquil royal garden landscaped with lotus pools, marble elephant fountains, rain water pavilions, and manicured rose lawns."
    },
    {
        "place_name": "Sajjangarh Monsoon Palace",
        "destination": "Udaipur", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 4, "shopping_score": 1, "culture_score": 3,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.5,
        "location": "Bansdara Peak", "distance_from_city_centre": 9.0,
        "image": "https://images.unsplash.com/photo-1617854818583-09e7f077a156?w=700&q=80",
        "description": "Hilltop castle perched 944m high in the Aravallis, built to track monsoon clouds and famed for sunset vistas across the lake basin."
    },
    {
        "place_name": "Bagore Ki Haveli Folk Dance Show",
        "destination": "Udaipur", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 1, "food_score": 2, "history_score": 4, "shopping_score": 3, "culture_score": 5,
        "average_cost": 250, "time_needed": 2.0, "rating": 4.7,
        "location": "Gangaur Ghat", "distance_from_city_centre": 1.8,
        "image": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=700&q=80",
        "description": "18th-century waterfront mansion staging the Dharohar cultural showcase of Chari fire dances, balancing pot tricks, and puppet theatre."
    },
    {
        "place_name": "Fateh Sagar Lake & Nehru Park Walk",
        "destination": "Udaipur", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 4, "history_score": 2, "shopping_score": 2, "culture_score": 3,
        "average_cost": 200, "time_needed": 2.0, "rating": 4.5,
        "location": "Fateh Sagar", "distance_from_city_centre": 5.0,
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=700&q=80",
        "description": "Scenic pear-shaped artificial lake flanked by hills, featuring speedboating, an island solar observatory, and street food kiosks."
    },

    # ─── 8. MUMBAI (8 Places) ─────────────────────────────────────────────────
    {
        "place_name": "Gateway of India & Apollo Bunder",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "History",
        "nature_score": 3, "adventure_score": 2, "food_score": 4, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.6,
        "location": "Colaba, Mumbai", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=700&q=80",
        "description": "Monumental 26m Indo-Saracenic basalt arch built to commemorate King George V's visit, standing beside the iconic Taj Mahal Palace hotel."
    },
    {
        "place_name": "Elephanta Caves UNESCO Island Excursion",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "History",
        "nature_score": 4, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 450, "time_needed": 4.0, "rating": 4.6,
        "location": "Elephanta Island, Mumbai Harbour", "distance_from_city_centre": 11.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "5th-century rock-cut cave temples dedicated to Lord Shiva, featuring the renowned 6m three-headed Trimurti bas-relief sculpture."
    },
    {
        "place_name": "Marine Drive Queen's Necklace Promenade",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 1, "food_score": 4, "history_score": 3, "shopping_score": 2, "culture_score": 4,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.8,
        "location": "Netaji Subhash Chandra Bose Road", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=700&q=80",
        "description": "3.6-kilometer curved seafront promenade celebrated for evening coastal breezes, sunset vistas, and Art Deco residential architecture."
    },
    {
        "place_name": "Chhatrapati Shivaji Terminus (CST)",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Culture",
        "nature_score": 1, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 1.5, "rating": 4.7,
        "location": "Fort, Mumbai", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=700&q=80",
        "description": "UNESCO-listed Victorian Gothic revival railway station masterpiece constructed in 1887, featuring high domes, stained glass, and stone gargoyles."
    },
    {
        "place_name": "Colaba Causeway Curio Shopping",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Shopping",
        "nature_score": 1, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 4,
        "average_cost": 700, "time_needed": 2.5, "rating": 4.4,
        "location": "Shahid Bhagat Singh Road", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=700&q=80",
        "description": "Lively commercial corridor brimming with antique brassware, bohemian jewelry, leather footwear, and historic eateries like Cafe Mondegar."
    },
    {
        "place_name": "Bandra Bandstand & Fort Walk",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 4, "history_score": 4, "shopping_score": 3, "culture_score": 4,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.5,
        "location": "Bandra West", "distance_from_city_centre": 14.0,
        "image": "https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=700&q=80",
        "description": "Celebrated sea-facing walkway overlooking the Bandra-Worli Sea Link, featuring Castella de Aguada fort ruins and celebrity residences."
    },

    # ─── 9. RISHIKESH (8 Places) ──────────────────────────────────────────────
    {
        "place_name": "Ganges White Water Rafting at Shivpuri",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 1200, "time_needed": 3.5, "rating": 4.8,
        "location": "Shivpuri to Rishikesh", "distance_from_city_centre": 16.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Adrenaline-fueled 16km descent through Grade III and IV rapids like Roller Coaster and Golf Course amidst towering Himalayan gorges."
    },
    {
        "place_name": "Triveni Ghat Evening Maha Aarti",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.8,
        "location": "Mayakund, Rishikesh", "distance_from_city_centre": 1.5,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "Sacred confluence of three holy rivers where priests conduct mesmerizing twilight fire worship accompanied by drums and floating butter lamps."
    },
    {
        "place_name": "Beatles Ashram (Chaurasi Kutia)",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 4, "shopping_score": 1, "culture_score": 5,
        "average_cost": 150, "time_needed": 2.5, "rating": 4.5,
        "location": "Swarg Ashram, Rajaji Reserve", "distance_from_city_centre": 4.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Forest meditation retreat where The Beatles wrote much of the White Album in 1968, adorned with graffiti art and stone meditation igloos."
    },
    {
        "place_name": "Neer Garh Multi-Tier Waterfall Hike",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 100, "time_needed": 3.0, "rating": 4.5,
        "location": "Badrinath Highway", "distance_from_city_centre": 7.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Refreshing jungle trek leading to pristine turquoise plunge pools ideal for wading beneath natural forest canopy."
    },
    {
        "place_name": "Lakshman Jhula & Suspension Bridges",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 4, "history_score": 4, "shopping_score": 4, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.5,
        "location": "Tapovan, Rishikesh", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=700&q=80",
        "description": "Famous 137m iron suspension bridge linking historic ashrams, yoga schools, and organic rooftop cafes with views of holy rafters."
    },
    {
        "place_name": "Kunjapuri Temple Sunrise Peak Trek",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 4, "shopping_score": 1, "culture_score": 5,
        "average_cost": 400, "time_needed": 3.5, "rating": 4.7,
        "location": "Narendra Nagar Ridge", "distance_from_city_centre": 26.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Sacred ridge shrine at 1,676m elevation providing sunrise spectacles over the snowcapped peaks of Swargarohini, Gangotri, and Banderpoonch."
    },

    # ─── 10. LEH LADAKH (8 Places) ────────────────────────────────────────────
    {
        "place_name": "Pangong Tso Alpine Lake",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 2500, "time_needed": 6.0, "rating": 4.9,
        "location": "Changtang Plateau", "distance_from_city_centre": 150.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "High-altitude endorheic lake at 4,350m spanning 134km, world-renowned for shifting colors from deep emerald to vibrant azure."
    },
    {
        "place_name": "Nubra Valley & Hunder Sand Dunes",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 3, "history_score": 2, "shopping_score": 2, "culture_score": 4,
        "average_cost": 2000, "time_needed": 6.0, "rating": 4.8,
        "location": "Nubra Valley", "distance_from_city_centre": 125.0,
        "image": "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=700&q=80",
        "description": "Cold desert river valley renowned for double-humped Bactrian camel safaris across white dunes against glaciated mountain walls."
    },
    {
        "place_name": "Thiksey Monastery (Mini Potala)",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.8,
        "location": "Thiksey, Indus Valley", "distance_from_city_centre": 19.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Twelve-story Tibetan Buddhist complex resembling Lhasa's Potala Palace, housing a breathtaking 15m statue of Maitreya Buddha."
    },
    {
        "place_name": "Khardung La Mountain Pass",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 1, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 500, "time_needed": 3.0, "rating": 4.7,
        "location": "Ladakh Range", "distance_from_city_centre": 39.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "One of the highest motorable mountain passes in the world at 5,359m, acting as the gateway to the Shyok and Nubra valleys."
    },
    {
        "place_name": "Shanti Stupa White Dome",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 2, "history_score": 3, "shopping_score": 1, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.7,
        "location": "Changsjpa, Leh", "distance_from_city_centre": 3.5,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "White-domed Buddhist chorten perched on a hilltop in Changspa, offering unparalleled panoramic sunset views across Leh town and Stok Kangri."
    },
    {
        "place_name": "Sangam: Indus & Zanskar Confluence",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 200, "time_needed": 2.0, "rating": 4.6,
        "location": "Nimmu, Leh Highway", "distance_from_city_centre": 32.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Remarkable meeting point where the emerald green Indus and muddy brown Zanskar rivers merge distinctly amidst moonscape ravines."
    },

    # ─── 11. COORG (8 Places) ─────────────────────────────────────────────────
    {
        "place_name": "Abbey Falls & Coffee Estate Trail",
        "destination": "Coorg", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 1, "shopping_score": 2, "culture_score": 2,
        "average_cost": 150, "time_needed": 2.0, "rating": 4.5,
        "location": "Madikeri", "distance_from_city_centre": 7.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Spectacular cascade tumbling down 70 feet between spice and coffee plantations, viewed from a rustic hanging footbridge."
    },
    {
        "place_name": "Namdroling Tibetan Golden Temple",
        "destination": "Coorg", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 4, "history_score": 3, "shopping_score": 4, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.7,
        "location": "Bylakuppe", "distance_from_city_centre": 35.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Largest Tibetan settlement in southern India, housing colossal 40-foot gilded Buddha statues amidst prayer wheels and thangka murals."
    },
    {
        "place_name": "Raja's Seat Sunset Viewpoint",
        "destination": "Coorg", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 3, "history_score": 4, "shopping_score": 2, "culture_score": 4,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.5,
        "location": "Madikeri Town", "distance_from_city_centre": 1.5,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Seasonal garden pavilion where the Kodagu Kings watched dramatic sunsets across rolling mist-covered valleys and green hills."
    },
    {
        "place_name": "Dubare Elephant Camp & River Bathing",
        "destination": "Coorg", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 3,
        "average_cost": 500, "time_needed": 3.0, "rating": 4.4,
        "location": "Kaveri River Bank, Kushalnagar", "distance_from_city_centre": 28.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Forest eco-tourism river camp where visitors can participate in grooming and bathing Asian elephants in the Kaveri River."
    },
    {
        "place_name": "Talakaveri Sacred Spring & Brahmagiri",
        "destination": "Coorg", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 5, "adventure_score": 3, "food_score": 1, "history_score": 4, "shopping_score": 1, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.6,
        "location": "Brahmagiri Hills, Bhagamandala", "distance_from_city_centre": 45.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "The sacred source of the River Kaveri perched at 1,276m on Brahmagiri Hill, commanding breathtaking vistas of the Ghats."
    },
    {
        "place_name": "Organic Coffee & Spice Estate Tour",
        "destination": "Coorg", "country": "India", "region": "South India",
        "category": "Food",
        "nature_score": 5, "adventure_score": 2, "food_score": 5, "history_score": 2, "shopping_score": 5, "culture_score": 4,
        "average_cost": 400, "time_needed": 2.0, "rating": 4.7,
        "location": "Siddapur / Madikeri", "distance_from_city_centre": 12.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Walk among Arabica coffee shrubs, pepper vines, and cardamom plants, followed by freshly brewed estate coffee and Kodava honey tasting."
    },

    # ─── 12. DARJEELING (8 Places) ───────────────────────────────────────────
    {
        "place_name": "Tiger Hill Sunrise over Kanchenjunga",
        "destination": "Darjeeling", "country": "India", "region": "East India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 3,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.8,
        "location": "Senchal Hills", "distance_from_city_centre": 11.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Famed dawn lookout at 2,590m witnessing the morning sun illuminate the snow-clad peaks of Kanchenjunga and Mount Everest."
    },
    {
        "place_name": "Darjeeling Himalayan Railway (Toy Train)",
        "destination": "Darjeeling", "country": "India", "region": "East India",
        "category": "History",
        "nature_score": 4, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 1000, "time_needed": 2.5, "rating": 4.7,
        "location": "Darjeeling Station to Ghum", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=700&q=80",
        "description": "UNESCO World Heritage 2-foot narrow-gauge vintage steam engine ride looping through dramatic alpine spirals and pine forests."
    },
    {
        "place_name": "Batasia Loop & Gorkha War Memorial",
        "destination": "Darjeeling", "country": "India", "region": "East India",
        "category": "History",
        "nature_score": 4, "adventure_score": 1, "food_score": 2, "history_score": 4, "shopping_score": 3, "culture_score": 4,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.5,
        "location": "Hill Cart Road, Ghum", "distance_from_city_centre": 5.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Double-loop engineering marvel encircled by landscaped gardens, offering panoramic views of Darjeeling town and mountain ridges."
    },
    {
        "place_name": "Happy Valley Tea Estate & Factory",
        "destination": "Darjeeling", "country": "India", "region": "East India",
        "category": "Food",
        "nature_score": 5, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 4, "culture_score": 4,
        "average_cost": 250, "time_needed": 2.0, "rating": 4.6,
        "location": "Lebong Cart Road", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "One of Darjeeling's oldest organic tea gardens (established 1854); experience tea plucking and sample fragrant Muscatel flushes."
    },
    {
        "place_name": "Japanese Peace Pagoda & Temple",
        "destination": "Darjeeling", "country": "India", "region": "East India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 1, "food_score": 1, "history_score": 3, "shopping_score": 1, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.5,
        "location": "Jalapahar Hill", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Serene white stupa displaying four avatars of Lord Buddha and sandstone carvings, built to foster global peace and unity."
    },
    {
        "place_name": "Mall Road & Chowrasta Promenade",
        "destination": "Darjeeling", "country": "India", "region": "East India",
        "category": "Shopping",
        "nature_score": 3, "adventure_score": 1, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 4,
        "average_cost": 400, "time_needed": 2.0, "rating": 4.5,
        "location": "Chowrasta Town Center", "distance_from_city_centre": 0.5,
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=700&q=80",
        "description": "Pedestrian heritage square with benches, pony rides, Curio craft boutiques, and historic tea lounges like Nathmulls."
    },

    # ─── 13. HAMPI (8 Places) ─────────────────────────────────────────────────
    {
        "place_name": "Vijaya Vittala Temple & Stone Chariot",
        "destination": "Hampi", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 3, "adventure_score": 2, "food_score": 1, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 300, "time_needed": 3.0, "rating": 4.9,
        "location": "Hampi Ruins, Bellary", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "16th-century Vijayanagara architectural masterpiece featuring musical stone pillars and the iconic stone chariot shrine."
    },
    {
        "place_name": "Virupaksha Temple Riverfront",
        "destination": "Hampi", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.7,
        "location": "Hampi Bazaar", "distance_from_city_centre": 0.5,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "Continuously active 7th-century shrine with a 50m tiered gopuram on the Tungabhadra River, dedicated to Lord Shiva."
    },
    {
        "place_name": "Matanga Hill Sunrise Boulder Trek",
        "destination": "Hampi", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 1, "history_score": 3, "shopping_score": 1, "culture_score": 4,
        "average_cost": 50, "time_needed": 2.5, "rating": 4.8,
        "location": "East of Hampi Bazaar", "distance_from_city_centre": 1.5,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "The highest point in central Hampi; early morning climb delivers 360-degree vistas across boulder fields, temples, and banana groves."
    },
    {
        "place_name": "Lotus Mahal & Royal Elephant Stables",
        "destination": "Hampi", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 3, "adventure_score": 1, "food_score": 1, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 250, "time_needed": 2.0, "rating": 4.6,
        "location": "Zenana Enclosure", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "Indo-Islamic secular complex showing lotus-bud arches, water-cooling channels, and eleven grand domed elephant chambers."
    },
    {
        "place_name": "Tungabhadra River Coracle Boat Ride",
        "destination": "Hampi", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 3, "shopping_score": 1, "culture_score": 4,
        "average_cost": 400, "time_needed": 1.5, "rating": 4.6,
        "location": "Chakratirtha Ghat", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Authentic circular reed-and-bamboo boat glide along the swirling river through granite canyon gorges and rock-hewn shrines."
    },
    {
        "place_name": "Sanapur Lake Bouldering & Cliff Views",
        "destination": "Hampi", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 4, "food_score": 3, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 150, "time_needed": 2.5, "rating": 4.6,
        "location": "Anegundi, Gangavathi", "distance_from_city_centre": 7.0,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Reservoir lake surrounded by massive ochre granite boulders on the hippy island side, popular for relaxed swims and cliffside walks."
    },

    # ─── 14. ANDAMAN ISLANDS (8 Places) ───────────────────────────────────────
    {
        "place_name": "Radhanagar Beach (Beach No. 7)",
        "destination": "Andaman Islands", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 3, "food_score": 3, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 200, "time_needed": 4.0, "rating": 4.9,
        "location": "Havelock Island (Swaraj Dweep)", "distance_from_city_centre": 11.0,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Voted Asia's best beach by Time Magazine; expansive sweep of powdery white sand, turquoise water, and mahua rainforest backdrops."
    },
    {
        "place_name": "Cellular Jail National Memorial",
        "destination": "Andaman Islands", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 2, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.8,
        "location": "Atlanta Point, Port Blair", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "Colonial-era British prison (Kala Pani) where freedom fighters were exiled, preserved with a solemn light & sound tribute."
    },
    {
        "place_name": "Elephant Beach Snorkeling & Coral Reef",
        "destination": "Andaman Islands", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 1500, "time_needed": 3.5, "rating": 4.6,
        "location": "Havelock Island", "distance_from_city_centre": 8.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Crystal-clear shallow waters boasting vibrant coral heads, sea turtle sightings, sea walking, and guided snorkeling adventures."
    },
    {
        "place_name": "Ross Island (Netaji Subhash Chandra Bose Dweep)",
        "destination": "Andaman Islands", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 4,
        "average_cost": 400, "time_needed": 2.5, "rating": 4.6,
        "location": "Port Blair Harbour", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=700&q=80",
        "description": "Eerie ruins of British administrative headquarters intertwined with wild banyan tree roots, inhabited by free-roaming spotted deer."
    },
    {
        "place_name": "Bharatpur Beach & Natural Coral Bridge",
        "destination": "Andaman Islands", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 3, "history_score": 1, "shopping_score": 2, "culture_score": 2,
        "average_cost": 500, "time_needed": 3.0, "rating": 4.6,
        "location": "Neil Island (Shaheed Dweep)", "distance_from_city_centre": 38.0,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Shallow lagoon ideal for glass-bottom boat rides and a unique living natural rock arch carved by sea waves."
    },
    {
        "place_name": "Chidiya Tapu Sunset Point",
        "destination": "Andaman Islands", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 2, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 150, "time_needed": 2.5, "rating": 4.5,
        "location": "South Andaman", "distance_from_city_centre": 28.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Lush coastal mangrove forest and birdwatcher's paradise celebrated for spectacular sunset hues melting into the Bay of Bengal."
    },

    # ─── 15. KOLKATA (8 Places) ───────────────────────────────────────────────
    {
        "place_name": "Victoria Memorial Gallery & Gardens",
        "destination": "Kolkata", "country": "India", "region": "East India",
        "category": "History",
        "nature_score": 4, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.7,
        "location": "Maidan, Queens Way", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "Magnificent white Makrana marble monument honoring Queen Victoria, housing 25 galleries of British Raj paintings, weapons, and coins."
    },
    {
        "place_name": "Howrah Bridge & Flower Market Walk",
        "destination": "Kolkata", "country": "India", "region": "East India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 2, "food_score": 4, "history_score": 5, "shopping_score": 4, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.6,
        "location": "Hooghly Riverfront", "distance_from_city_centre": 3.0,
        "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=700&q=80",
        "description": "Iconic cantilever steel bridge over the Hooghly, paired with Mullick Ghat, one of Asia's largest marigold and rose flower bazaars."
    },
    {
        "place_name": "Dakshineswar Kali Temple Riverfront",
        "destination": "Kolkata", "country": "India", "region": "East India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.7,
        "location": "Dakshineswar", "distance_from_city_centre": 12.0,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "19th-century Navaratna-style sacred temple dedicated to Goddess Bhavatarini, closely associated with mystic saint Sri Ramakrishna Paramahamsa."
    },
    {
        "place_name": "Park Street Heritage Culinary Walk",
        "destination": "Kolkata", "country": "India", "region": "East India",
        "category": "Food",
        "nature_score": 1, "adventure_score": 1, "food_score": 5, "history_score": 3, "shopping_score": 4, "culture_score": 5,
        "average_cost": 700, "time_needed": 2.5, "rating": 4.6,
        "location": "Park Street (Mother Teresa Sarani)", "distance_from_city_centre": 1.5,
        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=700&q=80",
        "description": "Legendary gastronomic street famous for colonial tearoom Flurys, Peter Cat's Chelo Kebab, Nizam's kathi rolls, and live jazz."
    },
    {
        "place_name": "Indian Museum (Jadu Ghar)",
        "destination": "Kolkata", "country": "India", "region": "East India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 75, "time_needed": 2.5, "rating": 4.5,
        "location": "Jawaharlal Nehru Road", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "Ninth oldest regular museum in the world (established 1814), displaying rare fossils, meteorite fragments, Mughal art, and Buddhist sculptures."
    },
    {
        "place_name": "Kumartuli Artisan Potter Quarter",
        "destination": "Kolkata", "country": "India", "region": "East India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 2, "food_score": 3, "history_score": 4, "shopping_score": 3, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.7,
        "location": "North Kolkata", "distance_from_city_centre": 5.0,
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=700&q=80",
        "description": "Traditional 300-year-old potter district where skilled generational sculptors craft lifelike clay idols of Goddess Durga using holy Ganges silt."
    },

    # ─── 16. MYSORE (8 Places) ─────────────────────────────────────────────────
    {
        "place_name": "Mysore Palace & Night Illumination",
        "destination": "Mysore", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 3, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 200, "time_needed": 2.5, "rating": 4.8,
        "location": "Sayyaji Rao Road", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "Resplendent Indo-Saracenic palace of the Wadiyar dynasty featuring stained glass ceilings, carved mahogany, and 100,000 weekend bulbs."
    },
    {
        "place_name": "Chamundi Hill & Sri Chamundeshwari Temple",
        "destination": "Mysore", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.6,
        "location": "Chamundi Hills", "distance_from_city_centre": 12.0,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "Sacred summit at 1,000m with a seven-tier gopuram, flanked by a massive monolithic granite Nandi bull sculpture carved in 1659."
    },
    {
        "place_name": "Brindavan Gardens Musical Fountains",
        "destination": "Mysore", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 1, "food_score": 2, "history_score": 3, "shopping_score": 2, "culture_score": 3,
        "average_cost": 150, "time_needed": 2.5, "rating": 4.4,
        "location": "KRS Dam, Mandya", "distance_from_city_centre": 19.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Terraced Mughal-style garden laid beneath the Krishnarajasagara dam, featuring dancing water fountains synchronized to music."
    },
    {
        "place_name": "Devaraja Market & Mysore Pak Trail",
        "destination": "Mysore", "country": "India", "region": "South India",
        "category": "Shopping",
        "nature_score": 1, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 5,
        "average_cost": 450, "time_needed": 2.0, "rating": 4.5,
        "location": "Sayyaji Rao Road", "distance_from_city_centre": 1.2,
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=700&q=80",
        "description": "Centuries-old market famous for fragrant Mysore sandalwood oils, fresh jasmine garlands, Mysore silk sarees, and melt-in-mouth ghee Mysore Pak."
    },
    {
        "place_name": "St. Philomena's Neo-Gothic Cathedral",
        "destination": "Mysore", "country": "India", "region": "South India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 1, "food_score": 2, "history_score": 4, "shopping_score": 1, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.0, "rating": 4.5,
        "location": "Ashoka Road", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "One of the tallest churches in Asia, built in 1936 with 53m spires inspired by Germany's Cologne Cathedral and French stained glass."
    },
    {
        "place_name": "Ranganathittu Bird Sanctuary Boat Safari",
        "destination": "Mysore", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.6,
        "location": "Srirangapatna", "distance_from_city_centre": 16.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Islets in the Kaveri River hosting nesting painted storks, spoonbills, and marsh mugger crocodiles viewed from guided rowboats."
    },

    # ─── 17. SPITI VALLEY (8 Places) ──────────────────────────────────────────
    {
        "place_name": "Key Gompa Cliffside Monastery",
        "destination": "Spiti Valley", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.9,
        "location": "Key Village", "distance_from_city_centre": 14.0,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Thousand-year-old fort-like Tibetan Buddhist monastery perched on a conical hill at 4,166m, holding ancient murals and wind horns."
    },
    {
        "place_name": "Chandratal Moon Lake Trek",
        "destination": "Spiti Valley", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 800, "time_needed": 5.0, "rating": 4.9,
        "location": "Samudra Tapu Plateau", "distance_from_city_centre": 95.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Crescent-shaped high-altitude alpine lake at 4,300m surrounded by scree peaks, shimmering in shifting shades of navy and emerald."
    },
    {
        "place_name": "Dhankar Monastery & Fort Viewpoint",
        "destination": "Spiti Valley", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.7,
        "location": "Dhankar Village", "distance_from_city_centre": 35.0,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "Ancient capital of Spiti kingdom dramatically perched on a jagged 300m cliff spur overlooking the confluence of Spiti and Pin rivers."
    },
    {
        "place_name": "Kibber Village Wildlife & Fossil Walk",
        "destination": "Spiti Valley", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 2, "shopping_score": 1, "culture_score": 4,
        "average_cost": 250, "time_needed": 3.0, "rating": 4.7,
        "location": "Kibber", "distance_from_city_centre": 19.0,
        "image": "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=700&q=80",
        "description": "Whitewashed stone village at 4,270m, home to the Kibber Wildlife Sanctuary and prime winter habitat for the elusive snow leopard."
    },
    {
        "place_name": "Hikkim: World's Highest Post Office",
        "destination": "Spiti Valley", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 3, "food_score": 2, "history_score": 3, "shopping_score": 3, "culture_score": 5,
        "average_cost": 150, "time_needed": 1.5, "rating": 4.6,
        "location": "Hikkim Village", "distance_from_city_centre": 16.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Operating at 4,400m elevation; send hand-stamped postcards to loved ones from the highest working post office on planet Earth."
    },
    {
        "place_name": "Langza Golden Buddha & Marine Fossils",
        "destination": "Spiti Valley", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 4, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.8,
        "location": "Langza Village", "distance_from_city_centre": 15.0,
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=700&q=80",
        "description": "Guarded by a thousand-year-old gilded Buddha statue facing the Chau Chau Kang Nilda peak; fields contain millions of Tethys Sea fossils."
    },

    # ─── 18. OOTY (8 Places) ──────────────────────────────────────────────────
    {
        "place_name": "Government Botanical Gardens",
        "destination": "Ooty", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 1, "food_score": 2, "history_score": 3, "shopping_score": 2, "culture_score": 3,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.6,
        "location": "Vannarapettai", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "55-acre terraced garden established in 1848, housing over a thousand exotic plant species, cork trees, and a 20-million-year-old fossilized tree trunk."
    },
    {
        "place_name": "Nilgiri Mountain Railway (Toy Train)",
        "destination": "Ooty", "country": "India", "region": "South India",
        "category": "History",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 600, "time_needed": 3.0, "rating": 4.8,
        "location": "Ooty to Coonoor", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=700&q=80",
        "description": "UNESCO World Heritage meter-gauge rack-and-pinion railway chugging through 16 tunnels, 250 bridges, and scenic Nilgiri tea hills."
    },
    {
        "place_name": "Doddabetta Peak Highest Viewpoint",
        "destination": "Ooty", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 1, "shopping_score": 2, "culture_score": 2,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.5,
        "location": "Ooty-Kotagiri Road", "distance_from_city_centre": 9.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "The highest peak in the Nilgiris at 2,637m; telescopic observatory delivers sweeping views of Bandipur national park and Coimbatore plains."
    },
    {
        "place_name": "Pykara Lake Boating & Waterfalls",
        "destination": "Ooty", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 350, "time_needed": 2.5, "rating": 4.5,
        "location": "Pykara, Nilgiris", "distance_from_city_centre": 21.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Pristine shola-ringed lake offering speedboat cruises, followed by two scenic waterfalls cascading over rounded granite rocks."
    },
    {
        "place_name": "Ooty Tea Factory & Chocolate Museum",
        "destination": "Ooty", "country": "India", "region": "South India",
        "category": "Food",
        "nature_score": 3, "adventure_score": 1, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 4,
        "average_cost": 150, "time_needed": 1.5, "rating": 4.4,
        "location": "Doddabetta Road", "distance_from_city_centre": 4.5,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Observe CTC tea processing from green leaves to packaged dust, accompanied by homemade Nilgiri chocolate making and tastings."
    },
    {
        "place_name": "Avalanche Lake Pine Forest Sanctuary",
        "destination": "Ooty", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 4, "food_score": 1, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 400, "time_needed": 3.5, "rating": 4.7,
        "location": "Kundanahalli", "distance_from_city_centre": 26.0,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Wild, untouched emerald lake fringed with blooming rhododendrons and magnolia trees, ideal for trout fishing and nature walks."
    },

    # ─── 19. JAISALMER (8 Places) ─────────────────────────────────────────────
    {
        "place_name": "Jaisalmer Fort (Sonar Qila)",
        "destination": "Jaisalmer", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 3, "adventure_score": 2, "food_score": 4, "history_score": 5, "shopping_score": 4, "culture_score": 5,
        "average_cost": 250, "time_needed": 3.0, "rating": 4.8,
        "location": "Fort Road, Jaisalmer", "distance_from_city_centre": 1.0,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=700&q=80",
        "description": "A living golden sandstone fort rising from the Thar Desert, housing 4,000 residents, ancient Jain temples, and cannon bastions."
    },
    {
        "place_name": "Sam Sand Dunes Desert Safari & Sunset",
        "destination": "Jaisalmer", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 4, "history_score": 1, "shopping_score": 2, "culture_score": 5,
        "average_cost": 1500, "time_needed": 4.0, "rating": 4.7,
        "location": "Sam, Thar Desert", "distance_from_city_centre": 42.0,
        "image": "https://images.unsplash.com/photo-1586348943529-beaae6c28db9?w=700&q=80",
        "description": "Rippling golden desert dunes with sunset camel safaris, quad biking, campfires, and vibrant Manganiyar musical evenings under the stars."
    },
    {
        "place_name": "Patwon Ki Haveli Architectural Cluster",
        "destination": "Jaisalmer", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 1, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 200, "time_needed": 2.0, "rating": 4.6,
        "location": "Old City, Jaisalmer", "distance_from_city_centre": 1.5,
        "image": "https://images.unsplash.com/photo-1590766940554-634a7ed41450?w=700&q=80",
        "description": "Cluster of five ornate merchant mansions carved from yellow sandstone, featuring 60 balconies with lace-like stonework."
    },
    {
        "place_name": "Gadisar Lake & Desert Gateway",
        "destination": "Jaisalmer", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 4, "adventure_score": 2, "food_score": 3, "history_score": 4, "shopping_score": 3, "culture_score": 4,
        "average_cost": 150, "time_needed": 2.0, "rating": 4.5,
        "location": "Near Jaisalmer Fort", "distance_from_city_centre": 2.0,
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=700&q=80",
        "description": "14th-century rainwater reservoir bordered by small yellow sandstone shrines, chhatris, and the regal Tilon Ki Pol gateway."
    },
    {
        "place_name": "Kuldhara Abandoned Ghost Village",
        "destination": "Jaisalmer", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 3, "adventure_score": 3, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 4,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.3,
        "location": "Sam Road", "distance_from_city_centre": 18.0,
        "image": "https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=700&q=80",
        "description": "Cursed medieval village abandoned overnight by Paliwal Brahmins in 1825, leaving haunting stone ruins preserved in the desert."
    },
    {
        "place_name": "Bada Bagh Royal Cenotaphs",
        "destination": "Jaisalmer", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 150, "time_needed": 1.5, "rating": 4.5,
        "location": "Ramgarh Road", "distance_from_city_centre": 6.0,
        "image": "https://images.unsplash.com/photo-1617854818583-09e7f077a156?w=700&q=80",
        "description": "Dramatic garden complex housing carved sandstone chhatris (cenotaphs) of the Maharajas, glowing radiant amber in the golden hour."
    },

    # ─── 20. MUNNAR (8 Places) ────────────────────────────────────────────────
    {
        "place_name": "Eravikulam National Park & Anamudi",
        "destination": "Munnar", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 1, "history_score": 1, "shopping_score": 1, "culture_score": 3,
        "average_cost": 250, "time_needed": 3.5, "rating": 4.7,
        "location": "Kannan Devan Hills", "distance_from_city_centre": 13.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Protected high-altitude sanctuary harboring the endangered Nilgiri Tahr mountain goat and the highest peak in South India (2,695m)."
    },
    {
        "place_name": "KDHP Tea Museum & Factory Experience",
        "destination": "Munnar", "country": "India", "region": "South India",
        "category": "Food",
        "nature_score": 4, "adventure_score": 1, "food_score": 5, "history_score": 4, "shopping_score": 4, "culture_score": 4,
        "average_cost": 150, "time_needed": 2.0, "rating": 4.5,
        "location": "Nullatanni Estate", "distance_from_city_centre": 2.5,
        "image": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=700&q=80",
        "description": "Chronicles the transformation of Munnar's wilderness into tea plantations since 1880, featuring operational machinery and tea tastings."
    },
    {
        "place_name": "Mattupetty Dam & Lake Speedboating",
        "destination": "Munnar", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 3, "food_score": 3, "history_score": 2, "shopping_score": 2, "culture_score": 2,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.5,
        "location": "Mattupetty", "distance_from_city_centre": 11.0,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700&q=80",
        "description": "Concrete gravity storage dam nestled amidst rolling tea hills; speedboats skim past wild elephants grazing on the water's edge."
    },
    {
        "place_name": "Top Station Panoramic Western Ghats View",
        "destination": "Munnar", "country": "India", "region": "South India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 2, "shopping_score": 2, "culture_score": 2,
        "average_cost": 100, "time_needed": 3.0, "rating": 4.6,
        "location": "Kerala-Tamil Nadu Border", "distance_from_city_centre": 32.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "The highest point on the Munnar-Kodaikanal road at 1,700m, delivering panoramic views across cloud valleys and the Theni plains."
    },
    {
        "place_name": "Attukal Waterfalls Trek",
        "destination": "Munnar", "country": "India", "region": "South India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.5,
        "location": "Pallivasal", "distance_from_city_centre": 9.0,
        "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=700&q=80",
        "description": "Jungle waterfall rushing between rolling hills, reached via a scenic foot trek through emerald tea slopes and wooden bridges."
    },
    {
        "place_name": "Pothamedu Viewpoint Sunset & Spices",
        "destination": "Munnar", "country": "India", "region": "South India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 3, "history_score": 1, "shopping_score": 3, "culture_score": 3,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.5,
        "location": "Pothamedu", "distance_from_city_centre": 5.0,
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=700&q=80",
        "description": "Spectacular cliffside viewpoint surveying wide emerald valleys filled with cardamom, pepper, and tea, bathed in golden sunset glow."
    },
]


def generate_enriched_csv():
    df = pd.DataFrame(PLACES_DATA)
    df.insert(0, "place_id", range(1, len(df) + 1))
    
    # Save to CSV
    csv_path = "c:/Users/manoj/Desktop/ML Project/backend/datasets/places.csv"
    df.to_csv(csv_path, index=False)
    print(f"Successfully generated {len(df)} places across {df['destination'].nunique()} destinations!")
    print(df.groupby('destination').size())

if __name__ == "__main__":
    generate_enriched_csv()

