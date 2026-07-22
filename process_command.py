from config import TELEGRAM_TOKEN
from config import TELEGRAM_CHAT_ID_BOT
from google_sheet_service import sheet
from google_sheet_service import find_product_row
from google_sheet_service import get_current_quantity
from inventory_service import issue_stock
from inventory_service import receive_stock
from inventory_service import add_new_product
from telegram_service import send_message_to_user
def parse_command(text):
    parts = text.strip().split() 

    if len(parts) != 3:
        return None
    
    command, product_name, quantity = parts

    if (command == "/xuat" or command == "/nhap" or command == "/them_hang") and  quantity.isdigit():      # isdigit() -> trả về True nếu chuỗi chỉ gồm các chữ số (0-9) và không rỗng. False nếu có bất kỳ ký tự nào không phải là số.
        return {
            "product_name": product_name,
            "quantity": int(quantity),
            "command": command
        }

    return None

def total_process_command(command, chat_id):
    if command:
        print(f"Lệnh hợp lệ: {command}")
        print(f"Sản phẩm: {command["product_name"]}")
        print(f"Số lượng cần xử lý: {command["quantity"]}")
        result_process = detail_handle_command(command["command"], command['product_name'], command["quantity"])
        status_code = send_message_to_user(chat_id, result_process)
        return {
            "reply": result_process,
            "status_code": status_code
        }
    else:
        reply = "❌Không phải lệnh hợp lệ."
        status_code = send_message_to_user(chat_id,reply)
        return {
            "reply": reply,
            "status_code": status_code
        }

def detail_handle_command(command_name, product_name, handle_quantity):
    row_product = find_product_row(product_name)
    if command_name == "/them_hang":
        return add_new_product(product_name, handle_quantity)
    
    if row_product is None:
        reply = f"❌ Không tìm thấy sản phẩm '{product_name}' trong kho"
        return reply

    current_quantity = int(get_current_quantity(row_product))

    if command_name == "/xuat":
        return issue_stock(product_name,current_quantity, handle_quantity, row_product)
    elif command_name == "/nhap":
        return receive_stock(product_name,current_quantity, handle_quantity, row_product)
    