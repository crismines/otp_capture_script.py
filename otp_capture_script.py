import time
import telebot
import threading
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Telegram bot
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
telegram_user_id =   # Replace with your actual user ID
bot = telebot.TeleBot(bot_token)

# Global variables to control script execution, headless mode, and auto-start on system boot
running = True
capture_interval = 5  # Default capture interval in seconds
headless_mode = False  # Default headless mode
auto_start_enabled = False  # Default auto-start on system boot

# Additional variable to control manual capture triggering
manual_capture = False

# Function to retrieve websites from a text file
def retrieve_websites():
    with open("websites.txt", "r") as file:
        return file.read().splitlines()

# Function to capture OTP and send to Telegram
def capture_otp():
    websites = retrieve_websites()

    while running:
        if manual_capture:  # Only capture if manual triggering is enabled
            for website in websites:
                try:
                    otp = scrape_website(website)
                    if otp:
                        send_otp_telegram(otp)
                except Exception as e:
                    print(f"Error capturing OTP from {website}: {e}")

            time.sleep(capture_interval)
        else:
            time.sleep(1)  # Wait to avoid unnecessary CPU usage when not capturing

# Function to scrape website for OTP using Selenium
def scrape_website(website):
    try:
        options = Options()
        options.headless = headless_mode  # Set headless mode based on the global variable
        driver = webdriver.Firefox(options=options)

        # Adding more detailed logging
        logging.info(f"Opening {website} for OTP capture...")
        driver.get(website)

        # Example: Interacting with a login form (modify based on actual website structure)
        username_input = driver.find_element_by_name('username')
        password_input = driver.find_element_by_name('password')

        # Example: Providing login credentials (modify based on actual credentials)
        username_input.send_keys('your_username')
        password_input.send_keys('your_password')
        password_input.send_keys(Keys.RETURN)

        # Example: Wait for the page to load after login (modify based on actual website behavior)
        WebDriverWait(driver, 10).until(EC.title_contains('Dashboard'))

        # Example: Extracting OTP from the loaded page (modify based on actual HTML structure)
        otp = extract_otp_from_response(driver.page_source)

        driver.quit()  # Close the browser window

        if otp:
            logging.info(f"Captured OTP from {website}: {otp}")
        else:
            logging.info(f"No OTP found on {website}.")

        return otp
    except Exception as e:
        print(f"Error capturing OTP from {website}: {e}")
        logging.error(f"Error capturing OTP from {website}: {e}")
        return None

# Function to extract OTP from the HTML response using BeautifulSoup
def extract_otp_from_response(response_text):
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        # Adjust based on actual HTML structure where OTP is located
        otp_element = soup.find('span', class_='otp')
        otp = otp_element.text.strip() if otp_element else None
        return otp
    except Exception as e:
        print(f"Error extracting OTP: {e}")
        logging.error(f"Error extracting OTP: {e}")
        return None

# Function to send OTP to Telegram
def send_otp_telegram(otp):
    bot.send_message(telegram_user_id, f"Received OTP: {otp}")

# Logging configuration
logging.basicConfig(filename='script_log.txt', level=logging.INFO)

# Menu functions...

def main_menu():
    global manual_capture  # Use the global variable to control manual capture triggering
    print("1. Change contents of websites.txt")
    print("2. Run Script")
    print("3. View Current Websites")
    print("4. Set Capture Interval")
    print("5. Stop Script")
    print("6. Display Last Captured OTP")
    print("7. Toggle Headless Mode")
    print("8. Pause/Resume Script")
    print("9. Toggle Auto-Start on System Boot")
    print("10. Trigger Manual Capture")
    print("11. Exit Script")
    choice = input("Enter your choice: ")

    if choice == "1":
        change_websites_file()
    elif choice == "2":
        run_script()
    elif choice == "3":
        view_current_websites()
    elif choice == "4":
        set_capture_interval()
    elif choice == "5":
        stop_script()
    elif choice == "6":
        display_last_otp()
    elif choice == "7":
        toggle_headless_mode()
    elif choice == "8":
        pause_resume_script()
    elif choice == "9":
        toggle_auto_start()
    elif choice == "10":
        trigger_manual_capture()
    elif choice == "11":
        exit_script()
    else:
        print("Invalid choice.")

def change_websites_file():
    new_websites = []
    while True:
        website = input("Enter website URL (or 'done' to finish): ")
        if website.lower() == 'done':
            break
        else:
            new_websites.append(website)
    with open("websites.txt", "w") as file:
        for website in new_websites:
            file.write(website + "\n")
    print("Contents of websites.txt updated successfully.")

def run_script():
    global manual_capture  # Use the global variable to control manual capture triggering
    manual_capture = False  # Reset manual capture flag before starting the script
    print("Running script in the background...")
    otp_thread = threading.Thread(target=capture_otp)
    otp_thread.start()
    print("Script is running. Press Ctrl+C to stop.")

def view_current_websites():
    websites = retrieve_websites()
    print("Current Websites:")
    for idx, website in enumerate(websites, start=1):
        print(f"{idx}. {website}")

def set_capture_interval():
    global capture_interval
    new_interval = input("Enter capture interval in seconds (or press Enter to keep current): ")
    if new_interval:
        try:
            capture_interval = int(new_interval)
            print(f"Capture interval set to {capture_interval} seconds.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def stop_script():
    global running
    running = False
    print("Stopping script. Press Enter to return to the main menu.")

def display_last_otp():
    # Add logic to retrieve and display the last captured OTP
    print("Last Captured OTP: <OTP>")
    print("Timestamp: <Timestamp>")

def toggle_headless_mode():
    global headless_mode
    headless_mode = not headless_mode
    mode_status = "enabled" if headless_mode else "disabled"
    print(f"Headless mode is now {mode_status}.")

def pause_resume_script():
    global running
    running = not running
    status = "Resumed" if running else "Paused"
    print(f"Script is {status}.")

def toggle_auto_start():
    global auto_start_enabled
    auto_start_enabled = not auto_start_enabled
    status = "enabled" if auto_start_enabled else "disabled"
    print(f"Auto-Start on System Boot is now {status}.")

def trigger_manual_capture():
    global manual_capture
    manual_capture = True
    print("Manual capture triggered.")

def exit_script():
    global running
    running = False
    print("Exiting script. Goodbye!")
    # You might want to add any cleanup logic or save state before exiting

if __name__ == "__main__":
    while True:
        main_menu()

