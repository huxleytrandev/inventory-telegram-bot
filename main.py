import requests
import gspread
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import time

load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
TELEGRAM_URL_BASE = os.getenv("TELEGRAM_URL_BASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID_BOT = os.getenv("TELEGRAM_CHAT_ID_BOT")

# Phạm vi quyền truy cập cần thiết
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Xác thực bằng Service Account
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Mở sheet theo ID, lấy đúng sheet đầu tiên (worksheet)
sheet = client.open_by_key(SHEET_ID).sheet1

# Đọc toàn bộ dữ liệu dưới dạng list of dict (tự động lấy hàng đầu làm key)
data = sheet.get_all_records()

def get_updates(token, offset=None):
    url = f"{TELEGRAM_URL_BASE}{token}/getUpdates"
    params = {
        "timeout": 30
    }
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json()

def parse_command(text):
    parts = text.strip().split()        
    # strip(): dùng để loại bỏ khoảng trắng đầu và cuối
    # split(): Tách chuỗi thành danh sách dựa trên khoảng trắng.

    if len(parts) != 3:
        return None
    
    command, product_name, quantity = parts

    # command, product_name, quantity = parts --> unpacking : giải nén danh sách, python sẽ lấy từng phần tử trong parts để gán cho từng biến

    if command != "/xuat" or (not quantity.isdigit()):      # isdigit() -> trả về True nếu chuỗi chỉ gồm các chữ số (0-9) và không rỗng. False nếu có bất kỳ ký tự nào không phải là số.
        return None

    return {
        "product_name": product_name,
        "quantity": int(quantity)
    }

def find_product_row(sheet, product_name):
    cell = sheet.find(product_name)
    if cell is None:
        return None
    return cell.row

def get_current_quantity(sheet, row):
    return sheet.cell(row, 2).value     #sheet.cell(row, collumn)

def update_quantity(sheet, row, new_quantity):
    sheet.update_cell(row, 2, new_quantity)

def send_message_to_user(token, chat_id, text):
    url = f"{TELEGRAM_URL_BASE}{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

offset = None

while True:
    result = get_updates(TELEGRAM_TOKEN, offset=offset)
    
    if result["result"]:
        for update in result["result"]:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            print(f"Nhận lệnh: {text} từ chat_id: {chat_id}")
            
            offset = update["update_id"] + 1 

            command = parse_command(text)

            if command:
                print(f"Lệnh hợp lệ: {command}")
                print(f"Sản phẩm: {command["product_name"]}")
                print(f"Số lượng cần xuất: {command["quantity"]}")
                row_product = find_product_row(sheet,command["product_name"])
                if row_product is None:
                    reply = f"❌ Không tìm thấy sản phẩm '{command['product_name']}' trong kho"
                    send_message_to_user(TELEGRAM_TOKEN, chat_id, reply)
                else:
                    current_quantity = int(get_current_quantity(sheet, row_product))
                    if command["quantity"] > current_quantity:
                        reply = f"❌ Không đủ hàng! Kho chỉ còn {current_quantity}, không thể xuất {command['quantity']}"
                        send_message_to_user(TELEGRAM_TOKEN, chat_id, reply)
                    else:
                        new_quantity = current_quantity - command["quantity"]
                        update_quantity(sheet, row_product, new_quantity)
                        reply = f"✅ Đã xuất {command['quantity']} {command['product_name']}. Còn lại: {new_quantity}"
                        send_message_to_user(TELEGRAM_TOKEN, chat_id, reply)
            else:
                reply = "Không phải lệnh hợp lệ, bỏ qua"
                send_message_to_user(TELEGRAM_TOKEN, chat_id, reply)
    
    time.sleep(1)