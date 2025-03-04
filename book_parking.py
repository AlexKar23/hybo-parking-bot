from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
from datetime import datetime, timedelta

# Your Microsoft credentials
EMAIL = "your-email@example.com"
PASSWORD = "your-password"

def get_tomorrows_date():
    """ Returns tomorrow's date in MM/DD/YYYY format (for input in Hybo) """
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%m/%d/%Y")

def book_parking():
    """ Automates login and parking reservation on Hybo """

    # Setup WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background (remove if debugging)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Step 1: Open Hybo login page
        driver.get("https://app.hybo.app/home")
        time.sleep(2)

        # Step 2: Click on "Office 365 Account" button
        office365_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Office 365 Account')]")
        office365_button.click()
        time.sleep(3)

        # Step 3: Enter Microsoft Email
        email_input = driver.find_element(By.NAME, "loginfmt")
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Step 4: Enter Password
        password_input = driver.find_element(By.NAME, "passwd")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Step 5: Handle "Stay signed in?" prompt if it appears
        try:
            stay_signed_in = driver.find_element(By.ID, "idSIButton9")
            stay_signed_in.click()  # Click 'Yes'
            time.sleep(3)
        except:
            print("No 'Stay signed in' prompt.")

        # Step 6: Navigate to Parking Booking
        parking_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Parking')]")
        parking_button.click()
        time.sleep(2)

        # Step 7: Select tomorrow's date automatically
        reservation_date = get_tomorrows_date()
        date_field = driver.find_element(By.XPATH, "//input[@type='date']")
        date_field.send_keys(reservation_date)
        time.sleep(1)

        # Step 8: Select your vehicle
        vehicle_dropdown = driver.find_element(By.XPATH, "//select[@name='vehicle']")
        vehicle_dropdown.send_keys("9925KCV (Car)")
        time.sleep(1)

        # Step 9: Select the first available parking zone
        zones = driver.find_elements(By.XPATH, "//input[@type='radio']")
        for zone in zones:
            if "0 /" not in zone.get_attribute("outerHTML"):  # Check availability
                zone.click()
                break
        time.sleep(1)

        # Step 10: Confirm booking
        confirm_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
        confirm_button.click()
        time.sleep(3)

        print(f"✅ Parking successfully booked for {reservation_date}.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        driver.quit()

# Schedule the script to run every day at 08:01 AM (right after the booking opens)
schedule.every().day.at("08:01").do(book_parking)

print("⏳ Waiting for 08:01 AM to book parking automatically...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute

























