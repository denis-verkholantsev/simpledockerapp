FROM python:3.10

RUN pip install virtualenv

WORKDIR /app
COPY . .

RUN virtualenv .venv
RUN /app/.venv/bin/pip install --upgrade pip
RUN /app/.venv/bin/pip install -r requirements.txt

CMD ["/app/.venv/bin/python", "app.py"]
