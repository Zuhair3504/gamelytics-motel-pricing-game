import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from LinearRegression import get_best_price


# === Paths ===
data_directory = "Your data path directory"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = os.path.join(data_directory, f"motel_game_data_{timestamp}.csv")
os.makedirs(data_directory, exist_ok=True)

# === Chrome Setup ===
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": data_directory,
    "download.prompt_for_download": False,
    "directory_upgrade": True
})
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://gamelytics.net/motel-pricing-game.html")

# === Login ===
try:
    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login-email")))
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login-password")))
    email_input.send_keys("Your email address")  
    password_input.send_keys("Your password")  

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-formid="membership-login-form"]'))
    )
    login_button.click()
    print("🔐 Logged in successfully.")
except Exception as e:
    print("❌ Login failed:", e)
    driver.quit()
    exit()

# === Wait for game interface ===
time.sleep(3)
results = []

# === Loop through all 30 days ===
for day in range(30):
    try:
        # Get game conditions
        day_of_month = int(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[1]').get_attribute("value"))
        day_of_week = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[2]').get_attribute("value")
        weather = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[3]').get_attribute("value")

        # Get best price
        price, rooms, revpar = get_best_price (weather, day_of_week, day_of_month)  # ✅
        print(f"💡 Day {day+1}: {weather}, {day_of_week}, {day_of_month} → Price: ${price}")

        

        # Now define the price input field before using it
        price_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[4]'))
        )
        price_input.clear()
        price_input.send_keys(str(price))

        # Click the Set Price button
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[5]').click()
        time.sleep(0.5)

        # Collect result data
        row = {
            'Day': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[1]').get_attribute("value"),
            'DayOfWeek': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[2]').get_attribute("value"),
            'Weather': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[3]').get_attribute("value"),
            'Price': price,
            'RoomsBooked': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[6]').get_attribute("value"),
            'Revenue': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[7]').get_attribute("value"),
            'TotalRevenue': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[8]').get_attribute("value"),
            'AvgRevPerRoom': driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/input[9]').get_attribute("value")
        }
        results.append(row)
        
    except Exception as e:
        print(f"⚠️ Error on Day {day+1}:", e)


time.sleep(5)

# === Save to CSV ===
if results:
    with open(csv_filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"✅ Data saved to: {csv_filename}")
else:
    print("❌ No data collected.")

# === Trigger download from in-game download button ===
try:
    print("⏳ Waiting for final popup...")
    time.sleep(3)

    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[5]/div/button'))
    )
    download_button.click()
    print(" In-game download triggered.")
except Exception as e:
    print(" Could not trigger in-game download button:", e)

driver.quit()