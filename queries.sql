-- ===========================
-- Query 1
-- Show the total number of flights for each aircraft model
-- ===========================
SELECT a.model, COUNT(f.flight_id) AS flight_count
FROM flights f
JOIN aircraft a ON f.aircraft_registration = a.registration
GROUP BY a.model;

-- ===========================
-- Query 2
-- List all aircraft (registration, model) with more than 5 flights
-- ===========================
SELECT a.registration, a.model, COUNT(f.flight_id) AS flight_count
FROM flights f
JOIN aircraft a ON f.aircraft_registration = a.registration
GROUP BY a.registration, a.model
HAVING COUNT(f.flight_id) > 5;

-- ===========================
-- Query 3
-- For each airport, show name and outbound flights (>5)
-- ===========================
SELECT ap.name, COUNT(f.flight_id) AS outbound_flights
FROM flights f
JOIN airport ap ON f.origin_iata = ap.iata_code
GROUP BY ap.name
HAVING COUNT(f.flight_id) > 5;

-- ===========================
-- Query 4
-- Find top 3 destination airports (name, city) by arrivals
-- ===========================
SELECT ap.name, ap.city, COUNT(f.flight_id) AS arrivals
FROM flights f
JOIN airport ap ON f.destination_iata = ap.iata_code
GROUP BY ap.name, ap.city
ORDER BY arrivals DESC
LIMIT 3;

-- ===========================
-- Query 5
-- Show flight number, origin, destination, Domestic/International
-- ===========================
SELECT f.flight_number,
       f.origin_iata,
       f.destination_iata,
       CASE 
           WHEN ap1.country = ap2.country THEN 'Domestic'
           ELSE 'International'
       END AS route_type
FROM flights f
JOIN airport ap1 ON f.origin_iata = ap1.iata_code
JOIN airport ap2 ON f.destination_iata = ap2.iata_code;

-- ===========================
-- Query 6
-- Show 5 most recent arrivals at DEL
-- ===========================
SELECT f.flight_number,
       f.aircraft_registration,
       ap.name AS departure_airport,
       f.actual_arrival
FROM flights f
JOIN airport ap ON f.origin_iata = ap.iata_code
WHERE f.destination_iata = 'DEL'
ORDER BY f.actual_arrival DESC
LIMIT 5;

-- ===========================
-- Query 7
-- Find airports with no arriving flights
-- ===========================
SELECT ap.name, ap.iata_code
FROM airport ap
WHERE ap.iata_code NOT IN (
    SELECT DISTINCT destination_iata FROM flights
);

-- ===========================
-- Query 8
-- For each airline, count flights by status
-- ===========================
SELECT airline_code,
       SUM(CASE WHEN status = 'On Time' THEN 1 ELSE 0 END) AS on_time_count,
       SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count,
       SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_count
FROM flights
GROUP BY airline_code;

-- ===========================
-- Query 9
-- Show cancelled flights with aircraft and airports
-- ===========================
SELECT f.flight_number,
       f.aircraft_registration,
       ap1.name AS origin_airport,
       ap2.name AS destination_airport,
       f.scheduled_departure
FROM flights f
JOIN airport ap1 ON f.origin_iata = ap1.iata_code
JOIN airport ap2 ON f.destination_iata = ap2.iata_code
WHERE f.status = 'Cancelled'
ORDER BY f.scheduled_departure DESC;

-- ===========================
-- Query 10
-- List city pairs with >2 different aircraft models
-- ===========================
SELECT ap1.city AS origin_city,
       ap2.city AS destination_city,
       COUNT(DISTINCT a.model) AS model_count
FROM flights f
JOIN airport ap1 ON f.origin_iata = ap1.iata_code
JOIN airport ap2 ON f.destination_iata = ap2.iata_code
JOIN aircraft a ON f.aircraft_registration = a.registration
GROUP BY ap1.city, ap2.city
HAVING COUNT(DISTINCT a.model) > 2;

-- ===========================
-- Query 11
-- Compute % of delayed flights per destination airport
-- ===========================
SELECT ap.name AS destination_airport,
       (SUM(CASE WHEN f.status = 'Delayed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS delayed_percentage
FROM flights f
JOIN airport ap ON f.destination_iata = ap.iata_code
GROUP BY ap.name
ORDER BY delayed_percentage DESC;
