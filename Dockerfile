FROM python:3.11.1

WORKDIR /templeosrs

COPY /container/requirements.txt .

RUN pip install -r requirements.txt

COPY /container/ .

CMD [ "python", "src/bot.py"]