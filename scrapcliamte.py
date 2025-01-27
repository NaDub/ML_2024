import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_decorator(func):
    """
    Decorator function that fetches the content from a URL and 
    parses it using the provided parsing function.
    """
    def wrapper(url: str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return func(soup)
        else:
            print(f"Request failure for {url}: {response.status_code}")
            return None
    return wrapper

@fetch_decorator
def parse_climate(soup: BeautifulSoup) -> pd.DataFrame:
    """
    Function to parse type of climate of major cities in India from https://fr.climate-data.org/asie/inde-129/.
    
    Args:
        url (str): The URL of the page from which the content is retrieved.

    Returns:
        str: structured data about the type of major indian cities climate extracted from the HTML content.
    """
    rows = soup.find_all('tr')
    data = []
    
    for row in rows[1:]:
        koppen_code = row.find_all('td')[2].get_text(strip=True)
        cities_td = row.find_all('td')[3]
        cities = [a.text.strip() for a in cities_td.find_all('a')]

        for city in cities:
            data.append({
                "City": city,
                "Koppen Code": koppen_code
            })
    
    df = pd.DataFrame(data)
    return df

df = parse_climate('https://fr.climate-data.org/asie/inde-129/')
df.to_csv('data_climate.csv', index=False)
