FROM python:3.12-slim AS builder

WORKDIR /app

COPY /backend/requirements.txt ./backend/requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local

COPY /backend/requirements.txt ./backend/requirements.txt
COPY /frontend ./frontend
COPY /backend/app.py ./backend/app.py

EXPOSE 5000

CMD ["python", "app.py"]
