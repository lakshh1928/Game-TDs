FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local

COPY requirements.txt .
COPY /frontend ./frontend
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
