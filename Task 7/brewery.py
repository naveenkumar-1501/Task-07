"""
brewery.py

Python script to fetch and analyze brewery data from Open Brewery DB API.
"""

import requests

class BreweryData:
    def __init__(self):
        self.base_url = "https://api.openbrewerydb.org/breweries"
        self.states = ['Alaska', 'Maine', 'New York']

    # Fetch all breweries for a given state, handle pagination
    def fetch_breweries_by_state(self, state):
        page = 1
        breweries = []
        while True:
            response = requests.get(f"{self.base_url}?by_state={state}&per_page=50&page={page}")
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            breweries.extend(data)
            page += 1
        return breweries

    # List names of all breweries in the specified states
    def list_breweries(self):
        breweries = {state: self.fetch_breweries_by_state(state) for state in self.states}
        for state, data in breweries.items():
            print(f"\nBreweries in {state}:")
            for brewery in data:
                print(brewery.get('name', 'Unknown'))

    # Count the number of breweries in each specified state
    def count_breweries_in_states(self):
        for state in self.states:
            breweries = self.fetch_breweries_by_state(state)
            print(f"\nNumber of breweries in {state}: {len(breweries)}")

    # Count the types of breweries in individual cities of the specified states
    def count_brewery_types_by_city(self):
        for state in self.states:
            breweries = self.fetch_breweries_by_state(state)
            city_brewery_types = {}
            for brewery in breweries:
                city = brewery.get('city', 'Unknown')
                brewery_type = brewery.get('brewery_type', 'Unknown')
                if city not in city_brewery_types:
                    city_brewery_types[city] = {}
                if brewery_type not in city_brewery_types[city]:
                    city_brewery_types[city][brewery_type] = 0
                city_brewery_types[city][brewery_type] += 1
            print(f"\nBrewery types in cities of {state}:")
            for city, types in city_brewery_types.items():
                print(f"{city}: {types}")

    # Count and list breweries with websites in the specified states
    def count_breweries_with_websites(self):
        for state in self.states:
            breweries = self.fetch_breweries_by_state(state)
            breweries_with_websites = [brewery for brewery in breweries if brewery.get('website_url')]
            print(f"\nBreweries with websites in {state}:")
            for brewery in breweries_with_websites:
                print(brewery.get('name', 'Unknown'))
            print(f"\nTotal number of breweries with websites in {state}: {len(breweries_with_websites)}")

if __name__ == "__main__":
    brewery_data = BreweryData()

    # List names of all breweries
    brewery_data.list_breweries()

    # Count the number of breweries in each state
    brewery_data.count_breweries_in_states()

    # Count the types of breweries in individual cities
    brewery_data.count_brewery_types_by_city()

    # Count and list breweries with websites
    brewery_data.count_breweries_with_websites()
