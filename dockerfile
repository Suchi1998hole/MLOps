FROM --platform=linux/amd64 python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY data/ ./data/
COPY src/ ./src/

RUN mkdir -p model
RUN python src/train.py

EXPOSE $PORT

CMD ["sh", "-c", "python src/main.py --server.port $PORT"]