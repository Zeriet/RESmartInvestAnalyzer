import requests
import json
from bs4 import BeautifulSoup
import re

def get_redfin_property_data(url_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url_link, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for  {url_link}: {e}")
        return []

    if response.status_code != 200:
        print(f"Failed to retrieve data for {url_link}")
        return []
    soup = BeautifulSoup(response.content, 'html.parser')


    # Extract the entire HTML content as a string
    html_string = str(soup)

    # Print extracted HTML to inspect it
    print(html_string)

    # Extract homeInsuranceRate using regular expression
    home_insurance_match = re.search(r'"homeInsuranceRate":([0-9.]+)', html_string)
    print(home_insurance_match)
    home_insurance_rate = float(home_insurance_match.group(1)) if home_insurance_match else None

    # Extract mortgageInsuranceRate using regular expression
    mortgage_insurance_match = re.search(r'"mortgageInsuranceRate":([0-9.]+)', html_string)
    mortgage_insurance_rate = float(mortgage_insurance_match.group(1)) if mortgage_insurance_match else None

    print(f'homeInsuranceRate = {home_insurance_rate}')
    print(f'mortgageInsuranceRate = {mortgage_insurance_rate}')



link_url =  'https://www.redfin.com/TX/Pflugerville/1513-Dahlia-Ct-78660/home/31989395#property-history'
property_info = get_redfin_property_data(link_url)