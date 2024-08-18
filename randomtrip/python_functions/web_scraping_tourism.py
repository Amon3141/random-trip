from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import geocoder
import requests
import urllib
from geopy.geocoders import Nominatim


# get the content in the base info table, where the row's title is one of header_text_list
def parse_content(header_text_list, soup):
  for header_text in header_text_list:
    site_content_th = soup.find('th', class_='basic-information__contents-title', string=header_text)
    if site_content_th:
      break
    
  site_content_text = None
  
  if site_content_th:
    site_content_td = site_content_th.find_next_sibling('td')
    if site_content_td:
      site_content_texts = site_content_td.find_all('p', class_='basic-information__contents-detail-text')
      if site_content_texts:
        site_content_text = site_content_texts[0].get_text(strip=True)
      else:
        site_content_text = site_content_td.get_text(strip=True)
        
  return site_content_text


def get_description(soup):
  list_of_class_list = [
    ['introduction__text'],
    ['basic-information__introduction', 'basic-information__contents-detail--white-space']
  ]
  for class_list in list_of_class_list:
    description = soup.find('p', class_=class_list)
    if description:
      return description.get_text(strip=True)
  return None


# get the coordinate from the site's name or address
def get_coordinate(name, address):
  # geocoder (OpenStreetMap) - (lat, long)
  location = name
  ret = geocoder.osm(location, timeout=5.0)
  if ret.json is not None:
    return (ret.latlng[0], ret.latlng[1])

  # geopy (Nominatim) - (lat, long)
  try:
    geolocator = Nominatim(user_agent="user")
    location = geolocator.geocode(name)
    if (location is not None):
      return (location.latitude, location.longitude)
  except Exception as e:
    print(f"An error occurred (Nominatim)")

  # 国土地理院 (郵便番号は削除) - (long, lat)
  makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
  if address is not None:
    if (address[0] == '〒'):
      address = address.split(' ')[1]
    s_quote = urllib.parse.quote(address)
    response = requests.get(makeUrl + s_quote)
    if len(response.json()) >= 1:
      return (response.json()[0]["geometry"]["coordinates"][1], response.json()[0]["geometry"]["coordinates"][0])
  
  return (None, None)


# create site_df.csv
def create_csv():
  global site_df
  
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)
  wait = WebDriverWait(driver, 10) 

  url = "https://www.asoview.com/kankou/"
  driver.get(url)
  
  # Wait for area links to be present
  area_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".niap86-1.khwHWh")))

  for i in range(len(area_links)):
    area_link = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".niap86-1.khwHWh")))[i]
    # Click the area link and wait for site links to be available
    wait.until(EC.element_to_be_clickable(area_link)).click()
    
    # Wait for the site links to be present
    site_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s77yp8-1.khPkGn")))

    for j in range(len(site_links)):
      site_link = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s77yp8-1.khPkGn")))[j]
      wait.until(EC.element_to_be_clickable(site_link)).click()
      
      wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
      html_content = driver.page_source
      soup = BeautifulSoup(html_content, 'html.parser')

      site_name_text = parse_content(["名称", "店舗名"], soup)
      site_address_text = parse_content(["住所"], soup)
      site_coordinate_lat, site_coordinate_lng = get_coordinate(site_name_text, site_address_text)
      site_homepage_text = parse_content(["ホームページ"], soup)
      site_description = get_description(soup)
      
      print(site_name_text if site_name_text else "None")
      print(site_address_text if site_address_text else "None")
      print(site_coordinate_lat if site_coordinate_lat else "None")
      print(site_coordinate_lng if site_coordinate_lng else "None")
      print(site_homepage_text if site_homepage_text else "None")
      print(site_description if site_description else "None")
        
      print("\n")
      
      new_row = pd.DataFrame(
        [[site_name_text, site_address_text, site_coordinate_lat, site_coordinate_lng, site_homepage_text, site_description]], 
        columns=["Name", "Address", "Latitude", "Longitude", "Homepage", "Description"]
      )
      site_df = pd.concat([site_df, new_row], ignore_index=True)
      
      driver.back()
      
    driver.back()

  driver.quit()


#site_df = pd.DataFrame(columns=["Name", "Address", "Latitude", "Longitude", "Homepage", "Description"])
#create_csv()
#print(site_df.head(10))
#site_df.to_csv("data/site_data.csv", index=False)

#site_df_load = pd.read_csv("data/site_data.csv")
#print(site_df_load.shape)
#print(site_df_load.info())