# fetching airport delays by ICAO code and inserting into MySQL database
import requests, time
from datetime import datetime
from config import APIConfig, DBConfig

def delay_minutes(delay_str):
    if not delay_str:   # handles None or empty string
        return 0
    if delay_str.startswith('-'):
        h, m, s = map(int, delay_str.strip('-').split(':'))
        sign = -1
    else:
        h, m, s = map(int, delay_str.split(':'))
        sign = 1
    return sign * (h * 60 + m + (s // 60))

def fetch_airport_delays(icao_code):
    url = f"https://{APIConfig.HOST}/airports/icao/{icao_code}/delays"
    response = requests.get(url, headers=APIConfig.HEADERS)

    # Handle rate limit (HTTP 429)
    if response.status_code == 429:
        print("⚠️ Rate limit hit. Waiting 10 seconds...")
        time.sleep(10)
        return fetch_airport_delays(icao_code)

    response.raise_for_status()
    return response.json()

def insert_delay_records(cursor, icao_code, delay_data):
    # ICAO → IATA mapping kept inside the function
    icao_to_iata = {"VIDP": "DEL", "VOBL": "BLR", "VOMM": "MAA", "EHAM": "AMS", "VABB": "BOM", 
                    "KLAX": "LAX","KJFK": "JFK", "EGLL": "LHR", "LFPG": "CDG", "RJTT": "HND"}

    airport_iata = icao_to_iata.get(icao_code)
    delay_date = datetime.now().strftime("%Y-%m-%d")

    for direction in ("departures", "arrivals"):
        info = delay_data.get(f"{direction}DelayInformation", {})
        num_total = info.get("numTotal", 0)
        num_cancelled = info.get("numCancelled", 0)
        median_delay = delay_minutes(info.get("medianDelay"))
        delayed_flights = int(info.get("delayIndex", 0) * num_total)
        delay_index = info.get("delayIndex", 0)

        cursor.execute("""
            INSERT INTO airport_delays
                (airport_iata, delay_date, total_flights, delayed_flights,
                 median_delay_min, canceled_flights, delay_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                total_flights = VALUES(total_flights),
                delayed_flights = VALUES(delayed_flights),
                median_delay_min = VALUES(median_delay_min),
                canceled_flights = VALUES(canceled_flights),
                delay_index = VALUES(delay_index);
        """, (airport_iata, delay_date, num_total, delayed_flights, median_delay, num_cancelled, delay_index))

        print(f"✅ Inserted/Updated {direction} delays for {airport_iata} on {delay_date}")

# Run for all ICAO codes
icao_codes = ["EHAM", "VOBL", "VOMM", "VABB", "KLAX", "KJFK", "EGLL", "LFPG", "RJTT","VIDP"]

connection, cursor = DBConfig.get_connection()

for icao in icao_codes:
    try:
        delay_data = fetch_airport_delays(icao)
        insert_delay_records(cursor, icao, delay_data)
        print(f"✅ Inserted/Updated {icao} successfully")
        time.sleep(2) # pause to avoid hitting rate limits
    except Exception as e:
        print(f"❌ Error fetching delays for {icao}: {e}")

connection.commit()
cursor.close()
connection.close()
