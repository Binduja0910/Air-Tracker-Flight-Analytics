# fetching airport by IATA code and inserting into MySQL database
import requests, time
from config import APIConfig, DBConfig

def fetch_airport_by_iata(iata_code):
    """Fetch airport details from AeroDataBox API by IATA code."""
    url = f"https://{APIConfig.HOST}/airports/iata/{iata_code}"
    response = requests.get(url, headers=APIConfig.HEADERS)

    # Handle rate limit (HTTP 429)
    if response.status_code == 429:
        print("⚠️ Rate limit hit. Waiting 10 seconds...")
        time.sleep(10)
        return fetch_airport_by_iata(iata_code)

    response.raise_for_status()
    return response.json()

def insert_airport(cursor, airport_data):
    """Insert airport data into MySQL table."""
    icao_code = airport_data.get("icao")
    iata_code = airport_data.get("iata")
    name = airport_data.get("fullName")
    city = airport_data.get("municipalityName")
    country = airport_data.get("country", {}).get("name")
    continent = airport_data.get("continent", {}).get("name")
    latitude = airport_data.get("location", {}).get("lat")
    longitude = airport_data.get("location", {}).get("lon")
    timezone = airport_data.get("timeZone")

    cursor.execute("""
    INSERT INTO airport
        (icao_code, iata_code, name, city, country, continent, latitude, longitude, timezone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        city = VALUES(city),
        country = VALUES(country),
        continent = VALUES(continent),
        latitude = VALUES(latitude),
        longitude = VALUES(longitude),
        timezone = VALUES(timezone);
    """,
    (icao_code, iata_code, name, city, country, continent, latitude, longitude, timezone)
    )


# List of IATA codes for airports
iata_codes = ["DEL", "BLR", "MAA", "AMS", "BOM", "LAX", "JFK", "LHR", "CDG", "HND"]
connection, cursor = DBConfig.get_connection()

for iata in iata_codes:
    try:
        airport_data = fetch_airport_by_iata(iata)
        insert_airport(cursor, airport_data)
        print(f"✅ Inserted/Updated {iata} successfully")
        time.sleep(2)  # pause to avoid hitting rate limits
    except Exception as e:
        print(f"❌ Error fetching {iata}: {e}")

connection.commit()
cursor.close()
connection.close()
