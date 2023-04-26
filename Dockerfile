FROM python:3.10.11-bullseye
WORKDIR /portalssma

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]

EXPOSE 8000