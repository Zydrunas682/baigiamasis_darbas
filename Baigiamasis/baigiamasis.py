# Baigiamasis
# kainu ir pavadinimo isrinkimas


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import csv


opciones = Options()
opciones.add_argument('--incognito')
opciones.headless = True  
driver = webdriver.Chrome(options=opciones)

base_url = "https://elenta.lt/"
driver.get(base_url)

ads_data = []
page = 1

while True:
    print(f"Scraping page {page}...")
    
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    
    ad_elements = soup.find_all("div", class_="list_item")
    
    for ad_element in ad_elements:
        title_element = ad_element.find("a", class_="list_item-title")
        price_element = ad_element.find("span", class_="price-box")
        
        if title_element and price_element:
            title = title_element.get_text(strip=True)
            price = price_element.get_text(strip=True)
            
            ads_data.append([title, price])
            print(f"Title: {title}, Price: {price}")
    
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.page-item a[aria-label='Next']")
        next_button.click()
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))  
        sleep(2)
        page += 1
    except Exception as e:
        print(f"No next page found or error: {e}")
        break

if ads_data:
    with open('elenta_ads.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Pavadinimas', 'Kaina']) 
        writer.writerows(ads_data)
    print("Duomenys išsaugoti faile: elenta_ads.csv")
else:
    print("Nepavyko surasti jokių skelbimų.")

driver.quit()
