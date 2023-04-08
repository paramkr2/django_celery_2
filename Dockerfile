FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR .

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["railway.sh"]
