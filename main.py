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

offset = None

while True:
    result = get_updates(TELEGRAM_TOKEN, offset=offset)
    
    if result["result"]:
        for update in result["result"]:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            print(f"Nhận lệnh: {text} từ chat_id: {chat_id}")
            
            offset = update["update_id"] + 1  # cập nhật offset ngay sau mỗi tin nhắn xử lý
    
    time.sleep(1)  # nghỉ 1 giây trước khi hỏi lại (tránh gọi API dồn dập)