FROM python:3.7

WORKDIR /devman_bot

COPY requirements.txt .
RUN pip install -r ./requirements.txt

ENV DEVMAN_API_KEY=41242b4f1569d9cc6995fcdd3ca8cd3af9675a58
ENV TG_TOKEN=5748736583:AAFlSbmQ8cf3tGyiMb1a3GCYfJjkaNhBEjk
ENV TG_LOGGER_TOKEN=5916770125:AAFLtIi8ssa2BEEDz8GIYHWZRQWaPabiqAg
ENV TG_CHAT_ID=130324158

COPY devman_bot.py .
CMD ["python3", "devman_bot.py"]
