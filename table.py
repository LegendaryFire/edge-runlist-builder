class TableBuilder:
    def __init__(self, layout):
        self.__layout = layout
        self.__columns = [int(s.strip('col')) for s in list(layout.keys())]

    def build_table(self, vehicle_list) -> str:
        """
        Builds a table from the vehicle data provided and the table layout in the configuration file.
        :param vehicle_list: A list of vehicles pulled from Shadow Helper.
        :return: Returns the table as a string.
        """
        table = ''
        for vehicle in vehicle_list:
            for i in range(1, max(self.__columns) + 1):
                if i in self.__columns:
                    match self.__layout[f'col{i}']:
                        case 'run_number':
                            table += f'{vehicle.get_run_number()}'
                        case 'description':
                            table += f'{vehicle.get_year()} {vehicle.get_make()} {vehicle.get_model()} {vehicle.get_trim()}'
                        case 'vin':
                            table += f"'{vehicle.get_vin()[-6:]}"
                        case 'sold_price':
                            table += f'{vehicle.get_sale_price()}'
                        case 'seller_name':
                            table += f'{vehicle.get_seller()}'
                        case _:
                            table += f"{self.__layout[f'col{i}']}"
                    # Only add new column if we are not at the last column in the row.
                    if i != max(self.__columns):
                        table += '\t'
                else:
                    # Column not specified, skip column.
                    table += '\t'
            table += '\n'
        return table
