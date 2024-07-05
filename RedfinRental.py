

import requests
import json
from bs4 import BeautifulSoup
import re

def extract_numeric_value(value, allow_decimal=False):
    if allow_decimal:
        numeric_part = re.sub(r'[^\d.]', '', value)
    else:
        numeric_part = re.sub(r'[^\d]', '', value)
    return float(numeric_part) if numeric_part else 0

def get_redfin_rental_data(zipcode):
    # base_url = f"https://www.redfin.com/zipcode/{zipcode}"
    base_url = f"https://www.redfin.com/zipcode/{zipcode}/houses-for-rent"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for zipcode {zipcode}: {e}")
        return []

    if response.status_code != 200:
        print(f"Failed to retrieve data for zipcode {zipcode}")
        return []
    # print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    property_list = []

    properties = soup.find_all('div', class_='HomeCardContainer')
    
    for prop in properties:  # Limiting to 1 for testing
          # print(prop)
        address_elem = prop.find('div', class_='bp-Homecard__Address')
        beds_elem = prop.find('span', class_='bp-Homecard__Stats--beds')
        baths_elem = prop.find('span', class_='bp-Homecard__Stats--baths')
        sqft_elem = prop.find('span', class_='bp-Homecard__Stats--sqft')

        script_tag = prop.find('script', type='application/ld+json')

        latitude, longitude, url, offer_price = None, None, None, None
        if script_tag:
            json_data = json.loads(script_tag.string)
            for obj in json_data:
                if '@type' in obj and obj['@type'] == 'Product' and 'url' in obj:
                    url = obj['url']
                    break
            for obj in json_data:
                if '@context' in obj and obj['@context'] == 'http://schema.org' and 'geo' in obj:
                    latitude = obj['geo']['latitude']
                    longitude = obj['geo']['longitude']
                    break
            for obj in json_data:
                    if '@type' in obj and obj['@type'] == 'Product' and 'offers' in obj:
                        offer_price = obj['offers']['price']
                        break  # Stop after finding the offer price         

        property_details = {
            # 'address': address_elem.text.strip() if address_elem else '',
            'price': offer_price,
            'beds': extract_numeric_value(beds_elem.text.strip()) if beds_elem else 0,
            'baths': extract_numeric_value(baths_elem.text.strip(), allow_decimal=True) if baths_elem else 0,
            'sqft': extract_numeric_value(sqft_elem.text.strip()) if sqft_elem else 0,
            # 'coordinates': {
            #     'latitude': latitude,
            #     'longitude': longitude
            # },
            'url': url
        }
    
        property_list.append(property_details)
    
    return property_list

# Example usage:
zipcode = '78660'  # Replace with the desired zipcode
properties = get_redfin_rental_data(zipcode)
# Print the results
for property in properties:
    print(property)


# TODO
# get average property tax for a zip 
# get rent estimates of a zipcode from redfin and filter the closest houses by zipcode, beds, sqft and bath 
# and median of those will be the estimate renal