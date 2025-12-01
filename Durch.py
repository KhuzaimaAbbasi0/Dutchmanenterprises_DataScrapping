import csv
import time
from urllib.parse import urljoin
import time, random
from seleniumbase import Driver
from selenium import webdriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
driver = Driver(uc=True)
base_url = "https://www.dutchmanenterprises.com/inventory/?/listings/for-sale/all?DSCompanyID=127470&settingscrmid=19663818&IsSegmentSearch=1&dlr=1"
driver.uc_open_with_reconnect(base_url, 4)
time.sleep(10)
driver.execute_script("window.scrollBy(0, 300)")
product_urls = set()
fieldnames = ["URL", "Title", "Category", "Price", "Stock Number", "Length", "Composition", "VIN", "Number of Rear Axles", "Updated", "Description", "Location", "Floor Type" ,  "Gross Vehicle Weight", "Seller" ,"Type of Neck", '','Width', "PDP_Title", "PDP_Category", "PDP_Price", "PDP_Stock Number", "PDP_Length", "PDP_Composition", "PDP_VIN", "PDP_Number of Rear Axles", "PDP_Description", "PDP_Location", "PDP_Floor Type" ,  "PDP_Gross Vehicle Weight", "PDP_Seller" ,"PDP_Type of Neck", '','PDP_Width', "PDP_Condition", "PDP_Year", "PDP_Manufacturer" ]
all_data = []
PDP_URLs=[]
All_PLPs=[]
All_PDPs=[]

# Step 1: Extract URLs and PLP-only data
while True:
    time.sleep(3)
    product_cards = driver.find_elements("css selector", ".list-container .list-listing-card-wrapper") #Get All Trailers
   
    for card in product_cards: #Through each trailer
            time.sleep(random.uniform(1.5, 3.0))
            href_elem = card.find_element("css selector", ".listing-image-container a")
            href= href_elem.get_attribute("href")  #Get Link to PDP

            if href:
                plp_data ={}
                PDP_URLs.append(href)
                plp_data["URL"]=href
                Btn=card.find_element("css selector", ".specs-button")
                Btn.click()
                Specs=card.find_elements("css selector", ".spec")
                plp_data["Title"] = card.find_element("css selector", ".list-listing-title-link").text.strip()
                plp_data["Category"] = card.find_element("css selector", ".listing-category").text.strip()
                plp_data["Price"]=card.find_element("css selector", ".price-contain .price").text.strip()
                
            
                for steps in Specs:
                    key_temp,value=steps.find_element("css selector", ".spec-label").text.strip(), steps.find_element("css selector", ".spec-value").text.strip()
                    key=key_temp[:-1]
                    plp_data[key]=value
                Location,Value = driver.find_element("css selector", ".machine-location").text.split(':',1)
                plp_data[Location]=Value
                Seller,value = driver.find_element("css selector", ".seller").text.split(':',1)
                plp_data[Seller]=value
                All_PLPs.append(plp_data)

    
    button_next=driver.find_element("css selector", '[aria-label="Next Page"]')
    Present=True
    if(button_next.is_enabled()):
        button_next.click()

    else:        
        Present=False

    if(Present==False):
        for Page in PDP_URLs:

            driver.get(Page)
            time.sleep(random.uniform(1.5, 3.0))
            pdp_data={}
            pdp_data["PDP_Title"]=driver.find_element("css selector",".detail__title").text.strip()
            pdp_data["PDP_Category"]=driver.find_element("css selector",".detail__category").text.strip()
            pdp_data["PDP_Price"]=driver.find_element("css selector",".listing-prices__retail-price").text.strip()
            pdp_data["PDP_Location"]=driver.find_element("css selector", ".dealer-contact__location").text.strip()
            content= driver.find_elements("css selector", ".detail__specs-wrapper .detail__specs-label")
            Values= driver.find_elements("css selector", ".detail__specs-wrapper .detail__specs-value")
            for x,y in zip(content,Values):
                pdp_data["PDP_"+x.text.strip()]=y.text.strip()
            print(pdp_data)
            All_PDPs.append(pdp_data)
            
    
            for plp, pdp in zip(All_PLPs, All_PDPs):
                new_data = {**plp, **pdp}
                all_data.append(new_data)
              

                
            with open("trailers.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_data)  
    

           
