import requests

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.SHEETY_URL_DELETE = None
        self.SHEETY_URL_PUT = None
        self.response = None
        self.parameters = None
        self.headers = None
        self.request = None
        self.data = None
        self.SHEETY_URL_GET = "https://api.sheety.co/6dedb0620313a6019e11e783ebb61dce/copiaDeFlightDeals/prices"
        self.SHEETY_BEARER = "xdxdxdxd"
        self.headers = {
            "Authorization": f"Bearer {self.SHEETY_BEARER}",
        }

    def obtain_complete_data(self):
        self.request = requests.get(url=self.SHEETY_URL_GET, headers=self.headers)
        self.request.raise_for_status()
        self.data = self.request.json()
        return self.data

    def edit_sheet(self, column, parameter_1, id_number):
        self.SHEETY_URL_PUT = f"{self.SHEETY_URL_GET}/{id_number}"
        self.parameters = {
            "price": {
                column: parameter_1,
            }
        }
        self.response = requests.put(url=self.SHEETY_URL_PUT, json=self.parameters, headers=self.headers)
        self.response.raise_for_status()

    def delete_row(self, id_number):
        self.SHEETY_URL_DELETE = f"{self.SHEETY_URL_GET}/{id_number}"
        self.response = requests.delete(url=self.SHEETY_URL_DELETE, headers=self.headers)
        self.response.raise_for_status()

    def obtain_row_data(self, id):
        self.request = requests.get(url=f"{self.SHEETY_URL_GET}/{id}", headers=self.headers)
        self.request.raise_for_status()
        self.data = self.request.json()
        return self.data





