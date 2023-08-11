import yaml
import hashlib


class Credentials:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password


class Config:
    """
    The Config class contains all the configuration variables required for Edge Pipeline and Shadow Helper.
    """
    def __init__(self):
        self.__config = None

    def open_file(self, path="./config.yml") -> None:
        """
        Loads the configuration from file.
        :param path: The path to open the file from, default is ./config.yml.
        :return: Returns none.
        """
        with open(path, 'r') as config:
            self.__config = yaml.safe_load(config)

    def open_json(self, config) -> None:
        """
        Loads the configuration from JSON.
        :return: Returns none.
        """
        self.__config = config

    def get_table_layout(self) -> dict:
        """
        Gets the table layout.
        :return: Returns the table layout as a dictionary.
        """
        return self.__config['table']['layout']

    class ShadowConfig:
        """
        The configuration for Shadow Helper, created by a factory method.
        """
        def __init__(self, config):
            self.__config = config

        def get_credentials(self) -> Credentials:
            """
            Gets the credentials for ShadowHelper. Password is returned as a SHA256 hash.
            :return: Returns a Credentials object.
            """
            password = self.__config['shadow']['password'].encode('utf-8')
            password = hashlib.sha256(password).hexdigest()
            return Credentials(self.__config['shadow']['username'], password)

        def get_first_name_regex(self) -> str or None:
            """
            Gets the first name regex filter if provided in the configuration.
            :return: Returns the regex, or None.
            """
            try:
                return self.__config['regex']['shadow']['purchaser']['first_name']
            except KeyError:
                return None

        def get_last_name_regex(self) -> str or None:
            """
            Gets the last name regex filter if provided in the configuration.
            :return: Returns the regex, or None.
            """
            try:
                return self.__config['regex']['shadow']['purchaser']['last_name']
            except KeyError:
                return None

    class EdgeConfig:
        """
        The configuration for Edge Pipeline, created by a factory method.
        """
        def __init__(self, config):
            self.__config = config

        def get_credentials(self) -> Credentials:
            """
            Gets the credentials for Edge Pipeline.
            :return: Returns a Credentials object.
            """
            return Credentials(self.__config['edge']['username'], self.__config['edge']['password'])

        def get_auction(self) -> str:
            """
            Gets the auction to view on Edge Pipeline.
            :return:
            """
            return self.__config['settings']['edge']['auction']

        def get_consignor(self) -> str:
            """
            Gets the consignor to view on Edge Pipeline.
            :return:
            """
            return self.__config['settings']['edge']['consignor']

    def build_shadow_config(self) -> ShadowConfig:
        """
        Builds the configuration for the ShadowHelper class. This is a factory method.
        :return: Returns a ShadowConfig object.
        """
        return self.ShadowConfig(self.__config)

    def build_edge_config(self) -> EdgeConfig:
        """
        Builds the configuration for the EdgePipeline class. This is a factory method.
        :return: Returns a EdgeConfig object.
        """
        return self.EdgeConfig(self.__config)

