# Note: For proper working of this Script Good and Uninterepted Internet Connection is Required
# Keep all contacts unique
# Can save contact with their phone Number

# Import required packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import phonenumbers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime, time, os
import openpyxl as excel
import urllib.parse
from messages import get_all_message_templates

# function to read contacts from a text file

print("Fetching contacts details from sheet")
print("..................")

time.sleep(5)

def readSheet(fileName):
    lst = []
    file = excel.load_workbook(fileName)
    sheet = file.worksheets[0]
    bypass_title = False

    columns_name = [columnname.value.lower().replace(" ", "_") for columnname in next(sheet.iter_rows())]

    for row in sheet.iter_rows():
        if not bypass_title:
            bypass_title = True
            continue
        row_values = [row_item.value for row_item in row]
        lst.append(dict(zip(columns_name, row_values)))
        
    return lst

print("Validating Contact details............")

sheet_data = readSheet("contacts.xlsx")


def validateContacts():
    return sheet_data

# Not tested on Broadcast
contacts = validateContacts()

# Driver to open a browser
# ---------- CHROME OPTIONS ----------
chrome_options = Options()

# Persist WhatsApp session
SESSION_DIR = os.path.abspath("whatsapp-session")
chrome_options.add_argument(f"--user-data-dir={SESSION_DIR}")

# Recommended stability flags
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")

# ---------- AUTO DRIVER SETUP ----------
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)

attachment_files = [
    "/home/sonu/Documents/SONU_LEARN/whatsapp_bot/WhatsApp-bot-selenium/Lavanya Enterprises.png",
    "/home/sonu/Documents/SONU_LEARN/whatsapp_bot/WhatsApp-bot-selenium/HMAPISKL0001_02_DTL.png",
    "/home/sonu/Documents/SONU_LEARN/whatsapp_bot/WhatsApp-bot-selenium/HMAPISKL0002_01_DTL.png",
    "/home/sonu/Documents/SONU_LEARN/whatsapp_bot/WhatsApp-bot-selenium/HMAPISKL0003_01_DTL.png",
    "/home/sonu/Documents/SONU_LEARN/whatsapp_bot/WhatsApp-bot-selenium/HMAPISKL0004_01_DTL.png",
    
]

pdf_catalog = "/home/sonu/Documents/SONU_LEARN/whatsapp_bot/WhatsApp-bot-selenium/catalog.pdf",

# #link to open a site
whatsapp_url = f"https://web.whatsapp.com"
driver.get(whatsapp_url)
time.sleep(60)

def get_message(**kwargs):
    all_templates = get_all_message_templates()
    if  kwargs.get("template_name"):
        message = all_templates[kwargs["template_name"]]
    else:
        message = all_templates["LAVANYA_ENGLISH"]
    return message.format(**kwargs)



message_not_sent = []

for contact in contacts:
    phone_number = contact["phone"]
    print(contact)
    try:
        time.sleep(20)
        # Find the search box and search for the contact
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(phone_number)
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)  # Wait for chat to open

        # Find the message input box and send the message
        print("Writing Message.........")
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.click()
        # message_box.send_keys(LAVANYA_ENGLISH)

        # Splitting the message by lines and sending each line with Shift+Enter for a new line
        for line in get_message(**contact).splitlines():
            message_box.send_keys(line)
            message_box.send_keys(Keys.SHIFT + Keys.ENTER)
        message_box.send_keys(Keys.RETURN)  # Send the message

        time.sleep(4)  # Wait a bit for the message to be sent

        if attachment_files:
            existing_files = [f for f in attachment_files if os.path.exists(f)]
            if existing_files:
                attach_button = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable(
                                        (By.XPATH, '//button[@aria-label="Attach"]')
                                    )
                                )
                attach_button.click()
                time.sleep(2)  # Wait for the attach menu to open

                # Wait for file input
                file_input = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//input[@type="file"]')
                    )
                )

                # Send files (images/videos)
                file_input.send_keys("\n".join(existing_files))

                time.sleep(10)  # Allow upload preview to load

        # Send message
        send_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//button[@aria-label="Send"] | //span[@data-icon="send"]')
                        )
                    )
        send_button.click()
        print("Message sent to the user")
    except Exception as e:
            message_not_sent.append(phone_number)
            print(f"An error occurred with {contact}: {e}")

    # Optional: Send catalog link after sending attachments
    catalog_link = "https://wa.me/c/918882897947"  # Replace with your actual link
    try:
        time.sleep(2)  # Brief wait before sending the next message
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.click()
        message_box.send_keys("Check out our full catalog here:")
        message_box.send_keys(Keys.SHIFT + Keys.ENTER)
        message_box.send_keys(catalog_link)
        message_box.send_keys(Keys.RETURN)
        print("Catalog link sent.")
    except Exception as e:
        print(f"Could not send catalog link: {e}")

time.sleep(20)

print("This is list of peoples to who messages could not sent")
print(message_not_sent)

driver.quit()