from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

driver = webdriver.Chrome("/Users/emilywang/Desktop/chromedriver")

csv_file = open('cp_atl.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['tags', 'livestream', 'name', 'location', 'avg_rating', 'num_ratings'])

driver.get('https://classpass.com/search/atlanta/fitness-classes/55HtASzNJ2j')
index = 1

while True:
    print(f'Scraping page: {index}')
    time.sleep(2)

    studios = driver.find_elements_by_xpath('//li[@data-component="SearchResultsList"]')
    print(f'Studios = {len(studios)}')

    for studio in studios:
        data_dict = {}
        try:
            tags = studio.find_element_by_xpath('.//div[@data-qa="VenueItem.activities"]').text.lower()
            livestream = 'livestream' in tags
            tags = tags.split(',')
        except:
            tags = None
            livestream = None
    #     print(tags)

        name = studio.find_element_by_xpath('.//a[@data-qa="VenueItem.name"]').text

        try:
            location = studio.find_element_by_xpath('.//div[@data-qa="VenueItem.location"]').text
        except:
            location = None
    
        try:
            avg_rating = float(studio.find_element_by_xpath('.//span[@class="ratings__rating ratings--child"]/span').text)
        except:
            avg_rating = None

        try:
            num_ratings = studio.find_element_by_xpath('.//span[@class="ratings__count ratings--child"]').text
        except:
            num_ratings = None
            
        data_dict['tags'] = tags
        data_dict['livestream'] = livestream
        data_dict['name'] = name
        data_dict['location'] = location
        data_dict['avg_rating'] = avg_rating
        data_dict['num_ratings'] = num_ratings

        writer.writerow(data_dict.values())
        
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        next_button = driver.find_element_by_xpath('//nav[@role="navigation"]/button[2]')
        next_button.click()
        index += 1
        
    except ElementClickInterceptedException:
        #click through the intro popup
        try:
            ad_button = driver.find_element_by_xpath('//button[@aria-label="hide promotion"]')
            ad_button.click()
            next_button.click()
            index += 1
        except:
            break

driver.quit()