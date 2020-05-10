# REAL TIME STOCK DATA EXPORT TO EXCEL

![Logo of the project](https://images.pexels.com/photos/241544/pexels-photo-241544.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940)

### PROJECT INTENTION
This .py script allows to export real-time stock market data from various indices without relying on API keys or additional software. We make use of the Python library Selenium. Our webscraper accesses the german stock market website boerse-online and extracts the data by leveraging the strengths of the additional libraries bs4 and pandas.

***

🛑🛑🛑 **LOGIC OF SCRIPT** 🛑🛑🛑

1.) Definition of url list

2.) Looping over url list

3.) Removing cookie banner obstacle

4.) Extracting html source code of opened url

5.) Identifying column values by using html tags _tr_ and _td_ 

6.) Appending respective values to output lists

7.) Turning output lists into df

8.) Writing dataframe to output excel sheet

9.) Closing browser and - if condition is met - go back to step 2.) 

***

### SAMPLE OUTPUT

After executing the script, the output excel can be found in the respective project directory. See a sample output below.

![Logo of the project](https://github.com/JiGro/Realtime_stock_data_to_excel/blob/master/Sample_Output.png?raw=true)


***

### FURTHER EXTENSION

A possible extension / adapted version of this script would be to safe the respective stock data in a database. In a next step, the accessible historical data could be used to conduct time-series analysis as well as statistical analysis.
