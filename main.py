import os

import requests_cache
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

#===================== Used to preserve API response to reduce usage =====================
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)

#===================== Dates =====================
today = datetime.now().date()
tomorrow = today + timedelta(days=1)
six_month_from_today = today + timedelta(days=6 * 30)


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
customer_data = data_manager.get_customers_emails()
flight_search = FlightSearch()
notification_manager = NotificationManager()

#================== Search for direct flights =====================
ORIGIN_CITY_IATA = "BOM" #Change this to your preferred airport's IATA code.
CURRENCY_SYMBOL = os.environ['CURRENCY_SYMBOL']

for destination in sheet_data:
    # Search Flight
    print(f"Getting flights for {destination['city']}...")
    direct_flights = flight_search.check_flights(origin_city_code=ORIGIN_CITY_IATA,
                                                 destination_city_code=destination["iataCode"],
                                                 from_time=tomorrow,
                                                 to_time=six_month_from_today)

    cheapest_flight = find_cheapest_flight(direct_flights, six_month_from_today)
    print(f"Cheapest direct flight to {destination['city']}: {CURRENCY_SYMBOL} {cheapest_flight.price}")

    # ===================== Search for indirect flights if price = 'N/A' =====================
    if cheapest_flight.price == 'N/A':
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        indirect_flights = flight_search.check_flights(origin_city_code=ORIGIN_CITY_IATA,
                                                     destination_city_code=destination["iataCode"],
                                                     from_time=tomorrow,
                                                     to_time=six_month_from_today,
                                                     is_direct=False)
        cheapest_flight = find_cheapest_flight(indirect_flights, six_month_from_today)
        print(f"Cheapest indirect flight to {destination['city']}: {CURRENCY_SYMBOL} {cheapest_flight.price}")

    #===================== Send notifications/alerts via email/SMS/whatsapp =====================

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        #Updating lowest price
        print(f"Lower price flight found to {destination["city"]}")
        data_manager.update_lowest_price(destination["id"], cheapest_flight.price)

        customer_emails = [email['whatIsYourEmail?'] for email in customer_data]

        global message

        #Sending emails via SMTP protocol
        if cheapest_flight.stops >= 1:
            message = f"Low price alert! Only {CURRENCY_SYMBOL} {cheapest_flight.price} to fly "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"with {cheapest_flight.stops} stop(s) "\
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        else:
            message = f"Low price alert! Only {CURRENCY_SYMBOL} {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."


        print(f"Check your email. Lower price flight found to {destination['city']}!")

        #Sending Message via SMTP protocol
        notification_manager.send_email(email_list=customer_emails, message_body=message)

        notification_manager = NotificationManager()

        #Sending message via SMS
        print("Check your SMS")
        notification_manager.send_sms(message)

        # #Sending message via WhatsApp
        print("Check your WhatsApp")
        notification_manager.send_whatsapp(message)