#!/usr/bin/env python3

import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def search_name(driver, name):
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/div/div/input'))
        )
        search_input.clear()
        search_input.send_keys(name)
        
        search_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/div/div/span/button')
        search_button.click()
        
        time.sleep(2)
        
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error searching for {name}: {e}")
        return False

def download_image(driver, name):
    try:
        time.sleep(1)
        
        image_elements = driver.find_elements(By.TAG_NAME, 'img')
        
        for img in image_elements:
            src = img.get_attribute('src')
            if src and 'data:image' not in src:
                # Use the browser's session to fetch the image via JavaScript
                img_data = driver.execute_script("""
                    var img = arguments[0];
                    var canvas = document.createElement('canvas');
                    canvas.width = img.naturalWidth;
                    canvas.height = img.naturalHeight;
                    var ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);
                    return canvas.toDataURL('image/jpeg').split(',')[1];
                """, img)

                if img_data:
                    filename = f"{name.replace(' ', '_')}.jpg"
                    filepath = os.path.join('output', filename)

                    with open(filepath, 'wb') as f:
                        f.write(base64.b64decode(img_data))

                    print(f"Downloaded image for {name} to output/{filename}")
                    return True
        
        print(f"No suitable image found for {name}")
        return False
        
    except Exception as e:
        print(f"Error downloading image for {name}: {e}")
        return False

def main():
    if not os.path.exists('output'):
        os.makedirs('output')
        print("Created output directory")
    
    with open('names.txt', 'r') as f:
        names = [line.strip() for line in f if line.strip()]
    
    driver = setup_driver()
    
    try:
        print("Navigating to the website...")
        driver.get('https://collface.deptcpanel.princeton.edu')
        
        print("\nPlease login if needed.")
        print("Type 'y' when ready to start scraping, or 'n' to cancel: ")
        
        while True:
            user_input = input().strip().lower()
            if user_input == 'y':
                print("Starting scraping process...")
                break
            elif user_input == 'n':
                print("Scraping cancelled.")
                driver.quit()
                return
            else:
                print("Please type 'y' to continue or 'n' to cancel: ")
        
        for name in names:
            print(f"\nSearching for: {name}")
            
            if search_name(driver, name):
                download_image(driver, name)
            
            time.sleep(1)
        
        print("\nScraping completed!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()