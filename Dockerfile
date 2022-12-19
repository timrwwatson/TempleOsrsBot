FROM python:3.11.1

WORKDIR /templeosrs

COPY requirements.txt .

RUN pip install -r requirements

COPY src/ .

CMD [ "python", "./bot.py"]