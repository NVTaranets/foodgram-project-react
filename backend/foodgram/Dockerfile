FROM python:3.7-slim
RUN pip install --upgrade pip

WORKDIR /app
COPY ../../requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir
COPY . ./
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
RUN python manage.py collectstatic --no-input
