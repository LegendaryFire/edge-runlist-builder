class Vehicle:
    def __init__(self, run_number, json):
        self._json = json
        self._run_number = run_number

    def get_run_number(self):
        return self._run_number

    def get_year(self):
        return self._json['vehicle_info']['year']

    def get_make(self):
        return self._json['vehicle_info']['make']

    def get_model(self):
        return self._json['vehicle_info']['model']

    def get_trim(self):
        return self._json['vehicle_info']['trim']

    def get_vin(self):
        return self._json['vehicle_info']['vin']

    def get_sold_price(self):
        return self._json['vehicle_sales']['price']

    def get_seller(self):
        if self._json['vehicle_seller']['lastname'] != "":
            seller = self._json['vehicle_seller']['firstname']
            if seller is None:
                return "Private Seller"
            return seller
        else:
            seller = self._json['vehicle_seller']['firstname'] + self._json['vehicle_seller']['lastname']
            return seller
