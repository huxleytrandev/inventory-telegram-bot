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
    cell = sheet.find(product_name)
    if cell is None:
        return None
    return cell.row

def get_current_quantity(row):
    return sheet.cell(row, 2).value     #sheet.cell(row, collumn)

def update_quantity(row, new_quantity):
    sheet.update_cell(row, 2, new_quantity)

def get_all_products():
    return sheet.get_all_records()

def create_new_product(product_name, quantity):
    sheet.append_row([f"{product_name}", quantity])
