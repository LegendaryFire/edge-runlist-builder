class Vehicle:
    def __init__(self, json=None):
        self._run_number = None
        self._year = None
        self._make = None
        self._model = None
        self._trim = None
        self._vin = None
        self._sale_price = None
        self._seller = None

        if json:
            self._year = json['vehicle_info']['year']
            self._make = json['vehicle_info']['make']
            self._model = json['vehicle_info']['model']
            self._trim = json['vehicle_info']['trim']
            self._vin = json['vehicle_info']['vin']
            self._sale_price = json['vehicle_sales']['price']

            # If no seller was specified, it was a private seller.
            if not json['vehicle_seller']['firstname'] and not json['vehicle_seller']['lastname']:
                self._seller = "Private Seller"
            else:
                self._seller = f"{json['vehicle_seller']['firstname']} {json['vehicle_seller']['lastname']}"

    def get_run_number(self) -> str:
        """
        Gets the vehicle run-number.
        :return: Returns the run number.
        """
        return self._run_number

    def set_run_number(self, run_number) -> None:
        """
        Sets the vehicle run number.
        :param run_number: The run number as a string.
        :return: Returns None.
        """
        self._run_number = run_number

    def get_year(self) -> str:
        """
        Gets the vehicle year.
        :return: Returns the vehicle year.
        """
        return self._year

    def set_year(self, year) -> None:
        """
        Sets the vehicle year.
        :param year: The vehicle year as a string.
        :return: Returns None.
        """
        self._year = year

    def get_make(self) -> str:
        """
        Gets the vehicle make.
        :return: Returns the vehicle make.
        """
        return self._make

    def set_make(self, make) -> None:
        """
        Sets the vehicle make.
        :param make: The vehicle make as a string.
        :return: Returns None.
        """
        self._make = make

    def get_model(self) -> str:
        """
        Gets the vehicle model.
        :return: Returns the vehicle model.
        """
        return self._model

    def set_model(self, model) -> None:
        """
        Sets the vehicle model.
        :param model: The vehicle model as a string.
        :return: Returns None.
        """
        self._model = model

    def get_trim(self) -> str:
        """
        Gets the vehicle trim.
        :return: The vehicle trim.
        """
        return self._trim

    def set_trim(self, trim) -> None:
        """
        Sets the vehicle trim.
        :param trim: The vehicle trim as a string.
        :return: Returns None.
        """
        self._trim = trim

    def get_vin(self) -> str:
        """
        Gets the vehicle VIN.
        :return: Returns the vehicle VIN as a string.
        """
        return self._vin

    def set_vin(self, vin) -> None:
        """
        Sets the vehicle VIN.
        :param vin: The vehicle VIN as a string.
        :return: Returns None.
        """
        self._vin = vin

    def get_sale_price(self) -> str:
        """
        Gets the sale price of the vehicle.
        :return: Returns the sale price.
        """
        return self._sale_price

    def set_sale_price(self, sale_price) -> None:
        """
        Sets the sale price of the vehicle.
        :param sale_price: The sale price as a string.
        :return: Returns None.
        """
        self._sale_price = sale_price

    def get_seller(self) -> str:
        """
        Gets the previous owner/seller of the vehicle.
        :return: Returns the seller.
        """
        return self._seller

    def set_seller(self, seller) -> None:
        """
        Sets the previous owner/seller of the vehicle.
        :param seller: The seller as a string.
        :return: Returns None.
        """
        self._seller = seller

    def fill_empty(self, vehicle) -> None:
        """
        Takes a vehicle object and fills remaining empty properties with the data.
        :param vehicle: The vehicle object.
        :return: Returns None.
        """
        if not self._run_number:
            self._run_number = vehicle.get_run_number()
        if not self._year:
            self._year = vehicle.get_year()
        if not self._make:
            self._make = vehicle.get_make()
        if not self._model:
            self._model = vehicle.get_model()
        if not self._trim:
            self._trim = vehicle.get_trim()
        if not self._vin:
            self._vin = vehicle.get_vin()
        if not self._sale_price:
            self._sale_price = vehicle.get_sale_price()
        if not self._seller:
            self._seller = vehicle.get_seller()