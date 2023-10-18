import sys
import pyperclip
from config import Config
from table import TableBuilder
from loaders import EdgePipeline, ShadowHelper

if __name__ == '__main__':
    # Command line parameter to use filters when sorting matches.
    use_filters = False
    print_only = False
    if len(sys.argv) > 1:
        if '-use_filters' in sys.argv:
            use_filters = True
        if '-print_only' in sys.argv:
            print_only = True

    # Load the configuration file and initialize the configuration objects.
    config = Config()
    config.open_file()
    edge_config = config.build_edge_config()
    shadow_config = config.build_shadow_config()

    # Initialize the table builder and input the layout.
    table_builder = TableBuilder(config.get_table_layout())

    # Login and pull the runlist from Edge Pipeline.
    print('Please wait as sale data is being pulled.')
    edge_loader = EdgePipeline(edge_config)
    edge_loader.login()
    presale_data = edge_loader.get_vehicle_runlist()
    print(f"Scraped {len(presale_data)} vehicles from the run list. Please wait as units are found.")
    edge_loader.close()

    # Find matches of owned units from the runlist.
    shadow_loader = ShadowHelper(shadow_config)
    matches = shadow_loader.match_with_runlist(presale_data, use_filters=use_filters)

    if print_only is False:
        # Initialize table builder.
        table = table_builder.build_table(matches)

        # Copy results to clipboard.
        pyperclip.copy(table)
        print(f"{len(matches)} vehicles found in the run list and copied to the clipboard.")
        input("Press the enter key to exit.")
    else:
        # Initialize table builder.
        table = table_builder.build_generic(matches)

        # Print results to console.
        print(table)
        print(f"{len(matches)} vehicles found in the run list.")
        input("Press the enter key to exit.")
