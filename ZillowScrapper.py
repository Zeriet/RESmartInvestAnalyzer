import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
from tabulate import tabulate

# Function to extract numeric value from string
def extract_numeric_value(value):
    numeric_part = re.search(r'\d+', value)
    return numeric_part.group() if numeric_part else ''

# Set up Selenium WebDriver
def get_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("start-maximized")  # Open Browser in maximized mode
    options.add_argument("disable-infobars")  # Disable infobars
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("--disable-popup-blocking")  # Disable pop-up blocking
    options.add_argument("--disable-notifications")  # Disable notifications
    options.add_argument("--incognito")  # Open in incognito mode
    
    # Randomly select a user-agent string
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")

    service = Service('/usr/local/bin/chromedriver')  # Replace with your path to chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_zillow_data(zipcode):
    url = f"https://www.zillow.com/homes/{zipcode}_rb/"
    driver = get_driver()
    driver.get(url)

    # Wait for the listings to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'list-card-info')))

    # Parse property details
    property_list = []
    properties = driver.find_elements_by_class_name('list-card-info')
    
    for prop in properties:
        try:
            address = prop.find_element(By.CLASS_NAME, 'list-card-addr').text
            price = prop.find_element(By.CLASS_NAME, 'list-card-price').text
            beds = prop.find_element(By.XPATH, ".//ul/li[1]").text
            baths = prop.find_element(By.XPATH, ".//ul/li[2]").text
            sqft = prop.find_element(By.XPATH, ".//ul/li[3]").text

            property_details = {
                'address': address,
                'price': price,
                'beds': extract_numeric_value(beds),
                'baths': extract_numeric_value(baths),
                'sqft': extract_numeric_value(sqft)
            }

            property_list.append(property_details)
        except Exception as e:
            print(f"Error parsing property: {e}")
            continue

    driver.quit()
    return property_list

# Example usage:
zipcode = '78660'  # Replace with the desired zipcode
properties = get_zillow_data(zipcode)

# Print the results in a tabular format
print(tabulate(properties, headers="keys", tablefmt="grid"))
