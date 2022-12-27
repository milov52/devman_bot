Скрипт представляет из себя помощник для студента платформы Devman. Позволяет получать информацию о проверке своих работ
путем отправки сообщений в телеграмм
Для работы используется 2 бота - первый используется для вывода сообщений о проверках, второй о логах работы

Для запуска скрипта

Скачайте код:
```
git clone https://github.com/milov52/devman_bot.git
```

Перейдите в каталог проекта:
```
cd devman_bot
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```
pip install -r requirements.txt
```

Определите переменные окружения `API_KEY` (можно получить из личного кабинета учебного портала Devmnan),
`TOKEN` (токен чат бота, который будет отправлять сообщения), `CHAT_ID` (id вашего чата, можно получить через бота @userinfobot)
Создать файл `.env` в каталоге и добавьте туда значения для данных переменных:
Пример:
```
DEVMAN_API_KEY=123
TG_TOKEN=6699
TG_CHAT_ID=848
TG_LOGGER_TOKEN=333 
```

Для запуска скрипта указать команду
```sh
python3 devman_bot.py
```
