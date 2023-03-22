from bs4 import BeautifulSoup
import requests
import time
import re
from dotenv import load_dotenv
from datetime import datetime
import shortuuid
import os
import sys

class StockNotifier:
    def __init__(self, country):
        self.s = requests.Session()
        load_dotenv()
        self.phoneAPIToken = os.environ.get("API_TOKEN")
        self.userAPIKey = os.environ.get("USER_KEY")
        soup = self.__getWebPage()
        self.token = self.__extractLocalToken(soup)
        self.inStock = {}
        self.country = country

    def __getWebPage(self):
        r = self.s.get("https://rpilocator.com/?country=UK")
        soup = BeautifulSoup(r.text, "lxml")
        return soup

    def __extractLocalToken(self, soup):
        # Extract token for Website API call
        scripts = soup.find_all("script")
        tokenScriptTag = list(
            filter(lambda tag: "localToken" in str(tag.string), scripts))
        contents = str(tokenScriptTag[0].string)
        tokenVar = re.search(r"localToken=(\"|\").+(\"|\")", contents).group()
        token = re.search(r"(\"|\").+(\"|\")", tokenVar).group().strip("\"\"")

        print("\nRetrieved Token: {}\n\n".format(token))
        return token 

    def reconnectToServer(self):
        self.s = requests.Session()
        soup = self.__getWebPage()
        self.token = self.__extractLocalToken(soup)
    
    def setStoredStock(self, stock):
        for item in stock:
            id, itemStr = self.formatItem(item)
            self.inStock[id] = itemStr
    
    def clearStoredStock(self):
        self.inStock = {}
    
    def getStoredStock(self):
        return self.inStock

    def getCurrentStock(self):
    # Set up request headers and params
        headers = {"Connection": "keep-alive",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.5",
                "Host": "rpilocator.com",
                "Referer": "https://rpilocator.com/?country=UK",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers",
                "X-Requested-With": "XMLHttpRequest"}
        payload = {}
        if self.country:
            payload = {"method": "getProductTable", "token": self.token,
                    "country": self.country, "_": "1677696951662"}
        else:
            payload = {"method": "getProductTable", "token": self.token,
                    "_": "1677696951662"}
        url = "https://rpilocator.com/data.cfm"

        try:
            r = self.s.get(url, params=payload, headers=headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            t = datetime.now()
            print("{}: {}\n".format(t.strftime('%a, %d %b %Y %H:%M:%S'), e))
            with open("requestLog.txt", "a+") as f:
                f.write("{}: {}\n".format(t.strftime('%a, %d %b %Y %H:%M:%S'), e))
            self.reconnectToServer()
        
        return {"data": []}

    def sendNotification(self, stock):
        message = ""
        for item in stock:
            message = stock[item]
            payload = {"token": self.phoneAPIToken, "user": self.userAPIKey, "message": message}
            r = requests.post("https://api.pushover.net/1/messages.json", params=payload)
    
    def formatItem(self, item):
        itemStr = "{} is in stock in {}! Link to buy --> {}".format(
                item["description"],
                item["vendor"], 
                item["link"])
        id = shortuuid.uuid(name = itemStr)
        return id, itemStr

    def filterAndGetNewStock(self, stock):
        #get list of all current items in stock
        #compare items with previous stock check and add those
        newStock = {}
        for item in stock["data"]:
            id, itemStr = self.formatItem(item)
            if item["avail"] == "Yes":
                if id not in self.inStock:
                    newStock[id] = itemStr
                    self.inStock[id] = itemStr
                    
            else: #remove item from inStock if no longer available
                if id in self.inStock:
                    del self.inStock[id]
            
        return newStock

    def main(self):

        while True:
            stock = self.getCurrentStock()
            newStock = self.filterAndGetNewStock(stock)
            
            # Send notification
            if newStock:
                self.sendNotification(newStock)

            time.sleep(5)

if __name__ == "__main__":
    country = ""
    countries = {
        "australia": "AU", 
        "austria": "AT", 
        "belgium": "BE", 
        "canada": "CE",
        "china": "CN",
        "france": "FR",
        "germany": "DE",
        "italy": "IT",
        "mexico": "MX",
        "netherlands": "NL",
        "poland": "PL",
        "portugal": "PT",
        "south africa": "ZA",
        "spain": "ES",
        "sweden": "SE",
        "switzerland": "CH",
        "united kingdom": "UK",
        "united states": "US"
    }

    if 2 <= len(sys.argv) <= 3:
        args = sys.argv[1:]
        country = " ".join(args)
        if country not in countries:
            raise KeyError("Country not found")
        country = countries[country]
    elif len(sys.argv) == 1:
        pass
    else:
        raise IndexError("Too many args given")
    
    notifier = StockNotifier(country)
    notifier.main()
