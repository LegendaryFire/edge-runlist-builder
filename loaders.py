import os
import time
import csv
import requests
import re
from vehicle import Vehicle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class EdgePipeline:
    def __init__(self, config) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})
        self._driver = webdriver.Chrome(options=options)
        self.__config = config

    def login(self) -> bool:
        """
        Logs into Edge Pipeline.
        :return: Returns True if logged in successfully.
        """
        credentials = self.__config.get_credentials()

        self._driver.get("https://www.edgepipeline.com/components/login")
        # Wait for Edge Pipeline login page to load.
        try:
            wait = WebDriverWait(self._driver, 5).until(
                EC.presence_of_element_located((By.ID, "username"))
            )

            self._driver.find_element(By.ID, "username").send_keys(credentials.get_username())
            self._driver.find_element(By.ID, "password").send_keys(credentials.get_password())
            self._driver.find_element(By.NAME, "button_action").click()

            wait = WebDriverWait(self._driver, 5).until(
                EC.title_contains("Dashboard")
            )
        except TimeoutException:
            print("Unable to log into Edge. Please try again.")
            return False

        return True

    def get_vehicle_runlist(self) -> list[Vehicle]:
        """
        Downloads the presale data for DAA Northwest.
        :return: Returns a list of Vehicles with the run-number and VIN.
        """
        url = f"https://www.edgepipeline.com/components/report/presale/csv/" \
              f"{self.__config.get_auction()}?consignor={self.__config.get_consignor()}"
        self._driver.get(url)
        # Wait for download to be completed.
        filepath = os.path.join(os.getcwd(), f"edgepipeline_presale_{self.__config.get_auction()}.csv")
        timer, timeout = 0, 10000  # Measured in milliseconds.
        while True:
            if os.path.exists(filepath):
                break
            elif timer > timeout:
                raise TimeoutError("Pre-sale data download timed out.")
            time.sleep(0.25)
            timer += 250

        vehicle_runlist = []
        with open(f'edgepipeline_presale_{self.__config.get_auction()}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                vehicle = Vehicle()
                vehicle.set_run_number(row[1])
                vehicle.set_vin(row[14])
                vehicle_runlist.append(vehicle)

        os.remove(filepath)  # Delete the downloaded CSV once we're done with it.
        # First row is the headers, we don't include those.
        return vehicle_runlist[1:]

    def close(self):
        self._driver.close()


class ShadowHelper:
    def __init__(self, config):
        self.__config = config

    def match_with_runlist(self, runlist, use_filters=True) -> list:
        """
        Checks vehicle in the presale runlist with the point of sales to see which ones are owned by the Shadow Helper user.
        :param runlist: The vehicle runlist from Edge Pipeline.
        :param use_filters: Apply the filters specified in the configuration file. Default is True.
        :return: Returns a list of vehicles that match the conditions in the configuration.
        """
        session = requests.Session()
        results = []

        for edge_vehicle in runlist:
            resp = session.get(self.__build_vehicle_url(edge_vehicle.get_vin(), self.__config.get_credentials()))
            # Check to see if we have a vehicle match.
            vehicle_data = resp.json()
            if 'error' not in vehicle_data:
                shadow_vehicle = Vehicle(json=vehicle_data)
                # Does this vehicle match our conditions specified in the Shadow Helper configuration?
                conditions_met = True
                if self.__config.get_first_name_regex():
                    if not re.match(self.__config.get_first_name_regex(), vehicle_data['vehicle_purchaser']['firstname']):
                        conditions_met = False
                if self.__config.get_last_name_regex():
                    if not re.match(self.__config.get_last_name_regex(), vehicle_data['vehicle_purchaser']['lastname']):
                        conditions_met = False

                if use_filters:
                    if conditions_met:
                        edge_vehicle.fill_empty(shadow_vehicle)
                        results.append(edge_vehicle)
                else:
                    edge_vehicle.fill_empty(shadow_vehicle)
                    results.append(edge_vehicle)
        return results

    @staticmethod
    def __build_vehicle_url(vin, credentials) -> str:
        """
        Helper method to build the URL to pull vehicle data from Shadow Helper.
        :param vin: The VIN of the vehicle.
        :param credentials: The Credentials object for Shadow Helper.
        :return:
        """
        url = f"https://shadowhelper.com/watcher/api.php?vin={vin}" \
              f"&user={credentials.get_username()}" \
              f"&pass={credentials.get_password()}"
        return url

