""" 
CountryDataFetcher.py 
Python script to fetch and analyze country data from the REST Countries API. 

"""

import requests

class CountryDataFetcher:

    def __init__(self, url):
        self.url = url

    # Fetch Status code
    def api_status_code(self):
        response = requests.get(self.url)
        return response.status_code

    # Fetch the REST API server Headers
    def fetch_headers(self):
        if self.api_status_code() == 200:
            response = requests.get(self.url)
            return response.headers
        else:
            return 404

    # GET method - Fetch data from API server
    def fetch_api_data(self):
        if self.api_status_code() == 200:
            response = requests.get(self.url)
            return response.json()
        else:
            return None

    # Display names of countries, currencies, and currency symbols
    def display_countries_currencies(self, data):
        if data:
            for country in data:
                name = country.get('name', {}).get('common', 'Unknown')
                currencies = country.get('currencies', {})
                for currency_code, currency_info in currencies.items():
                    currency_name = currency_info.get('name', 'Unknown')
                    currency_symbol = currency_info.get('symbol', 'Unknown')
                    print(f"Country: {name}, Currency: {currency_name}, Symbol: {currency_symbol}")
        else:
            print("No data to display.")

    # Display names of countries that use the specified currency
    def display_countries_with_currency(self, data, currency_name):
        if data:
            for country in data:
                currencies = country.get('currencies', {})
                for currency_code, currency_info in currencies.items():
                    if currency_name.lower() in currency_info.get('name', '').lower():
                        print(country.get('name', {}).get('common', 'Unknown'))
        else:
            print("No data to display.")
    
    # Display names of countries that use Dollar as currency
    def display_countries_with_dollar(self, data):
        print("\nCountries using Dollar:")
        self.display_countries_with_currency(data, 'Dollar')

    # Display names of countries that use Euro as currency
    def display_countries_with_euro(self, data):
        print("\nCountries using Euro:")
        self.display_countries_with_currency(data, 'Euro')

if __name__ == "__main__":
    url = "https://restcountries.com/v3.1/all"

    fetcher = CountryDataFetcher(url)
    data = fetcher.fetch_api_data()

    # Print the API status code
    print("Status Code : ", fetcher.api_status_code())

    if data:
        # Indicate successful data fetch
        print("Data fetched successfully!")
        # Display countries and their currencies
        fetcher.display_countries_currencies(data)
        # Display countries that use Dollar as currency
        fetcher.display_countries_with_dollar(data)
        # Display countries that use Euro as currency
        fetcher.display_countries_with_euro(data)
    else:
        print("Failed to fetch data.")
