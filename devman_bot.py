import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

LONG_POOLING_URL = "https://dvmn.org/api/long_polling/"


def get_answer(attempt):
    lesson_title = attempt['lesson_title']
    lesson_url = attempt['lesson_url']
    check_result = 'К сожалению, в работе нашлись ошибки'
    if not attempt['is_negative']:
        check_result = 'Преподавателю все понравилось, можете приступать к след. уроку'

    return f'У вас проверили работу "{lesson_title}"\n{lesson_url}\n\n{check_result}'


def main():
    API_KEY = os.getenv("DEVMAN_API_KEY")
    TOKEN = os.getenv("TG_TOKEN")
    CHAT_ID = os.getenv("TG_CHAT_ID")

    headers = {
        "Authorization": f"Token {API_KEY}",
    }

    timestamp = ''
    logging.debug('bot started')
    bot = telegram.Bot(token=TOKEN)
    while True:
        try:
            payloads = {"timestamp": timestamp}
            reviews = requests.get(LONG_POOLING_URL, headers=headers, params=payloads)
            reviews.raise_for_status()
            reviews = reviews.json()

            if reviews["status"] == 'timeout':
                timestamp = reviews["timestamp_to_request"]
            else:
                timestamp = reviews['last_attempt_timestamp']

                attempt = reviews['new_attempts']
                bot.send_message(chat_id=CHAT_ID, text=get_answer(attempt[0]))
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Connection error')
            time.sleep(30)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    main()
