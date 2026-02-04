FROM python:3.x-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.x-slim
COPY --from=builder /root/.local /root/.local

COPY requirements.txt
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
