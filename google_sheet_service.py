import gspread
from google.oauth2.service_account import Credentials
from config import CREDENTIALS_FILE, SHEET_ID

# Phạm vi quyền truy cập cần thiết
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Xác thực bằng Service Account
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Mở sheet theo ID, lấy đúng sheet đầu tiên (worksheet)
sheet = client.open_by_key(SHEET_ID).sheet1

def find_product_row(product_name):
    all_records = get_all_products()
    normalized_target = product_name.strip().lower()

    for index, record in enumerate(all_records):
        normalized_existing = record["Product Name"].strip().lower()
        if normalized_existing == normalized_target:
            number_row_in_sheet = index + 2
            return number_row_in_sheet
    return None

def get_current_quantity(row):
    return sheet.cell(row, 2).value     #sheet.cell(row, collumn)

def update_quantity(row, new_quantity):
    sheet.update_cell(row, 2, new_quantity)

def get_all_products():
    return sheet.get_all_records()

def create_new_product(product_name, quantity):
    sheet.append_row([f"{product_name}", quantity])
    # Lấy số hàng vừa thêm (hàng cuối cùng hiện có)
    new_row = len(sheet.get_all_values())
    
    # Ép định dạng: không đậm, có viền
    sheet.format(f"A{new_row}:B{new_row}", {
        "textFormat": {"bold": False},
        "borders": {
            "top": {"style": "SOLID"},
            "right": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "bottom": {"style": "SOLID"}
        }
    })
