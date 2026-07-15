import time
from google_sheet_service import sheet
from telegram_service import get_updates
from telegram_service import send_message_to_user
from process_command import parse_command
from process_command import total_process_command


offset = None

while True:
    result = get_updates(offset=offset)
    
    if result["result"]:
        for update in result["result"]:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            print(f"Nhận lệnh: {text} từ chat_id: {chat_id}")
            
            offset = update["update_id"] + 1 

            command = parse_command(text)
            # print(command)
            result = total_process_command(command)
            if result:
                print(f"{result["reply"]}")
    
    time.sleep(1)