1. Overview
This project provides insights into flight operations, aircraft usage, and airport performance using SQL-based analytics. It is designed to help data enthusiasts and developers practice querying, reporting, and building dashboards from aviation datasets.
-----------------------------------------------------------------------------------------------------
2. Project Structure
/data – Raw and cleaned datasets (flights, aircraft, airports) 


| ICAO Code | IATA Code | Airport Name                                      | City / Country         |
| **VIDP**  | DEL       | Indira Gandhi International Airport               | New Delhi, India       |
| **VOBL**  | BLR       | Kempegowda International Airport                  | Bengaluru, India       |
| **VOMM**  | MAA       | Chennai International Airport                     | Chennai, India         |
| **EHAM**  | AMS       | Amsterdam Airport Schiphol                        | Amsterdam, Netherlands |
| **VABB**  | BOM       | Chhatrapati Shivaji Maharaj International Airport | Mumbai, India          |
| **KLAX**  | LAX       | Los Angeles International Airport                 | Los Angeles, USA       |
| **KJFK**  | JFK       | John F. Kennedy International Airport             | New York City, USA     |
| **EGLL**  | LHR       | Heathrow Airport                                  | London, United Kingdom |
| **LFPG**  | CDG       | Charles de Gaulle Airport                         | Paris, France          |
| **RJTT**  | HND       | Haneda Airport (Tokyo International Airport)      | Tokyo, Japan           |


/sql – SQL scripts for queries and analysis

/reports – Generated outputs, summaries, and visualizations

README.md – Project documentation

----------------------------------------------------------------------------------------------------------

3. Getting Started
Clone the repository:

Code
git clone https://github.com/Binduja0910/Air-Tracker-Flight-Analytics
Import datasets into your SQL environment

Run queries from the /sql folder

Explore results in /reports

----------------------------------------------------------------------------------------------------------

4. Tech Stack
SQL (MySQL)

Streamlit (for visualization)

GitHub for version control

----------------------------------------------------------------------------------------------------------

5. Example Queries
Show the total number of flights for each aircraft model

List all aircraft (registration, model) with more than 5 flights

Find top 3 destination airports (name, city) by arrivals

----------------------------------------------------------------------------------------------------------
