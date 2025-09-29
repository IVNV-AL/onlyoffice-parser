import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

IS_CI = os.getenv("GITHUB_ACTIONS") == "true"

def run_main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if IS_CI:
        options.binary_location = "/usr/bin/firefox"
        service = Service("/usr/local/bin/geckodriver")
    else:
        service = Service("/usr/local/bin/geckodriver")

    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://www.onlyoffice.com")
        wait = WebDriverWait(driver, 15)

        resources_menu = wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Resources"))
        )
        ActionChains(driver).move_to_element(resources_menu).perform()

        contacts_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Contacts"))
        )
        contacts_link.click()

        offices = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.companydata"))
        )

        data = []
        for office in offices:
            if "contactus_mails_area" in office.get_attribute("class"):
                continue

            country = office.find_element(By.CSS_SELECTOR, ".region").text.strip()
            company = office.find_element(By.CSS_SELECTOR, "b").text.strip()

            spans = office.find_elements(By.TAG_NAME, "span")
            address_parts = [
                span.text.strip()
                for span in spans
                if span.get_attribute("class") != "region" and not span.find_elements(By.TAG_NAME, "b")
            ]
            full_address = " ".join([p for p in address_parts if p])
            data.append([country, company, full_address])

        with open("offices.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Country", "CompanyName", "FullAddress"])
            writer.writerows(data)

        print(f"Файл offices.csv успешно создан. Количество офисов: {len(data)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_main()
