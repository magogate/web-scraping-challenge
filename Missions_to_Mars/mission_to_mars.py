import requests
import bs4
import re

baseUrl = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc"

response = requests.get(baseUrl)    
soup = bs4.BeautifulSoup(response.text, "html.parser")
print(response.text)