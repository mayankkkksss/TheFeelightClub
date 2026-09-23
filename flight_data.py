class FlightData:
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

def find_cheapest_flight(data, return_date):
    """This function takes dictionary API response from SerpAPI's Google Flight API to find the cheapest flight amongst the API's
    response and returns cheapest flight as dictionary"""
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data")
        return FlightData("N/A", "N/A","N/A", "N/A", "N/A", "N/A")


    flights_list = data.get("best_flights", []) + data.get("other_flights")

    first_flight = flights_list[0]
    lowest_price = first_flight["price"]
    origin = first_flight["flights"][0]["departure_airport"]["id"]
    destination = first_flight["flights"][-1]["arrival_airport"]["id"]
    out_date = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
    stops = len(first_flight["flights"]) - 1

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

    for flight in flights_list:
        try:
            price = flight["price"]
        except KeyError:
            print("--- No price available for flight. ---")
        else:
            if price < lowest_price:
                lowest_price = price
                origin = flight["flights"][0]["departure_airport"]["id"]
                destination = flight["flights"][-1]["arrival_airport"]["id"]
                out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
                stops = len(flight["flights"]) - 1
                cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, stops)

    return cheapest_flight
