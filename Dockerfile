FROM python:3.9

WORKDIR /app

ENV FLASK_ENV=development
ENV FLASK_APP=app.py

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
