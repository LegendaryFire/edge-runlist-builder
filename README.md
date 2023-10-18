# Edge Runlist Builder
Edge Runlist Builder is small personal project of mine to automate building vehicle runlists for Edge Pipeline auction sales. This tool uses Selenium to pull presale auction data to match with owned units on the point of sales for easy calculation of breakeven costs, reserve/line prices, source of purchasing and more. This tool copies the table it generates into the clipboard, so it can be easily entered in Microsoft Teams or an Excel document. 

### Requirements
* Python 3.10 and higher
* WebDriver for Google Chrome (version 114 and lower)

### Configuration
The configuration file is located in config.yml, an example configuration can be found below.
```
edge:
  username: email@example.com
  password: password
shadow:
  username: username
  password: password
settings:
  edge:
    auction: auction-code
    consignor: consignor-name
regex:
  shadow:
    purchaser:
      first_name: 'optional'
      last_name: 'optional'
table:
  layout:
    col1: run_number
    col2: description
    col3: vin
    col4: sold_price
    col6: 'sale notes'
    col11: seller_name
```

Regular expressions can be used for filtering vehicles in the presale data.

The table layout is configured as follows. Any columns without the variable names below can be used to input Excel functions or basic text. Any unused columns are assumed blank.

|    Variable   |     Output    |
| ------------- | ------------- |
| run_number | Auction run number |
| description | Year, make, model and trim |
| vin | Last 6 of the VIN |
| sold_price | Breakeven cost in CDN dollars |
| seller_name | Source of vehicle |

To run the script call ```python main.py -use_filters``` to use the regex filters specified in the configuration, or ```python main.py``` to use without regex filters. This script can also be ran without copying a table to the clipboard, but printing a generic table to the console instead by using the ```-print_only``` flag.
