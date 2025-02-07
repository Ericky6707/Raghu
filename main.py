# Created by Raghu | Acc Rullx
# Auto Name Change Script for Facebook Messenger Group

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# ========== CONFIGURATION ==========
FB_EMAIL = "your-email@example.com"  # Your Facebook email
FB_PASSWORD = "your-password"  # Your Facebook password
GROUP_CHAT_LINK = "https://www.messenger.com/t/YOUR_GROUP_ID"  # Your Messenger Group Link
NEW_GROUP_NAME = "My New Auto Group Name"  # New group name

# ========== SELENIUM SETUP ==========
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs in background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.get("https://www.messenger.com/")
time.sleep(5)

# ========== LOGIN TO FACEBOOK ==========
driver.find_element(By.NAME, "email").send_keys(FB_EMAIL)
driver.find_element(By.NAME, "pass").send_keys(FB_PASSWORD + Keys.RETURN)
time.sleep(10)  # Wait for login

# ========== OPEN MESSENGER GROUP ==========
driver.get(GROUP_CHAT_LINK)
time.sleep(5)

# ========== OPEN GROUP SETTINGS ==========
settings_button = driver.find_element(By.XPATH, "//div[@aria-label='Chat settings']")
settings_button.click()
time.sleep(2)

# ========== CLICK ON "EDIT CHAT NAME" ==========
rename_option = driver.find_element(By.XPATH, "//span[contains(text(),'Edit chat name')]")
rename_option.click()
time.sleep(2)

# ========== CHANGE GROUP NAME ==========
group_name_box = driver.find_element(By.XPATH, "//input[@type='text']")
group_name_box.clear()
group_name_box.send_keys(NEW_GROUP_NAME + Keys.RETURN)

print("✅ Group name changed successfully! | Created by Raghu | Acc Rullx")

time.sleep(5)
driver.quit()
