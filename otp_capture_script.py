import time
import random
import telebot
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Telegram bot
bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(bot_token)

# Global variables to control script execution, headless mode, and auto-start on system boot
running = True
capture_interval = 5  # Default capture interval in seconds
headless_mode = False  # Default headless mode
auto_start_enabled = False  # Default auto-start on system boot

# Function to retrieve websites from a text file
def retrieve_websites():
    with open("websites.txt", "r") as file:
        return file.read().splitlines()

# Function to capture OTP and send to Telegram
def capture_otp():
    options = webdriver.FirefoxOptions()
    if headless_mode:
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    websites = retrieve_websites()

    while running:
        for website in websites:
            driver.get(website)
            # Add OTP detection logic here
            try:
                otp_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "otp"))
                )
                otp = otp_element.text.strip()
                if otp:
                    send_otp_telegram(otp)
            except:
                pass
            time.sleep(capture_interval)

# Function to send OTP to Telegram
def send_otp_telegram(otp):
    bot.send_message("YOUR_TELEGRAM_USER_ID", f"Received OTP: {otp}")  # Replace with your actual user ID

# Menu to change websites.txt, run script, view websites, set interval, stop script, display last OTP, toggle headless mode, pause/resume script, and auto-start on system boot
def main_menu():
    print("1. Change contents of websites.txt")
    print("2. Run Script")
    print("3. View Current Websites")
    print("4. Set Capture Interval")
    print("5. Stop Script")
    print("6. Display Last Captured OTP")
    print("7. Toggle Headless Mode")
    print("8. Pause/Resume Script")
    print("9. Toggle Auto-Start on System Boot")
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
    else:
        print("Invalid choice.")

# Function to change contents of websites.txt
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

# Function to run the script in the background
def run_script():
    print("Running script in the background...")
    otp_thread = threading.Thread(target=capture_otp)
    otp_thread.start()
    print("Script is running. Press Ctrl+C to stop.")

# Function to view current websites
def view_current_websites():
    websites = retrieve_websites()
    print("Current Websites:")
    for idx, website in enumerate(websites, start=1):
        print(f"{idx}. {website}")

# Function to set capture interval
def set_capture_interval():
    global capture_interval
    new_interval = input("Enter capture interval in seconds: ")
    try:
        capture_interval = int(new_interval)
        print(f"Capture interval set to {capture_interval} seconds.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Function to stop the script
def stop_script():
    global running
    running = False
    print("Stopping script. Press Enter to return to the main menu.")

# Function to display the last captured OTP
def display_last_otp():
    # Add logic to retrieve and display the last captured OTP
    print("Last Captured OTP: <OTP>")
    print("Timestamp: <Timestamp>")

# Function to toggle headless mode
def toggle_headless_mode():
    global headless_mode
    headless_mode = not headless_mode
    mode_status = "enabled" if headless_mode else "disabled"
    print(f"Headless mode is now {mode_status}.")

# Function to pause or resume the script
def pause_resume_script():
    global running
    running = not running
    status = "Resumed" if running else "Paused"
    print(f"Script is {status}.")

# Function to toggle auto-start on system boot
def toggle_auto_start():
    global auto_start_enabled
    auto_start_enabled = not auto_start_enabled
    status = "enabled" if auto_start_enabled else "disabled"
    print(f"Auto-Start on System Boot is now {status}.")

# Main program
if __name__ == "__main__":
    main_menu()
