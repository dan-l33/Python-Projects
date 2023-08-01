import requests
from bs4 import BeautifulSoup
import csv

page = requests.get("https://www.hotukdeals.com/deals")
soup = BeautifulSoup(page.text, "html.parser")
temps = soup.findAll("span", attrs={"cept-vote-temp vote-temp vote-temp--hot"})
deals = soup.findAll("a", attrs={"class":"cept-tt thread-link linkPlain thread-title--list js-thread-title"})
prices = soup.findAll("span", attrs={"class":"thread-price text--b cept-tp size--all-l size--fromW3-xl"})

file = open("Scaped_deals.csv", "w")
writer = csv.writer(file)

writer.writerow(["TEMPS (°)", "DEALS", "PRICES (£)"])

for temp, deal, price in zip(temps, deals, prices):
    if temp.text.strip() + deal.text + price.text != "":
        print("[" + temp.text.strip() + "] " + deal.text + ": " + price.text)
        writer.writerow([temp.text.strip().replace("°",""), deal.text, price.text.replace("£","")])
    else:
        break

file.close()
