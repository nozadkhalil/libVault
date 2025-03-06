import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def submit_gacos_request(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Path to your GeckoDriver (replace with your actual path)
    geckodriver_path = "/opt/anaconda3/bin/geckodriver"  # Example: "/usr/local/bin/geckodriver"
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service)

    try:
        driver.get("http://www.gacos.net/")

        # Wait for the form to load (adjust timeout as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "N"))  # Wait for the N input field
        )

        # Fill the form
        driver.find_element(By.NAME, "N").send_keys(config["north"])
        driver.find_element(By.NAME, "W").send_keys(config["west"])
        driver.find_element(By.NAME, "E").send_keys(config["east"])
        driver.find_element(By.NAME, "S").send_keys(config["south"])

        time_parts = config["time_of_interest"].split(":")
        driver.find_element(By.NAME, "H").send_keys(time_parts[0])
        driver.find_element(By.NAME, "M").send_keys(time_parts[1])

        date_string = "\n".join(config["date_list"])
        driver.find_element(By.NAME, "date").send_keys(date_string)

        driver.find_element(By.NAME, "email").send_keys(config["email"])

        if config["output_format"] == "Geotiff":
            driver.find_element(By.ID, "optionsRadios2").click()
        elif config["output_format"] == "Binary grid":
            driver.find_element(By.ID, "optionsRadios1").click()
        
        # Wait for the submission to complete (adjust timeout as needed)
        time.sleep(15)  # Simple wait, improve as needed
        # Submit the form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()  # More robust way to find submit


        print("Request submitted successfully (or at least the form was filled and submitted).")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    config_file_path = "config.json"  # Replace with the actual path to your config file
    submit_gacos_request(config_file_path)
