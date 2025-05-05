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

# Session Names for Dataframes
AIRLINES = 'airlines'
AIRPLANES = 'airplanes'
AIRPORTS = 'airports'
CITIES = 'cities'
FLIGHTS = 'flights'
TOTAL_DISTANCE = 'total_distance'
TOTAL_PRICE = 'total_price'

TABLE_LIST = [AIRLINES, AIRPLANES, AIRPORTS, CITIES, FLIGHTS]
assert(len(CSV_LIST) == len(TABLE_LIST))

# Session Names for Filter data
LIST_CITIES = 'list_cities'
LIST_AIRLINES = 'list_airlines'
LIST_MODELS = 'list_models'
MAX_PRICE = 'max_price'
MIN_PRICE = 'min_price'
MAX_DEPARTURE_DATE = 'max_departure_date'
MIN_DEPARTURE_DATE = 'min_departure_date'

# Session Names for Filter Elements
CITY_SELECTED = 'city_selected'
AIRLINE_SELECTED = 'airline_selected'
MODEL_SELECTED = 'model_selected'
MAX_PRICE_SELECTED = 'max_price_selected'
DATE1_SELECTED = 'date1_selected'
DATE2_SELECTED = 'date2_selected'

# Session Names for ST elements
RADIO_AIRLINE_MODEL_KEY = 'radio_airline_model'
RADIO_AIRLINE_MODEL_OPTIONS = ['Aerolíneas', 'Modelos']
