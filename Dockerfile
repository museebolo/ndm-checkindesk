FROM python:3.12-slim

ARG YEAR
ENV YEAR=${YEAR}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATA_PATH=/data/state.json \
    PORT=8080

WORKDIR /app

COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install --no-cache-dir .

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8080
VOLUME ["/data", "/config"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
