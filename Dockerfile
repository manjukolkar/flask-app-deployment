FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install gunicorn flask psycopg2-binary
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
