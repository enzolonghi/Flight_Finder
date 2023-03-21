from amadeus import Client
# This class is responsible for talk to the flights data API
class FlightSearch:
    def __init__(self):
        self.arrival_airport_iata = None
        self.stops_number = None
        self.amadeus = None
        self.response = None
        self.MY_CITY_IATA = "EZE"

    def flight_price(self, destination_iata, date):
        self.amadeus = Client(
            client_id='kEQkuuMv3qPs5JRALaLlSHLqPIgSQewo',
            client_secret='Iuf37kUuwA0bOgs5'
        )
        self.response = self.amadeus.shopping.flight_offers_search.get(
            originLocationCode=self.MY_CITY_IATA,
            destinationLocationCode=destination_iata,
            departureDate=date,
            adults=1)
        self.stops_number = len(self.response.data[0]["itineraries"][0]["segments"])
        self.arrival_airport_iata = self.response.data[0]["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        return self.response.data[0]["price"]["total"]

    def flight_stops(self):
        return str(self.stops_number)

    def arrival_airport(self):
        return self.arrival_airport_iata
