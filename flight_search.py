import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_ENDPOINT = "https://serpapi.com/search"

class FlightSearch:
    """This FLightSearch class contains method to search flights with required parameters"""
    def __init__(self):
        self._api_key = os.environ["SERPAPI_API_KEY"]
        self.currency_code = os.environ['CURRENCY_CODE']

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """This function takes origin airport, destination IATA code, outbound date & inbound date as a parameter
            to search for available flights using SerpAPI's Google Flights API and returns API response as dictionary"""

        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time,
            "return_date": to_time,
            "type": 1,
            "adults": 1,
            "currency": self.currency_code,
            "api_key": self._api_key,
        }

        if is_direct:
            query["stops"] = 1

        response = requests.get(url=SERPAPI_ENDPOINT, params=query)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            return None

        data = response.json()

        if "error" in data:
            print(f"API error: {data['error']}")
            return None
        return data
