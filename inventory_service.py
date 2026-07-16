from google_sheet_service import update_quantity
from google_sheet_service import get_all_products
from google_sheet_service import find_product_row
from google_sheet_service import create_new_product

def issue_stock(product_name,current_quantity, handle_quantity, row_product):
    if handle_quantity > current_quantity:
        reply = f"❌ Không đủ hàng! Kho chỉ còn {current_quantity}, không thể xuất {handle_quantity}"
        return reply
    else:
        new_quantity = current_quantity - handle_quantity
        update_quantity(row_product, new_quantity)
        reply = f"✅ Đã xuất {handle_quantity} {product_name}. Còn lại: {new_quantity}"
        return reply

def receive_stock(product_name,current_quantity, handle_quantity, row_product):
    new_quantity = current_quantity + handle_quantity
    update_quantity(row_product, new_quantity)
    reply = f"✅ Đã nhập {handle_quantity} {product_name}. Tổng cộng: {new_quantity}"
    return reply

def is_product_exist(product_name):
    if find_product_row(product_name) is None:
        return False
    return True

def add_new_product(product_name, quantity):
    if is_product_exist(product_name):
        reply = "✅ Sản phẩm đã tồn tại trong kho, bạn hãy thêm số lượng bằng lệnh '/nhap'"
        return reply
    new_product = create_new_product(product_name, quantity)
    reply = f"✅ Đã thêm hàng {product_name}. Số lượng: {quantity}"
    return reply
