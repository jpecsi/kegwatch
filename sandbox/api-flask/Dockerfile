FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY api.py ./
RUN pip install Flask flask-cors requests waitress mysql-connector-python
CMD ["python3", "./api.py"]
