import requests, time
from datetime import datetime, timedelta
from config import APIConfig, DBConfig

def fetch_flights(iata_code: str, start: str, end: str):
    url = (f"https://{APIConfig.HOST}/flights/airports/iata/{iata_code}/{start}/{end}"
           "?withLeg=true&direction=Both&withCancelled=true&withCodeshared=true"
           "&withCargo=true&withPrivate=true&withLocation=false")
    response = requests.get(url, headers=APIConfig.HEADERS)

    if response.status_code == 429:
        print("⚠️ Rate limit hit. Waiting 20 seconds...")
        time.sleep(20)
        return fetch_flights(iata_code, start, end)

    response.raise_for_status()
    return response.json()

def insert_flight(cursor, flight_data: dict, origin_context: str = None, destination_context: str = None):
    """Insert flight data into MySQL flights table (ignoring flight_id)."""

    # Flight basics
    flight_number = flight_data.get("number")
    aircraft_registration = flight_data.get("aircraft", {}).get("reg")

    # Origin/Destination handling
    origin_iata = flight_data.get("departure", {}).get("airport", {}).get("iata", origin_context)
    destination_iata = flight_data.get("arrival", {}).get("airport", {}).get("iata", destination_context)

    # Times
    scheduled_departure = flight_data.get("departure", {}).get("scheduledTimeLocal")
    actual_departure = flight_data.get("departure", {}).get("actualTimeLocal")
    scheduled_arrival = flight_data.get("arrival", {}).get("scheduledTimeLocal")
    actual_arrival = flight_data.get("arrival", {}).get("actualTimeLocal")

    # Status & airline
    status = flight_data.get("status")
    airline_code = flight_data.get("airline", {}).get("iata")  # may be None

    # Insert into DB
    cursor.execute(
        f"""
        INSERT INTO flights
        (flight_number, aircraft_registration, origin_iata, destination_iata,
         scheduled_departure, actual_departure, scheduled_arrival, actual_arrival, status, airline_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (flight_number, aircraft_registration, origin_iata, destination_iata,
         scheduled_departure, actual_departure, scheduled_arrival, actual_arrival, status, airline_code),
    )

# Airports
iata_codes = ["DEL", "BLR", "MAA", "AMS", "BOM", "LAX", "JFK", "LHR", "CDG", "HND"]
now = datetime.now()
start_time = now.strftime("%Y-%m-%dT%H:%M")
end_time = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")

connection, cursor = DBConfig.get_connection()

for iata in iata_codes:
    try:
        data = fetch_flights(iata, start_time, end_time)
        for flight in data.get("departures", []) + data.get("arrivals", []):
            try:
                insert_flight(cursor, flight)
                print(f"✅ Inserted/Updated flight {flight.get('number')} at {iata}")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Error inserting flight {flight.get('number')} at {iata}: {e}")
    except Exception as e:
        print(f"❌ Error fetching flights for {iata}: {e}")

connection.commit()
cursor.close()
connection.close()
