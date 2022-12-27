import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

LONG_POOLING_URL = "https://dvmn.org/api/long_polling/"

logger = logging.getLogger('Logger')
class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)

def get_answer(attempt):
    lesson_title = attempt['lesson_title']
    lesson_url = attempt['lesson_url']
    check_result = 'К сожалению, в работе нашлись ошибки'
    if not attempt['is_negative']:
        check_result = 'Преподавателю все понравилось, можете приступать к след. уроку'

    return f'У вас проверили работу "{lesson_title}"\n{lesson_url}\n\n{check_result}'


def main():
    api_key = os.getenv("DEVMAN_API_KEY")
    token = os.getenv("TG_TOKEN")
    token_logger = os.getenv("TG_LOGGER_TOKEN")

    chat_id = os.getenv("TG_CHAT_ID")

    headers = {
        "Authorization": f"Token {api_key}",
    }

    timestamp = ''

    bot = telegram.Bot(token=token)
    bot_logger = telegram.Bot(token=token_logger)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(bot_logger, chat_id))

    logger.info('bot started')
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
                bot.send_message(chat_id=chat_id, text=get_answer(attempt[0]))
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            logger.error('Бот упал с ошибкой')
            logger.error(err, exc_info=True)
            time.sleep(30)
        except requests.exceptions.HTTPError as err:
            logger.error('Бот упал с ошибкой')
            logger.error(err, exc_info=True)

if __name__ == '__main__':
    load_dotenv()
    main()
