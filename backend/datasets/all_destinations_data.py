"""
Places data for destinations 6 through 20:
Agra, Mumbai, Leh Ladakh, Rishikesh, Varanasi, Coorg, Darjeeling, Hampi, Andaman Islands, Kolkata, Mysore, Spiti Valley, Ooty, Jaisalmer, Munnar.
"""

DESTINATIONS_6_TO_20 = [
    # ══════════════════════════════════════════════════════════════════════════
    # 6. AGRA (12 Places)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "place_name": "Taj Mahal (UNESCO World Wonder)",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 3, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 3, "culture_score": 5,
        "average_cost": 500, "time_needed": 3.5, "rating": 4.9,
        "location": "Dharmapuri, Forest Colony, Tajganj", "distance_from_city_centre": 3.8,
        "wiki_title": "Taj Mahal",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/800px-Taj_Mahal_%28Edited%29.jpeg",
        "description": "The world's greatest monument to love, commissioned in 1632 by Emperor Shah Jahan for Mumtaz Mahal, featuring pristine white marble and pietra dura inlay."
    },
    {
        "place_name": "Agra Fort (Red Sandstone Citadel)",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 2, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 400, "time_needed": 3.0, "rating": 4.7,
        "location": "Agra Fort, Rakabganj", "distance_from_city_centre": 2.5,
        "wiki_title": "Agra Fort",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Agra_Fort_India.jpg/800px-Agra_Fort_India.jpg",
        "description": "Sprawling 16th-century Mughal imperial fortress of red sandstone containing Jahangiri Mahal, Khas Mahal, Diwan-i-Khas, and Shah Jahan's Muasamman Burj prison."
    },
    {
        "place_name": "Mehtab Bagh (Moonlight Garden Sunset)",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 1, "food_score": 1, "history_score": 4, "shopping_score": 1, "culture_score": 4,
        "average_cost": 200, "time_needed": 2.0, "rating": 4.6,
        "location": "Yamuna River North Bank", "distance_from_city_centre": 6.0,
        "wiki_title": "Mehtab Bagh",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Mehtab_Bagh_Agra.jpg/800px-Mehtab_Bagh_Agra.jpg",
        "description": "Charbagh garden complex on the opposite bank of the Yamuna River, providing unobstructed sunset views of the Taj Mahal without crowds."
    },
    {
        "place_name": "Fatehpur Sikri Imperial Capital",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 2, "adventure_score": 2, "food_score": 1, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 350, "time_needed": 4.0, "rating": 4.7,
        "location": "Fatehpur Sikri", "distance_from_city_centre": 37.0,
        "wiki_title": "Fatehpur Sikri",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Buland_Darwaza_Fatehpur_Sikri.jpg/800px-Buland_Darwaza_Fatehpur_Sikri.jpg",
        "description": "Emperor Akbar's 16th-century ghost city, featuring the 54-meter Buland Darwaza, the white marble tomb of Salim Chishti, and Panch Mahal."
    },
    {
        "place_name": "Tomb of I'timād-ud-Daulah (Baby Taj)",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 250, "time_needed": 1.5, "rating": 4.5,
        "location": "Moti Bagh, Yamuna Riverfront", "distance_from_city_centre": 5.0,
        "wiki_title": "Tomb of I'timad-ud-Daulah",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Itmad-ud-Daula%27s_Tomb.jpg/800px-Itmad-ud-Daula%27s_Tomb.jpg",
        "description": "Often called the 'Jewel Box' or 'Baby Taj', this mausoleum built by Nur Jahan for her father is the first Mughal structure built from white marble with lattice screens."
    },
    {
        "place_name": "Akbar's Tomb at Sikandra",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 3, "adventure_score": 1, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 250, "time_needed": 2.0, "rating": 4.5,
        "location": "Sikandra, Agra Suburbs", "distance_from_city_centre": 10.0,
        "wiki_title": "Tomb of Akbar the Great",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Akbar%27s_Tomb_Sikandra.jpg/800px-Akbar%27s_Tomb_Sikandra.jpg",
        "description": "Grand four-tiered red sandstone and marble mausoleum of Emperor Akbar surrounded by peaceful gardens with roaming blackbuck antelopes and peacocks."
    },
    {
        "place_name": "Jama Masjid Agra",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 1, "adventure_score": 1, "food_score": 3, "history_score": 5, "shopping_score": 4, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.4,
        "location": "Kinari Bazaar, Old Agra", "distance_from_city_centre": 2.0,
        "wiki_title": "Jama Masjid, Agra",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Agra_Fort_India.jpg/800px-Agra_Fort_India.jpg",
        "description": "17th-century congregational mosque built by Shah Jahan's daughter Jahanara Begum, featuring red sandstone construction and zigzag marble inlay domes."
    },
    {
        "place_name": "Chini Ka Rauza Glazed Tile Tomb",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 1, "food_score": 1, "history_score": 4, "shopping_score": 1, "culture_score": 4,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.2,
        "location": "Ram Bagh, Yamuna Riverfront", "distance_from_city_centre": 6.5,
        "wiki_title": "Chini Ka Rauza",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Itmad-ud-Daula%27s_Tomb.jpg/800px-Itmad-ud-Daula%27s_Tomb.jpg",
        "description": "Unique Persian funerary monument decorated with turquoise, blue, and yellow enamelled glazed porcelain tiles, commemorating scholar-poet Afzal Khan."
    },
    {
        "place_name": "Sadar Bazaar & Kinari Bazaar Walk",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Shopping",
        "nature_score": 1, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 4,
        "average_cost": 500, "time_needed": 2.5, "rating": 4.4,
        "location": "Sadar Bazaar & Kinari Bazaar", "distance_from_city_centre": 1.5,
        "wiki_title": "Sadar Bazaar, Agra",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/800px-Taj_Mahal_%28Edited%29.jpeg",
        "description": "Vibrant markets famed for world-famous Agra Petha (pumpkin sweet from Panchhi Petha), leather boots and bags, and miniature marble replica inlay art."
    },
    {
        "place_name": "Wildlife SOS Elephant Conservation",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 1, "history_score": 1, "shopping_score": 1, "culture_score": 4,
        "average_cost": 1500, "time_needed": 3.0, "rating": 4.9,
        "location": "NH2, Farah, Mathura-Agra Road", "distance_from_city_centre": 32.0,
        "wiki_title": "Wildlife SOS",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Mehtab_Bagh_Agra.jpg/800px-Mehtab_Bagh_Agra.jpg",
        "description": "Ethical wildlife rescue and rehabilitation sanctuary providing lifelong care to rescued circus and working elephants, with guided education walks."
    },
    {
        "place_name": "Soor Sarovar Bird Sanctuary & Keetham",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 3, "food_score": 1, "history_score": 2, "shopping_score": 1, "culture_score": 3,
        "average_cost": 150, "time_needed": 2.5, "rating": 4.3,
        "location": "Keetham, Mathura Road", "distance_from_city_centre": 22.0,
        "wiki_title": "Soor Sarovar Bird Sanctuary",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Akbar%27s_Tomb_Sikandra.jpg/800px-Akbar%27s_Tomb_Sikandra.jpg",
        "description": "Ramsar wetland sanctuary surrounding Keetham Lake, hosting over 165 species of migratory water birds, resident spoonbills, and a sloth bear rescue center."
    },
    {
        "place_name": "Korai Tribal Village Cultural Experience",
        "destination": "Agra", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 2, "food_score": 3, "history_score": 3, "shopping_score": 3, "culture_score": 5,
        "average_cost": 300, "time_needed": 2.0, "rating": 4.5,
        "location": "Fatehpur Sikri Road", "distance_from_city_centre": 30.0,
        "wiki_title": "Fatehpur Sikri",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Buland_Darwaza_Fatehpur_Sikri.jpg/800px-Buland_Darwaza_Fatehpur_Sikri.jpg",
        "description": "Authentic rural cultural tour of the Kalandar community who formerly trained dancing bears, now sharing traditional village cooking and folklore."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 7. MUMBAI (14 Places)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "place_name": "Gateway of India & Taj Mahal Palace",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "History",
        "nature_score": 3, "adventure_score": 2, "food_score": 3, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.7,
        "location": "Apollo Bunder, Colaba", "distance_from_city_centre": 2.0,
        "wiki_title": "Gateway of India",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Gateway_of_India_front_view.jpg/800px-Gateway_of_India_front_view.jpg",
        "description": "Iconic 1924 basalt arch monument overlooking Mumbai Harbour, fronted by the grand dome and historic heritage wing of the Taj Mahal Palace hotel."
    },
    {
        "place_name": "Marine Drive (Queen's Necklace)",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Relaxation",
        "nature_score": 4, "adventure_score": 1, "food_score": 4, "history_score": 3, "shopping_score": 2, "culture_score": 4,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.8,
        "location": "Netaji Subhash Chandra Bose Road", "distance_from_city_centre": 3.0,
        "wiki_title": "Marine Drive, Mumbai",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Marine_Drive_Mumbai.jpg/800px-Marine_Drive_Mumbai.jpg",
        "description": "Famous 3.6-kilometer C-shaped boulevard along the Arabian Sea, flanked by Art Deco buildings, tetrapods, and sunset vistas glowing like a string of pearls."
    },
    {
        "place_name": "Chhatrapati Shivaji Maharaj Terminus",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "History",
        "nature_score": 1, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.7,
        "location": "Fort, South Mumbai", "distance_from_city_centre": 1.0,
        "wiki_title": "Chhatrapati Shivaji Terminus",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Victoria_Terminus_Mumbai.jpg/800px-Victoria_Terminus_Mumbai.jpg",
        "description": "UNESCO World Heritage masterpiece of Victorian High Gothic Revival architecture blended with traditional Indian styles, illuminated magnificently at night."
    },
    {
        "place_name": "Elephanta Caves UNESCO Temples",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "History",
        "nature_score": 4, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 400, "time_needed": 4.5, "rating": 4.6,
        "location": "Elephanta Island, Mumbai Harbour", "distance_from_city_centre": 11.0,
        "wiki_title": "Elephanta Caves",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Elephanta_Caves_Trimurti.jpg/800px-Elephanta_Caves_Trimurti.jpg",
        "description": "5th-century rock-cut cave temples reached by ferry from the Gateway of India, enshrining the colossal 20-foot high Trimurti sculpture of Lord Shiva."
    },
    {
        "place_name": "Colaba Causeway Flea Market",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Shopping",
        "nature_score": 1, "adventure_score": 2, "food_score": 5, "history_score": 3, "shopping_score": 5, "culture_score": 4,
        "average_cost": 600, "time_needed": 2.5, "rating": 4.5,
        "location": "Shahid Bhagat Singh Road, Colaba", "distance_from_city_centre": 2.5,
        "wiki_title": "Colaba Causeway",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Gateway_of_India_front_view.jpg/800px-Gateway_of_India_front_view.jpg",
        "description": "Eclectic street-shopping stretch loaded with antique brass, silver jewellery, clothing, and heritage culinary institutions like Leopold Cafe and Cafe Mondegar."
    },
    {
        "place_name": "Bandra-Worli Sea Link & Bandstand",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Relaxation",
        "nature_score": 4, "adventure_score": 2, "food_score": 4, "history_score": 2, "shopping_score": 2, "culture_score": 4,
        "average_cost": 150, "time_needed": 2.0, "rating": 4.7,
        "location": "Bandra West Promenade", "distance_from_city_centre": 14.0,
        "wiki_title": "Bandra–Worli Sea Link",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Marine_Drive_Mumbai.jpg/800px-Marine_Drive_Mumbai.jpg",
        "description": "Engineering marvel cable-stayed bridge spanning the sea, leading to Bandra Bandstand promenade with Castella de Aguada fort and Bollywood celebrity homes."
    },
    {
        "place_name": "Juhu Beach & Pav Bhaji Stalls",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Food",
        "nature_score": 4, "adventure_score": 2, "food_score": 5, "history_score": 1, "shopping_score": 2, "culture_score": 4,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.4,
        "location": "Juhu Tara Road, Vile Parle", "distance_from_city_centre": 20.0,
        "wiki_title": "Juhu Beach",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Marine_Drive_Mumbai.jpg/800px-Marine_Drive_Mumbai.jpg",
        "description": "Famous suburban beach crowded with lively Mumbai energy, known for butter-drenched Pav Bhaji, Bhelpuri, Sevpuri, and sunset views over the Arabian waves."
    },
    {
        "place_name": "CSMVS Prince of Wales Museum",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 350, "time_needed": 3.0, "rating": 4.6,
        "location": "Mahatma Gandhi Road, Kala Ghoda", "distance_from_city_centre": 1.5,
        "wiki_title": "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Victoria_Terminus_Mumbai.jpg/800px-Victoria_Terminus_Mumbai.jpg",
        "description": "Premier Indo-Saracenic museum housing over 50,000 exhibits spanning ancient Indus Valley relics, miniature Rajput paintings, Tibetan bronzes, and European art."
    },
    {
        "place_name": "Sanjay Gandhi NP & Kanheri Caves",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 4,
        "average_cost": 250, "time_needed": 4.0, "rating": 4.6,
        "location": "Borivali East", "distance_from_city_centre": 35.0,
        "wiki_title": "Kanheri Caves",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Elephanta_Caves_Trimurti.jpg/800px-Elephanta_Caves_Trimurti.jpg",
        "description": "Massive urban protected forest sheltering leopards and 109 rock-cut Buddhist Kanheri Caves dating from 1st century BC carved directly into basalt rock."
    },
    {
        "place_name": "Haji Ali Dargah (Offshore Mosque)",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 3, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.6,
        "location": "Lala Lajpat Rai Marg, Worli", "distance_from_city_centre": 8.0,
        "wiki_title": "Haji Ali Dargah",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Marine_Drive_Mumbai.jpg/800px-Marine_Drive_Mumbai.jpg",
        "description": "15th-century Indo-Islamic marble shrine resting on an islet 500 meters offshore in the Arabian Sea, linked to the mainland by a narrow causeway accessible at low tide."
    },
    {
        "place_name": "Siddhivinayak Temple Prabhadevi",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Culture",
        "nature_score": 1, "adventure_score": 1, "food_score": 3, "history_score": 4, "shopping_score": 3, "culture_score": 5,
        "average_cost": 100, "time_needed": 1.5, "rating": 4.7,
        "location": "SK Bole Marg, Prabhadevi", "distance_from_city_centre": 10.0,
        "wiki_title": "Siddhivinayak Temple, Mumbai",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Victoria_Terminus_Mumbai.jpg/800px-Victoria_Terminus_Mumbai.jpg",
        "description": "One of India's richest and most revered Hindu shrines dedicated to Lord Ganesha, with a two-century-old black stone idol adorned with gold."
    },
    {
        "place_name": "Kala Ghoda Art Precinct",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 1, "food_score": 5, "history_score": 4, "shopping_score": 4, "culture_score": 5,
        "average_cost": 250, "time_needed": 2.5, "rating": 4.6,
        "location": "Kala Ghoda, Fort", "distance_from_city_centre": 1.2,
        "wiki_title": "Kala Ghoda",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Gateway_of_India_front_view.jpg/800px-Gateway_of_India_front_view.jpg",
        "description": "Mumbai's creative cultural hub brimming with independent art galleries like Jehangir Art Gallery, designer boutiques, pavement bookstalls, and hip cafes."
    },
    {
        "place_name": "Dhobi Ghat Mahalaxmi Open Laundry",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Culture",
        "nature_score": 1, "adventure_score": 2, "food_score": 1, "history_score": 4, "shopping_score": 1, "culture_score": 4,
        "average_cost": 100, "time_needed": 1.5, "rating": 4.3,
        "location": "Dr. E. Moses Road, Mahalaxmi", "distance_from_city_centre": 7.5,
        "wiki_title": "Dhobi Ghat",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Victoria_Terminus_Mumbai.jpg/800px-Victoria_Terminus_Mumbai.jpg",
        "description": "World's largest outdoor laundry founded in 1890, where thousands of dhobis scrub, beat, bleach, and line-dry hundreds of thousands of clothes each day."
    },
    {
        "place_name": "Girgaon Chowpatty Sunset Beach",
        "destination": "Mumbai", "country": "India", "region": "West India",
        "category": "Relaxation",
        "nature_score": 4, "adventure_score": 1, "food_score": 4, "history_score": 2, "shopping_score": 2, "culture_score": 4,
        "average_cost": 150, "time_needed": 2.0, "rating": 4.4,
        "location": "Girgaon, North Marine Drive", "distance_from_city_centre": 4.0,
        "wiki_title": "Girgaon Chowpatty",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Marine_Drive_Mumbai.jpg/800px-Marine_Drive_Mumbai.jpg",
        "description": "Historic public beach at the northern end of Marine Drive, iconic for festive immersion celebrations of Ganesh Visarjan, street kulfi, and calm evening breezes."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 8. LEH LADAKH (14 Places)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "place_name": "Pangong Tso High-Altitude Lake",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 2, "shopping_score": 1, "culture_score": 3,
        "average_cost": 1200, "time_needed": 6.0, "rating": 4.9,
        "location": "Changthang Plateau", "distance_from_city_centre": 140.0,
        "wiki_title": "Pangong Tso",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Pangong_Tso.jpg/800px-Pangong_Tso.jpg",
        "description": "Enchanting endorheic lake sitting at 14,270 feet extending into Tibet, famous for changing shades of vivid azure, turquoise, and violet against desert mountains."
    },
    {
        "place_name": "Nubra Valley & Hunder Sand Dunes",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 3, "history_score": 2, "shopping_score": 2, "culture_score": 4,
        "average_cost": 1000, "time_needed": 6.0, "rating": 4.9,
        "location": "Hunder, Nubra Valley", "distance_from_city_centre": 125.0,
        "wiki_title": "Nubra Valley",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Hunder_sand_dunes_Ladakh.jpg/800px-Hunder_sand_dunes_Ladakh.jpg",
        "description": "High-altitude desert valley featuring wind-carved white sand dunes, seabuckthorn orchards, and rides on shaggy two-humped Bactrian camels along the ancient Silk Route."
    },
    {
        "place_name": "Khardung La Pass (17,982 ft)",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 1, "history_score": 2, "shopping_score": 1, "culture_score": 2,
        "average_cost": 500, "time_needed": 3.0, "rating": 4.8,
        "location": "Ladakh Range", "distance_from_city_centre": 39.0,
        "wiki_title": "Khardung La",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Khardung_La_Pass.jpg/800px-Khardung_La_Pass.jpg",
        "description": "One of the highest motorable mountain passes in the world, crowned with prayer flags and snowfields offering views over the Indus Valley and Karakoram range."
    },
    {
        "place_name": "Leh Palace (Royal Tibetan Citadel)",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 3, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.5,
        "location": "Namgyal Hill, Old Leh", "distance_from_city_centre": 1.0,
        "wiki_title": "Leh Palace",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Leh_Palace_from_below.jpg/800px-Leh_Palace_from_below.jpg",
        "description": "Nine-storey 17th-century fortress palace built by King Sengge Namgyal modeled on Lhasa's Potala Palace, perched dramatically over Leh's mudbrick old town."
    },
    {
        "place_name": "Shanti Stupa Panoramic Gompa",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 3, "shopping_score": 1, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.8,
        "location": "Changspha Hill", "distance_from_city_centre": 3.0,
        "wiki_title": "Shanti Stupa, Ladakh",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Shanti_Stupa_Leh.jpg/800px-Shanti_Stupa_Leh.jpg",
        "description": "White-domed Buddhist chorten built in 1991 by Japanese and Ladakhi Buddhists, providing sweeping 360-degree views of Leh town and Stok Kangri mountain."
    },
    {
        "place_name": "Magnetic Hill Gravity Phenomenon",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 4, "adventure_score": 4, "food_score": 1, "history_score": 2, "shopping_score": 1, "culture_score": 2,
        "average_cost": 100, "time_needed": 1.5, "rating": 4.3,
        "location": "Leh-Kargil National Highway", "distance_from_city_centre": 30.0,
        "wiki_title": "Magnetic Hill (India)",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Khardung_La_Pass.jpg/800px-Khardung_La_Pass.jpg",
        "description": "Fascinating optical illusion gravity hill on the Leh-Kargil highway where vehicles left in neutral appear to roll uphill against gravity."
    },
    {
        "place_name": "Thiksey Monastery (Mini Potala)",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.8,
        "location": "Thiksey, Indus Valley", "distance_from_city_centre": 19.0,
        "wiki_title": "Thikse Monastery",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Thikse_Monastery_Ladakh.jpg/800px-Thikse_Monastery_Ladakh.jpg",
        "description": "Twelve-storey Gelugpa complex resembling Lhasa's Potala Palace, housing a breathtaking 49-foot two-storey statue of Maitreya Future Buddha."
    },
    {
        "place_name": "Hemis Monastery & Mask Dance",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 150, "time_needed": 3.0, "rating": 4.7,
        "location": "Hemis, South of Indus River", "distance_from_city_centre": 45.0,
        "wiki_title": "Hemis Monastery",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Thikse_Monastery_Ladakh.jpg/800px-Thikse_Monastery_Ladakh.jpg",
        "description": "Wealthiest and largest Buddhist monastery in Ladakh, home to rare gold statues, ancient thangkas, and the vibrant Cham sacred mask dance festival."
    },
    {
        "place_name": "Sangam Point (Indus & Zanskar)",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 2, "shopping_score": 1, "culture_score": 3,
        "average_cost": 100, "time_needed": 2.0, "rating": 4.8,
        "location": "Nimmu, Leh-Srinagar Highway", "distance_from_city_centre": 32.0,
        "wiki_title": "Nimmu",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Pangong_Tso.jpg/800px-Pangong_Tso.jpg",
        "description": "Spectacular river confluence where the shimmering emerald green waters of the Indus meet the muddy brown rapids of the Zanskar River amidst canyon cliffs."
    },
    {
        "place_name": "Diskit Monastery & 106ft Buddha",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 150, "time_needed": 3.0, "rating": 4.8,
        "location": "Diskit, Nubra Valley", "distance_from_city_centre": 115.0,
        "wiki_title": "Diskit Monastery",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Hunder_sand_dunes_Ladakh.jpg/800px-Hunder_sand_dunes_Ladakh.jpg",
        "description": "Oldest and largest gompa in the Nubra Valley, crowned by a majestic 106-foot tall colorful statue of Maitreya Buddha overlooking the riverbed."
    },
    {
        "place_name": "Alchi Monastery & Ancient Murals",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 4, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 2, "culture_score": 5,
        "average_cost": 100, "time_needed": 2.5, "rating": 4.6,
        "location": "Alchi Village, Indus River", "distance_from_city_centre": 65.0,
        "wiki_title": "Alchi Monastery",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Thikse_Monastery_Ladakh.jpg/800px-Thikse_Monastery_Ladakh.jpg",
        "description": "11th-century monastic enclave famed for remarkably preserved Kashmiri-style Buddhist wood carvings, wall paintings, and miniature artwork."
    },
    {
        "place_name": "Hall of Fame Army Museum",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 1, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 3, "culture_score": 4,
        "average_cost": 250, "time_needed": 2.0, "rating": 4.7,
        "location": "Leh-Kargil Road", "distance_from_city_centre": 4.5,
        "wiki_title": "Hall of Fame, Leh",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Leh_Palace_from_below.jpg/800px-Leh_Palace_from_below.jpg",
        "description": "Museum built and maintained by the Indian Army commemorating brave soldiers of Siachen and Kargil, with exhibits on Ladakhi culture and flora."
    },
    {
        "place_name": "Tso Moriri High-Altitude Ramsar Lake",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 5, "food_score": 1, "history_score": 1, "shopping_score": 1, "culture_score": 3,
        "average_cost": 1500, "time_needed": 7.0, "rating": 4.8,
        "location": "Changthang, Korzok", "distance_from_city_centre": 220.0,
        "wiki_title": "Tso Moriri",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Pangong_Tso.jpg/800px-Pangong_Tso.jpg",
        "description": "Stunning alpine lake at 14,836 feet surrounded by snow peaks, home to the nomadic Changpa tribe and rare black-necked cranes."
    },
    {
        "place_name": "Lamayuru Monastery (Moonland)",
        "destination": "Leh Ladakh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 5, "adventure_score": 3, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 200, "time_needed": 3.5, "rating": 4.7,
        "location": "Lamayuru, Leh-Srinagar Highway", "distance_from_city_centre": 115.0,
        "wiki_title": "Lamayuru Monastery",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Thikse_Monastery_Ladakh.jpg/800px-Thikse_Monastery_Ladakh.jpg",
        "description": "Ancient 11th-century Drikung Kagyu monastery perched on cliffs over surreal yellow-white eroded sediment terrain known as the Moonland of Ladakh."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 9. RISHIKESH (13 Places)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "place_name": "Triveni Ghat Evening Maha Aarti",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 3, "adventure_score": 1, "food_score": 3, "history_score": 4, "shopping_score": 3, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.8,
        "location": "Mayakund, Central Rishikesh", "distance_from_city_centre": 1.0,
        "wiki_title": "Triveni Ghat",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Ganga_Aarti_Rishikesh.jpg/800px-Ganga_Aarti_Rishikesh.jpg",
        "description": "The sacred confluence where thousands gather at sunset for the stirring Ganga Aarti with glowing brass lamps, ringing bells, and Vedic chants."
    },
    {
        "place_name": "Lakshman Jhula Suspension Bridge",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "History",
        "nature_score": 4, "adventure_score": 3, "food_score": 4, "history_score": 5, "shopping_score": 4, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.6,
        "location": "Tapovan / Lakshman Jhula", "distance_from_city_centre": 4.5,
        "wiki_title": "Lakshman Jhula",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "Iconic 450-foot iron suspension bridge spanning the emerald Ganges river, connecting spiritual cafes, ashrams, and temples with Himalayan vistas."
    },
    {
        "place_name": "Ganges River White Water Rafting",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 850, "time_needed": 4.0, "rating": 4.9,
        "location": "Shivpuri to NIM Beach Stretch", "distance_from_city_centre": 16.0,
        "wiki_title": "Rishikesh",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "World-class white-water rafting navigating exhilarating rapids like Roller Coaster, Golf Course, and Club House along the pristine turquoise Ganges."
    },
    {
        "place_name": "The Beatles Ashram (Chaurasi Kutia)",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 5, "adventure_score": 2, "food_score": 2, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 300, "time_needed": 2.5, "rating": 4.6,
        "location": "Rajaji Tiger Reserve Boundary, Swarg Ashram", "distance_from_city_centre": 4.0,
        "wiki_title": "Beatles Ashram",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Ganga_Aarti_Rishikesh.jpg/800px-Ganga_Aarti_Rishikesh.jpg",
        "description": "Atmospheric woodland ashram of Maharishi Mahesh Yogi where The Beatles composed the White Album in 1968, filled with stone meditation huts and murals."
    },
    {
        "place_name": "Neer Garh Waterfall Nature Hike",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 4, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 100, "time_needed": 3.0, "rating": 4.6,
        "location": "Neer Waterfall Road, Badrinath Highway", "distance_from_city_centre": 7.0,
        "wiki_title": "Neer Garh Waterfall",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "Two-tiered crystal mountain cascade hidden in forested hills with cool turquoise natural rock bathing pools reached via an invigorating uphill trail."
    },
    {
        "place_name": "Parmarth Niketan Ashram & Music Satsang",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 4, "adventure_score": 1, "food_score": 3, "history_score": 4, "shopping_score": 2, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.5, "rating": 4.7,
        "location": "Swarg Ashram, Ganga Waterfront", "distance_from_city_centre": 3.5,
        "wiki_title": "Parmarth Niketan",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Ganga_Aarti_Rishikesh.jpg/800px-Ganga_Aarti_Rishikesh.jpg",
        "description": "Rishikesh's largest yoga ashram, featuring manicured gardens, spiritual satsangs, and the renowned sunset Ganga Aarti led by ashram gurukul students."
    },
    {
        "place_name": "Kunjapuri Devi Sunrise Temple",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 4, "food_score": 1, "history_score": 4, "shopping_score": 1, "culture_score": 5,
        "average_cost": 250, "time_needed": 3.5, "rating": 4.8,
        "location": "Kunjapuri Peak, Tehri Garhwal", "distance_from_city_centre": 26.0,
        "wiki_title": "Kunjapuri Temple",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "One of the 52 sacred Shakti Peeths sitting at 5,400 feet, famed for ethereal Himalayan dawn panoramas illuminating Chaukhamba and Swargarohini peaks."
    },
    {
        "place_name": "Vashistha Cave Meditation Cavern",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 5, "adventure_score": 2, "food_score": 1, "history_score": 5, "shopping_score": 1, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.7,
        "location": "Badrinath Road, Shivpuri", "distance_from_city_centre": 22.0,
        "wiki_title": "Vashistha Cave",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Ganga_Aarti_Rishikesh.jpg/800px-Ganga_Aarti_Rishikesh.jpg",
        "description": "Quiet ancient natural cave on the banks of the Ganges where Sage Vashistha meditated, revered for its profound spiritual stillness and river beach."
    },
    {
        "place_name": "Jumpin Heights India Bungee Jump",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 1, "history_score": 1, "shopping_score": 1, "culture_score": 1,
        "average_cost": 3500, "time_needed": 4.0, "rating": 4.9,
        "location": "Mohan Chatti Village", "distance_from_city_centre": 28.0,
        "wiki_title": "Jumpin Heights",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "India's highest fixed-platform bungee jump leaping 83 meters above the Hall River gorge, operated by New Zealand safety jump masters."
    },
    {
        "place_name": "Tera Manzil Trimbakeshwar Temple",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Culture",
        "nature_score": 2, "adventure_score": 2, "food_score": 2, "history_score": 4, "shopping_score": 3, "culture_score": 5,
        "average_cost": 50, "time_needed": 1.5, "rating": 4.5,
        "location": "Lakshman Jhula Ghat", "distance_from_city_centre": 4.5,
        "wiki_title": "Trayambakeshwar Temple, Rishikesh",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "Eye-catching thirteen-storey temple complex towering right at the foot of Lakshman Jhula, enshrining hundreds of Hindu deities on each terrace level."
    },
    {
        "place_name": "Ram Jhula & Geeta Bhawan Walk",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Relaxation",
        "nature_score": 3, "adventure_score": 2, "food_score": 4, "history_score": 4, "shopping_score": 4, "culture_score": 5,
        "average_cost": 50, "time_needed": 2.0, "rating": 4.6,
        "location": "Swarg Ashram / Muni Ki Reti", "distance_from_city_centre": 3.0,
        "wiki_title": "Ram Jhula",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "Elegant iron suspension bridge connecting Muni Ki Reti with Swarg Ashram, bustling with sadhus, organic sweet shops, and Gita Bhavan's epic murals."
    },
    {
        "place_name": "Patna Waterfall & Limestone Caves",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Nature",
        "nature_score": 5, "adventure_score": 4, "food_score": 1, "history_score": 2, "shopping_score": 1, "culture_score": 2,
        "average_cost": 50, "time_needed": 2.5, "rating": 4.5,
        "location": "Patna Village, Neelkanth Temple Road", "distance_from_city_centre": 11.0,
        "wiki_title": "Rishikesh",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Ganga_Aarti_Rishikesh.jpg/800px-Ganga_Aarti_Rishikesh.jpg",
        "description": "Secluded waterfall cascading over limestone cliffs containing natural caves, reached by a scenic short jungle hike above the Ganges."
    },
    {
        "place_name": "Kaudiyala White Sands & Kayaking",
        "destination": "Rishikesh", "country": "India", "region": "North India",
        "category": "Adventure",
        "nature_score": 5, "adventure_score": 5, "food_score": 2, "history_score": 1, "shopping_score": 1, "culture_score": 2,
        "average_cost": 750, "time_needed": 4.0, "rating": 4.7,
        "location": "Kaudiyala, Badrinath Highway", "distance_from_city_centre": 38.0,
        "wiki_title": "Rishikesh",
        "fallback_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lakshman_Jhula_Rishikesh.jpg/800px-Lakshman_Jhula_Rishikesh.jpg",
        "description": "Dramatic white sand river beaches along the Upper Ganges famous for Grade IV rapids (The Wall), river camping, night bonfires, and open-water kayaking."
    },
]

print(f"Loaded destinations 6-9 places: {len(DESTINATIONS_6_TO_20)}")

