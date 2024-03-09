import os
import json
import time
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

TERM = 'spring-2024' #< -- CHOOSE TERM HERE

def setup_driver() -> webdriver.Chrome:
    """
    Set up the Chrome webdriver with appropriate options.

    Returns:
        webdriver.Chrome: The configured Chrome webdriver instance.
    """
    print("Setting up Chrome webdriver...")
    service = Service('./chromedriver-mac-arm64/chromedriver')
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome webdriver set up successfully.")
    return driver

def get_majors(driver: webdriver.Chrome) -> List[str]:
    """
    Get the list of majors from the base URL.

    Args:
        driver (webdriver.Chrome): The configured Chrome webdriver instance.

    Returns:
        List[str]: A list of majors.
    """
    print("Retrieving list of majors...")
    url = f"https://www.csus.edu/class-schedule/{TERM}/"
    driver.get(url)

    time.sleep(2)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("a", href=lambda href: href and f'/class-schedule/{TERM}/' in href)

    majors = []
    for link in links:
        href = link.get('href')
        major = href.split('/')[-1]
        majors.append(major)

    print(f"{len(majors)} majors found.")
    return majors

def scrape_major(driver: webdriver.Chrome, major: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Scrape the course schedule data for a given major.

    Args:
        driver (webdriver.Chrome): The configured Chrome webdriver instance.
        major (str): The major for which to scrape the course schedule data.

    Returns:
        Dict[str, List[Dict[str, str]]]: A dictionary containing the course schedule data for the given major.
    """
    print(f'Scraping major: {major}')

    url = f"https://www.csus.edu/class-schedule/{TERM}/{major}"
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.table')))

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    table_divs = soup.find_all('div', class_='table')

    data = {}

    for table_div in table_divs:
        h2_element = table_div.find('h2')

        if h2_element:
            h2_text = h2_element.text.strip()
            class_name = h2_text.split(' - ')[0]
            data[class_name] = []

            row_divs = table_div.find_all('div', role='row')
            row_divs = row_divs[1:]

            for row_div in row_divs:
                cells = row_div.find_all(recursive=False)

                if len(cells) >= 3:
                    days = cells[3].text.strip()
                    start_time = cells[5].text.strip()
                    end_time = cells[6].text.strip()
                    row_data = {
                        'days': days,
                        'startTime': start_time,
                        'endTime': end_time
                    }

                    if class_name in data:
                        data[class_name].append(row_data)

    print(f'{len(data.keys())} courses found for {major}.')
    return data

def scrape_all_majors(majors: List[str]) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    """
    Scrape the course schedule data for all provided majors.

    Args:
        majors (List[str]): A list of majors for which to scrape the course schedule data.

    Returns:
        Dict[str, Dict[str, List[Dict[str, str]]]]: A dictionary containing the course schedule data for all majors.
    """
    print("Scraping course schedules for all majors...")
    driver = setup_driver()
    all_data = {}

    try:
        for major in majors:
            data = scrape_major(driver, major)
            all_data[major] = data
    finally:
        print("Scraping complete. Quitting webdriver...")
        driver.quit()

    return all_data

def save_data(data: Dict[str, Dict[str, List[Dict[str, str]]]], output_directory: str):
    """
    Save the scraped course schedule data to a JSON file.

    Args:
        data (Dict[str, Dict[str, List[Dict[str, str]]]]): The course schedule data to be saved.
        output_directory (str): The directory where the JSON file should be saved.
    """
    os.makedirs(output_directory, exist_ok=True)
    output_filename = os.path.join(output_directory, f"{TERM}.json")
    try:
        with open(output_filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to {output_filename}")
    except Exception as e:
        print(f"Error saving data to {output_filename}: {e}")

def main():
    print("Starting scraper...")
    driver = setup_driver()
    majors = get_majors(driver)

    all_data = scrape_all_majors(majors)
    save_data(all_data, './schedules/')
    print("Scraping process completed successfully.")

if __name__ == "__main__":
    main()