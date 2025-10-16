import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


SHEET_LINK = "https://forms.gle/77ebpiJJx4Rj4uut9"
ZILLOW_CLONE = "https://appbrewery.github.io/Zillow-Clone/"

# Get the Website
response = requests.get(ZILLOW_CLONE)

# Make a soup from Website
soup = BeautifulSoup(response.text, "html.parser")

# Make a list of all apartments listed on Website
list_of_apartments = soup.find_all(name="div", class_="StyledPropertyCardDataWrapper")
# print(list_of_apartments[2].prettify())

# Create a list of links for all the listings
list_of_links = []
# Create a list of prices for all the listings + clean up
list_of_prices = []
# Create a list of addresses for all the listings + clean up
list_of_addresses = []

for offer in list_of_apartments:
    list_of_links.append(offer.a.get("href"))
    list_of_addresses.append(offer.address.text.strip().replace(" |", ","))
    list_of_prices.append(offer.span.text.split("+")[0].strip('/mo'))


#TODO-4 Use Selenium to fill in the form you created (step 1,2,3 above).
# Each listing should have its price/address/link added to the form.
# You will need to fill in a new form for each new listing. e.g.

# Make Chrome to not close immediately
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Open browser with Google Worksheet
driver.get(SHEET_LINK)
time.sleep(3)

# Fill in a new form with each listing
for i in range(len(list_of_addresses)):
    inputs = driver.find_elements(By.CSS_SELECTOR, "div div div div div input")
    send_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    inputs[0].send_keys(list_of_addresses[i])
    inputs[1].send_keys(list_of_prices[i])
    inputs[2].send_keys(list_of_links[i])
    send_button.click()
    time.sleep(2.1)
    next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_button.click()
    time.sleep(1.7)

driver.quit()

print(f"Saving data completed! Log in to Google and access link {SHEET_LINK} to view responses!")
