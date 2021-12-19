import json
import os
import re
import time
from hashlib import sha256 as sha


def mk_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_team(gang):
    horus = gang.find_elements_by_css_selector(".EventTeams-styles-titles > div > span")
    juchi = []
    for idaho in horus:
        juchi.append(idaho.get_attribute("innerText"))
    return juchi

def hashify(juchi):
    string = " - ".join(juchi)
    id = sha(string.encode("utf-8")).hexdigest()
    return id

def first_init(gang):
    juchi = get_team(gang)
    id = hashify(juchi)
    kori = gang.find_elements_by_css_selector(".EventOddButton-styles-odd-button > span")
    mari = []
    for lambo in kori:
        mari.append(lambo.get_attribute("innerText"))
    cols = ["1", "X", "2"]
    press = {col: orega for col, orega in zip(cols, mari)}
    [roli, ster] = juchi
    train = {"id": id, "team_1": roli, "team_2": ster, **press}
    return train


from selenium import webdriver

driver = webdriver.Chrome(executable_path="chromedriver.exe")

with open("leagues.json", "r") as file:
    datas = json.loads(file.read())

mk_dir("data")
driver.get("https://sports.tipico.de/en")
time.sleep(8)
driver.find_element_by_css_selector("#_evidon-option-button").click()
time.sleep(3)
driver.find_element_by_css_selector("#evidon-prefdiag-decline").click()
for country in datas:
    path = f"data/{country['country']}"
    mk_dir(path)
    for league in country["league"]:
        link = league["league_link"]
        name = league["league_name"]
        path_2 = path + f"/{name}.json"
        driver.get(link)
        driver.implicitly_wait(3)
        containers = driver.find_elements_by_css_selector(".Sport-styles-sport-container")
        faruk = None
        for container in containers:
            dawg = container.find_element_by_css_selector(".SportTitle-styles-sport").text
            if dawg == "Football":
                faruk = container

        freak = faruk.find_elements_by_css_selector(".EventRow-styles-event-row") if faruk is not None else []
        uvi = []
        for gang in freak:
            train = first_init(gang)
            uvi.append(train)

        if faruk is not None:
            freak = faruk.find_elements_by_css_selector(".EventRow-styles-event-row")
            select = faruk.find_element_by_css_selector("select")
            select.click()
            options = select.find_elements_by_css_selector("option")
        else:
            freak = []
            options = []
        for option in options:
            if option.text == "Over/Under":
                option.click()
                break


        if faruk is not None:
            freak = faruk.find_elements_by_css_selector(".EventRow-styles-event-row")
            select = faruk.find_element_by_css_selector("select")
            select.click()
            options = select.find_elements_by_css_selector("option")
        else:
            freak = []
            options = []

        for gang in freak:
            juchi = get_team(gang)
            id = hashify(juchi)
            param = gang.find_elements_by_css_selector(".EventOddGroup-styles-fixed-param-text")
            if len(param):
                param = param[0].text
                over_under = gang.find_elements_by_css_selector(".EventOddGroup-styles-odd-group > button > span")
                [over, under] = [over_under[0].text, over_under[1].text]
                for u in uvi:
                    if u["id"] == id:
                        u.update({"ou_param": param, "over": over, "under": under})
            else:
                for u in uvi:
                    u.update({"ou_param": 0, "over": 0, "under": 0})

        if faruk is not None:
            freak = faruk.find_elements_by_css_selector(".EventRow-styles-event-row")
            select = faruk.find_element_by_css_selector("select")
            select.click()
            options = select.find_elements_by_css_selector("option")
        else:
            freak = []
            options = []
        for option in options:
            if option.text == "Handicap":
                option.click()
                break

        freak = faruk.find_elements_by_css_selector(".EventRow-styles-event-row") if faruk is not None else []
        for gang in freak:
            juchi = get_team(gang)
            id = hashify(juchi)
            param = gang.find_elements_by_css_selector(".EventOddGroup-styles-fixed-param-text")
            if len(param):
                param = param[0].text
                handicap = gang.find_elements_by_css_selector(".EventOddGroup-styles-odd-group > button > span")
                [h_1, h_x, h_2] = [handicap[0].text, handicap[1].text, handicap[2].text]
                for u in uvi:
                    if u["id"] == id:
                        u.update({"h_1": h_1, "h_X": h_x, "h_2": h_2, "ha_param": param})
            else:
                for u in uvi:
                    u.update({"h_1": 0, "h_X": 0, "h_2": 0, "ha_param": "0:0"})
        if os.path.exists(path_2):
            with open(path_2, "r") as file:
                old_league = file.read()
                try:
                    old_data = json.loads(old_league)
                    ids = [x["id"] for x in uvi]
                    for data in old_data:
                        if data["id"] not in ids:
                            uvi.append(data)
                except:
                    pass
        with open(path_2, "w") as file:
            file.write(json.dumps(uvi, indent=4))
