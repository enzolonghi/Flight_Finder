from twilio.rest import Client
import smtplib
import requests
# This class is responsible for sending the notifications via mail and message
class NotificationManager:
    def __init__(self):
        self.message = None
        self.client = None
        self.MY_EMAIL = "enzolonghi.03.03@gmail.com"
        self.MY_PASSWORD = "moqt dmti ezsl uhwy"
        self.ACCOUNT_SID = "AC499e4fe0384f6a4a2190106cc535d69b"
        self.AUTH_TOKEN = "8eacaf6045865fb1cd89af6da3a34d39"
        self.GOOGLE_FLIGHTS_URL = "https://www.google.com/flights/?hl=es_419"
        self.SHEETY_URL_GET = "https://api.sheety.co/6dedb0620313a6019e11e783ebb61dce/copiaDeFlightDeals/users/"
        self.SHEETY_BEARER = "xdxdxdxd"
        self.headers = {
            "Authorization": f"Bearer {self.SHEETY_BEARER}",
        }

    def send_message(self, price, city, date, stops):
        self.client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)
        self.message = self.client.messages \
            .create(
            body=f"Low price alert! only $EUR {price} to fly from Buenos Aires-EZE to {city}, from: {date}\n"
                 f"Number of stops: {stops}",
            from_='+15732848975',
            to='+542215908578'
        )
        print(self.message.status)

    def send_emails(self, price, city, date, stops, iata):
        response = requests.get(url=self.SHEETY_URL_GET, headers=self.headers)
        data = response.json()
        email_list = [user["email"] for user in data["users"]]
        for email in email_list:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=self.MY_EMAIL, password=self.MY_PASSWORD)
                connection.sendmail(from_addr=self.MY_EMAIL,
                                    to_addrs=email,
                                    msg=f"Subject:New flight price!\n\n"
                                        f"Low price alert!"
                                        f" only $EUR {price} to fly from Buenos Aires-EZE to {city}-{iata},"
                                        f" from: {date}\nNumber of stops: {stops}\n"
                                        f"Use Google Flights to buy a ticket\n{self.GOOGLE_FLIGHTS_URL}")
