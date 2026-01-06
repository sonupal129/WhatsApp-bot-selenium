import time
import os
import logging
import openpyxl as excel
import json
from datetime import date
from playwright.sync_api import sync_playwright
from messages import get_all_message_templates
import random
from datetime import datetime


# ---------------- CONFIG ----------------
WHATSAPP_URL = "https://web.whatsapp.com"
ATTACHMENT_DIR = "attachments"
ANTI_BAN_DELAY = 15  # seconds
USER_DATA_DIR = "whatsapp-user-data"
DAILY_SEND_LIMIT = 50   # change as needed (start low!)
DAILY_LIMIT_FILE = "daily_limit.json"
# --------------------------------------

# -------- HUMAN-LIKE DELAYS --------
TYPING_DELAY_RANGE = (30, 90)        # ms per character
SHORT_PAUSE_RANGE = (0.3, 0.9)       # seconds
ACTION_PAUSE_RANGE = (1.0, 2.5)      # seconds
BETWEEN_CONTACTS_RANGE = (12, 25)    # seconds
# ----------------------------------


# ---------------- LOGGING (TERMINAL ONLY) ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
# --------------------------------------------------------


def readSheet(fileName):
    logging.info("Reading contacts sheet")

    wb = excel.load_workbook(fileName)
    sheet = wb.worksheets[0]

    headers = [
        cell.value.lower().replace(" ", "_")
        for cell in next(sheet.iter_rows())
    ]

    data = []

    for idx, row in enumerate(sheet.iter_rows(min_row=2), start=2):
        values = [cell.value for cell in row]

        if all(value is None for value in values):
            continue

        row_dict = dict(zip(headers, values))

        phone = row_dict.get("phone")
        if phone is None or str(phone).strip() == "":
            continue

        # Attach row number for write-back
        row_dict["_row"] = idx

        data.append(row_dict)

    logging.info(f"Loaded {len(data)} total rows")
    return data


def get_message(**kwargs):
    templates = get_all_message_templates()
    template = templates.get(
        kwargs.get("template_name"),
        templates["LAVANYA_ENGLISH"]
    )
    return template.format(**kwargs)


def get_attachments():
    if not os.path.exists(ATTACHMENT_DIR):
        logging.info("No attachment directory found")
        return []

    files = [
        os.path.join(ATTACHMENT_DIR, f)
        for f in os.listdir(ATTACHMENT_DIR)
        if os.path.isfile(os.path.join(ATTACHMENT_DIR, f))
    ]

    logging.info(f"Found {len(files)} attachment files")
    return files

def load_daily_limit():
    today = date.today().isoformat()

    if not os.path.exists(DAILY_LIMIT_FILE):
        return {"date": today, "sent_count": 0}

    with open(DAILY_LIMIT_FILE, "r") as f:
        data = json.load(f)

    # Reset if date changed
    if data.get("date") != today:
        return {"date": today, "sent_count": 0}

    return data


def save_daily_limit(data):
    with open(DAILY_LIMIT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def random_sleep(min_sec, max_sec):
    delay = round(random.uniform(min_sec, max_sec), 2)
    logging.info(f"Sleeping for {delay}s")
    time.sleep(delay)


def random_typing_delay():
    return random.randint(*TYPING_DELAY_RANGE)

def ensure_status_columns(sheet):
    headers = [cell.value.lower() for cell in sheet[1]]

    if "status" not in headers:
        sheet.cell(row=1, column=len(headers) + 1).value = "status"
        headers.append("status")

    if "sent_at" not in headers:
        sheet.cell(row=1, column=len(headers) + 1).value = "sent_at"

    return headers


def update_excel_status(
    workbook_path,
    row_number,
    status,
    timestamp=True
):
    wb = excel.load_workbook(workbook_path)
    sheet = wb.worksheets[0]

    headers = ensure_status_columns(sheet)
    header_map = {h: i + 1 for i, h in enumerate(headers)}

    sheet.cell(
        row=row_number,
        column=header_map["status"]
    ).value = status

    if timestamp:
        sheet.cell(
            row=row_number,
            column=header_map["sent_at"]
        ).value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    wb.save(workbook_path)

def main():
    contacts = readSheet("contacts.xlsx")

    daily_data = load_daily_limit()
    logging.info(
        f"Daily limit status: {daily_data['sent_count']} / {DAILY_SEND_LIMIT}"
    )

    with sync_playwright() as p:
        logging.info("Launching WhatsApp with persistent session")

        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"]
        )

        page = browser.new_page()
        page.goto(WHATSAPP_URL, timeout=60000)

        # ---------- FIRST LOGIN ----------
        if not os.path.exists(USER_DATA_DIR):
            logging.info("Waiting for WhatsApp QR login...")
            page.wait_for_selector(
                'div[contenteditable="true"][data-tab="3"]',
                timeout=0
            )
            logging.info("WhatsApp login successful and session stored")

        logging.info("WhatsApp ready. Starting message loop")

        failed = []

        for contact in contacts:
            phone = str(contact["phone"])
            name = contact.get("name", "")

            if daily_data["sent_count"] >= DAILY_SEND_LIMIT:
                logging.warning("Daily send limit reached. Stopping script.")
                break

            logging.info(f"Processing contact: {phone} | {name}")

            try:
                # -------- SEARCH CONTACT --------
                search_box = page.locator(
                    'div[contenteditable="true"][data-tab="3"]'
                )
                search_box.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(phone, delay=random_typing_delay())
                random_sleep(*SHORT_PAUSE_RANGE)
                page.keyboard.press("Enter")

                # -------- WAIT FOR CHAT --------
                page.wait_for_selector(
                    'div[contenteditable="true"][data-tab="10"]',
                    timeout=15000
                )

                # -------- SEND MESSAGE + PASTE ATTACHMENTS --------
                message_box = page.locator(
                    'div[contenteditable="true"][data-tab="10"]'
                )
                message_box.click()

                # Optional quick reply / command
                page.keyboard.type("/newCustomer", delay=random_typing_delay())
                random_sleep(*SHORT_PAUSE_RANGE)
                page.keyboard.press("Tab")
                random_sleep(*SHORT_PAUSE_RANGE)
                page.keyboard.press("Enter")
                random_sleep(*SHORT_PAUSE_RANGE)

                # Paste clipboard content (files must already be copied)
                logging.info("Pasting clipboard content")
                page.keyboard.press("Control+V")

                time.sleep(5)  # Wait for preview
                page.keyboard.press("Enter")

                daily_data["sent_count"] += 1
                save_daily_limit(daily_data)

                logging.info(
                    f"SUCCESS: {phone} | Daily count: {daily_data['sent_count']} / {DAILY_SEND_LIMIT}"
                )
                random_sleep(*BETWEEN_CONTACTS_RANGE)

            except Exception as e:
                logging.error(f"FAILED for {phone}: {e}")
                failed.append(phone)

        logging.info(f"Process completed. Failed contacts: {failed}")
        browser.close()


if __name__ == "__main__":
    main()
