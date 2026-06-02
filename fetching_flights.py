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

def insert_flight(cursor, flight_data: dict):
    for row in flight_data.keys():
        for i in range(len(flight_data.get(row))):
            aircraft_registration = (flight_data.get(row)[i].get("aircraft").get("reg"))
            flight_number = flight_data.get(row)[i].get("number")
            origin_iata = flight_data.get(row)[i].get("arrival").get("airport").get("iata")
            destination_iata = flight_data.get(row)[i].get("arrival").get("airport").get("iata")
            scheduled_departure = datetime.fromisoformat(flight_data.get(row)[i].get("departure").get("scheduledTimeLocal")).strftime("%Y-%m-%d %H:%M")
            actual_departure = datetime.fromisoformat(flight_data.get(row)[i].get("departure").get("actualTimeLocal")).strftime("%Y-%m-%d %H:%M")
            scheduled_arrival = datetime.fromisoformat(flight_data.get(row)[i].get("arrival").get("scheduledTimeLocal")).strftime("%Y-%m-%d %H:%M")
            actual_arrival = datetime.fromisoformat(flight_data.get(row)[i].get("arrival").get("actualTimeLocal")).strftime("%Y-%m-%d %H:%M")
            status = flight_data.get(row)[i].get("status")
            airline_code = flight_data.get(row)[i].get("airline").get("name")

            cursor.execute("""
                INSERT INTO flights_bk (
                    flight_number, aircraft_registration, origin_iata, destination_iata,
                    scheduled_departure, actual_departure, scheduled_arrival, actual_arrival,
                    status, airline_code
                )
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    actual_departure = VALUES(actual_departure),
                    actual_arrival = VALUES(actual_arrival),
                    status = VALUES(status),
                    aircraft_registration = VALUES(aircraft_registration),
                    airline_code = VALUES(airline_code)
                """,
                (flight_number, aircraft_registration, origin_iata, destination_iata,
                scheduled_departure, actual_departure, scheduled_arrival, actual_arrival,
                status, airline_code))

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
