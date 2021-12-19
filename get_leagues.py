import json
from selenium import webdriver
import time
driver = webdriver.Chrome(executable_path = "chromedriver.exe")

driver.get("https://sports.tipico.de/en/todays-matches")
time.sleep(5)
driver.find_element_by_css_selector("#_evidon-option-button").click()
time.sleep(3)
driver.find_element_by_css_selector("#evidon-prefdiag-decline").click()
aby = driver.find_elements_by_css_selector("#app > main > main > nav > div.Navigation-styles-navigation-container > ul:nth-child(4) > li > div")
for ab in aby:
    if ab.find_element_by_css_selector("div > div > div > span > a").get_attribute("innerText") == "Football":
        bre = ab
bre.click()
crazy = bre.find_elements_by_css_selector(".NavigationItem-styles-navigation-item-wrapper > ul > li")
drones = []
for crocks in crazy:
    crocks.click()
    drake = crocks.find_elements_by_css_selector("div > label > a")
    front = crocks.find_element_by_css_selector("div > div > div > div > span > a").get_attribute("innerText")
    dust = {"country": front, "league": []}
    for drive in drake:
        ella = drive.get_attribute("innerText")
        erin = drive.get_attribute("href")
        damn = {"league_name": ella, "league_link": erin}
        dust["league"].append(damn)
    drones.append(dust)

with open ("leagues.json", "w") as file:
    file.write(json.dumps(drones, indent=4))
# driver.quit()