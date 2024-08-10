FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY server.py ./
COPY support.py ./
COPY kegs.py ./
COPY pours.py ./
RUN pip install Flask flask-cors requests waitress mysql-connector-python python-dateutil
CMD ["python3", "./server.py"]
