import os

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

LONG_POOLING_URL = "https://dvmn.org/api/long_polling/"
API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_answer(response):
    lesson_title = response['lesson_title']
    lesson_url = response['lesson_url']
    check_result = 'К сожалению, в работе нашлись ошибки'
    if not response['is_negative']:
        check_result = 'Преподавателю все понравилось, можете приступать к след. уроку'

    return f'У вас проверили работу "{lesson_title}"\n{lesson_url}\n\n{check_result}'

def main():
    headers = {
        "Authorization": f"Token {API_KEY}",
    }

    timestamp = ''
    bot = telegram.Bot(token=TOKEN)
    while True:
        try:
            payloads = {"timestamp": timestamp}
            response = requests.get(LONG_POOLING_URL, headers=headers, params=payloads)
            response.raise_for_status()
            response = response.json()

            if response["status"] == 'timeout':
                timestamp = response["timestamp_to_request"]
            else:
                response = response['new_attempts']
                timestamp = response[0]['timestamp']
                bot.send_message(chat_id=CHAT_ID, text=get_answer(response[0]))
        except requests.exceptions.ReadTimeout:
            print('Ошибка ожидания timeout')
        except requests.exceptions.ConnectionError:
            print('Connection error')


if __name__ == '__main__':
    main()
