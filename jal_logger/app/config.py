from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

POSTGRES_DB = os.getenv('POSTGRES_DB')

ODPT_ACCESS_TOKEN = os.getenv('ODPT_ACCESS_TOKEN')


arrival_column_drop_list = [
    '@type', 
    '@context', 
    'owl:sameAs', 
    'odpt:airline', 
    'odpt:operator', 
    'odpt:arrivalAirportTerminal', 
    'odpt:flightInformationText', 
    'odpt:flightInformationSummary'
]
departure_column_drop_list = [
    '@type', 
    '@context', 
    'owl:sameAs', 
    'odpt:airline', 
    'odpt:operator', 
    'odpt:departureGate', 
    'odpt:departureAirportTerminal', 
    'odpt:flightInformationText', 
    'odpt:flightInformationSummary'
]

arrival_column_rename_list = {
    "@id": "id",
    "dc:date": "date",
    "dct:valid": "valid",
    "odpt:flightNumber": "flight_number",
    "odpt:originAirport": "origin_airport",
    "odpt:arrivalAirport": "arrival_airport",
    "odpt:flightStatus": "flight_status",
    "odpt:scheduledArrivalTime": "scheduled_arrival_time",
    "odpt:estimatedArrivalTime": "estimated_arrival_time",
    "odpt:actualArrivalTime": "actual_arrival_time",
}
departure_column_rename_list = {
    "@id": "id",
    "dc:date": "date",
    "dct:valid": "valid",
    "odpt:flightNumber": "flight_number",
    "odpt:departureAirport": "departure_airport",
    "odpt:destinationAirport": "destination_airport",
    "odpt:flightStatus": "flight_status",
    "odpt:scheduledDepartureTime": "scheduled_departure_time",
    "odpt:estimatedDepartureTime": "estimated_departure_time",
    "odpt:actualDepartureTime": "actual_departure_time",
}
