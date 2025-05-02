# General Paths
LOG_PATH = './log_app.log'
TOP_IMAGE = './resources/nttairAlargado.png'
BASE_CSV_PATH = 'G:/datasets/flight_prices_dataset/' # Modify it to locate the dataset folder path

# CSV Paths
AIRLINES_CSV = BASE_CSV_PATH + 'airlanes/extracted_airlanes.csv'
AIRPLANES_CSV = BASE_CSV_PATH + 'airplanes/extracted_airplanes_complete.csv'
AIRPORTS_CSV = BASE_CSV_PATH + 'airports/extracted_airports_complete.csv'
CITIES_CSV = BASE_CSV_PATH + 'cities/formatted_cities.csv'
FLIGHTS_CSV = BASE_CSV_PATH + 'itineraries/itineraries_splitted_formatted.csv'

CSV_LIST = [AIRLINES_CSV, AIRPLANES_CSV, AIRPORTS_CSV, CITIES_CSV, FLIGHTS_CSV]

# Session Names
AIRLINES = 'airlines'
AIRPLANES = 'airplanes'
AIRPORTS = 'airports'
CITIES = 'cities'
FLIGHTS = 'flights'
TOTAL_DISTANCE = 'total_distance'
TOTAL_PRICE = 'total_price'

TABLE_LIST = [AIRLINES, AIRPLANES, AIRPORTS, CITIES, FLIGHTS]
assert(len(CSV_LIST) == len(TABLE_LIST))
