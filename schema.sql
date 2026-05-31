-- ===========================
-- Aircraft Table
-- ===========================
CREATE TABLE aircraft (
    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,
    registration VARCHAR(10) UNIQUE,   -- Aircraft registration (e.g., VT-ABC)
    model VARCHAR(50),                 -- Aircraft model (e.g., Airbus A320)
    manufacturer VARCHAR(50),          -- Manufacturer (e.g., Airbus, Boeing)
    icao_type_code VARCHAR(10),        -- ICAO type designator (e.g., A320)
    owner VARCHAR(100)                 -- Owner/operator
);
-- ===========================
-- Airport Table
-- ===========================
CREATE TABLE airport (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    icao_code VARCHAR(4) UNIQUE,       -- ICAO code (e.g., VOMM)
    iata_code CHAR(3) UNIQUE,          -- IATA code (e.g., MAA)
    name VARCHAR(100),                 -- Airport name
    city VARCHAR(100),                 -- City
    country VARCHAR(100),              -- Country
    continent VARCHAR(50),             -- Continent
    latitude DOUBLE,                   -- Latitude
    longitude DOUBLE,                  -- Longitude
    timezone VARCHAR(50)               -- Timezone string (e.g., Asia/Kolkata)
);
-- ===========================
-- Flights Table
-- ===========================
CREATE TABLE flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,          -- Unique identifier for each flight record
    flight_number VARCHAR(10) NOT NULL,                -- Airline flight number (e.g., "6E 6377")
    aircraft_registration VARCHAR(20),                 -- FK → aircraft.registration (unique aircraft tail number)
    origin_iata CHAR(3),                               -- FK → airport.iata_code (departure airport)
    destination_iata CHAR(3),                          -- arrival airport
    scheduled_departure DATETIME,                      -- Scheduled departure time
    actual_departure DATETIME,                         -- Actual departure time
    scheduled_arrival DATETIME,                        -- Scheduled arrival time
    actual_arrival DATETIME,                           -- Actual arrival time
    status VARCHAR(10),                                -- Flight status
    airline_code VARCHAR(5),                           -- Airline IATA code (e.g., "6E" for IndiGo)

    FOREIGN KEY (aircraft_registration) REFERENCES aircraft(registration)
);


-- ===========================
-- Airport Delays Table
-- ===========================
CREATE TABLE airport_delays (
    delay_id INT AUTO_INCREMENT PRIMARY KEY,           -- Unique identifier for each delay record
    airport_iata CHAR(3),                              -- FK → airport.iata_code
    delay_date DATE,                                   -- Date of delay statistics
    total_flights INT,                                 -- Total flights in the time window
    delayed_flights INT,                               -- Number of delayed flights (derived from delayIndex × numTotal)
    avg_delay_min INT,                                 -- Average delay in minutes (optional, may be NULL if not provided)
    median_delay_min INT,                              -- Median delay in minutes (converted from HH:MM:SS string)
    canceled_flights INT,                              -- Number of cancelled flights
    delay_index FLOAT,                                  -- Delay index (proportion of delayed flights)

    FOREIGN KEY (airport_iata) REFERENCES airport(iata_code),
    UNIQUE (airport_iata, delay_date)                  -- Prevent duplicate records for same airport/date
);
