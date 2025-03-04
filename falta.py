from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Set up Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox")  # Required for root environments
options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in limited memory
options.add_argument("--remote-debugging-port=9222")  # Enables debugging
options.binary_location = "/usr/bin/google-chrome"  # Set Chrome path

# Set correct ChromeDriver path
service = Service("/usr/bin/chromedriver")

# Start Chrome WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Test if Chrome is working
driver.get("https://www.google.com")
print("Page Title:", driver.title)

driver.quit()
