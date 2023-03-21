#This file will need to use the DataManager,FlightSearch, NotificationManager classes to achieve the program requirements.
import requests
from data_manager import DataManager
from amadeus import Client
from flight_search import FlightSearch
from datetime import date
from datetime import timedelta
from notification_manager import NotificationManager


#Ask the user to add a new user
def add_new_user():
    SHEETY_URL = "https://api.sheety.co/6dedb0620313a6019e11e783ebb61dce/copiaDeFlightDeals/users"
    SHEETY_BEARER = "xdxdxdxd"
    print("Welcome to Enzo's Flight Club")
    first_name = input("What is your first name?: ")
    last_name = input("What is your last name?: ")
    email_check = True
    parameters = {}
    while email_check:
        first_email = input("What is your email?: ")
        second_email = input("Type yor email again please: ")
        if first_email == second_email:
            parameters = {
                "user": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": first_email,
                }
            }
            print("You are in the club!")
            email_check = False
        else:
            print("The emails aren't equal. Please try again")
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SHEETY_BEARER}"
    }
    post_request = requests.post(url=SHEETY_URL, json=parameters, headers=header)
    post_request.raise_for_status()

ask_to_add_new_user = input("Welcome to Enzo's Flight Club\nWould you like to add a new user? ").lower()
if ask_to_add_new_user == "yes":
    add_new_user()
else:
    pass

#Asign IATA code to each airport
data_manager = DataManager()
amadeus = Client(client_id='kEQkuuMv3qPs5JRALaLlSHLqPIgSQewo', client_secret='Iuf37kUuwA0bOgs5')
google_sheet_data = data_manager.obtain_complete_data()
cities = [city["city"] for city in google_sheet_data["prices"]]
cities_to_remove = {}

#Asign iata to each airport. If the city dos not have data, save it in a dictionary to delete it later
def asign_iata_to_sheet(cities_list):
    for city in cities_list:
        response = amadeus.get("/v1/reference-data/locations", subType=["CITY"], keyword=city)
        if not response.data:
            city_id_number = cities.index(city, 0, len(cities)) + 2
            cities_to_remove[city] = city_id_number
        else:
            iata_to_add = response.data[0]["iataCode"]
            city_id_number = cities.index(city, 0, len(cities)) + 2
            data_manager.edit_sheet(column="iataCode", parameter_1=iata_to_add, id_number=city_id_number)

asign_iata_to_sheet(cities_list=cities)

#Delete all the cities that not have data
def delete_cities(cities_list):
    for city in reversed(cities_list):
        data_manager.delete_row(id_number=cities_to_remove[city])

delete_cities(cities_list=cities_to_remove)

#Obtain the updated data from the Google sheet
google_sheet_data = data_manager.obtain_complete_data()

#Search flight price for the next 60 days

flight_searcher = FlightSearch()
cities_to_flight = [city["iataCode"] for city in google_sheet_data["prices"]]
cities_to_change = {}
def find_cheapest_flight(cities_to_search):
    for city in cities_to_search:
        id_number = cities_to_search.index(city) + 2
        row_data = data_manager.obtain_row_data(id=id_number)
        current_flight_price = row_data["price"]["lowestPrice"]
        for i in range(1, 60):
            flight_date = str(date.today() + timedelta(days=i))
            flight_price = float(flight_searcher.flight_price(destination_iata=city, date=flight_date))
            if flight_price < current_flight_price:
                current_flight_price = flight_price
                cheapest_flight_date = flight_date
                current_city_data = {"new_price": current_flight_price, f"id": id_number, "iataCode": city,
                                     "date": cheapest_flight_date}
                city_index_number = cities_to_search.index(city)
                cities_to_change[cities[city_index_number]] = current_city_data
            else:
                pass
    return cities_to_change

cities_to_actualize = find_cheapest_flight(cities_to_flight)

#Actualize the sheet and send message if the lowest price changed
notification_manager = NotificationManager()

#If there's no cities with a cheap flight just pass
def send_change_email(change_list):
    if not change_list:
        pass
    else:
        cities_to_change_price = change_list.items()
        for (key, value) in cities_to_change_price:
            city = key
            new_price = value["new_price"]
            city_id = value["id"]
            flight_date = value["date"]
            stops = flight_searcher.flight_stops()
            arrival_airport_iata = flight_searcher.arrival_airport()
            notification_manager.send_emails(price=new_price, city=city, date=flight_date, stops=stops,
                                             iata=arrival_airport_iata)
            #Edit the row with the new price
            data_manager.edit_sheet(column="lowestPrice", parameter_1=new_price, id_number=city_id)
        send_change_email(change_list=cities_to_actualize)
