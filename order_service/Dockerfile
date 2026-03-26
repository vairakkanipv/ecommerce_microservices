FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install django djangorestframework pika requests
RUN python manage.py migrate
EXPOSE 8002
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]