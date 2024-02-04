FROM python:3.8

WORKDIR /app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY . /app

EXPOSE 5000

CMD ["python", "server.py"]
