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

    def get_vehicle_runlist(self) -> list:
        """
        Downloads the presale data for DAA Northwest.
        :return: Returns the filepath for the downloaded CSV presale data. Returns False if failed or timed out.
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
                print("Unable to download presale data. Please try again.")
                raise TimeoutError("Presale data download timed out.")
            time.sleep(0.25)
            timer += 250

        presale_data = []
        with open(f'edgepipeline_presale_{self.__config.get_auction()}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                presale_data.append({
                    "Run Number": row[1],
                    "VIN": row[14],
                    "Grade": row[11],
                })

        os.remove(filepath)  # Delete the downloaded CSV once we're done with it.

        return presale_data[1:]

    def close(self):
        self._driver.close()


class ShadowHelper:
    def __init__(self, config):
        self.__config = config

    def match_with_runlist(self, runlist, filter_matches=True) -> list:
        session = requests.Session()
        results = []

        for vehicle in runlist:
            resp = session.get(self.__build_vehicle_url(vehicle['VIN'], self.__config.get_credentials()))
            # Check to see if we have a vehicle match.
            vehicle_data = resp.json()
            if 'error' not in vehicle_data:
                # Does this vehicle match our conditions specified in the Shadow Helper configuration?
                conditions_met = True
                if self.__config.get_first_name_regex():
                    if not re.match(self.__config.get_first_name_regex(), vehicle_data['vehicle_purchaser']['firstname']):
                        conditions_met = False
                if self.__config.get_last_name_regex():
                    if not re.match(self.__config.get_last_name_regex(), vehicle_data['vehicle_purchaser']['lastname']):
                        conditions_met = False

                if filter_matches:
                    if conditions_met:
                        results.append(Vehicle(vehicle['Run Number'], resp.json()))
                else:
                    results.append(Vehicle(vehicle['Run Number'], resp.json()))
        return results

    @staticmethod
    def __build_vehicle_url(vin, credentials) -> str:
        url = f"https://shadowhelper.com/watcher/api.php?vin={vin}" \
              f"&user={credentials.get_username()}" \
              f"&pass={credentials.get_password()}"
        return url

