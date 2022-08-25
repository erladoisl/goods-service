import requests
try:
    from config import token
except:
    from modules.config import token


def telegram_bot_send_text(bot_message, chat_id):
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)

    return response.json()


if __name__ == '__main__':
    test = telegram_bot_send_text("Testing Telegram bot", str(1875768814))
    print(test)
