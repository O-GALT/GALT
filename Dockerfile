FROM python:3.11-slim

WORKDIR app/

COPY . .

RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "-r", "requirements.txt"]
#RUN ["python", "manage.py", "makemigrations"]

EXPOSE 8000