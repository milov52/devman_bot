FROM python:3.7

WORKDIR /devman_bot


COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY devman_bot.py .
CMD ["python3", "devman_bot.py"]

