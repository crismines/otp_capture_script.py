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

# Function to retrieve websites from a text file
def retrieve_websites():
    with open("websites.txt", "r") as file:
        return file.read().splitlines()

# Function to capture OTP and send to Telegram
def capture_otp():
    driver = webdriver.Firefox()
    websites = retrieve_websites()

    while True:
        for website in websites:
            driver.get(website)
            # Add OTP detection logic here
            try:
                # Example: Find OTP element by its class name
                otp_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "otp"))
                )
                otp = otp_element.text.strip()
                if otp:
                    send_otp_telegram(otp)
            except:
                pass
            time.sleep(5)  # Adjust sleep time as needed

# Function to send OTP to Telegram
def send_otp_telegram(otp):
    bot.send_message("YOUR_TELEGRAM_USER_ID", f"Received OTP: {otp}")  # Replace with your actual user ID

# Menu to change websites.txt and run script
def main_menu():
    print("1. Change contents of websites.txt")
    print("2. Run Script")
    choice = input("Enter your choice: ")
    if choice == "1":
        change_websites_file()
    elif choice == "2":
        run_script()
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

# Main program
if __name__ == "__main__":
    main_menu()
