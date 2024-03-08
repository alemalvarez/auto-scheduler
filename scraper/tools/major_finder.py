from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json

# Set the path to the ChromeDriver executable. The driver for Apple ARM64 is included in the repo.
service = Service('./chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

# Navigate to the base URL for all schedules.
url = "https://www.csus.edu/class-schedule/fall-2024/"
driver.get(url)

# Wait for the page to fully load (adjust the delay as needed)
time.sleep(2)

# Parse the HTML content using BeautifulSoup
html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, "html.parser")

# Find all <a> tags with href containing '/class-schedule/fall-2024/'
links = soup.find_all("a", href=lambda href: href and '/class-schedule/fall-2024/' in href)

# Extract majors from the links
majors = []
for link in links:
    href = link.get('href')
    major = href.split('/')[-1]
    majors.append(major)

# Write the list of majors to a JSON file
with open("fall-2024-majors.json", "w") as json_file:
    json.dump(majors, json_file)

# Quit the webdriver

