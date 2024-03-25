FROM python:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /app 
COPY requirements.txt requirements.txt
EXPOSE 8000
RUN pip3 install -r requirements.txt