# Raspberry Pi Stock Scraper and Notifier
---
Python web scraper that checks stock for various Raspberry Pi models from https://rpilocator.com/ and sends device notifications using the [Pushover API](https://pushover.net/api). 

- Python 3.6.10 is recommended
- Use of pyenv/pyenv-virtualenv/virtualenv when running script is recommended too

## Installation
---
Setup your virtual environment for Python 3.6.10. Clone the github repo and download all dependencies using:
```
$ pip install -r requirements.txt
```
Create an account with [Pushover](https://pushover.net). You can make a one-time purchase or go on a 30 day trial. View their pricing information [here](https://pushover.net/pricing). 

Log in and create a new application [here](https://pushover.net/apps/build). Fill out the necessary fields (including the icon). After creating it, you should be able to obtain the *API Token/Key*:

![Screenshot of page after creating application](https://i.imgur.com/kx2KoSj.png)

You also need your *User Key* which can be found on the Pushover home page:

![Screenshot of pushover home page when logged in](https://i.imgur.com/WHMtRe7.png)

The environment variables need to be set up to send notifications via the [Pushover API](https://pushover.net/api). So create a .env file in the directory where you cloned the repo, enter these vars and add your token and key respectively (enclosed with ""):
```
API_TOKEN = "your_api_token"
USER_KEY = "your_user_key"
```
## Usage
---
To run the script to scrape all available stock in the world, enter:
```
$ python raspbStockNotifier.py
```
You can check for country-specific stock availability by:
```
$ python raspbStockNotifier.py country_of_your_choice
```
List of available countries are:
- "australia"
- "austria"
- "belgium"
- "canada"
- "china"
- "france"
- "germany"
- "italy"
- "mexico"
- "netherlands"
- "poland"
- "south africa"
- "spain"
- "sweden"
- "switzerland"
- "united kingdom"
- "united states"

## Author
---
- **Jonathan Rivera** - *jonemilnik* 

## Acknowledgements
--- 
- **André Costa** (andre@dphacks.com) - created https://rpilocator.com/
    - Links to socials [here](https://rpilocator.com/about.cfm)

