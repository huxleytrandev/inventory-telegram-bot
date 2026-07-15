from google_sheet_service import update_quantity

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