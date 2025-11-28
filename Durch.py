import csv
import time
from urllib.parse import urljoin
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
driver = Driver(uc=True)
base_url = "https://www.dutchmanenterprises.com/inventory/?/listings/for-sale/all?DSCompanyID=127470&settingscrmid=19663818&IsSegmentSearch=1&dlr=1"
driver.uc_open_with_reconnect(base_url, 4)
time.sleep(10)
product_urls = set()
fieldnames = ["URL", "Title", "Category", "Price", "Stock Number", "Length", "Composition", "VIN", "Number of Rear Axles", "Updated", "Description", "Location", "Floor Type" ,  "Gross Vehicle Weight", "Seller" ,"Type of Neck", '','Width' ]
all_data = []
PDP_URLs=[]
All_PLPs=[]
All_PDPs=[]
# Step 1: Extract URLs and PLP-only data
while True:
    time.sleep(3)
    product_cards = driver.find_elements("css selector", ".list-container .list-listing-card-wrapper") #Get All Trailers
    # print(product_cards)
   
    for card in product_cards: #Through each trailer
            time.sleep(1)
            href_elem = card.find_element("css selector", ".listing-image-container a")
            href= href_elem.get_attribute("href")  #Get Link to PDP
            # print(href)

            if href:
                plp_data ={}
                plp_data["URL"]=href
                Btn=card.find_element("css selector", ".specs-button")
                Btn.click()
                Specs=card.find_elements("css selector", ".spec")
                plp_data["Title"] = card.find_element("css selector", ".list-listing-title-link").text.strip()
                plp_data["Category"] = card.find_element("css selector", ".listing-category").text.strip()
                plp_data["Price"]=card.find_element("css selector", ".price-contain .price").text.strip()
                
                
                # Specs.pop()
                for steps in Specs:
                    key_temp,value=steps.find_element("css selector", ".spec-label").text.strip(), steps.find_element("css selector", ".spec-value").text.strip()
                    key=key_temp[:-1]
                    plp_data[key]=value
                Location,Value = driver.find_element("css selector", ".machine-location").text.split(':',1)
                plp_data[Location]=Value
                Seller,value = driver.find_element("css selector", ".seller").text.split(':',1)
                plp_data[Seller]=value
                All_PLPs.append(plp_data)

    with open("trailers.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(All_PLPs)   

            
    # for Page in PDP_URLs:
    #         driver.get(Page)
    #         time.sleep(6)
    #         pdp_data={}
    #         pdp_data["PDP_Title"]=driver.find_element("tag name","h1").text.strip()
    #         pdp_data["PDP_Condition"]=driver.find_element("css selector","h1 span.condition").text
    #         pdp_data["PDP_Price"]=driver.find_element("css selector"," span.price").text.strip()
    #         info_blocks = driver.find_elements("css selector", ".item-information-container .information")
    #         for info in info_blocks:
    #             text = info.text.strip()
    #             if ":" in text:
    #                 key, value = text.split(":", 1)
    #                 key = key.strip().title()   
    #                 pdp_data[key]=value     
    #         container=driver.find_element("css selector", ".toastui-editor-contents")
    #         elements=container.find_elements("tag name", "p")
    #         list=[]
    #         for i in elements:
    #             test=i.text.strip()
    #             list.append(test)
    #         pdp_data["Trailer Overview"]=list

    #         AdditionalSpecs_List=driver.find_elements("css selector", ".description-details-container .detail")

    #         list=[]
    #         for items in AdditionalSpecs_List:
    #             label = items.find_element("css selector", ".label").text.strip()
    #             value = items.find_element("css selector", ".value").text.strip()
    #             print(label,value)

    #             list.append(f"{label}{value}")

    #         pdp_data["Additional Specs"]=list
    #         All_PDPs.append(pdp_data)
            
    
    # for plp, pdp in zip(All_PLPs, All_PDPs):
    #     new_data = {**plp, **pdp}
    #     all_data.append(new_data)
              

                
    
    

           
