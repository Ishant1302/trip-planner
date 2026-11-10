import os
import shutil
import urllib.request
import ssl
import hashlib
import pandas as pd
from collections import defaultdict

FRONTEND_UPLOADS = os.path.abspath('frontend/public/uploads')
BACKEND_UPLOADS = os.path.abspath('backend/uploads')
DESTINATIONS_CSV = os.path.abspath('backend/datasets/destinations.csv')
PLACES_CSV = os.path.abspath('backend/datasets/places.csv')

os.makedirs(FRONTEND_UPLOADS, exist_ok=True)
os.makedirs(BACKEND_UPLOADS, exist_ok=True)

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'VoyageML/1.0 (academic travel project; contact@voyageml.edu)'}

# 1. 20 Destination Covers
DESTINATION_COVERS = {
    'Spiti Valley': {
        'file': 'cover_spiti_valley.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Spiti_River_Kaza_Himachal_Jun18_D72_7232.jpg/1280px-Spiti_River_Kaza_Himachal_Jun18_D72_7232.jpg'
    },
    'Leh Ladakh': {
        'file': 'cover_leh_ladakh.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/e/e5/Thikse_Monastery_.jpg'
    },
    'Manali': {
        'file': 'cover_manali.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/0/03/Manali_City.jpg'
    },
    'Jaipur': {
        'file': 'cover_jaipur.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/4/41/East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg'
    },
    'Jaisalmer': {
        'file': 'cover_jaisalmer.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Jaisalmer_forteresse.jpg'
    },
    'Hampi': {
        'file': 'cover_hampi.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Wide_angle_of_Galigopuram_of_Virupaksha_Temple%2C_Hampi_%2804%29_%28cropped%29.jpg/1280px-Wide_angle_of_Galigopuram_of_Virupaksha_Temple%2C_Hampi_%2804%29_%28cropped%29.jpg'
    },
    'Munnar': {
        'file': 'cover_munnar.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Munnar_Overview.jpg/1280px-Munnar_Overview.jpg'
    },
    'Kerala Backwaters': {
        'file': 'cover_kerala_backwaters.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/e/ee/House_Boat_DSW.jpg'
    },
    'Goa': {
        'file': 'cover_goa.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Palolem_Beach%2C_South_Goa.jpg/1280px-Palolem_Beach%2C_South_Goa.jpg'
    },
    'Ooty': {
        'file': 'cover_ooty.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Arts_College_Hill_Ooty_Nilgiris_Mar21_A7C_00188.jpg/1280px-Arts_College_Hill_Ooty_Nilgiris_Mar21_A7C_00188.jpg'
    },
    'Rishikesh': {
        'file': 'cover_rishikesh.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Rishikesh-Lakshman_Jhula_by_Kaustubh_Nayyar.jpg/1280px-Rishikesh-Lakshman_Jhula_by_Kaustubh_Nayyar.jpg'
    },
    'Mysore': {
        'file': 'cover_mysore.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Mysore_Palace_Morning.jpg/1280px-Mysore_Palace_Morning.jpg'
    },
    'Varanasi': {
        'file': 'cover_varanasi.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Dasaswamedh_ghat-varanasi_india-andres_larin.jpg/1280px-Dasaswamedh_ghat-varanasi_india-andres_larin.jpg'
    },
    'Agra': {
        'file': 'cover_agra.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/1/1d/Taj_Mahal_%28Edited%29.jpeg'
    },
    'Mumbai': {
        'file': 'cover_mumbai.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/3/3a/Mumbai_03-2016_30_Gateway_of_India.jpg'
    },
    'Udaipur': {
        'file': 'cover_udaipur.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/6/69/Udaipur_City_Palace.jpg'
    },
    'Coorg': {
        'file': 'cover_coorg.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/0/02/Raja%27s_Seat_View_Point.jpg'
    },
    'Darjeeling': {
        'file': 'cover_darjeeling.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/9/96/DarjeelingTrainFruitshop_%282%29.jpg'
    },
    'Andaman Islands': {
        'file': 'cover_andaman_islands.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/8/87/Havelock_Island%2C_Radhanagar_Beach_before_sunset%2C_Andaman_Islands.jpg'
    },
    'Kolkata': {
        'file': 'cover_kolkata.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Victoria_Memorial_situated_in_Kolkata.jpg/1280px-Victoria_Memorial_situated_in_Kolkata.jpg'
    }
}

# 2. Specific Attraction replacements
ATTRACTION_IMAGES = {
    ('Varanasi', 'Sunrise Ganges Boat Ride along Ghats'): {
        'file': 'varanasi_sunrise_ganges_boat_ride_along_ghats.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Ahilya_Ghat_by_the_Ganges%2C_Varanasi.jpg/1280px-Ahilya_Ghat_by_the_Ganges%2C_Varanasi.jpg'
    },
    ('Varanasi', 'Kashi Vishwanath Temple Golden Corridor'): {
        'file': 'varanasi_kashi_vishwanath_temple_golden_corri.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Kashi_Vishwanath.jpg'
    },
    ('Varanasi', 'Kachori Gali & Blue Lassi Food Walk'): {
        'file': 'varanasi_kachori_gali_blue_lassi_food_walk.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Salt_lassi.jpg'
    },
    ('Coorg', 'Abbey Falls Cascading Stream'): {
        'file': 'coorg_abbey_falls_cascading_stream.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Abbey_Falls_New.jpg/1280px-Abbey_Falls_New.jpg'
    },
    ('Coorg', "Raja's Seat Sunset Viewpoint"): {
        'file': 'coorg_raja_s_seat_sunset_viewpoint.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/0/02/Raja%27s_Seat_View_Point.jpg'
    },
    ('Coorg', 'Tadiandamol Peak Mountain Trek'): {
        'file': 'coorg_tadiandamol_peak_mountain_trek.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Tadiandamol_Trek_25Aug_Pic_3_View_From_Top.jpg/1280px-Tadiandamol_Trek_25Aug_Pic_3_View_From_Top.jpg'
    },
    ('Coorg', 'Mandalpatti Peak 4x4 Jeep Safari'): {
        'file': 'coorg_mandalpatti_peak_4x4_jeep_safari.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Mandalpatti_Hills.jpg/1280px-Mandalpatti_Hills.jpg'
    },
    ('Coorg', 'Nisargadhama Bamboo River Island'): {
        'file': 'coorg_nisargadhama_bamboo_river_island.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/2/26/Nisargadhama_Hanging_Bridge.jpg'
    },
    ('Rishikesh', 'Neer Garh Waterfall Nature Hike'): {
        'file': 'rishikesh_neer_garh_waterfall_nature_hike.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/0/03/Neer_Garh_Waterfall.jpg'
    },
    ('Rishikesh', 'Kunjapuri Devi Sunrise Temple'): {
        'file': 'rishikesh_kunjapuri_devi_sunrise_temple.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/9/92/Kunjapuri_Temple%2C_Rishikesh%2C_Uttarakhand%2C_India_%2815110748073%29.jpg'
    },
    ('Rishikesh', 'Vashistha Cave Meditation Cavern'): {
        'file': 'rishikesh_vashistha_cave_meditation_cavern.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Vashistha_temple_%2816871894434%29.jpg'
    },
    ('Rishikesh', 'Kaudiyala White Sands & Kayaking'): {
        'file': 'rishikesh_kaudiyala_white_sands_kayaking.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/6/68/River_Ganga_at_Kaudiyala.jpg'
    },
    ('Jaipur', 'Nahargarh Fort Sunset Viewpoint'): {
        'file': 'jaipur_nahargarh_fort_sunset_viewpoint.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Nahargarh_13.jpg'
    },
    ('Jaipur', 'Chokhi Dhani Ethnic Village'): {
        'file': 'jaipur_chokhi_dhani_ethnic_village.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/5/5b/Pottery_at_the_Chokhi_Dhani_Resort_Panchkula_31.jpg'
    },
    ('Kolkata', 'College Street Boi Para Book Market'): {
        'file': 'kolkata_college_street_boi_para_book_market.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/College_Street_-_Kolkata_7387.JPG/1280px-College_Street_-_Kolkata_7387.JPG'
    },
    ('Mysore', 'Devaraja Market Heritage Bazaar'): {
        'file': 'mysore_devaraja_market_heritage_bazaar.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/2/25/Devaraja_Market%2C_Mysore_%28306989724%29.jpg'
    },
    ('Mysore', 'Lalitha Mahal Palace Panoramic Estate'): {
        'file': 'mysore_lalitha_mahal_palace_panoramic_estate.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Lalitha_Mahal_Palace_Hotel.jpg/1280px-Lalitha_Mahal_Palace_Hotel.jpg'
    },
    ('Mysore', 'Mysore Railway Museum Heritage Locos'): {
        'file': 'mysore_railway_museum_heritage_locos.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Mysuru_rail_museum_entrance.jpg/1280px-Mysuru_rail_museum_entrance.jpg'
    },
    ('Ooty', 'Doddabetta Peak Nilgiris Highest Crest'): {
        'file': 'ooty_doddabetta_peak_nilgiris_highest_crest.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Arts_College_Hill_Ooty_Nilgiris_Mar21_A7C_00188.jpg/1280px-Arts_College_Hill_Ooty_Nilgiris_Mar21_A7C_00188.jpg'
    },
    ('Ooty', 'Avalanche Lake Pristine Biosphere'): {
        'file': 'ooty_avalanche_lake_pristine_biosphere.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Avalanche_lake_ooty_1.jpg'
    },
    ('Ooty', 'Emerald Lake Tea Plantation Basin'): {
        'file': 'ooty_emerald_lake_tea_plantation_basin.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/3/32/Emerald_Lake_Ooty_-_panoramio.jpg'
    },
    ('Udaipur', 'Ambrai Ghat Promenade'): {
        'file': 'udaipur_ambrai_ghat_promenade.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/7/79/Ambrai_ghat_at_evening.jpg'
    },
    ('Mumbai', 'Colaba Causeway Flea Market'): {
        'file': 'mumbai_colaba_causeway_flea_market.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Colaba_Causeway.jpg/1280px-Colaba_Causeway.jpg'
    },
    ('Darjeeling', 'Tenzing Rock Climbing Site'): {
        'file': 'darjeeling_tenzing_rock_climbing_site.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Tenzing_Rock.jpg/1280px-Tenzing_Rock.jpg'
    }
}

def download_and_save(url: str, filename: str) -> bool:
    target_f = os.path.join(FRONTEND_UPLOADS, filename)
    target_b = os.path.join(BACKEND_UPLOADS, filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = r.read()
            if len(data) < 5000:
                print(f"Warning: {filename} downloaded only {len(data)} bytes")
                return False
            with open(target_f, 'wb') as fp:
                fp.write(data)
            with open(target_b, 'wb') as fp:
                fp.write(data)
            print(f"SUCCESS: Saved {filename} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"FAILED to download {filename} from {url}: {e}")
        return False

print("=== STEP 1: DOWNLOADING ALL 20 DESTINATION COVERS ===")
for dest, info in DESTINATION_COVERS.items():
    print(f"Downloading cover for {dest}...")
    download_and_save(info['url'], info['file'])

print("\n=== STEP 2: DOWNLOADING TARGET ATTRACTION IMAGES ===")
for (dest, place), info in ATTRACTION_IMAGES.items():
    print(f"Downloading attraction for {dest} -> {place}...")
    download_and_save(info['url'], info['file'])

print("\n=== STEP 3: UPDATING destinations.csv ===")
dest_df = pd.read_csv(DESTINATIONS_CSV)
for idx, row in dest_df.iterrows():
    dname = row['destination']
    if dname in DESTINATION_COVERS:
        fname = DESTINATION_COVERS[dname]['file']
        dest_df.at[idx, 'image'] = f"/uploads/{fname}"
dest_df.to_csv(DESTINATIONS_CSV, index=False)
print("Updated destinations.csv successfully!")
print(dest_df[['destination', 'image']].to_string())

print("\n=== STEP 4: UPDATING places.csv ===")
places_df = pd.read_csv(PLACES_CSV)
for (dest, place), info in ATTRACTION_IMAGES.items():
    fname = info['file']
    mask = (places_df['destination'].str.lower() == dest.lower()) & (places_df['place_name'].str.lower() == place.lower())
    if mask.any():
        places_df.loc[mask, 'image'] = f"/uploads/{fname}"
        print(f"Updated places.csv: {dest} | {place} -> /uploads/{fname}")
    else:
        # Partial match if needed
        p_sub = place.split()[0].lower()
        mask2 = (places_df['destination'].str.lower() == dest.lower()) & (places_df['place_name'].str.lower().str.contains(p_sub))
        if mask2.any():
            places_df.loc[mask2, 'image'] = f"/uploads/{fname}"
            print(f"Updated places.csv (partial match): {dest} | {place} -> /uploads/{fname}")

places_df.to_csv(PLACES_CSV, index=False)
print("Updated places.csv successfully!")

print("\n=== STEP 5: VERIFYING ZERO MISSING & ZERO DUPLICATE COVERS ===")
dest_df = pd.read_csv(DESTINATIONS_CSV)
cover_hashes = {}
for idx, row in dest_df.iterrows():
    img_path = row['image']
    fname = os.path.basename(img_path)
    full_p = os.path.join(FRONTEND_UPLOADS, fname)
    if not os.path.exists(full_p):
        print(f"ERROR: Cover {full_p} does NOT exist!")
    else:
        with open(full_p, 'rb') as f:
            h = hashlib.md5(f.read()).hexdigest()
        if h in cover_hashes:
            print(f"DUPLICATE DETECTED: {row['destination']} and {cover_hashes[h]} share the same image ({fname})!")
        else:
            cover_hashes[h] = row['destination']
            print(f"OK: {row['destination']:<20} -> {fname} ({os.path.getsize(full_p)} bytes, MD5: {h[:8]})")

print("\n=== SCRIPT FINISHED SUCCESSFULLY ===")

