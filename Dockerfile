FROM python:3.12-slim

WORKDIR /app
COPY bot/ bot/

CMD ["python", "-u", "-m", "bot"]
