from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import datetime
import requests
import re
import time

CHROME_DRIVER_PATH = r"/Users/caleb/Documents/chromedriver/chromedriver"
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8"
}

itemurl= 'insert the url of the item you want here'
maxbid = "ENTER THE MAX AMOUNT YOU'D BE WILLING TO SPEND AS INT OR FLOAT"
timeleft = "ENTER A WHOLE NUMBER INT FOR HOW MANY MINUTES YOU'DLIKE THE BOT TO WATCH THE AUCTION FOR YOU"

now = datetime.datetime.now()
right_now = [now.day, now.hour, now.minute]

#SIGN-IN

try:

    driver.get("https://www.ebay.com/")
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "gh-ug-guest").click()

    def login():
        driver.find_element(By.ID, "userid").send_keys("ENTER YOUR USERNAME")
        time.sleep(3)
        driver.find_element(By.ID, "signin-continue-btn").click()
        time.sleep(3)
        driver.find_element(By.ID, "pass").send_keys("ENTER YOUR PASSWORD")
        time.sleep(3)
        driver.find_element(By.ID, "sgnBt").click()

    login()

except NoSuchElementException:
    print("Captcha Detected, please complete it for the sniper to continue.")
    time.sleep(30)
    login()


#GO TO URL OF ITEM YOU WANT TO SNIPE

time.sleep(1)
driver.get("https://www.ebay.com/itm/265493086466?hash=item3dd09f0102:g:mooAAOSw0gFh25aF")
response = requests.get(itemurl, headers=header)
time.sleep(2)
data = response.text
soup = BeautifulSoup(data, "html.parser")

noscripts = soup.find_all("noscript")
end_date = noscripts[2].text
raw_str = end_date
match = re.search(r'(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)', raw_str)
string_list = match.group(0).replace(':', ' ').split()
integer_map = map(int, string_list)
auction_end = list(integer_map)
print(auction_end)
time.sleep(2)


def bid():
    current_bid = soup.find("span", id="w1-19-_mtb").text.replace("Enter US $", "").replace(" or more", "")
    bid = float(current_bid)
    print(bid)
    while bid <= maxbid:
        new_bid = bid + 1
        driver.find_element(By.ID, "MaxBidId").send_keys(new_bid)
        driver.find_element(By.CLASS_NAME, "btn btn-prim  vi-VR-btnWdth-L vilens-item").click()
        time.sleep(1.5)
        driver.find_element(By.CLASS_NAME, "button-placebid").click()
        time.sleep(1)
        if driver.find_element(By.CLASS_NAME, "button-placebid"):
            detected = True
            while detected is True:
                winning_bid = driver.find_element(By.CLASS_NAME, "ui-text-span__BOLD").replace("US $", "")
                bid = float(winning_bid)
                new_bid = bid + 1
                driver.find_element(By.ID, "app-bidlayer-bidsection-input").send_keys(new_bid)
                driver.find_element(By.CLASS_NAME, "button-placebid").click()
                time.sleep(1)
    else:
        print("Bidding has exceeded your maximum price.")
        driver.close()


def bidding_time():
    bid_war = False
    while bid_war is False:
        if auction_end[0] == right_now[0] and auction_end[1] == right_now[1] and auction_end[2] - right_now[2] <= 5:
            bid_war = True
            bid()


bidding_time()

