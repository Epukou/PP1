import requests
import json
import logging
from bs4 import BeautifulSoup
from prettytable import PrettyTable

# Seems like I can't navigate with ctrl + space (suggestions?)
with open("IMDB\config\config.json", "r") as f:
    config = json.load(f)

#INFO level
log_level = config["logging"]["level"]

logging.basicConfig(filename=config["logging"]["filename"], level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

url = config["imdb"]["url"]

table_selector = config["imdb"]["table_selector"]

try:
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.content
    logging.info(f"Successfully fetched HTML content from {url}")
except requests.exceptions.RequestException as e:
    logging.error(f"Failed to fetch HTML content from {url}: {e}")
    raise

soup = BeautifulSoup(html_content, "html.parser")

table = soup.select_one(table_selector)

#PrettyTable for more clear data in the .txt file
x = PrettyTable()
x.field_names = ["Title", "IMDb Rating"]

for row in table.find_all("tr"):
    title = row.find("td", class_="titleColumn").a.text
    rating = row.find("td", class_="ratingColumn").strong.text
    x.add_row([title, rating])

try:
    #added encoding because of lithuanian language
    with open("IMDB_TOP250.txt", "w", encoding='utf-8') as f:
        f.write(str(x))
    logging.info("Successfully wrote the table to a text file")
except Exception as e:
    logging.error(f"Failed to write the table to a text file: {e}")
    raise
