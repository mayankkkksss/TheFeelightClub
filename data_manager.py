import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

SHEETY_PRICES_ENDPOINT = os.environ['SHEETY_PRICES_ENDPOINT']
SHEETY_USERS_ENDPOINT = os.environ['SHEETY_USERS_ENDPOINT']

class DataManager:
    """DataManager class manages all the data related part from SerpAPI's Google Flight API.
    Contains function to fetch updated data, update the lowest price"""
    def __init__(self):
        self._user = os.environ['SHEETY_USERNAME']
        self._password = os.environ['SHEETY_PASSWORD']
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        """This function used to fetch Google Sheet's sheet using Sheety's API to return data as dictionary"""
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data

    def update_lowest_price(self, row_id, new_price):
        """This function takes row_id & new_price as parameters to update the lowest price in Google Sheets by using Sheety's API"""
        parameters = {
            "price": {
                "lowestPrice": new_price
            }
        }

        requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{str(row_id)}", json=parameters, auth=self._authorization)

    def get_customers_emails(self):
        """This function returns user's spreadsheet data in Google Sheets by using Sheety API's"""
        response = requests.get(url=SHEETY_USERS_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.customer_data = data['users']
        return self.customer_data