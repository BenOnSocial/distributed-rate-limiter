FROM dhi.io/python:3-debian12-dev AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM dhi.io/python:3-debian12
WORKDIR /app

ENV PYTHONPATH=/usr/local/lib/python3.14/site-packages

COPY --from=builder /install /usr/local

COPY . .

USER nonroot

CMD ["python", "app.py"]
