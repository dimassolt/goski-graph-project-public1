FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "fuseki_client_api:app", "--host", "0.0.0.0", "--port", "8001"]