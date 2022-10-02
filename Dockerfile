FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TZ="Europe/Amsterdam"
RUN python3 emojis.py > emojis

CMD ["python3", "main.py"]