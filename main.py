import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Define download directory (current working directory)
download_dir = os.getcwd()

# Define driver options
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")

# Set preferences to automatically download files to the specified directory
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False, # Disables the "Save As" prompt
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

service = Service('chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options, service=service)

# Navigate to the login page
driver.get('https://demoqa.com/login')

# Locate username, password and login button
username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
login_button = driver.find_element(By.ID, 'login')

# Fill in username and password, and click the login button
username_field.send_keys('nabil29089')
password_field.send_keys('Nabil371#')
driver.execute_script("arguments[0].click();", login_button)

# 1. Locate the "Elements" accordion using a cleaner XPath
elements = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[text()='Elements']"))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elements)
driver.execute_script("arguments[0].click();", elements)

# 2. Wait for the "Text Box" option and click it
text_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Text Box']"))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", text_box)
driver.execute_script("arguments[0].click();", text_box)

# 3. Locate the form fields and fill them with fake data
full_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
email = driver.find_element(By.ID, 'userEmail')
current_address = driver.find_element(By.ID, 'currentAddress')
permanent_address = driver.find_element(By.ID, 'permanentAddress')
submit_button = driver.find_element(By.ID, 'submit')

full_name.send_keys("John Doe")
email.send_keys("johndoe@fakeemail.com")
current_address.send_keys("123 Fake Street, Springfield")
permanent_address.send_keys("456 Real Avenue, Shelbyville")

# Scroll to and click the Submit button
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
driver.execute_script("arguments[0].click();", submit_button)
print("Text Box form filled and submitted!")

# 4. Navigate to the "Upload and Download" section
upload_download_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Upload and Download']"))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_download_menu)
driver.execute_script("arguments[0].click();", upload_download_menu)

# 5. Locate the Download button and click it
download_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'downloadButton'))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
driver.execute_script("arguments[0].click();", download_button)
print(f"File downloaded to: {download_dir}")

input("Press Enter to close the browser")
driver.quit()