# fetching aircraft by registration number and inserting into MySQL database
import requests, time
from config import APIConfig, DBConfig

def fetch_aircraft_by_reg(registration):
    # Use /aircrafts/reg/{registration} for current info
    url = f"https://{APIConfig.HOST}/aircrafts/reg/{registration}"
    response = requests.get(url, headers=APIConfig.HEADERS)
    
    # Handle rate limit (HTTP 429)
    if response.status_code == 429:
        print("⚠️ Rate limit hit. Waiting 10 seconds...")
        time.sleep(10)
        return fetch_aircraft_by_reg(registration)
    
    response.raise_for_status()
    return response.json()

def insert_aircraft(cursor, aircraft_data):
    """Insert aircraft data into MySQL table."""
    reg = aircraft_data.get("reg")
    model = aircraft_data.get("model")
    manufacturer = aircraft_data.get("typeName") or aircraft_data.get("productionLine")
    icao_type_code = aircraft_data.get("icaoTypeCode") or aircraft_data.get("modelCode")
    owner = aircraft_data.get("airlineName")  # using airlineName as owner/operator

    cursor.execute("""
    INSERT INTO aircraft
        (registration, model, manufacturer, icao_type_code, owner)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            model = VALUES(model),
            manufacturer = VALUES(manufacturer),
            icao_type_code = VALUES(icao_type_code),
            owner = VALUES(owner);
    """,
    (reg, model, manufacturer, icao_type_code, owner)
    )


# List of aircraft registrations
registrations = ["TF-ELD", "VP-BZP", "PH-BXO", "D-ABYA", "F-GSQK", "JA823J", "HS-TJD", "9V-SKA", "C-FIVQ", "G-EZUI"]
connection, cursor = DBConfig.get_connection()

for reg in registrations:
    try:
        aircraft_data = fetch_aircraft_by_reg(reg)
        insert_aircraft(cursor, aircraft_data)
        print(f"✅ Inserted/Updated aircraft {reg} successfully")
        time.sleep(2)  # pause to avoid hitting rate limits
    except Exception as e:
        print(f"❌ Error fetching {reg}: {e}")

connection.commit()
cursor.close()
connection.close()
